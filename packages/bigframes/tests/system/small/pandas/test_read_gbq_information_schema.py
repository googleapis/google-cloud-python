# Copyright 2025 Google LLC
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

import pytest


@pytest.mark.parametrize("include_project", [True, False])
@pytest.mark.parametrize(
    "view_id",
    [
        # https://cloud.google.com/bigquery/docs/information-schema-intro
        "region-US.INFORMATION_SCHEMA.SESSIONS_BY_USER",
        "region-US.INFORMATION_SCHEMA.SCHEMATA",
    ],
)
def test_read_gbq_jobs_by_user_returns_schema(
    unordered_session, view_id: str, include_project: bool
):
    if include_project:
        table_id = unordered_session.bqclient.project + "." + view_id
    else:
        table_id = view_id

    df = unordered_session.read_gbq(table_id, max_results=10)
    assert df.dtypes is not None


def test_read_gbq_schemata_can_be_peeked(unordered_session):
    df = unordered_session.read_gbq("region-US.INFORMATION_SCHEMA.SCHEMATA")
    result = df.peek()
    assert result is not None


def test_read_gbq_schemata_four_parts_can_be_peeked(unordered_session):
    df = unordered_session.read_gbq(
        f"{unordered_session.bqclient.project}.region-US.INFORMATION_SCHEMA.SCHEMATA"
    )
    result = df.peek()
    assert result is not None
