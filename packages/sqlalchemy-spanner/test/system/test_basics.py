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

from typing import Optional
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
    BIGINT,
    select,
)
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import REAL
from sqlalchemy.testing import eq_, is_true
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
            Column("ln", REAL),
            PrimaryKeyConstraint("number"),
        )
        Index(
            "idx_numbers_name",
            numbers.c.name,
            numbers.c.prime.desc(),
            spanner_storing=[numbers.c.alternative_name],
        )
        Table(
            "users",
            metadata,
            Column("ID", Integer, primary_key=True),
            Column("name", String(20)),
        )

    def test_hello_world(self, connection):
        greeting = connection.execute(text("select 'Hello World'"))
        eq_("Hello World", greeting.fetchone()[0])

    def test_insert_number(self, connection):
        connection.execute(
            text(
                """insert or update into numbers (number, name, prime, ln)
                   values (1, 'One', false, cast(ln(1) as float32))"""
            )
        )
        name = connection.execute(text("select name from numbers where number=1"))
        eq_("One", name.fetchone()[0])

    def test_reflect(self, connection):
        engine = connection.engine
        meta: MetaData = MetaData()
        meta.reflect(bind=engine)
        eq_(2, len(meta.tables))
        table = meta.tables["numbers"]
        eq_(5, len(table.columns))
        eq_("number", table.columns[0].name)
        eq_(BIGINT, type(table.columns[0].type))
        eq_("name", table.columns[1].name)
        eq_(String, type(table.columns[1].type))
        eq_("alternative_name", table.columns[2].name)
        eq_(String, type(table.columns[2].type))
        eq_("prime", table.columns[3].name)
        eq_(Boolean, type(table.columns[3].type))
        eq_("ln", table.columns[4].name)
        eq_(REAL, type(table.columns[4].type))
        eq_(1, len(table.indexes))
        index = next(iter(table.indexes))
        eq_(2, len(index.columns))
        eq_("name", index.columns[0].name)
        eq_("prime", index.columns[1].name)
        dialect_options = index.dialect_options["spanner"]
        eq_(1, len(dialect_options["storing"]))
        eq_("alternative_name", dialect_options["storing"][0])

    def test_table_name_overlapping_with_system_table(self, connection):
        class Base(DeclarativeBase):
            pass

        class Role(Base):
            __tablename__ = "roles"
            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            name: Mapped[str] = mapped_column(String(100), nullable=True)
            type: Mapped[str] = mapped_column(String(100), nullable=True)
            description: Mapped[Optional[str]] = mapped_column(String(512))

        engine = connection.engine
        Base.metadata.create_all(engine)

        with Session(engine) as session:
            role = Role(
                id=1,
                name="Test",
                type="Test",
                description="Test",
            )
            session.add(role)
            session.commit()

    def test_orm(self, connection):
        class Base(DeclarativeBase):
            pass

        class Number(Base):
            __tablename__ = "numbers"
            number: Mapped[int] = mapped_column(primary_key=True)
            name: Mapped[str] = mapped_column(String(20))
            alternative_name: Mapped[str] = mapped_column(String(20))
            prime: Mapped[bool] = mapped_column(Boolean)
            ln: Mapped[float] = mapped_column(REAL)

        class User(Base):
            __tablename__ = "users"
            ID: Mapped[int] = mapped_column(primary_key=True)
            name: Mapped[str] = mapped_column(String(20))

        engine = connection.engine
        with Session(engine) as session:
            number = Number(
                number=1, name="One", alternative_name="Uno", prime=False, ln=0.0
            )
            session.add(number)
            session.commit()

        with Session(engine) as session:
            user = User(name="Test")
            session.add(user)
            session.commit()

            statement = select(User).filter_by(name="Test")
            users = session.scalars(statement).all()
            eq_(1, len(users))
            is_true(users[0].ID > 0)
