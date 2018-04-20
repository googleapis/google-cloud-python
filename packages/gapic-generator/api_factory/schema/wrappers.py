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

import dataclasses
from typing import List, Mapping, Sequence, Tuple

from google.protobuf import descriptor_pb2

from api_factory import utils
from api_factory.schema.metadata import Metadata
from api_factory.schema.pb import client_pb2
from api_factory.schema.pb import overload_pb2


@dataclasses.dataclass(frozen=True)
class Field:
    """Description of a field."""
    field_pb: descriptor_pb2.FieldDescriptorProto
    meta: Metadata = dataclasses.field(default_factory=Metadata)

    def __getattr__(self, name):
        return getattr(self.field_pb, name)


@dataclasses.dataclass(frozen=True)
class MessageType:
    """Description of a message (defined with the ``message`` keyword)."""
    message_pb: descriptor_pb2.DescriptorProto
    fields: Mapping[str, Field]
    meta: Metadata = dataclasses.field(default_factory=Metadata)

    def __getattr__(self, name):
        return getattr(self.message_pb, name)

    @property
    def pb2_module(self) -> str:
        """Return the name of the Python pb2 module."""
        return f'{self.meta.address.module}_pb2'

    @property
    def proto_path(self) -> str:
        """Return the fully qualfied proto path as a string."""
        return f'{str(self.meta.address)}.{self.name}'


@dataclasses.dataclass(frozen=True)
class EnumValueType:
    """Description of an enum value."""
    enum_value_pb: descriptor_pb2.EnumValueDescriptorProto
    meta: Metadata = dataclasses.field(default_factory=Metadata)

    def __getattr__(self, name):
        return getattr(self.enum_value_pb, name)


@dataclasses.dataclass(frozen=True)
class EnumType:
    """Description of an enum (defined with the ``enum`` keyword.)"""
    enum_pb: descriptor_pb2.EnumDescriptorProto
    values: List[EnumValueType]
    meta: Metadata = dataclasses.field(default_factory=Metadata)

    def __getattr__(self, name):
        return getattr(self.enum_pb, name)


@dataclasses.dataclass(frozen=True)
class Method:
    """Description of a method (defined with the ``rpc`` keyword)."""
    method_pb: descriptor_pb2.MethodDescriptorProto
    input: MessageType
    output: MessageType
    meta: Metadata = dataclasses.field(default_factory=Metadata)

    def __getattr__(self, name):
        return getattr(self.method_pb, name)

    @property
    def overloads(self):
        """Return the overloads defined for this method."""
        return self.method_pb.options.Extensions[overload_pb2.overloads]


@dataclasses.dataclass(frozen=True)
class Service:
    """Description of a service (defined with the ``service`` keyword)."""
    service_pb: descriptor_pb2.ServiceDescriptorProto
    methods: Mapping[str, Method]
    meta: Metadata = dataclasses.field(default_factory=Metadata)

    def __getattr__(self, name):
        return getattr(self.service_pb, name)

    @property
    def host(self) -> str:
        """Return the hostname for this service, if specified.

        Returns:
            str: The hostname, with no protocol and no trailing ``/``.
        """
        if self.service_pb.options.Extensions[client_pb2.host]:
            return self.service_pb.options.Extensions[client_pb2.host]
        return utils.Placeholder('<<< HOSTNAME >>>')

    @property
    def oauth_scopes(self) -> Sequence[str]:
        """Return a sequence of oauth scopes, if applicable.

        Returns:
            Sequence[str]: A sequence of OAuth scopes.
        """
        if self.service_pb.options.Extensions[client_pb2.oauth_scopes]:
            return self.service_pb.options.Extensions[client_pb2.oauth_scopes]
        return ()

    @property
    def module_name(self) -> str:
        """Return the appropriate module name for this service.

        Returns:
            str: The service name, in snake case.
        """
        return utils.to_snake_case(self.name)

    @property
    def pb2_modules(self) -> Sequence[Tuple[str, str]]:
        """Return a sequence of pb2 modules, for import.

        The results of this method are in alphabetical order (by package,
        then module), and do not contain duplicates.

        Returns:
            Sequence[str, str]: The package and pb2_module pair, intended
            for use in a ``from package import pb2_module`` type
            of statement.
        """
        answer = set()
        for method in self.methods.values():
            answer.add((
                '.'.join(method.input.meta.address.package),
                method.input.pb2_module,
            ))
            answer.add((
                '.'.join(method.output.meta.address.package),
                method.output.pb2_module,
            ))
        return sorted(answer)
