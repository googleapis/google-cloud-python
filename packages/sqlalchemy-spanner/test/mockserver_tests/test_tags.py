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

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.testing import eq_, is_instance_of
from google.cloud.spanner_v1 import (
    FixedSizePool,
    BatchCreateSessionsRequest,
    ExecuteSqlRequest,
    BeginTransactionRequest,
    CommitRequest,
)
from test.mockserver_tests.mock_server_test_base import (
    MockServerTestBase,
    add_update_count,
)
from test.mockserver_tests.mock_server_test_base import add_result
import google.cloud.spanner_v1.types.type as spanner_type
import google.cloud.spanner_v1.types.result_set as result_set


class TestStaleReads(MockServerTestBase):
    def test_request_tag(self):
        from test.mockserver_tests.tags_model import Singer

        add_singer_query_result("SELECT singers.id, singers.name \n" + "FROM singers")
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            connect_args={"client": self.client, "pool": FixedSizePool(size=10)},
        )

        with Session(engine.execution_options(read_only=True)) as session:
            # Execute two queries in a read-only transaction.
            session.scalars(
                select(Singer).execution_options(request_tag="my-tag-1")
            ).all()
            session.scalars(
                select(Singer).execution_options(request_tag="my-tag-2")
            ).all()

        # Verify the requests that we got.
        requests = self.spanner_service.requests
        eq_(4, len(requests))
        is_instance_of(requests[0], BatchCreateSessionsRequest)
        is_instance_of(requests[1], BeginTransactionRequest)
        is_instance_of(requests[2], ExecuteSqlRequest)
        is_instance_of(requests[3], ExecuteSqlRequest)
        # Verify that we got a request tag for the queries.
        eq_("my-tag-1", requests[2].request_options.request_tag)
        eq_("my-tag-2", requests[3].request_options.request_tag)

    def test_transaction_tag(self):
        from test.mockserver_tests.tags_model import Singer

        add_singer_query_result("SELECT singers.id, singers.name\n" + "FROM singers")
        add_update_count("INSERT INTO singers (id, name) VALUES (@a0, @a1)", 1)
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            connect_args={"client": self.client, "pool": FixedSizePool(size=10)},
        )

        with Session(
            engine.execution_options(transaction_tag="my-transaction-tag")
        ) as session:
            # Execute a query and an insert statement in a read/write transaction.
            session.scalars(
                select(Singer).execution_options(request_tag="my-tag-1")
            ).all()
            session.add(Singer(id=1, name="Some Singer"))
            session.commit()

        # Verify the requests that we got.
        requests = self.spanner_service.requests
        eq_(5, len(requests))
        is_instance_of(requests[0], BatchCreateSessionsRequest)
        is_instance_of(requests[1], BeginTransactionRequest)
        is_instance_of(requests[2], ExecuteSqlRequest)
        is_instance_of(requests[3], ExecuteSqlRequest)
        is_instance_of(requests[4], CommitRequest)
        for request in requests[2:]:
            eq_("my-transaction-tag", request.request_options.transaction_tag)


def add_singer_query_result(sql: str):
    result = result_set.ResultSet(
        dict(
            metadata=result_set.ResultSetMetadata(
                dict(
                    row_type=spanner_type.StructType(
                        dict(
                            fields=[
                                spanner_type.StructType.Field(
                                    dict(
                                        name="singers_id",
                                        type=spanner_type.Type(
                                            dict(code=spanner_type.TypeCode.INT64)
                                        ),
                                    )
                                ),
                                spanner_type.StructType.Field(
                                    dict(
                                        name="singers_name",
                                        type=spanner_type.Type(
                                            dict(code=spanner_type.TypeCode.STRING)
                                        ),
                                    )
                                ),
                            ]
                        )
                    )
                )
            ),
        )
    )
    result.rows.extend(
        [
            (
                "1",
                "Jane Doe",
            ),
            (
                "2",
                "John Doe",
            ),
        ]
    )
    add_result(sql, result)
