# Copyright 2023 Google LLC All rights reserved.
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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from google.cloud.spanner_dbapi import Connection
from google.cloud.spanner_dbapi.parsed_statement import (
    ParsedStatement,
    ClientSideStatementType,
)


def execute(connection: "Connection", parsed_statement: ParsedStatement):
    """Executes the client side statements by calling the relevant method.

    It is an internal method that can make backwards-incompatible changes.

    :type connection: Connection
    :param connection: Connection object of the dbApi

    :type parsed_statement: ParsedStatement
    :param parsed_statement: parsed_statement based on the sql query
    """
    if parsed_statement.client_side_statement_type == ClientSideStatementType.COMMIT:
        return connection.commit()
    if parsed_statement.client_side_statement_type == ClientSideStatementType.BEGIN:
        return connection.begin()
    if parsed_statement.client_side_statement_type == ClientSideStatementType.ROLLBACK:
        return connection.rollback()
