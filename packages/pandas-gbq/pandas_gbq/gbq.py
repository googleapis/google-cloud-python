import warnings
from datetime import datetime
import json
from time import sleep
import uuid
import time
import sys
import os

import numpy as np

from distutils.version import StrictVersion
from pandas import compat, DataFrame, concat
from pandas.compat import lzip, bytes_to_str


def _check_google_client_version():

    try:
        import pkg_resources

    except ImportError:
        raise ImportError('Could not import pkg_resources (setuptools).')

    # Version 1.6.0 is the first version to support google-auth.
    # https://github.com/google/google-api-python-client/blob/master/CHANGELOG
    google_api_minimum_version = '1.6.0'

    _GOOGLE_API_CLIENT_VERSION = pkg_resources.get_distribution(
        'google-api-python-client').version

    if (StrictVersion(_GOOGLE_API_CLIENT_VERSION) <
            StrictVersion(google_api_minimum_version)):
        raise ImportError('pandas requires google-api-python-client >= {0} '
                          'for Google BigQuery support, '
                          'current version {1}'
                          .format(google_api_minimum_version,
                                  _GOOGLE_API_CLIENT_VERSION))


def _test_google_api_imports():

    try:
        import httplib2  # noqa
    except ImportError as ex:
        raise ImportError(
            'pandas requires httplib2 for Google BigQuery support: '
            '{0}'.format(ex))

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow  # noqa
    except ImportError as ex:
        raise ImportError(
            'pandas requires google-auth-oauthlib for Google BigQuery '
            'support: {0}'.format(ex))

    try:
        from google_auth_httplib2 import AuthorizedHttp  # noqa
        from google_auth_httplib2 import Request  # noqa
    except ImportError as ex:
        raise ImportError(
            'pandas requires google-auth-httplib2 for Google BigQuery '
            'support: {0}'.format(ex))

    try:
        from googleapiclient.discovery import build  # noqa
        from googleapiclient.errors import HttpError  # noqa
    except ImportError as ex:
        raise ImportError(
            "pandas requires google-api-python-client for Google BigQuery "
            "support: {0}".format(ex))

    try:
        import google.auth  # noqa
    except ImportError as ex:
        raise ImportError(
            "pandas requires google-auth for Google BigQuery support: "
            "{0}".format(ex))

    _check_google_client_version()


def _try_credentials(project_id, credentials):
    import httplib2
    from googleapiclient.discovery import build
    import googleapiclient.errors
    from google_auth_httplib2 import AuthorizedHttp

    if credentials is None:
        return None

    http = httplib2.Http()
    try:
        authed_http = AuthorizedHttp(credentials, http=http)
        bigquery_service = build('bigquery', 'v2', http=authed_http)
        # Check if the application has rights to the BigQuery project
        jobs = bigquery_service.jobs()
        job_data = {'configuration': {'query': {'query': 'SELECT 1'}}}
        jobs.insert(projectId=project_id, body=job_data).execute()
        return credentials
    except googleapiclient.errors.Error:
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


class StreamingInsertError(ValueError):
    """
    Raised when BigQuery reports a streaming insert error.
    For more information see `Streaming Data Into BigQuery
    <https://cloud.google.com/bigquery/streaming-data-into-bigquery>`__
    """


class TableCreationError(ValueError):
    """
    Raised when the create table method fails
    """
    pass


class GbqConnector(object):
    scope = 'https://www.googleapis.com/auth/bigquery'

    def __init__(self, project_id, reauth=False, verbose=False,
                 private_key=None, auth_local_webserver=False,
                 dialect='legacy'):
        self.project_id = project_id
        self.reauth = reauth
        self.verbose = verbose
        self.private_key = private_key
        self.auth_local_webserver = auth_local_webserver
        self.dialect = dialect
        self.credentials_path = _get_credentials_file()
        self.credentials = self.get_credentials()
        self.service = self.get_service()

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
        import httplib2
        from google_auth_httplib2 import Request
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
        http = httplib2.Http()
        request = Request(http)
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
            self._print('Unable to save credentials.')

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
        import httplib2
        from google_auth_httplib2 import Request
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
            http = httplib2.Http()
            request = Request(http)
            credentials.refresh(request)

            return credentials
        except (KeyError, ValueError, TypeError, AttributeError):
            raise InvalidPrivateKeyFormat(
                "Private key is missing or invalid. It should be service "
                "account private key JSON (file path or string contents) "
                "with at least two keys: 'client_email' and 'private_key'. "
                "Can be obtained from: https://console.developers.google."
                "com/permissions/serviceaccounts")

    def _print(self, msg, end='\n'):
        if self.verbose:
            sys.stdout.write(msg + end)
            sys.stdout.flush()

    def _start_timer(self):
        self.start = time.time()

    def get_elapsed_seconds(self):
        return round(time.time() - self.start, 2)

    def print_elapsed_seconds(self, prefix='Elapsed', postfix='s.',
                              overlong=7):
        sec = self.get_elapsed_seconds()
        if sec > overlong:
            self._print('{} {} {}'.format(prefix, sec, postfix))

    # http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        fmt = "%3.1f %s%s"
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return fmt % (num, unit, suffix)
            num /= 1024.0
        return fmt % (num, 'Y', suffix)

    def get_service(self):
        import httplib2
        from google_auth_httplib2 import AuthorizedHttp
        from googleapiclient.discovery import build

        http = httplib2.Http()
        authed_http = AuthorizedHttp(
            self.credentials, http=http)
        bigquery_service = build('bigquery', 'v2', http=authed_http)

        return bigquery_service

    @staticmethod
    def process_http_error(ex):
        # See `BigQuery Troubleshooting Errors
        # <https://cloud.google.com/bigquery/troubleshooting-errors>`__

        status = json.loads(bytes_to_str(ex.content))['error']
        errors = status.get('errors', None)

        if errors:
            for error in errors:
                reason = error['reason']
                message = error['message']

                raise GenericGBQException(
                    "Reason: {0}, Message: {1}".format(reason, message))

        raise GenericGBQException(errors)

    def process_insert_errors(self, insert_errors):
        for insert_error in insert_errors:
            row = insert_error['index']
            errors = insert_error.get('errors', None)
            for error in errors:
                reason = error['reason']
                message = error['message']
                location = error['location']
                error_message = ('Error at Row: {0}, Reason: {1}, '
                                 'Location: {2}, Message: {3}'
                                 .format(row, reason, location, message))

                # Report all error messages if verbose is set
                if self.verbose:
                    self._print(error_message)
                else:
                    raise StreamingInsertError(error_message +
                                               '\nEnable verbose logging to '
                                               'see all errors')

        raise StreamingInsertError

    def run_query(self, query, **kwargs):
        try:
            from googleapiclient.errors import HttpError
        except ImportError:
            from apiclient.errors import HttpError
        from google.auth.exceptions import RefreshError

        job_collection = self.service.jobs()

        job_config = {
            'query': {
                'query': query,
                'useLegacySql': self.dialect == 'legacy'
                # 'allowLargeResults', 'createDisposition',
                # 'preserveNulls', destinationTable, useQueryCache
            }
        }
        config = kwargs.get('configuration')
        if config is not None:
            if len(config) != 1:
                raise ValueError("Only one job type must be specified, but "
                                 "given {}".format(','.join(config.keys())))
            if 'query' in config:
                if 'query' in config['query'] and query is not None:
                    raise ValueError("Query statement can't be specified "
                                     "inside config while it is specified "
                                     "as parameter")

                job_config['query'].update(config['query'])
            else:
                raise ValueError("Only 'query' job type is supported")

        job_data = {
            'configuration': job_config
        }

        self._start_timer()
        try:
            self._print('Requesting query... ', end="")
            query_reply = job_collection.insert(
                projectId=self.project_id, body=job_data).execute()
            self._print('ok.')
        except (RefreshError, ValueError):
            if self.private_key:
                raise AccessDenied(
                    "The service account credentials are not valid")
            else:
                raise AccessDenied(
                    "The credentials have been revoked or expired, "
                    "please re-run the application to re-authorize")
        except HttpError as ex:
            self.process_http_error(ex)

        job_reference = query_reply['jobReference']
        job_id = job_reference['jobId']
        self._print('Job ID: %s\nQuery running...' % job_id)

        while not query_reply.get('jobComplete', False):
            self.print_elapsed_seconds('  Elapsed', 's. Waiting...')

            timeout_ms = job_config['query'].get('timeoutMs')
            if timeout_ms and timeout_ms < self.get_elapsed_seconds() * 1000:
                raise QueryTimeout('Query timeout: {} ms'.format(timeout_ms))

            try:
                query_reply = job_collection.getQueryResults(
                    projectId=job_reference['projectId'],
                    jobId=job_id).execute()
            except HttpError as ex:
                self.process_http_error(ex)

        if self.verbose:
            if query_reply['cacheHit']:
                self._print('Query done.\nCache hit.\n')
            else:
                bytes_processed = int(query_reply.get(
                    'totalBytesProcessed', '0'))
                self._print('Query done.\nProcessed: {}'.format(
                    self.sizeof_fmt(bytes_processed)))
                self._print('Standard price: ${:,.2f} USD\n'.format(
                    bytes_processed * self.query_price_for_TB))

            self._print('Retrieving results...')

        total_rows = int(query_reply['totalRows'])
        result_pages = list()
        seen_page_tokens = list()
        current_row = 0
        # Only read schema on first page
        schema = query_reply['schema']

        # Loop through each page of data
        while 'rows' in query_reply and current_row < total_rows:
            page = query_reply['rows']
            result_pages.append(page)
            current_row += len(page)

            self.print_elapsed_seconds(
                '  Got page: {}; {}% done. Elapsed'.format(
                    len(result_pages),
                    round(100.0 * current_row / total_rows)))

            if current_row == total_rows:
                break

            page_token = query_reply.get('pageToken', None)

            if not page_token and current_row < total_rows:
                raise InvalidPageToken("Required pageToken was missing. "
                                       "Received {0} of {1} rows"
                                       .format(current_row, total_rows))

            elif page_token in seen_page_tokens:
                raise InvalidPageToken("A duplicate pageToken was returned")

            seen_page_tokens.append(page_token)

            try:
                query_reply = job_collection.getQueryResults(
                    projectId=job_reference['projectId'],
                    jobId=job_id,
                    pageToken=page_token).execute()
            except HttpError as ex:
                self.process_http_error(ex)

        if current_row < total_rows:
            raise InvalidPageToken()

        # print basic query stats
        self._print('Got {} rows.\n'.format(total_rows))

        return schema, result_pages

    def load_data(self, dataframe, dataset_id, table_id, chunksize):
        try:
            from googleapiclient.errors import HttpError
        except ImportError:
            from apiclient.errors import HttpError

        job_id = uuid.uuid4().hex
        rows = []
        remaining_rows = len(dataframe)

        total_rows = remaining_rows
        self._print("\n\n")

        for index, row in dataframe.reset_index(drop=True).iterrows():
            row_dict = dict()
            row_dict['json'] = json.loads(row.to_json(force_ascii=False,
                                                      date_unit='s',
                                                      date_format='iso'))
            row_dict['insertId'] = job_id + str(index)
            rows.append(row_dict)
            remaining_rows -= 1

            if (len(rows) % chunksize == 0) or (remaining_rows == 0):
                self._print("\rStreaming Insert is {0}% Complete".format(
                    ((total_rows - remaining_rows) * 100) / total_rows))

                body = {'rows': rows}

                try:
                    response = self.service.tabledata().insertAll(
                        projectId=self.project_id,
                        datasetId=dataset_id,
                        tableId=table_id,
                        body=body).execute()
                except HttpError as ex:
                    self.process_http_error(ex)

                # For streaming inserts, even if you receive a success HTTP
                # response code, you'll need to check the insertErrors property
                # of the response to determine if the row insertions were
                # successful, because it's possible that BigQuery was only
                # partially successful at inserting the rows.  See the `Success
                # HTTP Response Codes
                # <https://cloud.google.com/bigquery/
                #       streaming-data-into-bigquery#troubleshooting>`__
                # section

                insert_errors = response.get('insertErrors', None)
                if insert_errors:
                    self.process_insert_errors(insert_errors)

                sleep(1)  # Maintains the inserts "per second" rate per API
                rows = []

        self._print("\n")

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

        try:
            from googleapiclient.errors import HttpError
        except ImportError:
            from apiclient.errors import HttpError

        try:
            remote_schema = self.service.tables().get(
                projectId=self.project_id,
                datasetId=dataset_id,
                tableId=table_id).execute()['schema']

            remote_fields = [{'name': field_remote['name'],
                              'type': field_remote['type']}
                             for field_remote in remote_schema['fields']]

            return remote_fields
        except HttpError as ex:
            self.process_http_error(ex)

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

        fields_remote = sorted(self.schema(dataset_id, table_id),
                               key=lambda x: x['name'])
        fields_local = sorted(schema['fields'], key=lambda x: x['name'])

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

        fields_remote = self.schema(dataset_id, table_id)
        fields_local = schema['fields']

        return all(field in fields_remote for field in fields_local)

    def delete_and_recreate_table(self, dataset_id, table_id, table_schema):
        delay = 0

        # Changes to table schema may take up to 2 minutes as of May 2015 See
        # `Issue 191
        # <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__
        # Compare previous schema with new schema to determine if there should
        # be a 120 second delay

        if not self.verify_schema(dataset_id, table_id, table_schema):
            self._print('The existing table has a different schema. Please '
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
    col_dtypes = [dtype_map.get(field['type'], object) for field in fields]
    page_array = np.zeros((len(rows),), dtype=lzip(col_names, col_dtypes))
    for row_num, raw_row in enumerate(rows):
        entries = raw_row.get('f', [])
        for col_num, field_type in enumerate(col_types):
            field_value = _parse_entry(entries[col_num].get('v', ''),
                                       field_type)
            page_array[row_num][col_num] = field_value

    return DataFrame(page_array, columns=col_names)


def _parse_entry(field_value, field_type):
    if field_value is None or field_value == 'null':
        return None
    if field_type == 'INTEGER':
        return int(field_value)
    elif field_type == 'FLOAT':
        return float(field_value)
    elif field_type == 'TIMESTAMP':
        timestamp = datetime.utcfromtimestamp(float(field_value))
        return np.datetime64(timestamp)
    elif field_type == 'BOOLEAN':
        return field_value == 'true'
    return field_value


def read_gbq(query, project_id=None, index_col=None, col_order=None,
             reauth=False, verbose=True, private_key=None,
             auth_local_webserver=False, dialect='legacy', **kwargs):
    r"""Load data from Google BigQuery.

    The main method a user calls to execute a Query in Google BigQuery
    and read results into a pandas DataFrame.

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
    verbose : boolean (default True)
        Verbose output
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

    _test_google_api_imports()

    if not project_id:
        raise TypeError("Missing required parameter: project_id")

    if dialect not in ('legacy', 'standard'):
        raise ValueError("'{0}' is not valid for dialect".format(dialect))

    connector = GbqConnector(
        project_id, reauth=reauth, verbose=verbose, private_key=private_key,
        dialect=dialect, auth_local_webserver=auth_local_webserver)
    schema, pages = connector.run_query(query, **kwargs)
    dataframe_list = []
    while len(pages) > 0:
        page = pages.pop()
        dataframe_list.append(_parse_data(schema, page))

    if len(dataframe_list) > 0:
        final_df = concat(dataframe_list, ignore_index=True)
    else:
        final_df = _parse_data(schema, [])

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
    # if they dont have any nulls
    type_map = {'BOOLEAN': bool, 'INTEGER': int}
    for field in schema['fields']:
        if field['type'] in type_map and \
                final_df[field['name']].notnull().all():
            final_df[field['name']] = \
                final_df[field['name']].astype(type_map[field['type']])

    connector.print_elapsed_seconds(
        'Total time taken',
        datetime.now().strftime('s.\nFinished at %Y-%m-%d %H:%M:%S.'),
        0
    )

    return final_df


def to_gbq(dataframe, destination_table, project_id, chunksize=10000,
           verbose=True, reauth=False, if_exists='fail', private_key=None,
           auth_local_webserver=False):
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
    chunksize : int (default 10000)
        Number of rows to be inserted in each chunk from the dataframe.
    verbose : boolean (default True)
        Show percentage complete
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
    """

    _test_google_api_imports()

    if if_exists not in ('fail', 'replace', 'append'):
        raise ValueError("'{0}' is not valid for if_exists".format(if_exists))

    if '.' not in destination_table:
        raise NotFoundException(
            "Invalid Table Name. Should be of the form 'datasetId.tableId' ")

    connector = GbqConnector(
        project_id, reauth=reauth, verbose=verbose, private_key=private_key,
        auth_local_webserver=auth_local_webserver)
    dataset_id, table_id = destination_table.rsplit('.', 1)

    table = _Table(project_id, dataset_id, reauth=reauth,
                   private_key=private_key)

    table_schema = _generate_bq_schema(dataframe)

    # If table exists, check if_exists parameter
    if table.exists(table_id):
        if if_exists == 'fail':
            raise TableCreationError("Could not create the table because it "
                                     "already exists. "
                                     "Change the if_exists parameter to "
                                     "append or replace data.")
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

    connector.load_data(dataframe, dataset_id, table_id, chunksize)


def generate_bq_schema(df, default_type='STRING'):
    # deprecation TimeSeries, #11121
    warnings.warn("generate_bq_schema is deprecated and will be removed in "
                  "a future version", FutureWarning, stacklevel=2)

    return _generate_bq_schema(df, default_type=default_type)


def _generate_bq_schema(df, default_type='STRING'):
    """ Given a passed df, generate the associated Google BigQuery schema.

    Parameters
    ----------
    df : DataFrame
    default_type : string
        The default big query type in case the type of the column
        does not exist in the schema.
    """

    type_mapping = {
        'i': 'INTEGER',
        'b': 'BOOLEAN',
        'f': 'FLOAT',
        'O': 'STRING',
        'S': 'STRING',
        'U': 'STRING',
        'M': 'TIMESTAMP'
    }

    fields = []
    for column_name, dtype in df.dtypes.iteritems():
        fields.append({'name': column_name,
                       'type': type_mapping.get(dtype.kind, default_type)})

    return {'fields': fields}


class _Table(GbqConnector):

    def __init__(self, project_id, dataset_id, reauth=False, verbose=False,
                 private_key=None):
        try:
            from googleapiclient.errors import HttpError
        except ImportError:
            from apiclient.errors import HttpError
        self.http_error = HttpError
        self.dataset_id = dataset_id
        super(_Table, self).__init__(project_id, reauth, verbose, private_key)

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

        try:
            self.service.tables().get(
                projectId=self.project_id,
                datasetId=self.dataset_id,
                tableId=table_id).execute()
            return True
        except self.http_error as ex:
            if ex.resp.status == 404:
                return False
            else:
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

        if self.exists(table_id):
            raise TableCreationError("Table {0} already "
                                     "exists".format(table_id))

        if not _Dataset(self.project_id,
                        private_key=self.private_key).exists(self.dataset_id):
            _Dataset(self.project_id,
                     private_key=self.private_key).create(self.dataset_id)

        body = {
            'schema': schema,
            'tableReference': {
                'tableId': table_id,
                'projectId': self.project_id,
                'datasetId': self.dataset_id
            }
        }

        try:
            self.service.tables().insert(
                projectId=self.project_id,
                datasetId=self.dataset_id,
                body=body).execute()
        except self.http_error as ex:
            self.process_http_error(ex)

    def delete(self, table_id):
        """ Delete a table in Google BigQuery

        Parameters
        ----------
        table : str
            Name of table to be deleted
        """

        if not self.exists(table_id):
            raise NotFoundException("Table does not exist")

        try:
            self.service.tables().delete(
                datasetId=self.dataset_id,
                projectId=self.project_id,
                tableId=table_id).execute()
        except self.http_error as ex:
            # Ignore 404 error which may occur if table already deleted
            if ex.resp.status != 404:
                self.process_http_error(ex)


class _Dataset(GbqConnector):

    def __init__(self, project_id, reauth=False, verbose=False,
                 private_key=None):
        try:
            from googleapiclient.errors import HttpError
        except ImportError:
            from apiclient.errors import HttpError
        self.http_error = HttpError
        super(_Dataset, self).__init__(project_id, reauth, verbose,
                                       private_key)

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

        try:
            self.service.datasets().get(
                projectId=self.project_id,
                datasetId=dataset_id).execute()
            return True
        except self.http_error as ex:
            if ex.resp.status == 404:
                return False
            else:
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
        next_page_token = None
        first_query = True

        while first_query or next_page_token:
            first_query = False

            try:
                list_dataset_response = self.service.datasets().list(
                    projectId=self.project_id,
                    pageToken=next_page_token).execute()

                dataset_response = list_dataset_response.get('datasets')
                if dataset_response is None:
                    dataset_response = []

                next_page_token = list_dataset_response.get('nextPageToken')

                if dataset_response is None:
                    dataset_response = []

                for row_num, raw_row in enumerate(dataset_response):
                    dataset_list.append(
                        raw_row['datasetReference']['datasetId'])

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

        if self.exists(dataset_id):
            raise DatasetCreationError("Dataset {0} already "
                                       "exists".format(dataset_id))

        body = {
            'datasetReference': {
                'projectId': self.project_id,
                'datasetId': dataset_id
            }
        }

        try:
            self.service.datasets().insert(
                projectId=self.project_id,
                body=body).execute()
        except self.http_error as ex:
            self.process_http_error(ex)

    def delete(self, dataset_id):
        """ Delete a dataset in Google BigQuery

        Parameters
        ----------
        dataset : str
            Name of dataset to be deleted
        """

        if not self.exists(dataset_id):
            raise NotFoundException(
                "Dataset {0} does not exist".format(dataset_id))

        try:
            self.service.datasets().delete(
                datasetId=dataset_id,
                projectId=self.project_id).execute()

        except self.http_error as ex:
            # Ignore 404 error which may occur if dataset already deleted
            if ex.resp.status != 404:
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
        next_page_token = None
        first_query = True

        while first_query or next_page_token:
            first_query = False

            try:
                list_table_response = self.service.tables().list(
                    projectId=self.project_id,
                    datasetId=dataset_id,
                    pageToken=next_page_token).execute()

                table_response = list_table_response.get('tables')
                next_page_token = list_table_response.get('nextPageToken')

                if not table_response:
                    return table_list

                for row_num, raw_row in enumerate(table_response):
                    table_list.append(raw_row['tableReference']['tableId'])

            except self.http_error as ex:
                self.process_http_error(ex)

        return table_list
