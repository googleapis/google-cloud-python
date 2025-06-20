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

import google.cloud.bigquery as bigquery

import bigframes.core.compile.googlesql.abc as abc
import bigframes.core.compile.googlesql.expression as expr

"""This module provides a structured representation of GoogleSQL syntax using nodes.
Each node's name and child nodes are designed to strictly follow the official GoogleSQL
syntax rules outlined in the documentation:
https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax"""

TABLE_SOURCE_TYPE = typing.Union[str, bigquery.TableReference]


@dataclasses.dataclass
class QueryExpr(abc.SQLSyntax):
    """This class represents GoogleSQL `query_expr` syntax."""

    select: Select
    with_cte_list: typing.Sequence[NonRecursiveCTE] = ()

    def sql(self) -> str:
        text = []
        if len(self.with_cte_list) > 0:
            with_cte_text = ",\n".join(
                [with_cte.sql() for with_cte in self.with_cte_list]
            )
            text.append(f"WITH {with_cte_text}")

        text.append(self.select.sql())
        return "\n".join(text)


@dataclasses.dataclass
class Select(abc.SQLSyntax):
    """This class represents GoogleSQL `select` syntax."""

    select_list: typing.Sequence[
        typing.Union[SelectExpression, SelectAll]
    ] = dataclasses.field(default_factory=list)
    from_clause_list: typing.Sequence[FromClause] = dataclasses.field(
        default_factory=list
    )
    distinct: bool = False

    def select(
        self,
        columns: typing.Union[
            typing.Iterable[str], typing.Iterable[tuple[str, str]], str, None
        ] = None,
        distinct: bool = False,
    ) -> Select:
        if isinstance(columns, str):
            columns = [columns]
        self.select_list: typing.List[typing.Union[SelectExpression, SelectAll]] = (
            [self._select_field(column) for column in columns]
            if columns
            else [SelectAll(expression=expr.StarExpression())]
        )
        self.distinct = distinct
        return self

    def _select_field(self, field) -> SelectExpression:
        if isinstance(field, str):
            return SelectExpression(expression=expr.ColumnExpression(name=field))

        else:
            alias = (
                expr.AliasExpression(field[1])
                if isinstance(field[1], str)
                else field[1]
                if (field[0] != field[1])
                else None
            )
            return SelectExpression(
                expression=expr.ColumnExpression(name=field[0]), alias=alias
            )

    def from_(
        self,
        sources: typing.Union[TABLE_SOURCE_TYPE, typing.Iterable[TABLE_SOURCE_TYPE]],
    ) -> Select:
        if (not isinstance(sources, typing.Iterable)) or isinstance(sources, str):
            sources = [sources]
        self.from_clause_list = [
            FromClause(FromItem.from_source(source)) for source in sources
        ]
        return self

    def sql(self) -> str:
        if (self.select_list is not None) and (not self.select_list):
            raise ValueError("Select clause has not been properly initialized.")

        text = ["SELECT"]

        if self.distinct:
            text.append("DISTINCT")

        select_list_sql = ",\n".join([select.sql() for select in self.select_list])
        text.append(select_list_sql)

        if self.from_clause_list:
            from_clauses_sql = ",\n".join(
                [clause.sql() for clause in self.from_clause_list]
            )
            text.append(f"FROM\n{from_clauses_sql}")
        return "\n".join(text)


@dataclasses.dataclass(frozen=True)
class SelectExpression(abc.SQLSyntax):
    """This class represents `select_expression`."""

    expression: expr.ColumnExpression
    alias: typing.Optional[expr.AliasExpression] = None

    def sql(self) -> str:
        if self.alias is None:
            return self.expression.sql()
        else:
            return f"{self.expression.sql()} AS {self.alias.sql()}"


@dataclasses.dataclass
class SelectAll(abc.SQLSyntax):
    """This class represents `select_all` (aka. `SELECT *`)."""

    expression: expr.StarExpression

    def sql(self) -> str:
        return self.expression.sql()


@dataclasses.dataclass
class FromClause(abc.SQLSyntax):
    """This class represents GoogleSQL `from_clause` syntax."""

    from_item: FromItem

    def sql(self) -> str:
        return self.from_item.sql()


@dataclasses.dataclass
class FromItem(abc.SQLSyntax):
    """This class represents GoogleSQL `from_item` syntax."""

    # Note: Temporarily introduces the `str` type to interact with pre-existing,
    # compiled SQL strings.
    expression: typing.Union[expr.TableExpression, QueryExpr, str, expr.CTEExpression]
    as_alias: typing.Optional[AsAlias] = None

    @classmethod
    def from_source(
        cls,
        subquery_or_tableref: typing.Union[bigquery.TableReference, str],
        as_alias: typing.Optional[AsAlias] = None,
    ):
        if isinstance(subquery_or_tableref, bigquery.TableReference):
            return cls(
                expression=expr.TableExpression(
                    table_id=subquery_or_tableref.table_id,
                    dataset_id=subquery_or_tableref.dataset_id,
                    project_id=subquery_or_tableref.project,
                ),
                as_alias=as_alias,
            )
        elif isinstance(subquery_or_tableref, str):
            return cls(
                expression=subquery_or_tableref,
                as_alias=as_alias,
            )
        else:
            raise ValueError("The source must be bigquery.TableReference or str.")

    def sql(self) -> str:
        if isinstance(self.expression, (expr.TableExpression, expr.CTEExpression)):
            text = self.expression.sql()
        elif isinstance(self.expression, str):
            text = f"({self.expression})"
        elif isinstance(self.expression, QueryExpr):
            text = f"({self.expression.sql()})"
        else:
            raise ValueError(
                f"Unsupported expression type {type(self.expression).__name__};"
                "expected one of TableExpression, QueryExpr, str, or CTEExpression."
            )

        if self.as_alias is None:
            return text
        else:
            return f"{text} {self.as_alias.sql()}"


@dataclasses.dataclass
class NonRecursiveCTE(abc.SQLSyntax):
    """This class represents GoogleSQL `non_recursive_cte` syntax."""

    cte_name: expr.CTEExpression
    query_expr: QueryExpr

    def sql(self) -> str:
        return f"{self.cte_name.sql()} AS (\n{self.query_expr.sql()}\n)"


@dataclasses.dataclass
class AsAlias(abc.SQLSyntax):
    """This class represents GoogleSQL `as_alias` syntax."""

    alias: expr.AliasExpression

    def sql(self) -> str:
        return f"AS {self.alias.sql()}"
