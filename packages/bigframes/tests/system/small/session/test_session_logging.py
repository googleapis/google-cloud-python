# Copyright 2026 Google LLC
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

from unittest import mock

from bigframes.core.logging import data_types
import bigframes.session._io.bigquery as bq_io


def test_data_type_logging(scalars_df_index):
    s = scalars_df_index["int64_col"] + 1.5

    # We want to check the job_config passed to _query_and_wait_bigframes
    with mock.patch(
        "bigframes.session._io.bigquery.start_query_with_client",
        wraps=bq_io.start_query_with_client,
    ) as mock_query:
        s.to_pandas()

        # Fetch job labels sent to the BQ client and verify their values
        assert mock_query.called
        call_args = mock_query.call_args
        job_config = call_args.kwargs.get("job_config")
        assert job_config is not None
        job_labels = job_config.labels
        assert "bigframes-dtypes" in job_labels
        assert job_labels["bigframes-dtypes"] == data_types.encode_type_refs(
            s._block._expr.node
        )
