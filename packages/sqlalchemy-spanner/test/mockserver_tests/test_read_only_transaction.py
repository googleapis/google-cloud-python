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
    TransactionOptions,
)
from test.mockserver_tests.mock_server_test_base import MockServerTestBase
from test.mockserver_tests.mock_server_test_base import add_result
import google.cloud.spanner_v1.types.type as spanner_type
import google.cloud.spanner_v1.types.result_set as result_set


class TestReadOnlyTransaction(MockServerTestBase):
    def test_read_only_transaction(self):
        from test.mockserver_tests.read_only_model import Singer

        add_singer_query_result("SELECT singers.id, singers.name \n" + "FROM singers")
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            echo=True,
            connect_args={"client": self.client, "pool": FixedSizePool(size=10)},
        )

        for i in range(2):
            with Session(engine.execution_options(read_only=True)) as session:
                # Execute two queries in a read-only transaction.
                session.scalars(select(Singer)).all()
                session.scalars(select(Singer)).all()

        # Verify the requests that we got.
        requests = self.spanner_service.requests
        eq_(7, len(requests))
        is_instance_of(requests[0], BatchCreateSessionsRequest)
        is_instance_of(requests[1], BeginTransactionRequest)
        is_instance_of(requests[2], ExecuteSqlRequest)
        is_instance_of(requests[3], ExecuteSqlRequest)
        is_instance_of(requests[4], BeginTransactionRequest)
        is_instance_of(requests[5], ExecuteSqlRequest)
        is_instance_of(requests[6], ExecuteSqlRequest)
        # Verify that the transaction is a read-only transaction.
        for index in [1, 4]:
            begin_request: BeginTransactionRequest = requests[index]
            eq_(
                TransactionOptions(
                    dict(
                        read_only=TransactionOptions.ReadOnly(
                            dict(
                                strong=True,
                                return_read_timestamp=True,
                            )
                        )
                    )
                ),
                begin_request.options,
            )


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
