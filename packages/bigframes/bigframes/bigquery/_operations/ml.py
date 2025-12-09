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

from __future__ import annotations

from typing import cast, Mapping, Optional, Union

import bigframes_vendored.constants
import google.cloud.bigquery
import pandas as pd

import bigframes.core.log_adapter as log_adapter
import bigframes.core.sql.ml
import bigframes.dataframe as dataframe
import bigframes.ml.base
import bigframes.session


# Helper to convert DataFrame to SQL string
def _to_sql(df_or_sql: Union[pd.DataFrame, dataframe.DataFrame, str]) -> str:
    import bigframes.pandas as bpd

    if isinstance(df_or_sql, str):
        return df_or_sql

    if isinstance(df_or_sql, pd.DataFrame):
        bf_df = bpd.read_pandas(df_or_sql)
    else:
        bf_df = cast(dataframe.DataFrame, df_or_sql)

    # Cache dataframes to make sure base table is not a snapshot.
    # Cached dataframe creates a full copy, never uses snapshot.
    # This is a workaround for internal issue b/310266666.
    bf_df.cache()
    sql, _, _ = bf_df._to_sql_query(include_index=False)
    return sql


def _get_model_name_and_session(
    model: Union[bigframes.ml.base.BaseEstimator, str, pd.Series],
    # Other dataframe arguments to extract session from
    *dataframes: Optional[Union[pd.DataFrame, dataframe.DataFrame, str]],
) -> tuple[str, Optional[bigframes.session.Session]]:
    if isinstance(model, pd.Series):
        try:
            model_ref = model["modelReference"]
            model_name = f"{model_ref['projectId']}.{model_ref['datasetId']}.{model_ref['modelId']}"  # type: ignore
        except KeyError:
            raise ValueError("modelReference must be present in the pandas Series.")
    elif isinstance(model, str):
        model_name = model
    else:
        if model._bqml_model is None:
            raise ValueError("Model must be fitted to be used in ML operations.")
        return model._bqml_model.model_name, model._bqml_model.session

    session = None
    for df in dataframes:
        if isinstance(df, dataframe.DataFrame):
            session = df._session
            break

    return model_name, session


def _get_model_metadata(
    *,
    bqclient: google.cloud.bigquery.Client,
    model_name: str,
) -> pd.Series:
    model_metadata = bqclient.get_model(model_name)
    model_dict = model_metadata.to_api_repr()
    return pd.Series(model_dict)


@log_adapter.method_logger(custom_base_name="bigquery_ml")
def create_model(
    model_name: str,
    *,
    replace: bool = False,
    if_not_exists: bool = False,
    # TODO(tswast): Also support bigframes.ml transformer classes and/or
    # bigframes.pandas functions?
    transform: Optional[list[str]] = None,
    input_schema: Optional[Mapping[str, str]] = None,
    output_schema: Optional[Mapping[str, str]] = None,
    connection_name: Optional[str] = None,
    options: Optional[Mapping[str, Union[str, int, float, bool, list]]] = None,
    training_data: Optional[Union[pd.DataFrame, dataframe.DataFrame, str]] = None,
    custom_holiday: Optional[Union[pd.DataFrame, dataframe.DataFrame, str]] = None,
    session: Optional[bigframes.session.Session] = None,
) -> pd.Series:
    """
    Creates a BigQuery ML model.

    See the `BigQuery ML CREATE MODEL DDL syntax
    <https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create>`_
    for additional reference.

    Args:
        model_name (str):
            The name of the model in BigQuery.
        replace (bool, default False):
            Whether to replace the model if it already exists.
        if_not_exists (bool, default False):
            Whether to ignore the error if the model already exists.
        transform (list[str], optional):
            A list of SQL transformations for the TRANSFORM clause, which
            specifies the preprocessing steps to apply to the input data.
        input_schema (Mapping[str, str], optional):
            The INPUT clause, which specifies the schema of the input data.
        output_schema (Mapping[str, str], optional):
            The OUTPUT clause, which specifies the schema of the output data.
        connection_name (str, optional):
            The connection to use for the model.
        options (Mapping[str, Union[str, int, float, bool, list]], optional):
            The OPTIONS clause, which specifies the model options.
        training_data (Union[bigframes.pandas.DataFrame, str], optional):
            The query or DataFrame to use for training the model.
        custom_holiday (Union[bigframes.pandas.DataFrame, str], optional):
            The query or DataFrame to use for custom holiday data.
        session (bigframes.session.Session, optional):
            The session to use. If not provided, the default session is used.

    Returns:
        pandas.Series:
            A Series with object dtype containing the model metadata. Reference
            the `BigQuery Model REST API reference
            <https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models#Model>`_
            for available fields.

    """
    import bigframes.pandas as bpd

    training_data_sql = _to_sql(training_data) if training_data is not None else None
    custom_holiday_sql = _to_sql(custom_holiday) if custom_holiday is not None else None

    # Determine session from DataFrames if not provided
    if session is None:
        # Try to get session from inputs
        dfs = [
            obj
            for obj in [training_data, custom_holiday]
            if isinstance(obj, dataframe.DataFrame)
        ]
        if dfs:
            session = dfs[0]._session

    sql = bigframes.core.sql.ml.create_model_ddl(
        model_name=model_name,
        replace=replace,
        if_not_exists=if_not_exists,
        transform=transform,
        input_schema=input_schema,
        output_schema=output_schema,
        connection_name=connection_name,
        options=options,
        training_data=training_data_sql,
        custom_holiday=custom_holiday_sql,
    )

    if session is None:
        bpd.read_gbq_query(sql)
        session = bpd.get_global_session()
        assert (
            session is not None
        ), f"Missing connection to BigQuery. Please report how you encountered this error at {bigframes_vendored.constants.FEEDBACK_LINK}."
    else:
        session.read_gbq_query(sql)

    return _get_model_metadata(bqclient=session.bqclient, model_name=model_name)


@log_adapter.method_logger(custom_base_name="bigquery_ml")
def evaluate(
    model: Union[bigframes.ml.base.BaseEstimator, str, pd.Series],
    input_: Optional[Union[pd.DataFrame, dataframe.DataFrame, str]] = None,
    *,
    perform_aggregation: Optional[bool] = None,
    horizon: Optional[int] = None,
    confidence_level: Optional[float] = None,
) -> dataframe.DataFrame:
    """
    Evaluates a BigQuery ML model.

    See the `BigQuery ML EVALUATE function syntax
    <https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate>`_
    for additional reference.

    Args:
        model (bigframes.ml.base.BaseEstimator or str):
            The model to evaluate.
        input_ (Union[bigframes.pandas.DataFrame, str], optional):
            The DataFrame or query to use for evaluation. If not provided, the
            evaluation data from training is used.
        perform_aggregation (bool, optional):
            A BOOL value that indicates the level of evaluation for forecasting
            accuracy. If you specify TRUE, then the forecasting accuracy is on
            the time series level. If you specify FALSE, the forecasting
            accuracy is on the timestamp level. The default value is TRUE.
        horizon (int, optional):
            An INT64 value that specifies the number of forecasted time points
            against which the evaluation metrics are computed. The default value
            is the horizon value specified in the CREATE MODEL statement for the
            time series model, or 1000 if unspecified. When evaluating multiple
            time series at the same time, this parameter applies to each time
            series.
        confidence_level (float, optional):
            A FLOAT64 value that specifies the percentage of the future values
            that fall in the prediction interval. The default value is 0.95. The
            valid input range is ``[0, 1)``.

    Returns:
        bigframes.pandas.DataFrame:
            The evaluation results.
    """
    import bigframes.pandas as bpd

    model_name, session = _get_model_name_and_session(model, input_)
    table_sql = _to_sql(input_) if input_ is not None else None

    sql = bigframes.core.sql.ml.evaluate(
        model_name=model_name,
        table=table_sql,
        perform_aggregation=perform_aggregation,
        horizon=horizon,
        confidence_level=confidence_level,
    )

    if session is None:
        return bpd.read_gbq_query(sql)
    else:
        return session.read_gbq_query(sql)


@log_adapter.method_logger(custom_base_name="bigquery_ml")
def predict(
    model: Union[bigframes.ml.base.BaseEstimator, str, pd.Series],
    input_: Union[pd.DataFrame, dataframe.DataFrame, str],
    *,
    threshold: Optional[float] = None,
    keep_original_columns: Optional[bool] = None,
    trial_id: Optional[int] = None,
) -> dataframe.DataFrame:
    """
    Runs prediction on a BigQuery ML model.

    See the `BigQuery ML PREDICT function syntax
    <https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict>`_
    for additional reference.

    Args:
        model (bigframes.ml.base.BaseEstimator or str):
            The model to use for prediction.
        input_ (Union[bigframes.pandas.DataFrame, str]):
            The DataFrame or query to use for prediction.
        threshold (float, optional):
            The threshold to use for classification models.
        keep_original_columns (bool, optional):
            Whether to keep the original columns in the output.
        trial_id (int, optional):
            An INT64 value that identifies the hyperparameter tuning trial that
            you want the function to evaluate. The function uses the optimal
            trial by default. Only specify this argument if you ran
            hyperparameter tuning when creating the model.

    Returns:
        bigframes.pandas.DataFrame:
            The prediction results.
    """
    import bigframes.pandas as bpd

    model_name, session = _get_model_name_and_session(model, input_)
    table_sql = _to_sql(input_)

    sql = bigframes.core.sql.ml.predict(
        model_name=model_name,
        table=table_sql,
        threshold=threshold,
        keep_original_columns=keep_original_columns,
        trial_id=trial_id,
    )

    if session is None:
        return bpd.read_gbq_query(sql)
    else:
        return session.read_gbq_query(sql)


@log_adapter.method_logger(custom_base_name="bigquery_ml")
def explain_predict(
    model: Union[bigframes.ml.base.BaseEstimator, str, pd.Series],
    input_: Union[pd.DataFrame, dataframe.DataFrame, str],
    *,
    top_k_features: Optional[int] = None,
    threshold: Optional[float] = None,
    integrated_gradients_num_steps: Optional[int] = None,
    approx_feature_contrib: Optional[bool] = None,
) -> dataframe.DataFrame:
    """
    Runs explainable prediction on a BigQuery ML model.

    See the `BigQuery ML EXPLAIN_PREDICT function syntax
    <https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict>`_
    for additional reference.

    Args:
        model (bigframes.ml.base.BaseEstimator or str):
            The model to use for prediction.
        input_ (Union[bigframes.pandas.DataFrame, str]):
            The DataFrame or query to use for prediction.
        top_k_features (int, optional):
            The number of top features to return.
        threshold (float, optional):
            The threshold for binary classification models.
        integrated_gradients_num_steps (int, optional):
            an INT64 value that specifies the number of steps to sample between
            the example being explained and its baseline. This value is used to
            approximate the integral in integrated gradients attribution
            methods. Increasing the value improves the precision of feature
            attributions, but can be slower and more computationally expensive.
        approx_feature_contrib (bool, optional):
            A BOOL value that indicates whether to use an approximate feature
            contribution method in the XGBoost model explanation.

    Returns:
        bigframes.pandas.DataFrame:
            The prediction results with explanations.
    """
    import bigframes.pandas as bpd

    model_name, session = _get_model_name_and_session(model, input_)
    table_sql = _to_sql(input_)

    sql = bigframes.core.sql.ml.explain_predict(
        model_name=model_name,
        table=table_sql,
        top_k_features=top_k_features,
        threshold=threshold,
        integrated_gradients_num_steps=integrated_gradients_num_steps,
        approx_feature_contrib=approx_feature_contrib,
    )

    if session is None:
        return bpd.read_gbq_query(sql)
    else:
        return session.read_gbq_query(sql)


@log_adapter.method_logger(custom_base_name="bigquery_ml")
def global_explain(
    model: Union[bigframes.ml.base.BaseEstimator, str, pd.Series],
    *,
    class_level_explain: Optional[bool] = None,
) -> dataframe.DataFrame:
    """
    Gets global explanations for a BigQuery ML model.

    See the `BigQuery ML GLOBAL_EXPLAIN function syntax
    <https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain>`_
    for additional reference.

    Args:
        model (bigframes.ml.base.BaseEstimator or str):
            The model to get explanations from.
        class_level_explain (bool, optional):
            Whether to return class-level explanations.

    Returns:
        bigframes.pandas.DataFrame:
            The global explanation results.
    """
    import bigframes.pandas as bpd

    model_name, session = _get_model_name_and_session(model)
    sql = bigframes.core.sql.ml.global_explain(
        model_name=model_name,
        class_level_explain=class_level_explain,
    )

    if session is None:
        return bpd.read_gbq_query(sql)
    else:
        return session.read_gbq_query(sql)
