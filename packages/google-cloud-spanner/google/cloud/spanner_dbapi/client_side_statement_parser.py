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

import re

from google.cloud.spanner_dbapi.parsed_statement import (
    ParsedStatement,
    StatementType,
    ClientSideStatementType,
)

RE_COMMIT = re.compile(r"^\s*(COMMIT)(TRANSACTION)?", re.IGNORECASE)


def parse_stmt(query):
    """Parses the sql query to check if it matches with any of the client side
        statement regex.

    It is an internal method that can make backwards-incompatible changes.

    :type query: str
    :param query: sql query

    :rtype: ParsedStatement
    :returns: ParsedStatement object.
    """
    if RE_COMMIT.match(query):
        return ParsedStatement(
            StatementType.CLIENT_SIDE, query, ClientSideStatementType.COMMIT
        )
    return None
