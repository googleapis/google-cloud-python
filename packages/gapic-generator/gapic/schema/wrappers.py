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
from typing import (cast, Dict, FrozenSet, Iterable, List, Mapping, Optional,
                    Sequence, Set, Tuple, Union)

from google.api import annotations_pb2      # type: ignore
from google.api import client_pb2
from google.api import field_behavior_pb2
from google.api import resource_pb2
from google.api_core import exceptions      # type: ignore
from google.protobuf import descriptor_pb2  # type: ignore

from gapic import utils
from gapic.schema import metadata


@dataclasses.dataclass(frozen=True)
class Field:
    """Description of a field."""
    field_pb: descriptor_pb2.FieldDescriptorProto
    message: Optional['MessageType'] = None
    enum: Optional['EnumType'] = None
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )
    oneof: Optional[str] = None

    def __getattr__(self, name):
        return getattr(self.field_pb, name)

    @property
    def name(self) -> str:
        """Used to prevent collisions with python keywords"""
        name = self.field_pb.name
        return name + "_" if name in utils.RESERVED_NAMES else name

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
        return isinstance(self.type, PrimitiveType)

    @property
    def map(self) -> bool:
        """Return True if this field is a map, False otherwise."""
        return bool(self.repeated and self.message and self.message.map)

    @utils.cached_property
    def mock_value(self) -> str:
        """Return a repr of a valid, usually truthy mock value."""
        # For primitives, send a truthy value computed from the
        # field name.
        answer = 'None'
        if isinstance(self.type, PrimitiveType):
            if self.type.python_type == bool:
                answer = 'True'
            elif self.type.python_type == str:
                answer = f"'{self.name}_value'"
            elif self.type.python_type == bytes:
                answer = f"b'{self.name}_blob'"
            elif self.type.python_type == int:
                answer = f'{sum([ord(i) for i in self.name])}'
            elif self.type.python_type == float:
                answer = f'0.{sum([ord(i) for i in self.name])}'
            else:  # Impossible; skip coverage checks.
                raise TypeError('Unrecognized PrimitiveType. This should '
                                'never happen; please file an issue.')

        # If this is an enum, select the first truthy value (or the zero
        # value if nothing else exists).
        if isinstance(self.type, EnumType):
            # Note: The slightly-goofy [:2][-1] lets us gracefully fall
            # back to index 0 if there is only one element.
            mock_value = self.type.values[:2][-1]
            answer = f'{self.type.ident}.{mock_value.name}'

        # If this is another message, set one value on the message.
        if isinstance(self.type, MessageType) and len(self.type.fields):
            sub = next(iter(self.type.fields.values()))
            answer = f'{self.type.ident}({sub.name}={sub.mock_value})'

        if self.map:
            # Maps are a special case beacuse they're represented internally as
            # a list of a generated type with two fields: 'key' and 'value'.
            answer = '{{{}: {}}}'.format(
                self.type.fields["key"].mock_value,
                self.type.fields["value"].mock_value,
            )
        elif self.repeated:
            # If this is a repeated field, then the mock answer should
            # be a list.
            answer = f'[{answer}]'

        # Done; return the mock value.
        return answer

    @property
    def proto_type(self) -> str:
        """Return the proto type constant to be used in templates."""
        return cast(str, descriptor_pb2.FieldDescriptorProto.Type.Name(
            self.field_pb.type,
        ))[len('TYPE_'):]

    @property
    def repeated(self) -> bool:
        """Return True if this is a repeated field, False otherwise.

        Returns:
            bool: Whether this field is repeated.
        """
        return self.label == \
            descriptor_pb2.FieldDescriptorProto.Label.Value(
                'LABEL_REPEATED')   # type: ignore

    @property
    def required(self) -> bool:
        """Return True if this is a required field, False otherwise.

        Returns:
            bool: Whether this field is required.
        """
        return (field_behavior_pb2.FieldBehavior.Value('REQUIRED') in
                self.options.Extensions[field_behavior_pb2.field_behavior])

    @utils.cached_property
    def type(self) -> Union['MessageType', 'EnumType', 'PrimitiveType']:
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
            return PrimitiveType.build(float)
        if self.field_pb.type in (3, 4, 5, 6, 7, 13, 15, 16, 17, 18):
            return PrimitiveType.build(int)
        if self.field_pb.type == 8:
            return PrimitiveType.build(bool)
        if self.field_pb.type == 9:
            return PrimitiveType.build(str)
        if self.field_pb.type == 12:
            return PrimitiveType.build(bytes)

        # This should never happen.
        raise TypeError(f'Unrecognized protobuf type: {self.field_pb.type}. '
                        'This code should not be reachable; please file a bug.')

    def with_context(self, *, collisions: FrozenSet[str]) -> 'Field':
        """Return a derivative of this field with the provided context.

        This method is used to address naming collisions. The returned
        ``Field`` object aliases module names to avoid naming collisions
        in the file being written.
        """
        return dataclasses.replace(
            self,
            message=self.message.with_context(
                collisions=collisions,
                skip_fields=True,
            ) if self.message else None,
            enum=self.enum.with_context(collisions=collisions)
            if self.enum else None,
            meta=self.meta.with_context(collisions=collisions),
        )


@dataclasses.dataclass(frozen=True)
class Oneof:
    """Description of a field."""
    oneof_pb: descriptor_pb2.OneofDescriptorProto

    def __getattr__(self, name):
        return getattr(self.oneof_pb, name)


@dataclasses.dataclass(frozen=True)
class MessageType:
    """Description of a message (defined with the ``message`` keyword)."""
    # Class attributes
    PATH_ARG_RE = re.compile(r'\{([a-zA-Z0-9_-]+)\}')

    # Instance attributes
    message_pb: descriptor_pb2.DescriptorProto
    fields: Mapping[str, Field]
    nested_enums: Mapping[str, 'EnumType']
    nested_messages: Mapping[str, 'MessageType']
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )
    oneofs: Optional[Mapping[str, 'Oneof']] = None

    def __getattr__(self, name):
        return getattr(self.message_pb, name)

    def __hash__(self):
        # Identity is sufficiently unambiguous.
        return hash(self.ident)

    def oneof_fields(self, include_optional=False):
        oneof_fields = collections.defaultdict(list)
        for field in self.fields.values():
            # Only include proto3 optional oneofs if explicitly looked for.
            if field.oneof and not field.proto3_optional or include_optional:
                oneof_fields[field.oneof].append(field)

        return oneof_fields

    @utils.cached_property
    def field_types(self) -> Sequence[Union['MessageType', 'EnumType']]:
        answer = tuple(
            field.type
            for field in self.fields.values()
            if field.message or field.enum
        )

        return answer

    @utils.cached_property
    def recursive_field_types(self) -> Sequence[
        Union['MessageType', 'EnumType']
    ]:
        """Return all composite fields used in this proto's messages."""
        types: Set[Union['MessageType', 'EnumType']] = set()

        stack = [iter(self.fields.values())]
        while stack:
            fields_iter = stack.pop()
            for field in fields_iter:
                if field.message and field.type not in types:
                    stack.append(iter(field.message.fields.values()))
                if not field.is_primitive:
                    types.add(field.type)

        return tuple(types)

    @property
    def map(self) -> bool:
        """Return True if the given message is a map, False otherwise."""
        return self.message_pb.options.map_entry

    @property
    def ident(self) -> metadata.Address:
        """Return the identifier data to be used in templates."""
        return self.meta.address

    @property
    def resource_path(self) -> Optional[str]:
        """If this message describes a resource, return the path to the resource.
        If there are multiple paths, returns the first one."""
        return next(
            iter(self.options.Extensions[resource_pb2.resource].pattern),
            None
        )

    @property
    def resource_type(self) -> Optional[str]:
        resource = self.options.Extensions[resource_pb2.resource]
        return resource.type[resource.type.find('/') + 1:] if resource else None

    @property
    def resource_path_args(self) -> Sequence[str]:
        return self.PATH_ARG_RE.findall(self.resource_path or '')

    @utils.cached_property
    def path_regex_str(self) -> str:
        # The indirection here is a little confusing:
        # we're using the resource path template as the base of a regex,
        # with each resource ID segment being captured by a regex.
        # E.g., the path schema
        # kingdoms/{kingdom}/phyla/{phylum}
        # becomes the regex
        # ^kingdoms/(?P<kingdom>.+?)/phyla/(?P<phylum>.+?)$
        parsing_regex_str = (
            "^" +
            self.PATH_ARG_RE.sub(
                # We can't just use (?P<name>[^/]+) because segments may be
                # separated by delimiters other than '/'.
                # Multiple delimiter characters within one schema are allowed,
                # e.g.
                # as/{a}-{b}/cs/{c}%{d}_{e}
                # This is discouraged but permitted by AIP4231
                lambda m: "(?P<{name}>.+?)".format(name=m.groups()[0]),
                self.resource_path or ''
            ) +
            "$"
        )
        return parsing_regex_str

    def get_field(self, *field_path: str,
                  collisions: FrozenSet[str] = frozenset()) -> Field:
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

        # Sanity check: If this cursor has no message, there is a problem.
        if not cursor.message:
            raise KeyError(
                f'Field {".".join(field_path)} could not be resolved from '
                f'{cursor.name}.',
            )

        # Recursion case: Pass the remainder of the path to the sub-field's
        # message.
        return cursor.message.get_field(*field_path[1:], collisions=collisions)

    def with_context(self, *,
                     collisions: FrozenSet[str],
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
        return dataclasses.replace(
            self,
            fields=collections.OrderedDict(
                (k, v.with_context(collisions=collisions))
                for k, v in self.fields.items()
            ) if not skip_fields else self.fields,
            nested_enums=collections.OrderedDict(
                (k, v.with_context(collisions=collisions))
                for k, v in self.nested_enums.items()
            ),
            nested_messages=collections.OrderedDict(
                (k, v.with_context(
                    collisions=collisions,
                    skip_fields=skip_fields,))
                for k, v in self.nested_messages.items()),
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

    def __hash__(self):
        # Identity is sufficiently unambiguous.
        return hash(self.ident)

    def __getattr__(self, name):
        return getattr(self.enum_pb, name)

    @property
    def resource_path(self) -> Optional[str]:
        # This is a minor duck-typing workaround for the resource_messages
        # property in the Service class: we need to check fields recursively
        # to see if they're resources, and recursive_field_types includes enums
        return None

    @property
    def ident(self) -> metadata.Address:
        """Return the identifier data to be used in templates."""
        return self.meta.address

    def with_context(self, *, collisions: FrozenSet[str]) -> 'EnumType':
        """Return a derivative of this enum with the provided context.

        This method is used to address naming collisions. The returned
        ``EnumType`` object aliases module names to avoid naming collisions in
        the file being written.
        """
        return dataclasses.replace(
            self,
            meta=self.meta.with_context(collisions=collisions),
        )


@dataclasses.dataclass(frozen=True)
class PythonType:
    """Wrapper class for Python types.

    This exists for interface consistency, so that methods like
    :meth:`Field.type` can return an object and the caller can be confident
    that a ``name`` property will be present.
    """
    meta: metadata.Metadata

    def __eq__(self, other):
        return self.meta == other.meta

    def __ne__(self, other):
        return not self == other

    @utils.cached_property
    def ident(self) -> metadata.Address:
        """Return the identifier to be used in templates."""
        return self.meta.address

    @property
    def name(self) -> str:
        return self.ident.name

    @property
    def field_types(self) -> Sequence[Union['MessageType', 'EnumType']]:
        return tuple()


@dataclasses.dataclass(frozen=True)
class PrimitiveType(PythonType):
    """A representation of a Python primitive type."""
    python_type: Optional[type]

    @classmethod
    def build(cls, primitive_type: Optional[type]):
        """Return a PrimitiveType object for the given Python primitive type.

        Args:
            primitive_type (cls): A Python primitive type, such as
                :class:`int` or :class:`str`. Despite not being a type,
                ``None`` is also accepted here.

        Returns:
            ~.PrimitiveType: The instantiated PrimitiveType object.
        """
        # Primitives have no import, and no module to reference, so the
        # address just uses the name of the class (e.g. "int", "str").
        return cls(meta=metadata.Metadata(address=metadata.Address(
            name='None' if primitive_type is None else primitive_type.__name__,
        )), python_type=primitive_type)

    def __eq__(self, other):
        # If we are sent the actual Python type (not the PrimitiveType object),
        # claim to be equal to that.
        if not hasattr(other, 'meta'):
            return self.python_type is other
        return super().__eq__(other)


@dataclasses.dataclass(frozen=True)
class OperationInfo:
    """Representation of long-running operation info."""
    response_type: MessageType
    metadata_type: MessageType

    def with_context(self, *, collisions: FrozenSet[str]) -> 'OperationInfo':
        """Return a derivative of this OperationInfo with the provided context.

          This method is used to address naming collisions. The returned
          ``OperationInfo`` object aliases module names to avoid naming collisions
          in the file being written.
          """
        return dataclasses.replace(
            self,
            response_type=self.response_type.with_context(
                collisions=collisions
            ),
            metadata_type=self.metadata_type.with_context(
                collisions=collisions
            ),
        )


@dataclasses.dataclass(frozen=True)
class RetryInfo:
    """Representation of the method's retry behavior."""
    max_attempts: int
    initial_backoff: float
    max_backoff: float
    backoff_multiplier: float
    retryable_exceptions: FrozenSet[exceptions.GoogleAPICallError]


@dataclasses.dataclass(frozen=True)
class Method:
    """Description of a method (defined with the ``rpc`` keyword)."""
    method_pb: descriptor_pb2.MethodDescriptorProto
    input: MessageType
    output: MessageType
    lro: Optional[OperationInfo] = dataclasses.field(default=None)
    retry: Optional[RetryInfo] = dataclasses.field(default=None)
    timeout: Optional[float] = None
    meta: metadata.Metadata = dataclasses.field(
        default_factory=metadata.Metadata,
    )

    def __getattr__(self, name):
        return getattr(self.method_pb, name)

    @utils.cached_property
    def client_output(self):
        return self._client_output(enable_asyncio=False)

    @utils.cached_property
    def client_output_async(self):
        return self._client_output(enable_asyncio=True)

    def flattened_oneof_fields(self, include_optional=False):
        oneof_fields = collections.defaultdict(list)
        for field in self.flattened_fields.values():
            # Only include proto3 optional oneofs if explicitly looked for.
            if field.oneof and not field.proto3_optional or include_optional:
                oneof_fields[field.oneof].append(field)

        return oneof_fields

    def _client_output(self, enable_asyncio: bool):
        """Return the output from the client layer.

        This takes into account transformations made by the outer GAPIC
        client to transform the output from the transport.

        Returns:
            Union[~.MessageType, ~.PythonType]:
                A description of the return type.
        """
        # Void messages ultimately return None.
        if self.void:
            return PrimitiveType.build(None)

        # If this method is an LRO, return a PythonType instance representing
        # that.
        if self.lro:
            return PythonType(meta=metadata.Metadata(
                address=metadata.Address(
                    name='AsyncOperation' if enable_asyncio else 'Operation',
                    module='operation_async' if enable_asyncio else 'operation',
                    package=('google', 'api_core'),
                    collisions=self.lro.response_type.ident.collisions,
                ),
                documentation=utils.doc(
                    'An object representing a long-running operation. \n\n'
                    'The result type for the operation will be '
                    ':class:`{ident}`: {doc}'.format(
                        doc=self.lro.response_type.meta.doc,
                        ident=self.lro.response_type.ident.sphinx,
                    ),
                ),
            ))

        # If this method is paginated, return that method's pager class.
        if self.paged_result_field:
            return PythonType(meta=metadata.Metadata(
                address=metadata.Address(
                    name=f'{self.name}AsyncPager' if enable_asyncio else f'{self.name}Pager',
                    package=self.ident.api_naming.module_namespace + (self.ident.api_naming.versioned_module_name,) + self.ident.subpackage + (
                        'services',
                        utils.to_snake_case(self.ident.parent[-1]),
                    ),
                    module='pagers',
                    collisions=self.input.ident.collisions,
                ),
                documentation=utils.doc(
                    f'{self.output.meta.doc}\n\n'
                    'Iterating over this object will yield results and '
                    'resolve additional pages automatically.',
                ),
            ))

        # Return the usual output.
        return self.output

    @property
    def field_headers(self) -> Sequence[str]:
        """Return the field headers defined for this method."""
        http = self.options.Extensions[annotations_pb2.http]

        pattern = re.compile(r'\{([a-z][\w\d_.]+)=')

        potential_verbs = [
            http.get,
            http.put,
            http.post,
            http.delete,
            http.patch,
            http.custom.path,
        ]

        return next((tuple(pattern.findall(verb)) for verb in potential_verbs if verb), ())

    @utils.cached_property
    def flattened_fields(self) -> Mapping[str, Field]:
        """Return the signature defined for this method."""
        cross_pkg_request = self.input.ident.package != self.ident.package

        def filter_fields(sig: str) -> Iterable[Tuple[str, Field]]:
            for f in sig.split(','):
                if not f:
                    # Special case for an empty signature
                    continue
                name = f.strip()
                field = self.input.get_field(*name.split('.'))
                if cross_pkg_request and not field.is_primitive:
                    # This is not a proto-plus wrapped message type,
                    # and setting a non-primitive field directly is verboten.
                    continue

                yield name, field

        signatures = self.options.Extensions[client_pb2.method_signature]
        answer: Dict[str, Field] = collections.OrderedDict(
            name_and_field
            for sig in signatures
            for name_and_field in filter_fields(sig)
        )

        return answer

    @utils.cached_property
    def flattened_field_to_key(self):
        return {field.name: key for key, field in self.flattened_fields.items()}

    @utils.cached_property
    def legacy_flattened_fields(self) -> Mapping[str, Field]:
        """Return the legacy flattening interface: top level fields only,
        required fields first"""
        required, optional = utils.partition(lambda f: f.required,
                                             self.input.fields.values())
        return collections.OrderedDict((f.name, f)
                                       for f in chain(required, optional))

    @property
    def grpc_stub_type(self) -> str:
        """Return the type of gRPC stub to use."""
        return '{client}_{server}'.format(
            client='stream' if self.client_streaming else 'unary',
            server='stream' if self.server_streaming else 'unary',
        )

    @utils.cached_property
    def idempotent(self) -> bool:
        """Return True if we know this method is idempotent, False otherwise.

        Note: We are intentionally conservative here. It is far less bad
        to falsely believe an idempotent method is non-idempotent than
        the converse.
        """
        return bool(self.options.Extensions[annotations_pb2.http].get)

    @property
    def ident(self) -> metadata.Address:
        """Return the identifier data to be used in templates."""
        return self.meta.address

    @utils.cached_property
    def paged_result_field(self) -> Optional[Field]:
        """Return the response pagination field if the method is paginated."""
        # If the request field lacks any of the expected pagination fields,
        # then the method is not paginated.
        for page_field in ((self.input, int, 'page_size'),
                           (self.input, str, 'page_token'),
                           (self.output, str, 'next_page_token')):
            field = page_field[0].fields.get(page_field[2], None)
            if not field or field.type != page_field[1]:
                return None

        # Return the first repeated field.
        for field in self.output.fields.values():
            if field.repeated:
                return field

        # We found no repeated fields. Return None.
        return None

    @utils.cached_property
    def ref_types(self) -> Sequence[Union[MessageType, EnumType]]:
        return self._ref_types(True)

    @utils.cached_property
    def flat_ref_types(self) -> Sequence[Union[MessageType, EnumType]]:
        return self._ref_types(False)

    def _ref_types(self, recursive: bool) -> Sequence[Union[MessageType, EnumType]]:
        """Return types referenced by this method."""
        # Begin with the input (request) and output (response) messages.
        answer: List[Union[MessageType, EnumType]] = [self.input]
        types: Iterable[Union[MessageType, EnumType]] = (
            self.input.recursive_field_types if recursive
            else (
                f.type
                for f in self.flattened_fields.values()
                if f.message or f.enum
            )
        )
        answer.extend(types)

        if not self.void:
            answer.append(self.client_output)
            answer.extend(self.client_output.field_types)
            answer.append(self.client_output_async)
            answer.extend(self.client_output_async.field_types)

        # If this method has LRO, it is possible (albeit unlikely) that
        # the LRO messages reside in a different module.
        if self.lro:
            answer.append(self.lro.response_type)
            answer.append(self.lro.metadata_type)

        # If this message paginates its responses, it is possible
        # that the individual result messages reside in a different module.
        if self.paged_result_field and self.paged_result_field.message:
            answer.append(self.paged_result_field.message)

        # Done; return the answer.
        return tuple(answer)

    @property
    def void(self) -> bool:
        """Return True if this method has no return value, False otherwise."""
        return self.output.ident.proto == 'google.protobuf.Empty'

    def with_context(self, *, collisions: FrozenSet[str]) -> 'Method':
        """Return a derivative of this method with the provided context.

        This method is used to address naming collisions. The returned
        ``Method`` object aliases module names to avoid naming collisions
        in the file being written.
        """
        maybe_lro = self.lro.with_context(
            collisions=collisions
        ) if self.lro else None

        return dataclasses.replace(
            self,
            lro=maybe_lro,
            input=self.input.with_context(collisions=collisions),
            output=self.output.with_context(collisions=collisions),
            meta=self.meta.with_context(collisions=collisions),
        )


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
    def client_name(self) -> str:
        """Returns the name of the generated client class"""
        return self.name + "Client"

    @property
    def async_client_name(self) -> str:
        """Returns the name of the generated AsyncIO client class"""
        return self.name + "AsyncClient"

    @property
    def transport_name(self):
        return self.name + "Transport"

    @property
    def grpc_transport_name(self):
        return self.name + "GrpcTransport"

    @property
    def grpc_asyncio_transport_name(self):
        return self.name + "GrpcAsyncIOTransport"

    @property
    def has_lro(self) -> bool:
        """Return whether the service has a long-running method."""
        return any([m.lro for m in self.methods.values()])

    @property
    def has_pagers(self) -> bool:
        """Return whether the service has paged methods."""
        return any(m.paged_result_field for m in self.methods.values())

    @property
    def host(self) -> str:
        """Return the hostname for this service, if specified.

        Returns:
            str: The hostname, with no protocol and no trailing ``/``.
        """
        if self.options.Extensions[client_pb2.default_host]:
            return self.options.Extensions[client_pb2.default_host]
        return ''

    @property
    def oauth_scopes(self) -> Sequence[str]:
        """Return a sequence of oauth scopes, if applicable.

        Returns:
            Sequence[str]: A sequence of OAuth scopes.
        """
        # Return the OAuth scopes, split on comma.
        return tuple(
            i.strip()
            for i in self.options.Extensions[client_pb2.oauth_scopes].split(',')
            if i
        )

    @property
    def module_name(self) -> str:
        """Return the appropriate module name for this service.

        Returns:
            str: The service name, in snake case.
        """
        return utils.to_snake_case(self.name)

    @utils.cached_property
    def names(self) -> FrozenSet[str]:
        """Return a set of names used in this service.

        This is used for detecting naming collisions in the module names
        used for imports.
        """
        # Put together a set of the service and method names.
        answer = {self.name, self.client_name, self.async_client_name}
        answer.update(
            utils.to_snake_case(i.name) for i in self.methods.values()
        )

        # Identify any import module names where the same module name is used
        # from distinct packages.
        modules: Dict[str, Set[str]] = collections.defaultdict(set)
        for m in self.methods.values():
            for t in m.ref_types:
                modules[t.ident.module].add(t.ident.package)

        answer.update(
            module_name
            for module_name, packages in modules.items()
            if len(packages) > 1
        )

        # Done; return the answer.
        return frozenset(answer)

    @utils.cached_property
    def resource_messages(self) -> FrozenSet[MessageType]:
        """Returns all the resource message types used in all
        request fields in the service."""
        def gen_resources(message):
            if message.resource_path:
                yield message

            for type_ in message.recursive_field_types:
                if type_.resource_path:
                    yield type_

        return frozenset(
            resource_msg
            for method in self.methods.values()
            for resource_msg in gen_resources(method.input)
        )

    @utils.cached_property
    def any_client_streaming(self) -> bool:
        return any(m.client_streaming for m in self.methods.values())

    @utils.cached_property
    def any_server_streaming(self) -> bool:
        return any(m.server_streaming for m in self.methods.values())

    def with_context(self, *, collisions: FrozenSet[str]) -> 'Service':
        """Return a derivative of this service with the provided context.

        This method is used to address naming collisions. The returned
        ``Service`` object aliases module names to avoid naming collisions
        in the file being written.
        """
        return dataclasses.replace(
            self,
            methods=collections.OrderedDict(
                (k, v.with_context(
                    # A methodd's flattened fields create additional names
                    # that may conflict with module imports.
                    collisions=collisions | frozenset(v.flattened_fields.keys()))
                 )
                for k, v in self.methods.items()
            ),
            meta=self.meta.with_context(collisions=collisions),
        )
