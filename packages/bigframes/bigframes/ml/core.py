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

import datetime
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
        self._model_manipulation_sql_generator = ml_sql.ModelManipulationSqlGenerator(
            self.model_name
        )

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

    def _apply_sql(
        self,
        input_data: bpd.DataFrame,
        func: Callable[[bpd.DataFrame], str],
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
        _, index_col_ids, index_labels = input_data._to_sql_query(include_index=True)

        sql = func(input_data)
        df = self._session.read_gbq(sql, index_col=index_col_ids)
        df.index.names = index_labels

        return df

    def predict(self, input_data: bpd.DataFrame) -> bpd.DataFrame:
        # TODO: validate input data schema
        return self._apply_sql(
            input_data,
            self._model_manipulation_sql_generator.ml_predict,
        )

    def transform(self, input_data: bpd.DataFrame) -> bpd.DataFrame:
        # TODO: validate input data schema
        return self._apply_sql(
            input_data,
            self._model_manipulation_sql_generator.ml_transform,
        )

    def generate_text(
        self,
        input_data: bpd.DataFrame,
        options: Mapping[str, int | float],
    ) -> bpd.DataFrame:
        # TODO: validate input data schema
        return self._apply_sql(
            input_data,
            lambda source_df: self._model_manipulation_sql_generator.ml_generate_text(
                source_df=source_df,
                struct_options=options,
            ),
        )

    def generate_text_embedding(
        self,
        input_data: bpd.DataFrame,
        options: Mapping[str, int | float],
    ) -> bpd.DataFrame:
        # TODO: validate input data schema
        return self._apply_sql(
            input_data,
            lambda source_df: self._model_manipulation_sql_generator.ml_generate_text_embedding(
                source_df=source_df,
                struct_options=options,
            ),
        )

    def forecast(self) -> bpd.DataFrame:
        sql = self._model_manipulation_sql_generator.ml_forecast()
        return self._session.read_gbq(sql, index_col="forecast_timestamp").reset_index()

    def evaluate(self, input_data: Optional[bpd.DataFrame] = None):
        # TODO: validate input data schema
        sql = self._model_manipulation_sql_generator.ml_evaluate(input_data)

        return self._session.read_gbq(sql)

    def centroids(self) -> bpd.DataFrame:
        assert self._model.model_type == "KMEANS"

        sql = self._model_manipulation_sql_generator.ml_centroids()

        return self._session.read_gbq(
            sql, index_col=["centroid_id", "feature"]
        ).reset_index()

    def principal_components(self) -> bpd.DataFrame:
        assert self._model.model_type == "PCA"

        sql = self._model_manipulation_sql_generator.ml_principal_components()

        return self._session.read_gbq(
            sql, index_col=["principal_component_id", "feature"]
        ).reset_index()

    def principal_component_info(self) -> bpd.DataFrame:
        assert self._model.model_type == "PCA"

        sql = self._model_manipulation_sql_generator.ml_principal_component_info()

        return self._session.read_gbq(sql)

    def copy(self, new_model_name: str, replace: bool = False) -> BqmlModel:
        job_config = bigquery.job.CopyJobConfig()
        if replace:
            job_config.write_disposition = "WRITE_TRUNCATE"

        copy_job = self._session.bqclient.copy_table(
            self.model_name, new_model_name, job_config=job_config
        )
        self._session._start_generic_job(copy_job)

        new_model = self._session.bqclient.get_model(new_model_name)
        return BqmlModel(self._session, new_model)

    def register(self, vertex_ai_model_id: Optional[str] = None) -> BqmlModel:
        if vertex_ai_model_id is None:
            # vertex id needs to start with letters. https://cloud.google.com/vertex-ai/docs/general/resource-naming
            vertex_ai_model_id = "bigframes_" + cast(str, self._model.model_id)

        # truncate as Vertex ID only accepts 63 characters, easily exceeding the limit for temp models.
        # The possibility of conflicts should be low.
        vertex_ai_model_id = vertex_ai_model_id[:63]
        sql = self._model_manipulation_sql_generator.alter_model(
            options={"vertex_ai_model_id": vertex_ai_model_id}
        )
        # Register the model and wait it to finish
        self._session._start_query(sql)

        self._model = self._session.bqclient.get_model(self.model_name)
        return self


class BqmlModelFactory:
    def __init__(self):
        self._model_creation_sql_generator = ml_sql.ModelCreationSqlGenerator()

    def _create_model_ref(
        self, dataset: bigquery.DatasetReference
    ) -> bigquery.ModelReference:
        return bigquery.ModelReference.from_string(
            f"{dataset.project}.{dataset.dataset_id}.{uuid.uuid4().hex}"
        )

    def _create_model_with_sql(self, session: bigframes.Session, sql: str) -> BqmlModel:
        # fit the model, synchronously
        _, job = session._start_query(sql)

        # real model path in the session specific hidden dataset and table prefix
        model_name_full = f"{job.destination.project}.{job.destination.dataset_id}.{job.destination.table_id}"
        model = bigquery.Model(model_name_full)
        model.expires = (
            datetime.datetime.now(datetime.timezone.utc) + constants.DEFAULT_EXPIRATION
        )
        model = session.bqclient.update_model(model, ["expires"])

        return BqmlModel(session, model)

    def create_model(
        self,
        X_train: bpd.DataFrame,
        y_train: Optional[bpd.DataFrame] = None,
        transforms: Optional[Iterable[str]] = None,
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> BqmlModel:
        """Create a session-temporary BQML model with the CREATE OR REPLACE MODEL statement

        Args:
            X_train: features columns for training
            y_train: labels columns for training, if applicable
            transforms: an optional list of SQL expressions that implement preprocessing
                on top of the input data. Generates a BQML TRANSFORM clause
            options: a dict of options to configure the model. Generates a BQML OPTIONS
                clause

        Returns: a BqmlModel, wrapping a trained model in BigQuery
        """
        options = dict(options)
        # Cache dataframes to make sure base table is not a snapshot
        # cached dataframe creates a full copy, never uses snapshot
        if y_train is None:
            input_data = X_train._cached()
        else:
            input_data = X_train._cached().join(y_train._cached(), how="outer")
            options.update({"INPUT_LABEL_COLS": y_train.columns.tolist()})

        session = X_train._session
        model_ref = self._create_model_ref(session._anonymous_dataset)

        sql = self._model_creation_sql_generator.create_model(
            source_df=input_data,
            model_ref=model_ref,
            transforms=transforms,
            options=options,
        )

        return self._create_model_with_sql(session=session, sql=sql)

    def create_time_series_model(
        self,
        X_train: bpd.DataFrame,
        y_train: bpd.DataFrame,
        transforms: Optional[Iterable[str]] = None,
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> BqmlModel:
        assert (
            X_train.columns.size == 1
        ), "Time series timestamp input must only contain 1 column."
        assert (
            y_train.columns.size == 1
        ), "Time stamp data input must only contain 1 column."

        options = dict(options)
        # Cache dataframes to make sure base table is not a snapshot
        # cached dataframe creates a full copy, never uses snapshot
        input_data = X_train._cached().join(y_train._cached(), how="outer")
        options.update({"TIME_SERIES_TIMESTAMP_COL": X_train.columns.tolist()[0]})
        options.update({"TIME_SERIES_DATA_COL": y_train.columns.tolist()[0]})

        session = X_train._session
        model_ref = self._create_model_ref(session._anonymous_dataset)

        sql = self._model_creation_sql_generator.create_model(
            source_df=input_data,
            model_ref=model_ref,
            transforms=transforms,
            options=options,
        )

        return self._create_model_with_sql(session=session, sql=sql)

    def create_remote_model(
        self,
        session: bigframes.Session,
        connection_name: str,
        input: Mapping[str, str] = {},
        output: Mapping[str, str] = {},
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> BqmlModel:
        """Create a session-temporary BQML remote model with the CREATE OR REPLACE MODEL statement

        Args:
            connection_name:
                a BQ connection to talk with Vertex AI, of the format <PROJECT_NUMBER>.<REGION>.<CONNECTION_NAME>. https://cloud.google.com/bigquery/docs/create-cloud-resource-connection
            input:
                input schema for general remote models
            output:
                output schema for general remote models
            options:
                a dict of options to configure the model. Generates a BQML OPTIONS clause

        Returns:
            BqmlModel: a BqmlModel wrapping a trained model in BigQuery
        """
        model_ref = self._create_model_ref(session._anonymous_dataset)
        sql = self._model_creation_sql_generator.create_remote_model(
            connection_name=connection_name,
            model_ref=model_ref,
            input=input,
            output=output,
            options=options,
        )

        return self._create_model_with_sql(session=session, sql=sql)

    def create_imported_model(
        self,
        session: bigframes.Session,
        options: Mapping[str, Union[str, int, float, Iterable[str]]] = {},
    ) -> BqmlModel:
        """Create a session-temporary BQML imported model with the CREATE OR REPLACE MODEL statement

        Args:
            options: a dict of options to configure the model. Generates a BQML OPTIONS
                clause

        Returns: a BqmlModel, wrapping a trained model in BigQuery
        """
        model_ref = self._create_model_ref(session._anonymous_dataset)
        sql = self._model_creation_sql_generator.create_imported_model(
            model_ref=model_ref,
            options=options,
        )

        return self._create_model_with_sql(session=session, sql=sql)
