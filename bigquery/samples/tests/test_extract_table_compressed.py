# Copyright 2019 Google LLC
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


from .. import extract_table_compressed


def test_extract_table_compressed(capsys, client):

    from test_utils.retry import RetryErrors
    from google.api_core.exceptions import InternalServerError
    from google.api_core.exceptions import ServiceUnavailable
    from google.api_core.exceptions import TooManyRequests
    retry_storage_errors = RetryErrors(
        (TooManyRequests, InternalServerError, ServiceUnavailable)
    )

    out, err = capsys.readouterr()
    assert 