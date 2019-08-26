# Copyright 2018 Google LLC
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

import copy
import re
from concurrent import futures

import mock
import pytest
import six

try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None
try:
    import IPython
    from IPython.utils import io
    from IPython.testing import tools
    from IPython.terminal import interactiveshell
except ImportError:  # pragma: NO COVER
    IPython = None

from google.api_core import exceptions
import google.auth.credentials

try:
    from google.cloud import bigquery_storage_v1beta1
except ImportError:  # pragma: NO COVER
    bigquery_storage_v1beta1 = None
from google.cloud.bigquery import job
from google.cloud.bigquery import table
from google.cloud.bigquery import magics
from tests.unit.helpers import make_connection
from test_utils.imports import maybe_fail_import


pytestmark = pytest.mark.skipif(IPython is None, reason="Requires `ipython`")


@pytest.fixture(scope="session")
def ipython():
    config = tools.default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = interactiveshell.TerminalInteractiveShell.instance(config=config)
    return shell


@pytest.fixture()
def ipython_interactive(request, ipython):
    """Activate IPython's builtin hooks

    for the duration of the test scope.
    """
    with ipython.builtin_trap:
        yield ipython


@pytest.fixture(scope="session")
def missing_bq_storage():
    """Provide a patcher that can make the bigquery storage import to fail."""

    def fail_if(name, globals, locals, fromlist, level):
        # NOTE: *very* simplified, assuming a straightforward absolute import
        return "bigquery_storage_v1beta1" in name or (
            fromlist is not None and "bigquery_storage_v1beta1" in fromlist
        )

    return maybe_fail_import(predicate=fail_if)


@pytest.fixture(scope="session")
def missing_grpcio_lib():
    """Provide a patcher that can make the gapic library import to fail."""

    def fail_if(name, globals, locals, fromlist, level):
        # NOTE: *very* simplified, assuming a straightforward absolute import
        return "gapic_v1" in name or (fromlist is not None and "gapic_v1" in fromlist)

    return maybe_fail_import(predicate=fail_if)


JOB_REFERENCE_RESOURCE = {"projectId": "its-a-project-eh", "jobId": "some-random-id"}
TABLE_REFERENCE_RESOURCE = {
    "projectId": "its-a-project-eh",
    "datasetId": "ds",
    "tableId": "persons",
}
QUERY_RESOURCE = {
    "jobReference": JOB_REFERENCE_RESOURCE,
    "configuration": {
        "query": {
            "destinationTable": TABLE_REFERENCE_RESOURCE,
            "query": "SELECT 42 FROM `life.the_universe.and_everything`;",
            "queryParameters": [],
            "useLegacySql": False,
        }
    },
    "status": {"state": "DONE"},
}


def test_context_credentials_auto_set_w_application_default_credentials():
    """When Application Default Credentials are set, the context credentials
    will be created the first time it is called
    """
    assert magics.context._credentials is None
    assert magics.context._project is None

    project = "prahj-ekt"
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, project)
    )
    with default_patch as default_mock:
        assert magics.context.credentials is credentials_mock
        assert magics.context.project == project

    assert default_mock.call_count == 2


def test_context_credentials_and_project_can_be_set_explicitly():
    project1 = "one-project-55564"
    project2 = "other-project-52569"
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, project1)
    )
    with default_patch as default_mock:
        magics.context.credentials = credentials_mock
        magics.context.project = project2

    assert magics.context.project == project2
    assert magics.context.credentials is credentials_mock
    # default should not be called if credentials & project are explicitly set
    assert default_mock.call_count == 0


@pytest.mark.usefixtures("ipython_interactive")
def test_context_connection_can_be_overriden():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context._project = None
    magics.context._credentials = None

    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    project = "project-123"
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, project)
    )
    job_reference = copy.deepcopy(JOB_REFERENCE_RESOURCE)
    job_reference["projectId"] = project

    query = "select * from persons"
    resource = copy.deepcopy(QUERY_RESOURCE)
    resource["jobReference"] = job_reference
    resource["configuration"]["query"]["query"] = query
    data = {"jobReference": job_reference, "totalRows": 0, "rows": []}

    conn = magics.context._connection = make_connection(resource, data)
    list_rows_patch = mock.patch(
        "google.cloud.bigquery.client.Client.list_rows",
        return_value=google.cloud.bigquery.table._EmptyRowIterator(),
    )
    with list_rows_patch as list_rows, default_patch:
        ip.run_cell_magic("bigquery", "", query)

    # Check that query actually starts the job.
    list_rows.assert_called()
    assert len(conn.api_request.call_args_list) == 2
    _, req = conn.api_request.call_args_list[0]
    assert req["method"] == "POST"
    assert req["path"] == "/projects/{}/jobs".format(project)
    sent = req["data"]
    assert isinstance(sent["jobReference"]["jobId"], six.string_types)
    sent_config = sent["configuration"]["query"]
    assert sent_config["query"] == query


@pytest.mark.usefixtures("ipython_interactive")
def test_context_no_connection():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context._project = None
    magics.context._credentials = None
    magics.context._connection = None

    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    project = "project-123"
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, project)
    )
    job_reference = copy.deepcopy(JOB_REFERENCE_RESOURCE)
    job_reference["projectId"] = project

    query = "select * from persons"
    resource = copy.deepcopy(QUERY_RESOURCE)
    resource["jobReference"] = job_reference
    resource["configuration"]["query"]["query"] = query
    data = {"jobReference": job_reference, "totalRows": 0, "rows": []}

    conn_mock = make_connection(resource, data, data, data)
    conn_patch = mock.patch("google.cloud.bigquery.client.Connection", autospec=True)
    list_rows_patch = mock.patch(
        "google.cloud.bigquery.client.Client.list_rows",
        return_value=google.cloud.bigquery.table._EmptyRowIterator(),
    )
    with conn_patch as conn, list_rows_patch as list_rows, default_patch:
        conn.return_value = conn_mock
        ip.run_cell_magic("bigquery", "", query)

    # Check that query actually starts the job.
    list_rows.assert_called()
    assert len(conn_mock.api_request.call_args_list) == 2
    _, req = conn_mock.api_request.call_args_list[0]
    assert req["method"] == "POST"
    assert req["path"] == "/projects/{}/jobs".format(project)
    sent = req["data"]
    assert isinstance(sent["jobReference"]["jobId"], six.string_types)
    sent_config = sent["configuration"]["query"]
    assert sent_config["query"] == query


def test__run_query():
    magics.context._credentials = None

    job_id = "job_1234"
    sql = "SELECT 17"
    responses = [
        futures.TimeoutError,
        futures.TimeoutError,
        [table.Row((17,), {"num": 0})],
    ]

    client_patch = mock.patch(
        "google.cloud.bigquery.magics.bigquery.Client", autospec=True
    )
    with client_patch as client_mock, io.capture_output() as captured:
        client_mock().query(sql).result.side_effect = responses
        client_mock().query(sql).job_id = job_id

        query_job = magics._run_query(client_mock(), sql)

    lines = re.split("\n|\r", captured.stdout)
    # Removes blanks & terminal code (result of display clearing)
    updates = list(filter(lambda x: bool(x) and x != "\x1b[2K", lines))

    assert query_job.job_id == job_id
    expected_first_line = "Executing query with job ID: {}".format(job_id)
    assert updates[0] == expected_first_line
    execution_updates = updates[1:-1]
    assert len(execution_updates) == 3  # one update per API response
    for line in execution_updates:
        assert re.match("Query executing: .*s", line)
    assert re.match("Query complete after .*s", updates[-1])


def test__run_query_dry_run_without_errors_is_silent():
    magics.context._credentials = None

    sql = "SELECT 17"

    client_patch = mock.patch(
        "google.cloud.bigquery.magics.bigquery.Client", autospec=True
    )

    job_config = job.QueryJobConfig()
    job_config.dry_run = True
    with client_patch as client_mock, io.capture_output() as captured:
        client_mock().query(sql).job_id = None
        magics._run_query(client_mock(), sql, job_config=job_config)

    assert len(captured.stderr) == 0
    assert len(captured.stdout) == 0


def test__make_bqstorage_client_false():
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    got = magics._make_bqstorage_client(False, credentials_mock)
    assert got is None


@pytest.mark.skipif(
    bigquery_storage_v1beta1 is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test__make_bqstorage_client_true():
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    got = magics._make_bqstorage_client(True, credentials_mock)
    assert isinstance(got, bigquery_storage_v1beta1.BigQueryStorageClient)


def test__make_bqstorage_client_true_raises_import_error(missing_bq_storage):
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    with pytest.raises(ImportError) as exc_context, missing_bq_storage:
        magics._make_bqstorage_client(True, credentials_mock)

    error_msg = str(exc_context.value)
    assert "google-cloud-bigquery-storage" in error_msg
    assert "pyarrow" in error_msg


def test__make_bqstorage_client_true_missing_gapic(missing_grpcio_lib):
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    with pytest.raises(ImportError) as exc_context, missing_grpcio_lib:
        magics._make_bqstorage_client(True, credentials_mock)

    assert "grpcio" in str(exc_context.value)


@pytest.mark.usefixtures("ipython_interactive")
def test_extension_load():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")

    # verify that the magic is registered and has the correct source
    magic = ip.magics_manager.magics["cell"].get("bigquery")
    assert magic.__module__ == "google.cloud.bigquery.magics"


@pytest.mark.usefixtures("ipython_interactive")
@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_bigquery_magic_without_optional_arguments(missing_bq_storage):
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    sql = "SELECT 17 AS num"
    result = pandas.DataFrame([17], columns=["num"])
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True
    )
    query_job_mock.to_dataframe.return_value = result

    # Shouldn't fail when BigQuery Storage client isn't installed.
    with run_query_patch as run_query_mock, missing_bq_storage:
        run_query_mock.return_value = query_job_mock
        return_value = ip.run_cell_magic("bigquery", "", sql)

    assert isinstance(return_value, pandas.DataFrame)
    assert len(return_value) == len(result)  # verify row count
    assert list(return_value) == list(result)  # verify column names


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_default_connection_user_agent():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context._connection = None

    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, "general-project")
    )
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    conn_patch = mock.patch("google.cloud.bigquery.client.Connection", autospec=True)

    with conn_patch as conn, run_query_patch, default_patch:
        ip.run_cell_magic("bigquery", "", "SELECT 17 as num")

    client_info_arg = conn.call_args.kwargs.get("client_info")
    assert client_info_arg is not None
    assert client_info_arg.user_agent == "ipython-" + IPython.__version__


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_with_legacy_sql():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    with run_query_patch as run_query_mock:
        ip.run_cell_magic("bigquery", "--use_legacy_sql", "SELECT 17 AS num")

        job_config_used = run_query_mock.call_args_list[0][0][-1]
        assert job_config_used.use_legacy_sql is True


@pytest.mark.usefixtures("ipython_interactive")
@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_bigquery_magic_with_result_saved_to_variable():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    sql = "SELECT 17 AS num"
    result = pandas.DataFrame([17], columns=["num"])
    assert "df" not in ip.user_ns

    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True
    )
    query_job_mock.to_dataframe.return_value = result
    with run_query_patch as run_query_mock:
        run_query_mock.return_value = query_job_mock

        return_value = ip.run_cell_magic("bigquery", "df", sql)

    assert return_value is None
    assert "df" in ip.user_ns  # verify that variable exists
    df = ip.user_ns["df"]
    assert len(df) == len(result)  # verify row count
    assert list(df) == list(result)  # verify column names


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_does_not_clear_display_in_verbose_mode():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    clear_patch = mock.patch(
        "google.cloud.bigquery.magics.display.clear_output", autospec=True
    )
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    with clear_patch as clear_mock, run_query_patch:
        ip.run_cell_magic("bigquery", "--verbose", "SELECT 17 as num")

        assert clear_mock.call_count == 0


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_clears_display_in_verbose_mode():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    clear_patch = mock.patch(
        "google.cloud.bigquery.magics.display.clear_output", autospec=True
    )
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    with clear_patch as clear_mock, run_query_patch:
        ip.run_cell_magic("bigquery", "", "SELECT 17 as num")

        assert clear_mock.call_count == 1


@pytest.mark.usefixtures("ipython_interactive")
@pytest.mark.skipif(
    bigquery_storage_v1beta1 is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_bigquery_magic_with_bqstorage_from_argument(monkeypatch):
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    mock_credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    # Set up the context with monkeypatch so that it's reset for subsequent
    # tests.
    monkeypatch.setattr(magics.context, "credentials", mock_credentials)
    monkeypatch.setattr(magics.context, "use_bqstorage_api", False)

    # Mock out the BigQuery Storage API.
    bqstorage_mock = mock.create_autospec(
        bigquery_storage_v1beta1.BigQueryStorageClient
    )
    bqstorage_instance_mock = mock.create_autospec(
        bigquery_storage_v1beta1.BigQueryStorageClient, instance=True
    )
    bqstorage_mock.return_value = bqstorage_instance_mock
    bqstorage_client_patch = mock.patch(
        "google.cloud.bigquery_storage_v1beta1.BigQueryStorageClient", bqstorage_mock
    )

    sql = "SELECT 17 AS num"
    result = pandas.DataFrame([17], columns=["num"])
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True
    )
    query_job_mock.to_dataframe.return_value = result
    with run_query_patch as run_query_mock, bqstorage_client_patch:
        run_query_mock.return_value = query_job_mock

        return_value = ip.run_cell_magic("bigquery", "--use_bqstorage_api", sql)

    assert len(bqstorage_mock.call_args_list) == 1
    kwargs = bqstorage_mock.call_args_list[0].kwargs
    assert kwargs.get("credentials") is mock_credentials
    client_info = kwargs.get("client_info")
    assert client_info is not None
    assert client_info.user_agent == "ipython-" + IPython.__version__

    query_job_mock.to_dataframe.assert_called_once_with(
        bqstorage_client=bqstorage_instance_mock
    )

    assert isinstance(return_value, pandas.DataFrame)


@pytest.mark.usefixtures("ipython_interactive")
@pytest.mark.skipif(
    bigquery_storage_v1beta1 is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_bigquery_magic_with_bqstorage_from_context(monkeypatch):
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    mock_credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    # Set up the context with monkeypatch so that it's reset for subsequent
    # tests.
    monkeypatch.setattr(magics.context, "credentials", mock_credentials)
    monkeypatch.setattr(magics.context, "use_bqstorage_api", True)

    # Mock out the BigQuery Storage API.
    bqstorage_mock = mock.create_autospec(
        bigquery_storage_v1beta1.BigQueryStorageClient
    )
    bqstorage_instance_mock = mock.create_autospec(
        bigquery_storage_v1beta1.BigQueryStorageClient, instance=True
    )
    bqstorage_mock.return_value = bqstorage_instance_mock
    bqstorage_client_patch = mock.patch(
        "google.cloud.bigquery_storage_v1beta1.BigQueryStorageClient", bqstorage_mock
    )

    sql = "SELECT 17 AS num"
    result = pandas.DataFrame([17], columns=["num"])
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True
    )
    query_job_mock.to_dataframe.return_value = result
    with run_query_patch as run_query_mock, bqstorage_client_patch:
        run_query_mock.return_value = query_job_mock

        return_value = ip.run_cell_magic("bigquery", "", sql)

    assert len(bqstorage_mock.call_args_list) == 1
    kwargs = bqstorage_mock.call_args_list[0].kwargs
    assert kwargs.get("credentials") is mock_credentials
    client_info = kwargs.get("client_info")
    assert client_info is not None
    assert client_info.user_agent == "ipython-" + IPython.__version__

    query_job_mock.to_dataframe.assert_called_once_with(
        bqstorage_client=bqstorage_instance_mock
    )

    assert isinstance(return_value, pandas.DataFrame)


@pytest.mark.usefixtures("ipython_interactive")
@pytest.mark.skipif(
    bigquery_storage_v1beta1 is None, reason="Requires `google-cloud-bigquery-storage`"
)
def test_bigquery_magic_without_bqstorage(monkeypatch):
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    mock_credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    # Set up the context with monkeypatch so that it's reset for subsequent
    # tests.
    monkeypatch.setattr(magics.context, "credentials", mock_credentials)

    # Mock out the BigQuery Storage API.
    bqstorage_mock = mock.create_autospec(
        bigquery_storage_v1beta1.BigQueryStorageClient
    )
    bqstorage_client_patch = mock.patch(
        "google.cloud.bigquery_storage_v1beta1.BigQueryStorageClient", bqstorage_mock
    )

    sql = "SELECT 17 AS num"
    result = pandas.DataFrame([17], columns=["num"])
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True
    )
    query_job_mock.to_dataframe.return_value = result
    with run_query_patch as run_query_mock, bqstorage_client_patch:
        run_query_mock.return_value = query_job_mock

        return_value = ip.run_cell_magic("bigquery", "", sql)

        bqstorage_mock.assert_not_called()
        query_job_mock.to_dataframe.assert_called_once_with(bqstorage_client=None)

    assert isinstance(return_value, pandas.DataFrame)


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_dryrun_option_sets_job_config():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )

    sql = "SELECT 17 AS num"

    with run_query_patch as run_query_mock:
        ip.run_cell_magic("bigquery", "--dry_run", sql)

        job_config_used = run_query_mock.call_args_list[0][0][-1]
        assert job_config_used.dry_run is True


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_dryrun_option_returns_query_job():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True
    )
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )

    sql = "SELECT 17 AS num"

    with run_query_patch as run_query_mock, io.capture_output() as captured_io:
        run_query_mock.return_value = query_job_mock
        return_value = ip.run_cell_magic("bigquery", "--dry_run", sql)

        assert "Query validated. This query will process" in captured_io.stdout
        assert isinstance(return_value, job.QueryJob)


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_dryrun_option_variable_error_message():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query",
        autospec=True,
        side_effect=exceptions.BadRequest("Syntax error in SQL query"),
    )

    sql = "SELECT SELECT 17 AS num"

    assert "q_job" not in ip.user_ns

    with run_query_patch, io.capture_output() as captured:
        ip.run_cell_magic("bigquery", "q_job --dry_run", sql)

    full_text = captured.stderr
    assert "Could not save output to variable 'q_job'." in full_text


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_dryrun_option_saves_query_job_to_variable():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True
    )
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )

    sql = "SELECT 17 AS num"

    assert "q_job" not in ip.user_ns

    with run_query_patch as run_query_mock:
        run_query_mock.return_value = query_job_mock
        return_value = ip.run_cell_magic("bigquery", "q_job --dry_run", sql)

    assert return_value is None
    assert "q_job" in ip.user_ns
    q_job = ip.user_ns["q_job"]
    assert isinstance(q_job, job.QueryJob)


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_w_maximum_bytes_billed_invalid():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context._project = None

    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, "general-project")
    )
    client_query_patch = mock.patch("google.cloud.bigquery.client.Client.query")

    sql = "SELECT 17 AS num"

    with pytest.raises(ValueError), default_patch, client_query_patch:
        ip.run_cell_magic("bigquery", "--maximum_bytes_billed=abc", sql)


@pytest.mark.parametrize(
    "param_value,expected", [("987654321", "987654321"), ("None", "0")]
)
@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_w_maximum_bytes_billed_overrides_context(param_value, expected):
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context._project = None

    # Set the default maximum bytes billed, so we know it's overridable by the param.
    magics.context.default_query_job_config.maximum_bytes_billed = 1234567

    project = "test-project"
    job_reference = copy.deepcopy(JOB_REFERENCE_RESOURCE)
    job_reference["projectId"] = project
    query = "SELECT 17 AS num"
    resource = copy.deepcopy(QUERY_RESOURCE)
    resource["jobReference"] = job_reference
    resource["configuration"]["query"]["query"] = query
    data = {"jobReference": job_reference, "totalRows": 0, "rows": []}
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, "general-project")
    )
    conn = magics.context._connection = make_connection(resource, data)
    list_rows_patch = mock.patch(
        "google.cloud.bigquery.client.Client.list_rows",
        return_value=google.cloud.bigquery.table._EmptyRowIterator(),
    )
    with list_rows_patch, default_patch:
        ip.run_cell_magic(
            "bigquery", "--maximum_bytes_billed={}".format(param_value), query
        )

    _, req = conn.api_request.call_args_list[0]
    sent_config = req["data"]["configuration"]["query"]
    assert sent_config["maximumBytesBilled"] == expected


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_w_maximum_bytes_billed_w_context_inplace():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context._project = None

    magics.context.default_query_job_config.maximum_bytes_billed = 1337

    project = "test-project"
    job_reference = copy.deepcopy(JOB_REFERENCE_RESOURCE)
    job_reference["projectId"] = project
    query = "SELECT 17 AS num"
    resource = copy.deepcopy(QUERY_RESOURCE)
    resource["jobReference"] = job_reference
    resource["configuration"]["query"]["query"] = query
    data = {"jobReference": job_reference, "totalRows": 0, "rows": []}
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, "general-project")
    )
    conn = magics.context._connection = make_connection(resource, data)
    list_rows_patch = mock.patch(
        "google.cloud.bigquery.client.Client.list_rows",
        return_value=google.cloud.bigquery.table._EmptyRowIterator(),
    )
    with list_rows_patch, default_patch:
        ip.run_cell_magic("bigquery", "", query)

    _, req = conn.api_request.call_args_list[0]
    sent_config = req["data"]["configuration"]["query"]
    assert sent_config["maximumBytesBilled"] == "1337"


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_w_maximum_bytes_billed_w_context_setter():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context._project = None

    magics.context.default_query_job_config = job.QueryJobConfig(
        maximum_bytes_billed=10203
    )

    project = "test-project"
    job_reference = copy.deepcopy(JOB_REFERENCE_RESOURCE)
    job_reference["projectId"] = project
    query = "SELECT 17 AS num"
    resource = copy.deepcopy(QUERY_RESOURCE)
    resource["jobReference"] = job_reference
    resource["configuration"]["query"]["query"] = query
    data = {"jobReference": job_reference, "totalRows": 0, "rows": []}
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, "general-project")
    )
    conn = magics.context._connection = make_connection(resource, data)
    list_rows_patch = mock.patch(
        "google.cloud.bigquery.client.Client.list_rows",
        return_value=google.cloud.bigquery.table._EmptyRowIterator(),
    )
    with list_rows_patch, default_patch:
        ip.run_cell_magic("bigquery", "", query)

    _, req = conn.api_request.call_args_list[0]
    sent_config = req["data"]["configuration"]["query"]
    assert sent_config["maximumBytesBilled"] == "10203"


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_with_project():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context._project = None

    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, "general-project")
    )
    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    with run_query_patch as run_query_mock, default_patch:
        ip.run_cell_magic("bigquery", "--project=specific-project", "SELECT 17 as num")

        client_used = run_query_mock.call_args_list[0][0][0]
        assert client_used.project == "specific-project"
        # context project should not change
        assert magics.context.project == "general-project"


@pytest.mark.usefixtures("ipython_interactive")
@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_bigquery_magic_with_string_params():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    sql = "SELECT @num AS num"
    result = pandas.DataFrame([17], columns=["num"])
    assert "params_string_df" not in ip.user_ns

    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True
    )
    query_job_mock.to_dataframe.return_value = result
    with run_query_patch as run_query_mock:
        run_query_mock.return_value = query_job_mock

        ip.run_cell_magic("bigquery", 'params_string_df --params {"num":17}', sql)
        run_query_mock.assert_called_once_with(mock.ANY, sql.format(num=17), mock.ANY)

    assert "params_string_df" in ip.user_ns  # verify that the variable exists
    df = ip.user_ns["params_string_df"]
    assert len(df) == len(result)  # verify row count
    assert list(df) == list(result)  # verify column names


@pytest.mark.usefixtures("ipython_interactive")
@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_bigquery_magic_with_dict_params():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    sql = "SELECT @num AS num"
    result = pandas.DataFrame([17], columns=["num"])
    assert "params_dict_df" not in ip.user_ns

    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query", autospec=True
    )
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True
    )
    query_job_mock.to_dataframe.return_value = result
    with run_query_patch as run_query_mock:
        run_query_mock.return_value = query_job_mock

        params = {"num": 17}
        # Insert dictionary into user namespace so that it can be expanded
        ip.user_ns["params"] = params
        ip.run_cell_magic("bigquery", "params_dict_df --params $params", sql)
        run_query_mock.assert_called_once_with(mock.ANY, sql.format(num=17), mock.ANY)

    assert "params_dict_df" in ip.user_ns  # verify that the variable exists
    df = ip.user_ns["params_dict_df"]
    assert len(df) == len(result)  # verify row count
    assert list(df) == list(result)  # verify column names


@pytest.mark.usefixtures("ipython_interactive")
@pytest.mark.skipif(pandas is None, reason="Requires `pandas`")
def test_bigquery_magic_with_improperly_formatted_params():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    sql = "SELECT @num AS num"

    with pytest.raises(SyntaxError):
        ip.run_cell_magic("bigquery", "--params {17}", sql)


@pytest.mark.usefixtures("ipython_interactive")
def test_bigquery_magic_omits_tracebacks_from_error_message():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension("google.cloud.bigquery")

    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )
    default_patch = mock.patch(
        "google.auth.default", return_value=(credentials_mock, "general-project")
    )

    run_query_patch = mock.patch(
        "google.cloud.bigquery.magics._run_query",
        autospec=True,
        side_effect=exceptions.BadRequest("Syntax error in SQL query"),
    )

    with run_query_patch, default_patch, io.capture_output() as captured_io:
        ip.run_cell_magic("bigquery", "", "SELECT foo FROM WHERE LIMIT bar")

    output = captured_io.stderr
    assert "400 Syntax error in SQL query" in output
    assert "Traceback (most recent call last)" not in output
    assert "Syntax error" not in captured_io.stdout
