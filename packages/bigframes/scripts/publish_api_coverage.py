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
import pathlib
import sys

import pandas as pd
import pandas.core.groupby
import pandas.core.indexes.accessors
import pandas.core.strings.accessor
import pandas.core.window.rolling

import bigframes
import bigframes.core.groupby
import bigframes.core.window
import bigframes.operations.datetimes
import bigframes.operations.strings
import bigframes.pandas as bpd

REPO_ROOT = pathlib.Path(__file__).parent.parent

URL_PREFIX = {
    "pandas": (
        "https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.pandas#bigframes_pandas_"
    ),
    "dataframe": (
        "https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.dataframe.DataFrame#bigframes_dataframe_DataFrame_"
    ),
    "dataframegroupby": (
        "https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.core.groupby.DataFrameGroupBy#bigframes_core_groupby_DataFrameGroupBy_"
    ),
    "index": (
        "https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.core.indexes.base.Index#bigframes_core_indexes_base_Index_"
    ),
    "series": (
        "https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.series.Series#bigframes_series_Series_"
    ),
    "seriesgroupby": (
        "https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.core.groupby.SeriesGroupBy#bigframes_core_groupby_SeriesGroupBy_"
    ),
    "datetimemethods": (
        "https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.operations.datetimes.DatetimeMethods#bigframes_operations_datetimes_DatetimeMethods_"
    ),
    "stringmethods": (
        "https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.operations.strings.StringMethods#bigframes_operations_strings_StringMethods_"
    ),
    "window": (
        "https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.core.window.Window#bigframes_core_window_Window_"
    ),
}


PANDAS_TARGETS = [
    ("pandas", pd, bpd),
    ("dataframe", pd.DataFrame, bpd.DataFrame),
    (
        "dataframegroupby",
        pandas.core.groupby.DataFrameGroupBy,
        bigframes.core.groupby.DataFrameGroupBy,
    ),
    ("series", pd.Series, bpd.Series),
    (
        "seriesgroupby",
        pandas.core.groupby.DataFrameGroupBy,
        bigframes.core.groupby.DataFrameGroupBy,
    ),
    (
        "datetimemethods",
        pandas.core.indexes.accessors.CombinedDatetimelikeProperties,
        bigframes.operations.datetimes.DatetimeMethods,
    ),
    (
        "stringmethods",
        pandas.core.strings.accessor.StringMethods,
        bigframes.operations.strings.StringMethods,
    ),
    (
        "window",
        pandas.core.window.rolling.Rolling,
        bigframes.core.window.Window,
    ),
    ("index", pd.Index, bpd.Index),
]


def names_from_signature(signature):
    """Extract the names of parameters from signature

    See: https://docs.python.org/3/library/inspect.html#inspect.signature
    """
    return frozenset({parameter for parameter in signature.parameters})


def calculate_missing_parameters(bigframes_function, target_function):
    # Some built-in functions can't be inspected. These raise a ValueError.
    try:
        bigframes_signature = inspect.signature(bigframes_function)
        target_signature = inspect.signature(target_function)
    except ValueError:
        return {}

    bigframes_params = names_from_signature(bigframes_signature)
    target_params = names_from_signature(target_signature)
    return target_params - bigframes_params


def generate_pandas_api_coverage():
    """Inspect all our pandas objects, and compare with the real pandas objects, to see
    which methods we implement. For each, generate a regex that can be used to check if
    its present in a notebook"""
    header = [
        "api",
        "pattern",
        "kind",
        "is_in_bigframes",
        "missing_parameters",
        "requires_index",
        "requires_ordering",
    ]
    api_patterns = []
    indexers = ["loc", "iloc", "iat", "ix", "at"]
    for name, pandas_obj, bigframes_obj in PANDAS_TARGETS:
        for member in dir(pandas_obj):
            missing_parameters = ""

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

                if hasattr(bigframes_obj, member):
                    bigframes_function = getattr(bigframes_obj, member)
                    pandas_function = getattr(pandas_obj, member)
                    missing_parameters = ", ".join(
                        sorted(
                            calculate_missing_parameters(
                                bigframes_function, pandas_function
                            )
                        )
                    )
            elif member in indexers:
                # Indexer, match .indexer[
                token = f"\\.{member}\\["
                token_type = "indexer"
            else:
                # Property
                token = f"\\.{member}\\b"
                token_type = "property"

            is_in_bigframes = hasattr(bigframes_obj, member)
            requires_index = ""
            requires_ordering = ""

            if is_in_bigframes:
                attr = getattr(bigframes_obj, member)

                # TODO(b/361101138): Add check/documentation for partial
                # support (e.g. with some parameters).
                requires_index = (
                    "Y" if hasattr(attr, "_validations_requires_index") else ""
                )
                requires_ordering = (
                    "Y" if hasattr(attr, "_validations_requires_ordering") else ""
                )

            api_patterns.append(
                [
                    f"{name}.{member}",
                    token,
                    token_type,
                    is_in_bigframes,
                    missing_parameters,
                    requires_index,
                    requires_ordering,
                ]
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
    # BigQuery only supports microsecond precision timestamps.
    combined_df["timestamp"] = combined_df["timestamp"].astype("datetime64[us]")
    combined_df["bigframes_version"] = bigframes_version
    combined_df["release_version"] = release_version
    combined_df = combined_df.infer_objects().convert_dtypes()
    return combined_df


def format_api(api_names, is_in_bigframes, api_prefix):
    api_names = api_names.str.slice(start=len(f"{api_prefix}."))
    formatted = "<code>" + api_names + "</code>"
    url_prefix = URL_PREFIX.get(api_prefix)
    if url_prefix is None:
        return formatted

    linked = '<a href="' + url_prefix + api_names + '">' + formatted + "</a>"
    return formatted.mask(is_in_bigframes, linked)


def generate_api_coverage(df, api_prefix):
    dataframe_apis = df.loc[df["api"].str.startswith(f"{api_prefix}.")]
    fully_implemented = (
        dataframe_apis["missing_parameters"].str.len() == 0
    ) & dataframe_apis["is_in_bigframes"]
    partial_implemented = (
        dataframe_apis["missing_parameters"].str.len() != 0
    ) & dataframe_apis["is_in_bigframes"]
    not_implemented = ~dataframe_apis["is_in_bigframes"]

    dataframe_table = pd.DataFrame(
        {
            "API": format_api(
                dataframe_apis["api"],
                dataframe_apis["is_in_bigframes"],
                api_prefix,
            ),
            "Implemented": "",
            "Requires index": dataframe_apis["requires_index"],
            "Requires ordering": dataframe_apis["requires_ordering"],
            "Missing parameters": dataframe_apis["missing_parameters"],
        }
    )
    dataframe_table.loc[fully_implemented, "Implemented"] = "Y"
    dataframe_table.loc[partial_implemented, "Implemented"] = "P"
    dataframe_table.loc[not_implemented, "Implemented"] = "N"
    return dataframe_table


def generate_api_coverage_doc(df, api_prefix):
    dataframe_table = generate_api_coverage(df, api_prefix)
    dataframe_table = dataframe_table.loc[~(dataframe_table["Implemented"] == "N")]
    dataframe_table["Implemented"] = dataframe_table["Implemented"].map(
        {
            "Y": "<b>Y</b>",
            "P": "<i>P</i>",
        }
    )

    with open(
        REPO_ROOT / "docs" / "supported_pandas_apis" / f"bf_{api_prefix}.html",
        "w",
    ) as html_file:
        dataframe_table.to_html(
            html_file, index=False, header=True, escape=False, border=0, col_space="8em"
        )


def generate_api_coverage_docs(df):
    for target in PANDAS_TARGETS:
        api_prefix = target[0]
        generate_api_coverage_doc(df, api_prefix)


def print_api_coverage_summary(df, api_prefix):
    dataframe_table = generate_api_coverage(df, api_prefix)

    print(api_prefix)
    print(dataframe_table[["Implemented", "API"]].groupby(["Implemented"]).count())
    print(f"{api_prefix} APIs: {dataframe_table.shape[0]}\n")


def print_api_coverage_summaries(df):
    for target in PANDAS_TARGETS:
        api_prefix = target[0]
        print_api_coverage_summary(df, api_prefix)

    print(f"\nAll APIs: {len(df.index)}")
    fully_implemented = (df["missing_parameters"].str.len() == 0) & df[
        "is_in_bigframes"
    ]
    print(f"Y: {fully_implemented.sum()}")
    partial_implemented = (df["missing_parameters"].str.len() != 0) & df[
        "is_in_bigframes"
    ]
    print(f"P: {partial_implemented.sum()}")
    not_implemented = ~df["is_in_bigframes"]
    print(f"N: {not_implemented.sum()}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_type")
    parser.add_argument("--bigframes_version", default=bigframes.__version__)
    parser.add_argument("--release_version", default="")
    parser.add_argument("--bigquery_table_name")
    args = parser.parse_args()
    df = build_api_coverage_table(args.bigframes_version, args.release_version)

    if args.output_type == "bigquery":
        df.to_gbq(args.bigquery_table_name, if_exists="append")
    elif args.output_type == "docs":
        generate_api_coverage_docs(df)
    elif args.output_type == "summary":
        print_api_coverage_summaries(df)
    else:
        print(f"Unexpected output_type {repr(args.output_type)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
