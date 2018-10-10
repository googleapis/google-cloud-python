import logging
import os
import time
import warnings
from collections import OrderedDict
from datetime import datetime

import numpy as np
from pandas import DataFrame

from pandas_gbq.exceptions import AccessDenied

logger = logging.getLogger(__name__)

BIGQUERY_INSTALLED_VERSION = None
SHOW_VERBOSE_DEPRECATION = False

try:
    import tqdm  # noqa
except ImportError:
    tqdm = None


def _check_google_client_version():
    global BIGQUERY_INSTALLED_VERSION, SHOW_VERBOSE_DEPRECATION

    try:
        import pkg_resources

    except ImportError:
        raise ImportError("Could not import pkg_resources (setuptools).")

    # https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/bigquery/CHANGELOG.md
    bigquery_minimum_version = pkg_resources.parse_version("0.32.0")
    BIGQUERY_INSTALLED_VERSION = pkg_resources.get_distribution(
        "google-cloud-bigquery"
    ).parsed_version

    if BIGQUERY_INSTALLED_VERSION < bigquery_minimum_version:
        raise ImportError(
            "pandas-gbq requires google-cloud-bigquery >= {0}, "
            "current version {1}".format(
                bigquery_minimum_version, BIGQUERY_INSTALLED_VERSION
            )
        )

    # Add check for Pandas version before showing deprecation warning.
    # https://github.com/pydata/pandas-gbq/issues/157
    pandas_installed_version = pkg_resources.get_distribution(
        "pandas"
    ).parsed_version
    pandas_version_wo_verbosity = pkg_resources.parse_version("0.23.0")
    SHOW_VERBOSE_DEPRECATION = (
        pandas_installed_version >= pandas_version_wo_verbosity
    )


def _test_google_api_imports():

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow  # noqa
    except ImportError as ex:
        raise ImportError(
            "pandas-gbq requires google-auth-oauthlib: {0}".format(ex)
        )

    try:
        import google.auth  # noqa
    except ImportError as ex:
        raise ImportError("pandas-gbq requires google-auth: {0}".format(ex))

    try:
        from google.cloud import bigquery  # noqa
    except ImportError as ex:
        raise ImportError(
            "pandas-gbq requires google-cloud-bigquery: {0}".format(ex)
        )

    _check_google_client_version()


class DatasetCreationError(ValueError):
    """
    Raised when the create dataset method fails
    """

    pass


class GenericGBQException(ValueError):
    """
    Raised when an unrecognized Google API Error occurs.
    """

    pass


class InvalidColumnOrder(ValueError):
    """
    Raised when the provided column order for output
    results DataFrame does not match the schema
    returned by BigQuery.
    """

    pass


class InvalidIndexColumn(ValueError):
    """
    Raised when the provided index column for output
    results DataFrame does not match the schema
    returned by BigQuery.
    """

    pass


class InvalidPageToken(ValueError):
    """
    Raised when Google BigQuery fails to return,
    or returns a duplicate page token.
    """

    pass


class InvalidSchema(ValueError):
    """
    Raised when the provided DataFrame does
    not match the schema of the destination
    table in BigQuery.
    """

    pass


class NotFoundException(ValueError):
    """
    Raised when the project_id, table or dataset provided in the query could
    not be found.
    """

    pass


class QueryTimeout(ValueError):
    """
    Raised when the query request exceeds the timeoutMs value specified in the
    BigQuery configuration.
    """

    pass


class TableCreationError(ValueError):
    """
    Raised when the create table method fails
    """

    pass


class Context(object):
    """Storage for objects to be used throughout a session.

    A Context object is initialized when the ``pandas_gbq`` module is
    imported, and can be found at :attr:`pandas_gbq.context`.
    """

    def __init__(self):
        self._credentials = None
        self._project = None

    @property
    def credentials(self):
        """google.auth.credentials.Credentials: Credentials to use for Google
        APIs.

        Note:
            These credentials are automatically cached in memory by calls to
            :func:`pandas_gbq.read_gbq` and :func:`pandas_gbq.to_gbq`. To
            manually set the credentials, construct an
            :class:`google.auth.credentials.Credentials` object and set it as
            the context credentials as demonstrated in the example below. See
            `auth docs`_ for more information on obtaining credentials.

        Example:
            Manually setting the context credentials:
            >>> import pandas_gbq
            >>> from google.oauth2 import service_account
            >>> credentials = (service_account
            ...     .Credentials.from_service_account_file(
            ...         '/path/to/key.json'))
            >>> pandas_gbq.context.credentials = credentials
        .. _auth docs: http://google-auth.readthedocs.io
            /en/latest/user-guide.html#obtaining-credentials
        """
        return self._credentials

    @credentials.setter
    def credentials(self, value):
        self._credentials = value

    @property
    def project(self):
        """str: Default project to use for calls to Google APIs.

        Example:
            Manually setting the context project:
            >>> import pandas_gbq
            >>> pandas_gbq.context.project = 'my-project'
        """
        return self._project

    @project.setter
    def project(self, value):
        self._project = value


# Create an empty context, used to cache credentials.
context = Context()
"""A :class:`pandas_gbq.Context` object used to cache credentials.

Credentials automatically are cached in-memory by :func:`pandas_gbq.read_gbq`
and :func:`pandas_gbq.to_gbq`.
"""


class GbqConnector(object):
    def __init__(
        self,
        project_id,
        reauth=False,
        private_key=None,
        auth_local_webserver=False,
        dialect="legacy",
        location=None,
        try_credentials=None,
    ):
        global context
        from google.api_core.exceptions import GoogleAPIError
        from google.api_core.exceptions import ClientError
        from pandas_gbq import auth

        self.http_error = (ClientError, GoogleAPIError)
        self.project_id = project_id
        self.location = location
        self.reauth = reauth
        self.private_key = private_key
        self.auth_local_webserver = auth_local_webserver
        self.dialect = dialect
        self.credentials_path = _get_credentials_file()

        # Load credentials from cache.
        self.credentials = context.credentials
        default_project = context.project

        # Credentials were explicitly asked for, so don't use the cache.
        if private_key or reauth or not self.credentials:
            self.credentials, default_project = auth.get_credentials(
                private_key=private_key,
                project_id=project_id,
                reauth=reauth,
                auth_local_webserver=auth_local_webserver,
                try_credentials=try_credentials,
            )

        if self.project_id is None:
            self.project_id = default_project

        if self.project_id is None:
            raise ValueError(
                "Could not determine project ID and one was not supplied."
            )

        # Cache the credentials if they haven't been set yet.
        if context.credentials is None:
            context.credentials = self.credentials
        if context.project is None:
            context.project = self.project_id

        self.client = self.get_client()

        # BQ Queries costs $5 per TB. First 1 TB per month is free
        # see here for more: https://cloud.google.com/bigquery/pricing
        self.query_price_for_TB = 5.0 / 2 ** 40  # USD/TB

    def _start_timer(self):
        self.start = time.time()

    def get_elapsed_seconds(self):
        return round(time.time() - self.start, 2)

    def log_elapsed_seconds(self, prefix="Elapsed", postfix="s.", overlong=6):
        sec = self.get_elapsed_seconds()
        if sec > overlong:
            logger.info("{} {} {}".format(prefix, sec, postfix))

    # http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    @staticmethod
    def sizeof_fmt(num, suffix="B"):
        fmt = "%3.1f %s%s"
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if abs(num) < 1024.0:
                return fmt % (num, unit, suffix)
            num /= 1024.0
        return fmt % (num, "Y", suffix)

    def get_client(self):
        from google.cloud import bigquery

        return bigquery.Client(
            project=self.project_id, credentials=self.credentials
        )

    @staticmethod
    def process_http_error(ex):
        # See `BigQuery Troubleshooting Errors
        # <https://cloud.google.com/bigquery/troubleshooting-errors>`__

        raise GenericGBQException("Reason: {0}".format(ex))

    def run_query(self, query, **kwargs):
        from concurrent.futures import TimeoutError
        from google.auth.exceptions import RefreshError
        from google.cloud import bigquery

        job_config = {
            "query": {
                "useLegacySql": self.dialect
                == "legacy"
                # 'allowLargeResults', 'createDisposition',
                # 'preserveNulls', destinationTable, useQueryCache
            }
        }
        config = kwargs.get("configuration")
        if config is not None:
            job_config.update(config)

            if "query" in config and "query" in config["query"]:
                if query is not None:
                    raise ValueError(
                        "Query statement can't be specified "
                        "inside config while it is specified "
                        "as parameter"
                    )
                query = config["query"].pop("query")

        self._start_timer()

        try:
            logger.debug("Requesting query... ")
            query_reply = self.client.query(
                query,
                job_config=bigquery.QueryJobConfig.from_api_repr(job_config),
                location=self.location,
            )
            logger.debug("Query running...")
        except (RefreshError, ValueError):
            if self.private_key:
                raise AccessDenied(
                    "The service account credentials are not valid"
                )
            else:
                raise AccessDenied(
                    "The credentials have been revoked or expired, "
                    "please re-run the application to re-authorize"
                )
        except self.http_error as ex:
            self.process_http_error(ex)

        job_id = query_reply.job_id
        logger.debug("Job ID: %s" % job_id)

        while query_reply.state != "DONE":
            self.log_elapsed_seconds("  Elapsed", "s. Waiting...")

            timeout_ms = job_config["query"].get("timeoutMs")
            if timeout_ms and timeout_ms < self.get_elapsed_seconds() * 1000:
                raise QueryTimeout("Query timeout: {} ms".format(timeout_ms))

            timeout_sec = 1.0
            if timeout_ms:
                # Wait at most 1 second so we can show progress bar
                timeout_sec = min(1.0, timeout_ms / 1000.0)

            try:
                query_reply.result(timeout=timeout_sec)
            except TimeoutError:
                # Use our own timeout logic
                pass
            except self.http_error as ex:
                self.process_http_error(ex)

        if query_reply.cache_hit:
            logger.debug("Query done.\nCache hit.\n")
        else:
            bytes_processed = query_reply.total_bytes_processed or 0
            bytes_billed = query_reply.total_bytes_billed or 0
            logger.debug(
                "Query done.\nProcessed: {} Billed: {}".format(
                    self.sizeof_fmt(bytes_processed),
                    self.sizeof_fmt(bytes_billed),
                )
            )
            logger.debug(
                "Standard price: ${:,.2f} USD\n".format(
                    bytes_billed * self.query_price_for_TB
                )
            )

        try:
            rows_iter = query_reply.result()
        except self.http_error as ex:
            self.process_http_error(ex)
        result_rows = list(rows_iter)
        total_rows = rows_iter.total_rows
        schema = {
            "fields": [field.to_api_repr() for field in rows_iter.schema]
        }

        logger.debug("Got {} rows.\n".format(total_rows))

        return schema, result_rows

    def load_data(
        self,
        dataframe,
        dataset_id,
        table_id,
        chunksize=None,
        schema=None,
        progress_bar=True,
    ):
        from pandas_gbq import load

        total_rows = len(dataframe)

        try:
            chunks = load.load_chunks(
                self.client,
                dataframe,
                dataset_id,
                table_id,
                chunksize=chunksize,
                schema=schema,
                location=self.location,
            )
            if progress_bar and tqdm:
                chunks = tqdm.tqdm(chunks)
            for remaining_rows in chunks:
                logger.info(
                    "\rLoad is {0}% Complete".format(
                        ((total_rows - remaining_rows) * 100) / total_rows
                    )
                )
        except self.http_error as ex:
            self.process_http_error(ex)

    def schema(self, dataset_id, table_id):
        """Retrieve the schema of the table

        Obtain from BigQuery the field names and field types
        for the table defined by the parameters

        Parameters
        ----------
        dataset_id : str
            Name of the BigQuery dataset for the table
        table_id : str
            Name of the BigQuery table

        Returns
        -------
        list of dicts
            Fields representing the schema
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)

        try:
            table = self.client.get_table(table_ref)
            remote_schema = table.schema

            remote_fields = [
                field_remote.to_api_repr() for field_remote in remote_schema
            ]
            for field in remote_fields:
                field["type"] = field["type"].upper()
                field["mode"] = field["mode"].upper()

            return remote_fields
        except self.http_error as ex:
            self.process_http_error(ex)

    def _clean_schema_fields(self, fields):
        """Return a sanitized version of the schema for comparisons."""
        fields_sorted = sorted(fields, key=lambda field: field["name"])
        # Ignore mode and description when comparing schemas.
        return [
            {"name": field["name"], "type": field["type"]}
            for field in fields_sorted
        ]

    def verify_schema(self, dataset_id, table_id, schema):
        """Indicate whether schemas match exactly

        Compare the BigQuery table identified in the parameters with
        the schema passed in and indicate whether all fields in the former
        are present in the latter. Order is not considered.

        Parameters
        ----------
        dataset_id :str
            Name of the BigQuery dataset for the table
        table_id : str
            Name of the BigQuery table
        schema : list(dict)
            Schema for comparison. Each item should have
            a 'name' and a 'type'

        Returns
        -------
        bool
            Whether the schemas match
        """

        fields_remote = self._clean_schema_fields(
            self.schema(dataset_id, table_id)
        )
        fields_local = self._clean_schema_fields(schema["fields"])

        return fields_remote == fields_local

    def schema_is_subset(self, dataset_id, table_id, schema):
        """Indicate whether the schema to be uploaded is a subset

        Compare the BigQuery table identified in the parameters with
        the schema passed in and indicate whether a subset of the fields in
        the former are present in the latter. Order is not considered.

        Parameters
        ----------
        dataset_id : str
            Name of the BigQuery dataset for the table
        table_id : str
            Name of the BigQuery table
        schema : list(dict)
            Schema for comparison. Each item should have
            a 'name' and a 'type'

        Returns
        -------
        bool
            Whether the passed schema is a subset
        """

        fields_remote = self._clean_schema_fields(
            self.schema(dataset_id, table_id)
        )
        fields_local = self._clean_schema_fields(schema["fields"])

        return all(field in fields_remote for field in fields_local)

    def delete_and_recreate_table(self, dataset_id, table_id, table_schema):
        table = _Table(
            self.project_id, dataset_id, private_key=self.private_key
        )
        table.delete(table_id)
        table.create(table_id, table_schema)


def _get_credentials_file():
    return os.environ.get("PANDAS_GBQ_CREDENTIALS_FILE")


def _parse_schema(schema_fields):
    # see:
    # http://pandas.pydata.org/pandas-docs/dev/missing_data.html
    # #missing-data-casting-rules-and-indexing
    dtype_map = {
        "FLOAT": np.dtype(float),
        "TIMESTAMP": "datetime64[ns]",
        "TIME": "datetime64[ns]",
        "DATE": "datetime64[ns]",
        "DATETIME": "datetime64[ns]",
        "BOOLEAN": bool,
        "INTEGER": np.int64,
    }

    for field in schema_fields:
        name = str(field["name"])
        if field["mode"].upper() == "REPEATED":
            yield name, object
        else:
            dtype = dtype_map.get(field["type"].upper())
            yield name, dtype


def _parse_data(schema, rows):

    column_dtypes = OrderedDict(_parse_schema(schema["fields"]))
    df = DataFrame(data=(iter(r) for r in rows), columns=column_dtypes.keys())

    for column in df:
        dtype = column_dtypes[column]
        null_safe = (
            df[column].notnull().all()
            or dtype == float
            or dtype == "datetime64[ns]"
        )
        if dtype and null_safe:
            df[column] = df[column].astype(
                column_dtypes[column], errors="ignore"
            )
    return df


def read_gbq(
    query,
    project_id=None,
    index_col=None,
    col_order=None,
    reauth=False,
    private_key=None,
    auth_local_webserver=False,
    dialect=None,
    location=None,
    configuration=None,
    verbose=None,
):
    r"""Load data from Google BigQuery using google-cloud-python

    The main method a user calls to execute a Query in Google BigQuery
    and read results into a pandas DataFrame.

    This method uses the Google Cloud client library to make requests to
    Google BigQuery, documented `here
    <https://google-cloud-python.readthedocs.io/en/latest/bigquery/usage.html>`__.

    See the :ref:`How to authenticate with Google BigQuery <authentication>`
    guide for authentication instructions.

    Parameters
    ----------
    query : str
        SQL-Like Query to return data values.
    project_id : str, optional
        Google BigQuery Account project ID. Optional when available from
        the environment.
    index_col : str, optional
        Name of result column to use for index in results DataFrame.
    col_order : list(str), optional
        List of BigQuery column names in the desired order for results
        DataFrame.
    reauth : boolean, default False
        Force Google BigQuery to re-authenticate the user. This is useful
        if multiple accounts are used.
    private_key : str, optional
        Service account private key in JSON format. Can be file path
        or string contents. This is useful for remote server
        authentication (eg. Jupyter/IPython notebook on remote host).
    auth_local_webserver : boolean, default False
        Use the `local webserver flow`_ instead of the `console flow`_
        when getting user credentials.

        .. _local webserver flow:
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_local_server
        .. _console flow:
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_console

        .. versionadded:: 0.2.0
    dialect : str, default 'legacy'
        Note: The default value is changing to 'standard' in a future verion.

        SQL syntax dialect to use. Value can be one of:

        ``'legacy'``
            Use BigQuery's legacy SQL dialect. For more information see
            `BigQuery Legacy SQL Reference
            <https://cloud.google.com/bigquery/docs/reference/legacy-sql>`__.
        ``'standard'``
            Use BigQuery's standard SQL, which is
            compliant with the SQL 2011 standard. For more information
            see `BigQuery Standard SQL Reference
            <https://cloud.google.com/bigquery/docs/reference/standard-sql/>`__.
    location : str, optional
        Location where the query job should run. See the `BigQuery locations
        documentation
        <https://cloud.google.com/bigquery/docs/dataset-locations>`__ for a
        list of available locations. The location must match that of any
        datasets used in the query.

        .. versionadded:: 0.5.0
    configuration : dict, optional
        Query config parameters for job processing.
        For example:

            configuration = {'query': {'useQueryCache': False}}

        For more information see `BigQuery REST API Reference
        <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query>`__.
    verbose : None, deprecated
        Deprecated in Pandas-GBQ 0.4.0. Use the `logging module
        to adjust verbosity instead
        <https://pandas-gbq.readthedocs.io/en/latest/intro.html#logging>`__.

    Returns
    -------
    df: DataFrame
        DataFrame representing results of query.
    """
    if dialect is None:
        dialect = "legacy"
        warnings.warn(
            'The default value for dialect is changing to "standard" in a '
            'future version. Pass in dialect="legacy" to disable this '
            "warning.",
            FutureWarning,
            stacklevel=2,
        )

    _test_google_api_imports()

    if verbose is not None and SHOW_VERBOSE_DEPRECATION:
        warnings.warn(
            "verbose is deprecated and will be removed in "
            "a future version. Set logging level in order to vary "
            "verbosity",
            FutureWarning,
            stacklevel=2,
        )

    if dialect not in ("legacy", "standard"):
        raise ValueError("'{0}' is not valid for dialect".format(dialect))

    connector = GbqConnector(
        project_id,
        reauth=reauth,
        private_key=private_key,
        dialect=dialect,
        auth_local_webserver=auth_local_webserver,
        location=location,
    )
    schema, rows = connector.run_query(query, configuration=configuration)
    final_df = _parse_data(schema, rows)

    # Reindex the DataFrame on the provided column
    if index_col is not None:
        if index_col in final_df.columns:
            final_df.set_index(index_col, inplace=True)
        else:
            raise InvalidIndexColumn(
                'Index column "{0}" does not exist in DataFrame.'.format(
                    index_col
                )
            )

    # Change the order of columns in the DataFrame based on provided list
    if col_order is not None:
        if sorted(col_order) == sorted(final_df.columns):
            final_df = final_df[col_order]
        else:
            raise InvalidColumnOrder(
                "Column order does not match this DataFrame."
            )

    connector.log_elapsed_seconds(
        "Total time taken",
        datetime.now().strftime("s.\nFinished at %Y-%m-%d %H:%M:%S."),
    )

    return final_df


def to_gbq(
    dataframe,
    destination_table,
    project_id=None,
    chunksize=None,
    reauth=False,
    if_exists="fail",
    private_key=None,
    auth_local_webserver=False,
    table_schema=None,
    location=None,
    progress_bar=True,
    verbose=None,
):
    """Write a DataFrame to a Google BigQuery table.

    The main method a user calls to export pandas DataFrame contents to
    Google BigQuery table.

    This method uses the Google Cloud client library to make requests to
    Google BigQuery, documented `here
    <https://google-cloud-python.readthedocs.io/en/latest/bigquery/usage.html>`__.

    See the :ref:`How to authenticate with Google BigQuery <authentication>`
    guide for authentication instructions.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        DataFrame to be written to a Google BigQuery table.
    destination_table : str
        Name of table to be written, in the form ``dataset.tablename``.
    project_id : str, optional
        Google BigQuery Account project ID. Optional when available from
        the environment.
    chunksize : int, optional
        Number of rows to be inserted in each chunk from the dataframe.
        Set to ``None`` to load the whole dataframe at once.
    reauth : bool, default False
        Force Google BigQuery to re-authenticate the user. This is useful
        if multiple accounts are used.
    if_exists : str, default 'fail'
        Behavior when the destination table exists. Value can be one of:

        ``'fail'``
            If table exists, do nothing.
        ``'replace'``
            If table exists, drop it, recreate it, and insert data.
        ``'append'``
            If table exists, insert data. Create if does not exist.
    private_key : str, optional
        Service account private key in JSON format. Can be file path
        or string contents. This is useful for remote server
        authentication (eg. Jupyter/IPython notebook on remote host).
    auth_local_webserver : bool, default False
        Use the `local webserver flow`_ instead of the `console flow`_
        when getting user credentials.

        .. _local webserver flow:
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_local_server
        .. _console flow:
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_console

        .. versionadded:: 0.2.0
    table_schema : list of dicts, optional
        List of BigQuery table fields to which according DataFrame
        columns conform to, e.g. ``[{'name': 'col1', 'type':
        'STRING'},...]``.
        If schema is not provided, it will be
        generated according to dtypes of DataFrame columns.
        If schema is provided, it must contain all DataFrame columns.
        pandas_gbq.gbq._generate_bq_schema() may be used to create an initial
        schema, though it doesn't preserve column order.
        See BigQuery API documentation on available names of a field.

        .. versionadded:: 0.3.1
    location : str, optional
        Location where the load job should run. See the `BigQuery locations
        documentation
        <https://cloud.google.com/bigquery/docs/dataset-locations>`__ for a
        list of available locations. The location must match that of the
        target dataset.

        .. versionadded:: 0.5.0
    progress_bar : bool, default True
        Use the library `tqdm` to show the progress bar for the upload,
        chunk by chunk.

        .. versionadded:: 0.5.0
    verbose : bool, deprecated
        Deprecated in Pandas-GBQ 0.4.0. Use the `logging module
        to adjust verbosity instead
        <https://pandas-gbq.readthedocs.io/en/latest/intro.html#logging>`__.
    """

    _test_google_api_imports()

    if verbose is not None and SHOW_VERBOSE_DEPRECATION:
        warnings.warn(
            "verbose is deprecated and will be removed in "
            "a future version. Set logging level in order to vary "
            "verbosity",
            FutureWarning,
            stacklevel=1,
        )

    if if_exists not in ("fail", "replace", "append"):
        raise ValueError("'{0}' is not valid for if_exists".format(if_exists))

    if "." not in destination_table:
        raise NotFoundException(
            "Invalid Table Name. Should be of the form 'datasetId.tableId' "
        )

    connector = GbqConnector(
        project_id,
        reauth=reauth,
        private_key=private_key,
        auth_local_webserver=auth_local_webserver,
        location=location,
        # Avoid reads when writing tables.
        # https://github.com/pydata/pandas-gbq/issues/202
        try_credentials=lambda project, creds: creds,
    )
    dataset_id, table_id = destination_table.rsplit(".", 1)

    table = _Table(
        project_id,
        dataset_id,
        reauth=reauth,
        private_key=private_key,
        location=location,
    )

    if not table_schema:
        table_schema = _generate_bq_schema(dataframe)
    else:
        table_schema = dict(fields=table_schema)

    # If table exists, check if_exists parameter
    if table.exists(table_id):
        if if_exists == "fail":
            raise TableCreationError(
                "Could not create the table because it "
                "already exists. "
                "Change the if_exists parameter to "
                "'append' or 'replace' data."
            )
        elif if_exists == "replace":
            connector.delete_and_recreate_table(
                dataset_id, table_id, table_schema
            )
        elif if_exists == "append":
            if not connector.schema_is_subset(
                dataset_id, table_id, table_schema
            ):
                raise InvalidSchema(
                    "Please verify that the structure and "
                    "data types in the DataFrame match the "
                    "schema of the destination table."
                )
    else:
        table.create(table_id, table_schema)

    connector.load_data(
        dataframe,
        dataset_id,
        table_id,
        chunksize=chunksize,
        schema=table_schema,
        progress_bar=progress_bar,
    )


def generate_bq_schema(df, default_type="STRING"):
    """DEPRECATED: Given a passed df, generate the associated Google BigQuery
    schema.

    Parameters
    ----------
    df : DataFrame
    default_type : string
        The default big query type in case the type of the column
        does not exist in the schema.
    """
    # deprecation TimeSeries, #11121
    warnings.warn(
        "generate_bq_schema is deprecated and will be removed in "
        "a future version",
        FutureWarning,
        stacklevel=2,
    )

    return _generate_bq_schema(df, default_type=default_type)


def _generate_bq_schema(df, default_type="STRING"):
    from pandas_gbq import schema

    return schema.generate_bq_schema(df, default_type=default_type)


class _Table(GbqConnector):
    def __init__(
        self,
        project_id,
        dataset_id,
        reauth=False,
        private_key=None,
        location=None,
    ):
        self.dataset_id = dataset_id
        super(_Table, self).__init__(
            project_id, reauth, private_key, location=location
        )

    def exists(self, table_id):
        """ Check if a table exists in Google BigQuery

        Parameters
        ----------
        table : str
            Name of table to be verified

        Returns
        -------
        boolean
            true if table exists, otherwise false
        """
        from google.api_core.exceptions import NotFound

        table_ref = self.client.dataset(self.dataset_id).table(table_id)
        try:
            self.client.get_table(table_ref)
            return True
        except NotFound:
            return False
        except self.http_error as ex:
            self.process_http_error(ex)

    def create(self, table_id, schema):
        """ Create a table in Google BigQuery given a table and schema

        Parameters
        ----------
        table : str
            Name of table to be written
        schema : str
            Use the generate_bq_schema to generate your table schema from a
            dataframe.
        """
        from google.cloud.bigquery import SchemaField
        from google.cloud.bigquery import Table

        if self.exists(table_id):
            raise TableCreationError(
                "Table {0} already " "exists".format(table_id)
            )

        if not _Dataset(self.project_id, private_key=self.private_key).exists(
            self.dataset_id
        ):
            _Dataset(
                self.project_id,
                private_key=self.private_key,
                location=self.location,
            ).create(self.dataset_id)

        table_ref = self.client.dataset(self.dataset_id).table(table_id)
        table = Table(table_ref)

        # Manually create the schema objects, adding NULLABLE mode
        # as a workaround for
        # https://github.com/GoogleCloudPlatform/google-cloud-python/issues/4456
        for field in schema["fields"]:
            if "mode" not in field:
                field["mode"] = "NULLABLE"

        table.schema = [
            SchemaField.from_api_repr(field) for field in schema["fields"]
        ]

        try:
            self.client.create_table(table)
        except self.http_error as ex:
            self.process_http_error(ex)

    def delete(self, table_id):
        """ Delete a table in Google BigQuery

        Parameters
        ----------
        table : str
            Name of table to be deleted
        """
        from google.api_core.exceptions import NotFound

        if not self.exists(table_id):
            raise NotFoundException("Table does not exist")

        table_ref = self.client.dataset(self.dataset_id).table(table_id)
        try:
            self.client.delete_table(table_ref)
        except NotFound:
            # Ignore 404 error which may occur if table already deleted
            pass
        except self.http_error as ex:
            self.process_http_error(ex)


class _Dataset(GbqConnector):
    def __init__(
        self, project_id, reauth=False, private_key=None, location=None
    ):
        super(_Dataset, self).__init__(
            project_id, reauth, private_key, location=location
        )

    def exists(self, dataset_id):
        """ Check if a dataset exists in Google BigQuery

        Parameters
        ----------
        dataset_id : str
            Name of dataset to be verified

        Returns
        -------
        boolean
            true if dataset exists, otherwise false
        """
        from google.api_core.exceptions import NotFound

        try:
            self.client.get_dataset(self.client.dataset(dataset_id))
            return True
        except NotFound:
            return False
        except self.http_error as ex:
            self.process_http_error(ex)

    def create(self, dataset_id):
        """ Create a dataset in Google BigQuery

        Parameters
        ----------
        dataset : str
            Name of dataset to be written
        """
        from google.cloud.bigquery import Dataset

        if self.exists(dataset_id):
            raise DatasetCreationError(
                "Dataset {0} already " "exists".format(dataset_id)
            )

        dataset = Dataset(self.client.dataset(dataset_id))

        if self.location is not None:
            dataset.location = self.location

        try:
            self.client.create_dataset(dataset)
        except self.http_error as ex:
            self.process_http_error(ex)
