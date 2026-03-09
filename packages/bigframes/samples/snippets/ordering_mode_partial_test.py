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


def test_quickstart() -> None:
    import bigframes.pandas

    try:
        # We need a fresh session since we're modifying connection options.
        bigframes.pandas.close_session()

        # [START bigquery_bigframes_ordering_mode_partial]
        import bigframes.pandas as bpd

        bpd.options.bigquery.ordering_mode = "partial"
        # [END bigquery_bigframes_ordering_mode_partial]

        # [START bigquery_bigframes_ordering_mode_partial_ambiguous_window_warning]
        import warnings

        import bigframes.exceptions

        warnings.simplefilter(
            "ignore", category=bigframes.exceptions.AmbiguousWindowWarning
        )
        # [END bigquery_bigframes_ordering_mode_partial_ambiguous_window_warning]

        df = bpd.DataFrame({"column": [1, 2, 1, 3, 1, 2, 3]})

        # [START bigquery_bigframes_ordering_mode_partial_drop_duplicates]
        # Avoid order dependency by using groupby instead of drop_duplicates.
        unique_col = df.groupby(["column"], as_index=False).size().drop(columns="size")
        # [END bigquery_bigframes_ordering_mode_partial_drop_duplicates]

        assert len(unique_col) == 3
    finally:
        # Don't leak partial ordering mode to other code samples.
        bigframes.pandas.close_session()
        bpd.options.bigquery.ordering_mode = "strict"
