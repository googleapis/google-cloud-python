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
from sqlalchemy import text, Table, Column, Integer, PrimaryKeyConstraint, String
from sqlalchemy.testing import eq_
from sqlalchemy.testing.plugin.plugin_base import fixtures


class TestBasics(fixtures.TablesTest):
    @classmethod
    def define_tables(cls, metadata):
        Table(
            "numbers",
            metadata,
            Column("number", Integer),
            Column("name", String(20)),
            PrimaryKeyConstraint("number"),
        )

    def test_hello_world(self, connection):
        greeting = connection.execute(text("select 'Hello World'"))
        eq_("Hello World", greeting.fetchone()[0])

    def test_insert_number(self, connection):
        connection.execute(
            text("insert or update into numbers(number, name) values (1, 'One')")
        )
        name = connection.execute(text("select name from numbers where number=1"))
        eq_("One", name.fetchone()[0])
