# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.api_core import exceptions
import pytest

from google.cloud.bigquery_storage_v1 import types as gapic_types


@pytest.fixture(scope="session")
def bqstorage_write_client(credentials):
    from google.cloud import bigquery_storage_v1

    return bigquery_storage_v1.BigQueryWriteClient(credentials=credentials)


def test_append_rows_with_invalid_stream_name_fails_fast(bqstorage_write_client):
    bad_request = gapic_types.AppendRowsRequest()
    bad_request.write_stream = "this-is-an-invalid-stream-resource-path"

    with pytest.raises(exceptions.GoogleAPICallError):
        bqstorage_write_client.append_rows(bad_request)
