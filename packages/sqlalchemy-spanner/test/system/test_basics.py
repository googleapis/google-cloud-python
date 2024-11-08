# Copyright 2024 Google LLC All rights reserved.
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

from sqlalchemy import (
    text,
    Table,
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    Index,
    MetaData,
    Boolean,
)
from sqlalchemy.testing import eq_
from sqlalchemy.testing.plugin.plugin_base import fixtures


class TestBasics(fixtures.TablesTest):
    @classmethod
    def define_tables(cls, metadata):
        numbers = Table(
            "numbers",
            metadata,
            Column("number", Integer),
            Column("name", String(20)),
            Column("alternative_name", String(20)),
            Column("prime", Boolean),
            PrimaryKeyConstraint("number"),
        )
        Index(
            "idx_numbers_name",
            numbers.c.name,
            numbers.c.prime.desc(),
            spanner_storing=[numbers.c.alternative_name],
        )

    def test_hello_world(self, connection):
        greeting = connection.execute(text("select 'Hello World'"))
        eq_("Hello World", greeting.fetchone()[0])

    def test_insert_number(self, connection):
        connection.execute(
            text(
                """insert or update into numbers (number, name, prime)
                   values (1, 'One', false)"""
            )
        )
        name = connection.execute(text("select name from numbers where number=1"))
        eq_("One", name.fetchone()[0])

    def test_reflect(self, connection):
        engine = connection.engine
        meta: MetaData = MetaData()
        meta.reflect(bind=engine)
        eq_(1, len(meta.tables))
        table = meta.tables["numbers"]
        eq_(1, len(table.indexes))
        index = next(iter(table.indexes))
        eq_(2, len(index.columns))
        eq_("name", index.columns[0].name)
        eq_("prime", index.columns[1].name)
        dialect_options = index.dialect_options["spanner"]
        eq_(1, len(dialect_options["storing"]))
        eq_("alternative_name", dialect_options["storing"][0])
