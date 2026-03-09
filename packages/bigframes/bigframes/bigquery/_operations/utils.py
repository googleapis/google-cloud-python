# Copyright 2026 Google LLC
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

from typing import cast, Optional, Union

import pandas as pd

import bigframes
from bigframes import dataframe
from bigframes.ml import base as ml_base


def get_model_name_and_session(
    model: Union[ml_base.BaseEstimator, str, pd.Series],
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


def to_sql(df_or_sql: Union[pd.DataFrame, dataframe.DataFrame, str]) -> str:
    """
    Helper to convert DataFrame to SQL string
    """
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
