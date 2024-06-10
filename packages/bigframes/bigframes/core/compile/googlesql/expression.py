# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import dataclasses
import typing

import bigframes.core.compile.googlesql.abc as abc

"""This module represents GoogleSQL `expression` and its extensions.
Core class:

* `expression`: Models basic SQL expressions.

Extended classes (not part of standard GoogleSQL syntax, but added for convenience):

* `ColumnExpression`:  Represents column references.
* `TableExpression`:   Represents table references.
* `AliasExpression`:   Represents aliased expressions.
* ...
"""


@dataclasses.dataclass
class Expression(abc.SQLSyntax):
    pass


@dataclasses.dataclass
class ColumnExpression(Expression):
    name: str
    parent: typing.Optional[TableExpression | AliasExpression | CTEExpression] = None

    def sql(self) -> str:
        if self.parent is not None:
            return f"{self.parent.sql()}.`{self.name}`"
        return f"`{self.name}`"


@dataclasses.dataclass
class StarExpression(Expression):
    parent: typing.Optional[TableExpression | AliasExpression | CTEExpression] = None

    def sql(self) -> str:
        if self.parent is not None:
            return f"{self.parent.sql()}.*"
        return "*"


@dataclasses.dataclass
class TableExpression(Expression):
    table_id: str
    dataset_id: typing.Optional[str] = None
    project_id: typing.Optional[str] = None

    def __post_init__(self):
        if self.project_id is not None and self.dataset_id is None:
            raise ValueError("The `dataset_id` is missing.")

    def sql(self) -> str:
        text = []
        if self.project_id is not None:
            text.append(f"`{self.project_id}`")
        if self.dataset_id is not None:
            text.append(f"`{self.dataset_id}`")
        text.append(f"`{self.table_id}`")
        return ".".join(text)


@dataclasses.dataclass
class AliasExpression(Expression):
    alias: str

    def sql(self) -> str:
        return f"`{self.alias}`"


@dataclasses.dataclass
class CTEExpression(Expression):
    name: str

    def sql(self) -> str:
        return f"`{self.name}`"
