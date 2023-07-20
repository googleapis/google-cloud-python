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

"""This script runs with each release and publishes information about our pandas
and sklearn API coverage to BigQuery, where it can be used in our dashboards."""

import argparse
import inspect

import pandas as pd

import bigframes.pandas as bpd


def generate_pandas_api_coverage():
    """Inspect all our pandas objects, and compare with the real pandas objects, to see
    which methods we implement. For each, generate a regex that can be used to check if
    its present in a notebook"""
    header = ["api", "pattern", "kind", "is_in_bigframes"]
    api_patterns = []
    targets = [
        ("pandas", pd, bpd),
        ("dataframe", pd.DataFrame, bpd.DataFrame),
        ("series", pd.Series, bpd.Series),
        ("index", pd.Index, bpd.Index),
    ]
    indexers = ["loc", "iloc", "iat", "ix", "at"]
    for name, pandas_obj, bigframes_obj in targets:
        for member in dir(pandas_obj):
            # skip private functions and properties
            if member[0] == "_" and member[1] != "_":
                continue

            # skip members that are also common python methods
            if member in {"append", "tolist", "format", "items", "keys"}:
                continue

            if inspect.isfunction(getattr(pandas_obj, member)):
                # Function, match .member(
                token = f"\\.{member}\\("
                token_type = "function"
            elif member in indexers:
                # Indexer, match .indexer[
                token = f"\\.{member}\\["
                token_type = "indexer"
            else:
                # Property
                token = f"\\.{member}\\b"
                token_type = "property"

            is_in_bigframes = hasattr(bigframes_obj, member)

            api_patterns.append(
                [f"{name}.{member}", token, token_type, is_in_bigframes]
            )

    return pd.DataFrame(api_patterns, columns=header)


def generate_sklearn_api_coverage():
    """Explore all SKLearn modules, and for each item contained generate a
    regex to detect it being imported, and record whether we implement it"""
    sklearn_modules = [
        "sklearn",
        "sklearn.model_selection",
        "sklearn.preprocessing",
        "sklearn.metrics",
        "sklearn.linear_model",
        "sklearn.ensemble",
        "sklearn.tree",
        "sklearn.neighbors",
        "sklearn.svm",
        "sklearn.naive_bayes",
        "sklearn.pipeline",
        "sklearn.decomposition",
        "sklearn.impute",
        "sklearn.cluster",
        "sklearn.feature_selection",
        "sklearn.utils",
        "sklearn.compose",
        "sklearn.neural_network",
        "sklearn.datasets",
        "sklearn.base",
        "sklearn.manifold",
        "sklearn.discriminant_analysis",
        "sklearn.experimental",
        "sklearn.multiclass",
        "sklearn.kernel_ridge",
        "sklearn.feature_extraction",
        "sklearn.dummy",
        "sklearn.mixture",
        "sklearn.gaussian_process",
        "sklearn.calibration",
        "sklearn.multioutput",
        "sklearn.inspection",
        "sklearn.exceptions",
        "sklearn.cross_decomposition",
        "sklearn.random_projection",
        "sklearn.covariance",
        "sklearn.semi_supervised",
        "sklearn.isotonic",
        "sklearn.kernel_approximation",
    ]

    header = ["api", "pattern", "kind", "is_in_bigframes"]
    api_patterns = []
    for module in sklearn_modules:
        exec(f"import {module}")
        members = eval(f"dir({module})")
        bigframes_has_module = False
        bigframes_members = []
        try:
            bigframes_module = module.replace("sklearn", "bigframes.ml")
            exec(f"import {bigframes_module}")
            bigframes_has_module = True
            bigframes_members = eval(f"dir({bigframes_module})")
        except ImportError:
            pass

        api_patterns.append(
            [
                module,
                f"from {module} import ",
                "module",
                bigframes_has_module,
            ]
        )
        for member in members:
            # skip private functions and properties
            if member[0] == "_":
                continue

            api_patterns.append(
                [
                    f"{module}.{member}",
                    rf"from {module} import [^\n]*\b{member}\b",
                    "api",
                    member in bigframes_members,
                ]
            )

    return pd.DataFrame(api_patterns, columns=header)


def build_api_coverage_table(bigframes_version: str, release_version: str):
    pandas_cov_df = generate_pandas_api_coverage()
    pandas_cov_df["module"] = "bigframes"
    sklearn_cov_df = generate_sklearn_api_coverage()
    sklearn_cov_df["module"] = "bigframes.ml"
    combined_df = pd.concat([pandas_cov_df, sklearn_cov_df])
    combined_df["timestamp"] = pd.Timestamp.now()
    combined_df["bigframes_version"] = bigframes_version
    combined_df["release_version"] = release_version
    return combined_df.infer_objects().convert_dtypes()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bigframes_version")
    parser.add_argument("--release_version")
    parser.add_argument("--bigquery_table_name")
    args = parser.parse_args()
    df = build_api_coverage_table(args.bigframes_version, args.release_version)
    df.to_gbq(args.bigquery_table_name, if_exists="append")


if __name__ == "__main__":
    main()
