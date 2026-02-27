#  Copyright 2026 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Helper functions for compliance tests."""
import os

SPANNER_EMULATOR_HOST = os.environ.get("SPANNER_EMULATOR_HOST")

PROJECT_ID = "test-project"
INSTANCE_ID = "test-instance"
DATABASE_ID = "test-db"

EMULATOR_TEST_CONNECTION_STRING = (
    f"{SPANNER_EMULATOR_HOST}"
    f"projects/{PROJECT_ID}"
    f"/instances/{INSTANCE_ID}"
    f"/databases/{DATABASE_ID}"
    "?autoConfigEmulator=true"
)


def setup_test_env() -> None:
    print(
        f"Set SPANNER_EMULATOR_HOST to "
        f"{os.environ['SPANNER_EMULATOR_HOST']}"
    )
    print(f"Using Connection String: {get_test_connection_string()}")


def get_test_connection_string() -> str:
    return EMULATOR_TEST_CONNECTION_STRING
