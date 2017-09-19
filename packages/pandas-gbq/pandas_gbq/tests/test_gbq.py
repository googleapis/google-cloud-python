import pytest

import re
from datetime import datetime
import pytz
from time import sleep
import os
from random import randint
import logging

import numpy as np

from pandas import compat

from pandas.compat import u, range
from pandas import NaT, DataFrame
from pandas_gbq import gbq
import pandas.util.testing as tm
from pandas.compat.numpy import np_datetime64_compat


TABLE_ID = 'new_test'


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
    return os.environ.get('GBQ_PROJECT_ID')


def _get_private_key_path():
    if _in_travis_environment():
        return os.path.join(*[os.environ.get('TRAVIS_BUILD_DIR'), 'ci',
                              'travis_gbq.json'])
    else:
        return os.environ.get('GBQ_GOOGLE_APPLICATION_CREDENTIALS')


def _get_private_key_contents():
    key_path = _get_private_key_path()
    if key_path is None:
        return None

    with open(key_path) as f:
        return f.read()


def _test_imports():
    try:
        import pkg_resources  # noqa
    except ImportError:
        raise ImportError('Could not import pkg_resources (setuptools).')

    gbq._test_google_api_imports()


def _setup_common():
    try:
        _test_imports()
    except (ImportError, NotImplementedError) as import_exception:
        pytest.skip(str(import_exception))

    if _in_travis_environment():
        logging.getLogger('oauth2client').setLevel(logging.ERROR)
        logging.getLogger('apiclient').setLevel(logging.ERROR)


def _check_if_can_get_correct_default_credentials():
    # Checks if "Application Default Credentials" can be fetched
    # from the environment the tests are running in.
    # See https://github.com/pandas-dev/pandas/issues/13577

    import google.auth
    from google.auth.exceptions import DefaultCredentialsError

    try:
        credentials, _ = google.auth.default(scopes=[gbq.GbqConnector.scope])
    except (DefaultCredentialsError, IOError):
        return False

    return gbq._try_credentials(_get_project_id(), credentials) is not None


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

                    # Table listing is eventually consistent, so loop until
                    # all tables no longer appear (max 30 seconds).
                    table_retry = 30
                    all_tables = dataset.tables(dataset_id)
                    while all_tables and table_retry > 0:
                        for table_id in all_tables:
                            try:
                                table.delete(table_id)
                            except gbq.NotFoundException:
                                pass
                        sleep(1)
                        table_retry = table_retry - 1
                        all_tables = dataset.tables(dataset_id)

                    dataset.delete(dataset_id)
            retry = 0
        except gbq.GenericGBQException as ex:
            # Build in retry logic to work around the following errors :
            # An internal error occurred and the request could not be...
            # Dataset ... is still in use
            error_message = str(ex).lower()
            if ('an internal error occurred' in error_message or
                    'still in use' in error_message) and retry > 0:
                sleep(30)
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


class TestGBQConnectorIntegrationWithLocalUserAccountAuth(object):

    def setup_method(self, method):
        _setup_common()
        _skip_if_no_project_id()
        _skip_local_auth_if_in_travis_env()

        self.sut = gbq.GbqConnector(
            _get_project_id(), auth_local_webserver=True)

    def test_should_be_able_to_make_a_connector(self):
        assert self.sut is not None, 'Could not create a GbqConnector'

    def test_should_be_able_to_get_valid_credentials(self):
        credentials = self.sut.get_credentials()
        assert credentials.valid

    def test_should_be_able_to_get_a_bigquery_service(self):
        bigquery_service = self.sut.get_service()
        assert bigquery_service is not None

    def test_should_be_able_to_get_schema_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        assert schema is not None

    def test_should_be_able_to_get_results_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        assert pages is not None

    def test_get_application_default_credentials_does_not_throw_error(self):
        if _check_if_can_get_correct_default_credentials():
            # Can get real credentials, so mock it out to fail.
            import mock
            from google.auth.exceptions import DefaultCredentialsError
            with mock.patch('google.auth.default',
                            side_effect=DefaultCredentialsError()):
                credentials = self.sut.get_application_default_credentials()
        else:
            credentials = self.sut.get_application_default_credentials()
        assert credentials is None

    def test_get_application_default_credentials_returns_credentials(self):
        if not _check_if_can_get_correct_default_credentials():
            pytest.skip("Cannot get default_credentials "
                        "from the environment!")
        from google.auth.credentials import Credentials
        credentials = self.sut.get_application_default_credentials()
        assert isinstance(credentials, Credentials)

    def test_get_user_account_credentials_bad_file_returns_credentials(self):
        import mock
        from google.auth.credentials import Credentials
        with mock.patch('__main__.open', side_effect=IOError()):
            credentials = self.sut.get_user_account_credentials()
        assert isinstance(credentials, Credentials)

    def test_get_user_account_credentials_returns_credentials(self):
        from google.auth.credentials import Credentials
        credentials = self.sut.get_user_account_credentials()
        assert isinstance(credentials, Credentials)


class TestGBQConnectorIntegrationWithServiceAccountKeyPath(object):

    def setup_method(self, method):
        _setup_common()

        _skip_if_no_project_id()
        _skip_if_no_private_key_path()

        self.sut = gbq.GbqConnector(_get_project_id(),
                                    private_key=_get_private_key_path())

    def test_should_be_able_to_make_a_connector(self):
        assert self.sut is not None

    def test_should_be_able_to_get_valid_credentials(self):
        credentials = self.sut.get_credentials()
        assert credentials.valid

    def test_should_be_able_to_get_a_bigquery_service(self):
        bigquery_service = self.sut.get_service()
        assert bigquery_service is not None

    def test_should_be_able_to_get_schema_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        assert schema is not None

    def test_should_be_able_to_get_results_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        assert pages is not None


class TestGBQConnectorIntegrationWithServiceAccountKeyContents(object):

    def setup_method(self, method):
        _setup_common()

        _skip_if_no_project_id()
        _skip_if_no_private_key_contents()

        self.sut = gbq.GbqConnector(_get_project_id(),
                                    private_key=_get_private_key_contents())

    def test_should_be_able_to_make_a_connector(self):
        assert self.sut is not None

    def test_should_be_able_to_get_valid_credentials(self):
        credentials = self.sut.get_credentials()
        assert credentials.valid

    def test_should_be_able_to_get_a_bigquery_service(self):
        bigquery_service = self.sut.get_service()
        assert bigquery_service is not None

    def test_should_be_able_to_get_schema_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        assert schema is not None

    def test_should_be_able_to_get_results_from_query(self):
        schema, pages = self.sut.run_query('SELECT 1')
        assert pages is not None


class GBQUnitTests(object):

    def setup_method(self, method):
        _setup_common()

    def test_import_google_api_python_client(self):
        if not _in_travis_environment():
            pytest.skip("Skip if not in travis environment. Extra test to "
                        "make sure pandas_gbq doesn't break when "
                        "using google-api-python-client==1.2")

        if compat.PY2:
            with pytest.raises(ImportError):
                from googleapiclient.discovery import build  # noqa
                from googleapiclient.errors import HttpError  # noqa
            from apiclient.discovery import build  # noqa
            from apiclient.errors import HttpError  # noqa
        else:
            from googleapiclient.discovery import build  # noqa
            from googleapiclient.errors import HttpError  # noqa

    def test_should_return_credentials_path_set_by_env_var(self):
        import mock
        env = {'PANDAS_GBQ_CREDENTIALS_FILE': '/tmp/dummy.dat'}
        with mock.patch.dict('os.environ', env):
            assert gbq._get_credentials_file() == '/tmp/dummy.dat'

        assert gbq._get_credentials_file() == 'bigquery_credentials.dat'

    def test_should_return_bigquery_integers_as_python_ints(self):
        result = gbq._parse_entry(1, 'INTEGER')
        assert result == int(1)

    def test_should_return_bigquery_floats_as_python_floats(self):
        result = gbq._parse_entry(1, 'FLOAT')
        assert result == float(1)

    def test_should_return_bigquery_timestamps_as_numpy_datetime(self):
        result = gbq._parse_entry('0e9', 'TIMESTAMP')
        assert result == np_datetime64_compat('1970-01-01T00:00:00Z')

    def test_should_return_bigquery_booleans_as_python_booleans(self):
        result = gbq._parse_entry('false', 'BOOLEAN')
        assert not result

    def test_should_return_bigquery_strings_as_python_strings(self):
        result = gbq._parse_entry('STRING', 'STRING')
        assert result == 'STRING'

    def test_to_gbq_should_fail_if_invalid_table_name_passed(self):
        with pytest.raises(gbq.NotFoundException):
            gbq.to_gbq(DataFrame(), 'invalid_table_name', project_id="1234")

    def test_to_gbq_with_no_project_id_given_should_fail(self):
        with pytest.raises(TypeError):
            gbq.to_gbq(DataFrame(), 'dataset.tablename')

    def test_read_gbq_with_no_project_id_given_should_fail(self):
        with pytest.raises(TypeError):
            gbq.read_gbq('SELECT 1')

    def test_that_parse_data_works_properly(self):
        test_schema = {'fields': [
            {'mode': 'NULLABLE', 'name': 'valid_string', 'type': 'STRING'}]}
        test_page = [{'f': [{'v': 'PI'}]}]

        test_output = gbq._parse_data(test_schema, test_page)
        correct_output = DataFrame({'valid_string': ['PI']})
        tm.assert_frame_equal(test_output, correct_output)

    def test_read_gbq_with_invalid_private_key_json_should_fail(self):
        with pytest.raises(gbq.InvalidPrivateKeyFormat):
            gbq.read_gbq('SELECT 1', project_id='x', private_key='y')

    def test_read_gbq_with_empty_private_key_json_should_fail(self):
        with pytest.raises(gbq.InvalidPrivateKeyFormat):
            gbq.read_gbq('SELECT 1', project_id='x', private_key='{}')

    def test_read_gbq_with_private_key_json_wrong_types_should_fail(self):
        with pytest.raises(gbq.InvalidPrivateKeyFormat):
            gbq.read_gbq(
                'SELECT 1', project_id='x',
                private_key='{ "client_email" : 1, "private_key" : True }')

    def test_read_gbq_with_empty_private_key_file_should_fail(self):
        with tm.ensure_clean() as empty_file_path:
            with pytest.raises(gbq.InvalidPrivateKeyFormat):
                gbq.read_gbq('SELECT 1', project_id='x',
                             private_key=empty_file_path)

    def test_read_gbq_with_corrupted_private_key_json_should_fail(self):
        _skip_if_no_private_key_contents()

        with pytest.raises(gbq.InvalidPrivateKeyFormat):
            gbq.read_gbq(
                'SELECT 1', project_id='x',
                private_key=re.sub('[a-z]', '9', _get_private_key_contents()))


class TestReadGBQIntegration(object):

    @classmethod
    def setup_class(cls):
        # - GLOBAL CLASS FIXTURES -
        #   put here any instruction you want to execute only *ONCE* *BEFORE*
        #   executing *ALL* tests described below.

        _skip_if_no_project_id()

        _setup_common()

    def setup_method(self, method):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test is
        # executed.
        pass

    @classmethod
    def teardown_class(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def teardown_method(self, method):
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


class TestReadGBQIntegrationWithServiceAccountKeyPath(object):

    @classmethod
    def setup_class(cls):
        # - GLOBAL CLASS FIXTURES -
        #   put here any instruction you want to execute only *ONCE* *BEFORE*
        #   executing *ALL* tests described below.

        _skip_if_no_project_id()
        _skip_if_no_private_key_path()

        _setup_common()

    def setup_method(self, method):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test is
        # executed.
        self.gbq_connector = gbq.GbqConnector(
            _get_project_id(), private_key=_get_private_key_path())

    @classmethod
    def teardown_class(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def teardown_method(self):
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
        assert result_frame.index.name == correct_frame.index.name

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
        with pytest.raises(gbq.InvalidColumnOrder):
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
        with pytest.raises(gbq.InvalidIndexColumn):
            gbq.read_gbq(query, project_id=_get_project_id(),
                         index_col='string_bbb', col_order=col_order,
                         private_key=_get_private_key_path())

    def test_malformed_query(self):
        with pytest.raises(gbq.GenericGBQException):
            gbq.read_gbq("SELCET * FORM [publicdata:samples.shakespeare]",
                         project_id=_get_project_id(),
                         private_key=_get_private_key_path())

    def test_bad_project_id(self):
        with pytest.raises(gbq.GenericGBQException):
            gbq.read_gbq("SELECT 1", project_id='001',
                         private_key=_get_private_key_path())

    def test_bad_table_name(self):
        with pytest.raises(gbq.GenericGBQException):
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
        assert len(df.drop_duplicates()) == test_size

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
        tm.assert_frame_equal(df, expected_result)

    def test_legacy_sql(self):
        legacy_sql = "SELECT id FROM [publicdata.samples.wikipedia] LIMIT 10"

        # Test that a legacy sql statement fails when
        # setting dialect='standard'
        with pytest.raises(gbq.GenericGBQException):
            gbq.read_gbq(legacy_sql, project_id=_get_project_id(),
                         dialect='standard',
                         private_key=_get_private_key_path())

        # Test that a legacy sql statement succeeds when
        # setting dialect='legacy'
        df = gbq.read_gbq(legacy_sql, project_id=_get_project_id(),
                          dialect='legacy',
                          private_key=_get_private_key_path())
        assert len(df.drop_duplicates()) == 10

    def test_standard_sql(self):
        standard_sql = "SELECT DISTINCT id FROM " \
                       "`publicdata.samples.wikipedia` LIMIT 10"

        # Test that a standard sql statement fails when using
        # the legacy SQL dialect (default value)
        with pytest.raises(gbq.GenericGBQException):
            gbq.read_gbq(standard_sql, project_id=_get_project_id(),
                         private_key=_get_private_key_path())

        # Test that a standard sql statement succeeds when
        # setting dialect='standard'
        df = gbq.read_gbq(standard_sql, project_id=_get_project_id(),
                          dialect='standard',
                          private_key=_get_private_key_path())
        assert len(df.drop_duplicates()) == 10

    def test_invalid_option_for_sql_dialect(self):
        sql_statement = "SELECT DISTINCT id FROM " \
                        "`publicdata.samples.wikipedia` LIMIT 10"

        # Test that an invalid option for `dialect` raises ValueError
        with pytest.raises(ValueError):
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
        with pytest.raises(ValueError):
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
        with pytest.raises(ValueError):
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
        with pytest.raises(ValueError):
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
        with pytest.raises(ValueError):
            gbq.read_gbq(sql_statement, project_id=_get_project_id(),
                         private_key=_get_private_key_path(),
                         configuration=config)

    def test_timeout_configuration(self):
        sql_statement = 'SELECT 1'
        config = {
            'query': {
                "timeoutMs": 1
            }
        }
        # Test that QueryTimeout error raises
        with pytest.raises(gbq.QueryTimeout):
            gbq.read_gbq(sql_statement, project_id=_get_project_id(),
                         private_key=_get_private_key_path(),
                         configuration=config)

    def test_query_response_bytes(self):
        assert self.gbq_connector.sizeof_fmt(999) == "999.0 B"
        assert self.gbq_connector.sizeof_fmt(1024) == "1.0 KB"
        assert self.gbq_connector.sizeof_fmt(1099) == "1.1 KB"
        assert self.gbq_connector.sizeof_fmt(1044480) == "1020.0 KB"
        assert self.gbq_connector.sizeof_fmt(1048576) == "1.0 MB"
        assert self.gbq_connector.sizeof_fmt(1048576000) == "1000.0 MB"
        assert self.gbq_connector.sizeof_fmt(1073741824) == "1.0 GB"
        assert self.gbq_connector.sizeof_fmt(1.099512E12) == "1.0 TB"
        assert self.gbq_connector.sizeof_fmt(1.125900E15) == "1.0 PB"
        assert self.gbq_connector.sizeof_fmt(1.152922E18) == "1.0 EB"
        assert self.gbq_connector.sizeof_fmt(1.180592E21) == "1.0 ZB"
        assert self.gbq_connector.sizeof_fmt(1.208926E24) == "1.0 YB"
        assert self.gbq_connector.sizeof_fmt(1.208926E28) == "10000.0 YB"


class TestToGBQIntegrationWithServiceAccountKeyPath(object):
    # Changes to BigQuery table schema may take up to 2 minutes as of May 2015
    # As a workaround to this issue, each test should use a unique table name.
    # Make sure to modify the for loop range in the teardown_class when a new
    # test is added See `Issue 191
    # <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__

    @classmethod
    def setup_class(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *BEFORE*
        # executing *ALL* tests described below.

        _skip_if_no_project_id()
        _skip_if_no_private_key_path()

        _setup_common()

    def setup_method(self, method):
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
    def teardown_class(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def teardown_method(self, method):
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
        assert result['num_rows'][0] == test_size

    def test_upload_data_if_table_exists_fail(self):
        test_id = "2"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        self.table.create(TABLE_ID + test_id, gbq._generate_bq_schema(df))

        # Test the default value of if_exists is 'fail'
        with pytest.raises(gbq.TableCreationError):
            gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                       private_key=_get_private_key_path())

        # Test the if_exists parameter with value 'fail'
        with pytest.raises(gbq.TableCreationError):
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
        assert result['num_rows'][0] == test_size * 2

        # Try inserting with a different schema, confirm failure
        with pytest.raises(gbq.InvalidSchema):
            gbq.to_gbq(df_different_schema, self.destination_table + test_id,
                       _get_project_id(), if_exists='append',
                       private_key=_get_private_key_path())

    def test_upload_subset_columns_if_table_exists_append(self):
        # Issue 24: Upload is succesful if dataframe has columns
        # which are a subset of the current schema
        test_id = "16"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        df_subset_cols = df.iloc[:, :2]

        # Initialize table with sample data
        gbq.to_gbq(df, self.destination_table + test_id, _get_project_id(),
                   chunksize=10000, private_key=_get_private_key_path())

        # Test the if_exists parameter with value 'append'
        gbq.to_gbq(df_subset_cols,
                   self.destination_table + test_id, _get_project_id(),
                   if_exists='append', private_key=_get_private_key_path())

        sleep(30)  # <- Curses Google!!!

        result = gbq.read_gbq("SELECT COUNT(*) AS num_rows FROM {0}"
                              .format(self.destination_table + test_id),
                              project_id=_get_project_id(),
                              private_key=_get_private_key_path())
        assert result['num_rows'][0] == test_size * 2

    # This test is currently failing intermittently due to changes in the
    # BigQuery backend. You can track the issue in the Google BigQuery issue
    # tracker `here <https://issuetracker.google.com/issues/64329577>`__.
    # Currently you need to stream data twice in order to successfully stream
    # data when you delete and re-create a table with a different schema.
    # Something to consider is that google-cloud-bigquery returns an array of
    # streaming insert errors rather than raising an exception. In this
    # scenario, a decision could be made by the user to check for streaming
    # errors and retry as needed. See `Issue 75
    # <https://github.com/pydata/pandas-gbq/issues/75>`__
    @pytest.mark.xfail(reason="Delete/create table w/ different schema issue")
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
        assert result['num_rows'][0] == 5

    def test_upload_data_if_table_exists_raises_value_error(self):
        test_id = "4"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)

        # Test invalid value for if_exists parameter raises value error
        with pytest.raises(ValueError):
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

        with pytest.raises(gbq.StreamingInsertError):
            gbq.to_gbq(bad_df, self.destination_table + test_id,
                       _get_project_id(), private_key=_get_private_key_path())

    def test_generate_schema(self):
        df = tm.makeMixedDataFrame()
        schema = gbq._generate_bq_schema(df)

        test_schema = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                  {'name': 'B', 'type': 'FLOAT'},
                                  {'name': 'C', 'type': 'STRING'},
                                  {'name': 'D', 'type': 'TIMESTAMP'}]}

        assert schema == test_schema

    def test_create_table(self):
        test_id = "6"
        schema = gbq._generate_bq_schema(tm.makeMixedDataFrame())
        self.table.create(TABLE_ID + test_id, schema)
        assert self.table.exists(TABLE_ID + test_id)

    def test_create_table_already_exists(self):
        test_id = "6"
        schema = gbq._generate_bq_schema(tm.makeMixedDataFrame())
        self.table.create(TABLE_ID + test_id, schema)
        with pytest.raises(gbq.TableCreationError):
            self.table.create(TABLE_ID + test_id, schema)

    def test_table_does_not_exist(self):
        test_id = "7"
        assert not self.table.exists(TABLE_ID + test_id)

    def test_delete_table(self):
        test_id = "8"
        test_schema = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                  {'name': 'B', 'type': 'FLOAT'},
                                  {'name': 'C', 'type': 'STRING'},
                                  {'name': 'D', 'type': 'TIMESTAMP'}]}
        self.table.create(TABLE_ID + test_id, test_schema)
        self.table.delete(TABLE_ID + test_id)
        assert not self.table.exists(
            TABLE_ID + test_id)

    def test_delete_table_not_found(self):
        with pytest.raises(gbq.NotFoundException):
            self.table.delete(TABLE_ID + "not_found")

    def test_list_table(self):
        test_id = "9"
        test_schema = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                  {'name': 'B', 'type': 'FLOAT'},
                                  {'name': 'C', 'type': 'STRING'},
                                  {'name': 'D', 'type': 'TIMESTAMP'}]}
        self.table.create(TABLE_ID + test_id, test_schema)
        assert TABLE_ID + test_id in self.dataset.tables(
            self.dataset_prefix + "1")

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
        assert self.sut.verify_schema(
            self.dataset_prefix + "1", TABLE_ID + test_id, test_schema_2)

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
        assert not self.sut.verify_schema(self.dataset_prefix + "1",
                                          TABLE_ID + test_id, test_schema_2)

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
        assert not self.sut.verify_schema(
            self.dataset_prefix + "1", TABLE_ID + test_id, test_schema_2)

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
        assert self.sut.verify_schema(
            self.dataset_prefix + "1", TABLE_ID + test_id, test_schema_2)

    def test_retrieve_schema(self):
        # Issue #24 schema function returns the schema in biquery
        test_id = "15"
        test_schema = {'fields': [{'name': 'A', 'type': 'FLOAT'},
                                  {'name': 'B', 'type': 'FLOAT'},
                                  {'name': 'C', 'type': 'STRING'},
                                  {'name': 'D', 'type': 'TIMESTAMP'}]}

        self.table.create(TABLE_ID + test_id, test_schema)
        actual = self.sut.schema(self.dataset_prefix + "1", TABLE_ID + test_id)
        expected = test_schema['fields']
        assert expected == actual, 'Expected schema used to create table'

    def test_schema_is_subset_passes_if_subset(self):
        # Issue #24 schema_is_subset indicates whether the schema of the
        # dataframe is a subset of the schema of the bigquery table
        test_id = '16'

        table_name = TABLE_ID + test_id
        dataset = self.dataset_prefix + '1'

        table_schema = {'fields': [{'name': 'A',
                                    'type': 'FLOAT'},
                                   {'name': 'B',
                                    'type': 'FLOAT'},
                                   {'name': 'C',
                                    'type': 'STRING'}]}
        tested_schema = {'fields': [{'name': 'A',
                                     'type': 'FLOAT'},
                                    {'name': 'B',
                                     'type': 'FLOAT'}]}

        self.table.create(table_name, table_schema)

        assert self.sut.schema_is_subset(
            dataset, table_name, tested_schema) is True

    def test_schema_is_subset_fails_if_not_subset(self):
        # For pull request #24
        test_id = '17'

        table_name = TABLE_ID + test_id
        dataset = self.dataset_prefix + '1'

        table_schema = {'fields': [{'name': 'A',
                                    'type': 'FLOAT'},
                                   {'name': 'B',
                                    'type': 'FLOAT'},
                                   {'name': 'C',
                                    'type': 'STRING'}]}
        tested_schema = {'fields': [{'name': 'A',
                                     'type': 'FLOAT'},
                                    {'name': 'C',
                                     'type': 'FLOAT'}]}

        self.table.create(table_name, table_schema)

        assert self.sut.schema_is_subset(
            dataset, table_name, tested_schema) is False

    def test_list_dataset(self):
        dataset_id = self.dataset_prefix + "1"
        assert dataset_id in self.dataset.datasets()

    def test_list_table_zero_results(self):
        dataset_id = self.dataset_prefix + "2"
        self.dataset.create(dataset_id)
        table_list = gbq._Dataset(_get_project_id(),
                                  private_key=_get_private_key_path()
                                  ).tables(dataset_id)
        assert len(table_list) == 0

    def test_create_dataset(self):
        dataset_id = self.dataset_prefix + "3"
        self.dataset.create(dataset_id)
        assert dataset_id in self.dataset.datasets()

    def test_create_dataset_already_exists(self):
        dataset_id = self.dataset_prefix + "3"
        self.dataset.create(dataset_id)
        with pytest.raises(gbq.DatasetCreationError):
            self.dataset.create(dataset_id)

    def test_delete_dataset(self):
        dataset_id = self.dataset_prefix + "4"
        self.dataset.create(dataset_id)
        self.dataset.delete(dataset_id)
        assert dataset_id not in self.dataset.datasets()

    def test_delete_dataset_not_found(self):
        dataset_id = self.dataset_prefix + "not_found"
        with pytest.raises(gbq.NotFoundException):
            self.dataset.delete(dataset_id)

    def test_dataset_exists(self):
        dataset_id = self.dataset_prefix + "5"
        self.dataset.create(dataset_id)
        assert self.dataset.exists(dataset_id)

    def create_table_data_dataset_does_not_exist(self):
        dataset_id = self.dataset_prefix + "6"
        table_id = TABLE_ID + "1"
        table_with_new_dataset = gbq._Table(_get_project_id(), dataset_id)
        df = make_mixed_dataframe_v2(10)
        table_with_new_dataset.create(table_id, gbq._generate_bq_schema(df))
        assert self.dataset.exists(dataset_id)
        assert table_with_new_dataset.exists(table_id)

    def test_dataset_does_not_exist(self):
        assert not self.dataset.exists(self.dataset_prefix + "_not_found")


class TestToGBQIntegrationWithLocalUserAccountAuth(object):
    # Changes to BigQuery table schema may take up to 2 minutes as of May 2015
    # As a workaround to this issue, each test should use a unique table name.
    # Make sure to modify the for loop range in the teardown_class when a new
    # test is added
    # See `Issue 191
    # <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__

    @classmethod
    def setup_class(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *BEFORE*
        # executing *ALL* tests described below.

        _skip_if_no_project_id()
        _skip_local_auth_if_in_travis_env()

        _setup_common()

    def setup_method(self, method):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test
        # is executed.

        gbq.GbqConnector(_get_project_id(), auth_local_webserver=True)
        self.dataset_prefix = _get_dataset_prefix_random()
        clean_gbq_environment(self.dataset_prefix)
        self.destination_table = "{0}{1}.{2}".format(self.dataset_prefix, "2",
                                                     TABLE_ID)

    @classmethod
    def teardown_class(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def teardown_method(self):
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

        assert result['num_rows'][0] == test_size


class TestToGBQIntegrationWithServiceAccountKeyContents(object):
    # Changes to BigQuery table schema may take up to 2 minutes as of May 2015
    # As a workaround to this issue, each test should use a unique table name.
    # Make sure to modify the for loop range in the teardown_class when a new
    # test is added
    # See `Issue 191
    # <https://code.google.com/p/google-bigquery/issues/detail?id=191>`__

    @classmethod
    def setup_class(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *BEFORE*
        # executing *ALL* tests described below.

        _setup_common()
        _skip_if_no_project_id()

        _skip_if_no_private_key_contents()

    def setup_method(self, method):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test
        # is executed.
        self.dataset_prefix = _get_dataset_prefix_random()
        clean_gbq_environment(self.dataset_prefix, _get_private_key_contents())
        self.destination_table = "{0}{1}.{2}".format(self.dataset_prefix, "3",
                                                     TABLE_ID)

    @classmethod
    def teardown_class(cls):
        # - GLOBAL CLASS FIXTURES -
        # put here any instruction you want to execute only *ONCE* *AFTER*
        # executing all tests.
        pass

    def teardown_method(self, method):
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
        assert result['num_rows'][0] == test_size
