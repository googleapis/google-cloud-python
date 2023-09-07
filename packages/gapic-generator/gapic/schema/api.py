# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module contains the "roll-up" class, :class:`~.API`.
Everything else in the :mod:`~.schema` module is usually accessed
through an :class:`~.API` object.
"""

import collections
import dataclasses
import itertools
import keyword
import os
import sys
from typing import Callable, Container, Dict, FrozenSet, Mapping, Optional, Sequence, Set, Tuple
from types import MappingProxyType

from google.api_core import exceptions
from google.api import http_pb2  # type: ignore
from google.api import resource_pb2  # type: ignore
from google.api import service_pb2  # type: ignore
from google.cloud import extended_operations_pb2 as ex_ops_pb2  # type: ignore
from google.gapic.metadata import gapic_metadata_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import descriptor_pb2  # type: ignore
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import ParseDict
from google.protobuf.descriptor import ServiceDescriptor
import grpc  # type: ignore
from google.protobuf.descriptor_pb2 import MethodDescriptorProto
from google.api import annotations_pb2  # type: ignore
from gapic.schema import metadata
from gapic.schema import mixins
from gapic.schema import wrappers
from gapic.schema import naming as api_naming
from gapic.utils import cached_property
from gapic.utils import nth
from gapic.utils import Options
from gapic.utils import to_snake_case
from gapic.utils import RESERVED_NAMES


TRANSPORT_GRPC = "grpc"
TRANSPORT_GRPC_ASYNC = "grpc-async"
TRANSPORT_REST = "rest"


@dataclasses.dataclass(frozen=True)
class Proto:
    """A representation of a particular proto file within an API."""

    file_pb2: descriptor_pb2.FileDescriptorProto
    services: Mapping[str, wrappers.Service]
    all_messages: Mapping[str, wrappers.MessageType]
    all_enums: Mapping[str, wrappers.EnumType]
    file_to_generate: bool
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )

    def __getattr__(self, name: str):
        return getattr(self.file_pb2, name)

    @classmethod
    def build(
            cls,
            file_descriptor: descriptor_pb2.FileDescriptorProto,
            file_to_generate: bool,
            naming: api_naming.Naming,
            opts: Options = Options(),
            prior_protos: Optional[Mapping[str, 'Proto']] = None,
            load_services: bool = True,
            all_resources: Optional[Mapping[str, wrappers.MessageType]] = None,
    ) -> 'Proto':
        """Build and return a Proto instance.

        Args:
            file_descriptor (~.FileDescriptorProto): The protocol buffer
                object describing the proto file.
            file_to_generate (bool): Whether this is a file which is
                to be directly generated, or a dependency.
            naming (~.Naming): The :class:`~.Naming` instance associated
                with the API.
            prior_protos (~.Proto): Previous, already processed protos.
                These are needed to look up messages in imported protos.
            load_services (bool): Toggle whether the proto file should
                load its services. Not doing so enables a two-pass fix for
                LRO response and metadata types in certain situations.
        """
        return _ProtoBuilder(
            file_descriptor,
            file_to_generate=file_to_generate,
            naming=naming,
            opts=opts,
            prior_protos=prior_protos or {},
            load_services=load_services,
            all_resources=all_resources or {},
        ).proto

    @cached_property
    def enums(self) -> Mapping[str, wrappers.EnumType]:
        """Return top-level enums on the proto."""
        return collections.OrderedDict([
            (k, v) for k, v in self.all_enums.items()
            if not v.meta.address.parent
        ])

    @cached_property
    def messages(self) -> Mapping[str, wrappers.MessageType]:
        """Return top-level messages on the proto."""
        return collections.OrderedDict(
            (k, v) for k, v in self.all_messages.items()
            if not v.meta.address.parent
        )

    @cached_property
    def resource_messages(self) -> Mapping[str, wrappers.MessageType]:
        """Return the file level resources of the proto."""
        file_resource_messages = (
            (res.type, wrappers.CommonResource.build(res).message_type)
            for res in self.file_pb2.options.Extensions[resource_pb2.resource_definition]
        )
        resource_messages = (
            (msg.options.Extensions[resource_pb2.resource].type, msg)
            for msg in self.messages.values()
            if msg.options.Extensions[resource_pb2.resource].type
        )
        return collections.OrderedDict(
            itertools.chain(
                file_resource_messages, resource_messages,
            )
        )

    @property
    def module_name(self) -> str:
        """Return the appropriate module name for this service.

        Returns:
            str: The module name for this service (which is the service
                name in snake case).
        """
        return to_snake_case(self.name.split('/')[-1][:-len('.proto')])

    @cached_property
    def names(self) -> FrozenSet[str]:
        """Return a set of names used by this proto.

        This is used for detecting naming collisions in the module names
        used for imports.
        """
        # Add names of all enums, messages, and fields.
        answer: Set[str] = {e.name for e in self.all_enums.values()}
        for message in self.all_messages.values():
            answer.update(f.name for f in message.fields.values())
            answer.add(message.name)

        # Identify any import module names where the same module name is used
        # from distinct packages.
        modules: Dict[str, Set[str]] = collections.defaultdict(set)
        for m in self.all_messages.values():
            for t in m.recursive_field_types:
                modules[t.ident.module].add(t.ident.package)

        answer.update(
            module_name
            for module_name, packages in modules.items()
            if len(packages) > 1 or module_name in RESERVED_NAMES
        )

        # Return the set of collision names.
        return frozenset(answer)

    @cached_property
    def python_modules(self) -> Sequence[Tuple[str, str]]:
        """Return a sequence of Python modules, for import.

        The results of this method are in alphabetical order (by package,
        then module), and do not contain duplicates.

        Returns:
            Sequence[Tuple[str, str]]: The package and module pair, intended
            for use in a ``from package import module`` type
            of statement.
        """
        self_reference = self.meta.address.python_import

        answer = {
            t.ident.python_import
            for m in self.all_messages.values()
            # Quick check: We do make sure that we are not trying to have
            # a module import itself.
            for t in m.field_types if t.ident.python_import != self_reference
        }

        # Done; return the sorted sequence.
        return tuple(sorted(answer))

    def disambiguate(self, string: str) -> str:
        """Return a disambiguated string for the context of this proto.

        This is used for avoiding naming collisions. Generally, this method
        returns the same string, but it returns a modified version if
        it will cause a naming collision with messages or fields in this proto.
        """
        if string in self.names:
            return self.disambiguate(f'_{string}')
        return string


@dataclasses.dataclass(frozen=True)
class API:
    """A representation of a full API.

    This represents a top-down view of a complete API, as loaded from a
    set of protocol buffer files. Once the descriptors are loaded
    (see :meth:`load`), this object contains every message, method, service,
    and everything else needed to write a client library.

    An instance of this object is made available to every template
    (as ``api``).
    """
    naming: api_naming.Naming
    all_protos: Mapping[str, Proto]
    service_yaml_config: service_pb2.Service
    subpackage_view: Tuple[str, ...] = dataclasses.field(default_factory=tuple)

    @classmethod
    def build(
        cls,
        file_descriptors: Sequence[descriptor_pb2.FileDescriptorProto],
        package: str = '',
        opts: Options = Options(),
        prior_protos: Optional[Mapping[str, 'Proto']] = None,
    ) -> 'API':
        """Build the internal API schema based on the request.

        Args:
            file_descriptors (Sequence[~.FileDescriptorProto]): A list of
                :class:`~.FileDescriptorProto` objects describing the
                API.
            package (str): A protocol buffer package, as a string, for which
                code should be explicitly generated (including subpackages).
                Protos with packages outside this list are considered imports
                rather than explicit targets.
            opts (~.options.Options): CLI options passed to the generator.
            prior_protos (~.Proto): Previous, already processed protos.
                These are needed to look up messages in imported protos.
                Primarily used for testing.
        """
        # Save information about the overall naming for this API.
        naming = api_naming.Naming.build(*filter(
            lambda fd: fd.package.startswith(package),
            file_descriptors,
        ), opts=opts)

        # "metadata", "retry", "timeout", and "request" are reserved words in client methods.
        invalid_module_names = set(keyword.kwlist) | {
            "metadata", "retry", "timeout", "request"}

        def disambiguate_keyword_sanitize_fname(
                full_path: str,
                visited_names: Container[str]) -> str:
            path, fname = os.path.split(full_path)
            name, ext = os.path.splitext(fname)

            # Replace `.` with `_` in the basename as
            # `.` is not a valid character for modules names.
            # See https://peps.python.org/pep-0008/#package-and-module-names
            if "." in name:
                name = name.replace(".", "_")
                full_path = os.path.join(path, name + ext)

            if name in invalid_module_names or full_path in visited_names:
                name += "_"
                full_path = os.path.join(path, name + ext)
                if full_path in visited_names:
                    return disambiguate_keyword_sanitize_fname(full_path, visited_names)

            return full_path

        # Iterate over each FileDescriptorProto and fill out a Proto
        # object describing it, and save these to the instance.
        #
        # The first pass gathers messages and enums but NOT services or methods.
        # This is a workaround for a limitation in protobuf annotations for
        # long running operations: the annotations are strings that reference
        # message types but do not require a proto import.
        # This hack attempts to address a common case where API authors,
        # not wishing to generate an 'unused import' warning,
        # don't import the proto file defining the real response or metadata
        # type into the proto file that defines an LRO.
        # We just load all the APIs types first and then
        # load the services and methods with the full scope of types.
        pre_protos: Dict[str, Proto] = dict(prior_protos or {})
        for fd in file_descriptors:
            fd.name = disambiguate_keyword_sanitize_fname(fd.name, pre_protos)
            pre_protos[fd.name] = Proto.build(
                file_descriptor=fd,
                file_to_generate=fd.package.startswith(package),
                naming=naming,
                opts=opts,
                prior_protos=pre_protos,
                # Ugly, ugly hack.
                load_services=False,
            )

        # A file descriptor's file-level resources are NOT visible to any importers.
        # The only way to make referenced resources visible is to aggregate them at
        # the API level and then pass that around.
        all_file_resources = collections.ChainMap(
            *(proto.resource_messages for proto in pre_protos.values())
        )

        # Second pass uses all the messages and enums defined in the entire API.
        # This allows LRO returning methods to see all the types in the API,
        # bypassing the above missing import problem.
        protos: Dict[str, Proto] = {
            name: Proto.build(
                file_descriptor=proto.file_pb2,
                file_to_generate=proto.file_to_generate,
                naming=naming,
                opts=opts,
                prior_protos=pre_protos,
                all_resources=MappingProxyType(all_file_resources),
            )
            for name, proto in pre_protos.items()
        }

        # Parse the google.api.Service proto from the service_yaml data.
        service_yaml_config = service_pb2.Service()
        ParseDict(
            opts.service_yaml_config,
            service_yaml_config,
            ignore_unknown_fields=True
        )

        # Done; return the API.
        return cls(naming=naming,
                   all_protos=protos,
                   service_yaml_config=service_yaml_config)

    @cached_property
    def enums(self) -> Mapping[str, wrappers.EnumType]:
        """Return a map of all enums available in the API."""
        return collections.ChainMap({},
                                    *[p.all_enums for p in self.protos.values()],
                                    )

    @cached_property
    def messages(self) -> Mapping[str, wrappers.MessageType]:
        """Return a map of all messages available in the API."""
        return collections.ChainMap({},
                                    *[p.all_messages for p in self.protos.values()],
                                    )

    @cached_property
    def top_level_messages(self) -> Mapping[str, wrappers.MessageType]:
        """Return a map of all messages that are NOT nested."""
        return {
            k: v
            for p in self.protos.values()
            for k, v in p.messages.items()
        }

    @cached_property
    def top_level_enums(self) -> Mapping[str, wrappers.EnumType]:
        """Return a map of all messages that are NOT nested."""
        return {
            k: v
            for p in self.protos.values()
            for k, v in p.enums.items()
        }

    @cached_property
    def protos(self) -> Mapping[str, Proto]:
        """Return a map of all protos specific to this API.

        This property excludes imported protos that are dependencies
        of this API but not being directly generated.
        """
        view = self.subpackage_view
        return collections.OrderedDict([
            (k, v) for k, v in self.all_protos.items()
            if v.file_to_generate and
            v.meta.address.subpackage[:len(view)] == view
        ])

    @cached_property
    def services(self) -> Mapping[str, wrappers.Service]:
        """Return a map of all services available in the API."""
        return collections.ChainMap({},
                                    *[p.services for p in self.protos.values()],
                                    )

    @cached_property
    def http_options(self) -> Mapping[str, Sequence[wrappers.HttpRule]]:
        """Return a map of API-wide http rules."""

        def make_http_options(rule: http_pb2.HttpRule
                              ) -> Sequence[wrappers.HttpRule]:
            http_options = [rule] + list(rule.additional_bindings)
            opt_gen = (wrappers.HttpRule.try_parse_http_rule(http_rule)
                       for http_rule in http_options)
            return [rule for rule in opt_gen if rule]

        result: Mapping[str, Sequence[http_pb2.HttpRule]] = {
            rule.selector: make_http_options(rule)
            for rule in self.service_yaml_config.http.rules
        }

        return result

    @cached_property
    def subpackages(self) -> Mapping[str, 'API']:
        """Return a map of all subpackages, if any.

        Each value in the mapping is another API object, but the ``protos``
        property only shows protos belonging to the subpackage.
        """
        answer: Dict[str, API] = collections.OrderedDict()

        # Get the actual subpackages we have.
        #
        # Note that this intentionally only goes one level deep; nested
        # subpackages can be accessed by requesting subpackages of the
        # derivative API objects returned here.
        level = len(self.subpackage_view)
        for subpkg_name in sorted({p.meta.address.subpackage[0]
                                   for p in self.protos.values()
                                   if len(p.meta.address.subpackage) > level and
                                   p.meta.address.subpackage[:level] == self.subpackage_view}):
            answer[subpkg_name] = dataclasses.replace(self,
                                                      subpackage_view=self.subpackage_view +
                                                      (subpkg_name,),
                                                      )
        return answer

    def gapic_metadata(self, options: Options) -> gapic_metadata_pb2.GapicMetadata:
        gm = gapic_metadata_pb2.GapicMetadata(
            schema="1.0",
            comment="This file maps proto services/RPCs to the corresponding library clients/methods",
            language="python",
            proto_package=self.naming.proto_package,
            library_package=".".join(
                self.naming.module_namespace +
                    (self.naming.versioned_module_name,)
            ),
        )

        for service in sorted(self.services.values(), key=lambda s: s.name):
            service_desc = gm.services.get_or_create(service.name)

            # At least one of "grpc" or "rest" is guaranteed to be present because
            # of the way that Options instances are created.
            # This assumes the options are generated by the class method factory.
            transports = []
            if "grpc" in options.transport:
                transports.append((TRANSPORT_GRPC, service.client_name))
                transports.append(
                    (TRANSPORT_GRPC_ASYNC, service.async_client_name))

            if "rest" in options.transport:
                transports.append((TRANSPORT_REST, service.client_name))

            methods = sorted(service.methods.values(), key=lambda m: m.name)
            for tprt, client_name in transports:
                transport = service_desc.clients.get_or_create(tprt)
                transport.library_client = client_name
                for method in methods:
                    method_desc = transport.rpcs.get_or_create(method.name)
                    method_desc.methods.append(to_snake_case(method.name))

        return gm

    def gapic_metadata_json(self, options: Options) -> str:
        return MessageToJson(self.gapic_metadata(options), sort_keys=True)

    def requires_package(self, pkg: Tuple[str, ...]) -> bool:
        pkg_has_iam_mixin = self.has_iam_mixin and \
            pkg == ('google', 'iam', 'v1')
        return pkg_has_iam_mixin or any(
            message.ident.package == pkg
            for proto in self.all_protos.values()
            for message in proto.all_messages.values()
        )

    def get_custom_operation_service(self, method: "wrappers.Method") -> "wrappers.Service":
        """Return the extended operation service that should be polled for progress
        from a given initial method.

        Precondition: `method` returns an Extended Operation type message
        and has an `operation_polling_service` annotation.
        """
        if not method.output.is_extended_operation:
            raise ValueError(
                f"Method is not an extended operation LRO: {method.name}")

        op_serv_name = self.naming.proto_package + "." + \
            method.options.Extensions[ex_ops_pb2.operation_service]
        op_serv = self.services.get(op_serv_name)
        if not op_serv:
            raise ValueError(
                f"No such service: {op_serv_name}"
            )

        if not op_serv.operation_polling_method:
            raise ValueError(
                f"Service is not an extended operation operation service: {op_serv.name}")

        return op_serv

    @cached_property
    def mixin_api_signatures(self):
        """Compile useful info about MixIn API signatures.

        Returns:
            Mapping[str, wrappers.MixinMethod]: Useful info
                about MixIn methods present for the main API.
        """
        return {name: mixins.MIXINS_MAP[name] for name in self.mixin_api_methods}

    @cached_property
    def mixin_api_methods(self) -> Dict[str, MethodDescriptorProto]:
        methods: Dict[str, MethodDescriptorProto] = {}
        if self.has_location_mixin:
            methods = {**methods, **
                self._get_methods_from_service(locations_pb2)}
        if not self._has_iam_overrides and self.has_iam_mixin:
            methods = {**methods, **
                self._get_methods_from_service(iam_policy_pb2)}
        if self.has_operations_mixin:
            methods = {**methods, **
                self._get_methods_from_service(operations_pb2)}
        return methods

    @cached_property
    def mixin_http_options(self):
        """Gather HTTP options for the MixIn methods."""
        api_methods = self.mixin_api_methods
        res = {}
        for s in api_methods:
            m = api_methods[s]
            http = m.options.Extensions[annotations_pb2.http]
            http_options = [http] + list(http.additional_bindings)
            opt_gen = (wrappers.MixinHttpRule.try_parse_http_rule(http_rule)
                   for http_rule in http_options)
            res[s] = [rule for rule in opt_gen if rule]
        return res

    @cached_property
    def has_location_mixin(self) -> bool:
        return len(list(filter(lambda api: api.name == "google.cloud.location.Locations", self.service_yaml_config.apis))) > 0

    @cached_property
    def has_iam_mixin(self) -> bool:
        return len(list(filter(lambda api: api.name == "google.iam.v1.IAMPolicy", self.service_yaml_config.apis))) > 0

    @cached_property
    def has_operations_mixin(self) -> bool:
        return len(list(filter(lambda api: api.name == "google.longrunning.Operations", self.service_yaml_config.apis))) > 0

    @cached_property
    def _has_iam_overrides(self) -> bool:
        if not self.has_iam_mixin:
            return False
        iam_mixin_methods: Dict[str, MethodDescriptorProto] = self._get_methods_from_service(
            iam_policy_pb2)
        for (_, s) in self.services.items():
            for m_name in iam_mixin_methods:
                if m_name in s.methods:
                    return True
        return False

    def _get_methods_from_service(self, service_pb) -> Dict[str, MethodDescriptorProto]:
        services = service_pb.DESCRIPTOR.services_by_name
        methods = {}
        methods_to_generate = {}
        for service_name in services:
            service: ServiceDescriptor = services[service_name]
            for method in service.methods:
                fqn = "{}.{}.{}".format(
                    service_pb.DESCRIPTOR.package, service.name, method.name)
                methods[fqn] = method
        for rule in self.service_yaml_config.http.rules:
            if rule.selector in methods:
                m = methods[rule.selector]
                x = descriptor_pb2.MethodDescriptorProto()
                m.CopyToProto(x)
                x.options.Extensions[annotations_pb2.http].CopyFrom(rule)
                methods_to_generate[x.name] = x
        return methods_to_generate

    def get_extended_operations_services(self, service) -> Set["wrappers.Service"]:
        """Return a set of all the extended operation services used by the input service.

        Precondition: `service` is NOT an extended operation service
        """
        return set(
            self.get_custom_operation_service(m)
            for m in service.methods.values()
            if m.operation_service
        )


class _ProtoBuilder:
    """A "builder class" for Proto objects.

    The sole purpose of this class is to accept the information from the
    file descriptor and "piece together" the components of the :class:`~.Proto`
    object in-place.

    This allows the public :class:`~.Proto` object to be frozen, and free
    of the setup machinations.

    The correct usage of this class is always to create an instance, call
    the :attr:`proto` property, and then throw the builder away. Additionally,
    there should be no reason to use this class outside of this module.
    """
    EMPTY = descriptor_pb2.SourceCodeInfo.Location()

    def __init__(
        self,
        file_descriptor: descriptor_pb2.FileDescriptorProto,
        file_to_generate: bool,
        naming: api_naming.Naming,
        opts: Options = Options(),
        prior_protos: Optional[Mapping[str, Proto]] = None,
        load_services: bool = True,
        all_resources: Optional[Mapping[str, wrappers.MessageType]] = None,
    ):
        self.proto_messages: Dict[str, wrappers.MessageType] = {}
        self.proto_enums: Dict[str, wrappers.EnumType] = {}
        self.proto_services: Dict[str, wrappers.Service] = {}
        self.file_descriptor = file_descriptor
        self.file_to_generate = file_to_generate
        self.prior_protos = prior_protos or {}
        self.opts = opts

        # Iterate over the documentation and place it into a dictionary.
        #
        # The comments in protocol buffers are sorted by a concept called
        # the "path", which is a sequence of integers described in more
        # detail below; this code simply shifts from a list to a dict,
        # with tuples of paths as the dictionary keys.
        self.docs: Dict[Tuple[int, ...],
                        descriptor_pb2.SourceCodeInfo.Location] = {}
        for location in file_descriptor.source_code_info.location:
            self.docs[tuple(location.path)] = location

        # Everything has an "address", which is the proto where the thing
        # was declared.
        #
        # We put this together by a baton pass of sorts: everything in
        # this file *starts with* this address, which is appended to
        # for each item as it is loaded.
        self.address = metadata.Address(
            api_naming=naming,
            module=file_descriptor.name.split('/')[-1][:-len('.proto')],
            package=tuple(file_descriptor.package.split('.')),
        )

        # Now iterate over the FileDescriptorProto and pull out each of
        # the messages, enums, and services.
        #
        # The hard-coded path keys sent here are based on how descriptor.proto
        # works; it uses the proto message number of the pieces of each
        # message (e.g. the hard-code `4` for `message_type` immediately
        # below is because `repeated DescriptorProto message_type = 4;` in
        # descriptor.proto itself).
        self._load_children(file_descriptor.enum_type, self._load_enum,
                            address=self.address, path=(5,),
                            resources=all_resources or {})
        self._load_children(file_descriptor.message_type, self._load_message,
                            address=self.address, path=(4,),
                            resources=all_resources or {})

        # Edge case: Protocol buffers is not particularly picky about
        # ordering, and it is possible that a message will have had a field
        # referencing another message which appears later in the file
        # (or itself, recursively).
        #
        # In this situation, we would not have come across the message yet,
        # and the field would have its original textual reference to the
        # message (`type_name`) but not its resolved message wrapper.
        orphan_field_gen = (
            (field.type_name.lstrip('.'), field)
            for message in self.proto_messages.values()
            for field in message.fields.values()
            if field.type_name and not (field.message or field.enum)
        )
        for key, field in orphan_field_gen:
            maybe_msg_type = self.proto_messages.get(key)
            maybe_enum_type = self.proto_enums.get(key)
            if maybe_msg_type:
                object.__setattr__(field, 'message', maybe_msg_type)
            elif maybe_enum_type:
                object.__setattr__(field, 'enum', maybe_enum_type)
            else:
                raise TypeError(
                    f"Unknown type referenced in "
                    f"{self.file_descriptor.name}: '{key}'"
                )

        # Only generate the service if this is a target file to be generated.
        # This prevents us from generating common services (e.g. LRO) when
        # they are being used as an import just to get types declared in the
        # same files.
        if file_to_generate and load_services:
            self._load_children(file_descriptor.service, self._load_service,
                                address=self.address, path=(6,),
                                resources=all_resources or {})
        # TODO(lukesneeringer): oneofs are on path 7.

    @property
    def proto(self) -> Proto:
        """Return a Proto dataclass object."""
        # Create a "context-naïve" proto.
        # This has everything but is ignorant of naming collisions in the
        # ultimate file that will be written.
        naive = Proto(
            all_enums=self.proto_enums,
            all_messages=self.proto_messages,
            file_pb2=self.file_descriptor,
            file_to_generate=self.file_to_generate,
            services=self.proto_services,
            meta=metadata.Metadata(
                address=self.address,
            ),
        )

        # If this is not a file being generated, we do not need to
        # do anything else.
        if not self.file_to_generate:
            return naive

        visited_messages: Set[wrappers.MessageType] = set()
        # Return a context-aware proto object.
        return dataclasses.replace(
            naive,
            all_enums=collections.OrderedDict(
                (k, v.with_context(collisions=naive.names))
                for k, v in naive.all_enums.items()
            ),
            all_messages=collections.OrderedDict(
                (k, v.with_context(
                    collisions=naive.names,
                    visited_messages=visited_messages,
                ))
                for k, v in naive.all_messages.items()
            ),
            services=collections.OrderedDict(
                # Note: services bind to themselves because services get their
                # own output files.
                (k, v.with_context(
                    collisions=v.names,
                    visited_messages=visited_messages,
                ))
                for k, v in naive.services.items()
            ),
            meta=naive.meta.with_context(collisions=naive.names),
        )

    @cached_property
    def api_enums(self) -> Mapping[str, wrappers.EnumType]:
        return collections.ChainMap(
            {},
            self.proto_enums,
            # This is actually fine from a typing perspective:
            # we're agglutinating all the prior protos' enums, which are
            # stored in maps. This is just a convenient way to expand it out.
            *[p.all_enums for p in self.prior_protos.values()],  # type: ignore
        )

    @cached_property
    def api_messages(self) -> Mapping[str, wrappers.MessageType]:
        return collections.ChainMap(
            {},
            self.proto_messages,
            # This is actually fine from a typing perspective:
            # we're agglutinating all the prior protos' enums, which are
            # stored in maps. This is just a convenient way to expand it out.
            *[p.all_messages for p in self.prior_protos.values()],  # type: ignore
        )

    def _load_children(self,
                       children: Sequence, loader: Callable, *,
                       address: metadata.Address, path: Tuple[int, ...],
                       resources: Mapping[str, wrappers.MessageType]) -> Mapping:
        """Return wrapped versions of arbitrary children from a Descriptor.

        Args:
            children (list): A sequence of children of the given field to
                be loaded. For example, a FileDescriptorProto contains the
                lists ``message_type``, ``enum_type``, etc.; these are valid
                inputs for this argument.
            loader (Callable[Message, Address, Tuple[int]]): The function able
                to load the kind of message in ``children``. This should
                be one of the ``_load_{noun}`` methods on this class
                (e.g. ``_load_descriptor``).
            address (~.metadata.Address): The address up to this point.
                This will include the package and may include outer messages.
            path (Tuple[int]): The location path up to this point. This is
                used to correspond to documentation in
                ``SourceCodeInfo.Location`` in ``descriptor.proto``.

        Return:
            Mapping[str, Union[~.MessageType, ~.Service, ~.EnumType]]: A
                sequence of the objects that were loaded.
        """
        # Iterate over the list of children provided and call the
        # applicable loader function on each.
        answer = {}
        for child, i in zip(children, range(0, sys.maxsize)):
            wrapped = loader(child, address=address, path=path + (i,),
                             resources=resources)
            answer[wrapped.name] = wrapped
        return answer

    def _get_oneofs(self,
                    oneof_pbs: Sequence[descriptor_pb2.OneofDescriptorProto],
                    address: metadata.Address, path: Tuple[int, ...],
                    ) -> Dict[str, wrappers.Oneof]:
        """Return a dictionary of wrapped oneofs for the given message.

        Args:
            oneof_fields (Sequence[~.descriptor_pb2.OneofDescriptorProto]): A
                sequence of protobuf field objects.
            address (~.metadata.Address): An address object denoting the
                location of these oneofs.
            path (Tuple[int]): The source location path thus far, as
                understood by ``SourceCodeInfo.Location``.

        Returns:
            Mapping[str, ~.wrappers.Oneof]: A ordered mapping of
                :class:`~.wrappers.Oneof` objects.
        """
        # Iterate over the oneofs and collect them into a dictionary.
        answer = collections.OrderedDict(
            (oneof_pb.name, wrappers.Oneof(oneof_pb=oneof_pb))
            for i, oneof_pb in enumerate(oneof_pbs)
        )

        # Done; return the answer.
        return answer

    def _get_fields(self,
                    field_pbs: Sequence[descriptor_pb2.FieldDescriptorProto],
                    address: metadata.Address, path: Tuple[int, ...],
                    oneofs: Optional[Dict[str, wrappers.Oneof]] = None
                    ) -> Dict[str, wrappers.Field]:
        """Return a dictionary of wrapped fields for the given message.

        Args:
            field_pbs (Sequence[~.descriptor_pb2.FieldDescriptorProto]): A
                sequence of protobuf field objects.
            address (~.metadata.Address): An address object denoting the
                location of these fields.
            path (Tuple[int]): The source location path thus far, as
                understood by ``SourceCodeInfo.Location``.

        Returns:
            Mapping[str, ~.wrappers.Field]: A ordered mapping of
                :class:`~.wrappers.Field` objects.
        """
        # Iterate over the fields and collect them into a dictionary.
        #
        # The saving of the enum and message types rely on protocol buffers'
        # naming rules to trust that they will never collide.
        #
        # Note: If this field is a recursive reference to its own message,
        # then the message will not be in `api_messages` yet (because the
        # message wrapper is not yet created, because it needs this object
        # first) and this will be None. This case is addressed in the
        # `_load_message` method.
        answer: Dict[str, wrappers.Field] = collections.OrderedDict()
        for i, field_pb in enumerate(field_pbs):
            is_oneof = oneofs and field_pb.HasField('oneof_index')
            oneof_name = nth(
                (oneofs or {}).keys(),
                field_pb.oneof_index
            ) if is_oneof else None

            field = wrappers.Field(
                field_pb=field_pb,
                enum=self.api_enums.get(field_pb.type_name.lstrip('.')),
                message=self.api_messages.get(field_pb.type_name.lstrip('.')),
                meta=metadata.Metadata(
                    address=address.child(field_pb.name, path + (i,)),
                    documentation=self.docs.get(path + (i,), self.EMPTY),
                ),
                oneof=oneof_name,
            )
            answer[field.name] = field

        # Done; return the answer.
        return answer

    def _get_retry_and_timeout(
        self,
        service_address: metadata.Address,
        meth_pb: descriptor_pb2.MethodDescriptorProto
    ) -> Tuple[Optional[wrappers.RetryInfo], Optional[float]]:
        """Returns the retry and timeout configuration of a method if it exists.

        Args:
            service_address (~.metadata.Address): An address object for the
                service, denoting the location of these methods.
            meth_pb (~.descriptor_pb2.MethodDescriptorProto): A
                protobuf method objects.

        Returns:
            Tuple[Optional[~.wrappers.RetryInfo], Optional[float]]: The retry
                and timeout information for the method if it exists.
        """

        # If we got a gRPC service config, get the appropriate retry
        # and timeout information from it.
        retry = None
        timeout = None

        # This object should be a dictionary that conforms to the
        # gRPC service config proto:
        #   Repo: https://github.com/grpc/grpc-proto/
        #   Filename: grpc/service_config/service_config.proto
        #
        # We only care about a small piece, so we are just leaving
        # it as a dictionary and parsing accordingly.
        if self.opts.retry:
            # The gRPC service config uses a repeated `name` field
            # with a particular format, which we match against.
            # This defines the expected selector for *this* method.
            selector = {
                'service': '{package}.{service_name}'.format(
                    package='.'.join(service_address.package),
                    service_name=service_address.name,
                ),
                'method': meth_pb.name,
            }

            # Find the method config that applies to us, if any.
            mc = next((c for c in self.opts.retry.get('methodConfig', [])
                       if selector in c.get('name')), None)
            if mc:
                # Set the timeout according to this method config.
                if mc.get('timeout'):
                    timeout = self._to_float(mc['timeout'])

                # Set the retry according to this method config.
                if 'retryPolicy' in mc:
                    r = mc['retryPolicy']
                    retry = wrappers.RetryInfo(
                        max_attempts=r.get('maxAttempts', 0),
                        initial_backoff=self._to_float(
                            r.get('initialBackoff', '0s'),
                        ),
                        max_backoff=self._to_float(r.get('maxBackoff', '0s')),
                        backoff_multiplier=r.get('backoffMultiplier', 0.0),
                        retryable_exceptions=frozenset(
                            exceptions.exception_class_for_grpc_status(
                                getattr(grpc.StatusCode, code),
                            )
                            for code in r.get('retryableStatusCodes', [])
                        ),
                    )

        return retry, timeout

    def _maybe_get_lro(
        self,
        service_address: metadata.Address,
        meth_pb: descriptor_pb2.MethodDescriptorProto
    ) -> Optional[wrappers.OperationInfo]:
        """Determines whether a method is a Long Running Operation (aka LRO)
               and, if it is, return an OperationInfo that includes the response
               and metadata types.

        Args:
            service_address (~.metadata.Address): An address object for the
                service, denoting the location of these methods.
            meth_pb (~.descriptor_pb2.MethodDescriptorProto): A
                protobuf method objects.

        Returns:
            Optional[~.wrappers.OperationInfo]: The info for the long-running
                operation, if the passed method is an LRO.
        """
        lro = None

        # If the output type is google.longrunning.Operation, we use
        # a specialized object in its place.
        if meth_pb.output_type.endswith('google.longrunning.Operation'):
            if not meth_pb.options.HasExtension(operations_pb2.operation_info):
                # This is not a long running operation even though it returns
                # an Operation.
                return None
            op = meth_pb.options.Extensions[operations_pb2.operation_info]
            if not op.response_type or not op.metadata_type:
                raise TypeError(
                    f'rpc {meth_pb.name} returns a google.longrunning.'
                    'Operation, but is missing a response type or '
                    'metadata type.',
                )
            response_key = service_address.resolve(op.response_type)
            metadata_key = service_address.resolve(op.metadata_type)
            lro = wrappers.OperationInfo(
                response_type=self.api_messages[response_key],
                metadata_type=self.api_messages[metadata_key],
            )

        return lro

    def _maybe_get_extended_lro(
        self,
        service_address: metadata.Address,
        meth_pb: descriptor_pb2.MethodDescriptorProto,
    ) -> Optional[wrappers.ExtendedOperationInfo]:
        op_service_name = meth_pb.options.Extensions[ex_ops_pb2.operation_service]
        if not op_service_name:
            return None

        # Manual lookups because services and methods haven't been loaded.
        # Note: this assumes that the operation service lives in the same proto file.
        # This is a reasonable assumption as of March '22, but it may (unlikely)
        # change in the future.
        op_service_pb = next(
            (s for s in self.file_descriptor.service if s.name == op_service_name),
            None,
        )
        if not op_service_pb:
            raise ValueError(
                f"Could not find custom operation service: {op_service_name}"
            )

        operation_polling_method_pb = next(
            (
                m
                for m in op_service_pb.method
                if m.options.Extensions[ex_ops_pb2.operation_polling_method]
            ),
            None,
        )
        if not operation_polling_method_pb:
            raise ValueError(
                f"Could not find operation polling method for custom operation service: {op_service_name}"
            )

        operation_request_key = service_address.resolve(
            operation_polling_method_pb.input_type.lstrip(".")
        )
        operation_request_message = self.api_messages[operation_request_key]

        operation_type = service_address.resolve(
            operation_polling_method_pb.output_type.lstrip(".")
        )
        method_output_type = service_address.resolve(
            meth_pb.output_type.lstrip(".")
        )
        if operation_type != method_output_type:
            raise ValueError(
                f"Inconsistent return types between extended lro method '{meth_pb.name}'"
                f" and extended lro polling method '{operation_polling_method_pb.name}':"
                f" '{method_output_type}' and '{operation_type}'"
            )

        operation_message = self.api_messages[operation_type]
        if not operation_message.is_extended_operation:
            raise ValueError(
                f"Message is not an extended operation: {operation_type}"
            )

        return wrappers.ExtendedOperationInfo(
            request_type=operation_request_message,
            operation_type=operation_message,
        )

    def _get_methods(self,
                     methods: Sequence[descriptor_pb2.MethodDescriptorProto],
                     service_address: metadata.Address, path: Tuple[int, ...],
                     ) -> Mapping[str, wrappers.Method]:
        """Return a dictionary of wrapped methods for the given service.

        Args:
            methods (Sequence[~.descriptor_pb2.MethodDescriptorProto]): A
                sequence of protobuf method objects.
            service_address (~.metadata.Address): An address object for the
                service, denoting the location of these methods.
            path (Tuple[int]): The source location path thus far, as understood
                by ``SourceCodeInfo.Location``.

        Returns:
            Mapping[str, ~.wrappers.Method]: A ordered mapping of
                :class:`~.wrappers.Method` objects.
        """
        # Iterate over the methods and collect them into a dictionary.
        answer: Dict[str, wrappers.Method] = collections.OrderedDict()
        for i, meth_pb in enumerate(methods):
            retry, timeout = self._get_retry_and_timeout(
                service_address,
                meth_pb
            )

            # Create the method wrapper object.
            answer[meth_pb.name] = wrappers.Method(
                input=self.api_messages[meth_pb.input_type.lstrip('.')],
                lro=self._maybe_get_lro(service_address, meth_pb),
                extended_lro=self._maybe_get_extended_lro(
                    service_address,
                    meth_pb,
                ),
                method_pb=meth_pb,
                meta=metadata.Metadata(
                    address=service_address.child(meth_pb.name, path + (i,)),
                    documentation=self.docs.get(path + (i,), self.EMPTY),
                ),
                output=self.api_messages[meth_pb.output_type.lstrip('.')],
                retry=retry,
                timeout=timeout,
            )

        # Done; return the answer.
        return answer

    def _load_message(self,
                      message_pb: descriptor_pb2.DescriptorProto,
                      address: metadata.Address,
                      path: Tuple[int],
                      resources: Mapping[str, wrappers.MessageType],
                      ) -> wrappers.MessageType:
        """Load message descriptions from DescriptorProtos."""
        address = address.child(message_pb.name, path)

        # Load all nested items.
        #
        # Note: This occurs before piecing together this message's fields
        # because if nested types are present, they are generally the
        # type of one of this message's fields, and they need to be in
        # the registry for the field's message or enum attributes to be
        # set correctly.
        nested_enums = self._load_children(
            message_pb.enum_type,
            address=address,
            loader=self._load_enum,
            path=path + (4,),
            resources=resources,
        )
        nested_messages = self._load_children(
            message_pb.nested_type,
            address=address,
            loader=self._load_message,
            path=path + (3,),
            resources=resources,
        )

        oneofs = self._get_oneofs(
            message_pb.oneof_decl,
            address=address,
            path=path + (7,),
        )

        # Create a dictionary of all the fields for this message.
        fields = self._get_fields(
            message_pb.field,
            address=address,
            path=path + (2,),
            oneofs=oneofs,
        )
        fields.update(self._get_fields(
            message_pb.extension,
            address=address,
            path=path + (6,),
            oneofs=oneofs,
        ))

        # Create a message correspoding to this descriptor.
        self.proto_messages[address.proto] = wrappers.MessageType(
            fields=fields,
            message_pb=message_pb,
            nested_enums=nested_enums,
            nested_messages=nested_messages,
            meta=metadata.Metadata(
                address=address,
                documentation=self.docs.get(path, self.EMPTY),
            ),
            oneofs=oneofs,
        )
        return self.proto_messages[address.proto]

    def _load_enum(self,
                   enum: descriptor_pb2.EnumDescriptorProto,
                   address: metadata.Address,
                   path: Tuple[int],
                   resources: Mapping[str, wrappers.MessageType],
                   ) -> wrappers.EnumType:
        """Load enum descriptions from EnumDescriptorProtos."""
        address = address.child(enum.name, path)

        # Put together wrapped objects for the enum values.
        values = []
        for enum_value, i in zip(enum.value, range(0, sys.maxsize)):
            values.append(wrappers.EnumValueType(
                enum_value_pb=enum_value,
                meta=metadata.Metadata(
                    address=address,
                    documentation=self.docs.get(path + (2, i), self.EMPTY),
                ),
            ))

        # Load the enum itself.
        self.proto_enums[address.proto] = wrappers.EnumType(
            enum_pb=enum,
            meta=metadata.Metadata(
                address=address,
                documentation=self.docs.get(path, self.EMPTY),
            ),
            values=values,
        )
        return self.proto_enums[address.proto]

    def _load_service(self,
                      service: descriptor_pb2.ServiceDescriptorProto,
                      address: metadata.Address,
                      path: Tuple[int],
                      resources: Mapping[str, wrappers.MessageType],
                      ) -> wrappers.Service:
        """Load comments for a service and its methods."""
        address = address.child(service.name, path)

        # Put together a dictionary of the service's methods.
        methods = self._get_methods(
            service.method,
            service_address=address,
            path=path + (2,),
        )

        # Load the comments for the service itself.
        self.proto_services[address.proto] = wrappers.Service(
            meta=metadata.Metadata(
                address=address,
                documentation=self.docs.get(path, self.EMPTY),
            ),
            methods=methods,
            service_pb=service,
            visible_resources=resources,
        )
        return self.proto_services[address.proto]

    def _to_float(self, s: str) -> float:
        """Convert a protobuf duration string (e.g. `"30s"`) to float."""
        return int(s[:-1]) / 1e9 if s.endswith('n') else float(s[:-1])
