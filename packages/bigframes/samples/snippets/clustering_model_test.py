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


def test_clustering_model() -> None:
    # [START bigquery_dataframes_clustering_model]
    from bigframes.ml.cluster import KMeans
    import bigframes.pandas as bpd

    # Load data from BigQuery
    query_or_table = "bigquery-public-data.ml_datasets.penguins"
    bq_df = bpd.read_gbq(query_or_table)

    # Create the KMeans model
    cluster_model = KMeans(n_clusters=10)
    cluster_model.fit(bq_df["culmen_length_mm"], bq_df["sex"])

    # Predict using the model
    result = cluster_model.predict(bq_df)
    # Score the model
    score = cluster_model.score(bq_df)
    # [END bigquery_dataframes_clustering_model]
    assert result is not None
    assert score is not None
