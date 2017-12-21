import time
from concurrent import futures

try:
    import IPython
except ImportError:
    raise Exception('This module can only be loaded in IPython.')

from google.cloud.bigquery.client import Client
from google.cloud.bigquery.job import QueryJobConfig


class Context(object):
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = Client()
        return self._client

    @client.setter
    def client(self, value):
        self._client = value


context = Context()


def run_query(query, project=None, job_config=None):
    start_time = time.time()
    client = Client(project=project)
    query_job = client.query(query, job_id_prefix='query-',
                             job_config=job_config)
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


@IPython.core.magic.register_cell_magic('bigquery')
@IPython.core.magic_arguments.magic_arguments()
@IPython.core.magic_arguments.argument(
    'destination_var',
    nargs='?',
    help=('If provided, save the output to this variable in addition '
          'to displaying it.'))
@IPython.core.magic_arguments.argument(
    '--project',
    type=str,
    default=None,
    help=('Project to use for executing this query. Defaults to the '
          'client\'s project'))
@IPython.core.magic_arguments.argument(
    '--use_legacy_sql', action='store_true', default=False,
    help='If set, use legacy SQL instead of standard SQL.')
@IPython.core.magic_arguments.argument(
    '--verbose', action='store_true', default=False,
    help='If set, print verbose output.')
def _cell_magic(line, query):
    args = IPython.core.magic_arguments.parse_argstring(_cell_magic, line)

    client = context.client
    project = args.project or client.project
    job_config = QueryJobConfig()
    job_config.use_legacy_sql = args.use_legacy_sql
    job_id = run_query(query, project, job_config)

    if not args.verbose:
        IPython.display.clear_output()

    # Fetch the results.
    result = client.get_job(job_id, project=project).to_dataframe()
    if args.destination_var:
        IPython.get_ipython().push({args.destination_var: result})
    return result
