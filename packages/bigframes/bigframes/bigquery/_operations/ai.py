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

"""This module integrates BigQuery built-in AI functions for use with Series/DataFrame objects,
such as AI.GENERATE_BOOL:
https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-bool"""

from __future__ import annotations

import json
from typing import Any, Iterable, List, Literal, Mapping, Tuple, Union

import pandas as pd

from bigframes import clients, dataframe, dtypes
from bigframes import pandas as bpd
from bigframes import series, session
from bigframes.core import convert, log_adapter
from bigframes.ml import core as ml_core
from bigframes.operations import ai_ops, output_schemas

PROMPT_TYPE = Union[
    str,
    series.Series,
    pd.Series,
    List[Union[str, series.Series, pd.Series]],
    Tuple[Union[str, series.Series, pd.Series], ...],
]


@log_adapter.method_logger(custom_base_name="bigquery_ai")
def generate(
    prompt: PROMPT_TYPE,
    *,
    connection_id: str | None = None,
    endpoint: str | None = None,
    request_type: Literal["dedicated", "shared", "unspecified"] = "unspecified",
    model_params: Mapping[Any, Any] | None = None,
    output_schema: Mapping[str, str] | None = None,
) -> series.Series:
    """
    Returns the AI analysis based on the prompt, which can be any combination of text and unstructured data.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> country = bpd.Series(["Japan", "Canada"])
        >>> bbq.ai.generate(("What's the capital city of ", country, " one word only"))
        0    {'result': 'Tokyo\\n', 'full_response': '{"cand...
        1    {'result': 'Ottawa\\n', 'full_response': '{"can...
        dtype: struct<result: string, full_response: extension<dbjson<JSONArrowType>>, status: string>[pyarrow]

        >>> bbq.ai.generate(("What's the capital city of ", country, " one word only")).struct.field("result")
        0     Tokyo\\n
        1    Ottawa\\n
        Name: result, dtype: string

    You get structured output when the `output_schema` parameter is set:

        >>> animals = bpd.Series(["Rabbit", "Spider"])
        >>> bbq.ai.generate(animals, output_schema={"number_of_legs": "INT64", "is_herbivore": "BOOL"})
        0    {'is_herbivore': True, 'number_of_legs': 4, 'f...
        1    {'is_herbivore': False, 'number_of_legs': 8, '...
        dtype: struct<is_herbivore: bool, number_of_legs: int64, full_response: extension<dbjson<JSONArrowType>>, status: string>[pyarrow]

    .. note::

        This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).

    Args:
        prompt (str | Series | List[str|Series] | Tuple[str|Series, ...]):
            A mixture of Series and string literals that specifies the prompt to send to the model. The Series can be BigFrames Series
            or pandas Series.
        connection_id (str, optional):
            Specifies the connection to use to communicate with the model. For example, `myproject.us.myconnection`.
            If not provided, the connection from the current session will be used.
        endpoint (str, optional):
            Specifies the Vertex AI endpoint to use for the model. For example `"gemini-2.5-flash"`. You can specify any
            generally available or preview Gemini model. If you specify the model name, BigQuery ML automatically identifies and
            uses the full endpoint of the model. If you don't specify an ENDPOINT value, BigQuery ML selects a recent stable
            version of Gemini to use.
        request_type (Literal["dedicated", "shared", "unspecified"]):
            Specifies the type of inference request to send to the Gemini model. The request type determines what quota the request uses.
            * "dedicated": function only uses Provisioned Throughput quota. The function returns the error Provisioned throughput is not
            purchased or is not active if Provisioned Throughput quota isn't available.
            * "shared": the function only uses dynamic shared quota (DSQ), even if you have purchased Provisioned Throughput quota.
            * "unspecified": If you haven't purchased Provisioned Throughput quota, the function uses DSQ quota.
            If you have purchased Provisioned Throughput quota, the function uses the Provisioned Throughput quota first.
            If requests exceed the Provisioned Throughput quota, the overflow traffic uses DSQ quota.
        model_params (Mapping[Any, Any]):
            Provides additional parameters to the model. The MODEL_PARAMS value must conform to the generateContent request body format.
        output_schema (Mapping[str, str]):
            A mapping value that specifies the schema of the output, in the form {field_name: data_type}. Supported data types include
            `STRING`, `INT64`, `FLOAT64`, `BOOL`, `ARRAY`, and `STRUCT`.

    Returns:
        bigframes.series.Series: A new struct Series with the result data. The struct contains these fields:
        * "result": a STRING value containing the model's response to the prompt. The result is None if the request fails or is filtered by responsible AI.
        If you specify an output schema then result is replaced by your custom schema.
        * "full_response": a JSON value containing the response from the projects.locations.endpoints.generateContent call to the model.
        The generated text is in the text element.
        * "status": a STRING value that contains the API response status for the corresponding row. This value is empty if the operation was successful.
    """

    prompt_context, series_list = _separate_context_and_series(prompt)
    assert len(series_list) > 0

    if output_schema is None:
        output_schema_str = None
    else:
        output_schema_str = ", ".join(
            [f"{name} {sql_type}" for name, sql_type in output_schema.items()]
        )
        # Validate user input
        output_schemas.parse_sql_fields(output_schema_str)

    operator = ai_ops.AIGenerate(
        prompt_context=tuple(prompt_context),
        connection_id=_resolve_connection_id(series_list[0], connection_id),
        endpoint=endpoint,
        request_type=request_type,
        model_params=json.dumps(model_params) if model_params else None,
        output_schema=output_schema_str,
    )

    return series_list[0]._apply_nary_op(operator, series_list[1:])


@log_adapter.method_logger(custom_base_name="bigquery_ai")
def generate_bool(
    prompt: PROMPT_TYPE,
    *,
    connection_id: str | None = None,
    endpoint: str | None = None,
    request_type: Literal["dedicated", "shared", "unspecified"] = "unspecified",
    model_params: Mapping[Any, Any] | None = None,
) -> series.Series:
    """
    Returns the AI analysis based on the prompt, which can be any combination of text and unstructured data.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> df = bpd.DataFrame({
        ...     "col_1": ["apple", "bear", "pear"],
        ...     "col_2": ["fruit", "animal", "animal"]
        ... })
        >>> bbq.ai.generate_bool((df["col_1"], " is a ", df["col_2"]))
        0    {'result': True, 'full_response': '{"candidate...
        1    {'result': True, 'full_response': '{"candidate...
        2    {'result': False, 'full_response': '{"candidat...
        dtype: struct<result: bool, full_response: extension<dbjson<JSONArrowType>>, status: string>[pyarrow]

        >>> bbq.ai.generate_bool((df["col_1"], " is a ", df["col_2"])).struct.field("result")
        0     True
        1     True
        2    False
        Name: result, dtype: boolean

    .. note::

        This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).

    Args:
        prompt (str | Series | List[str|Series] | Tuple[str|Series, ...]):
            A mixture of Series and string literals that specifies the prompt to send to the model. The Series can be BigFrames Series
            or pandas Series.
        connection_id (str, optional):
            Specifies the connection to use to communicate with the model. For example, `myproject.us.myconnection`.
            If not provided, the connection from the current session will be used.
        endpoint (str, optional):
            Specifies the Vertex AI endpoint to use for the model. For example `"gemini-2.5-flash"`. You can specify any
            generally available or preview Gemini model. If you specify the model name, BigQuery ML automatically identifies and
            uses the full endpoint of the model. If you don't specify an ENDPOINT value, BigQuery ML selects a recent stable
            version of Gemini to use.
        request_type (Literal["dedicated", "shared", "unspecified"]):
            Specifies the type of inference request to send to the Gemini model. The request type determines what quota the request uses.
            * "dedicated": function only uses Provisioned Throughput quota. The function returns the error Provisioned throughput is not
            purchased or is not active if Provisioned Throughput quota isn't available.
            * "shared": the function only uses dynamic shared quota (DSQ), even if you have purchased Provisioned Throughput quota.
            * "unspecified": If you haven't purchased Provisioned Throughput quota, the function uses DSQ quota.
            If you have purchased Provisioned Throughput quota, the function uses the Provisioned Throughput quota first.
            If requests exceed the Provisioned Throughput quota, the overflow traffic uses DSQ quota.
        model_params (Mapping[Any, Any]):
            Provides additional parameters to the model. The MODEL_PARAMS value must conform to the generateContent request body format.

    Returns:
        bigframes.series.Series: A new struct Series with the result data. The struct contains these fields:
        * "result": a BOOL value containing the model's response to the prompt. The result is None if the request fails or is filtered by responsible AI.
        * "full_response": a JSON value containing the response from the projects.locations.endpoints.generateContent call to the model.
        The generated text is in the text element.
        * "status": a STRING value that contains the API response status for the corresponding row. This value is empty if the operation was successful.
    """

    prompt_context, series_list = _separate_context_and_series(prompt)
    assert len(series_list) > 0

    operator = ai_ops.AIGenerateBool(
        prompt_context=tuple(prompt_context),
        connection_id=_resolve_connection_id(series_list[0], connection_id),
        endpoint=endpoint,
        request_type=request_type,
        model_params=json.dumps(model_params) if model_params else None,
    )

    return series_list[0]._apply_nary_op(operator, series_list[1:])


@log_adapter.method_logger(custom_base_name="bigquery_ai")
def generate_int(
    prompt: PROMPT_TYPE,
    *,
    connection_id: str | None = None,
    endpoint: str | None = None,
    request_type: Literal["dedicated", "shared", "unspecified"] = "unspecified",
    model_params: Mapping[Any, Any] | None = None,
) -> series.Series:
    """
    Returns the AI analysis based on the prompt, which can be any combination of text and unstructured data.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> animal = bpd.Series(["Kangaroo", "Rabbit", "Spider"])
        >>> bbq.ai.generate_int(("How many legs does a ", animal, " have?"))
        0    {'result': 2, 'full_response': '{"candidates":...
        1    {'result': 4, 'full_response': '{"candidates":...
        2    {'result': 8, 'full_response': '{"candidates":...
        dtype: struct<result: int64, full_response: extension<dbjson<JSONArrowType>>, status: string>[pyarrow]

        >>> bbq.ai.generate_int(("How many legs does a ", animal, " have?")).struct.field("result")
        0    2
        1    4
        2    8
        Name: result, dtype: Int64

    .. note::

        This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).

    Args:
        prompt (str | Series | List[str|Series] | Tuple[str|Series, ...]):
            A mixture of Series and string literals that specifies the prompt to send to the model. The Series can be BigFrames Series
            or pandas Series.
        connection_id (str, optional):
            Specifies the connection to use to communicate with the model. For example, `myproject.us.myconnection`.
            If not provided, the connection from the current session will be used.
        endpoint (str, optional):
            Specifies the Vertex AI endpoint to use for the model. For example `"gemini-2.5-flash"`. You can specify any
            generally available or preview Gemini model. If you specify the model name, BigQuery ML automatically identifies and
            uses the full endpoint of the model. If you don't specify an ENDPOINT value, BigQuery ML selects a recent stable
            version of Gemini to use.
        request_type (Literal["dedicated", "shared", "unspecified"]):
            Specifies the type of inference request to send to the Gemini model. The request type determines what quota the request uses.
            * "dedicated": function only uses Provisioned Throughput quota. The function returns the error Provisioned throughput is not
            purchased or is not active if Provisioned Throughput quota isn't available.
            * "shared": the function only uses dynamic shared quota (DSQ), even if you have purchased Provisioned Throughput quota.
            * "unspecified": If you haven't purchased Provisioned Throughput quota, the function uses DSQ quota.
            If you have purchased Provisioned Throughput quota, the function uses the Provisioned Throughput quota first.
            If requests exceed the Provisioned Throughput quota, the overflow traffic uses DSQ quota.
        model_params (Mapping[Any, Any]):
            Provides additional parameters to the model. The MODEL_PARAMS value must conform to the generateContent request body format.

    Returns:
        bigframes.series.Series: A new struct Series with the result data. The struct contains these fields:
        * "result": an integer (INT64) value containing the model's response to the prompt. The result is None if the request fails or is filtered by responsible AI.
        * "full_response": a JSON value containing the response from the projects.locations.endpoints.generateContent call to the model.
        The generated text is in the text element.
        * "status": a STRING value that contains the API response status for the corresponding row. This value is empty if the operation was successful.
    """

    prompt_context, series_list = _separate_context_and_series(prompt)
    assert len(series_list) > 0

    operator = ai_ops.AIGenerateInt(
        prompt_context=tuple(prompt_context),
        connection_id=_resolve_connection_id(series_list[0], connection_id),
        endpoint=endpoint,
        request_type=request_type,
        model_params=json.dumps(model_params) if model_params else None,
    )

    return series_list[0]._apply_nary_op(operator, series_list[1:])


@log_adapter.method_logger(custom_base_name="bigquery_ai")
def generate_double(
    prompt: PROMPT_TYPE,
    *,
    connection_id: str | None = None,
    endpoint: str | None = None,
    request_type: Literal["dedicated", "shared", "unspecified"] = "unspecified",
    model_params: Mapping[Any, Any] | None = None,
) -> series.Series:
    """
    Returns the AI analysis based on the prompt, which can be any combination of text and unstructured data.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> animal = bpd.Series(["Kangaroo", "Rabbit", "Spider"])
        >>> bbq.ai.generate_double(("How many legs does a ", animal, " have?"))
        0    {'result': 2.0, 'full_response': '{"candidates...
        1    {'result': 4.0, 'full_response': '{"candidates...
        2    {'result': 8.0, 'full_response': '{"candidates...
        dtype: struct<result: double, full_response: extension<dbjson<JSONArrowType>>, status: string>[pyarrow]

        >>> bbq.ai.generate_double(("How many legs does a ", animal, " have?")).struct.field("result")
        0    2.0
        1    4.0
        2    8.0
        Name: result, dtype: Float64

    .. note::

        This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).

    Args:
        prompt (str | Series | List[str|Series] | Tuple[str|Series, ...]):
            A mixture of Series and string literals that specifies the prompt to send to the model. The Series can be BigFrames Series
            or pandas Series.
        connection_id (str, optional):
            Specifies the connection to use to communicate with the model. For example, `myproject.us.myconnection`.
            If not provided, the connection from the current session will be used.
        endpoint (str, optional):
            Specifies the Vertex AI endpoint to use for the model. For example `"gemini-2.5-flash"`. You can specify any
            generally available or preview Gemini model. If you specify the model name, BigQuery ML automatically identifies and
            uses the full endpoint of the model. If you don't specify an ENDPOINT value, BigQuery ML selects a recent stable
            version of Gemini to use.
        request_type (Literal["dedicated", "shared", "unspecified"]):
            Specifies the type of inference request to send to the Gemini model. The request type determines what quota the request uses.
            * "dedicated": function only uses Provisioned Throughput quota. The function returns the error Provisioned throughput is not
            purchased or is not active if Provisioned Throughput quota isn't available.
            * "shared": the function only uses dynamic shared quota (DSQ), even if you have purchased Provisioned Throughput quota.
            * "unspecified": If you haven't purchased Provisioned Throughput quota, the function uses DSQ quota.
            If you have purchased Provisioned Throughput quota, the function uses the Provisioned Throughput quota first.
            If requests exceed the Provisioned Throughput quota, the overflow traffic uses DSQ quota.
        model_params (Mapping[Any, Any]):
            Provides additional parameters to the model. The MODEL_PARAMS value must conform to the generateContent request body format.

    Returns:
        bigframes.series.Series: A new struct Series with the result data. The struct contains these fields:
        * "result": an DOUBLE value containing the model's response to the prompt. The result is None if the request fails or is filtered by responsible AI.
        * "full_response": a JSON value containing the response from the projects.locations.endpoints.generateContent call to the model.
        The generated text is in the text element.
        * "status": a STRING value that contains the API response status for the corresponding row. This value is empty if the operation was successful.
    """

    prompt_context, series_list = _separate_context_and_series(prompt)
    assert len(series_list) > 0

    operator = ai_ops.AIGenerateDouble(
        prompt_context=tuple(prompt_context),
        connection_id=_resolve_connection_id(series_list[0], connection_id),
        endpoint=endpoint,
        request_type=request_type,
        model_params=json.dumps(model_params) if model_params else None,
    )

    return series_list[0]._apply_nary_op(operator, series_list[1:])


@log_adapter.method_logger(custom_base_name="bigquery_ai")
def if_(
    prompt: PROMPT_TYPE,
    *,
    connection_id: str | None = None,
) -> series.Series:
    """
    Evaluates the prompt to True or False. Compared to `ai.generate_bool()`, this function
    provides optimization such that not all rows are evaluated with the LLM.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> us_state = bpd.Series(["Massachusetts", "Illinois", "Hawaii"])
        >>> bbq.ai.if_((us_state, " has a city called Springfield"))
        0     True
        1     True
        2    False
        dtype: boolean

        >>> us_state[bbq.ai.if_((us_state, " has a city called Springfield"))]
        0    Massachusetts
        1         Illinois
        dtype: string

    .. note::

        This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).

    Args:
        prompt (str | Series | List[str|Series] | Tuple[str|Series, ...]):
            A mixture of Series and string literals that specifies the prompt to send to the model. The Series can be BigFrames Series
            or pandas Series.
        connection_id (str, optional):
            Specifies the connection to use to communicate with the model. For example, `myproject.us.myconnection`.
            If not provided, the connection from the current session will be used.

    Returns:
        bigframes.series.Series: A new series of bools.
    """

    prompt_context, series_list = _separate_context_and_series(prompt)
    assert len(series_list) > 0

    operator = ai_ops.AIIf(
        prompt_context=tuple(prompt_context),
        connection_id=_resolve_connection_id(series_list[0], connection_id),
    )

    return series_list[0]._apply_nary_op(operator, series_list[1:])


@log_adapter.method_logger(custom_base_name="bigquery_ai")
def classify(
    input: PROMPT_TYPE,
    categories: tuple[str, ...] | list[str],
    *,
    connection_id: str | None = None,
) -> series.Series:
    """
    Classifies a given input into one of the specified categories. It will always return one of the provided categories best fit the prompt input.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> df = bpd.DataFrame({'creature': ['Cat', 'Salmon']})
        >>> df['type'] = bbq.ai.classify(df['creature'], ['Mammal', 'Fish'])
        >>> df
          creature    type
        0      Cat  Mammal
        1   Salmon    Fish
        <BLANKLINE>
        [2 rows x 2 columns]

    .. note::

        This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).

    Args:
        input (str | Series | List[str|Series] | Tuple[str|Series, ...]):
            A mixture of Series and string literals that specifies the input to send to the model. The Series can be BigFrames Series
            or pandas Series.
        categories (tuple[str, ...] | list[str]):
            Categories to classify the input into.
        connection_id (str, optional):
            Specifies the connection to use to communicate with the model. For example, `myproject.us.myconnection`.
            If not provided, the connection from the current session will be used.

    Returns:
        bigframes.series.Series: A new series of strings.
    """

    prompt_context, series_list = _separate_context_and_series(input)
    assert len(series_list) > 0

    operator = ai_ops.AIClassify(
        prompt_context=tuple(prompt_context),
        categories=tuple(categories),
        connection_id=_resolve_connection_id(series_list[0], connection_id),
    )

    return series_list[0]._apply_nary_op(operator, series_list[1:])


@log_adapter.method_logger(custom_base_name="bigquery_ai")
def score(
    prompt: PROMPT_TYPE,
    *,
    connection_id: str | None = None,
) -> series.Series:
    """
    Computes a score based on rubrics described in natural language. It will return a double value.
    There is no fixed range for the score returned. To get high quality results, provide a scoring
    rubric with examples in the prompt.

    **Examples:**

        >>> import bigframes.pandas as bpd
        >>> import bigframes.bigquery as bbq
        >>> animal = bpd.Series(["Tiger", "Rabbit", "Blue Whale"])
        >>> bbq.ai.score(("Rank the relative weights of ", animal, " on the scale from 1 to 3")) # doctest: +SKIP
        0    2.0
        1    1.0
        2    3.0
        dtype: Float64

    .. note::

        This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).

    Args:
        prompt (str | Series | List[str|Series] | Tuple[str|Series, ...]):
            A mixture of Series and string literals that specifies the prompt to send to the model. The Series can be BigFrames Series
            or pandas Series.
        connection_id (str, optional):
            Specifies the connection to use to communicate with the model. For example, `myproject.us.myconnection`.
            If not provided, the connection from the current session will be used.

    Returns:
        bigframes.series.Series: A new series of double (float) values.
    """

    prompt_context, series_list = _separate_context_and_series(prompt)
    assert len(series_list) > 0

    operator = ai_ops.AIScore(
        prompt_context=tuple(prompt_context),
        connection_id=_resolve_connection_id(series_list[0], connection_id),
    )

    return series_list[0]._apply_nary_op(operator, series_list[1:])


@log_adapter.method_logger(custom_base_name="bigquery_ai")
def forecast(
    df: dataframe.DataFrame | pd.DataFrame,
    *,
    data_col: str,
    timestamp_col: str,
    model: str = "TimesFM 2.0",
    id_cols: Iterable[str] | None = None,
    horizon: int = 10,
    confidence_level: float = 0.95,
    context_window: int | None = None,
) -> dataframe.DataFrame:
    """
    Forecast time series at future horizon. Using Google Research's open source TimesFM(https://github.com/google-research/timesfm) model.

    .. note::

        This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the
        Service Specific Terms(https://cloud.google.com/terms/service-terms#1). Pre-GA products and features are available "as is"
        and might have limited support. For more information, see the launch stage descriptions
        (https://cloud.google.com/products#product-launch-stages).

    Args:
        df (DataFrame):
            The dataframe that contains the data that you want to forecast. It could be either a BigFrames Dataframe or
            a pandas DataFrame. If it's a pandas DataFrame, the global BigQuery session will be used to load the data.
        data_col (str):
            A str value that specifies the name of the data column. The data column contains the data to forecast.
            The data column must use one of the following data types: INT64, NUMERIC and FLOAT64
        timestamp_col (str):
            A str value that specified the name of the time points column.
            The time points column provides the time points used to generate the forecast.
            The time points column must use one of the following data types: TIMESTAMP, DATE and DATETIME
        model (str, default "TimesFM 2.0"):
            A str value that specifies the name of the model. TimesFM 2.0 is the only supported value, and is the default value.
        id_cols (Iterable[str], optional):
            An iterable of str value that specifies the names of one or more ID columns. Each ID identifies a unique time series to forecast.
            Specify one or more values for this argument in order to forecast multiple time series using a single query.
            The columns that you specify must use one of the following data types: STRING, INT64, ARRAY<STRING> and ARRAY<INT64>
        horizon (int, default 10):
            An int value that specifies the number of time points to forecast. The default value is 10. The valid input range is [1, 10,000].
        confidence_level (float, default 0.95):
            A FLOAT64 value that specifies the percentage of the future values that fall in the prediction interval.
            The default value is 0.95. The valid input range is [0, 1).
        context_window (int, optional):
            An int value that specifies the context window length used by BigQuery ML's built-in TimesFM model.
            The context window length determines how many of the most recent data points from the input time series are use by the model.
            If you don't specify a value, the AI.FORECAST function automatically chooses the smallest possible context window length to use
            that is still large enough to cover the number of time series data points in your input data.

    Returns:
        DataFrame:
            The forecast dataframe matches that of the BigQuery AI.FORECAST function.
            See: https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast

    Raises:
        ValueError: when any column ID does not exist in the dataframe.
    """

    if isinstance(df, pd.DataFrame):
        # Load the pandas DataFrame with global session
        df = bpd.read_pandas(df)

    columns = [timestamp_col, data_col]
    if id_cols:
        columns += id_cols
    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Column `{column}` not found")

    options: dict[str, Union[int, float, str, Iterable[str]]] = {
        "data_col": data_col,
        "timestamp_col": timestamp_col,
        "model": model,
        "horizon": horizon,
        "confidence_level": confidence_level,
    }
    if id_cols:
        options["id_cols"] = id_cols
    if context_window:
        options["context_window"] = context_window

    return ml_core.BaseBqml(df._session).ai_forecast(input_data=df, options=options)


def _separate_context_and_series(
    prompt: PROMPT_TYPE,
) -> Tuple[List[str | None], List[series.Series]]:
    """
    Returns the two values. The first value is the prompt with all series replaced by None. The second value is all the series
    in the prompt. The original item order is kept.
    For example:
    Input: ("str1", series1, "str2", "str3", series2)
    Output: ["str1", None, "str2", "str3", None], [series1, series2]
    """
    if not isinstance(prompt, (str, list, tuple, series.Series)):
        raise ValueError(f"Unsupported prompt type: {type(prompt)}")

    if isinstance(prompt, str):
        return [None], [series.Series([prompt])]

    if isinstance(prompt, series.Series):
        if prompt.dtype == dtypes.OBJ_REF_DTYPE:
            # Multi-model support
            return [None], [prompt.blob.read_url()]
        return [None], [prompt]

    prompt_context: List[str | None] = []
    series_list: List[series.Series | pd.Series] = []

    session = None
    for item in prompt:
        if isinstance(item, str):
            prompt_context.append(item)

        elif isinstance(item, (series.Series, pd.Series)):
            prompt_context.append(None)

            if isinstance(item, series.Series) and session is None:
                # Use the first available BF session if there's any.
                session = item._session
            series_list.append(item)

        else:
            raise TypeError(f"Unsupported type in prompt: {type(item)}")

    if not series_list:
        raise ValueError("Please provide at least one Series in the prompt")

    converted_list = [_convert_series(s, session) for s in series_list]

    return prompt_context, converted_list


def _convert_series(
    s: series.Series | pd.Series, session: session.Session | None
) -> series.Series:
    result = convert.to_bf_series(s, default_index=None, session=session)

    if result.dtype == dtypes.OBJ_REF_DTYPE:
        # Support multimodel
        return result.blob.read_url()
    return result


def _resolve_connection_id(series: series.Series, connection_id: str | None):
    return clients.get_canonical_bq_connection_id(
        connection_id or series._session._bq_connection,
        series._session._project,
        series._session._location,
    )
