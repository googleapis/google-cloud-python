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

"""IPython Magics

.. function:: %%bigquery

    IPython cell magic to run a query and display the result as a DataFrame

    .. code-block:: python

        %%bigquery [<destination_var>] [--project <project>] [--use_legacy_sql]
                   [--verbose]
        <query>

    Parameters:

    * ``<destination_var>`` (optional, line argument):
        variable to store the query results.
    * ``--project <project>`` (optional, line argument):
        Project to use for running the query. Defaults to the context
        :attr:`~google.cloud.bigquery.magics.Context.project`.
    * ``--use_legacy_sql`` (optional, line argument):
        Runs the query using Legacy SQL syntax. Defaults to Standard SQL if
        this argument not used.
    * ``--verbose`` (optional, line argument):
        If this flag is used, information including the query job ID and the
        amount of time for the query to complete will not be cleared after the
        query is finished. By default, this information will be displayed but
        will be cleared after the query is finished.
    * ``<query>`` (required, cell argument):
        SQL query to run.

    Returns:
        A :class:`pandas.DataFrame` with the query results.

    .. note::
        All queries run using this magic will run using the context
        :attr:`~google.cloud.bigquery.magics.Context.credentials`.

    Examples:
        The following examples can be run in an IPython notebook after loading
        the bigquery IPython extension (see ``In[1]``) and setting up
        Application Default Credentials.

    .. code-block:: python

        In [1]: %load_ext google.cloud.bigquery

        In [2]: %%bigquery
           ...: SELECT name, SUM(number) as count
           ...: FROM `bigquery-public-data.usa_names.usa_1910_current`
           ...: GROUP BY name
           ...: ORDER BY count DESC
           ...: LIMIT 3

        Out[2]:       name    count
           ...: -------------------
           ...: 0    James  4987296
           ...: 1     John  4866302
           ...: 2   Robert  4738204

        In [3]: %%bigquery df --project my-alternate-project --verbose
           ...: SELECT name, SUM(number) as count
           ...: FROM `bigquery-public-data.usa_names.usa_1910_current`
           ...: WHERE gender = 'F'
           ...: GROUP BY name
           ...: ORDER BY count DESC
           ...: LIMIT 3
        Executing query with job ID: bf633912-af2c-4780-b568-5d868058632b
        Query executing: 2.61s
        Query complete after 2.92s

        Out[3]:          name    count
           ...: ----------------------
           ...: 0        Mary  3736239
           ...: 1    Patricia  1568495
           ...: 2   Elizabeth  1519946

        In [4]: df

        Out[4]:          name    count
           ...: ----------------------
           ...: 0        Mary  3736239
           ...: 1    Patricia  1568495
           ...: 2   Elizabeth  1519946

"""

from __future__ import print_function

import time
from concurrent import futures

try:
    import IPython
    from IPython import display
    from IPython.core import magic_arguments
except ImportError:  # pragma: NO COVER
    raise ImportError('This module can only be loaded in IPython.')

import google.auth
from google.cloud import bigquery


class Context(object):
    """Storage for objects to be used throughout an IPython notebook session.

    A Context object is initialized when the ``magics`` module is imported,
    and can be found at ``google.cloud.bigquery.magics.context``.
    """
    def __init__(self):
        self._credentials = None
        self._project = None

    @property
    def credentials(self):
        """google.auth.credentials.Credentials: Credentials to use for queries
        performed through IPython magics

        Note:
            These credentials do not need to be explicitly defined if you are
            using Application Default Credentials. If you are not using
            Application Default Credentials, manually construct a
            :class:`google.auth.credentials.Credentials` object and set it as
            the context credentials as demonstrated in the example below. See
            `auth docs`_ for more information on obtaining credentials.

        Example:
            Manually setting the context credentials:

            >>> from google.cloud.bigquery import magics
            >>> from google.oauth2 import service_account
            >>> credentials = (service_account
            ...     .Credentials.from_service_account_file(
            ...         '/path/to/key.json'))
            >>> magics.context.credentials = credentials


        .. _auth docs: http://google-auth.readthedocs.io
            /en/latest/user-guide.html#obtaining-credentials
        """
        if self._credentials is None:
            self._credentials, _ = google.auth.default()
        return self._credentials

    @credentials.setter
    def credentials(self, value):
        self._credentials = value

    @property
    def project(self):
        """str: Default project to use for queries performed through IPython
        magics

        Note:
            The project does not need to be explicitly defined if you have an
            environment default project set. If you do not have a default
            project set in your environment, manually assign the project as
            demonstrated in the example below.

        Example:
            Manually setting the context project:

            >>> from google.cloud.bigquery import magics
            >>> magics.context.project = 'my-project'
        """
        if self._project is None:
            _, self._project = google.auth.default()
        return self._project

    @project.setter
    def project(self, value):
        self._project = value


context = Context()


def _run_query(client, query, job_config=None):
    """Runs a query while printing status updates

    Args:
        client (google.cloud.bigquery.client.Client):
            Client to bundle configuration needed for API requests.
        query (str):
            SQL query to be executed. Defaults to the standard SQL dialect.
            Use the ``job_config`` parameter to change dialects.
        job_config (google.cloud.bigquery.job.QueryJobConfig, optional):
            Extra configuration options for the job.

    Returns:
        google.cloud.bigquery.job.QueryJob: the query job created

    Example:
        >>> client = bigquery.Client()
        >>> _run_query(client, "SELECT 17")
        Executing query with job ID: bf633912-af2c-4780-b568-5d868058632b
        Query executing: 1.66s
        Query complete after 2.07s
        'bf633912-af2c-4780-b568-5d868058632b'
    """
    start_time = time.time()
    query_job = client.query(query, job_config=job_config)
    print('Executing query with job ID: {}'.format(query_job.job_id))

    while True:
        print('\rQuery executing: {:0.2f}s'.format(
            time.time() - start_time), end='')
        try:
            query_job.result(timeout=0.5)
            break
        except futures.TimeoutError:
            continue
    print('\nQuery complete after {:0.2f}s'.format(time.time() - start_time))
    return query_job


@magic_arguments.magic_arguments()
@magic_arguments.argument(
    'destination_var',
    nargs='?',
    help=('If provided, save the output to this variable in addition '
          'to displaying it.'))
@magic_arguments.argument(
    '--project',
    type=str,
    default=None,
    help=('Project to use for executing this query. Defaults to the context '
          'project.'))
@magic_arguments.argument(
    '--use_legacy_sql', action='store_true', default=False,
    help=('Sets query to use Legacy SQL instead of Standard SQL. Defaults to '
          'Standard SQL if this argument is not used.'))
@magic_arguments.argument(
    '--verbose', action='store_true', default=False,
    help=('If set, print verbose output, including the query job ID and the '
          'amount of time for the query to finish. By default, this '
          'information will be displayed as the query runs, but will be '
          'cleared after the query is finished.'))
def _cell_magic(line, query):
    """Underlying function for bigquery cell magic

    Note:
        This function contains the underlying logic for the 'bigquery' cell
        magic. This function is not meant to be called directly.

    Args:
        line (str): "%%bigquery" followed by arguments as required
        query (str): SQL query to run

    Returns:
        pandas.DataFrame: the query results.
    """
    args = magic_arguments.parse_argstring(_cell_magic, line)

    project = args.project or context.project
    client = bigquery.Client(project=project, credentials=context.credentials)
    job_config = bigquery.job.QueryJobConfig()
    job_config.use_legacy_sql = args.use_legacy_sql
    query_job = _run_query(client, query, job_config)

    if not args.verbose:
        display.clear_output()

    result = query_job.to_dataframe()
    if args.destination_var:
        IPython.get_ipython().push({args.destination_var: result})
    return result
