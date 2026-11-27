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
import base64
import datetime
import os
from contextlib import contextmanager
from typing import Optional
from unittest import mock

import pytest
from google.cloud.spanner_v1.database import Database
from sqlalchemy import (
    ARRAY,
    BIGINT,
    BINARY,
    DDL,
    Boolean,
    Column,
    Computed,
    DefaultClause,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    LargeBinary,
    MetaData,
    PrimaryKeyConstraint,
    Sequence,
    String,
    Table,
    bindparam,
    column,
    delete,
    event,
    func,
    inspect,
    literal,
    select,
    text,
    update,
)
from sqlalchemy.engine.reflection import ObjectKind
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.testing import eq_, in_, is_false, is_none, is_not_none, is_true
from sqlalchemy.testing.plugin.plugin_base import fixtures
from sqlalchemy.types import REAL


class TestBasics(fixtures.TablesTest):
    @classmethod
    def define_tables(cls, metadata):
        numbers = Table(
            "numbers",
            metadata,
            Column("number", Integer),
            Column("name", String(20)),
            Column("alternative_name", String(20)),
            Column("prime", Boolean, server_default=text("FALSE")),
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
        # Add a foreign key example.
        Table(
            "number_colors",
            metadata,
            Column("ID", Integer, primary_key=True),
            Column(
                "number_id", Integer, ForeignKey("numbers.number", name="number_fk")
            ),
            Column("color", String(20)),
        )

        with cls.bind.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS schema"))
        Table(
            "users",
            metadata,
            Column("ID", Integer, primary_key=True),
            Column("name", String(20)),
            schema="schema",
        )
        # Add a foreign key example which crosses schema.
        Table(
            "number_colors",
            metadata,
            Column("ID", Integer, primary_key=True),
            Column(
                "number_id",
                Integer,
                ForeignKey("numbers.number", name="cross_schema_number_fk"),
            ),
            Column("color", String(20)),
            schema="schema",
        )
        # Add a composite primary key & foreign key example.
        Table(
            "composite_pk",
            metadata,
            Column("a", String, primary_key=True),
            Column("b", String, primary_key=True),
        )
        composite_fk = Table(
            "composite_fk",
            metadata,
            Column("my_a", String, primary_key=True),
            Column("my_b", String, primary_key=True),
            Column("my_c", String, primary_key=True),
            ForeignKeyConstraint(
                ["my_a", "my_b"],
                ["composite_pk.a", "composite_pk.b"],
                name="composite_fk_composite_pk_a_b",
            ),
        )
        Index(
            "idx_composte_fk_all",
            composite_fk.c.my_a,
            composite_fk.c.my_b,
            composite_fk.c.my_c,
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
        eq_(5, len(meta.tables))
        table = meta.tables["numbers"]
        eq_(5, len(table.columns))
        eq_("number", table.columns[0].name)
        eq_(BIGINT, type(table.columns[0].type))
        is_none(table.columns[0].server_default)
        eq_("name", table.columns[1].name)
        eq_(String, type(table.columns[1].type))
        eq_("alternative_name", table.columns[2].name)
        eq_(String, type(table.columns[2].type))
        eq_("prime", table.columns[3].name)
        eq_(Boolean, type(table.columns[3].type))
        is_not_none(table.columns[3].server_default)
        eq_("FALSE", table.columns[3].server_default.arg.text)
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

        class SchemaUser(Base):
            __tablename__ = "users"
            __table_args__ = {"schema": "schema"}
            ID: Mapped[int] = mapped_column(primary_key=True)
            name: Mapped[str] = mapped_column(String(20))

        engine = connection.engine
        with Session(engine) as session:
            number = Number(
                number=1, name="One", alternative_name="Uno", prime=False, ln=0.0
            )
            session.add(number)
            session.commit()

        level = "serializable"
        if os.environ.get("SPANNER_EMULATOR_HOST", ""):
            level = "REPEATABLE READ"
        with Session(engine.execution_options(isolation_level=level)) as session:
            user = User(name="Test")
            session.add(user)
            session.commit()

            statement = select(User).filter_by(name="Test")
            users = session.scalars(statement).all()
            eq_(1, len(users))
            is_true(users[0].ID > 0)

        with Session(engine) as session:
            user = SchemaUser(name="SchemaTest")
            session.add(user)
            session.commit()

            users = session.scalars(
                select(SchemaUser).where(SchemaUser.name == "SchemaTest")
            ).all()
            eq_(1, len(users))
            is_true(users[0].ID > 0)

            session.execute(
                update(SchemaUser)
                .where(SchemaUser.name == "SchemaTest")
                .values(name="NewName")
            )
            session.commit()

            users = session.scalars(
                select(SchemaUser).where(SchemaUser.name == "NewName")
            ).all()
            eq_(1, len(users))
            is_true(users[0].ID > 0)

            session.execute(delete(SchemaUser).where(SchemaUser.name == "NewName"))
            session.commit()

            users = session.scalars(
                select(SchemaUser).where(SchemaUser.name == "NewName")
            ).all()
            eq_(0, len(users))

    def test_multi_row_insert(self, connection):
        """Ensures we can perform multi-row inserts."""

        class Base(DeclarativeBase):
            pass

        class User(Base):
            __tablename__ = "users"
            ID: Mapped[int] = mapped_column(primary_key=True)
            name: Mapped[str] = mapped_column(String(20))

        with connection.engine.begin() as conn:
            inserted_rows = list(
                conn.execute(
                    User.__table__.insert()
                    .values([{"name": "a"}, {"name": "b"}])
                    .returning(User.__table__.c.ID, User.__table__.c.name)
                )
            )

        eq_(2, len(inserted_rows))
        eq_({"a", "b"}, {row.name for row in inserted_rows})

        with connection.engine.connect() as conn:
            selected_rows = list(conn.execute(User.__table__.select()))

        eq_(len(inserted_rows), len(selected_rows))
        eq_(set(inserted_rows), set(selected_rows))

    @pytest.mark.skipif(
        os.environ.get("SPANNER_EMULATOR_HOST") is not None,
        reason=(
            "Fails in emulator due to bug: "
            "https://github.com/GoogleCloudPlatform/cloud-spanner-emulator/issues/279"
        ),
    )
    def test_cross_schema_fk_lookups(self, connection):
        """Ensures we introspect FKs within & across schema."""

        engine = connection.engine

        insp = inspect(engine)
        eq_(
            {
                (None, "number_colors"): [
                    {
                        "name": "number_fk",
                        "referred_table": "numbers",
                        "referred_schema": None,
                        "referred_columns": ["number"],
                        "constrained_columns": ["number_id"],
                    }
                ]
            },
            insp.get_multi_foreign_keys(filter_names=["number_colors"]),
        )
        eq_(
            {
                ("schema", "number_colors"): [
                    {
                        "name": "cross_schema_number_fk",
                        "referred_table": "numbers",
                        "referred_schema": None,
                        "referred_columns": ["number"],
                        "constrained_columns": ["number_id"],
                    }
                ]
            },
            insp.get_multi_foreign_keys(
                filter_names=["number_colors"], schema="schema"
            ),
        )

    def test_composite_fk_lookups(self, connection):
        """Ensures we introspect composite FKs."""

        engine = connection.engine

        insp = inspect(engine)
        eq_(
            {
                (None, "composite_fk"): [
                    {
                        "name": "composite_fk_composite_pk_a_b",
                        "referred_table": "composite_pk",
                        "referred_schema": None,
                        "referred_columns": ["a", "b"],
                        "constrained_columns": ["my_a", "my_b"],
                    }
                ]
            },
            insp.get_multi_foreign_keys(filter_names=["composite_fk"]),
        )

    def test_composite_index_lookups(self, connection):
        """Ensures we introspect composite indexes."""

        engine = connection.engine

        insp = inspect(engine)
        eq_(
            {
                (None, "composite_fk"): [
                    {
                        "name": "idx_composte_fk_all",
                        "column_names": ["my_a", "my_b", "my_c"],
                        "unique": False,
                        "column_sorting": {"my_a": "asc", "my_b": "asc", "my_c": "asc"},
                        "include_columns": [],
                        "dialect_options": {},
                    }
                ]
            },
            insp.get_multi_indexes(filter_names=["composite_fk"]),
        )

    def test_commit_timestamp(self, connection):
        """Ensures commit timestamps are set."""

        class Base(DeclarativeBase):
            pass

        class TimestampUser(Base):
            __tablename__ = "timestamp_users"
            ID: Mapped[int] = mapped_column(primary_key=True)
            name: Mapped[str]
            updated_at: Mapped[datetime.datetime] = mapped_column(
                spanner_allow_commit_timestamp=True,
                default=text("PENDING_COMMIT_TIMESTAMP()"),
                # Make sure that this column is never part of a THEN RETURN clause.
                spanner_exclude_from_returning=True,
            )

        @event.listens_for(TimestampUser, "before_update")
        def before_update(mapper, connection, target):
            target.updated_at = text("PENDING_COMMIT_TIMESTAMP()")

        engine = connection.engine
        Base.metadata.create_all(engine)
        try:
            with Session(engine) as session:
                session.add(TimestampUser(name="name"))
                session.commit()

            with Session(engine) as session:
                users = list(
                    session.scalars(
                        select(TimestampUser).where(TimestampUser.name == "name")
                    )
                )
                user = users[0]

                is_not_none(user.updated_at)
                created_at = user.updated_at

                user.name = "new-name"
                session.commit()

            with Session(engine) as session:
                users = list(
                    session.scalars(
                        select(TimestampUser).where(TimestampUser.name == "new-name")
                    )
                )
                user = users[0]

                is_not_none(user.updated_at)
                is_true(user.updated_at > created_at)

        finally:
            Base.metadata.drop_all(engine)

    @pytest.mark.parametrize(
        "payload",
        [
            b"",
            b"hello world",
            rb"\' OR 1=1 --",
            b"%s",
            b"a\"b'c\\d%s\x00\n\r\t\x7f\xff\xfe",
            bytes(range(256)),
            bytearray(b"a\x00\xff"),
            memoryview(b"a\x00\xff"),
        ],
    )
    def test_binary_literal_roundtrip(self, connection, payload):
        """Verify generated BYTES literals evaluate identically on Spanner."""
        row = connection.execute(
            select(literal(payload, LargeBinary, literal_execute=True))
        ).fetchone()
        eq_(base64.b64decode(row[0]), bytes(payload))

    @contextmanager
    def _binary_literals_table(self, connection):
        metadata = MetaData()
        binary_table = Table(
            "binary_literals_test",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("payload", LargeBinary),
            Column("fixed", BINARY(32)),
            Column("tags", ARRAY(LargeBinary)),
            Column(
                "default_blob",
                LargeBinary,
                server_default=DefaultClause(literal(rb"\' OR 1=1 --")),
            ),
            Column(
                "computed_blob",
                LargeBinary,
                Computed(func.coalesce(column("payload"), rb"\' OR 1=1 --")),
            ),
        )
        engine = connection.engine
        metadata.create_all(engine)
        try:
            yield engine, binary_table
        finally:
            metadata.drop_all(engine)

    def test_binary_literal_ddl_defaults_and_computed(self, connection):
        """Verify BYTES literals evaluate in DEFAULT, Computed, and ARRAY columns."""
        injection_payload = rb"\' OR 1=1 --"
        with self._binary_literals_table(connection) as (engine, binary_table):
            with engine.begin() as conn:
                conn.execute(
                    binary_table.insert().values(
                        id=1,
                        payload=literal(b"custom", LargeBinary, literal_execute=True),
                        fixed=literal(b"\x00\xff", BINARY(32), literal_execute=True),
                        tags=literal(
                            [injection_payload, b"\xff"],
                            ARRAY(LargeBinary),
                            literal_execute=True,
                        ),
                    )
                )
                conn.execute(
                    binary_table.insert().values(
                        id=2,
                        payload=None,
                        fixed=literal(b"nil", BINARY(32), literal_execute=True),
                        tags=literal([], ARRAY(LargeBinary), literal_execute=True),
                    )
                )

            with engine.connect() as conn:
                rows = conn.execute(
                    select(
                        binary_table.c.id,
                        binary_table.c.fixed,
                        binary_table.c.tags,
                        binary_table.c.default_blob,
                        binary_table.c.computed_blob,
                    ).order_by(binary_table.c.id)
                ).all()

            row1, row2 = rows
            eq_(base64.b64decode(row1.fixed), b"\x00\xff")
            eq_(
                [base64.b64decode(item) for item in row1.tags],
                [injection_payload, b"\xff"],
            )
            eq_(base64.b64decode(row1.default_blob), injection_payload)
            eq_(base64.b64decode(row1.computed_blob), b"custom")
            eq_(base64.b64decode(row2.fixed), b"nil")
            eq_(row2.tags, [])
            eq_(base64.b64decode(row2.default_blob), injection_payload)
            eq_(base64.b64decode(row2.computed_blob), injection_payload)

    def test_binary_literal_queries_and_injection_safety(self, connection):
        """Verify BYTES literal predicates work safely without SQL injection."""
        injection_payload = rb"\' OR 1=1 --"
        percent_payload = b"%s"

        with self._binary_literals_table(connection) as (engine, binary_table):
            with engine.begin() as conn:
                for row_id, payload in (
                    (1, injection_payload),
                    (2, percent_payload),
                    (3, b"other"),
                ):
                    conn.execute(
                        binary_table.insert().values(
                            id=row_id,
                            payload=literal(payload, LargeBinary, literal_execute=True),
                        )
                    )

            by_payload = select(binary_table.c.id).where(
                binary_table.c.payload
                == literal(injection_payload, LargeBinary, literal_execute=True)
            )
            mixed_param_and_percent = select(binary_table.c.id).where(
                binary_table.c.id == 2,
                binary_table.c.payload
                == literal(percent_payload, LargeBinary, literal_execute=True),
            )
            expanding_in = select(binary_table.c.id).where(
                binary_table.c.payload.in_(
                    bindparam(
                        "vals",
                        [injection_payload, percent_payload],
                        expanding=True,
                        literal_execute=True,
                    )
                )
            )
            compiled_literal_binds = str(
                select(binary_table.c.id)
                .where(binary_table.c.payload == injection_payload)
                .compile(dialect=engine.dialect, compile_kwargs={"literal_binds": True})
            )

            with engine.connect() as conn:
                eq_(conn.scalars(by_payload).all(), [1])
                eq_(conn.scalars(mixed_param_and_percent).all(), [2])
                eq_(sorted(conn.scalars(expanding_in).all()), [1, 2])
                eq_(conn.scalars(text(compiled_literal_binds)).all(), [1])


class TestReflection(fixtures.TablesTest):
    @classmethod
    @contextmanager
    def _assert_single_ddl_batch(cls, expected_statement_count):
        """Assert the wrapped block issues one update_ddl call of expected size."""
        ddl_batches = []
        original_update_ddl = Database.update_ddl

        def record_update_ddl(database, ddl_statements, *args, **kwargs):
            ddl_batches.append(list(ddl_statements))
            return original_update_ddl(database, ddl_statements, *args, **kwargs)

        with mock.patch.object(Database, "update_ddl", record_update_ddl):
            yield

        eq_(1, len(ddl_batches))
        eq_(expected_statement_count, len(ddl_batches[0]))

    @classmethod
    def _setup_once_tables(cls):
        with cls._assert_single_ddl_batch(expected_statement_count=7):
            super()._setup_once_tables()

    @classmethod
    def _teardown_once_metadata_bind(cls):
        with cls._assert_single_ddl_batch(expected_statement_count=8):
            super()._teardown_once_metadata_bind()

    @classmethod
    def define_tables(cls, metadata):
        """Define schema objects so setup and teardown each run as one DDL batch.

        Registering the schema and view statements via ``metadata`` DDL events
        (``before_create`` / ``after_create`` and ``before_drop`` /
        ``after_drop``) keeps them inside ``TablesTest``'s single
        ``create_all`` / ``drop_all`` transaction, so ``spanner_dbapi`` batches
        all statements into one ``UpdateDatabaseDdlRequest`` for setup and one
        for teardown.
        """
        event.listen(
            metadata,
            "before_create",
            DDL("CREATE SCHEMA IF NOT EXISTS reflection_schema"),
        )
        items = Table(
            "reflection_items",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(20)),
        )
        Index("idx_reflection_items_name", items.c.name)
        Table(
            "reflection_item_tags",
            metadata,
            Column("id", Integer, primary_key=True),
            Column(
                "item_id",
                Integer,
                ForeignKey("reflection_items.id", name="fk_reflection_item_tags"),
            ),
        )
        Table(
            "reflection_schema_items",
            metadata,
            Column("id", Integer, primary_key=True),
            schema="reflection_schema",
        )
        Sequence("reflection_seq", metadata=metadata)
        event.listen(
            metadata,
            "after_create",
            DDL(
                "CREATE VIEW reflection_items_view SQL SECURITY INVOKER AS "
                "SELECT reflection_items.id AS id, reflection_items.name AS name "
                "FROM reflection_items"
            ),
        )
        event.listen(
            metadata,
            "before_drop",
            DDL("DROP VIEW IF EXISTS reflection_items_view"),
        )
        event.listen(
            metadata,
            "after_drop",
            DDL("DROP SCHEMA IF EXISTS reflection_schema"),
        )

    def test_reflection_methods(self, connection):
        inspector = inspect(connection)

        is_true(inspector.has_table("reflection_items"))
        is_true(
            inspector.has_table("reflection_schema_items", schema="reflection_schema")
        )
        is_false(inspector.has_table("does_not_exist"))

        is_true(inspector.has_sequence("reflection_seq"))
        is_false(inspector.has_sequence("does_not_exist"))

        in_("reflection_items", inspector.get_table_names())
        in_(
            "reflection_schema_items",
            inspector.get_table_names(schema="reflection_schema"),
        )
        in_("reflection_items_view", inspector.get_view_names())
        in_("reflection_seq", inspector.get_sequence_names())
        in_("reflection_schema", inspector.get_schema_names())
        in_(
            "reflection_items.id",
            inspector.get_view_definition("reflection_items_view"),
        )

        eq_(2, len(inspector.get_columns("reflection_items")))
        multi_columns = inspector.get_multi_columns(
            filter_names={"reflection_items", "reflection_item_tags"}
        )
        in_((None, "reflection_items"), multi_columns)
        in_((None, "reflection_item_tags"), multi_columns)
        eq_({}, inspector.get_multi_columns(filter_names=[]))
        in_(
            (None, "reflection_items_view"),
            inspector.get_multi_columns(
                filter_names=["reflection_items_view"], kind=ObjectKind.VIEW
            ),
        )

        eq_(
            ["id"],
            inspector.get_pk_constraint("reflection_items")["constrained_columns"],
        )
        in_(
            (None, "reflection_items"),
            inspector.get_multi_pk_constraint(filter_names=["reflection_items"]),
        )
        eq_(
            ["idx_reflection_items_name"],
            [idx["name"] for idx in inspector.get_indexes("reflection_items")],
        )
        in_(
            (None, "reflection_items"),
            inspector.get_multi_indexes(filter_names=["reflection_items"]),
        )
        eq_(
            ["fk_reflection_item_tags"],
            [fk["name"] for fk in inspector.get_foreign_keys("reflection_item_tags")],
        )
        in_(
            (None, "reflection_item_tags"),
            inspector.get_multi_foreign_keys(filter_names=["reflection_item_tags"]),
        )
        eq_([], inspector.get_unique_constraints("reflection_items"))

    @pytest.mark.parametrize(
        "payload",
        [
            "' OR '1'='1' UNION ALL SELECT 'pwned' --",
            '" OR "1"="1" UNION ALL SELECT "pwned" --',
        ],
    )
    def test_reflection_sql_injection_prevented(self, connection, payload):
        inspector = inspect(connection)

        is_false(inspector.has_table(payload))
        is_false(inspector.has_table("reflection_items", schema=payload))
        is_false(inspector.has_sequence(payload))
        is_false(inspector.has_sequence("reflection_seq", schema=payload))
        eq_([], inspector.get_table_names(schema=payload))
        eq_([], inspector.get_view_names(schema=payload))
        eq_([], inspector.get_sequence_names(schema=payload))
        with pytest.raises(NoSuchTableError, match="UNION ALL"):
            inspector.get_view_definition(payload)
        with pytest.raises(NoSuchTableError, match="reflection_items_view"):
            inspector.get_view_definition("reflection_items_view", schema=payload)
        eq_([], inspector.get_columns(payload))
        eq_([], inspector.get_columns("reflection_items", schema=payload))
        eq_({}, inspector.get_multi_columns(filter_names=[payload]))
        eq_({}, inspector.get_multi_columns(schema=payload))
        eq_(
            [(None, "reflection_items")],
            list(
                inspector.get_multi_columns(
                    filter_names=["reflection_items", payload]
                ).keys()
            ),
        )
        eq_([], inspector.get_indexes(payload))
        eq_([], inspector.get_indexes("reflection_items", schema=payload))
        eq_({}, inspector.get_multi_indexes(filter_names=[payload]))
        eq_({}, inspector.get_multi_indexes(schema=payload))
        eq_([], inspector.get_pk_constraint(payload))
        eq_([], inspector.get_pk_constraint("reflection_items", schema=payload))
        eq_({}, inspector.get_multi_pk_constraint(filter_names=[payload]))
        eq_({}, inspector.get_multi_pk_constraint(schema=payload))
        eq_([], inspector.get_foreign_keys(payload))
        eq_([], inspector.get_foreign_keys("reflection_item_tags", schema=payload))
        eq_({}, inspector.get_multi_foreign_keys(filter_names=[payload]))
        eq_({}, inspector.get_multi_foreign_keys(schema=payload))
        eq_([], inspector.get_unique_constraints(payload))
        eq_([], inspector.get_unique_constraints("reflection_items", schema=payload))
