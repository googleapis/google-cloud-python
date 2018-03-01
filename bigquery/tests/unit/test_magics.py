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
import os
import mock
from concurrent import futures

import pytest
try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None
try:
    import IPython
    from IPython import get_ipython
    from IPython.utils.io import capture_output
    from IPython.testing.tools import default_config
    from IPython.terminal.interactiveshell import TerminalInteractiveShell
except ImportError:  # pragma: NO COVER
    IPython = None

from google.cloud.bigquery.client import Client
from google.cloud.bigquery.table import Row
from google.cloud.bigquery import magics


@pytest.fixture(scope='session')
def ipython():
    config = default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = TerminalInteractiveShell.instance(config=config)
    return shell


@pytest.fixture()
def ipython_interactive(request, ipython):
    """Activate IPython's builtin hooks

    for the duration of the test scope.
    """
    with ipython.builtin_trap:
        yield ipython


@pytest.mark.skipif(IPython is None, reason='Requires `ipython`')
@pytest.mark.usefixtures('ipython_interactive')
class TestMagics():
    def test_context_client_auto_set_w_application_default_credentials(self):
        """When Application Default Credentials are set, the context client
        will be created the first time it is called
        """
        assert magics.context._client is None
        assert os.environ['GOOGLE_APPLICATION_CREDENTIALS'] is not None
        adc_client = Client()

        assert magics.context.client.project == adc_client.project

    def test_context_client_can_be_set_explicitly(self):
        new_client = Client(project='other-project-52569')
        magics.context.client = new_client

        assert magics.context.client.project == 'other-project-52569'

    def test__run_query(self):
        magics.context._client = None

        JOB_ID = 'job_1234'
        SQL = 'SELECT 17'
        RESPONSES = [
            futures.TimeoutError,
            futures.TimeoutError,
            [Row((17,), {'num': 0})]
        ]

        client_patch = mock.patch(
            'google.cloud.bigquery.magics.Client', autospec=True)
        with client_patch as client_mock, capture_output() as captured:
            client_mock().query(SQL).result.side_effect = RESPONSES
            client_mock().query(SQL).job_id = JOB_ID

            job_id = magics._run_query(client_mock(), SQL)

        lines = re.split('\n|\r', captured.stdout)
        # Removes blanks & terminal code (result of display clearing)
        updates = list(filter(lambda x: bool(x) and x != '\x1b[2K', lines))

        assert job_id == JOB_ID
        expected_first_line = "Executing query with job ID: {}".format(JOB_ID)
        assert updates[0] == expected_first_line
        execution_updates = updates[1:-1]
        assert len(execution_updates) == 3  # one update per API response
        assert all(re.match("Query executing: .*s", line)
                   for line in execution_updates)
        assert re.match("Query complete after .*s", updates[-1])

    def test_extension_load(self):
        ip = get_ipython()
        ip.extension_manager.load_extension('google.cloud.bigquery')

        # verify that the magic is registered and has the correct source
        magic = ip.magics_manager.magics['cell'].get('bigquery')
        assert magic.__module__ == 'google.cloud.bigquery.magics'

    @pytest.mark.skipif(pandas is None, reason='Requires `pandas`')
    def test_bigquery_magic_without_optional_arguments(self):
        ip = get_ipython()
        ip.extension_manager.load_extension('google.cloud.bigquery')
        magics.context._client = None

        JOB_ID = 'job_1234'
        SQL = 'SELECT 17 AS num'
        RESPONSES = [
            futures.TimeoutError,
            futures.TimeoutError,
            [Row((17,), {'num': 0})]
        ]
        RESULT = pandas.DataFrame([17], columns=['num'])

        client_patch = mock.patch(
            'google.cloud.bigquery.magics.Client', autospec=True)
        with client_patch as client_mock:
            client_mock().project = 'my-project'
            client_mock().query(SQL).result.side_effect = RESPONSES
            client_mock().query(SQL).job_id = JOB_ID
            client_mock().get_job(JOB_ID).to_dataframe.return_value = RESULT
            magics.context.client = client_mock()

            result = ip.run_cell_magic('bigquery', '', SQL)

        assert isinstance(result, pandas.DataFrame)
        assert len(result) == len(RESULT)    # verify row count
        assert list(result) == list(RESULT)  # verify column names

    def test_bigquery_magic_with_legacy_sql(self):
        ip = get_ipython()
        ip.extension_manager.load_extension('google.cloud.bigquery')
        magics.context._client = None

        run_query_patch = mock.patch(
            'google.cloud.bigquery.magics._run_query', autospec=True)
        get_job_patch = mock.patch(
            'google.cloud.bigquery.magics.Client.get_job', autospec=True)
        with run_query_patch as run_query_mock, get_job_patch:
            ip.run_cell_magic(
                'bigquery', '--use_legacy_sql', 'SELECT 17 AS num')

            job_config_used = run_query_mock.call_args_list[0][0][-1]
            assert job_config_used.use_legacy_sql is True

    @pytest.mark.skipif(pandas is None, reason='Requires `pandas`')
    def test_bigquery_magic_with_result_saved_to_variable(self):
        ip = get_ipython()
        ip.extension_manager.load_extension('google.cloud.bigquery')
        magics.context._client = None

        JOB_ID = 'job_1234'
        RESULT = pandas.DataFrame([17], columns=['num'])
        assert 'myvariable' not in ip.user_ns

        client_patch = mock.patch(
            'google.cloud.bigquery.magics.Client', autospec=True)
        with client_patch as client_mock:
            client_mock().get_job(JOB_ID).to_dataframe.return_value = RESULT

            ip.run_cell_magic('bigquery', 'df', 'SELECT 17 as num')

        assert 'df' in ip.user_ns        # verify that variable exists
        df = ip.user_ns['df']
        assert len(df) == len(RESULT)    # verify row count
        assert list(df) == list(RESULT)  # verify column names

    def test_bigquery_magic_does_not_clear_display_in_verbose_mode(self):
        ip = get_ipython()
        ip.extension_manager.load_extension('google.cloud.bigquery')
        magics.context._client = None

        clear_patch = mock.patch(
            'google.cloud.bigquery.magics.clear_output', autospec=True)
        run_query_patch = mock.patch(
            'google.cloud.bigquery.magics._run_query', autospec=True)
        client_patch = mock.patch(
            'google.cloud.bigquery.magics.Client', autospec=True)
        with clear_patch as clear_mock, run_query_patch, client_patch:
            ip.run_cell_magic('bigquery', '--verbose', 'SELECT 17 as num')

            assert clear_mock.call_count == 0

    def test_bigquery_magic_clears_display_in_verbose_mode(self):
        ip = get_ipython()
        ip.extension_manager.load_extension('google.cloud.bigquery')
        magics.context._client = None

        clear_patch = mock.patch(
            'google.cloud.bigquery.magics.clear_output', autospec=True)
        run_query_patch = mock.patch(
            'google.cloud.bigquery.magics._run_query', autospec=True)
        client_patch = mock.patch(
            'google.cloud.bigquery.magics.Client', autospec=True)
        with clear_patch as clear_mock, run_query_patch, client_patch:
            ip.run_cell_magic('bigquery', '', 'SELECT 17 as num')

            assert clear_mock.call_count == 1

    def test_bigquery_magic_with_project(self):
        ip = get_ipython()
        ip.extension_manager.load_extension('google.cloud.bigquery')
        magics.context._client = None

        run_query_patch = mock.patch(
            'google.cloud.bigquery.magics._run_query', autospec=True)
        get_job_patch = mock.patch(
            'google.cloud.bigquery.magics.Client.get_job', autospec=True)
        with run_query_patch as run_query_mock, get_job_patch:
            magics.context.client = Client(project='general-project')

            ip.run_cell_magic(
                'bigquery', '--project=specific-project', 'SELECT 17 as num')

            client_used = run_query_mock.call_args_list[0][0][0]
            assert client_used.project == 'specific-project'
            # context client default project should not change
            assert magics.context.client.project == 'general-project'
