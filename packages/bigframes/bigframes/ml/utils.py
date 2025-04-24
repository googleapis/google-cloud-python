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

import typing
from typing import (
    Any,
    Generator,
    Hashable,
    Iterable,
    Literal,
    Mapping,
    Optional,
    Tuple,
    Union,
)

import bigframes_vendored.constants as constants
from google.cloud import bigquery
import pandas as pd

from bigframes.core import convert, guid
import bigframes.pandas as bpd
from bigframes.session import Session

# Internal type alias
ArrayType = Union[bpd.DataFrame, bpd.Series, pd.DataFrame, pd.Series]
BigFramesArrayType = Union[bpd.DataFrame, bpd.Series]


def batch_convert_to_dataframe(
    *input: ArrayType,
    session: Optional[Session] = None,
) -> Generator[bpd.DataFrame, None, None]:
    """Converts the input to BigFrames DataFrame.

    Args:
        session:
            The session to convert local pandas instances to BigFrames counter-parts.
            It is not used if the input itself is already a BigFrame data frame or series.

    """
    _validate_sessions(*input, session=session)

    return (
        convert.to_bf_dataframe(frame, default_index=None, session=session)
        for frame in input
    )


def batch_convert_to_series(
    *input: ArrayType, session: Optional[Session] = None
) -> Generator[bpd.Series, None, None]:
    """Converts the input to BigFrames Series.

    Args:
        session:
            The session to convert local pandas instances to BigFrames counter-parts.
            It is not used if the input itself is already a BigFrame data frame or series.

    """
    _validate_sessions(*input, session=session)

    return (
        convert.to_bf_series(
            _get_only_column(frame), default_index=None, session=session
        )
        for frame in input
    )


def _validate_sessions(*input: ArrayType, session: Optional[Session]):
    session_ids = set(
        i._session.session_id
        for i in input
        if isinstance(i, bpd.DataFrame) or isinstance(i, bpd.Series)
    )
    if len(session_ids) > 1:
        raise ValueError("Cannot convert data from multiple sessions")


def _get_only_column(input: ArrayType) -> Union[pd.Series, bpd.Series]:
    if isinstance(input, pd.Series) or isinstance(input, bpd.Series):
        return input

    if len(input.columns) != 1:
        raise ValueError(
            "To convert into Series, DataFrames can only contain one column. "
            f"Try input with only one column. {constants.FEEDBACK_LINK}"
        )

    label = typing.cast(Hashable, input.columns.tolist()[0])
    if isinstance(input, pd.DataFrame):
        return typing.cast(pd.Series, input[label])
    return typing.cast(bpd.Series, input[label])  # type: ignore


def parse_model_endpoint(model_endpoint: str) -> tuple[str, Optional[str]]:
    """Parse model endpoint string to model_name and version."""
    model_name = model_endpoint
    version = None

    if model_endpoint.startswith("multimodalembedding"):
        return model_name, version

    at_idx = model_endpoint.find("@")
    if at_idx != -1:
        version = model_endpoint[at_idx + 1 :]
        model_name = model_endpoint[:at_idx]

    return model_name, version


def _resolve_param_type(t: type) -> type:
    def is_optional(t):
        return typing.get_origin(t) is Union and type(None) in typing.get_args(t)

    # Optional[type] to type
    if is_optional(t):
        union_set = set(typing.get_args(t))
        union_set.remove(type(None))
        t = Union[tuple(union_set)]  # type: ignore

    # Literal[value0, value1...] to type(value0)
    if typing.get_origin(t) is Literal:
        return type(typing.get_args(t)[0])

    return t


def retrieve_params_from_bq_model(
    cls, bq_model: bigquery.Model, params_mapping: Mapping[str, str]
) -> dict[str, Any]:
    """Retrieve parameters of class constructor from BQ model. params_mapping specifies the names mapping param_name -> bqml_name. Params couldn't be found will be ignored."""
    kwargs = {}

    # See https://cloud.google.com/bigquery/docs/reference/rest/v2/models#trainingrun
    last_fitting = bq_model.training_runs[-1]["trainingOptions"]

    for bf_param, bf_param_type in typing.get_type_hints(cls.__init__).items():
        bqml_param = params_mapping.get(bf_param)
        if bqml_param in last_fitting:
            bf_param_type = _resolve_param_type(bf_param_type)
            kwargs[bf_param] = bf_param_type(last_fitting[bqml_param])

    return kwargs


def combine_training_and_evaluation_data(
    X_train: bpd.DataFrame,
    y_train: bpd.DataFrame,
    X_eval: bpd.DataFrame,
    y_eval: bpd.DataFrame,
    bqml_options: dict,
) -> Tuple[bpd.DataFrame, bpd.DataFrame, dict]:
    """
    Combine training data and labels with evlauation data and labels, and keep
    them differentiated through a split column in the combined data and labels.
    """

    assert X_train.columns.equals(X_eval.columns)
    assert y_train.columns.equals(y_eval.columns)

    # create a custom split column for BQML and supply the evaluation
    # data along with the training data in a combined single table
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#data_split_col.
    split_col = guid.generate_guid()
    assert split_col not in X_train.columns

    X_train[split_col] = False
    X_eval[split_col] = True
    X = bpd.concat([X_train, X_eval])
    y = bpd.concat([y_train, y_eval])

    # create options copy to not mutate the incoming one
    bqml_options = bqml_options.copy()
    bqml_options["data_split_method"] = "CUSTOM"
    bqml_options["data_split_col"] = split_col

    return X, y, bqml_options


def standardize_type(v: str, supported_dtypes: Optional[Iterable[str]] = None):
    t = v.lower()
    t = t.replace("boolean", "bool")

    if supported_dtypes:
        if t not in supported_dtypes:
            raise ValueError(
                f"Data type {v} is not supported. We only support {', '.join(supported_dtypes)}."
            )

    return t
