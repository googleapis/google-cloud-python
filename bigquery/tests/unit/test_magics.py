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

import re
import mock
from concurrent import futures

import pytest
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

import google.auth.credentials
from google.cloud.bigquery import table
from google.cloud.bigquery import magics


pytestmark = pytest.mark.skipif(IPython is None, reason='Requires `ipython`')


@pytest.fixture(scope='session')
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


def test_context_credentials_auto_set_w_application_default_credentials():
    """When Application Default Credentials are set, the context credentials
    will be created the first time it is called
    """
    assert magics.context._credentials is None
    assert magics.context._project is None

    project = 'prahj-ekt'
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True)
    default_patch = mock.patch(
        'google.auth.default', return_value=(credentials_mock, project))
    with default_patch as default_mock:
        assert magics.context.credentials is credentials_mock
        assert magics.context.project == project

    assert default_mock.call_count == 2


def test_context_credentials_and_project_can_be_set_explicitly():
    project1 = 'one-project-55564'
    project2 = 'other-project-52569'
    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True)
    default_patch = mock.patch(
        'google.auth.default', return_value=(credentials_mock, project1))
    with default_patch as default_mock:
        magics.context.credentials = credentials_mock
        magics.context.project = project2

    assert magics.context.project == project2
    assert magics.context.credentials is credentials_mock
    # default should not be called if credentials & project are explicitly set
    assert default_mock.call_count == 0


def test__run_query():
    magics.context._credentials = None

    job_id = 'job_1234'
    sql = 'SELECT 17'
    responses = [
        futures.TimeoutError,
        futures.TimeoutError,
        [table.Row((17,), {'num': 0})]
    ]

    client_patch = mock.patch(
        'google.cloud.bigquery.magics.bigquery.Client', autospec=True)
    with client_patch as client_mock, io.capture_output() as captured:
        client_mock().query(sql).result.side_effect = responses
        client_mock().query(sql).job_id = job_id

        query_job = magics._run_query(client_mock(), sql)

    lines = re.split('\n|\r', captured.stdout)
    # Removes blanks & terminal code (result of display clearing)
    updates = list(filter(lambda x: bool(x) and x != '\x1b[2K', lines))

    assert query_job.job_id == job_id
    expected_first_line = "Executing query with job ID: {}".format(job_id)
    assert updates[0] == expected_first_line
    execution_updates = updates[1:-1]
    assert len(execution_updates) == 3  # one update per API response
    assert all(re.match("Query executing: .*s", line)
               for line in execution_updates)
    assert re.match("Query complete after .*s", updates[-1])


@pytest.mark.usefixtures('ipython_interactive')
def test_extension_load():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')

    # verify that the magic is registered and has the correct source
    magic = ip.magics_manager.magics['cell'].get('bigquery')
    assert magic.__module__ == 'google.cloud.bigquery.magics'


@pytest.mark.usefixtures('ipython_interactive')
@pytest.mark.skipif(pandas is None, reason='Requires `pandas`')
def test_bigquery_magic_without_optional_arguments():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True)

    sql = 'SELECT 17 AS num'
    result = pandas.DataFrame([17], columns=['num'])
    run_query_patch = mock.patch(
        'google.cloud.bigquery.magics._run_query', autospec=True)
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True)
    query_job_mock.to_dataframe.return_value = result
    with run_query_patch as run_query_mock:
        run_query_mock.return_value = query_job_mock

        result = ip.run_cell_magic('bigquery', '', sql)

    assert isinstance(result, pandas.DataFrame)
    assert len(result) == len(result)    # verify row count
    assert list(result) == list(result)  # verify column names


@pytest.mark.usefixtures('ipython_interactive')
def test_bigquery_magic_with_legacy_sql():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True)

    run_query_patch = mock.patch(
        'google.cloud.bigquery.magics._run_query', autospec=True)
    with run_query_patch as run_query_mock:
        ip.run_cell_magic(
            'bigquery', '--use_legacy_sql', 'SELECT 17 AS num')

        job_config_used = run_query_mock.call_args_list[0][0][-1]
        assert job_config_used.use_legacy_sql is True


@pytest.mark.usefixtures('ipython_interactive')
@pytest.mark.skipif(pandas is None, reason='Requires `pandas`')
def test_bigquery_magic_with_result_saved_to_variable():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True)

    sql = 'SELECT 17 AS num'
    result = pandas.DataFrame([17], columns=['num'])
    assert 'myvariable' not in ip.user_ns

    run_query_patch = mock.patch(
        'google.cloud.bigquery.magics._run_query', autospec=True)
    query_job_mock = mock.create_autospec(
        google.cloud.bigquery.job.QueryJob, instance=True)
    query_job_mock.to_dataframe.return_value = result
    with run_query_patch as run_query_mock:
        run_query_mock.return_value = query_job_mock

        ip.run_cell_magic('bigquery', 'df', sql)

    assert 'df' in ip.user_ns        # verify that variable exists
    df = ip.user_ns['df']
    assert len(df) == len(result)    # verify row count
    assert list(df) == list(result)  # verify column names


@pytest.mark.usefixtures('ipython_interactive')
def test_bigquery_magic_does_not_clear_display_in_verbose_mode():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True)

    clear_patch = mock.patch(
        'google.cloud.bigquery.magics.display.clear_output', autospec=True)
    run_query_patch = mock.patch(
        'google.cloud.bigquery.magics._run_query', autospec=True)
    with clear_patch as clear_mock, run_query_patch:
        ip.run_cell_magic('bigquery', '--verbose', 'SELECT 17 as num')

        assert clear_mock.call_count == 0


@pytest.mark.usefixtures('ipython_interactive')
def test_bigquery_magic_clears_display_in_verbose_mode():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')
    magics.context.credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True)

    clear_patch = mock.patch(
        'google.cloud.bigquery.magics.display.clear_output', autospec=True)
    run_query_patch = mock.patch(
        'google.cloud.bigquery.magics._run_query', autospec=True)
    with clear_patch as clear_mock, run_query_patch:
        ip.run_cell_magic('bigquery', '', 'SELECT 17 as num')

        assert clear_mock.call_count == 1


@pytest.mark.usefixtures('ipython_interactive')
def test_bigquery_magic_with_project():
    ip = IPython.get_ipython()
    ip.extension_manager.load_extension('google.cloud.bigquery')
    magics.context._project = None

    credentials_mock = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True)
    default_patch = mock.patch(
        'google.auth.default',
        return_value=(credentials_mock, 'general-project'))
    run_query_patch = mock.patch(
        'google.cloud.bigquery.magics._run_query', autospec=True)
    with run_query_patch as run_query_mock, default_patch:
        ip.run_cell_magic(
            'bigquery', '--project=specific-project', 'SELECT 17 as num')

        client_used = run_query_mock.call_args_list[0][0][0]
        assert client_used.project == 'specific-project'
        # context project should not change
        assert magics.context.project == 'general-project'
