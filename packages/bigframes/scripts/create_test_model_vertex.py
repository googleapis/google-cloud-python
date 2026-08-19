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

import argparse
import sys

import bigframes.ml.linear_model
import bigframes.pandas


def create_vertex_model(vertex_model_name):
    df = bigframes.pandas.read_gbq("bigquery-public-data.ml_datasets.penguins")

    # filter down to the data we want to analyze
    adelie_data = df[df.species == "Adelie Penguin (Pygoscelis adeliae)"]

    # drop the columns we don't care about
    adelie_data = adelie_data.drop(columns=["species"])

    # drop rows with nulls to get our training data
    training_data = adelie_data.dropna()

    feature_columns = training_data["culmen_length_mm"]
    label_columns = training_data[["body_mass_g"]]

    # create model
    model = bigframes.ml.linear_model.LinearRegression()
    model.fit(feature_columns, label_columns)

    # register to Vertex Registry
    model.register(vertex_model_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get top APIs for which there are no code samples in the docstring."
    )
    parser.add_argument(
        "-m",
        "--model-name",
        type=str,
        required=True,
        action="store",
        help="Name of the model in Vertex.",
    )
    parser.add_argument(
        "-p",
        "--project-id",
        type=str,
        required=False,
        action="store",
        help="Project id in which the model should be created. "
        "By default, a project will be resolved as per https://cloud.google.com/python/docs/reference/google-cloud-core/latest/config#overview.",
    )

    args = parser.parse_args(sys.argv[1:])
    if args.project_id:
        bigframes.pandas.options.bigquery.project = args.project_id

    create_vertex_model(args.model_name)
