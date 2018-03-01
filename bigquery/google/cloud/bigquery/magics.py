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

"""Define IPython Magics

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
        Project to use for running the query. Defaults to the client's default
        project.
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
        All queries run using this magic will run using the context client
        (:func:`Context.client <google.cloud.bigquery.magics.Context.client>`)

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
    from IPython import get_ipython
    from IPython.display import clear_output
    from IPython.core import magic_arguments
except ImportError:  # pragma: NO COVER
    raise ImportError('This module can only be loaded in IPython.')

from google.cloud.bigquery.client import Client
from google.cloud.bigquery.job import QueryJobConfig


class Context(object):
    """Storage for objects to be used throughout an IPython notebook session

    A Context object is initialized when the ``magics`` module is imported,
    and can be found at ``google.cloud.bigquery.magics.context``.
    """
    def __init__(self):
        self._client = None

    @property
    def client(self):
        """BigQuery Client to use for queries performed through IPython magics

        Note:
            The client does not need to be explicitly defined if you are using
            Application Default Credentials. If you are not using Application
            Default Credentials, manually construct a BigQuery Client with your
            credentials and set it as the context client as demonstrated in the
            example below.

        Example:
            Manually setting the context client:

            >>> from google.cloud.bigquery import magics
            >>> from google.cloud.bigquery import Client
            >>> client = Client.from_service_account_json('/path/to/key.json')
            >>> magics.context.client = client
        """
        if self._client is None:
            self._client = Client()
        return self._client

    @client.setter
    def client(self, value):
        self._client = value


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
        str: the ID of the query job created

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
        except futures.TimeoutError:
            continue
        break
    print('\nQuery complete after {:0.2f}s'.format(time.time() - start_time))
    return query_job.job_id


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
    help=('Project to use for executing this query. Defaults to the '
          'client\'s project'))
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

    if args.project:
        client = Client(
            project=args.project, credentials=context.client._credentials)
    else:
        client = context.client

    job_config = QueryJobConfig()
    job_config.use_legacy_sql = args.use_legacy_sql
    job_id = _run_query(client, query, job_config)

    if not args.verbose:
        clear_output()

    # Fetch the results.
    result = client.get_job(job_id).to_dataframe()
    if args.destination_var:
        get_ipython().push({args.destination_var: result})
    return result
