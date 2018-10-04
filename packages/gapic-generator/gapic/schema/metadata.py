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

"""The ``metadata`` module defines schema for where data was parsed from.
This library places every protocol buffer descriptor in a wrapper class
(see :mod:`~.wrappers`) before loading it into the :class:`~.API` object.

As we iterate over descriptors during the loading process, it is important
to know where they came from, because sometimes protocol buffer types are
referenced by fully-qualified string (e.g. ``method.input_type``), and we
want to resolve those references.

Additionally, protocol buffers stores data from the comments in the ``.proto``
in a separate structure, and this object model re-connects the comments
with the things they describe for easy access in templates.
"""

import dataclasses
from typing import Sequence, Tuple

from google.protobuf import descriptor_pb2

from gapic.schema import naming


@dataclasses.dataclass(frozen=True)
class Address:
    name: str = ''
    module: str = ''
    module_path: Tuple[int] = dataclasses.field(default_factory=tuple)
    package: Tuple[str] = dataclasses.field(default_factory=tuple)
    parent: Tuple[str] = dataclasses.field(default_factory=tuple)
    api_naming: naming.Naming = dataclasses.field(
        default_factory=naming.Naming,
    )

    def __str__(self) -> str:
        """Return the Python identifier for this type.

        Because we import modules as a whole, rather than individual
        members from modules, this is consistently `module.Name`.
        """
        if self.module:
            return '.'.join((self.module,) + self.parent + (self.name,))
        return '.'.join(self.parent + (self.name,))

    @property
    def proto(self) -> str:
        """Return the proto selector for this type."""
        return '.'.join(self.package + self.parent + (self.name,))

    @property
    def proto_package(self) -> str:
        """Return the proto package for this type."""
        return '.'.join(self.package)

    @property
    def python_import(self) -> Tuple[Sequence[str], str]:
        """Return the Python import for this type."""
        # If there is no naming object, this is a special case for operation.
        # FIXME(#34): OperationType does not work well. Fix or expunge it.
        if not self.api_naming:
            return ('.'.join(self.package), self.module)

        # If this is part of the proto package that we are generating,
        # rewrite the package to our structure.
        if self.proto_package.startswith(self.api_naming.proto_package):
            return (
                '.'.join(self.api_naming.module_namespace + (
                    self.api_naming.versioned_module_name,
                    'types',
                )),
                self.module,
            )

        # Return the standard import.
        return ('.'.join(self.package), f'{self.module}_pb2')

    @property
    def sphinx(self) -> str:
        """Return the Sphinx identifier for this type."""
        if self.module:
            return f'~.{self}'
        return self.name

    def child(self, child_name: str, path: Tuple[int]) -> 'Address':
        """Return a new child of the current Address.

        Args:
            child_name (str): The name of the child node.
                This address' name is appended to ``parent``.

        Returns:
            ~.Address: The new address object.
        """
        return type(self)(
            api_naming=self.api_naming,
            module=self.module,
            module_path=self.module_path + path,
            name=child_name,
            package=self.package,
            parent=self.parent + (self.name,) if self.name else self.parent,
        )

    def rel(self, address: 'Address') -> str:
        """Return an identifier for this type, relative to the given address.

        Similar to :meth:`__str__`, but accepts an address (expected to be the
        module being written) and truncates the beginning module if the
        address matches the identifier's address. Templates can use this in
        situations where otherwise they would refer to themselves.

        Args:
            address (~.metadata.Address): The address to compare against.

        Returns:
            str: The appropriate identifier.
        """
        # Is this referencing a message in the same proto file?
        if self.package == address.package and self.module == address.module:
            # It is possible that a field references a message that has
            # not yet been declared. If so, send its name enclosed in quotes
            # (a string) instead.
            if (len(self.module_path) == len(address.module_path) and
                    self.module_path > address.module_path or
                    self == address):
                return f"'{self.name}'"

            # Edge case: If two (or more) messages are nested under a common
            # parent message, and one references another, then return that
            # enclosed in quotes.
            #
            # The reason for this is that each nested class creates a new
            # scope in Python, without reference to the parent class being
            # created, so there is no way for one nested class to reference
            # another at class instantiation time.
            if (self.parent and address.parent and
                    self.parent[0] == address.parent[0]):
                return f"'{'.'.join(self.parent)}.{self.name}'"

            # Edge case: Similar to above, if this is a message that is
            # referencing a nested message that it contains, we need
            # the message to be referenced relative to this message's
            # namespace.
            if self.parent and self.parent[0] == address.name:
                return '.'.join(self.parent[1:] + (self.name,))

            # This is a message in the same module, already declared.
            # Send its name.
            return '.'.join(self.parent + (self.name,))

        # Return the usual `module.Name`.
        return f'_.{str(self)}'

    def resolve(self, selector: str) -> str:
        """Resolve a potentially-relative protobuf selector.

        This takes a protobuf selector which may be fully-qualified
        (e.g. `foo.bar.v1.Baz`) or may be relative (`Baz`) and
        returns the fully-qualified version.

        This method is naive and does not check to see if the message
        actually exists.

        Args:
            selector (str): A protobuf selector, either fully-qualified
                or relative.

        Returns:
            str: An absolute selector.
        """
        if '.' not in selector:
            return f'{".".join(self.package)}.{selector}'
        return selector


@dataclasses.dataclass(frozen=True)
class Metadata:
    address: Address = dataclasses.field(default_factory=Address)
    documentation: descriptor_pb2.SourceCodeInfo.Location = dataclasses.field(
        default_factory=descriptor_pb2.SourceCodeInfo.Location,
    )

    @property
    def doc(self):
        """Return the best comment.

        This property prefers the leading comment if one is available,
        and falls back to a trailing comment or a detached comment otherwise.

        If there are no comments, return empty string. (This means a template
        is always guaranteed to get a string.)
        """
        if self.documentation.leading_comments:
            return self.documentation.leading_comments.strip()
        if self.documentation.trailing_comments:
            return self.documentation.trailing_comments.strip()
        if self.documentation.leading_detached_comments:
            return '\n\n'.join(self.documentation.leading_detached_comments)
        return ''


@dataclasses.dataclass(frozen=True)
class FieldIdentifier:
    ident: Address
    repeated: bool

    def __str__(self) -> str:
        if self.repeated:
            return f'Sequence[{self.ident}]'
        return str(self.ident)

    @property
    def sphinx(self) -> str:
        if self.repeated:
            return f'Sequence[{self.ident.sphinx}]'
        return self.ident.sphinx
