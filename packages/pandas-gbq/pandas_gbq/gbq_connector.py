# Copyright (c) 2025 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


import logging
import time
import typing
from typing import Any, Dict, Optional, Sequence, Union
import warnings

import numpy as np

# Only import at module-level at type checking time to avoid circular
# dependencies in the pandas package, which has an optional dependency on
# pandas-gbq.
if typing.TYPE_CHECKING:  # pragma: NO COVER
    import pandas

import pandas_gbq.constants
from pandas_gbq.contexts import context
import pandas_gbq.environment as environment
import pandas_gbq.exceptions
from pandas_gbq.exceptions import (
    GenericGBQException,
    InvalidSchema,
    QueryTimeout,
    TableCreationError,
)
from pandas_gbq.features import FEATURES
import pandas_gbq.query
import pandas_gbq.timestamp

try:
    import tqdm  # noqa
except ImportError:
    tqdm = None

logger = logging.getLogger(__name__)


class GbqConnector:
    def __init__(
        self,
        project_id,
        reauth=False,
        private_key=None,
        auth_local_webserver=True,
        dialect="standard",
        location=None,
        credentials=None,
        use_bqstorage_api=False,
        auth_redirect_uri=None,
        client_id=None,
        client_secret=None,
        user_agent=None,
        rfc9110_delimiter=False,
        bigquery_client=None,
    ):
        from google.api_core.exceptions import ClientError, GoogleAPIError

        from pandas_gbq import auth

        self.http_error = (ClientError, GoogleAPIError)
        self.project_id = project_id
        self.location = location
        self.reauth = reauth
        self.private_key = private_key
        self.auth_local_webserver = auth_local_webserver
        self.dialect = dialect
        self.credentials = credentials
        self.auth_redirect_uri = auth_redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.rfc9110_delimiter = rfc9110_delimiter
        self.use_bqstorage_api = use_bqstorage_api

        if bigquery_client is not None:
            # If a bq client is already provided, use it to populate auth fields.
            self.project_id = bigquery_client.project
            self.credentials = bigquery_client._credentials
            self.client = bigquery_client
            return

        default_project = None

        # Service account credentials have a project associated with them.
        # Prefer that project if none was supplied.
        if self.project_id is None and hasattr(self.credentials, "project_id"):
            self.project_id = credentials.project_id

        # Load credentials from cache.
        if not self.credentials:
            self.credentials = context.credentials
            default_project = context.project

        # Credentials were explicitly asked for, so don't use the cache.
        if private_key or reauth or not self.credentials:
            self.credentials, default_project = auth.get_credentials(
                private_key=private_key,
                project_id=project_id,
                reauth=reauth,
                auth_local_webserver=auth_local_webserver,
                auth_redirect_uri=auth_redirect_uri,
                client_id=client_id,
                client_secret=client_secret,
            )

        if self.project_id is None:
            self.project_id = default_project

        if self.project_id is None:
            raise ValueError("Could not determine project ID and one was not supplied.")

        # Cache the credentials if they haven't been set yet.
        if context.credentials is None:
            context.credentials = self.credentials
        if context.project is None:
            context.project = self.project_id

        self.client = _get_client(
            self.user_agent, self.rfc9110_delimiter, self.project_id, self.credentials
        )

    def _start_timer(self):
        self.start = time.time()

    def get_elapsed_seconds(self):
        return round(time.time() - self.start, 2)

    def log_elapsed_seconds(self, prefix="Elapsed", postfix="s.", overlong=6):
        sec = self.get_elapsed_seconds()
        if sec > overlong:
            logger.info("{} {} {}".format(prefix, sec, postfix))

    def get_client(self):
        import google.api_core.client_info

        bigquery = FEATURES.bigquery_try_import()

        user_agent = create_user_agent(
            user_agent=self.user_agent, rfc9110_delimiter=self.rfc9110_delimiter
        )

        client_info = google.api_core.client_info.ClientInfo(
            user_agent=user_agent,
        )
        return bigquery.Client(
            project=self.project_id,
            credentials=self.credentials,
            client_info=client_info,
        )

    @staticmethod
    def process_http_error(ex):
        # See `BigQuery Troubleshooting Errors
        # <https://cloud.google.com/bigquery/troubleshooting-errors>`__

        message = (
            ex.message.casefold()
            if hasattr(ex, "message") and ex.message is not None
            else ""
        )
        if "cancelled" in message:
            raise QueryTimeout("Reason: {0}".format(ex))
        elif "schema does not match" in message:
            error_message = ex.errors[0]["message"]
            raise InvalidSchema(f"Reason: {error_message}")
        elif "already exists: table" in message:
            error_message = ex.errors[0]["message"]
            raise TableCreationError(f"Reason: {error_message}")
        else:
            raise GenericGBQException("Reason: {0}".format(ex)) from ex

    def download_table(
        self,
        table_id: str,
        max_results: Optional[int] = None,
        progress_bar_type: Optional[str] = None,
        dtypes: Optional[Dict[str, Union[str, Any]]] = None,
    ) -> "pandas.DataFrame":
        from google.cloud import bigquery

        self._start_timer()

        try:
            table_ref = bigquery.TableReference.from_string(
                table_id, default_project=self.project_id
            )
            rows_iter = self.client.list_rows(table_ref, max_results=max_results)
        except self.http_error as ex:
            self.process_http_error(ex)

        return self._download_results(
            rows_iter,
            max_results=max_results,
            progress_bar_type=progress_bar_type,
            user_dtypes=dtypes,
        )

    def run_query(self, query, max_results=None, progress_bar_type=None, **kwargs):
        from google.cloud import bigquery

        job_config_dict = {
            "query": {
                "useLegacySql": self.dialect
                == "legacy"
                # 'allowLargeResults', 'createDisposition',
                # 'preserveNulls', destinationTable, useQueryCache
            }
        }
        config = kwargs.get("configuration")
        if config is not None:
            job_config_dict.update(config)

        timeout_ms = job_config_dict.get("jobTimeoutMs") or job_config_dict[
            "query"
        ].get("timeoutMs")

        if timeout_ms:
            timeout_ms = int(timeout_ms)
            # Having too small a timeout_ms results in individual
            # API calls timing out before they can finish.
            # ~300 milliseconds is rule of thumb for bare minimum
            # latency from the BigQuery API, however, 400 milliseconds
            # produced too many issues with flakybot failures.
            minimum_latency = 500
            if timeout_ms < minimum_latency:
                raise QueryTimeout(
                    f"Query timeout must be at least 500 milliseconds: timeout_ms equals {timeout_ms}."
                )
        else:
            timeout_ms = None

        self._start_timer()
        job_config = bigquery.QueryJobConfig.from_api_repr(job_config_dict)

        if FEATURES.bigquery_has_query_and_wait:
            rows_iter = pandas_gbq.query.query_and_wait_via_client_library(
                self,
                self.client,
                query,
                location=self.location,
                project_id=self.project_id,
                job_config=job_config,
                max_results=max_results,
                timeout_ms=timeout_ms,
            )
        else:
            rows_iter = pandas_gbq.query.query_and_wait(
                self,
                self.client,
                query,
                location=self.location,
                project_id=self.project_id,
                job_config=job_config,
                max_results=max_results,
                timeout_ms=timeout_ms,
            )

        dtypes = kwargs.get("dtypes")
        return self._download_results(
            rows_iter,
            max_results=max_results,
            progress_bar_type=progress_bar_type,
            user_dtypes=dtypes,
        )

    def _download_results(
        self,
        rows_iter,
        max_results=None,
        progress_bar_type=None,
        user_dtypes=None,
    ):
        # No results are desired, so don't bother downloading anything.
        if max_results == 0:
            return None

        if user_dtypes is None:
            user_dtypes = {}

        create_bqstorage_client = self.use_bqstorage_api
        if max_results is not None:
            create_bqstorage_client = False

        # If we're downloading a large table, BigQuery DataFrames might be a
        # better fit. Not all code paths will populate rows_iter._table, but
        # if it's not populated that means we are working with a small result
        # set.
        if (table_ref := getattr(rows_iter, "_table", None)) is not None:
            table = self.client.get_table(table_ref)
            if (
                isinstance((num_bytes := table.num_bytes), int)
                and num_bytes > pandas_gbq.constants.BYTES_TO_RECOMMEND_BIGFRAMES
            ):
                num_gib = num_bytes / pandas_gbq.constants.BYTES_IN_GIB
                warnings.warn(
                    f"Recommendation: Your results are {num_gib:.1f} GiB. "
                    "Consider using BigQuery DataFrames (https://bit.ly/bigframes-intro)"
                    "to process large results with pandas compatible APIs with transparent SQL "
                    "pushdown to BigQuery engine. This provides an opportunity to save on costs "
                    "and improve performance. "
                    "Please reach out to bigframes-feedback@google.com with any "
                    "questions or concerns. To disable this message, run "
                    "warnings.simplefilter('ignore', category=pandas_gbq.exceptions.LargeResultsWarning)",
                    category=pandas_gbq.exceptions.LargeResultsWarning,
                    # user's code
                    # -> read_gbq
                    # -> run_query
                    # -> download_results
                    stacklevel=4,
                )

        try:
            schema_fields = [field.to_api_repr() for field in rows_iter.schema]
            conversion_dtypes = _bqschema_to_nullsafe_dtypes(schema_fields)
            conversion_dtypes.update(user_dtypes)
            df = rows_iter.to_dataframe(
                dtypes=conversion_dtypes,
                progress_bar_type=progress_bar_type,
                create_bqstorage_client=create_bqstorage_client,
            )
        except self.http_error as ex:
            self.process_http_error(ex)

        df = _finalize_dtypes(df, schema_fields)

        logger.debug("Got {} rows.\n".format(rows_iter.total_rows))
        return df

    def load_data(
        self,
        dataframe,
        destination_table_ref,
        write_disposition,
        chunksize=None,
        schema=None,
        progress_bar=True,
        api_method: str = "load_parquet",
        billing_project: Optional[str] = None,
    ):
        from pandas_gbq import load

        total_rows = len(dataframe)

        try:
            chunks = load.load_chunks(
                self.client,
                dataframe,
                destination_table_ref,
                chunksize=chunksize,
                schema=schema,
                location=self.location,
                api_method=api_method,
                write_disposition=write_disposition,
                billing_project=billing_project,
            )
            if progress_bar and tqdm:
                chunks = tqdm.tqdm(chunks)
            for remaining_rows in chunks:
                logger.info(
                    "\r{} out of {} rows loaded.".format(
                        total_rows - remaining_rows, total_rows
                    )
                )
        except self.http_error as ex:
            self.process_http_error(ex)


def _bqschema_to_nullsafe_dtypes(schema_fields):
    """Specify explicit dtypes based on BigQuery schema.

    This function only specifies a dtype when the dtype allows nulls.
    Otherwise, use pandas's default dtype choice.

    See: http://pandas.pydata.org/pandas-docs/dev/missing_data.html
    #missing-data-casting-rules-and-indexing
    """
    import db_dtypes

    # If you update this mapping, also update the table at
    # `docs/reading.rst`.
    dtype_map = {
        "FLOAT": np.dtype(float),
        "INTEGER": "Int64",
        "TIME": db_dtypes.TimeDtype(),
        # Note: Other types such as 'datetime64[ns]' and db_types.DateDtype()
        # are not included because the pandas range does not align with the
        # BigQuery range. We need to attempt a conversion to those types and
        # fall back to 'object' when there are out-of-range values.
    }

    # Amend dtype_map with newer extension types if pandas version allows.
    if FEATURES.pandas_has_boolean_dtype:
        dtype_map["BOOLEAN"] = "boolean"

    dtypes = {}
    for field in schema_fields:
        name = str(field["name"])
        # Array BigQuery type is represented as an object column containing
        # list objects.
        if field["mode"].upper() == "REPEATED":
            dtypes[name] = "object"
            continue

        dtype = dtype_map.get(field["type"].upper())
        if dtype:
            dtypes[name] = dtype

    return dtypes


def _finalize_dtypes(
    df: "pandas.DataFrame", schema_fields: Sequence[Dict[str, Any]]
) -> "pandas.DataFrame":
    """
    Attempt to change the dtypes of those columns that don't map exactly.

    For example db_dtypes.DateDtype() and datetime64[ns] cannot represent
    0001-01-01, but they can represent dates within a couple hundred years of
    1970. See:
    https://github.com/googleapis/python-bigquery-pandas/issues/365
    """
    import db_dtypes
    import pandas.api.types

    # If you update this mapping, also update the table at
    # `docs/reading.rst`.
    dtype_map = {
        "DATE": db_dtypes.DateDtype(),
        "DATETIME": "datetime64[ns]",
        "TIMESTAMP": "datetime64[ns]",
    }

    for field in schema_fields:
        # This method doesn't modify ARRAY/REPEATED columns.
        if field["mode"].upper() == "REPEATED":
            continue

        name = str(field["name"])
        dtype = dtype_map.get(field["type"].upper())

        # Avoid deprecated conversion to timezone-naive dtype by only casting
        # object dtypes.
        if dtype and pandas.api.types.is_object_dtype(df[name]):
            df[name] = df[name].astype(dtype, errors="ignore")

    # Ensure any TIMESTAMP columns are tz-aware.
    df = pandas_gbq.timestamp.localize_df(df, schema_fields)

    return df


def _get_client(user_agent, rfc9110_delimiter, project_id, credentials):
    import google.api_core.client_info

    bigquery = FEATURES.bigquery_try_import()

    user_agent = create_user_agent(
        user_agent=user_agent, rfc9110_delimiter=rfc9110_delimiter
    )

    client_info = google.api_core.client_info.ClientInfo(
        user_agent=user_agent,
    )
    return bigquery.Client(
        project=project_id,
        credentials=credentials,
        client_info=client_info,
    )


def create_user_agent(
    user_agent: Optional[str] = None, rfc9110_delimiter: bool = False
) -> str:
    """Creates a user agent string.

    The legacy format of our the user agent string was: `product-x.y.z` (where x,
    y, and z are the major, minor, and micro version numbers).

    Users are able to prepend this string with their own user agent identifier
    to render something similar to `<my_user_agent> pandas-x.y.z`.

    The legacy format used a hyphen to separate the product from the product
    version which differs slightly from the format recommended by RFC9110, which is:
    `product/x.y.z`. To produce a user agent more in line with the RFC, set
    rfc9110_delimiter to True. This setting does not depend on whether a
    user_agent is also supplied.

    Reference:
        https://www.rfc-editor.org/info/rfc9110

    Args:
        user_agent (Optional[str]): User agent string.

        rfc9110_delimiter (Optional[bool]): Sets delimiter to a hyphen or a slash.
        Default is False, meaning a hyphen will be used.

    Returns (str):
        Customized user agent string.

    Deprecation Warning:
        In a future major release, the default delimiter will be changed to
        a `/` in accordance with RFC9110.
    """
    import pandas as pd

    if rfc9110_delimiter:
        delimiter = "/"
    else:
        warnings.warn(
            "In a future major release, the default delimiter will be "
            "changed to a `/` in accordance with RFC9110.",
            PendingDeprecationWarning,
            stacklevel=2,
        )
        delimiter = "-"

    identities = [] if user_agent is None else [user_agent]
    identities.append(f"pandas{delimiter}{pd.__version__}")

    if environment.is_vscode():
        identities.append("vscode")
        if environment.is_vscode_google_cloud_code_extension_installed():
            identities.append(environment.GOOGLE_CLOUD_CODE_EXTENSION_NAME)
    elif environment.is_jupyter():
        identities.append("jupyter")
        if environment.is_jupyter_bigquery_plugin_installed():
            identities.append(environment.BIGQUERY_JUPYTER_PLUGIN_NAME)

    return " ".join(identities)
