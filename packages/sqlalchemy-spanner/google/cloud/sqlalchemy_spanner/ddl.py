# Copyright 2026 Google LLC
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

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DDLElement


class DropColumn(DDLElement):
    """DDL element for dropping a column in Spanner."""

    def __init__(self, table, name):
        self.table = table
        self.name = name

    def reverse(self):
        raise NotImplementedError(
            "DropColumn reverse requires full column type definition."
        )


class AddTokenlistColumn(DDLElement):
    """DDL element for adding a generated TOKENLIST column in Spanner."""

    def __init__(self, table, name, expr, hidden=True):
        self.table = table
        self.name = name
        self.expr = expr
        self.hidden = hidden

    def reverse(self):
        return DropColumn(self.table, self.name)


class CreateSearchIndex(DDLElement):
    """DDL element for creating a SEARCH INDEX in Spanner."""

    def __init__(self, name, table, columns, storing=None):
        self.name = name
        self.table = table
        self.columns = columns
        self.storing = storing or []

    def reverse(self):
        return DropSearchIndex(self.name)


class DropSearchIndex(DDLElement):
    """DDL element for dropping a SEARCH INDEX in Spanner."""

    def __init__(self, name):
        self.name = name


class CreatePropertyGraph(DDLElement):
    """DDL element for creating a PROPERTY GRAPH in Spanner."""

    def __init__(self, name, definition):
        self.name = name
        self.definition = definition

    def reverse(self):
        return DropPropertyGraph(self.name)


class DropPropertyGraph(DDLElement):
    """DDL element for dropping a PROPERTY GRAPH in Spanner."""

    def __init__(self, name):
        self.name = name


@compiles(DropColumn, "spanner+spanner")
def _compile_drop_column(element, compiler, **kw):
    table_name = compiler.preparer.quote(element.table)
    col_name = compiler.preparer.quote(element.name)
    return f"ALTER TABLE {table_name} DROP COLUMN {col_name}"


@compiles(AddTokenlistColumn, "spanner+spanner")
def _compile_add_tokenlist_column(element, compiler, **kw):
    table_name = compiler.preparer.quote(element.table)
    col_name = compiler.preparer.quote(element.name)
    hidden_str = " HIDDEN" if element.hidden else ""
    return (
        f"ALTER TABLE {table_name} "
        f"ADD COLUMN {col_name} TOKENLIST AS ({element.expr}){hidden_str}"
    )


@compiles(CreateSearchIndex, "spanner+spanner")
def _compile_create_search_index(element, compiler, **kw):
    cols = ", ".join(element.columns)
    sql = f"CREATE SEARCH INDEX {element.name} ON {element.table} ({cols})"
    if element.storing:
        storing_cols = ", ".join(element.storing)
        sql += f" STORING ({storing_cols})"
    return sql


@compiles(DropSearchIndex, "spanner+spanner")
def _compile_drop_search_index(element, compiler, **kw):
    return f"DROP SEARCH INDEX IF EXISTS {element.name}"


@compiles(CreatePropertyGraph, "spanner+spanner")
def _compile_create_property_graph(element, compiler, **kw):
    return f"CREATE PROPERTY GRAPH {element.name} {element.definition}"


@compiles(DropPropertyGraph, "spanner+spanner")
def _compile_drop_property_graph(element, compiler, **kw):
    return f"DROP PROPERTY GRAPH IF EXISTS {element.name}"
