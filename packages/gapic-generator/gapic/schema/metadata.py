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
from typing import Tuple

from google.protobuf import descriptor_pb2


@dataclasses.dataclass(frozen=True)
class Address:
    name: str = ''
    module: str = ''
    package: Tuple[str] = dataclasses.field(default_factory=tuple)
    parent: Tuple[str] = dataclasses.field(default_factory=tuple)

    def __str__(self) -> str:
        """Return the Python identifier for this type.

        Because we import modules as a whole, rather than individual
        members from modules, this is consistently `module.Name`.
        """
        # TODO(#34): Special cases are not special enough to break the rules.
        #            Allowing this temporarily because it will be fixed by
        #            refactoring proto generation and/or OperationType.
        if self.package == ('google', 'api_core'):
            return f'{self.module}.{self.name}'
        if self.module:
            return f'{self.module}_pb2.{self.name}'
        return self.name

    @property
    def proto(self) -> str:
        """Return the proto selector for this type."""
        return '.'.join(self.package + self.parent + (self.name,))

    @property
    def proto_package(self) -> str:
        """Return the proto package for this type."""
        return '.'.join(self.package)

    @property
    def sphinx(self) -> str:
        """Return the Sphinx identifier for this type."""
        if self.module:
            return f'~.{self}'
        return self.name

    def child(self, child_name: str) -> 'Address':
        """Return a new child of the current Address.

        Args:
            child_name (str): The name of the child node.
                This address' name is appended to ``parent``.

        Returns:
            ~.Address: The new address object.
        """
        return type(self)(
            name=child_name,
            module=self.module,
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
        if self.package == address.package and self.module == address.module:
            return self.name
        return str(self)

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
