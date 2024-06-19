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

import json
from typing import Optional

from google.cloud import bigquery

import bigframes


def to_bigtable(
    query: str,
    instance: str,
    table: str,
    bq_client: Optional[bigquery.Client] = None,
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
        bq_client (str, default None):
            The Client object to use for the query. This determines
            the project id and location of the query. If None, will
            default to the bigframes global session default client.
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
    # get default client if not passed
    if bq_client is None:
        bq_client = bigframes.get_global_session().bqclient

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
    job_config_filled = job_config.from_api_repr({"query": {"continuous": True}})

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
