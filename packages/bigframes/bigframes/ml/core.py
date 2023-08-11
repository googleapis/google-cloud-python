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

"""Core operations for BQML based models"""

from __future__ import annotations

from typing import Callable, cast, Iterable, Mapping, Optional, Union
import uuid

from google.cloud import bigquery

import bigframes
import bigframes.constants as constants
from bigframes.ml import sql as ml_sql
import bigframes.pandas as bpd


class BqmlModel:
    """Represents an existing BQML model in BigQuery.

    Wraps the BQML API and SQL interface to expose the functionality needed for
    BigQuery DataFrames ML.
    """

    def __init__(self, session: bigframes.Session, model: bigquery.Model):
        self._session = session
        self._model = model

    @property
    def session(self) -> bigframes.Session:
        """Get the BigQuery DataFrames session that this BQML model wrapper is tied to"""
        return self._session

    @property
    def model_name(self) -> str:
        """Get the fully qualified name of the model, i.e. project_id.dataset_id.model_id"""
        return f"{self._model.project}.{self._model.dataset_id}.{self._model.model_id}"

    @property
    def model(self) -> bigquery.Model:
        """Get the BQML model associated with this wrapper"""
        return self._model

    @classmethod
    def _apply_sql(
        cls,
        session: bigframes.Session,
        input_data: bpd.DataFrame,
        func: Callable[[str], str],
    ) -> bpd.DataFrame:
        """Helper to wrap a dataframe in a SQL query, keeping the index intact.

        Args:
            session (bigframes.Session):
                the active bigframes.Session

            input_data (bigframes.dataframe.DataFrame):
                the dataframe to be wrapped

            func (function):
                a function that will accept a SQL string and produce a new SQL
                string from which to construct the output dataframe. It must
                include the index columns of the input SQL.
        """
        source_sql, tagged_index_cols = input_data._to_sql_query(
            always_include_index=True
        )

        if len(tagged_index_cols) != 1:
            raise NotImplementedError(
                f"Only exactly one index column is supported. {constants.FEEDBACK_LINK}"
            )

        index_col_name, is_named_index = tagged_index_cols[0]
        sql = func(source_sql)
        df = session.read_gbq(sql, index_col=[index_col_name])
        if not is_named_index:
            df.index.name = None

        return df

    def predict(self, input_data: bpd.DataFrame) -> bpd.DataFrame:
        # TODO: validate input data schema
        return self._apply_sql(
            self._session,
            input_data,
            lambda source_sql: ml_sql.ml_predict(
                model_name=self.model_name, source_sql=source_sql
            ),
        )

    def transform(self, input_data: bpd.DataFrame) -> bpd.DataFrame:
        # TODO: validate input data schema
        return self._apply_sql(
            self._session,
            input_data,
            lambda source_sql: ml_sql.ml_transform(
                model_name=self.model_name, source_sql=source_sql
            ),
        )

    def generate_text(
        self,
        input_data: bpd.DataFrame,
        options: Mapping[str, int | float],
    ) -> bpd.DataFrame:
        # TODO: validate input data schema
        return self._apply_sql(
            self._session,
            input_data,
            lambda source_sql: ml_sql.ml_generate_text(
                model_name=self.model_name,
                source_sql=source_sql,
                struct_options=ml_sql.struct_options(**options),
            ),
        )

    def generate_text_embedding(
        self,
        input_data: bpd.DataFrame,
        options: Mapping[str, int | float],
    ) -> bpd.DataFrame:
        # TODO: validate input data schema
        return self._apply_sql(
            self._session,
            input_data,
            lambda source_sql: ml_sql.ml_generate_text_embedding(
                model_name=self.model_name,
                source_sql=source_sql,
                struct_options=ml_sql.struct_options(**options),
            ),
        )

    def forecast(self) -> bpd.DataFrame:
        sql = ml_sql.ml_forecast(self.model_name)
        return self._session.read_gbq(sql)

    def evaluate(self, input_data: Optional[bpd.DataFrame] = None):
        # TODO: validate input data schema
        # Note: don't need index as evaluate returns a new table
        source_sql, _ = (
            input_data._to_sql_query(always_include_index=False)
            if (input_data is not None)
            else (None, None)
        )
        sql = ml_sql.ml_evaluate(self.model_name, source_sql)

        return self._session.read_gbq(sql)

    def copy(self, new_model_name: str, replace: bool = False) -> BqmlModel:
        job_config = bigquery.job.CopyJobConfig()
        if replace:
            job_config.write_disposition = "WRITE_TRUNCATE"

        self._session.bqclient.copy_table(
            self.model_name, new_model_name, job_config=job_config
        ).result()

        new_model = self._session.bqclient.get_model(new_model_name)
        return BqmlModel(self._session, new_model)

    def register(self, vertex_ai_model_id: Optional[str] = None) -> BqmlModel:
        if vertex_ai_model_id is None:
            # vertex id needs to start with letters. https://cloud.google.com/vertex-ai/docs/general/resource-naming
            vertex_ai_model_id = "bigframes_" + cast(str, self._model.model_id)

        # truncate as Vertex ID only accepts 63 characters, easily exceeding the limit for temp models.
        # The possibility of conflicts should be low.
        vertex_ai_model_id = vertex_ai_model_id[:63]
        options_sql = ml_sql.options(**{"vertex_ai_model_id": vertex_ai_model_id})
        sql = ml_sql.alter_model(self.model_name, options_sql=options_sql)
        # Register the model and wait it to finish
        self._session.bqclient.query(sql).result()

        self._model = self._session.bqclient.get_model(self.model_name)
        return self


def create_bqml_model(
    train_X: bpd.DataFrame,
    train_y: Optional[bpd.DataFrame] = None,
    transforms: Optional[Iterable[str]] = None,
    options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
) -> BqmlModel:
    """Create a session-temporary BQML model with the CREATE MODEL statement

    Args:
        train_X: features columns for training
        train_y: labels columns for training, if applicable
        transforms: an optional list of SQL expressions that implement preprocessing
            on top of the input data. Generates a BQML TRANSFORM clause
        options: a dict of options to configure the model. Generates a BQML OPTIONS
            clause

    Returns: a BqmlModel, wrapping a trained model in BigQuery
    """
    options = dict(options)
    if train_y is None:
        input_data = train_X
    else:
        # TODO: handle case where train_y columns are renamed in the join
        input_data = train_X.join(train_y, how="outer")
        options.update({"INPUT_LABEL_COLS": train_y.columns.tolist()})

    # pickpocket session object from the dataframe
    session = train_X._get_block().expr._session

    # TODO(garrettwu): add wrapper to select the feature columns
    # for now, drop index to avoid including the index in feature columns
    input_data = input_data.reset_index(drop=True)

    source_sql = input_data.sql
    options_sql = ml_sql.options(**options)
    transform_sql = ml_sql.transform(*transforms) if transforms is not None else None
    sql = ml_sql.create_model(
        model_name=_create_temp_model_name(),
        source_sql=source_sql,
        transform_sql=transform_sql,
        options_sql=options_sql,
    )

    return _create_bqml_model_with_sql(session=session, sql=sql)


def create_bqml_time_series_model(
    train_X: bpd.DataFrame,
    train_y: bpd.DataFrame,
    transforms: Optional[Iterable[str]] = None,
    options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
) -> BqmlModel:

    assert (
        train_X.columns.size == 1
    ), "Time series timestamp input must only contain 1 column."
    assert (
        train_y.columns.size == 1
    ), "Time stamp data input must only contain 1 column."

    options = dict(options)
    input_data = train_X.join(train_y, how="outer")
    options.update({"TIME_SERIES_TIMESTAMP_COL": train_X.columns.tolist()[0]})
    options.update({"TIME_SERIES_DATA_COL": train_y.columns.tolist()[0]})
    # pickpocket session object from the dataframe
    session = train_X._get_block().expr._session

    source_sql = input_data.sql
    options_sql = ml_sql.options(**options)

    transform_sql = ml_sql.transform(*transforms) if transforms is not None else None
    sql = ml_sql.create_model(
        model_name=_create_temp_model_name(),
        source_sql=source_sql,
        transform_sql=transform_sql,
        options_sql=options_sql,
    )

    return _create_bqml_model_with_sql(session=session, sql=sql)


def create_bqml_remote_model(
    session: bigframes.Session,
    connection_name: str,
    options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
) -> BqmlModel:
    """Create a session-temporary BQML remote model with the CREATE MODEL statement

    Args:
        connection_name:
            a BQ connection to talk with Vertex AI, of the format <PROJECT_NUMBER>.<REGION>.<CONNECTION_NAME>. https://cloud.google.com/bigquery/docs/create-cloud-resource-connection
        options:
            a dict of options to configure the model. Generates a BQML OPTIONS clause

    Returns:
        BqmlModel: a BqmlModel wrapping a trained model in BigQuery
    """
    options_sql = ml_sql.options(**options)
    sql = ml_sql.create_remote_model(
        model_name=_create_temp_model_name(),
        connection_name=connection_name,
        options_sql=options_sql,
    )

    return _create_bqml_model_with_sql(session=session, sql=sql)


def create_bqml_imported_model(
    session: bigframes.Session,
    options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
) -> BqmlModel:
    """Create a session-temporary BQML imported model with the CREATE MODEL statement

    Args:
        options: a dict of options to configure the model. Generates a BQML OPTIONS
            clause

    Returns: a BqmlModel, wrapping a trained model in BigQuery
    """
    options_sql = ml_sql.options(**options)
    sql = ml_sql.create_imported_model(
        model_name=_create_temp_model_name(),
        options_sql=options_sql,
    )

    return _create_bqml_model_with_sql(session=session, sql=sql)


def _create_temp_model_name() -> str:
    return uuid.uuid4().hex


def _create_bqml_model_with_sql(session: bigframes.Session, sql: str) -> BqmlModel:
    # fit the model, synchronously
    job = session.bqclient.query(sql)
    job.result()

    # real model path in the session specific hidden dataset and table prefix
    model_name_full = f"{job.destination.dataset_id}.{job.destination.table_id}"
    model = session.bqclient.get_model(model_name_full)
    return BqmlModel(session, model)
