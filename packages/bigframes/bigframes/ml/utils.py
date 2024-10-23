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
from typing import Any, Generator, Literal, Mapping, Optional, Union

import bigframes_vendored.constants as constants
from google.cloud import bigquery
import pandas as pd

from bigframes.core import blocks
import bigframes.pandas as bpd
from bigframes.session import Session

# Internal type alias
ArrayType = Union[bpd.DataFrame, bpd.Series, pd.DataFrame, pd.Series]
BigFramesArrayType = Union[bpd.DataFrame, bpd.Series]


def convert_to_dataframe(
    *input: ArrayType,
    session: Optional[Session] = None,
) -> Generator[bpd.DataFrame, None, None]:
    """Converts the input to BigFrames DataFrame.

    Args:
        session:
            The session to convert local pandas instances to BigFrames counter-parts.
            It is not used if the input itself is already a BigFrame data frame or series.

    """
    return (_convert_to_dataframe(frame, session) for frame in input)


def _convert_to_dataframe(
    frame: ArrayType, session: Optional[Session] = None
) -> bpd.DataFrame:
    if isinstance(frame, bpd.DataFrame):
        return frame
    if isinstance(frame, bpd.Series):
        return frame.to_frame()
    if isinstance(frame, pd.DataFrame):
        if session is None:
            return bpd.read_pandas(frame)
        else:
            return session.read_pandas(frame)
    if isinstance(frame, pd.Series):
        if session is None:
            return bpd.read_pandas(frame).to_frame()
        else:
            return session.read_pandas(frame).to_frame()
    raise ValueError(
        f"Unsupported type {type(frame)} to convert to DataFrame. {constants.FEEDBACK_LINK}"
    )


def convert_to_series(
    *input: ArrayType, session: Optional[Session] = None
) -> Generator[bpd.Series, None, None]:
    """Converts the input to BigFrames Series.

    Args:
        session:
            The session to convert local pandas instances to BigFrames counter-parts.
            It is not used if the input itself is already a BigFrame data frame or series.

    """
    return (_convert_to_series(frame, session) for frame in input)


def _convert_to_series(
    frame: ArrayType, session: Optional[Session] = None
) -> bpd.Series:
    if isinstance(frame, bpd.DataFrame):
        if len(frame.columns) != 1:
            raise ValueError(
                "To convert into Series, DataFrames can only contain one column. "
                f"Try input with only one column. {constants.FEEDBACK_LINK}"
            )

        label = typing.cast(blocks.Label, frame.columns.tolist()[0])
        return typing.cast(bpd.Series, frame[label])
    if isinstance(frame, bpd.Series):
        return frame
    if isinstance(frame, pd.DataFrame):
        # Recursively call this method to re-use the length-checking logic
        if session is None:
            return _convert_to_series(bpd.read_pandas(frame))
        else:
            return _convert_to_series(session.read_pandas(frame), session)
    if isinstance(frame, pd.Series):
        if session is None:
            return bpd.read_pandas(frame)
        else:
            return session.read_pandas(frame)
    raise ValueError(
        f"Unsupported type {type(frame)} to convert to Series. {constants.FEEDBACK_LINK}"
    )


def parse_model_endpoint(model_endpoint: str) -> tuple[str, Optional[str]]:
    """Parse model endpoint string to model_name and version."""
    model_name = model_endpoint
    version = None

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
