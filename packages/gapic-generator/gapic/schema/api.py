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
import sys
from typing import Callable, List, Mapping, Sequence, Tuple

from google.longrunning import operations_pb2
from google.protobuf import descriptor_pb2

from gapic.schema import metadata
from gapic.schema import naming
from gapic.schema import wrappers
from gapic.utils import cached_property
from gapic.utils import to_snake_case


@dataclasses.dataclass(frozen=True)
class Proto:
    """A representation of a particular proto file within an API."""

    file_pb2: descriptor_pb2.FileDescriptorProto
    services: Mapping[str, wrappers.Service]
    messages: Mapping[str, wrappers.MessageType]
    enums: Mapping[str, wrappers.EnumType]
    file_to_generate: bool

    def __getattr__(self, name: str):
        return getattr(self.file_pb2, name)

    @classmethod
    def build(cls, file_descriptor: descriptor_pb2.FileDescriptorProto,
            file_to_generate: bool, prior_protos: Mapping[str, 'Proto'] = None,
            ) -> 'Proto':
        """Build and return a Proto instance.

        Args:
            file_descriptor (~.FileDescriptorProto): The protocol buffer
                object describing the proto file.
            file_to_generate (bool): Whether this is a file which is
                to be directly generated, or a dependency.
            prior_protos (~.Proto): Previous, already processed protos.
                These are needed to look up messages in imported protos.
        """
        return _ProtoBuilder(file_descriptor,
            file_to_generate=file_to_generate,
            prior_protos=prior_protos or {},
        ).proto

    @property
    def module_name(self) -> str:
        """Return the appropriate module name for this service.

        Returns:
            str: The module name for this service (which is the service
                name in snake case).
        """
        return to_snake_case(self.name.split('/')[-1][:-len('.proto')])

    @cached_property
    def top(self) -> 'Proto':
        """Return a proto shim which is only aware of top-level objects.

        This is useful in a situation where a template wishes to iterate
        over only those messages and enums that are at the top level of the
        file.
        """
        return type(self)(
            file_pb2=self.file_pb2,
            services=self.services,
            messages={k: v for k, v in self.messages.items()
                      if not v.meta.address.parent},
            enums={k: v for k, v in self.enums.items()
                   if not v.meta.address.parent},
            file_to_generate=False,
        )


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
    naming: naming.Naming
    protos: Mapping[str, Proto]

    @classmethod
    def build(cls,
            file_descriptors: Sequence[descriptor_pb2.FileDescriptorProto],
            package: str = '') -> 'API':
        """Build the internal API schema based on the request.

        Args:
            file_descriptors (Sequence[~.FileDescriptorProto]): A list of
                :class:`~.FileDescriptorProto` objects describing the
                API.
            package (str): A protocol buffer package, as a string, for which
                code should be explicitly generated (including subpackages).
                Protos with packages outside this list are considered imports
                rather than explicit targets.
        """
        # Save information about the overall naming for this API.
        n = naming.Naming.build(*filter(
            lambda fd: fd.package.startswith(package),
            file_descriptors,
        ))

        # Iterate over each FileDescriptorProto and fill out a Proto
        # object describing it, and save these to the instance.
        protos = {}
        for fd in file_descriptors:
            protos[fd.name] = _ProtoBuilder(
                file_descriptor=fd,
                file_to_generate=fd.package.startswith(package),
                prior_protos=protos,
            ).proto

        # Done; return the API.
        return cls(naming=n, protos=protos)

    @cached_property
    def enums(self) -> Mapping[str, wrappers.EnumType]:
        """Return a map of all enums available in the API."""
        return collections.ChainMap({},
            *[p.enums for p in self.protos.values()],
        )

    @cached_property
    def messages(self) -> Mapping[str, wrappers.MessageType]:
        """Return a map of all messages available in the API."""
        return collections.ChainMap({},
            *[p.messages for p in self.protos.values()],
        )

    @cached_property
    def services(self) -> Mapping[str, wrappers.Service]:
        """Return a map of all services available in the API."""
        return collections.ChainMap({},
            *[p.services for p in self.protos.values()],
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

    def __init__(self, file_descriptor: descriptor_pb2.FileDescriptorProto,
                 file_to_generate: bool,
                 prior_protos: Mapping[str, Proto] = None):
        self.messages = {}
        self.enums = {}
        self.services = {}
        self.file_descriptor = file_descriptor
        self.file_to_generate = file_to_generate
        self.prior_protos = prior_protos or {}

        # Iterate over the documentation and place it into a dictionary.
        #
        # The comments in protocol buffers are sorted by a concept called
        # the "path", which is a sequence of integers described in more
        # detail below; this code simply shifts from a list to a dict,
        # with tuples of paths as the dictionary keys.
        self.docs = {}
        for location in file_descriptor.source_code_info.location:
            self.docs[tuple(location.path)] = location

        # Everything has an "address", which is the proto where the thing
        # was declared.
        #
        # We put this together by a baton pass of sorts: everything in
        # this file *starts with* this address, which is appended to
        # for each item as it is loaded.
        address = metadata.Address(
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
                            address=address, path=(5,))
        self._load_children(file_descriptor.message_type, self._load_message,
                            address=address, path=(4,))

        # Edge case: Protocol buffers is not particularly picky about
        # ordering, and it is possible that a message will have had a field
        # referencing another message which appears later in the file
        # (or itself, recursively).
        #
        # In this situation, we would not have come across the message yet,
        # and the field would have its original textual reference to the
        # message (`type_name`) but not its resolved message wrapper.
        for message in self.messages.values():
            for field in message.fields.values():
                if field.type_name and not any((field.message, field.enum)):
                    object.__setattr__(
                        field, 'message',
                        self.messages[field.type_name.lstrip('.')],
                    )

        # Only generate the service if this is a target file to be generated.
        # This prevents us from generating common services (e.g. LRO) when
        # they are being used as an import just to get types declared in the
        # same files.
        if file_to_generate:
            self._load_children(file_descriptor.service, self._load_service,
                                address=address, path=(6,))
        # TODO(lukesneeringer): oneofs are on path 7.

    @property
    def proto(self) -> Proto:
        """Return a Proto dataclass object."""
        return Proto(
            enums=self.enums,
            file_pb2=self.file_descriptor,
            file_to_generate=self.file_to_generate,
            messages=self.messages,
            services=self.services,
        )

    @cached_property
    def all_enums(self) -> Mapping[str, wrappers.EnumType]:
        return collections.ChainMap({}, self.enums,
            *[p.enums for p in self.prior_protos.values()],
        )

    @cached_property
    def all_messages(self) -> Mapping[str, wrappers.MessageType]:
        return collections.ChainMap({}, self.messages,
            *[p.messages for p in self.prior_protos.values()],
        )

    def _get_operation_type(self,
            response_type: wrappers.Method,
            metadata_type: wrappers.Method = None,
            ) -> wrappers.PythonType:
        """Return a wrapper around Operation that designates the end result.

        Args:
            response_type (~.wrappers.Method): The response type that
                the Operation ultimately uses.
            metadata_type (~.wrappers.Method): The metadata type that
                the Operation ultimately uses, if any.

        Returns:
            ~.wrappers.OperationType: An OperationType object, which is
                sent down to templates, and aware of the LRO types used.
        """
        return wrappers.OperationType(
            lro_response=response_type,
            lro_metadata=metadata_type,
        )

    def _load_children(self, children: Sequence, loader: Callable, *,
                       address: metadata.Address, path: Tuple[int]) -> Mapping:
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
            wrapped = loader(child, address=address, path=path + (i,))
            answer[wrapped.name] = wrapped
        return answer

    def _get_fields(self, field_pbs: List[descriptor_pb2.FieldDescriptorProto],
                    address: metadata.Address, path: Tuple[int],
                    ) -> Mapping[str, wrappers.Field]:
        """Return a dictionary of wrapped fields for the given message.

        Args:
            fields (Sequence[~.descriptor_pb2.FieldDescriptorProto]): A
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
        # then the message will not be in `all_messages` yet (because the
        # message wrapper is not yet created, because it needs this object
        # first) and this will be None. This case is addressed in the
        # `_load_message` method.
        answer = collections.OrderedDict()
        for field_pb, i in zip(field_pbs, range(0, sys.maxsize)):
            answer[field_pb.name] = wrappers.Field(
                field_pb=field_pb,
                enum=self.all_enums.get(field_pb.type_name.lstrip('.')),
                message=self.all_messages.get(field_pb.type_name.lstrip('.')),
                meta=metadata.Metadata(
                    address=address,
                    documentation=self.docs.get(path + (i,), self.EMPTY),
                ),
            )

        # Done; return the answer.
        return answer

    def _get_methods(self, methods: List[descriptor_pb2.MethodDescriptorProto],
                     address: metadata.Address, path: Tuple[int],
                     ) -> Mapping[str, wrappers.Method]:
        """Return a dictionary of wrapped methods for the given service.

        Args:
            methods (Sequence[~.descriptor_pb2.MethodDescriptorProto]): A
                sequence of protobuf method objects.
            address (~.metadata.Address): An address object denoting the
                location of these methods.
            path (Tuple[int]): The source location path thus far, as understood
                by ``SourceCodeInfo.Location``.

        Returns:
            Mapping[str, ~.wrappers.Method]: A ordered mapping of
                :class:`~.wrappers.Method` objects.
        """
        # Iterate over the methods and collect them into a dictionary.
        answer = collections.OrderedDict()
        for meth_pb, i in zip(methods, range(0, sys.maxsize)):
            types = meth_pb.options.Extensions[operations_pb2.operation_types]

            # If the output type is google.longrunning.Operation, we use
            # a specialized object in its place.
            output_type = self.all_messages[meth_pb.output_type.lstrip('.')]
            if meth_pb.output_type.endswith('google.longrunning.Operation'):
                output_type = self._get_operation_type(
                    response_type=self.all_messages[
                        address.resolve(types.response)
                    ],
                    metadata_type=self.all_messages.get(
                        address.resolve(types.metadata),
                    ),
                )

            # Create the method wrapper object.
            answer[meth_pb.name] = wrappers.Method(
                input=self.all_messages[meth_pb.input_type.lstrip('.')],
                method_pb=meth_pb,
                meta=metadata.Metadata(
                    address=address,
                    documentation=self.docs.get(path + (i,), self.EMPTY),
                ),
                output=output_type,
            )

        # Done; return the answer.
        return answer

    def _load_message(self,
            message_pb: descriptor_pb2.DescriptorProto,
            address: metadata.Address,
            path: Tuple[int],
            ) -> wrappers.MessageType:
        """Load message descriptions from DescriptorProtos."""
        address = address.child(message_pb.name)

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
        )
        nested_messages = self._load_children(
            message_pb.nested_type,
            address=address,
            loader=self._load_message,
            path=path + (3,),
        )
        # self._load_children(message.oneof_decl, loader=self._load_field,
        #                     address=nested_addr, info=info.get(8, {}))

        # Create a dictionary of all the fields for this message.
        fields = self._get_fields(
            message_pb.field,
            address=address,
            path=path + (2,),
        )
        fields.update(self._get_fields(
            message_pb.extension,
            address=address,
            path=path + (6,),
        ))

        # Create a message correspoding to this descriptor.
        self.messages[address.proto] = wrappers.MessageType(
            fields=fields,
            message_pb=message_pb,
            nested_enums=nested_enums,
            nested_messages=nested_messages,
            meta=metadata.Metadata(
                address=address,
                documentation=self.docs.get(path, self.EMPTY),
            ),
        )
        return self.messages[address.proto]

    def _load_enum(self,
            enum: descriptor_pb2.EnumDescriptorProto,
            address: metadata.Address,
            path: Tuple[int],
            ) -> wrappers.EnumType:
        """Load enum descriptions from EnumDescriptorProtos."""
        address = address.child(enum.name)

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
        self.enums[address.proto] = wrappers.EnumType(
            enum_pb=enum,
            meta=metadata.Metadata(
                address=address,
                documentation=self.docs.get(path, self.EMPTY),
            ),
            values=values,
        )
        return self.enums[address.proto]

    def _load_service(self,
            service: descriptor_pb2.ServiceDescriptorProto,
            address: metadata.Address,
            path: Tuple[int],
            ) -> wrappers.Service:
        """Load comments for a service and its methods."""
        address = address.child(service.name)

        # Put together a dictionary of the service's methods.
        methods = self._get_methods(
            service.method,
            address=address,
            path=path + (2,),
        )

        # Load the comments for the service itself.
        self.services[address.proto] = wrappers.Service(
            meta=metadata.Metadata(
                address=address,
                documentation=self.docs.get(path, self.EMPTY),
            ),
            methods=methods,
            service_pb=service,
        )
        return self.services[address.proto]
