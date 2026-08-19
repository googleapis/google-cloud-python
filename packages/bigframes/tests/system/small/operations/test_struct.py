# Copyright 2024 Google LLC
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


def test_dataframe_struct_explode_multiple_columns(nested_df):
    got = nested_df.struct.explode(["label", "address"])
    assert got.columns.to_list() == [
        "customer_id",
        "day",
        "flag",
        "label.key",
        "label.value",
        "event_sequence",
        "address.street",
        "address.city",
    ]


def test_dataframe_struct_explode_separator(nested_df):
    got = nested_df.struct.explode("label", separator="__sep__")
    assert got.columns.to_list() == [
        "customer_id",
        "day",
        "flag",
        "label__sep__key",
        "label__sep__value",
        "event_sequence",
        "address",
    ]
