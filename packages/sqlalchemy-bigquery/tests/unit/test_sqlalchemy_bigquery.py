# Copyright 2021 The sqlalchemy-bigquery Authors
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import base64
import json
from unittest import mock

import google.api_core.exceptions
import google.auth
import google.auth.credentials
import google.auth.exceptions
import pytest
import sqlalchemy
from google.cloud import bigquery
from google.cloud.bigquery.dataset import DatasetListItem
from google.cloud.bigquery.table import TableListItem
from google.oauth2 import service_account
from sqlalchemy.engine.url import make_url

import sqlalchemy_bigquery

from .conftest import setup_table


@pytest.fixture
def mock_bigquery_client():
    return mock.create_autospec(bigquery.Client, instance=True)


@pytest.fixture
def mock_connection(monkeypatch, mock_bigquery_client):
    import sqlalchemy_bigquery

    def mock_connect_args(*args, **kwargs):
        return ([mock_bigquery_client], {})

    monkeypatch.setattr(
        sqlalchemy_bigquery.BigQueryDialect, "create_connect_args", mock_connect_args
    )


@pytest.fixture
def engine_under_test(mock_connection):
    return sqlalchemy.create_engine("bigquery://")


@pytest.fixture
def inspector_under_test(engine_under_test):
    from sqlalchemy.engine.reflection import Inspector

    return Inspector.from_engine(engine_under_test)


def dataset_item(dataset_id):
    return DatasetListItem(
        {"datasetReference": {"projectId": "some-project-id", "datasetId": dataset_id}}
    )


def table_item(dataset_id, table_id, type_="TABLE"):
    return TableListItem(
        {
            "type": type_,
            "tableReference": {
                "projectId": "some-project-id",
                "datasetId": dataset_id,
                "tableId": table_id,
            },
        }
    )


@pytest.mark.parametrize(
    ["datasets_list", "tables_lists", "expected"],
    [
        ([], [], []),
        ([dataset_item("dataset_1")], [[]], []),
        (
            [dataset_item("dataset_1"), dataset_item("dataset_2")],
            [
                [table_item("dataset_1", "d1t1"), table_item("dataset_1", "d1t2")],
                [
                    table_item("dataset_2", "d2t1"),
                    table_item("dataset_2", "d2view", type_="VIEW"),
                    table_item("dataset_2", "d2ext", type_="EXTERNAL"),
                    table_item("dataset_2", "d2mv", type_="MATERIALIZED_VIEW"),
                ],
            ],
            ["dataset_1.d1t1", "dataset_1.d1t2", "dataset_2.d2t1", "dataset_2.d2ext"],
        ),
        (
            [dataset_item("dataset_1"), dataset_item("dataset_deleted")],
            [
                [table_item("dataset_1", "d1t1")],
                google.api_core.exceptions.NotFound("dataset_deleted"),
            ],
            ["dataset_1.d1t1"],
        ),
    ],
)
def test_get_table_names(
    engine_under_test, mock_bigquery_client, datasets_list, tables_lists, expected
):
    mock_bigquery_client.list_datasets.return_value = datasets_list
    mock_bigquery_client.list_tables.side_effect = tables_lists
    table_names = sqlalchemy.inspect(engine_under_test).get_table_names()
    mock_bigquery_client.list_datasets.assert_called_once()
    assert mock_bigquery_client.list_tables.call_count == len(datasets_list)
    assert list(sorted(table_names)) == list(sorted(expected))


@pytest.mark.parametrize(
    ["datasets_list", "tables_lists", "expected"],
    [
        ([], [], []),
        ([dataset_item("dataset_1")], [[]], []),
        (
            [dataset_item("dataset_1"), dataset_item("dataset_2")],
            [
                [
                    table_item("dataset_1", "d1t1"),
                    table_item("dataset_1", "d1view", type_="VIEW"),
                ],
                [
                    table_item("dataset_2", "d2t1"),
                    table_item("dataset_2", "d2view", type_="VIEW"),
                    table_item("dataset_2", "d2ext", type_="EXTERNAL"),
                    table_item("dataset_2", "d2mv", type_="MATERIALIZED_VIEW"),
                ],
            ],
            ["dataset_1.d1view", "dataset_2.d2view", "dataset_2.d2mv"],
        ),
        (
            [dataset_item("dataset_1"), dataset_item("dataset_deleted")],
            [
                [table_item("dataset_1", "d1view", type_="VIEW")],
                google.api_core.exceptions.NotFound("dataset_deleted"),
            ],
            ["dataset_1.d1view"],
        ),
    ],
)
def test_get_view_names(
    inspector_under_test, mock_bigquery_client, datasets_list, tables_lists, expected
):
    mock_bigquery_client.list_datasets.return_value = datasets_list
    mock_bigquery_client.list_tables.side_effect = tables_lists
    view_names = inspector_under_test.get_view_names()
    mock_bigquery_client.list_datasets.assert_called_once()
    assert mock_bigquery_client.list_tables.call_count == len(datasets_list)
    assert list(sorted(view_names)) == list(sorted(expected))


@pytest.mark.parametrize(
    "inp, outp",
    [
        ("(NULL IN UNNEST([ NULL) AND (1 != 1 ]))", "(NULL IN(NULL) AND (1 != 1))"),
        (
            "(NULL IN UNNEST([ NULL) AND (1 != 1:INT64 ]))",
            "(NULL IN(NULL) AND (1 != 1))",
        ),
        (
            "(NULL IN UNNEST([ (NULL, NULL)) AND (1 != 1:INT64 ]))",
            "(NULL IN((NULL, NULL)) AND (1 != 1))",
        ),
    ],
)
def test__remove_type_from_empty_in(inp, outp):
    from sqlalchemy_bigquery.base import BigQueryExecutionContext

    r = BigQueryExecutionContext._BigQueryExecutionContext__remove_type_from_empty_in
    assert r(None, inp) == outp


def test_multi_value_insert(faux_conn, last_query):
    table = setup_table(faux_conn, "t", sqlalchemy.Column("id", sqlalchemy.Integer))
    faux_conn.execute(table.insert().values([dict(id=i) for i in range(3)]))

    last_query(
        "INSERT INTO `t` (`id`) VALUES"
        " (%(id_m0:INT64)s), (%(id_m1:INT64)s), (%(id_m2:INT64)s)",
        {"id_m0": 0, "id_m1": 1, "id_m2": 2},
    )


def test_follow_dialect_attribute_convention():
    import sqlalchemy_bigquery.base

    assert sqlalchemy_bigquery.dialect is sqlalchemy_bigquery.BigQueryDialect
    assert sqlalchemy_bigquery.base.dialect is sqlalchemy_bigquery.BigQueryDialect


@pytest.mark.parametrize(
    "args,kw,error",
    [
        ((), {}, "The unnest function requires a single argument."),
        ((1, 1), {}, "The unnest function requires a single argument."),
        ((1,), {"expr": 1}, "The unnest function requires a single argument."),
        ((1, 1), {"expr": 1}, "The unnest function requires a single argument."),
        (
            (),
            {"expr": sqlalchemy.Column("x", sqlalchemy.String)},
            "The argument to unnest must have an ARRAY type.",
        ),
        (
            (sqlalchemy.Column("x", sqlalchemy.String),),
            {},
            "The argument to unnest must have an ARRAY type.",
        ),
    ],
)
def test_unnest_function_errors(args, kw, error):
    # Make sure the unnest function is registered with SQLAlchemy, which
    # happens when sqlalchemy_bigquery is imported.
    import sqlalchemy_bigquery  # noqa

    with pytest.raises(TypeError, match=error):
        sqlalchemy.func.unnest(*args, **kw)


@pytest.mark.parametrize(
    "args,kw",
    [
        ((), {"expr": sqlalchemy.Column("x", sqlalchemy.ARRAY(sqlalchemy.String))}),
        ((sqlalchemy.Column("x", sqlalchemy.ARRAY(sqlalchemy.String)),), {}),
    ],
)
def test_unnest_function(args, kw):
    # Make sure the unnest function is registered with SQLAlchemy, which
    # happens when sqlalchemy_bigquery is imported.
    import sqlalchemy_bigquery  # noqa

    f = sqlalchemy.func.unnest(*args, **kw)
    assert isinstance(f.type, sqlalchemy.String)
    assert isinstance(sqlalchemy.select(f).subquery().c.unnest.type, sqlalchemy.String)


@mock.patch("sqlalchemy_bigquery._helpers.create_bigquery_client")
def test_setting_user_supplied_client_skips_creating_client(
    mock_create_bigquery_client,
):
    import sqlalchemy_bigquery  # noqa

    result = sqlalchemy_bigquery.BigQueryDialect().create_connect_args(
        mock.MagicMock(database=None, query={"user_supplied_client": "true"})
    )
    assert result == ([], {})
    assert not mock_create_bigquery_client.called


def test_do_execute():
    # Ensures the do_execute() method overrides that of the parent class.
    import sqlalchemy_bigquery  # noqa
    from sqlalchemy_bigquery.base import BigQueryExecutionContext

    job_config_kwargs = {}
    job_config_kwargs["use_query_cache"] = False
    job_config = bigquery.QueryJobConfig(**job_config_kwargs)
    execution_options = {"job_config": job_config}
    context = mock.MagicMock(spec=BigQueryExecutionContext)
    type(context).execution_options = mock.PropertyMock(return_value=execution_options)

    cursor = mock.MagicMock()

    sqlalchemy_bigquery.BigQueryDialect().do_execute(
        cursor, sqlalchemy.text("SELECT 'a' AS `1`"), mock.MagicMock(), context=context
    )

    assert cursor.execute.call_args.kwargs["job_config"] is job_config


class _FakeServiceAccountCredentials(google.auth.credentials.AnonymousCredentials):
    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id

    def with_scopes(self, scopes):
        return self


def _patch_service_account_credentials(monkeypatch, project_id):
    creds = _FakeServiceAccountCredentials(project_id)
    mock_sa = mock.create_autospec(service_account.Credentials)
    mock_sa.from_service_account_info.return_value = creds
    mock_sa.from_service_account_file.return_value = creds
    monkeypatch.setattr(service_account, "Credentials", mock_sa)


def _raise_no_ambient_adc(*args, **kwargs):
    raise google.auth.exceptions.DefaultCredentialsError("ambient ADC unavailable")


_TENANT_A_CREDENTIALS_INFO = {
    "type": "service_account",
    "project_id": "tenant-a-project",
}
_TENANT_A_CREDENTIALS_BASE64 = base64.b64encode(
    json.dumps(_TENANT_A_CREDENTIALS_INFO).encode()
).decode()


@pytest.mark.parametrize(
    "dialect_kwargs,url_str",
    [
        (
            {"credentials_info": _TENANT_A_CREDENTIALS_INFO},
            "bigquery:///tenant_dataset",
        ),
        (
            {"credentials_path": "path/to/tenant-key.json"},
            "bigquery:///tenant_dataset",
        ),
        (
            {},
            f"bigquery:///tenant_dataset?credentials_base64={_TENANT_A_CREDENTIALS_BASE64}",
        ),
    ],
    ids=["credentials_info", "credentials_path", "credentials_base64"],
)
def test_create_connect_args_uses_explicit_credentials_project_for_default_dataset(
    monkeypatch, dialect_kwargs, url_str
):
    _patch_service_account_credentials(monkeypatch, "tenant-a-project")
    monkeypatch.setattr(google.auth, "default", _raise_no_ambient_adc)
    dialect = sqlalchemy_bigquery.BigQueryDialect(**dialect_kwargs)

    _, kwargs = dialect.create_connect_args(make_url(url_str))

    assert kwargs[
        "client"
    ].default_query_job_config.default_dataset == bigquery.DatasetReference(
        "tenant-a-project", "tenant_dataset"
    )


def test_create_connect_args_uses_billing_project_for_unqualified_dataset(monkeypatch):
    _patch_service_account_credentials(monkeypatch, "tenant-a-project")
    monkeypatch.setattr(google.auth, "default", _raise_no_ambient_adc)
    dialect = sqlalchemy_bigquery.BigQueryDialect(
        credentials_info=_TENANT_A_CREDENTIALS_INFO,
        billing_project_id="billing-project",
    )

    _, kwargs = dialect.create_connect_args(make_url("bigquery:///tenant_dataset"))

    job_config = kwargs["client"].default_query_job_config
    assert job_config.default_dataset == bigquery.DatasetReference(
        "billing-project", "tenant_dataset"
    )
    assert job_config.connection_properties == []


def test_create_connect_args_sets_dataset_project_for_remote_dataset(monkeypatch):
    _patch_service_account_credentials(monkeypatch, "tenant-a-project")
    monkeypatch.setattr(google.auth, "default", _raise_no_ambient_adc)
    dialect = sqlalchemy_bigquery.BigQueryDialect(
        credentials_info=_TENANT_A_CREDENTIALS_INFO,
        billing_project_id="billing-project",
    )

    _, kwargs = dialect.create_connect_args(
        make_url("bigquery://data-project/tenant_dataset")
    )

    job_config = kwargs["client"].default_query_job_config
    assert job_config.default_dataset == bigquery.DatasetReference(
        "data-project", "tenant_dataset"
    )
    assert [(prop.key, prop.value) for prop in job_config.connection_properties] == [
        ("dataset_project_id", "data-project")
    ]


def test_setting_user_supplied_client_with_dataset_skips_ambient_adc(monkeypatch):
    monkeypatch.setattr(
        sqlalchemy_bigquery._helpers,
        "create_bigquery_client",
        mock.MagicMock(side_effect=AssertionError("should not create client")),
    )
    monkeypatch.setattr(google.auth, "default", _raise_no_ambient_adc)

    result = sqlalchemy_bigquery.BigQueryDialect().create_connect_args(
        make_url("bigquery:///tenant_dataset?user_supplied_client=true")
    )

    assert result == ([], {})


def test_create_job_config_falls_back_to_auth_default_when_project_unset(monkeypatch):
    monkeypatch.setattr(google.auth, "default", lambda: ("creds", "default-project"))
    dialect = sqlalchemy_bigquery.BigQueryDialect()
    dialect.dataset_id = "tenant_dataset"

    job_config = dialect.create_job_config(None)

    assert job_config.default_dataset == bigquery.DatasetReference(
        "default-project", "tenant_dataset"
    )
