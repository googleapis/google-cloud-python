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


class TestStaleReads(MockServerTestBase):
    def test_stale_read_multi_use(self):
        from test.mockserver_tests.stale_read_model import Singer

        add_singer_query_result("SELECT singers.id, singers.name \n" + "FROM singers")
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            echo=True,
            connect_args={"client": self.client, "pool": FixedSizePool(size=10)},
        )

        timestamp = datetime.datetime.fromtimestamp(1733328910)
        for i in range(2):
            with Session(
                engine.execution_options(
                    read_only=True,
                    staleness={"read_timestamp": timestamp},
                )
            ) as session:
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
                                read_timestamp={"seconds": 1733328910},
                                return_read_timestamp=True,
                            )
                        )
                    )
                ),
                begin_request.options,
            )

    def test_stale_read_single_use(self):
        from test.mockserver_tests.stale_read_model import Singer

        add_singer_query_result("SELECT singers.id, singers.name\n" + "FROM singers")
        engine = create_engine(
            "spanner:///projects/p/instances/i/databases/d",
            echo=True,
            connect_args={"client": self.client, "pool": FixedSizePool(size=10)},
        )

        with Session(
            engine.execution_options(
                isolation_level="AUTOCOMMIT",
                staleness={"max_staleness": {"seconds": 15}},
            )
        ) as session:
            # Execute two queries in autocommit.
            session.scalars(select(Singer)).all()
            session.scalars(select(Singer)).all()

        # Verify the requests that we got.
        requests = self.spanner_service.requests
        eq_(3, len(requests))
        is_instance_of(requests[0], BatchCreateSessionsRequest)
        is_instance_of(requests[1], ExecuteSqlRequest)
        is_instance_of(requests[2], ExecuteSqlRequest)
        # Verify that the requests use a stale read.
        for index in [1, 2]:
            execute_request: ExecuteSqlRequest = requests[index]
            eq_(
                TransactionOptions(
                    dict(
                        read_only=TransactionOptions.ReadOnly(
                            dict(
                                max_staleness={"seconds": 15},
                                return_read_timestamp=True,
                            )
                        )
                    )
                ),
                execute_request.transaction.single_use,
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
