import json
import logging
import os
import time
import warnings
from datetime import datetime
from time import sleep

import numpy as np
from pandas import DataFrame, compat
from pandas.compat import lzip

logger = logging.getLogger(__name__)


BIGQUERY_INSTALLED_VERSION = None


def _check_google_client_version():
    global BIGQUERY_INSTALLED_VERSION

    try:
        import pkg_resources

    except ImportError:
        raise ImportError('Could not import pkg_resources (setuptools).')

    # https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/bigquery/CHANGELOG.md
    bigquery_minimum_version = pkg_resources.parse_version('0.29.0')
    BIGQUERY_INSTALLED_VERSION = pkg_resources.get_distribution(
        'google-cloud-bigquery').parsed_version

    if BIGQUERY_INSTALLED_VERSION < bigquery_minimum_version:
        raise ImportError(
            'pandas-gbq requires google-cloud-bigquery >= {0}, '
            'current version {1}'.format(
                bigquery_minimum_version, BIGQUERY_INSTALLED_VERSION))


def _test_google_api_imports():

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow  # noqa
    except ImportError as ex:
        raise ImportError(
            'pandas-gbq requires google-auth-oauthlib: {0}'.format(ex))

    try:
        import google.auth  # noqa
    except ImportError as ex:
        raise ImportError(
            "pandas-gbq requires google-auth: {0}".format(ex))

    try:
        from google.cloud import bigquery  # noqa
    except ImportError as ex:
        raise ImportError(
            "pandas-gbq requires google-cloud-bigquery: {0}".format(ex))

    _check_google_client_version()


def _try_credentials(project_id, credentials):
    from google.cloud import bigquery
    import google.api_core.exceptions

    if credentials is None:
        return None

    try:
        client = bigquery.Client(project=project_id, credentials=credentials)
        # Check if the application has rights to the BigQuery project
        client.query('SELECT 1').result()
        return credentials
    except google.api_core.exceptions.GoogleAPIError:
        return None


class InvalidPrivateKeyFormat(ValueError):
    """
    Raised when provided private key has invalid format.
    """
    pass


class AccessDenied(ValueError):
    """
    Raised when invalid credentials are provided, or tokens have expired.
    """
    pass


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


class GbqConnector(object):
    scope = 'https://www.googleapis.com/auth/bigquery'

    def __init__(self, project_id, reauth=False,
                 private_key=None, auth_local_webserver=False,
                 dialect='legacy'):
        from google.api_core.exceptions import GoogleAPIError
        from google.api_core.exceptions import ClientError
        self.http_error = (ClientError, GoogleAPIError)
        self.project_id = project_id
        self.reauth = reauth
        self.private_key = private_key
        self.auth_local_webserver = auth_local_webserver
        self.dialect = dialect
        self.credentials_path = _get_credentials_file()
        self.credentials = self.get_credentials()
        self.client = self.get_client()

        # BQ Queries costs $5 per TB. First 1 TB per month is free
        # see here for more: https://cloud.google.com/bigquery/pricing
        self.query_price_for_TB = 5. / 2**40  # USD/TB

    def get_credentials(self):
        if self.private_key:
            return self.get_service_account_credentials()
        else:
            # Try to retrieve Application Default Credentials
            credentials = self.get_application_default_credentials()
            if not credentials:
                credentials = self.get_user_account_credentials()
            return credentials

    def get_application_default_credentials(self):
        """
        This method tries to retrieve the "default application credentials".
        This could be useful for running code on Google Cloud Platform.

        Parameters
        ----------
        None

        Returns
        -------
        - GoogleCredentials,
            If the default application credentials can be retrieved
            from the environment. The retrieved credentials should also
            have access to the project (self.project_id) on BigQuery.
        - OR None,
            If default application credentials can not be retrieved
            from the environment. Or, the retrieved credentials do not
            have access to the project (self.project_id) on BigQuery.
        """
        import google.auth
        from google.auth.exceptions import DefaultCredentialsError

        try:
            credentials, _ = google.auth.default(scopes=[self.scope])
        except (DefaultCredentialsError, IOError):
            return None

        return _try_credentials(self.project_id, credentials)

    def load_user_account_credentials(self):
        """
        Loads user account credentials from a local file.

        .. versionadded 0.2.0

        Parameters
        ----------
        None

        Returns
        -------
        - GoogleCredentials,
            If the credentials can loaded. The retrieved credentials should
            also have access to the project (self.project_id) on BigQuery.
        - OR None,
            If credentials can not be loaded from a file. Or, the retrieved
            credentials do not have access to the project (self.project_id)
            on BigQuery.
        """
        import google.auth.transport.requests
        from google.oauth2.credentials import Credentials

        # Use the default credentials location under ~/.config and the
        # equivalent directory on windows if the user has not specified a
        # credentials path.
        if not self.credentials_path:
            self.credentials_path = self.get_default_credentials_path()

            # Previously, pandas-gbq saved user account credentials in the
            # current working directory. If the bigquery_credentials.dat file
            # exists in the current working directory, move the credentials to
            # the new default location.
            if os.path.isfile('bigquery_credentials.dat'):
                os.rename('bigquery_credentials.dat', self.credentials_path)

        try:
            with open(self.credentials_path) as credentials_file:
                credentials_json = json.load(credentials_file)
        except (IOError, ValueError):
            return None

        credentials = Credentials(
            token=credentials_json.get('access_token'),
            refresh_token=credentials_json.get('refresh_token'),
            id_token=credentials_json.get('id_token'),
            token_uri=credentials_json.get('token_uri'),
            client_id=credentials_json.get('client_id'),
            client_secret=credentials_json.get('client_secret'),
            scopes=credentials_json.get('scopes'))

        # Refresh the token before trying to use it.
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)

        return _try_credentials(self.project_id, credentials)

    def get_default_credentials_path(self):
        """
        Gets the default path to the BigQuery credentials

        .. versionadded 0.3.0

        Returns
        -------
        Path to the BigQuery credentials
        """

        import os

        if os.name == 'nt':
            config_path = os.environ['APPDATA']
        else:
            config_path = os.path.join(os.path.expanduser('~'), '.config')

        config_path = os.path.join(config_path, 'pandas_gbq')

        # Create a pandas_gbq directory in an application-specific hidden
        # user folder on the operating system.
        if not os.path.exists(config_path):
            os.makedirs(config_path)

        return os.path.join(config_path, 'bigquery_credentials.dat')

    def save_user_account_credentials(self, credentials):
        """
        Saves user account credentials to a local file.

        .. versionadded 0.2.0
        """
        try:
            with open(self.credentials_path, 'w') as credentials_file:
                credentials_json = {
                    'refresh_token': credentials.refresh_token,
                    'id_token': credentials.id_token,
                    'token_uri': credentials.token_uri,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'scopes': credentials.scopes,
                }
                json.dump(credentials_json, credentials_file)
        except IOError:
            logger.warning('Unable to save credentials.')

    def get_user_account_credentials(self):
        """Gets user account credentials.

        This method authenticates using user credentials, either loading saved
        credentials from a file or by going through the OAuth flow.

        Parameters
        ----------
        None

        Returns
        -------
        GoogleCredentials : credentials
            Credentials for the user with BigQuery access.
        """
        from google_auth_oauthlib.flow import InstalledAppFlow
        from oauthlib.oauth2.rfc6749.errors import OAuth2Error

        credentials = self.load_user_account_credentials()

        client_config = {
            'installed': {
                'client_id': ('495642085510-k0tmvj2m941jhre2nbqka17vqpjfddtd'
                              '.apps.googleusercontent.com'),
                'client_secret': 'kOc9wMptUtxkcIFbtZCcrEAc',
                'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob'],
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://accounts.google.com/o/oauth2/token',
            }
        }

        if credentials is None or self.reauth:
            app_flow = InstalledAppFlow.from_client_config(
                client_config, scopes=[self.scope])

            try:
                if self.auth_local_webserver:
                    credentials = app_flow.run_local_server()
                else:
                    credentials = app_flow.run_console()
            except OAuth2Error as ex:
                raise AccessDenied(
                    "Unable to get valid credentials: {0}".format(ex))

            self.save_user_account_credentials(credentials)

        return credentials

    def get_service_account_credentials(self):
        import google.auth.transport.requests
        from google.oauth2.service_account import Credentials
        from os.path import isfile

        try:
            if isfile(self.private_key):
                with open(self.private_key) as f:
                    json_key = json.loads(f.read())
            else:
                # ugly hack: 'private_key' field has new lines inside,
                # they break json parser, but we need to preserve them
                json_key = json.loads(self.private_key.replace('\n', '   '))
                json_key['private_key'] = json_key['private_key'].replace(
                    '   ', '\n')

            if compat.PY3:
                json_key['private_key'] = bytes(
                    json_key['private_key'], 'UTF-8')

            credentials = Credentials.from_service_account_info(json_key)
            credentials = credentials.with_scopes([self.scope])

            # Refresh the token before trying to use it.
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)

            return credentials
        except (KeyError, ValueError, TypeError, AttributeError):
            raise InvalidPrivateKeyFormat(
                "Private key is missing or invalid. It should be service "
                "account private key JSON (file path or string contents) "
                "with at least two keys: 'client_email' and 'private_key'. "
                "Can be obtained from: https://console.developers.google."
                "com/permissions/serviceaccounts")

    def _start_timer(self):
        self.start = time.time()

    def get_elapsed_seconds(self):
        return round(time.time() - self.start, 2)

    def log_elapsed_seconds(self, prefix='Elapsed', postfix='s.',
                            overlong=7):
        sec = self.get_elapsed_seconds()
        if sec > overlong:
            logger.info('{} {} {}'.format(prefix, sec, postfix))

    # http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        fmt = "%3.1f %s%s"
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return fmt % (num, unit, suffix)
            num /= 1024.0
        return fmt % (num, 'Y', suffix)

    def get_client(self):
        from google.cloud import bigquery
        return bigquery.Client(
            project=self.project_id, credentials=self.credentials)

    @staticmethod
    def process_http_error(ex):
        # See `BigQuery Troubleshooting Errors
        # <https://cloud.google.com/bigquery/troubleshooting-errors>`__

        raise GenericGBQException("Reason: {0}".format(ex))

    def run_query(self, query, **kwargs):
        from google.auth.exceptions import RefreshError
        from concurrent.futures import TimeoutError
        from pandas_gbq import _query

        job_config = {
            'query': {
                'useLegacySql': self.dialect == 'legacy'
                # 'allowLargeResults', 'createDisposition',
                # 'preserveNulls', destinationTable, useQueryCache
            }
        }
        config = kwargs.get('configuration')
        if config is not None:
            job_config.update(config)

            if 'query' in config and 'query' in config['query']:
                if query is not None:
                    raise ValueError("Query statement can't be specified "
                                     "inside config while it is specified "
                                     "as parameter")
                query = config['query'].pop('query')

        self._start_timer()

        try:
            logger.info('Requesting query... ')
            query_reply = self.client.query(
                query,
                job_config=_query.query_config(
                    job_config, BIGQUERY_INSTALLED_VERSION))
            logger.info('ok.\nQuery running...')
        except (RefreshError, ValueError):
            if self.private_key:
                raise AccessDenied(
                    "The service account credentials are not valid")
            else:
                raise AccessDenied(
                    "The credentials have been revoked or expired, "
                    "please re-run the application to re-authorize")
        except self.http_error as ex:
            self.process_http_error(ex)

        job_id = query_reply.job_id
        logger.info('Job ID: %s\nQuery running...' % job_id)

        while query_reply.state != 'DONE':
            self.log_elapsed_seconds('  Elapsed', 's. Waiting...')

            timeout_ms = job_config['query'].get('timeoutMs')
            if timeout_ms and timeout_ms < self.get_elapsed_seconds() * 1000:
                raise QueryTimeout('Query timeout: {} ms'.format(timeout_ms))

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
            logger.debug('Query done.\nCache hit.\n')
        else:
            bytes_processed = query_reply.total_bytes_processed or 0
            bytes_billed = query_reply.total_bytes_billed or 0
            logger.debug('Query done.\nProcessed: {} Billed: {}'.format(
                self.sizeof_fmt(bytes_processed),
                self.sizeof_fmt(bytes_billed)))
            logger.debug('Standard price: ${:,.2f} USD\n'.format(
                bytes_billed * self.query_price_for_TB))

        try:
            rows_iter = query_reply.result()
        except self.http_error as ex:
            self.process_http_error(ex)
        result_rows = list(rows_iter)
        total_rows = rows_iter.total_rows
        schema = {
            'fields': [
                field.to_api_repr()
                for field in rows_iter.schema],
        }

        # log basic query stats
        logger.info('Got {} rows.\n'.format(total_rows))

        return schema, result_rows

    def load_data(
            self, dataframe, dataset_id, table_id, chunksize=None,
            schema=None):
        from pandas_gbq import _load

        total_rows = len(dataframe)
        logger.info("\n\n")

        try:
            for remaining_rows in _load.load_chunks(
                    self.client, dataframe, dataset_id, table_id,
                    chunksize=chunksize, schema=schema):
                logger.info("\rLoad is {0}% Complete".format(
                    ((total_rows - remaining_rows) * 100) / total_rows))
        except self.http_error as ex:
            self.process_http_error(ex)

        logger.info("\n")

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
                field_remote.to_api_repr() for field_remote in remote_schema]
            for field in remote_fields:
                field['type'] = field['type'].upper()
                field['mode'] = field['mode'].upper()

            return remote_fields
        except self.http_error as ex:
            self.process_http_error(ex)

    def _clean_schema_fields(self, fields):
        """Return a sanitized version of the schema for comparisons."""
        fields_sorted = sorted(fields, key=lambda field: field['name'])
        # Ignore mode and description when comparing schemas.
        return [
            {'name': field['name'], 'type': field['type']}
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
            self.schema(dataset_id, table_id))
        fields_local = self._clean_schema_fields(schema['fields'])

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
            self.schema(dataset_id, table_id))
        fields_local = self._clean_schema_fields(schema['fields'])

        return all(field in fields_remote for field in fields_local)

    def delete_and_recreate_table(self, dataset_id, table_id, table_schema):
        delay = 0

        # Changes to table schema may take up to 2 minutes as of May 2015 See
        # `Issue 191
        # <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__
        # Compare previous schema with new schema to determine if there should
        # be a 120 second delay

        if not self.verify_schema(dataset_id, table_id, table_schema):
            logger.info('The existing table has a different schema. Please '
                        'wait 2 minutes. See Google BigQuery issue #191')
            delay = 120

        table = _Table(self.project_id, dataset_id,
                       private_key=self.private_key)
        table.delete(table_id)
        table.create(table_id, table_schema)
        sleep(delay)


def _get_credentials_file():
    return os.environ.get(
        'PANDAS_GBQ_CREDENTIALS_FILE')


def _parse_data(schema, rows):
    # see:
    # http://pandas.pydata.org/pandas-docs/dev/missing_data.html
    # #missing-data-casting-rules-and-indexing
    dtype_map = {'FLOAT': np.dtype(float),
                 'TIMESTAMP': 'M8[ns]'}

    fields = schema['fields']
    col_types = [field['type'] for field in fields]
    col_names = [str(field['name']) for field in fields]
    col_dtypes = [
        dtype_map.get(field['type'].upper(), object)
        if field['mode'].lower() != 'repeated'
        else object
        for field in fields
    ]
    page_array = np.zeros((len(rows),), dtype=lzip(col_names, col_dtypes))
    for row_num, entries in enumerate(rows):
        for col_num in range(len(col_types)):
            field_value = entries[col_num]
            page_array[row_num][col_num] = field_value

    return DataFrame(page_array, columns=col_names)


def read_gbq(query, project_id=None, index_col=None, col_order=None,
             reauth=False, verbose=None, private_key=None,
             auth_local_webserver=False, dialect='legacy', **kwargs):
    r"""Load data from Google BigQuery using google-cloud-python

    The main method a user calls to execute a Query in Google BigQuery
    and read results into a pandas DataFrame.

    The Google Cloud library is used.
    Documentation is available `here
    <https://googlecloudplatform.github.io/google-cloud-python/stable/>`__

    Authentication to the Google BigQuery service is via OAuth 2.0.

    - If "private_key" is not provided:

      By default "application default credentials" are used.

      If default application credentials are not found or are restrictive,
      user account credentials are used. In this case, you will be asked to
      grant permissions for product name 'pandas GBQ'.

    - If "private_key" is provided:

      Service account credentials will be used to authenticate.

    Parameters
    ----------
    query : str
        SQL-Like Query to return data values
    project_id : str
        Google BigQuery Account project ID.
    index_col : str (optional)
        Name of result column to use for index in results DataFrame
    col_order : list(str) (optional)
        List of BigQuery column names in the desired order for results
        DataFrame
    reauth : boolean (default False)
        Force Google BigQuery to reauthenticate the user. This is useful
        if multiple accounts are used.
    private_key : str (optional)
        Service account private key in JSON format. Can be file path
        or string contents. This is useful for remote server
        authentication (eg. jupyter iPython notebook on remote host)
    auth_local_webserver : boolean, default False
        Use the [local webserver flow] instead of the [console flow] when
        getting user credentials. A file named bigquery_credentials.dat will
        be created in current dir. You can also set PANDAS_GBQ_CREDENTIALS_FILE
        environment variable so as to define a specific path to store this
        credential (eg. /etc/keys/bigquery.dat).

        .. [local webserver flow]
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_local_server
        .. [console flow]
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_console
        .. versionadded:: 0.2.0

    dialect : {'legacy', 'standard'}, default 'legacy'
        'legacy' : Use BigQuery's legacy SQL dialect.
        'standard' : Use BigQuery's standard SQL (beta), which is
        compliant with the SQL 2011 standard. For more information
        see `BigQuery SQL Reference
        <https://cloud.google.com/bigquery/sql-reference/>`__
    verbose : None, deprecated

    **kwargs : Arbitrary keyword arguments
        configuration (dict): query config parameters for job processing.
        For example:

            configuration = {'query': {'useQueryCache': False}}

        For more information see `BigQuery SQL Reference
        <https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query>`__

    Returns
    -------
    df: DataFrame
        DataFrame representing results of query

    """
    if verbose is not None:
        warnings.warn(
            "verbose is deprecated and will be removed in "
            "a future version. Set logging level in order to vary "
            "verbosity", FutureWarning, stacklevel=1)

    _test_google_api_imports()

    if not project_id:
        raise TypeError("Missing required parameter: project_id")

    if dialect not in ('legacy', 'standard'):
        raise ValueError("'{0}' is not valid for dialect".format(dialect))

    connector = GbqConnector(
        project_id, reauth=reauth, private_key=private_key,
        dialect=dialect, auth_local_webserver=auth_local_webserver)
    schema, rows = connector.run_query(query, **kwargs)
    final_df = _parse_data(schema, rows)

    # Reindex the DataFrame on the provided column
    if index_col is not None:
        if index_col in final_df.columns:
            final_df.set_index(index_col, inplace=True)
        else:
            raise InvalidIndexColumn(
                'Index column "{0}" does not exist in DataFrame.'
                .format(index_col)
            )

    # Change the order of columns in the DataFrame based on provided list
    if col_order is not None:
        if sorted(col_order) == sorted(final_df.columns):
            final_df = final_df[col_order]
        else:
            raise InvalidColumnOrder(
                'Column order does not match this DataFrame.'
            )

    # cast BOOLEAN and INTEGER columns from object to bool/int
    # if they dont have any nulls AND field mode is not repeated (i.e., array)
    type_map = {'BOOLEAN': bool, 'INTEGER': np.int64}
    for field in schema['fields']:
        if field['type'].upper() in type_map and \
                final_df[field['name']].notnull().all() and \
                field['mode'].lower() != 'repeated':
            final_df[field['name']] = \
                final_df[field['name']].astype(type_map[field['type'].upper()])

    connector.log_elapsed_seconds(
        'Total time taken',
        datetime.now().strftime('s.\nFinished at %Y-%m-%d %H:%M:%S.'),
        0
    )

    return final_df


def to_gbq(dataframe, destination_table, project_id, chunksize=None,
           verbose=None, reauth=False, if_exists='fail', private_key=None,
           auth_local_webserver=False, table_schema=None):
    """Write a DataFrame to a Google BigQuery table.

    The main method a user calls to export pandas DataFrame contents to
    Google BigQuery table.

    Google BigQuery API Client Library v2 for Python is used.
    Documentation is available `here
    <https://developers.google.com/api-client-library/python/apis/bigquery/v2>`__

    Authentication to the Google BigQuery service is via OAuth 2.0.

    - If "private_key" is not provided:

      By default "application default credentials" are used.

      If default application credentials are not found or are restrictive,
      user account credentials are used. In this case, you will be asked to
      grant permissions for product name 'pandas GBQ'.

    - If "private_key" is provided:

      Service account credentials will be used to authenticate.

    Parameters
    ----------
    dataframe : DataFrame
        DataFrame to be written
    destination_table : string
        Name of table to be written, in the form 'dataset.tablename'
    project_id : str
        Google BigQuery Account project ID.
    chunksize : int (default None)
        Number of rows to be inserted in each chunk from the dataframe. Use
        ``None`` to load the dataframe in a single chunk.
    reauth : boolean (default False)
        Force Google BigQuery to reauthenticate the user. This is useful
        if multiple accounts are used.
    if_exists : {'fail', 'replace', 'append'}, default 'fail'
        'fail': If table exists, do nothing.
        'replace': If table exists, drop it, recreate it, and insert data.
        'append': If table exists and the dataframe schema is a subset of
        the destination table schema, insert data. Create destination table
        if does not exist.
    private_key : str (optional)
        Service account private key in JSON format. Can be file path
        or string contents. This is useful for remote server
        authentication (eg. jupyter iPython notebook on remote host)
    auth_local_webserver : boolean, default False
        Use the [local webserver flow] instead of the [console flow] when
        getting user credentials.

        .. [local webserver flow]
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_local_server
        .. [console flow]
            http://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow.run_console
        .. versionadded:: 0.2.0
    table_schema : list of dicts
        List of BigQuery table fields to which according DataFrame columns
        conform to, e.g. `[{'name': 'col1', 'type': 'STRING'},...]`. If
        schema is not provided, it will be generated according to dtypes
        of DataFrame columns. See BigQuery API documentation on available
        names of a field.
        .. versionadded:: 0.3.1
    verbose : None, deprecated
    """

    _test_google_api_imports()

    if verbose is not None:
        warnings.warn(
            "verbose is deprecated and will be removed in "
            "a future version. Set logging level in order to vary "
            "verbosity", FutureWarning, stacklevel=1)

    if if_exists not in ('fail', 'replace', 'append'):
        raise ValueError("'{0}' is not valid for if_exists".format(if_exists))

    if '.' not in destination_table:
        raise NotFoundException(
            "Invalid Table Name. Should be of the form 'datasetId.tableId' ")

    connector = GbqConnector(
        project_id, reauth=reauth, private_key=private_key,
        auth_local_webserver=auth_local_webserver)
    dataset_id, table_id = destination_table.rsplit('.', 1)

    table = _Table(project_id, dataset_id, reauth=reauth,
                   private_key=private_key)

    if not table_schema:
        table_schema = _generate_bq_schema(dataframe)
    else:
        table_schema = dict(fields=table_schema)

    # If table exists, check if_exists parameter
    if table.exists(table_id):
        if if_exists == 'fail':
            raise TableCreationError("Could not create the table because it "
                                     "already exists. "
                                     "Change the if_exists parameter to "
                                     "'append' or 'replace' data.")
        elif if_exists == 'replace':
            connector.delete_and_recreate_table(
                dataset_id, table_id, table_schema)
        elif if_exists == 'append':
            if not connector.schema_is_subset(dataset_id,
                                              table_id,
                                              table_schema):
                raise InvalidSchema("Please verify that the structure and "
                                    "data types in the DataFrame match the "
                                    "schema of the destination table.")
    else:
        table.create(table_id, table_schema)

    connector.load_data(
        dataframe, dataset_id, table_id, chunksize=chunksize,
        schema=table_schema)


def generate_bq_schema(df, default_type='STRING'):
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
    warnings.warn("generate_bq_schema is deprecated and will be removed in "
                  "a future version", FutureWarning, stacklevel=2)

    return _generate_bq_schema(df, default_type=default_type)


def _generate_bq_schema(df, default_type='STRING'):
    from pandas_gbq import _schema
    return _schema.generate_bq_schema(df, default_type=default_type)


class _Table(GbqConnector):

    def __init__(self, project_id, dataset_id, reauth=False, private_key=None):
        self.dataset_id = dataset_id
        super(_Table, self).__init__(project_id, reauth, private_key)

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
            raise TableCreationError("Table {0} already "
                                     "exists".format(table_id))

        if not _Dataset(self.project_id,
                        private_key=self.private_key).exists(self.dataset_id):
            _Dataset(self.project_id,
                     private_key=self.private_key).create(self.dataset_id)

        table_ref = self.client.dataset(self.dataset_id).table(table_id)
        table = Table(table_ref)

        # Manually create the schema objects, adding NULLABLE mode
        # as a workaround for
        # https://github.com/GoogleCloudPlatform/google-cloud-python/issues/4456
        for field in schema['fields']:
            if 'mode' not in field:
                field['mode'] = 'NULLABLE'

        table.schema = [
            SchemaField.from_api_repr(field)
            for field in schema['fields']
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

    def __init__(self, project_id, reauth=False, private_key=None):
        super(_Dataset, self).__init__(project_id, reauth, private_key)

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

    def datasets(self):
        """ Return a list of datasets in Google BigQuery

        Parameters
        ----------
        None

        Returns
        -------
        list
            List of datasets under the specific project
        """

        dataset_list = []

        try:
            dataset_response = self.client.list_datasets()

            for row in dataset_response:
                dataset_list.append(row.dataset_id)

        except self.http_error as ex:
            self.process_http_error(ex)

        return dataset_list

    def create(self, dataset_id):
        """ Create a dataset in Google BigQuery

        Parameters
        ----------
        dataset : str
            Name of dataset to be written
        """
        from google.cloud.bigquery import Dataset

        if self.exists(dataset_id):
            raise DatasetCreationError("Dataset {0} already "
                                       "exists".format(dataset_id))

        dataset = Dataset(self.client.dataset(dataset_id))

        try:
            self.client.create_dataset(dataset)
        except self.http_error as ex:
            self.process_http_error(ex)

    def delete(self, dataset_id):
        """ Delete a dataset in Google BigQuery

        Parameters
        ----------
        dataset : str
            Name of dataset to be deleted
        """
        from google.api_core.exceptions import NotFound

        if not self.exists(dataset_id):
            raise NotFoundException(
                "Dataset {0} does not exist".format(dataset_id))

        try:
            self.client.delete_dataset(self.client.dataset(dataset_id))

        except NotFound:
            # Ignore 404 error which may occur if dataset already deleted
            pass
        except self.http_error as ex:
            self.process_http_error(ex)

    def tables(self, dataset_id):
        """ List tables in the specific dataset in Google BigQuery

        Parameters
        ----------
        dataset : str
            Name of dataset to list tables for

        Returns
        -------
        list
            List of tables under the specific dataset
        """

        table_list = []

        try:
            table_response = self.client.list_tables(
                self.client.dataset(dataset_id))

            for row in table_response:
                table_list.append(row.table_id)

        except self.http_error as ex:
            self.process_http_error(ex)

        return table_list
