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
                   [--verbose] [--params <params>]
        <query>

    Parameters:

    * ``<destination_var>`` (optional, line argument):
        variable to store the query results. The results are not displayed if
        this parameter is used. If an error occurs during the query execution,
        the corresponding ``QueryJob`` instance (if available) is stored in
        the variable instead.
    * ``--destination_table`` (optional, line argument):
        A dataset and table to store the query results. If table does not exists,
        it will be created. If table already exists, its data will be overwritten.
        Variable should be in a format <dataset_id>.<table_id>.
    * ``--project <project>`` (optional, line argument):
        Project to use for running the query. Defaults to the context
        :attr:`~google.cloud.bigquery.magics.Context.project`.
    * ``--use_bqstorage_api`` (optional, line argument):
        Downloads the DataFrame using the BigQuery Storage API. To use this
        option, install the ``google-cloud-bigquery-storage`` and ``fastavro``
        packages, and `enable the BigQuery Storage API
        <https://console.cloud.google.com/apis/library/bigquerystorage.googleapis.com>`_.
    * ``--use_legacy_sql`` (optional, line argument):
        Runs the query using Legacy SQL syntax. Defaults to Standard SQL if
        this argument not used.
    * ``--verbose`` (optional, line argument):
        If this flag is used, information including the query job ID and the
        amount of time for the query to complete will not be cleared after the
        query is finished. By default, this information will be displayed but
        will be cleared after the query is finished.
    * ``--params <params>`` (optional, line argument):
        If present, the argument following the ``--params`` flag must be
        either:

        * :class:`str` - A JSON string representation of a dictionary in the
          format ``{"param_name": "param_value"}`` (ex. ``{"num": 17}``). Use
          of the parameter in the query should be indicated with
          ``@param_name``. See ``In[5]`` in the Examples section below.

        * :class:`dict` reference - A reference to a ``dict`` in the format
          ``{"param_name": "param_value"}``, where the value types must be JSON
          serializable. The variable reference is indicated by a ``$`` before
          the variable name (ex. ``$my_dict_var``). See ``In[6]`` and ``In[7]``
          in the Examples section below.
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

    .. code-block:: none

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

        In [4]: df

        Out[4]:          name    count
           ...: ----------------------
           ...: 0        Mary  3736239
           ...: 1    Patricia  1568495
           ...: 2   Elizabeth  1519946

        In [5]: %%bigquery --params {"num": 17}
           ...: SELECT @num AS num

        Out[5]:     num
           ...: -------
           ...: 0    17

        In [6]: params = {"num": 17}

        In [7]: %%bigquery --params $params
           ...: SELECT @num AS num

        Out[7]:     num
           ...: -------
           ...: 0    17
"""

from __future__ import print_function

import re
import ast
import functools
import sys
import time
from concurrent import futures

try:
    import IPython
    from IPython import display
    from IPython.core import magic_arguments
except ImportError:  # pragma: NO COVER
    raise ImportError("This module can only be loaded in IPython.")

from google.api_core import client_info
from google.api_core.exceptions import NotFound
import google.auth
from google.cloud import bigquery
import google.cloud.bigquery.dataset
from google.cloud.bigquery.dbapi import _helpers
import six


IPYTHON_USER_AGENT = "ipython-{}".format(IPython.__version__)


class Context(object):
    """Storage for objects to be used throughout an IPython notebook session.

    A Context object is initialized when the ``magics`` module is imported,
    and can be found at ``google.cloud.bigquery.magics.context``.
    """

    def __init__(self):
        self._credentials = None
        self._project = None
        self._connection = None
        self._use_bqstorage_api = None
        self._default_query_job_config = bigquery.QueryJobConfig()

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

    @property
    def use_bqstorage_api(self):
        """bool: [Beta] Set to True to use the BigQuery Storage API to
        download query results

        To use this option, install the ``google-cloud-bigquery-storage`` and
        ``fastavro`` packages, and `enable the BigQuery Storage API
        <https://console.cloud.google.com/apis/library/bigquerystorage.googleapis.com>`_.
        """
        return self._use_bqstorage_api

    @use_bqstorage_api.setter
    def use_bqstorage_api(self, value):
        self._use_bqstorage_api = value

    @property
    def default_query_job_config(self):
        """google.cloud.bigquery.job.QueryJobConfig: Default job
        configuration for queries.

        The context's :class:`~google.cloud.bigquery.job.QueryJobConfig` is
        used for queries. Some properties can be overridden with arguments to
        the magics.

        Example:
            Manually setting the default value for ``maximum_bytes_billed``
            to 100 MB:

            >>> from google.cloud.bigquery import magics
            >>> magics.context.default_query_job_config.maximum_bytes_billed = 100000000
        """
        return self._default_query_job_config

    @default_query_job_config.setter
    def default_query_job_config(self, value):
        self._default_query_job_config = value


context = Context()


def _handle_error(error, destination_var=None):
    """Process a query execution error.

    Args:
        error (Exception):
            An exception that ocurred during the query exectution.
        destination_var (Optional[str]):
            The name of the IPython session variable to store the query job.
    """
    if destination_var:
        query_job = getattr(error, "query_job", None)

        if query_job is not None:
            IPython.get_ipython().push({destination_var: query_job})
        else:
            # this is the case when previewing table rows by providing just
            # table ID to cell magic
            print(
                "Could not save output to variable '{}'.".format(destination_var),
                file=sys.stderr,
            )

    print("\nERROR:\n", str(error), file=sys.stderr)


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

    if job_config and job_config.dry_run:
        return query_job

    print("Executing query with job ID: {}".format(query_job.job_id))

    while True:
        print("\rQuery executing: {:0.2f}s".format(time.time() - start_time), end="")
        try:
            query_job.result(timeout=0.5)
            break
        except futures.TimeoutError:
            continue
    print("\nQuery complete after {:0.2f}s".format(time.time() - start_time))
    return query_job


def _create_dataset_if_necessary(client, dataset_id):
    """Create a dataset in the current project if it doesn't exist.

    Args:
        client (google.cloud.bigquery.client.Client):
            Client to bundle configuration needed for API requests.
        dataset_id (str):
            Dataset id.
    """
    dataset_reference = bigquery.dataset.DatasetReference(client.project, dataset_id)
    try:
        dataset = client.get_dataset(dataset_reference)
        return
    except NotFound:
        pass
    dataset = bigquery.Dataset(dataset_reference)
    dataset.location = client.location
    print("Creating dataset: {}".format(dataset_id))
    dataset = client.create_dataset(dataset)


@magic_arguments.magic_arguments()
@magic_arguments.argument(
    "destination_var",
    nargs="?",
    help=("If provided, save the output to this variable instead of displaying it."),
)
@magic_arguments.argument(
    "--destination_table",
    type=str,
    default=None,
    help=(
        "If provided, save the output of the query to a new BigQuery table. "
        "Variable should be in a format <dataset_id>.<table_id>. "
        "If table does not exists, it will be created. "
        "If table already exists, its data will be overwritten."
    ),
)
@magic_arguments.argument(
    "--project",
    type=str,
    default=None,
    help=("Project to use for executing this query. Defaults to the context project."),
)
@magic_arguments.argument(
    "--max_results",
    default=None,
    help=(
        "Maximum number of rows in dataframe returned from executing the query."
        "Defaults to returning all rows."
    ),
)
@magic_arguments.argument(
    "--maximum_bytes_billed",
    default=None,
    help=(
        "maximum_bytes_billed to use for executing this query. Defaults to "
        "the context default_query_job_config.maximum_bytes_billed."
    ),
)
@magic_arguments.argument(
    "--dry_run",
    action="store_true",
    default=False,
    help=(
        "Sets query to be a dry run to estimate costs. "
        "Defaults to executing the query instead of dry run if this argument is not used."
    ),
)
@magic_arguments.argument(
    "--use_legacy_sql",
    action="store_true",
    default=False,
    help=(
        "Sets query to use Legacy SQL instead of Standard SQL. Defaults to "
        "Standard SQL if this argument is not used."
    ),
)
@magic_arguments.argument(
    "--use_bqstorage_api",
    action="store_true",
    default=False,
    help=(
        "[Beta] Use the BigQuery Storage API to download large query results. "
        "To use this option, install the google-cloud-bigquery-storage and "
        "fastavro packages, and enable the BigQuery Storage API."
    ),
)
@magic_arguments.argument(
    "--verbose",
    action="store_true",
    default=False,
    help=(
        "If set, print verbose output, including the query job ID and the "
        "amount of time for the query to finish. By default, this "
        "information will be displayed as the query runs, but will be "
        "cleared after the query is finished."
    ),
)
@magic_arguments.argument(
    "--params",
    nargs="+",
    default=None,
    help=(
        "Parameters to format the query string. If present, the --params "
        "flag should be followed by a string representation of a dictionary "
        "in the format {'param_name': 'param_value'} (ex. {\"num\": 17}), "
        "or a reference to a dictionary in the same format. The dictionary "
        "reference can be made by including a '$' before the variable "
        "name (ex. $my_dict_var)."
    ),
)
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

    params = []
    if args.params is not None:
        try:
            params = _helpers.to_query_parameters(
                ast.literal_eval("".join(args.params))
            )
        except Exception:
            raise SyntaxError(
                "--params is not a correctly formatted JSON string or a JSON "
                "serializable dictionary"
            )

    project = args.project or context.project
    client = bigquery.Client(
        project=project,
        credentials=context.credentials,
        default_query_job_config=context.default_query_job_config,
        client_info=client_info.ClientInfo(user_agent=IPYTHON_USER_AGENT),
    )
    if context._connection:
        client._connection = context._connection
    bqstorage_client = _make_bqstorage_client(
        args.use_bqstorage_api or context.use_bqstorage_api, context.credentials
    )

    close_transports = functools.partial(_close_transports, client, bqstorage_client)

    try:
        if args.max_results:
            max_results = int(args.max_results)
        else:
            max_results = None

        query = query.strip()

        # Any query that does not contain whitespace (aside from leading and trailing whitespace)
        # is assumed to be a table id
        if not re.search(r"\s", query):
            try:
                rows = client.list_rows(query, max_results=max_results)
            except Exception as ex:
                _handle_error(ex, args.destination_var)
                return

            result = rows.to_dataframe(bqstorage_client=bqstorage_client)
            if args.destination_var:
                IPython.get_ipython().push({args.destination_var: result})
                return
            else:
                return result

        job_config = bigquery.job.QueryJobConfig()
        job_config.query_parameters = params
        job_config.use_legacy_sql = args.use_legacy_sql
        job_config.dry_run = args.dry_run

        if args.destination_table:
            split = args.destination_table.split(".")
            if len(split) != 2:
                raise ValueError(
                    "--destination_table should be in a <dataset_id>.<table_id> format."
                )
            dataset_id, table_id = split
            job_config.allow_large_results = True
            dataset_ref = bigquery.dataset.DatasetReference(client.project, dataset_id)
            destination_table_ref = dataset_ref.table(table_id)
            job_config.destination = destination_table_ref
            job_config.create_disposition = "CREATE_IF_NEEDED"
            job_config.write_disposition = "WRITE_TRUNCATE"
            _create_dataset_if_necessary(client, dataset_id)

        if args.maximum_bytes_billed == "None":
            job_config.maximum_bytes_billed = 0
        elif args.maximum_bytes_billed is not None:
            value = int(args.maximum_bytes_billed)
            job_config.maximum_bytes_billed = value

        try:
            query_job = _run_query(client, query, job_config=job_config)
        except Exception as ex:
            _handle_error(ex, args.destination_var)
            return

        if not args.verbose:
            display.clear_output()

        if args.dry_run and args.destination_var:
            IPython.get_ipython().push({args.destination_var: query_job})
            return
        elif args.dry_run:
            print(
                "Query validated. This query will process {} bytes.".format(
                    query_job.total_bytes_processed
                )
            )
            return query_job

        if max_results:
            result = query_job.result(max_results=max_results).to_dataframe(
                bqstorage_client=bqstorage_client
            )
        else:
            result = query_job.to_dataframe(bqstorage_client=bqstorage_client)

        if args.destination_var:
            IPython.get_ipython().push({args.destination_var: result})
        else:
            return result
    finally:
        close_transports()


def _make_bqstorage_client(use_bqstorage_api, credentials):
    if not use_bqstorage_api:
        return None

    try:
        from google.cloud import bigquery_storage_v1beta1
    except ImportError as err:
        customized_error = ImportError(
            "Install the google-cloud-bigquery-storage and pyarrow packages "
            "to use the BigQuery Storage API."
        )
        six.raise_from(customized_error, err)

    try:
        from google.api_core.gapic_v1 import client_info as gapic_client_info
    except ImportError as err:
        customized_error = ImportError(
            "Install the grpcio package to use the BigQuery Storage API."
        )
        six.raise_from(customized_error, err)

    return bigquery_storage_v1beta1.BigQueryStorageClient(
        credentials=credentials,
        client_info=gapic_client_info.ClientInfo(user_agent=IPYTHON_USER_AGENT),
    )


def _close_transports(client, bqstorage_client):
    """Close the given clients' underlying transport channels.

    Closing the transport is needed to release system resources, namely open
    sockets.

    Args:
        client (:class:`~google.cloud.bigquery.client.Client`):
        bqstorage_client
            (Optional[:class:`~google.cloud.bigquery_storage_v1beta1.BigQueryStorageClient`]):
            A client for the BigQuery Storage API.

    """
    client.close()
    if bqstorage_client is not None:
        bqstorage_client.transport.channel.close()
