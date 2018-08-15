# -*- coding: utf-8 -*-

import pandas.util.testing as tm
import pytest
from pandas import DataFrame
from pandas.compat.numpy import np_datetime64_compat

import pandas_gbq.exceptions
from pandas_gbq import gbq

try:
    import mock
except ImportError:  # pragma: NO COVER
    from unittest import mock


@pytest.fixture
def min_bq_version():
    import pkg_resources
    return pkg_resources.parse_version('0.32.0')


@pytest.fixture(autouse=True)
def mock_bigquery_client(monkeypatch):
    from google.api_core.exceptions import NotFound
    import google.cloud.bigquery
    import google.cloud.bigquery.table
    mock_client = mock.create_autospec(google.cloud.bigquery.Client)
    mock_schema = [
        google.cloud.bigquery.SchemaField('_f0', 'INTEGER')
    ]
    # Mock out SELECT 1 query results.
    mock_query = mock.create_autospec(google.cloud.bigquery.QueryJob)
    mock_query.job_id = 'some-random-id'
    mock_query.state = 'DONE'
    mock_rows = mock.create_autospec(
        google.cloud.bigquery.table.RowIterator)
    mock_rows.total_rows = 1
    mock_rows.schema = mock_schema
    mock_rows.__iter__.return_value = [(1,)]
    mock_query.result.return_value = mock_rows
    mock_client.query.return_value = mock_query
    # Mock table creation.
    mock_client.get_table.side_effect = NotFound('nope')
    monkeypatch.setattr(
        gbq.GbqConnector, 'get_client', lambda _: mock_client)


def mock_none_credentials(*args, **kwargs):
    return None, None


def mock_get_credentials(*args, **kwargs):
    import google.auth.credentials
    mock_credentials = mock.create_autospec(
        google.auth.credentials.Credentials)
    return mock_credentials, 'default-project'


def mock_get_user_credentials(*args, **kwargs):
    import google.auth.credentials
    mock_credentials = mock.create_autospec(
        google.auth.credentials.Credentials)
    return mock_credentials


@pytest.fixture(autouse=True)
def no_auth(monkeypatch):
    from pandas_gbq import auth
    monkeypatch.setattr(
        auth, 'get_application_default_credentials', mock_get_credentials)
    monkeypatch.setattr(
        auth, 'get_user_account_credentials', mock_get_user_credentials)
    monkeypatch.setattr(
        auth, '_try_credentials', lambda project_id, credentials: credentials)


def test_should_return_credentials_path_set_by_env_var():
    env = {'PANDAS_GBQ_CREDENTIALS_FILE': '/tmp/dummy.dat'}
    with mock.patch.dict('os.environ', env):
        assert gbq._get_credentials_file() == '/tmp/dummy.dat'


@pytest.mark.parametrize(
    ('input', 'type_', 'expected'), [
        (1, 'INTEGER', int(1)),
        (1, 'FLOAT', float(1)),
        pytest.param('false', 'BOOLEAN', False, marks=pytest.mark.xfail),
        pytest.param(
            '0e9', 'TIMESTAMP',
            np_datetime64_compat('1970-01-01T00:00:00Z'),
            marks=pytest.mark.xfail),
        ('STRING', 'STRING', 'STRING'),
    ])
def test_should_return_bigquery_correctly_typed(
        input, type_, expected):
    result = gbq._parse_data(
        dict(fields=[dict(name='x', type=type_, mode='NULLABLE')]),
        rows=[[input]]).iloc[0, 0]
    assert result == expected


def test_to_gbq_should_fail_if_invalid_table_name_passed():
    with pytest.raises(gbq.NotFoundException):
        gbq.to_gbq(DataFrame([[1]]), 'invalid_table_name', project_id="1234")


def test_to_gbq_with_no_project_id_given_should_fail(monkeypatch):
    from pandas_gbq import auth
    monkeypatch.setattr(
        auth, 'get_application_default_credentials', mock_none_credentials)

    with pytest.raises(ValueError) as exception:
        gbq.to_gbq(DataFrame([[1]]), 'dataset.tablename')
    assert 'Could not determine project ID' in str(exception)


def test_to_gbq_with_verbose_new_pandas_warns_deprecation(min_bq_version):
    import pkg_resources
    pandas_version = pkg_resources.parse_version('0.23.0')
    with pytest.warns(FutureWarning), \
            mock.patch(
                'pkg_resources.Distribution.parsed_version',
                new_callable=mock.PropertyMock) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]),
                'dataset.tablename',
                project_id='my-project',
                verbose=True)
        except gbq.TableCreationError:
            pass


def test_to_gbq_with_not_verbose_new_pandas_warns_deprecation(min_bq_version):
    import pkg_resources
    pandas_version = pkg_resources.parse_version('0.23.0')
    with pytest.warns(FutureWarning), \
            mock.patch(
                'pkg_resources.Distribution.parsed_version',
                new_callable=mock.PropertyMock) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]),
                'dataset.tablename',
                project_id='my-project',
                verbose=False)
        except gbq.TableCreationError:
            pass


def test_to_gbq_wo_verbose_w_new_pandas_no_warnings(recwarn, min_bq_version):
    import pkg_resources
    pandas_version = pkg_resources.parse_version('0.23.0')
    with mock.patch(
            'pkg_resources.Distribution.parsed_version',
            new_callable=mock.PropertyMock) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]), 'dataset.tablename', project_id='my-project')
        except gbq.TableCreationError:
            pass
        assert len(recwarn) == 0


def test_to_gbq_with_verbose_old_pandas_no_warnings(recwarn, min_bq_version):
    import pkg_resources
    pandas_version = pkg_resources.parse_version('0.22.0')
    with mock.patch(
            'pkg_resources.Distribution.parsed_version',
            new_callable=mock.PropertyMock) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]),
                'dataset.tablename',
                project_id='my-project',
                verbose=True)
        except gbq.TableCreationError:
            pass
        assert len(recwarn) == 0


def test_read_gbq_with_no_project_id_given_should_fail(monkeypatch):
    from pandas_gbq import auth
    monkeypatch.setattr(
        auth, 'get_application_default_credentials', mock_none_credentials)

    with pytest.raises(ValueError) as exception:
        gbq.read_gbq('SELECT 1', dialect='standard')
    assert 'Could not determine project ID' in str(exception)


def test_read_gbq_with_inferred_project_id(monkeypatch):
    df = gbq.read_gbq('SELECT 1', dialect='standard')
    assert df is not None


def test_that_parse_data_works_properly():
    from google.cloud.bigquery.table import Row
    test_schema = {'fields': [
        {'mode': 'NULLABLE', 'name': 'column_x', 'type': 'STRING'}]}
    field_to_index = {'column_x': 0}
    values = ('row_value',)
    test_page = [Row(values, field_to_index)]

    test_output = gbq._parse_data(test_schema, test_page)
    correct_output = DataFrame({'column_x': ['row_value']})
    tm.assert_frame_equal(test_output, correct_output)


def test_read_gbq_with_invalid_private_key_json_should_fail():
    with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
        gbq.read_gbq(
            'SELECT 1', dialect='standard', project_id='x', private_key='y')


def test_read_gbq_with_empty_private_key_json_should_fail():
    with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
        gbq.read_gbq(
            'SELECT 1', dialect='standard', project_id='x', private_key='{}')


def test_read_gbq_with_private_key_json_wrong_types_should_fail():
    with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
        gbq.read_gbq(
            'SELECT 1', dialect='standard', project_id='x',
            private_key='{ "client_email" : 1, "private_key" : True }')


def test_read_gbq_with_empty_private_key_file_should_fail():
    with tm.ensure_clean() as empty_file_path:
        with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
            gbq.read_gbq('SELECT 1', dialect='standard', project_id='x',
                         private_key=empty_file_path)


def test_read_gbq_with_corrupted_private_key_json_should_fail():
    with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
        gbq.read_gbq(
            'SELECT 1', dialect='standard', project_id='x',
            private_key='99999999999999999')


def test_read_gbq_with_verbose_new_pandas_warns_deprecation(min_bq_version):
    import pkg_resources
    pandas_version = pkg_resources.parse_version('0.23.0')
    with pytest.warns(FutureWarning), \
            mock.patch(
                'pkg_resources.Distribution.parsed_version',
                new_callable=mock.PropertyMock) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq('SELECT 1', project_id='my-project', verbose=True)


def test_read_gbq_with_not_verbose_new_pandas_warns_deprecation(
        min_bq_version):
    import pkg_resources
    pandas_version = pkg_resources.parse_version('0.23.0')
    with pytest.warns(FutureWarning), \
            mock.patch(
                'pkg_resources.Distribution.parsed_version',
                new_callable=mock.PropertyMock) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq('SELECT 1', project_id='my-project', verbose=False)


def test_read_gbq_wo_verbose_w_new_pandas_no_warnings(recwarn, min_bq_version):
    import pkg_resources
    pandas_version = pkg_resources.parse_version('0.23.0')
    with mock.patch(
            'pkg_resources.Distribution.parsed_version',
            new_callable=mock.PropertyMock) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq('SELECT 1', project_id='my-project', dialect='standard')
        assert len(recwarn) == 0


def test_read_gbq_with_verbose_old_pandas_no_warnings(recwarn, min_bq_version):
    import pkg_resources
    pandas_version = pkg_resources.parse_version('0.22.0')
    with mock.patch(
            'pkg_resources.Distribution.parsed_version',
            new_callable=mock.PropertyMock) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq(
            'SELECT 1', project_id='my-project', dialect='standard',
            verbose=True)
        assert len(recwarn) == 0


def test_read_gbq_with_invalid_dialect():
    with pytest.raises(ValueError) as excinfo:
        gbq.read_gbq('SELECT 1', dialect='invalid')
    assert 'is not valid for dialect' in str(excinfo.value)


def test_read_gbq_without_dialect_warns_future_change():
    with pytest.warns(FutureWarning):
        gbq.read_gbq('SELECT 1')


def test_generate_bq_schema_deprecated():
    # 11121 Deprecation of generate_bq_schema
    with pytest.warns(FutureWarning):
        df = DataFrame([[1, 'two'], [3, 'four']])
        gbq.generate_bq_schema(df)
