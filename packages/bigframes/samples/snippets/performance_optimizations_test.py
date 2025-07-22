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


def test_performance_optimizations() -> None:
    # [START bigquery_bigframes_use_peek_to_preview_data]
    import bigframes.pandas as bpd

    # Read the "Penguins" table into a dataframe
    df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

    # Preview 3 random rows
    df.peek(3)
    # [END bigquery_bigframes_use_peek_to_preview_data]
    assert df.peek(3) is not None

    import bigframes.pandas as bpd

    users = bpd.DataFrame({"user_name": ["John"]})
    groups = bpd.DataFrame({"group_id": ["group_1"]})
    transactions = bpd.DataFrame({"amount": [3], "completed": [True]})

    # [START bigquery_bigframes_use_cache_after_expensive_operations]
    # Assume you have 3 large dataframes "users", "group" and "transactions"

    # Expensive join operations
    final_df = users.join(groups).join(transactions)
    final_df.cache()
    # Subsequent derived results will reuse the cached join
    print(final_df.peek())
    print(len(final_df[final_df["completed"]]))
    print(final_df.groupby("group_id")["amount"].mean().peek(30))
    # [END bigquery_bigframes_use_cache_after_expensive_operations]
    assert final_df is not None

    # [START bigquery_bigframes_enable_deferred_repr_for_debugging]
    import bigframes.pandas as bpd

    bpd.options.display.repr_mode = "deferred"
    # [END bigquery_bigframes_enable_deferred_repr_for_debugging]
    assert bpd.options.display.repr_mode == "deferred"
