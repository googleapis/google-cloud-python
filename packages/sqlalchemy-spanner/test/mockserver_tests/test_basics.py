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

import datetime
from google.cloud.spanner_admin_database_v1 import UpdateDatabaseDdlRequest
from google.cloud.spanner_dbapi.parsed_statement import AutocommitDmlMode
from sqlalchemy import (
    create_engine,
    select,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    func,
    text,
    BigInteger,
)
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.testing import eq_, is_instance_of
from google.cloud.spanner_v1 import (
    FixedSizePool,
    BatchCreateSessionsRequest,
    ExecuteSqlRequest,
    ResultSet,
    PingingPool,
    TypeCode,
)
from test.mockserver_tests.mock_server_test_base import (
    MockServerTestBase,
    add_select1_result,
    add_result,
    add_single_result,
    add_update_count,
    add_singer_query_result,
)


class TestBasics(MockServerTestBase):
    def verify_select1(self, results):
        result_list = []
        for row in results:
            result_list.append(row)
            eq_(1, row[0])
        eq_(1, len(result_list))
        requests = self.spanner_service.requests
        eq_(2, len(requests))
        is_instance_of(requests[0], BatchCreateSessionsRequest)
        is_instance_of(requests[1], ExecuteSqlRequest)

    def test_select1(self):
        add_select1_result()
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql("select 1")
            self.verify_select1(results)

    def test_sqlalchemy_select1(self):
        add_select1_result()
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            connect_args={"client": self.client, "pool": PingingPool(size=10)},
        )
        with engine.connect().execution_options(
            isolation_level="AUTOCOMMIT"
        ) as connection:
            results = connection.execute(select(1)).fetchall()
            self.verify_select1(results)

    def test_sqlalchemy_select_now(self):
        now = datetime.datetime.now(datetime.UTC)
        iso_now = now.isoformat().replace("+00:00", "Z")
        add_single_result(
            "SELECT current_timestamp AS now_1",
            "now_1",
            TypeCode.TIMESTAMP,
            [(iso_now,)],
        )
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            connect_args={"client": self.client, "pool": PingingPool(size=10)},
        )
        with engine.connect().execution_options(
            isolation_level="AUTOCOMMIT"
        ) as connection:
            spanner_now = connection.execute(select(func.now())).fetchone()[0]
            eq_(spanner_now.timestamp(), now.timestamp())

    def test_create_table(self):
        add_result(
            """SELECT true
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA="" AND TABLE_NAME="users"
LIMIT 1
""",
            ResultSet(),
        )
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            connect_args={"client": self.client, "pool": FixedSizePool(size=10)},
        )
        metadata = MetaData()
        Table(
            "users",
            metadata,
            Column("user_id", Integer, primary_key=True),
            Column("user_name", String(16), nullable=False),
        )
        metadata.create_all(engine)
        requests = self.database_admin_service.requests
        eq_(1, len(requests))
        is_instance_of(requests[0], UpdateDatabaseDdlRequest)
        eq_(1, len(requests[0].statements))
        eq_(
            "CREATE TABLE users (\n"
            "\tuser_id INT64 NOT NULL, \n"
            "\tuser_name STRING(16) NOT NULL\n"
            ") PRIMARY KEY (user_id)",
            requests[0].statements[0],
        )

    def test_create_multiple_tables(self):
        for i in range(2):
            add_result(
                f"""SELECT true
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA="" AND TABLE_NAME="table{i}"
LIMIT 1
""",
                ResultSet(),
            )
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            connect_args={"client": self.client, "pool": FixedSizePool(size=10)},
        )
        metadata = MetaData()
        for i in range(2):
            Table(
                "table" + str(i),
                metadata,
                Column("id", Integer, primary_key=True),
                Column("value", String(16), nullable=False),
            )
        metadata.create_all(engine)
        requests = self.database_admin_service.requests
        eq_(1, len(requests))
        is_instance_of(requests[0], UpdateDatabaseDdlRequest)
        eq_(2, len(requests[0].statements))
        for i in range(2):
            eq_(
                f"CREATE TABLE table{i} (\n"
                "\tid INT64 NOT NULL, \n"
                "\tvalue STRING(16) NOT NULL"
                "\n) PRIMARY KEY (id)",
                requests[0].statements[i],
            )

    def test_partitioned_dml(self):
        sql = "UPDATE singers SET checked=true WHERE active = true"
        add_update_count(sql, 100, AutocommitDmlMode.PARTITIONED_NON_ATOMIC)
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            connect_args={"client": self.client, "pool": PingingPool(size=10)},
        )
        # TODO: Support autocommit_dml_mode as a connection variable in execution
        #       options.
        with engine.connect().execution_options(
            isolation_level="AUTOCOMMIT"
        ) as connection:
            connection.connection.set_autocommit_dml_mode(
                AutocommitDmlMode.PARTITIONED_NON_ATOMIC
            )
            results = connection.execute(text(sql)).rowcount
            eq_(100, results)

    def test_select_for_update(self):
        class Base(DeclarativeBase):
            pass

        class Singer(Base):
            __tablename__ = "singers"
            id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
            name: Mapped[str] = mapped_column(String)

        query = (
            "SELECT singers.id AS singers_id, singers.name AS singers_name\n"
            "FROM singers\n"
            "WHERE singers.id = @a0\n"
            " LIMIT @a1 FOR UPDATE"
        )
        add_singer_query_result(query)
        update = "UPDATE singers SET name=@a0 WHERE singers.id = @a1"
        add_update_count(update, 1)

        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            connect_args={"client": self.client, "pool": FixedSizePool(size=10)},
        )

        with Session(engine) as session:
            singer = (
                session.query(Singer).filter(Singer.id == 1).with_for_update().first()
            )
            singer.name = "New Name"
            session.add(singer)
            session.commit()
