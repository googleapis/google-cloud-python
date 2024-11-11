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


def test_boosted_tree_model(random_model_id: str) -> None:
    # your_model_id = random_model_id
    # [START bigquery_dataframes_bqml_boosted_tree_prepare]
    import bigframes.pandas as bpd

    input_data = bpd.read_gbq(
        "bigquery-public-data.ml_datasets.census_adult_income",
        columns=(
            "age",
            "workclass",
            "marital_status",
            "education_num",
            "occupation",
            "hours_per_week",
            "income_bracket",
            "functional_weight",
        ),
    )
    input_data["dataframe"] = bpd.Series("training", index=input_data.index,).case_when(
        [
            (((input_data["functional_weight"] % 10) == 8), "evaluation"),
            (((input_data["functional_weight"] % 10) == 9), "prediction"),
        ]
    )
    del input_data["functional_weight"]
    # [END bigquery_dataframes_bqml_boosted_tree_prepare]
    assert input_data is not None
