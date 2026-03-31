# Copyright 2023 Google LLC
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

import google.api_core.exceptions
import google.cloud.bigquery_connection_v1
import pytest

import bigframes.pandas

from . import remote_function


# TODO(tswast): Once the connections are cleaned up in the sample test project
# and https://github.com/GoogleCloudPlatform/python-docs-samples/issues/11720
# is closed, we shouldn't need this because AFAIK we only use one BQ connection
# in this sample.
@pytest.fixture(autouse=True)
def cleanup_connections() -> None:
    client = google.cloud.bigquery_connection_v1.ConnectionServiceClient()

    for conn in client.list_connections(
        parent="projects/python-docs-samples-tests/locations/us"
    ):
        try:
            int(conn.name.split("/")[-1].split("-")[0], base=16)
        except ValueError:
            print(f"Couldn't parse {conn.name}")
            continue

        try:
            print(f"removing {conn.name}")
            client.delete_connection(
                google.cloud.bigquery_connection_v1.DeleteConnectionRequest(
                    {"name": conn.name},
                )
            )
        except google.api_core.exceptions.GoogleAPIError:
            # We did as much clean up as we can.
            break


def test_remote_function_and_read_gbq_function(
    capsys: pytest.CaptureFixture[str],
) -> None:
    # We need a fresh session since we're modifying connection options.
    bigframes.pandas.close_session()

    # Determine project id, in this case prefer the one set in the environment
    # variable GOOGLE_CLOUD_PROJECT (if any)
    import os

    your_project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "bigframes-dev")

    remote_function.run_remote_function_and_read_gbq_function(your_project_id)
    out, _ = capsys.readouterr()
    assert "Created BQ remote function:" in out
    assert "Created cloud function:" in out
