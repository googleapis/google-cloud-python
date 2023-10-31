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
import bigframes as bf

from . import resources


def test_maximum_bytes_option():
    session = resources.create_bigquery_session()
    num_query_calls = 0
    with bf.option_context("compute.maximum_bytes_billed", 10000):
        # clear initial method calls
        session.bqclient.method_calls = []
        session._start_query("query")
        for call in session.bqclient.method_calls:
            _, _, kwargs = call
            num_query_calls += 1
            assert kwargs["job_config"].maximum_bytes_billed == 10000
    assert num_query_calls > 0
