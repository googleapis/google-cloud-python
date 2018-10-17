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

"""Module containing wrapper classes around meta-descriptors.

This module contains dataclasses which wrap the descriptor protos
defined in google/protobuf/descriptor.proto (which are descriptors that
describe descriptors).

These wrappers exist in order to provide useful helper methods and
generally ease access to things in templates (in particular, documentation,
certain aggregate views of things, etc.)

Reading of underlying descriptor properties in templates *is* okay, a
``__getattr__`` method which consistently routes in this way is provided.
Documentation is consistently at ``{thing}.meta.doc``.
"""

import collections
import dataclasses
import re
from itertools import chain
from typing import Iterable, List, Mapping, Sequence, Set, Tuple, Union

from google.api import annotations_pb2
from google.api import signature_pb2
from google.protobuf import descriptor_pb2

from gapic import utils
from gapic.schema import imp
from gapic.schema import metadata


@dataclasses.dataclass(frozen=True)
class Field:
    """Description of a field."""
    field_pb: descriptor_pb2.FieldDescriptorProto
    message: 'MessageType' = None
    enum: 'EnumType' = None
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )

    def __getattr__(self, name):
        return getattr(self.field_pb, name)

    @utils.cached_property
    def ident(self) -> metadata.FieldIdentifier:
        """Return the identifier to be used in templates."""
        return metadata.FieldIdentifier(
            ident=self.type.ident,
            repeated=self.repeated,
        )

    @property
    def is_primitive(self) -> bool:
        """Return True if the field is a primitive, False otherwise."""
        return isinstance(self.type, PythonType)

    @property
    def proto_type(self) -> str:
        """Return the proto type constant to be used in templates."""
        return descriptor_pb2.FieldDescriptorProto.Type.Name(
            self.field_pb.type,
        )[len('TYPE_'):]

    @property
    def repeated(self) -> bool:
        """Return True if this is a repeated field, False otherwise.

        Returns:
            bool: Whether this field is repeated.
        """
        return self.label == \
            descriptor_pb2.FieldDescriptorProto.Label.Value('LABEL_REPEATED')

    @property
    def required(self) -> bool:
        """Return True if this is a required field, False otherwise.

        Returns:
            bool: Whether this field is required.
        """
        return bool(self.options.Extensions[annotations_pb2.required])

    @utils.cached_property
    def type(self) -> Union['MessageType', 'EnumType', 'PythonType']:
        """Return the type of this field."""
        # If this is a message or enum, return the appropriate thing.
        if self.type_name and self.message:
            return self.message
        if self.type_name and self.enum:
            return self.enum

        # This is a primitive. Return the corresponding Python type.
        # The enum values used here are defined in:
        #   Repository: https://github.com/google/protobuf/
        #   Path: src/google/protobuf/descriptor.proto
        #
        # The values are used here because the code would be excessively
        # verbose otherwise, and this is guaranteed never to change.
        #
        # 10, 11, and 14 are intentionally missing. They correspond to
        # group (unused), message (covered above), and enum (covered above).
        if self.field_pb.type in (1, 2):
            return PythonType(python_type=float)
        if self.field_pb.type in (3, 4, 5, 6, 7, 13, 15, 16, 17, 18):
            return PythonType(python_type=int)
        if self.field_pb.type == 8:
            return PythonType(python_type=bool)
        if self.field_pb.type == 9:
            return PythonType(python_type=str)
        if self.field_pb.type == 12:
            return PythonType(python_type=bytes)

        # This should never happen.
        raise TypeError('Unrecognized protobuf type. This code should '
                        'not be reachable; please file a bug.')

    def with_context(self, *, collisions: Set[str]) -> 'Field':
        """Return a derivative of this field with the provided context.

        This method is used to address naming collisions. The returned
        ``Field`` object aliases module names to avoid naming collisions
        in the file being written.
        """
        return dataclasses.replace(self,
            message=self.message.with_context(
                collisions=collisions,
                skip_fields=True,
            ) if self.message else None,
            enum=self.enum.with_context(collisions=collisions)
                if self.enum else None,
            meta=self.meta.with_context(collisions=collisions),
        )


@dataclasses.dataclass(frozen=True)
class MessageType:
    """Description of a message (defined with the ``message`` keyword)."""
    message_pb: descriptor_pb2.DescriptorProto
    fields: Mapping[str, Field]
    nested_enums: Mapping[str, 'EnumType']
    nested_messages: Mapping[str, 'MessageType']
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )

    def __getattr__(self, name):
        return getattr(self.message_pb, name)

    @utils.cached_property
    def field_types(self) -> Sequence[Union['MessageType', 'EnumType']]:
        """Return all composite fields used in this proto's messages."""
        answer = []
        for field in self.fields.values():
            if field.message or field.enum:
                answer.append(field.type)
        return tuple(answer)

    @property
    def ident(self) -> metadata.Address:
        """Return the identifier data to be used in templates."""
        return self.meta.address

    def get_field(self, *field_path: Sequence[str],
            collisions: Set[str] = frozenset()) -> Field:
        """Return a field arbitrarily deep in this message's structure.

        This method recursively traverses the message tree to return the
        requested inner-field.

        Traversing through repeated fields is not supported; a repeated field
        may be specified if and only if it is the last field in the path.

        Args:
            field_path (Sequence[str]): The field path.

        Returns:
            ~.Field: A field object.

        Raises:
            KeyError: If a repeated field is used in the non-terminal position
                in the path.
        """
        # If collisions are not explicitly specified, retrieve them
        # from this message's address.
        # This ensures that calls to `get_field` will return a field with
        # the same context, regardless of the number of levels through the
        # chain (in order to avoid infinite recursion on circular references,
        # we only shallowly bind message references held by fields; this
        # binds deeply in the one spot where that might be a problem).
        collisions = collisions or self.meta.address.collisions

        # Get the first field in the path.
        cursor = self.fields[field_path[0]]

        # Base case: If this is the last field in the path, return it outright.
        if len(field_path) == 1:
            return cursor.with_context(collisions=collisions)

        # Sanity check: If cursor is a repeated field, then raise an exception.
        # Repeated fields are only permitted in the terminal position.
        if cursor.repeated:
            raise KeyError(
                f'The {cursor.name} field is repeated; unable to use '
                '`get_field` to retrieve its children.\n'
                'This exception usually indicates that a '
                'google.api.method_signature annotation uses a repeated field '
                'in the fields list in a position other than the end.',
            )

        # Recursion case: Pass the remainder of the path to the sub-field's
        # message.
        return cursor.message.get_field(*field_path[1:], collisions=collisions)

    def with_context(self, *,
            collisions: Set[str],
            skip_fields: bool = False,
            ) -> 'MessageType':
        """Return a derivative of this message with the provided context.

        This method is used to address naming collisions. The returned
        ``MessageType`` object aliases module names to avoid naming collisions
        in the file being written.

        The ``skip_fields`` argument will omit applying the context to the
        underlying fields. This provides for an "exit" in the case of circular
        references.
        """
        return dataclasses.replace(self,
            fields=collections.OrderedDict([
                (k, v.with_context(collisions=collisions))
                for k, v in self.fields.items()
            ]) if not skip_fields else self.fields,
            nested_enums=collections.OrderedDict([
                (k, v.with_context(collisions=collisions))
                for k, v in self.nested_enums.items()
            ]),
            nested_messages=collections.OrderedDict([(k, v.with_context(
                collisions=collisions,
                skip_fields=skip_fields,
            )) for k, v in self.nested_messages.items()]),
            meta=self.meta.with_context(collisions=collisions),
        )


@dataclasses.dataclass(frozen=True)
class EnumValueType:
    """Description of an enum value."""
    enum_value_pb: descriptor_pb2.EnumValueDescriptorProto
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )

    def __getattr__(self, name):
        return getattr(self.enum_value_pb, name)


@dataclasses.dataclass(frozen=True)
class EnumType:
    """Description of an enum (defined with the ``enum`` keyword.)"""
    enum_pb: descriptor_pb2.EnumDescriptorProto
    values: List[EnumValueType]
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )

    def __getattr__(self, name):
        return getattr(self.enum_pb, name)

    @property
    def ident(self) -> metadata.Address:
        """Return the identifier data to be used in templates."""
        return self.meta.address

    def with_context(self, *, collisions: Set[str]) -> 'EnumType':
        """Return a derivative of this enum with the provided context.

        This method is used to address naming collisions. The returned
        ``EnumType`` object aliases module names to avoid naming collisions in
        the file being written.
        """
        return dataclasses.replace(self,
            meta=self.meta.with_context(collisions=collisions),
        )


@dataclasses.dataclass(frozen=True)
class PythonType:
    """Wrapper class for Python types.

    This exists for interface consistency, so that methods like
    :meth:`Field.type` can return an object and the caller can be confident
    that a ``name`` property will be present.
    """
    python_type: type

    @property
    def name(self) -> str:
        return self.python_type.__name__

    @utils.cached_property
    def ident(self) -> metadata.Address:
        """Return the identifier to be used in templates.

        Primitives have no import, and no module to reference, so this
        is simply the name of the class (e.g. "int", "str").
        """
        return metadata.Address(name=self.name)


@dataclasses.dataclass(frozen=True)
class OperationType:
    """Wrapper class for :class:`~.operations.Operation`.

    This exists for interface consistency, so Operations can be used
    alongside :class:`~.MessageType` instances.
    """
    lro_response: MessageType
    lro_metadata: MessageType = None

    @property
    def ident(self) -> metadata.Address:
        return self.meta.address

    @utils.cached_property
    def meta(self) -> metadata.Metadata:
        """Return a Metadata object."""
        return metadata.Metadata(
            address=metadata.Address(
                name='Operation',
                module='operation',
                package=('google', 'api_core'),
                collisions=self.lro_response.meta.address.collisions,
            ),
            documentation=descriptor_pb2.SourceCodeInfo.Location(
                leading_comments='An object representing a long-running '
                                 'operation. \n\n'
                                 'The result type for the operation will be '
                                 ':class:`{ident}`: {doc}'.format(
                                     doc=self.lro_response.meta.doc,
                                     ident=self.lro_response.ident.sphinx,
                                 ),
            ),
        )

    @property
    def name(self) -> str:
        """Return the class name."""
        # This is always "Operation", because it is always a reference to
        # `google.api_core.operation.Operation`.
        #
        # This is hard-coded rather than subclassing PythonType (above) so
        # that this generator is not forced to take an entire dependency
        # on google.api_core just to get these strings.
        return 'Operation'

    def with_context(self, *, collisions: Set[str]) -> 'OperationType':
        """Return a derivative of this operation with the provided context.

        This method is used to address naming collisions. The returned
        ``OperationType`` object aliases module names to avoid naming
        collisions in the file being written.
        """
        return dataclasses.replace(self,
            lro_response=self.lro_response.with_context(collisions=collisions),
            lro_metadata=self.lro_metadata.with_context(collisions=collisions),
        )


@dataclasses.dataclass(frozen=True)
class Method:
    """Description of a method (defined with the ``rpc`` keyword)."""
    method_pb: descriptor_pb2.MethodDescriptorProto
    input: MessageType
    output: MessageType
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )

    def __getattr__(self, name):
        return getattr(self.method_pb, name)

    @property
    def field_headers(self) -> Sequence[str]:
        """Return the field headers defined for this method."""
        http = self.options.Extensions[annotations_pb2.http]
        if http.get:
            return tuple(re.findall(r'\{([a-z][\w\d_.]+)=', http.get))
        return ()

    @property
    def grpc_stub_type(self) -> str:
        """Return the type of gRPC stub to use."""
        return '{client}_{server}'.format(
            client='stream' if self.client_streaming else 'unary',
            server='stream' if self.server_streaming else 'unary',
        )

    @utils.cached_property
    def ref_types(self) -> Sequence[Union[MessageType, EnumType]]:
        """Return types referenced by this method."""
        # Begin with the input (request) and output (response) messages.
        answer = [self.input, self.output]

        # If this method has flattening that is honored, add its
        # composite types.
        #
        # This entails adding the module for any field on the signature
        # unless the field is a primitive.
        for sig in self.signatures.single_dispatch:
            answer += sig.composite_types

        # If this method has LRO, it is possible (albeit unlikely) that
        # the LRO messages reside in a different module.
        if getattr(self.output, 'lro_response', None):
            answer.append(self.output.lro_response)
        if getattr(self.output, 'lro_metadata', None):
            answer.append(self.output.lro_metadata)

        # Done; return the answer.
        return tuple(answer)

    @utils.cached_property
    def signatures(self) -> Tuple[signature_pb2.MethodSignature]:
        """Return the signature defined for this method."""
        sig_pb2 = self.options.Extensions[annotations_pb2.method_signature]

        # Sanity check: If there are no signatures (which should be by far
        # the common case), just abort now.
        if len(sig_pb2.fields) == 0:
            return MethodSignatures(all=())

        # Signatures are annotated with an `additional_signatures` key that
        # allows for specifying additional signatures. This is an uncommon
        # case but we still want to deal with it.
        answer = []
        for sig in (sig_pb2,) + tuple(sig_pb2.additional_signatures):
            # Build a MethodSignature object with the appropriate name
            # and fields. The fields are field objects, retrieved from
            # the method's `input` message.
            answer.append(MethodSignature(
                name=sig.function_name if sig.function_name else self.name,
                fields=collections.OrderedDict([
                    (f.split('.')[-1], self.input.get_field(f))
                    for f in sig.fields
                ]),
            ))

        # Done; return a tuple of signatures.
        return MethodSignatures(all=tuple(answer))

    def with_context(self, *, collisions: Set[str]) -> 'Method':
        """Return a derivative of this method with the provided context.

        This method is used to address naming collisions. The returned
        ``Method`` object aliases module names to avoid naming collisions
        in the file being written.
        """
        return dataclasses.replace(self,
            input=self.input.with_context(collisions=collisions),
            output=self.output.with_context(collisions=collisions),
            meta=self.meta.with_context(collisions=collisions),
        )


@dataclasses.dataclass(frozen=True)
class MethodSignature:
    name: str
    fields: Mapping[str, Field]

    @utils.cached_property
    def dispatch_field(self) -> Union[MessageType, EnumType, PythonType]:
        """Return the first field.

        This is what is used for `functools.singledispatch`."""
        return next(iter(self.fields.values()))

    @utils.cached_property
    def composite_types(self) -> Sequence[Union[MessageType, EnumType]]:
        """Return all composite types used in this signature."""
        answer = []
        for field in self.fields.values():
            if field.message or field.enum:
                answer.append(field.type)
        return answer


@dataclasses.dataclass(frozen=True)
class MethodSignatures:
    all: Tuple[MethodSignature]

    def __getitem__(self, key: Union[int, slice]) -> MethodSignature:
        return self.all[key]

    def __iter__(self) -> Iterable[MethodSignature]:
        return iter(self.all)

    def __len__(self) -> int:
        return len(self.all)

    @utils.cached_property
    def single_dispatch(self) -> Tuple[MethodSignature]:
        """Return a tuple of signatures, grouped and deduped by dispatch type.

        In the Python 3 templates, we only honor at most one method
        signature per initial argument type, and only for primitives.

        This method groups and deduplicates signatures and sends back only
        the signatures that the template actually wants.

        Returns:
            Tuple[MethodSignature]: Method signatures to be used with
                "single dispatch" routing.
        """
        answer = collections.OrderedDict()
        for sig in [i for i in self.all
                    if isinstance(i.dispatch_field.type, PythonType)]:
            answer.setdefault(sig.dispatch_field.ident, sig)
        return tuple(answer.values())


@dataclasses.dataclass(frozen=True)
class Service:
    """Description of a service (defined with the ``service`` keyword)."""
    service_pb: descriptor_pb2.ServiceDescriptorProto
    methods: Mapping[str, Method]
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )

    def __getattr__(self, name):
        return getattr(self.service_pb, name)

    @property
    def host(self) -> str:
        """Return the hostname for this service, if specified.

        Returns:
            str: The hostname, with no protocol and no trailing ``/``.
        """
        if self.options.Extensions[annotations_pb2.default_host]:
            return self.options.Extensions[annotations_pb2.default_host]
        return utils.Placeholder('<<< SERVICE ADDRESS >>>')

    @property
    def oauth_scopes(self) -> Sequence[str]:
        """Return a sequence of oauth scopes, if applicable.

        Returns:
            Sequence[str]: A sequence of OAuth scopes.
        """
        oauth = self.options.Extensions[annotations_pb2.oauth]
        return tuple(oauth.scopes)

    @property
    def module_name(self) -> str:
        """Return the appropriate module name for this service.

        Returns:
            str: The service name, in snake case.
        """
        return utils.to_snake_case(self.name)

    @utils.cached_property
    def names(self) -> Set[str]:
        """Return a set of names used in this service.

        This is used for detecting naming collisions in the module names
        used for imports.
        """
        # Put together a set of the service and method names.
        answer = {self.name}.union(
            {utils.to_snake_case(i.name) for i in self.methods.values()}
        )

        # Identify any import module names where the same module name is used
        # from distinct packages.
        modules = {}
        for t in chain(*[m.ref_types for m in self.methods.values()]):
            modules.setdefault(t.ident.module, set())
            modules[t.ident.module].add(t.ident.package)
        for module_name, packages in modules.items():
            if len(packages) > 1:
                answer.add(module_name)

        # Done; return the answer.
        return frozenset(answer)

    @utils.cached_property
    def python_modules(self) -> Sequence[imp.Import]:
        """Return a sequence of Python modules, for import.

        The results of this method are in alphabetical order (by package,
        then module), and do not contain duplicates.

        Returns:
            Sequence[~.imp.Import]: The package and module, intended for
                use in templates.
        """
        answer = set()
        for method in self.methods.values():
            for t in method.ref_types:
                answer.add(t.ident.python_import)
        return tuple(sorted(list(answer)))

    @property
    def has_lro(self) -> bool:
        """Return whether the service has a long-running method."""
        return any([getattr(m.output, 'lro_response', None)
                    for m in self.methods.values()])

    def with_context(self, *, collisions: Set[str]) -> 'Service':
        """Return a derivative of this service with the provided context.

        This method is used to address naming collisions. The returned
        ``Service`` object aliases module names to avoid naming collisions
        in the file being written.
        """
        return dataclasses.replace(self,
            methods=collections.OrderedDict([
                (k, v.with_context(collisions=collisions))
                for k, v in self.methods.items()
            ]),
            meta=self.meta.with_context(collisions=collisions),
        )
