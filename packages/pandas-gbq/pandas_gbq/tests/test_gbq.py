import pytest

import re
from datetime import datetime
import pytz
from time import sleep
import os
from random import randint
import logging

import numpy as np

from distutils.version import StrictVersion
from pandas import compat

from pandas.compat import u, range
from pandas import NaT, DataFrame
from pandas_gbq import gbq
import pandas.util.testing as tm
from pandas.compat.numpy import np_datetime64_compat

PROJECT_ID = None
PRIVATE_KEY_JSON_PATH = None
PRIVATE_KEY_JSON_CONTENTS = None

TABLE_ID = 'new_test'


_IMPORTS = False
_GOOGLE_API_CLIENT_INSTALLED = False
_GOOGLE_API_CLIENT_VALID_VERSION = False
_HTTPLIB2_INSTALLED = False
_SETUPTOOLS_INSTALLED = False


def _skip_if_no_project_id():
    if not _get_project_id():
        pytest.skip(
            "Cannot run integration tests without a project id")


def _skip_local_auth_if_in_travis_env():
    if _in_travis_environment():
        pytest.skip("Cannot run local auth in travis environment")


def _skip_if_no_private_key_path():
    if not _get_private_key_path():
        pytest.skip("Cannot run integration tests without a "
                    "private key json file path")


def _skip_if_no_private_key_contents():
    if not _get_private_key_contents():
        raise pytest.skip("Cannot run integration tests without a "
                          "private key json contents")


def _in_travis_environment():
    return 'TRAVIS_BUILD_DIR' in os.environ and \
           'GBQ_PROJECT_ID' in os.environ


def _get_dataset_prefix_random():
    return ''.join(['pandas_gbq_', str(randint(1, 100000))])


def _get_project_id():
    if _in_travis_environment():
        return os.environ.get('GBQ_PROJECT_ID')
    else:
        return PROJECT_ID


def _get_private_key_path():
    if _in_travis_environment():
        return os.path.join(*[os.environ.get('TRAVIS_BUILD_DIR'), 'ci',
                              'travis_gbq.json'])
    else:
        return PRIVATE_KEY_JSON_PATH


def _get_private_key_contents():
    if _in_travis_environment():
        with open(os.path.join(*[os.environ.get('TRAVIS_BUILD_DIR'), 'ci',
                                 'travis_gbq.json'])) as f:
            return f.read()
    else:
        return PRIVATE_KEY_JSON_CONTENTS


def _test_imports():
    global _GOOGLE_API_CLIENT_INSTALLED, _GOOGLE_API_CLIENT_VALID_VERSION, \
        _HTTPLIB2_INSTALLED, _SETUPTOOLS_INSTALLED

    try:
        import pkg_resources
        _SETUPTOOLS_INSTALLED = True
    except ImportError:
        _SETUPTOOLS_INSTALLED = False

    if compat.PY3:
        google_api_minimum_version = '1.4.1'
    else:
        google_api_minimum_version = '1.2.0'

    if _SETUPTOOLS_INSTALLED:
        try:
            try:
                from googleapiclient.discovery import build  # noqa
                from googleapiclient.errors import HttpError  # noqa
            except:
                from apiclient.discovery import build  # noqa
                from apiclient.errors import HttpError  # noqa

            from oauth2client.client import OAuth2WebServerFlow  # noqa
            from oauth2client.client import AccessTokenRefreshError  # noqa

            from oauth2client.file import Storage  # noqa
            from oauth2client.tools import run_flow  # noqa
            _GOOGLE_API_CLIENT_INSTALLED = True
            _GOOGLE_API_CLIENT_VERSION = pkg_resources.get_distribution(
                'google-api-python-client').version

            if (StrictVersion(_GOOGLE_API_CLIENT_VERSION) >=
                    StrictVersion(google_api_minimum_version)):
                _GOOGLE_API_CLIENT_VALID_VERSION = True

        except ImportError:
            _GOOGLE_API_CLIENT_INSTALLED = False

        try:
            import httplib2  # noqa
            _HTTPLIB2_INSTALLED = True
        except ImportError:
            _HTTPLIB2_INSTALLED = False

    if not _SETUPTOOLS_INSTALLED:
        raise ImportError('Could not import pkg_resources (setuptools).')

    if not _GOOGLE_API_CLIENT_INSTALLED:
        raise ImportError('Could not import Google API Client.')

    if not _GOOGLE_API_CLIENT_VALID_VERSION:
        raise ImportError("pandas requires google-api-python-client >= {0} "
                          "for Google BigQuery support, "
                          "current version {1}"
                          .format(google_api_minimum_version,
                                  _GOOGLE_API_CLIENT_VERSION))

    if not _HTTPLIB2_INSTALLED:
        raise ImportError(
            "pandas requires httplib2 for Google BigQuery support")

    # Bug fix for https://github.com/pandas-dev/pandas/issues/12572
    # We need to know that a supported version of oauth2client is installed
    # Test that either of the following is installed:
    # - SignedJwtAssertionCredentials from oauth2client.client
    # - ServiceAccountCredentials from oauth2client.service_account
    # SignedJwtAssertionCredentials is available in oauthclient < 2.0.0
    # ServiceAccountCredentials is available in oauthclient >= 2.0.0
    oauth2client_v1 = True
    oauth2client_v2 = True

    try:
        from oauth2client.client import SignedJwtAssertionCredentials  # noqa
    except ImportError:
        oauth2client_v1 = False

    try:
        from oauth2client.service_account import ServiceAccountCredentials  # noqa
    except ImportError:
        oauth2client_v2 = False

    if not oauth2client_v1 and not oauth2client_v2:
        raise ImportError("Missing oauth2client required for BigQuery "
                          "service account support")


def _setup_common():
    try:
        _test_imports()
    except (ImportError, NotImplementedError) as import_exception:
        pytest.skip(import_exception)

    if _in_travis_environment():
        logging.getLogger('oauth2client').setLevel(logging.ERROR)
        logging.getLogger('apiclient').setLevel(logging.ERROR)


def _check_if_can_get_correct_default_credentials():
    # Checks if "Application Default Credentials" can be fetched
    # from the environment the tests are running in.
    # See Issue #13577

    import httplib2
    try:
        from googleapiclient.discovery import build
    except ImportError:
        from apiclient.discovery import build
    try:
        from oauth2client.client import GoogleCredentials
        credentials = GoogleCredentials.get_application_default()
        http = httplib2.Http()
        http = credentials.authorize(http)
        bigquery_service = build('bigquery', 'v2', http=http)
        jobs = bigquery_service.jobs()
        job_data = {'configuration': {'query': {'query': 'SELECT 1'}}}
        jobs.insert(projectId=_get_project_id(), body=job_data).execute()
        return True
    except:
        return False


def clean_gbq_environment(dataset_prefix, private_key=None):
    dataset = gbq._Dataset(_get_project_id(), private_key=private_key)
    all_datasets = dataset.datasets()

    retry = 3
    while retry > 0:
        try:
            retry = retry - 1
            for i in range(1, 10):
                dataset_id = dataset_prefix + str(i)
                if dataset_id in all_datasets:
                    table = gbq._Table(_get_project_id(), dataset_id,
                                       private_key=private_key)
                    all_tables = dataset.tables(dataset_id)
                    for table_id in all_tables:
                        table.delete(table_id)

                    dataset.delete(dataset_id)
            retry = 0
        except gbq.GenericGBQException as ex:
            # Build in retry logic to work around the following error :
            # An internal error occurred and the request could not be...
            if 'An internal error occurred' in ex.message and retry > 0:
                pass
            else:
                raise ex


def make_mixed_dataframe_v2(test_size):
    # create df to test for all BQ datatypes except RECORD
    bools = np.random.randint(2, size=(1, test_size)).astype(bool)
    flts = np.random.randn(1, test_size)
    ints = np.random.randint(1, 10, size=(1, test_size))
    strs = np.random.randint(1, 10, size=(1, test_size)).astype(str)
    times = [datetime.now(pytz.timezone('US/Arizona'))
             for t in range(test_size)]
    return DataFrame({'bools': bools[0],
                      'flts': flts[0],
                      'ints': ints[0],
                      'strs': strs[0],
                      'times': times[0]},
                     index=range(test_size))


def test_generate_bq_schema_deprecated():
    # 11121 Deprecation of generate_bq_schema
    with tm.assert_produces_warning(FutureWarning):
        df = make_mixed_dataframe_v2(10)
        gbq.generate_bq_schema(df)


class TestGBQConnectorIntegrationWithLocalUserAccountAuth(tm.TestCase):

    def setUp(self):
        _setup_common()
        _skip_if_no_project_id()
        _skip_local_auth_if_in_travis_env()

        self.sut = gbq.GbqConnector(_get_project_id())

    def test_should_be_able_to_make_a_connector(self):
        self.assertTrue(self.sut is not None,
                        'Could not create a GbqConnector')

    def test_should_be_able_to_get_valid_credentials(self):
        credentials = self.sut.get_credentials()
        self.assertFalse(credentials.invalid, 'Returned credentials invalid')

    def test_should_be_able_to_get_a_bigquery_service(self):
        bigquery_service = self.sut.get_service()
        self.assertTrue(bigquery_service is not None, 'No service returned')

    def test_should_be_able_to_get_schema_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        self.assertTrue(schema is not None)

    def test_should_be_able_to_get_results_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        self.assertTrue(pages is not None)

    def test_get_application_default_credentials_does_not_throw_error(self):
        if _check_if_can_get_correct_default_credentials():
            pytest.skip("Can get default_credentials "
                        "from the environment!")
        credentials = self.sut.get_application_default_credentials()
        self.assertIsNone(credentials)

    def test_get_application_default_credentials_returns_credentials(self):
        if not _check_if_can_get_correct_default_credentials():
            pytest.skip("Cannot get default_credentials "
                        "from the environment!")
        from oauth2client.client import GoogleCredentials
        credentials = self.sut.get_application_default_credentials()
        self.assertTrue(isinstance(credentials, GoogleCredentials))


class TestGBQConnectorIntegrationWithServiceAccountKeyPath(tm.TestCase):
    def setUp(self):
        _setup_common()

        _skip_if_no_project_id()
        _skip_if_no_private_key_path()

        self.sut = gbq.GbqConnector(_get_project_id(),
                                    private_key=_get_private_key_path())

    def test_should_be_able_to_make_a_connector(self):
        self.assertTrue(self.sut is not None,
                        'Could not create a GbqConnector')

    def test_should_be_able_to_get_valid_credentials(self):
        credentials = self.sut.get_credentials()
        self.assertFalse(credentials.invalid, 'Returned credentials invalid')

    def test_should_be_able_to_get_a_bigquery_service(self):
        bigquery_service = self.sut.get_service()
        self.assertTrue(bigquery_service is not None, 'No service returned')

    def test_should_be_able_to_get_schema_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        self.assertTrue(schema is not None)

    def test_should_be_able_to_get_results_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        self.assertTrue(pages is not None)


class TestGBQConnectorIntegrationWithServiceAccountKeyContents(tm.TestCase):
    def setUp(self):
        _setup_common()

        _skip_if_no_project_id()
        _skip_if_no_private_key_contents()

        self.sut = gbq.GbqConnector(_get_project_id(),
                                    private_key=_get_private_key_contents())

    def test_should_be_able_to_make_a_connector(self):
        self.assertTrue(self.sut is not None,
                        'Could not create a GbqConnector')

    def test_should_be_able_to_get_valid_credentials(self):
        credentials = self.sut.get_credentials()
        self.assertFalse(credentials.invalid, 'Returned credentials invalid')

    def test_should_be_able_to_get_a_bigquery_service(self):
        bigquery_service = self.sut.get_service()
        self.assertTrue(bigquery_service is not None, 'No service returned')

    def test_should_be_able_to_get_schema_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        self.assertTrue(schema is not None)

    def test_should_be_able_to_get_results_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        self.assertTrue(pages is not None)


class GBQUnitTests(tm.TestCase):

    def setUp(self):
        _setup_common()

    def test_import_google_api_python_client(self):
        if not _in_travis_environment():
            pytest.skip("Skip if not in travis environment. Extra test to "
                        "make sure pandas_gbq doesn't break when "
                        "using google-api-python-client==1.2")

        if compat.PY2:
            with tm.assertRaises(ImportError):
                from googleapiclient.discovery import build  # noqa
                from googleapiclient.errors import HttpError  # noqa
            from apiclient.discovery import build  # noqa
            from apiclient.errors import HttpError  # noqa
        else:
            from googleapiclient.discovery import build  # noqa
            from googleapiclient.errors import HttpError  # noqa

    def test_should_return_bigquery_integers_as_python_ints(self):
        result = gbq._parse_entry(1, 'INTEGER')
        tm.assert_equal(result, int(1))

    def test_should_return_bigquery_floats_as_python_floats(self):
        result = gbq._parse_entry(1, 'FLOAT')
        tm.assert_equal(result, float(1))

    def test_should_return_bigquery_timestamps_as_numpy_datetime(self):
        result = gbq._parse_entry('0e9', 'TIMESTAMP')
        tm.assert_equal(result, np_datetime64_compat('1970-01-01T00:00:00Z'))

    def test_should_return_bigquery_booleans_as_python_booleans(self):
        result = gbq._parse_entry('false', 'BOOLEAN')
        tm.assert_equal(result, False)

    def test_should_return_bigquery_strings_as_python_strings(self):
        result = gbq._parse_entry('STRING', 'STRING')
        tm.assert_equal(result, 'STRING')

    def test_to_gbq_should_fail_if_invalid_table_name_passed(self):
        with tm.assertRaises(gbq.NotFoundException):
            gbq.to_gbq(DataFrame(), 'invalid_table_name', project_id="1234")

    def test_to_gbq_with_no_project_id_given_should_fail(self):
        with tm.assertRaises(TypeError):
            gbq.to_gbq(DataFrame(), 'dataset.tablename')

    def test_read_gbq_with_no_project_id_given_should_fail(self):
        with tm.assertRaises(TypeError):
            gbq.read_gbq('SELECT 1')

    def test_that_parse_data_works_properly(self):
        test_schema = {'fields': [
            {'mode': 'NULLABLE', 'name': 'valid_string', 'type': 'STRING'}]}
        test_page = [{'f': [{'v': 'PI'}]}]

        test_output = gbq._parse_data(test_schema, test_page)
        correct_output = DataFrame({'valid_string': ['PI']})
        tm.assert_frame_equal(test_output, correct_output)

    def test_read_gbq_with_invalid_private_key_json_should_fail(self):
        with tm.assertRaises(gbq.InvalidPrivateKeyFormat):
            gbq.read_gbq('SELECT 1', project_id='x', private_key='y')

    def test_read_gbq_with_empty_private_key_json_should_fail(self):
        with tm.assertRaises(gbq.InvalidPrivateKeyFormat):
            gbq.read_gbq('SELECT 1', project_id='x', private_key='{}')

    def test_read_gbq_with_private_key_json_wrong_types_should_fail(self):
        with tm.assertRaises(gbq.InvalidPrivateKeyFormat):
            gbq.read_gbq(
                'SELECT 1', project_id='x',
                private_key='{ "client_email" : 1, "private_key" : True }')

    def test_read_gbq_with_empty_private_key_file_should_fail(self):
        with tm.ensure_clean() as empty_file_path:
            with tm.assertRaises(gbq.InvalidPrivateKeyFormat):
                gbq.read_gbq('SELECT 1', project_id='x',
                             private_key=empty_file_path)

    def test_read_gbq_with_corrupted_private_key_json_should_fail(self):
        _skip_if_no_private_key_contents()

        with tm.assertRaises(gbq.InvalidPrivateKeyFormat):
            gbq.read_gbq(
                'SELECT 1', project_id='x',
                private_key=re.sub('[a-z]', '9', _get_private_key_contents()))


class TestReadGBQIntegration(tm.TestCase):

    @classmethod
    def setUpClass(cls):
        # - GLOBAL CLASS FIXTURES -
        #   put here any instruction you want to execute only *ONCE* *BEFORE*
        #   executing *ALL* tests described below.

        _skip_if_no_project_id()

        _setup_common()

    def setUp(self):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test is
        # executed.
        pass

    @classmethod
    def tearDownClass(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def tearDown(self):
        # - PER-TEST FIXTURES -
        # put here any instructions you want to be run *AFTER* *EVERY* test is
        # executed.
        pass

    def test_should_read_as_user_account(self):
        _skip_local_auth_if_in_travis_env()

        query = 'SELECT "PI" AS valid_string'
        df = gbq.read_gbq(query, project_id=_get_project_id())
        tm.assert_frame_equal(df, DataFrame({'valid_string': ['PI']}))

    def test_should_read_as_service_account_with_key_path(self):
        _skip_if_no_private_key_path()
        query = 'SELECT "PI" AS valid_string'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'valid_string': ['PI']}))

    def test_should_read_as_service_account_with_key_contents(self):
        _skip_if_no_private_key_contents()
        query = 'SELECT "PI" AS valid_string'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_contents())
        tm.assert_frame_equal(df, DataFrame({'valid_string': ['PI']}))


class TestReadGBQIntegrationWithServiceAccountKeyPath(tm.TestCase):

    @classmethod
    def setUpClass(cls):
        # - GLOBAL CLASS FIXTURES -
        #   put here any instruction you want to execute only *ONCE* *BEFORE*
        #   executing *ALL* tests described below.

        _skip_if_no_project_id()
        _skip_if_no_private_key_path()

        _setup_common()

    def setUp(self):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test is
        # executed.
        self.gbq_connector = gbq.GbqConnector(
            _get_project_id(), private_key=_get_private_key_path())

    @classmethod
    def tearDownClass(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def tearDown(self):
        # - PER-TEST FIXTURES -
        # put here any instructions you want to be run *AFTER* *EVERY* test is
        # executed.
        pass

    def test_should_properly_handle_valid_strings(self):
        query = 'SELECT "PI" AS valid_string'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'valid_string': ['PI']}))

    def test_should_properly_handle_empty_strings(self):
        query = 'SELECT "" AS empty_string'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'empty_string': [""]}))

    def test_should_properly_handle_null_strings(self):
        query = 'SELECT STRING(NULL) AS null_string'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'null_string': [None]}))

    def test_should_properly_handle_valid_integers(self):
        query = 'SELECT INTEGER(3) AS valid_integer'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'valid_integer': [3]}))

    def test_should_properly_handle_nullable_integers(self):
        query = '''SELECT * FROM
                    (SELECT 1 AS nullable_integer),
                    (SELECT NULL AS nullable_integer)'''
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(
            df, DataFrame({'nullable_integer': [1, None]}).astype(object))

    def test_should_properly_handle_valid_longs(self):
        query = 'SELECT 1 << 62 AS valid_long'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(
            df, DataFrame({'valid_long': [1 << 62]}))

    def test_should_properly_handle_nullable_longs(self):
        query = '''SELECT * FROM
                    (SELECT 1 << 62 AS nullable_long),
                    (SELECT NULL AS nullable_long)'''
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(
            df, DataFrame({'nullable_long': [1 << 62, None]}).astype(object))

    def test_should_properly_handle_null_integers(self):
        query = 'SELECT INTEGER(NULL) AS null_integer'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'null_integer': [None]}))

    def test_should_properly_handle_valid_floats(self):
        from math import pi
        query = 'SELECT PI() AS valid_float'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame(
            {'valid_float': [pi]}))

    def test_should_properly_handle_nullable_floats(self):
        from math import pi
        query = '''SELECT * FROM
                    (SELECT PI() AS nullable_float),
                    (SELECT NULL AS nullable_float)'''
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(
            df, DataFrame({'nullable_float': [pi, None]}))

    def test_should_properly_handle_valid_doubles(self):
        from math import pi
        query = 'SELECT PI() * POW(10, 307) AS valid_double'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame(
            {'valid_double': [pi * 10 ** 307]}))

    def test_should_properly_handle_nullable_doubles(self):
        from math import pi
        query = '''SELECT * FROM
                    (SELECT PI() * POW(10, 307) AS nullable_double),
                    (SELECT NULL AS nullable_double)'''
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(
            df, DataFrame({'nullable_double': [pi * 10 ** 307, None]}))

    def test_should_properly_handle_null_floats(self):
        query = 'SELECT FLOAT(NULL) AS null_float'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'null_float': [np.nan]}))

    def test_should_properly_handle_timestamp_unix_epoch(self):
        query = 'SELECT TIMESTAMP("1970-01-01 00:00:00") AS unix_epoch'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame(
            {'unix_epoch': [np.datetime64('1970-01-01T00:00:00.000000Z')]}))

    def test_should_properly_handle_arbitrary_timestamp(self):
        query = 'SELECT TIMESTAMP("2004-09-15 05:00:00") AS valid_timestamp'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({
            'valid_timestamp': [np.datetime64('2004-09-15T05:00:00.000000Z')]
        }))

    def test_should_properly_handle_null_timestamp(self):
        query = 'SELECT TIMESTAMP(NULL) AS null_timestamp'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'null_timestamp': [NaT]}))

    def test_should_properly_handle_true_boolean(self):
        query = 'SELECT BOOLEAN(TRUE) AS true_boolean'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'true_boolean': [True]}))

    def test_should_properly_handle_false_boolean(self):
        query = 'SELECT BOOLEAN(FALSE) AS false_boolean'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'false_boolean': [False]}))

    def test_should_properly_handle_null_boolean(self):
        query = 'SELECT BOOLEAN(NULL) AS null_boolean'
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, DataFrame({'null_boolean': [None]}))

    def test_should_properly_handle_nullable_booleans(self):
        query = '''SELECT * FROM
                    (SELECT BOOLEAN(TRUE) AS nullable_boolean),
                    (SELECT NULL AS nullable_boolean)'''
        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(
            df, DataFrame({'nullable_boolean': [True, None]}).astype(object))

    def test_unicode_string_conversion_and_normalization(self):
        correct_test_datatype = DataFrame(
            {'unicode_string': [u("\xe9\xfc")]}
        )

        unicode_string = "\xc3\xa9\xc3\xbc"

        if compat.PY3:
            unicode_string = unicode_string.encode('latin-1').decode('utf8')

        query = 'SELECT "{0}" AS unicode_string'.format(unicode_string)

        df = gbq.read_gbq(query, project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        tm.assert_frame_equal(df, correct_test_datatype)

    def test_index_column(self):
        query = "SELECT 'a' AS string_1, 'b' AS string_2"
        result_frame = gbq.read_gbq(query, project_id=_get_project_id(),
                                    index_col="string_1",
                                    private_key=_get_private_key_path())
        correct_frame = DataFrame(
            {'string_1': ['a'], 'string_2': ['b']}).set_index("string_1")
        tm.assert_equal(result_frame.index.name, correct_frame.index.name)

    def test_column_order(self):
        query = "SELECT 'a' AS string_1, 'b' AS string_2, 'c' AS string_3"
        col_order = ['string_3', 'string_1', 'string_2']
        result_frame = gbq.read_gbq(query, project_id=_get_project_id(),
                                    col_order=col_order,
                                    private_key=_get_private_key_path())
        correct_frame = DataFrame({'string_1': ['a'], 'string_2': [
                                  'b'], 'string_3': ['c']})[col_order]
        tm.assert_frame_equal(result_frame, correct_frame)

    def test_read_gbq_raises_invalid_column_order(self):
        query = "SELECT 'a' AS string_1, 'b' AS string_2, 'c' AS string_3"
        col_order = ['string_aaa', 'string_1', 'string_2']

        # Column string_aaa does not exist. Should raise InvalidColumnOrder
        with tm.assertRaises(gbq.InvalidColumnOrder):
            gbq.read_gbq(query, project_id=_get_project_id(),
                         col_order=col_order,
                         private_key=_get_private_key_path())

    def test_column_order_plus_index(self):
        query = "SELECT 'a' AS string_1, 'b' AS string_2, 'c' AS string_3"
        col_order = ['string_3', 'string_2']
        result_frame = gbq.read_gbq(query, project_id=_get_project_id(),
                                    index_col='string_1', col_order=col_order,
                                    private_key=_get_private_key_path())
        correct_frame = DataFrame(
            {'string_1': ['a'], 'string_2': ['b'], 'string_3': ['c']})
        correct_frame.set_index('string_1', inplace=True)
        correct_frame = correct_frame[col_order]
        tm.assert_frame_equal(result_frame, correct_frame)

    def test_read_gbq_raises_invalid_index_column(self):
        query = "SELECT 'a' AS string_1, 'b' AS string_2, 'c' AS string_3"
        col_order = ['string_3', 'string_2']

        # Column string_bbb does not exist. Should raise InvalidIndexColumn
        with tm.assertRaises(gbq.InvalidIndexColumn):
            gbq.read_gbq(query, project_id=_get_project_id(),
                         index_col='string_bbb', col_order=col_order,
                         private_key=_get_private_key_path())

    def test_malformed_query(self):
        with tm.assertRaises(gbq.GenericGBQException):
            gbq.read_gbq("SELCET * FORM [publicdata:samples.shakespeare]",
                         project_id=_get_project_id(),
                         private_key=_get_private_key_path())

    def test_bad_project_id(self):
        with tm.assertRaises(gbq.GenericGBQException):
            gbq.read_gbq("SELECT 1", project_id='001',
                         private_key=_get_private_key_path())

    def test_bad_table_name(self):
        with tm.assertRaises(gbq.GenericGBQException):
            gbq.read_gbq("SELECT * FROM [publicdata:samples.nope]",
                         project_id=_get_project_id(),
                         private_key=_get_private_key_path())

    def test_download_dataset_larger_than_200k_rows(self):
        test_size = 200005
        # Test for known BigQuery bug in datasets larger than 100k rows
        # http://stackoverflow.com/questions/19145587/bq-py-not-paging-results
        df = gbq.read_gbq("SELECT id FROM [publicdata:samples.wikipedia] "
                          "GROUP EACH BY id ORDER BY id ASC LIMIT {0}"
                          .format(test_size),
                          project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        self.assertEqual(len(df.drop_duplicates()), test_size)

    def test_zero_rows(self):
        # Bug fix for https://github.com/pandas-dev/pandas/issues/10273
        df = gbq.read_gbq("SELECT title, id, is_bot, "
                          "SEC_TO_TIMESTAMP(timestamp) ts "
                          "FROM [publicdata:samples.wikipedia] "
                          "WHERE timestamp=-9999999",
                          project_id=_get_project_id(),
                          private_key=_get_private_key_path())
        page_array = np.zeros(
            (0,), dtype=[('title', object), ('id', np.dtype(int)),
                         ('is_bot', np.dtype(bool)), ('ts', 'M8[ns]')])
        expected_result = DataFrame(
            page_array, columns=['title', 'id', 'is_bot', 'ts'])
        self.assert_frame_equal(df, expected_result)

    def test_legacy_sql(self):
        legacy_sql = "SELECT id FROM [publicdata.samples.wikipedia] LIMIT 10"

        # Test that a legacy sql statement fails when
        # setting dialect='standard'
        with tm.assertRaises(gbq.GenericGBQException):
            gbq.read_gbq(legacy_sql, project_id=_get_project_id(),
                         dialect='standard',
                         private_key=_get_private_key_path())

        # Test that a legacy sql statement succeeds when
        # setting dialect='legacy'
        df = gbq.read_gbq(legacy_sql, project_id=_get_project_id(),
                          dialect='legacy',
                          private_key=_get_private_key_path())
        self.assertEqual(len(df.drop_duplicates()), 10)

    def test_standard_sql(self):
        standard_sql = "SELECT DISTINCT id FROM " \
                       "`publicdata.samples.wikipedia` LIMIT 10"

        # Test that a standard sql statement fails when using
        # the legacy SQL dialect (default value)
        with tm.assertRaises(gbq.GenericGBQException):
            gbq.read_gbq(standard_sql, project_id=_get_project_id(),
                         private_key=_get_private_key_path())

        # Test that a standard sql statement succeeds when
        # setting dialect='standard'
        df = gbq.read_gbq(standard_sql, project_id=_get_project_id(),
                          dialect='standard',
                          private_key=_get_private_key_path())
        self.assertEqual(len(df.drop_duplicates()), 10)

    def test_invalid_option_for_sql_dialect(self):
        sql_statement = "SELECT DISTINCT id FROM " \
                        "`publicdata.samples.wikipedia` LIMIT 10"

        # Test that an invalid option for `dialect` raises ValueError
        with tm.assertRaises(ValueError):
            gbq.read_gbq(sql_statement, project_id=_get_project_id(),
                         dialect='invalid',
                         private_key=_get_private_key_path())

        # Test that a correct option for dialect succeeds
        # to make sure ValueError was due to invalid dialect
        gbq.read_gbq(sql_statement, project_id=_get_project_id(),
                     dialect='standard', private_key=_get_private_key_path())

    def test_query_with_parameters(self):
        sql_statement = "SELECT @param1 + @param2 AS valid_result"
        config = {
            'query': {
                "useLegacySql": False,
                "parameterMode": "named",
                "queryParameters": [
                    {
                        "name": "param1",
                        "parameterType": {
                            "type": "INTEGER"
                        },
                        "parameterValue": {
                            "value": 1
                        }
                    },
                    {
                        "name": "param2",
                        "parameterType": {
                            "type": "INTEGER"
                        },
                        "parameterValue": {
                            "value": 2
                        }
                    }
                ]
            }
        }
        # Test that a query that relies on parameters fails
        # when parameters are not supplied via configuration
        with tm.assertRaises(ValueError):
            gbq.read_gbq(sql_statement, project_id=_get_project_id(),
                         private_key=_get_private_key_path())

        # Test that the query is successful because we have supplied
        # the correct query parameters via the 'config' option
        df = gbq.read_gbq(sql_statement, project_id=_get_project_id(),
                          private_key=_get_private_key_path(),
                          configuration=config)
        tm.assert_frame_equal(df, DataFrame({'valid_result': [3]}))

    def test_query_inside_configuration(self):
        query_no_use = 'SELECT "PI_WRONG" AS valid_string'
        query = 'SELECT "PI" AS valid_string'
        config = {
            'query': {
                "query": query,
                "useQueryCache": False,
            }
        }
        # Test that it can't pass query both
        # inside config and as parameter
        with tm.assertRaises(ValueError):
            gbq.read_gbq(query_no_use, project_id=_get_project_id(),
                         private_key=_get_private_key_path(),
                         configuration=config)

        df = gbq.read_gbq(None, project_id=_get_project_id(),
                          private_key=_get_private_key_path(),
                          configuration=config)
        tm.assert_frame_equal(df, DataFrame({'valid_string': ['PI']}))

    def test_configuration_without_query(self):
        sql_statement = 'SELECT 1'
        config = {
            'copy': {
                "sourceTable": {
                    "projectId": _get_project_id(),
                    "datasetId": "publicdata:samples",
                    "tableId": "wikipedia"
                },
                "destinationTable": {
                    "projectId": _get_project_id(),
                    "datasetId": "publicdata:samples",
                    "tableId": "wikipedia_copied"
                },
            }
        }
        # Test that only 'query' configurations are supported
        # nor 'copy','load','extract'
        with tm.assertRaises(ValueError):
            gbq.read_gbq(sql_statement, project_id=_get_project_id(),
                         private_key=_get_private_key_path(),
                         configuration=config)

    def test_configuration_raises_value_error_with_multiple_config(self):
        sql_statement = 'SELECT 1'
        config = {
            'query': {
                "query": sql_statement,
                "useQueryCache": False,
            },
            'load': {
                "query": sql_statement,
                "useQueryCache": False,
            }
        }
        # Test that only ValueError is raised with multiple configurations
        with tm.assertRaises(ValueError):
            gbq.read_gbq(sql_statement, project_id=_get_project_id(),
                         private_key=_get_private_key_path(),
                         configuration=config)

    def test_query_response_bytes(self):
        self.assertEqual(self.gbq_connector.sizeof_fmt(999), "999.0 B")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1024), "1.0 KB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1099), "1.1 KB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1044480), "1020.0 KB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1048576), "1.0 MB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1048576000),
                         "1000.0 MB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1073741824), "1.0 GB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1.099512E12), "1.0 TB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1.125900E15), "1.0 PB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1.152922E18), "1.0 EB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1.180592E21), "1.0 ZB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1.208926E24), "1.0 YB")
        self.assertEqual(self.gbq_connector.sizeof_fmt(1.208926E28),
                         "10000.0 YB")


class TestToGBQIntegrationWithServiceAccountKeyPath(tm.TestCase):
    # Changes to BigQuery table schema may take up to 2 minutes as of May 2015
    # As a workaround to this issue, each test should use a unique table name.
    # Make sure to modify the for loop range in the tearDownClass when a new
    # test is added See `Issue 191
    # <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__

    @classmethod
    def setUpClass(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *BEFORE*
        # executing *ALL* tests described below.

        _skip_if_no_project_id()
        _skip_if_no_private_key_path()

        _setup_common()

    def setUp(self):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test is
        # executed.

        self.dataset_prefix = _get_dataset_prefix_random()
        clean_gbq_environment(self.dataset_prefix, _get_private_key_path())
        self.dataset = gbq._Dataset(_get_project_id(),
                                    private_key=_get_private_key_path())
        self.table = gbq._Table(_get_project_id(), self.dataset_prefix + "1",
                                private_key=_get_private_key_path())
        self.sut = gbq.GbqConnector(_get_project_id(),
                                    private_key=_get_private_key_path())
        self.destination_table = "{0}{1}.{2}".format(self.dataset_prefix, "1",
                                                     TABLE_ID)
        self.dataset.create(self.dataset_prefix + "1")

    @classmethod
    def tearDownClass(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def tearDown(self):
        # - PER-TEST FIXTURES -
        # put here any instructions you want to be run *AFTER* *EVERY* test is
        # executed.
        clean_gbq_environment(self.dataset_prefix, _get_private_key_path())

    def test_upload_data(self):
        test_id = "1"
        test_size = 20001
        df = make_mixed_dataframe_v2(test_size)

        gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                   chunksize=10000, private_key=_get_private_key_path())

        sleep(30)  # <- Curses Google!!!

        result = gbq.read_gbq("SELECT COUNT(*) AS num_rows FROM {0}"
                              .format(self.destination_table + test_id),
                              project_id=_get_project_id(),
                              private_key=_get_private_key_path())
        self.assertEqual(result['num_rows'][0], test_size)

    def test_upload_data_if_table_exists_fail(self):
        test_id = "2"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        self.table.create(TABLE_ID + test_id, gbq._generate_bq_schema(df))

        # Test the default value of if_exists is 'fail'
        with tm.assertRaises(gbq.TableCreationError):
            gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                       private_key=_get_private_key_path())

        # Test the if_exists parameter with value 'fail'
        with tm.assertRaises(gbq.TableCreationError):
            gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                       if_exists='fail', private_key=_get_private_key_path())

    def test_upload_data_if_table_exists_append(self):
        test_id = "3"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        df_different_schema = tm.makeMixedDataFrame()

        # Initialize table with sample data
        gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                   chunksize=10000, private_key=_get_private_key_path())

        # Test the if_exists parameter with value 'append'
        gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                   if_exists='append', private_key=_get_private_key_path())

        sleep(30)  # <- Curses Google!!!

        result = gbq.read_gbq("SELECT COUNT(*) AS num_rows FROM {0}"
                              .format(self.destination_table + test_id),
                              project_id=_get_project_id(),
                              private_key=_get_private_key_path())
        self.assertEqual(result['num_rows'][0], test_size * 2)

        # Try inserting with a different schema, confirm failure
        with tm.assertRaises(gbq.InvalidSchema):
            gbq.to_gbq(df_different_schema, self.destination_table + test_id,
                       _get_project_id(), if_exists='append',
                       private_key=_get_private_key_path())

    def test_upload_data_if_table_exists_replace(self):
        test_id = "4"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        df_different_schema = tm.makeMixedDataFrame()

        # Initialize table with sample data
        gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                   chunksize=10000, private_key=_get_private_key_path())

        # Test the if_exists parameter with the value 'replace'.
        gbq.to_gbq(df_different_schema, self.destination_table + test_id,
                   _get_project_id(), if_exists='replace',
                   private_key=_get_private_key_path())

        sleep(30)  # <- Curses Google!!!

        result = gbq.read_gbq("SELECT COUNT(*) AS num_rows FROM {0}"
                              .format(self.destination_table + test_id),
                              project_id=_get_project_id(),
                              private_key=_get_private_key_path())
        self.assertEqual(result['num_rows'][0], 5)

    def test_upload_data_if_table_exists_raises_value_error(self):
        test_id = "4"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)

        # Test invalid value for if_exists parameter raises value error
        with tm.assertRaises(ValueError):
            gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                       if_exists='xxxxx', private_key=_get_private_key_path())

    def test_google_upload_errors_should_raise_exception(self):
        raise pytest.skip("buggy test")

        test_id = "5"
        test_timestamp = datetime.now(pytz.timezone('US/Arizona'))
        bad_df = DataFrame({'bools': [False, False], 'flts': [0.0, 1.0],
                            'ints': [0, '1'], 'strs': ['a', 1],
                            'times': [test_timestamp, test_timestamp]},
                           index=range(2))

        with tm.assertRaises(gbq.StreamingInsertError):
            gbq.to_gbq(bad_df, self.destination_table + test_id,
                       _get_project_id(), private_key=_get_private_key_path())

    def test_generate_schema(self):
        df = tm.makeMixedDataFrame()
        schema = gbq._generate_bq_schema(df)

        test_schema = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                  {'name': 'B', 'type': 'FLOAT'},
                                  {'name': 'C', 'type': 'STRING'},
                                  {'name': 'D', 'type': 'TIMESTAMP'}]}

        self.assertEqual(schema, test_schema)

    def test_create_table(self):
        test_id = "6"
        schema = gbq._generate_bq_schema(tm.makeMixedDataFrame())
        self.table.create(TABLE_ID + test_id, schema)
        self.assertTrue(self.table.exists(TABLE_ID + test_id),
                        'Expected table to exist')

    def test_create_table_already_exists(self):
        test_id = "6"
        schema = gbq._generate_bq_schema(tm.makeMixedDataFrame())
        self.table.create(TABLE_ID + test_id, schema)
        with tm.assertRaises(gbq.TableCreationError):
            self.table.create(TABLE_ID + test_id, schema)

    def test_table_does_not_exist(self):
        test_id = "7"
        self.assertTrue(not self.table.exists(TABLE_ID + test_id),
                        'Expected table not to exist')

    def test_delete_table(self):
        test_id = "8"
        test_schema = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                  {'name': 'B', 'type': 'FLOAT'},
                                  {'name': 'C', 'type': 'STRING'},
                                  {'name': 'D', 'type': 'TIMESTAMP'}]}
        self.table.create(TABLE_ID + test_id, test_schema)
        self.table.delete(TABLE_ID + test_id)
        self.assertTrue(not self.table.exists(
            TABLE_ID + test_id), 'Expected table not to exist')

    def test_delete_table_not_found(self):
        with tm.assertRaises(gbq.NotFoundException):
            self.table.delete(TABLE_ID + "not_found")

    def test_list_table(self):
        test_id = "9"
        test_schema = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                  {'name': 'B', 'type': 'FLOAT'},
                                  {'name': 'C', 'type': 'STRING'},
                                  {'name': 'D', 'type': 'TIMESTAMP'}]}
        self.table.create(TABLE_ID + test_id, test_schema)
        self.assertTrue(TABLE_ID + test_id in
                        self.dataset.tables(self.dataset_prefix + "1"),
                        'Expected table list to contain table {0}'
                        .format(TABLE_ID + test_id))

    def test_verify_schema_allows_flexible_column_order(self):
        test_id = "10"
        test_schema_1 = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                    {'name': 'B', 'type': 'FLOAT'},
                                    {'name': 'C', 'type': 'STRING'},
                                    {'name': 'D', 'type': 'TIMESTAMP'}]}
        test_schema_2 = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                    {'name': 'C', 'type': 'STRING'},
                                    {'name': 'B', 'type': 'FLOAT'},
                                    {'name': 'D', 'type': 'TIMESTAMP'}]}

        self.table.create(TABLE_ID + test_id, test_schema_1)
        self.assertTrue(self.sut.verify_schema(
            self.dataset_prefix + "1", TABLE_ID + test_id, test_schema_2),
            'Expected schema to match')

    def test_verify_schema_fails_different_data_type(self):
        test_id = "11"
        test_schema_1 = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                    {'name': 'B', 'type': 'FLOAT'},
                                    {'name': 'C', 'type': 'STRING'},
                                    {'name': 'D', 'type': 'TIMESTAMP'}]}
        test_schema_2 = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                    {'name': 'B', 'type': 'STRING'},
                                    {'name': 'C', 'type': 'STRING'},
                                    {'name': 'D', 'type': 'TIMESTAMP'}]}

        self.table.create(TABLE_ID + test_id, test_schema_1)
        self.assertFalse(self.sut.verify_schema(
            self.dataset_prefix + "1", TABLE_ID + test_id, test_schema_2),
            'Expected different schema')

    def test_verify_schema_fails_different_structure(self):
        test_id = "12"
        test_schema_1 = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                    {'name': 'B', 'type': 'FLOAT'},
                                    {'name': 'C', 'type': 'STRING'},
                                    {'name': 'D', 'type': 'TIMESTAMP'}]}
        test_schema_2 = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                    {'name': 'B2', 'type': 'FLOAT'},
                                    {'name': 'C', 'type': 'STRING'},
                                    {'name': 'D', 'type': 'TIMESTAMP'}]}

        self.table.create(TABLE_ID + test_id, test_schema_1)
        self.assertFalse(self.sut.verify_schema(
            self.dataset_prefix + "1", TABLE_ID + test_id, test_schema_2),
            'Expected different schema')

    def test_upload_data_flexible_column_order(self):
        test_id = "13"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)

        # Initialize table with sample data
        gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                   chunksize=10000, private_key=_get_private_key_path())

        df_columns_reversed = df[df.columns[::-1]]

        gbq.to_gbq(df_columns_reversed, self.destination_table + test_id,
                   _get_project_id(), if_exists='append',
                   private_key=_get_private_key_path())

    def test_verify_schema_ignores_field_mode(self):
        test_id = "14"
        test_schema_1 = {'fields': [{'name': 'A',
                                     'type': 'FLOAT',
                                     'mode': 'NULLABLE'},
                                    {'name': 'B',
                                     'type': 'FLOAT',
                                     'mode': 'NULLABLE'},
                                    {'name': 'C',
                                     'type': 'STRING',
                                     'mode': 'NULLABLE'},
                                    {'name': 'D',
                                     'type': 'TIMESTAMP',
                                     'mode': 'REQUIRED'}]}
        test_schema_2 = {'fields': [{'name': 'A',
                                     'type': 'FLOAT'},
                                    {'name': 'B',
                                     'type': 'FLOAT'},
                                    {'name': 'C',
                                     'type': 'STRING'},
                                    {'name': 'D',
                                     'type': 'TIMESTAMP'}]}

        self.table.create(TABLE_ID + test_id, test_schema_1)
        self.assertTrue(self.sut.verify_schema(
            self.dataset_prefix + "1", TABLE_ID + test_id, test_schema_2),
            'Expected schema to match')

    def test_list_dataset(self):
        dataset_id = self.dataset_prefix + "1"
        self.assertTrue(dataset_id in self.dataset.datasets(),
                        'Expected dataset list to contain dataset {0}'
                        .format(dataset_id))

    def test_list_table_zero_results(self):
        dataset_id = self.dataset_prefix + "2"
        self.dataset.create(dataset_id)
        table_list = gbq._Dataset(_get_project_id(),
                                  private_key=_get_private_key_path()
                                  ).tables(dataset_id)
        self.assertEqual(len(table_list), 0,
                         'Expected gbq.list_table() to return 0')

    def test_create_dataset(self):
        dataset_id = self.dataset_prefix + "3"
        self.dataset.create(dataset_id)
        self.assertTrue(dataset_id in self.dataset.datasets(),
                        'Expected dataset to exist')

    def test_create_dataset_already_exists(self):
        dataset_id = self.dataset_prefix + "3"
        self.dataset.create(dataset_id)
        with tm.assertRaises(gbq.DatasetCreationError):
            self.dataset.create(dataset_id)

    def test_delete_dataset(self):
        dataset_id = self.dataset_prefix + "4"
        self.dataset.create(dataset_id)
        self.dataset.delete(dataset_id)
        self.assertTrue(dataset_id not in self.dataset.datasets(),
                        'Expected dataset not to exist')

    def test_delete_dataset_not_found(self):
        dataset_id = self.dataset_prefix + "not_found"
        with tm.assertRaises(gbq.NotFoundException):
            self.dataset.delete(dataset_id)

    def test_dataset_exists(self):
        dataset_id = self.dataset_prefix + "5"
        self.dataset.create(dataset_id)
        self.assertTrue(self.dataset.exists(dataset_id),
                        'Expected dataset to exist')

    def create_table_data_dataset_does_not_exist(self):
        dataset_id = self.dataset_prefix + "6"
        table_id = TABLE_ID + "1"
        table_with_new_dataset = gbq._Table(_get_project_id(), dataset_id)
        df = make_mixed_dataframe_v2(10)
        table_with_new_dataset.create(table_id, gbq._generate_bq_schema(df))
        self.assertTrue(self.dataset.exists(dataset_id),
                        'Expected dataset to exist')
        self.assertTrue(table_with_new_dataset.exists(
            table_id), 'Expected dataset to exist')

    def test_dataset_does_not_exist(self):
        self.assertTrue(not self.dataset.exists(
                        self.dataset_prefix + "_not_found"),
                        'Expected dataset not to exist')


class TestToGBQIntegrationWithLocalUserAccountAuth(tm.TestCase):
    # Changes to BigQuery table schema may take up to 2 minutes as of May 2015
    # As a workaround to this issue, each test should use a unique table name.
    # Make sure to modify the for loop range in the tearDownClass when a new
    # test is added
    # See `Issue 191
    # <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__

    @classmethod
    def setUpClass(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *BEFORE*
        # executing *ALL* tests described below.

        _skip_if_no_project_id()
        _skip_local_auth_if_in_travis_env()

        _setup_common()

    def setUp(self):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test
        # is executed.

        self.dataset_prefix = _get_dataset_prefix_random()
        clean_gbq_environment(self.dataset_prefix)
        self.destination_table = "{0}{1}.{2}".format(self.dataset_prefix, "2",
                                                     TABLE_ID)

    @classmethod
    def tearDownClass(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def tearDown(self):
        # - PER-TEST FIXTURES -
        # put here any instructions you want to be run *AFTER* *EVERY* test
        # is executed.
        clean_gbq_environment(self.dataset_prefix, _get_private_key_path())

    def test_upload_data(self):
        test_id = "1"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)

        gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                   chunksize=10000)

        sleep(30)  # <- Curses Google!!!

        result = gbq.read_gbq("SELECT COUNT(*) AS num_rows FROM {0}".format(
            self.destination_table + test_id),
            project_id=_get_project_id())

        self.assertEqual(result['num_rows'][0], test_size)


class TestToGBQIntegrationWithServiceAccountKeyContents(tm.TestCase):
    # Changes to BigQuery table schema may take up to 2 minutes as of May 2015
    # As a workaround to this issue, each test should use a unique table name.
    # Make sure to modify the for loop range in the tearDownClass when a new
    # test is added
    # See `Issue 191
    # <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__

    @classmethod
    def setUpClass(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *BEFORE*
        # executing *ALL* tests described below.

        _setup_common()
        _skip_if_no_project_id()

        _skip_if_no_private_key_contents()

    def setUp(self):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test
        # is executed.
        self.dataset_prefix = _get_dataset_prefix_random()
        clean_gbq_environment(self.dataset_prefix, _get_private_key_contents())
        self.destination_table = "{0}{1}.{2}".format(self.dataset_prefix, "3",
                                                     TABLE_ID)

    @classmethod
    def tearDownClass(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def tearDown(self):
        # - PER-TEST FIXTURES -
        # put here any instructions you want to be run *AFTER* *EVERY* test
        # is executed.
        clean_gbq_environment(self.dataset_prefix, _get_private_key_contents())

    def test_upload_data(self):
        test_id = "1"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)

        gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                   chunksize=10000, private_key=_get_private_key_contents())

        sleep(30)  # <- Curses Google!!!

        result = gbq.read_gbq("SELECT COUNT(*) as num_rows FROM {0}".format(
            self.destination_table + test_id),
            project_id=_get_project_id(),
            private_key=_get_private_key_contents())
        self.assertEqual(result['num_rows'][0], test_size)
