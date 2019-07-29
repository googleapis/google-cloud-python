# -*- coding: utf-8 -*-

import copy
import datetime
from unittest import mock

import numpy
import pandas
from pandas import DataFrame
import pandas.util.testing as tm
import pkg_resources
import pytest

import pandas_gbq.exceptions
from pandas_gbq import gbq


pytestmark = pytest.mark.filter_warnings(
    "ignore:credentials from Google Cloud SDK"
)
pandas_installed_version = pkg_resources.get_distribution(
    "pandas"
).parsed_version


def _make_connector(project_id="some-project", **kwargs):
    return gbq.GbqConnector(project_id, **kwargs)


@pytest.fixture
def min_bq_version():
    import pkg_resources

    return pkg_resources.parse_version("1.9.0")


def mock_none_credentials(*args, **kwargs):
    return None, None


def mock_get_credentials_no_project(*args, **kwargs):
    import google.auth.credentials

    mock_credentials = mock.create_autospec(
        google.auth.credentials.Credentials
    )
    return mock_credentials, None


def mock_get_credentials(*args, **kwargs):
    import google.auth.credentials

    mock_credentials = mock.create_autospec(
        google.auth.credentials.Credentials
    )
    return mock_credentials, "default-project"


@pytest.fixture
def mock_service_account_credentials():
    import google.oauth2.service_account

    mock_credentials = mock.create_autospec(
        google.oauth2.service_account.Credentials
    )
    return mock_credentials


@pytest.fixture
def mock_compute_engine_credentials():
    import google.auth.compute_engine

    mock_credentials = mock.create_autospec(
        google.auth.compute_engine.Credentials
    )
    return mock_credentials


@pytest.fixture
def mock_get_user_credentials(*args, **kwargs):
    import google.auth.credentials

    mock_credentials = mock.create_autospec(
        google.auth.credentials.Credentials
    )
    return mock_credentials


@pytest.fixture(autouse=True)
def no_auth(monkeypatch):
    import pydata_google_auth

    monkeypatch.setattr(pydata_google_auth, "default", mock_get_credentials)


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        ("INTEGER", None),  # Can't handle NULL
        ("BOOLEAN", None),  # Can't handle NULL
        ("FLOAT", numpy.dtype(float)),
        # TIMESTAMP will be localized after DataFrame construction.
        ("TIMESTAMP", "datetime64[ns]"),
        ("DATETIME", "datetime64[ns]"),
    ],
)
def test__bqschema_to_nullsafe_dtypes(type_, expected):
    result = gbq._bqschema_to_nullsafe_dtypes(
        [dict(name="x", type=type_, mode="NULLABLE")]
    )
    if not expected:
        assert result == {}
    else:
        assert result == {"x": expected}


def test_GbqConnector_get_client_w_old_bq(monkeypatch, mock_bigquery_client):
    gbq._test_google_api_imports()
    connector = _make_connector()
    monkeypatch.setattr(gbq, "HAS_CLIENT_INFO", False)

    connector.get_client()

    # No client_info argument.
    mock_bigquery_client.assert_called_with(
        credentials=mock.ANY, project=mock.ANY
    )


def test_GbqConnector_get_client_w_new_bq(mock_bigquery_client):
    gbq._test_google_api_imports()
    pytest.importorskip(
        "google.cloud.bigquery", minversion=gbq.BIGQUERY_CLIENT_INFO_VERSION
    )
    pytest.importorskip("google.api_core.client_info")

    connector = _make_connector()
    connector.get_client()

    _, kwargs = mock_bigquery_client.call_args
    assert kwargs["client_info"].user_agent == "pandas-{}".format(
        pandas.__version__
    )


def test_to_gbq_should_fail_if_invalid_table_name_passed():
    with pytest.raises(gbq.NotFoundException):
        gbq.to_gbq(DataFrame([[1]]), "invalid_table_name", project_id="1234")


def test_to_gbq_with_no_project_id_given_should_fail(monkeypatch):
    import pydata_google_auth

    monkeypatch.setattr(
        pydata_google_auth, "default", mock_get_credentials_no_project
    )

    with pytest.raises(ValueError, match="Could not determine project ID"):
        gbq.to_gbq(DataFrame([[1]]), "dataset.tablename")


def test_to_gbq_with_verbose_new_pandas_warns_deprecation(min_bq_version):
    import pkg_resources

    pandas_version = pkg_resources.parse_version("0.23.0")
    with pytest.warns(FutureWarning), mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]),
                "dataset.tablename",
                project_id="my-project",
                verbose=True,
            )
        except gbq.TableCreationError:
            pass


def test_to_gbq_with_not_verbose_new_pandas_warns_deprecation(min_bq_version):
    import pkg_resources

    pandas_version = pkg_resources.parse_version("0.23.0")
    with pytest.warns(FutureWarning), mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]),
                "dataset.tablename",
                project_id="my-project",
                verbose=False,
            )
        except gbq.TableCreationError:
            pass


def test_to_gbq_wo_verbose_w_new_pandas_no_warnings(recwarn, min_bq_version):
    import pkg_resources

    pandas_version = pkg_resources.parse_version("0.23.0")
    with mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]), "dataset.tablename", project_id="my-project"
            )
        except gbq.TableCreationError:
            pass
        assert len(recwarn) == 0


def test_to_gbq_with_verbose_old_pandas_no_warnings(recwarn, min_bq_version):
    import pkg_resources

    pandas_version = pkg_resources.parse_version("0.22.0")
    with mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]),
                "dataset.tablename",
                project_id="my-project",
                verbose=True,
            )
        except gbq.TableCreationError:
            pass
        assert len(recwarn) == 0


@pytest.mark.skipif(
    pandas_installed_version < pkg_resources.parse_version("0.24.0"),
    reason="Requires pandas 0.24+",
)
def test_to_gbq_with_private_key_new_pandas_warns_deprecation(
    min_bq_version, monkeypatch
):
    import pkg_resources
    from pandas_gbq import auth

    monkeypatch.setattr(auth, "get_credentials", mock_get_credentials)

    pandas_version = pkg_resources.parse_version("0.24.0")
    with pytest.warns(FutureWarning), mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]),
                "dataset.tablename",
                project_id="my-project",
                private_key="path/to/key.json",
            )
        except gbq.TableCreationError:
            pass


def test_to_gbq_with_private_key_old_pandas_no_warnings(
    recwarn, min_bq_version, monkeypatch
):
    import pkg_resources
    from pandas_gbq import auth

    monkeypatch.setattr(auth, "get_credentials", mock_get_credentials)

    pandas_version = pkg_resources.parse_version("0.23.4")
    with mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        try:
            gbq.to_gbq(
                DataFrame([[1]]),
                "dataset.tablename",
                project_id="my-project",
                private_key="path/to/key.json",
            )
        except gbq.TableCreationError:
            pass
        assert len(recwarn) == 0


def test_to_gbq_doesnt_run_query(
    recwarn, mock_bigquery_client, min_bq_version
):
    try:
        gbq.to_gbq(
            DataFrame([[1]]), "dataset.tablename", project_id="my-project"
        )
    except gbq.TableCreationError:
        pass

    mock_bigquery_client.query.assert_not_called()


def test_read_gbq_with_no_project_id_given_should_fail(monkeypatch):
    import pydata_google_auth

    monkeypatch.setattr(
        pydata_google_auth, "default", mock_get_credentials_no_project
    )

    with pytest.raises(ValueError, match="Could not determine project ID"):
        gbq.read_gbq("SELECT 1", dialect="standard")


def test_read_gbq_with_inferred_project_id(monkeypatch):
    df = gbq.read_gbq("SELECT 1", dialect="standard")
    assert df is not None


def test_read_gbq_with_inferred_project_id_from_service_account_credentials(
    mock_bigquery_client, mock_service_account_credentials
):
    mock_service_account_credentials.project_id = "service_account_project_id"
    df = gbq.read_gbq(
        "SELECT 1",
        dialect="standard",
        credentials=mock_service_account_credentials,
    )
    assert df is not None
    mock_bigquery_client.query.assert_called_once_with(
        "SELECT 1",
        job_config=mock.ANY,
        location=None,
        project="service_account_project_id",
    )


def test_read_gbq_without_inferred_project_id_from_compute_engine_credentials(
    mock_compute_engine_credentials
):
    with pytest.raises(ValueError, match="Could not determine project ID"):
        gbq.read_gbq(
            "SELECT 1",
            dialect="standard",
            credentials=mock_compute_engine_credentials,
        )


def test_read_gbq_with_invalid_private_key_json_should_fail():
    with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
        gbq.read_gbq(
            "SELECT 1", dialect="standard", project_id="x", private_key="y"
        )


def test_read_gbq_with_empty_private_key_json_should_fail():
    with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
        gbq.read_gbq(
            "SELECT 1", dialect="standard", project_id="x", private_key="{}"
        )


def test_read_gbq_with_private_key_json_wrong_types_should_fail():
    with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
        gbq.read_gbq(
            "SELECT 1",
            dialect="standard",
            project_id="x",
            private_key='{ "client_email" : 1, "private_key" : True }',
        )


def test_read_gbq_with_empty_private_key_file_should_fail():
    with tm.ensure_clean() as empty_file_path:
        with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
            gbq.read_gbq(
                "SELECT 1",
                dialect="standard",
                project_id="x",
                private_key=empty_file_path,
            )


def test_read_gbq_with_corrupted_private_key_json_should_fail():
    with pytest.raises(pandas_gbq.exceptions.InvalidPrivateKeyFormat):
        gbq.read_gbq(
            "SELECT 1",
            dialect="standard",
            project_id="x",
            private_key="99999999999999999",
        )


def test_read_gbq_with_verbose_new_pandas_warns_deprecation(min_bq_version):
    import pkg_resources

    pandas_version = pkg_resources.parse_version("0.23.0")
    with pytest.warns(FutureWarning), mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq("SELECT 1", project_id="my-project", verbose=True)


def test_read_gbq_with_not_verbose_new_pandas_warns_deprecation(
    min_bq_version
):
    import pkg_resources

    pandas_version = pkg_resources.parse_version("0.23.0")
    with pytest.warns(FutureWarning), mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq("SELECT 1", project_id="my-project", verbose=False)


def test_read_gbq_wo_verbose_w_new_pandas_no_warnings(recwarn, min_bq_version):
    import pkg_resources

    pandas_version = pkg_resources.parse_version("0.23.0")
    with mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq("SELECT 1", project_id="my-project", dialect="standard")
        assert len(recwarn) == 0


def test_read_gbq_with_verbose_old_pandas_no_warnings(recwarn, min_bq_version):
    import pkg_resources

    pandas_version = pkg_resources.parse_version("0.22.0")
    with mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq(
            "SELECT 1",
            project_id="my-project",
            dialect="standard",
            verbose=True,
        )
        assert len(recwarn) == 0


@pytest.mark.skipif(
    pandas_installed_version < pkg_resources.parse_version("0.24.0"),
    reason="Requires pandas 0.24+",
)
def test_read_gbq_with_private_key_new_pandas_warns_deprecation(
    min_bq_version, monkeypatch
):
    import pkg_resources
    from pandas_gbq import auth

    monkeypatch.setattr(auth, "get_credentials", mock_get_credentials)

    pandas_version = pkg_resources.parse_version("0.24.0")
    with pytest.warns(FutureWarning), mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq(
            "SELECT 1", project_id="my-project", private_key="path/to/key.json"
        )


def test_read_gbq_with_private_key_old_pandas_no_warnings(
    recwarn, min_bq_version, monkeypatch
):
    import pkg_resources
    from pandas_gbq import auth

    monkeypatch.setattr(auth, "get_credentials", mock_get_credentials)

    pandas_version = pkg_resources.parse_version("0.23.4")
    with mock.patch(
        "pkg_resources.Distribution.parsed_version",
        new_callable=mock.PropertyMock,
    ) as mock_version:
        mock_version.side_effect = [min_bq_version, pandas_version]
        gbq.read_gbq(
            "SELECT 1",
            project_id="my-project",
            dialect="standard",
            private_key="path/to/key.json",
        )
        assert len(recwarn) == 0


def test_read_gbq_with_invalid_dialect():
    with pytest.raises(ValueError, match="is not valid for dialect"):
        gbq.read_gbq("SELECT 1", dialect="invalid")


def test_generate_bq_schema_deprecated():
    # 11121 Deprecation of generate_bq_schema
    with pytest.warns(FutureWarning):
        df = DataFrame([[1, "two"], [3, "four"]])
        gbq.generate_bq_schema(df)


def test_load_does_not_modify_schema_arg():
    # Test of Issue # 277
    df = DataFrame(
        {
            "field1": ["a", "b"],
            "field2": [1, 2],
            "field3": [datetime.date(2019, 1, 1), datetime.date(2019, 5, 1)],
        }
    )
    original_schema = [
        {"name": "field1", "type": "STRING", "mode": "REQUIRED"},
        {"name": "field2", "type": "INTEGER"},
        {"name": "field3", "type": "DATE"},
    ]
    original_schema_cp = copy.deepcopy(original_schema)
    gbq.to_gbq(
        df,
        "dataset.schematest",
        project_id="my-project",
        table_schema=original_schema,
        if_exists="fail",
    )
    assert original_schema == original_schema_cp

    # Test again now that table exists - behavior will differ internally
    # branch at if table.exists(table_id)
    original_schema = [
        {"name": "field1", "type": "STRING", "mode": "REQUIRED"},
        {"name": "field2", "type": "INTEGER"},
        {"name": "field3", "type": "DATE"},
    ]
    original_schema_cp = copy.deepcopy(original_schema)
    gbq.to_gbq(
        df,
        "dataset.schematest",
        project_id="my-project",
        table_schema=original_schema,
        if_exists="append",
    )
    assert original_schema == original_schema_cp
