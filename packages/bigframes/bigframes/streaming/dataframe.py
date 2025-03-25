# Copyright 2024 Google LLC
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

"""Module for bigquery continuous queries"""
from __future__ import annotations

import functools
import inspect
import json
from typing import Optional
import warnings

from google.cloud import bigquery

from bigframes import dataframe
from bigframes.core import log_adapter, nodes
import bigframes.exceptions as bfe
import bigframes.session


def _return_type_wrapper(method, cls):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        return_value = method(*args, **kwargs)
        if isinstance(return_value, dataframe.DataFrame):
            return cls._from_table_df(return_value)
        return return_value

    return wrapper


def _curate_df_doc(doc: Optional[str]):
    if not doc:
        return doc

    # Remove examples, some are not applicable to StreamingDataFrame
    doc = doc[: doc.find("**Examples:**")] + doc[doc.find("Args:") :]

    doc = doc.replace("dataframe.DataFrame", "streaming.StreamingDataFrame")
    doc = doc.replace(" DataFrame", " StreamingDataFrame")

    return doc


class StreamingBase:
    _appends_sql: str
    _session: bigframes.session.Session

    def to_bigtable(
        self,
        *,
        instance: str,
        table: str,
        service_account_email: Optional[str] = None,
        app_profile: Optional[str] = None,
        truncate: bool = False,
        overwrite: bool = False,
        auto_create_column_families: bool = False,
        bigtable_options: Optional[dict] = None,
        job_id: Optional[str] = None,
        job_id_prefix: Optional[str] = None,
    ) -> bigquery.QueryJob:
        """
        Export the StreamingDataFrame as a continue job and returns a
        QueryJob object for some management functionality.

        This method requires an existing bigtable preconfigured to
        accept the continuous query export statement. For instructions
        on export to bigtable, see
        https://cloud.google.com/bigquery/docs/export-to-bigtable.

        Args:
            instance (str):
                The name of the bigtable instance to export to.
            table (str):
                The name of the bigtable table to export to.
            service_account_email (str):
                Full name of the service account to run the continuous query.
                Example: accountname@projectname.gserviceaccounts.com
                If not provided, the user account will be used, but this
                limits the lifetime of the continuous query.
            app_profile (str, default None):
                The bigtable app profile to export to. If None, no app
                profile will be used.
            truncate (bool, default False):
                The export truncate option, see
                https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#bigtable_export_option
            overwrite (bool, default False):
                The export overwrite option, see
                https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#bigtable_export_option
            auto_create_column_families (bool, default False):
                The auto_create_column_families option, see
                https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#bigtable_export_option
            bigtable_options (dict, default None):
                The bigtable options dict, which will be converted to JSON
                using json.dumps, see
                https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#bigtable_export_option
                If None, no bigtable_options parameter will be passed.
            job_id (str, default None):
                If specified, replace the default job id for the query,
                see job_id parameter of
                https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query
            job_id_prefix (str, default None):
                If specified, a job id prefix for the query, see
                job_id_prefix parameter of
                https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query

        Returns:
            google.cloud.bigquery.QueryJob:
                See https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob
                The ongoing query job can be managed using this object.
                For example, the job can be cancelled or its error status
                can be examined.
        """
        return _to_bigtable(
            self._appends_sql,
            instance=instance,
            table=table,
            service_account_email=service_account_email,
            session=self._session,
            app_profile=app_profile,
            truncate=truncate,
            overwrite=overwrite,
            auto_create_column_families=auto_create_column_families,
            bigtable_options=bigtable_options,
            job_id=job_id,
            job_id_prefix=job_id_prefix,
        )

    def to_pubsub(
        self,
        *,
        topic: str,
        service_account_email: str,
        job_id: Optional[str] = None,
        job_id_prefix: Optional[str] = None,
    ) -> bigquery.QueryJob:
        """
        Export the StreamingDataFrame as a continue job and returns a
        QueryJob object for some management functionality.

        This method requires an existing pubsub topic. For instructions
        on creating a pubsub topic, see
        https://cloud.google.com/pubsub/docs/samples/pubsub-quickstart-create-topic?hl=en

        Note that a service account is a requirement for continuous queries
        exporting to pubsub.

        Args:
            topic (str):
                The name of the pubsub topic to export to.
                For example: "taxi-rides"
            service_account_email (str):
                Full name of the service account to run the continuous query.
                Example: accountname@projectname.gserviceaccounts.com
            job_id (str, default None):
                If specified, replace the default job id for the query,
                see job_id parameter of
                https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query
            job_id_prefix (str, default None):
                If specified, a job id prefix for the query, see
                job_id_prefix parameter of
                https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query

        Returns:
            google.cloud.bigquery.QueryJob:
                See https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob
                The ongoing query job can be managed using this object.
                For example, the job can be cancelled or its error status
                can be examined.
        """
        return _to_pubsub(
            self._appends_sql,
            topic=topic,
            service_account_email=service_account_email,
            session=self._session,
            job_id=job_id,
            job_id_prefix=job_id_prefix,
        )


@log_adapter.class_logger
class StreamingDataFrame(StreamingBase):
    __doc__ = (
        _curate_df_doc(dataframe.DataFrame.__doc__)
        + """
    .. note::

        The bigframes.streaming module is a preview feature, and subject to change.

    Currently only supports basic projection, filtering and preview operations.
    """
    )

    # Private constructor
    _create_key = object()

    def __init__(self, df: dataframe.DataFrame, *, create_key=0):
        if create_key is not StreamingDataFrame._create_key:
            raise ValueError(
                "StreamingDataFrame class shouldn't be created through constructor. Call bigframes.pandas.read_gbq_table_streaming method to create."
            )
        self._df = df
        self._df._disable_cache_override = True

    @classmethod
    def _from_table_df(cls, df: dataframe.DataFrame) -> StreamingDataFrame:
        return cls(df, create_key=cls._create_key)

    @property
    def _original_table(self):
        def traverse(node: nodes.BigFrameNode):
            if isinstance(node, nodes.ReadTableNode):
                return f"{node.source.table.project_id}.{node.source.table.dataset_id}.{node.source.table.table_id}"
            for child in node.child_nodes:
                original_table = traverse(child)
                if original_table:
                    return original_table
            return None

        return traverse(self._df._block._expr.node)

    def __getitem__(self, *args, **kwargs):
        return _return_type_wrapper(self._df.__getitem__, StreamingDataFrame)(
            *args, **kwargs
        )

    __getitem__.__doc__ = _curate_df_doc(
        inspect.getdoc(dataframe.DataFrame.__getitem__)
    )

    def __setitem__(self, *args, **kwargs):
        return _return_type_wrapper(self._df.__setitem__, StreamingDataFrame)(
            *args, **kwargs
        )

    __setitem__.__doc__ = _curate_df_doc(
        inspect.getdoc(dataframe.DataFrame.__setitem__)
    )

    def rename(self, *args, **kwargs):
        return _return_type_wrapper(self._df.rename, StreamingDataFrame)(
            *args, **kwargs
        )

    rename.__doc__ = _curate_df_doc(inspect.getdoc(dataframe.DataFrame.rename))

    def __repr__(self, *args, **kwargs):
        return _return_type_wrapper(self._df.__repr__, StreamingDataFrame)(
            *args, **kwargs
        )

    __repr__.__doc__ = _curate_df_doc(inspect.getdoc(dataframe.DataFrame.__repr__))

    def _repr_html_(self, *args, **kwargs):
        return _return_type_wrapper(self._df._repr_html_, StreamingDataFrame)(
            *args, **kwargs
        )

    _repr_html_.__doc__ = _curate_df_doc(
        inspect.getdoc(dataframe.DataFrame._repr_html_)
    )

    @property
    def sql(self):
        sql_str, _, _ = self._df._to_sql_query(include_index=False, enable_cache=False)
        return sql_str

    sql.__doc__ = _curate_df_doc(inspect.getdoc(dataframe.DataFrame.sql))

    # Patch for the required APPENDS clause
    @property
    def _appends_sql(self):
        sql_str = self.sql
        original_table = self._original_table
        assert original_table is not None

        # TODO(b/405691193): set start time back to NULL. Now set it slightly after 7 days max interval to avoid the bug.
        appends_clause = f"APPENDS(TABLE `{original_table}`, CURRENT_TIMESTAMP() - (INTERVAL 7 DAY - INTERVAL 5 MINUTE))"
        sql_str = sql_str.replace(f"`{original_table}`", appends_clause)
        return sql_str

    @property
    def _session(self):
        return self._df._session

    _session.__doc__ = _curate_df_doc(inspect.getdoc(dataframe.DataFrame._session))


def _to_bigtable(
    query: str,
    *,
    instance: str,
    table: str,
    service_account_email: Optional[str] = None,
    session: Optional[bigframes.session.Session] = None,
    app_profile: Optional[str] = None,
    truncate: bool = False,
    overwrite: bool = False,
    auto_create_column_families: bool = False,
    bigtable_options: Optional[dict] = None,
    job_id: Optional[str] = None,
    job_id_prefix: Optional[str] = None,
) -> bigquery.QueryJob:
    """Launches a BigQuery continuous query and returns a
    QueryJob object for some management functionality.

    This method requires an existing bigtable preconfigured to
    accept the continuous query export statement. For instructions
    on export to bigtable, see
    https://cloud.google.com/bigquery/docs/export-to-bigtable.

    Args:
        query (str):
            The sql statement to execute as a continuous function.
            For example: "SELECT * FROM dataset.table"
            This will be wrapped in an EXPORT DATA statement to
            launch a continuous query writing to bigtable.
        instance (str):
            The name of the bigtable instance to export to.
        table (str):
            The name of the bigtable table to export to.
        service_account_email (str):
            Full name of the service account to run the continuous query.
            Example: accountname@projectname.gserviceaccounts.com
            If not provided, the user account will be used, but this
            limits the lifetime of the continuous query.
        session (bigframes.session.Session, default None):
            The session object to use for the query. This determines
            the project id and location of the query. If None, will
            default to the bigframes global session.
        app_profile (str, default None):
            The bigtable app profile to export to. If None, no app
            profile will be used.
        truncate (bool, default False):
            The export truncate option, see
            https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#bigtable_export_option
        overwrite (bool, default False):
            The export overwrite option, see
            https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#bigtable_export_option
        auto_create_column_families (bool, default False):
            The auto_create_column_families option, see
            https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#bigtable_export_option
        bigtable_options (dict, default None):
            The bigtable options dict, which will be converted to JSON
            using json.dumps, see
            https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#bigtable_export_option
            If None, no bigtable_options parameter will be passed.
        job_id (str, default None):
            If specified, replace the default job id for the query,
            see job_id parameter of
            https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query
        job_id_prefix (str, default None):
            If specified, a job id prefix for the query, see
            job_id_prefix parameter of
            https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query

    Returns:
        google.cloud.bigquery.QueryJob:
            See https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob
            The ongoing query job can be managed using this object.
            For example, the job can be cancelled or its error status
            can be examined.
    """
    msg = bfe.format_message(
        "The bigframes.streaming module is a preview feature, and subject to change."
    )
    warnings.warn(msg, stacklevel=1, category=bfe.PreviewWarning)

    # get default client if not passed
    if session is None:
        session = bigframes.get_global_session()
    bq_client = session.bqclient

    # build export string from parameters
    project = bq_client.project

    app_profile_url_string = ""
    if app_profile is not None:
        app_profile_url_string = f"appProfiles/{app_profile}/"

    bigtable_options_parameter_string = ""
    if bigtable_options is not None:
        bigtable_options_parameter_string = (
            'bigtable_options = """' + json.dumps(bigtable_options) + '""",\n'
        )

    sql = (
        "EXPORT DATA\n"
        "OPTIONS (\n"
        "format = 'CLOUD_BIGTABLE',\n"
        f"{bigtable_options_parameter_string}"
        f"truncate = {str(truncate)},\n"
        f"overwrite = {str(overwrite)},\n"
        f"auto_create_column_families = {str(auto_create_column_families)},\n"
        f'uri = "https://bigtable.googleapis.com/projects/{project}/instances/{instance}/{app_profile_url_string}tables/{table}"\n'
        ")\n"
        "AS (\n"
        f"{query});"
    )

    # override continuous http parameter
    job_config = bigquery.job.QueryJobConfig()

    job_config_dict: dict = {"query": {"continuous": True}}
    if service_account_email is not None:
        job_config_dict["query"]["connectionProperties"] = {
            "key": "service_account",
            "value": service_account_email,
        }
    job_config_filled = job_config.from_api_repr(job_config_dict)
    job_config_filled.labels = {"bigframes-api": "streaming_to_bigtable"}

    # begin the query job
    query_job = bq_client.query(
        sql,
        job_config=job_config_filled,  # type:ignore
        # typing error above is in bq client library
        # (should accept abstract job_config, only takes concrete)
        job_id=job_id,
        job_id_prefix=job_id_prefix,
    )

    # return the query job to the user for lifetime management
    return query_job


def _to_pubsub(
    query: str,
    *,
    topic: str,
    service_account_email: str,
    session: Optional[bigframes.session.Session] = None,
    job_id: Optional[str] = None,
    job_id_prefix: Optional[str] = None,
) -> bigquery.QueryJob:
    """Launches a BigQuery continuous query and returns a
    QueryJob object for some management functionality.

    This method requires an existing pubsub topic. For instructions
    on creating a pubsub topic, see
    https://cloud.google.com/pubsub/docs/samples/pubsub-quickstart-create-topic?hl=en

    Note that a service account is a requirement for continuous queries
    exporting to pubsub.

    Args:
        query (str):
            The sql statement to execute as a continuous function.
            For example: "SELECT * FROM dataset.table"
            This will be wrapped in an EXPORT DATA statement to
            launch a continuous query writing to pubsub.
        topic (str):
            The name of the pubsub topic to export to.
            For example: "taxi-rides"
        service_account_email (str):
            Full name of the service account to run the continuous query.
            Example: accountname@projectname.gserviceaccounts.com
        session (bigframes.session.Session, default None):
            The session object to use for the query. This determines
            the project id and location of the query. If None, will
            default to the bigframes global session.
        job_id (str, default None):
            If specified, replace the default job id for the query,
            see job_id parameter of
            https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query
        job_id_prefix (str, default None):
            If specified, a job id prefix for the query, see
            job_id_prefix parameter of
            https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query

    Returns:
        google.cloud.bigquery.QueryJob:
            See https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob
            The ongoing query job can be managed using this object.
            For example, the job can be cancelled or its error status
            can be examined.
    """
    msg = bfe.format_message(
        "The bigframes.streaming module is a preview feature, and subject to change."
    )
    warnings.warn(msg, stacklevel=1, category=bfe.PreviewWarning)

    # get default client if not passed
    if session is None:
        session = bigframes.get_global_session()
    bq_client = session.bqclient

    # build export string from parameters
    sql = (
        "EXPORT DATA\n"
        "OPTIONS (\n"
        "format = 'CLOUD_PUBSUB',\n"
        f'uri = "https://pubsub.googleapis.com/projects/{bq_client.project}/topics/{topic}"\n'
        ")\n"
        "AS (\n"
        f"{query});"
    )

    # override continuous http parameter
    job_config = bigquery.job.QueryJobConfig()
    job_config_filled = job_config.from_api_repr(
        {
            "query": {
                "continuous": True,
                "connectionProperties": {
                    "key": "service_account",
                    "value": service_account_email,
                },
            }
        }
    )
    job_config_filled.labels = {"bigframes-api": "streaming_to_pubsub"}

    # begin the query job
    query_job = bq_client.query(
        sql,
        job_config=job_config_filled,  # type:ignore
        # typing error above is in bq client library
        # (should accept abstract job_config, only takes concrete)
        job_id=job_id,
        job_id_prefix=job_id_prefix,
    )

    # return the query job to the user for lifetime management
    return query_job
