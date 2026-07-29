# Copyright 2025 Google LLC All rights reserved.
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

import unittest

from google.cloud.spanner_dbapi.client_side_statement_executor import (
    _get_isolation_level,
)
from google.cloud.spanner_dbapi.parse_utils import classify_statement
from google.cloud.spanner_v1 import TransactionOptions


class TestParseUtils(unittest.TestCase):
    def test_get_isolation_level(self):
        self.assertIsNone(_get_isolation_level(classify_statement("begin")))
        self.assertEqual(
            TransactionOptions.IsolationLevel.SERIALIZABLE,
            _get_isolation_level(
                classify_statement("begin isolation level serializable")
            ),
        )
        self.assertEqual(
            TransactionOptions.IsolationLevel.SERIALIZABLE,
            _get_isolation_level(
                classify_statement(
                    "begin  transaction  isolation    level     serializable    "
                )
            ),
        )
        self.assertEqual(
            TransactionOptions.IsolationLevel.REPEATABLE_READ,
            _get_isolation_level(
                classify_statement("begin isolation level repeatable read")
            ),
        )
        self.assertEqual(
            TransactionOptions.IsolationLevel.REPEATABLE_READ,
            _get_isolation_level(
                classify_statement(
                    "begin    transaction  isolation    level   repeatable    read "
                )
            ),
        )
