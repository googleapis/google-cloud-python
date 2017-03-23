# Copyright 2015 Google Inc.
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

"""Client for interacting with the Google BigQuery API."""


from google.cloud.client import ClientWithProject
from google.cloud.bigquery._http import Connection
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.job import CopyJob
from google.cloud.bigquery.job import ExtractTableToStorageJob
from google.cloud.bigquery.job import LoadTableFromStorageJob
from google.cloud.bigquery.job import QueryJob
from google.cloud.bigquery.query import QueryResults
from google.cloud.iterator import HTTPIterator


class Project(object):
    """Wrapper for resource describing a BigQuery project.

    :type project_id: str
    :param project_id: Opaque ID of the project

    :type numeric_id: int
    :param numeric_id: Numeric ID of the project

    :type friendly_name: str
    :param friendly_name: Display name of the project
    """
    def __init__(self, project_id, numeric_id, friendly_name):
        self.project_id = project_id
        self.numeric_id = numeric_id
        self.friendly_name = friendly_name

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct an instance from a resource dict."""
        return cls(
            resource['id'], resource['numericId'], resource['friendlyName'])


class Client(ClientWithProject):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a dataset / job.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type http: :class:`~httplib2.Http`
    :param http: (Optional) HTTP object to make requests. Can be any object
                 that defines ``request()`` with the same interface as
                 :meth:`~httplib2.Http.request`. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    SCOPE = ('https://www.googleapis.com/auth/bigquery',
             'https://www.googleapis.com/auth/cloud-platform')
    """The scopes required for authenticating as a BigQuery consumer."""

    def __init__(self, project=None, credentials=None, http=None):
        super(Client, self).__init__(
            project=project, credentials=credentials, http=http)
        self._connection = Connection(self)

    def list_projects(self, max_results=None, page_token=None):
        """List projects for the project associated with this client.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/projects/list

        :type max_results: int
        :param max_results: maximum number of projects to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of projects. If
                           not passed, the API will return the first page of
                           projects.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.bigquery.client.Project`
                  accessible to the current client.
        """
        return HTTPIterator(
            client=self, path='/projects', item_to_value=_item_to_project,
            items_key='projects', page_token=page_token,
            max_results=max_results)

    def list_datasets(self, include_all=False, max_results=None,
                      page_token=None):
        """List datasets for the project associated with this client.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list

        :type include_all: bool
        :param include_all: True if results include hidden datasets.

        :type max_results: int
        :param max_results: maximum number of datasets to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of datasets. If
                           not passed, the API will return the first page of
                           datasets.

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.bigquery.dataset.Dataset`.
                  accessible to the current client.
        """
        extra_params = {}
        if include_all:
            extra_params['all'] = True
        path = '/projects/%s/datasets' % (self.project,)
        return HTTPIterator(
            client=self, path=path, item_to_value=_item_to_dataset,
            items_key='datasets', page_token=page_token,
            max_results=max_results, extra_params=extra_params)

    def dataset(self, dataset_name, project=None):
        """Construct a dataset bound to this client.

        :type dataset_name: str
        :param dataset_name: Name of the dataset.

        :type project: str
        :param project: (Optional) project ID for the dataset (defaults to
                        the project of the client).

        :rtype: :class:`google.cloud.bigquery.dataset.Dataset`
        :returns: a new ``Dataset`` instance
        """
        return Dataset(dataset_name, client=self, project=project)

    def job_from_resource(self, resource):
        """Detect correct job type from resource and instantiate.

        :type resource: dict
        :param resource: one job resource from API response

        :rtype: One of:
                :class:`google.cloud.bigquery.job.LoadTableFromStorageJob`,
                :class:`google.cloud.bigquery.job.CopyJob`,
                :class:`google.cloud.bigquery.job.ExtractTableToStorageJob`,
                :class:`google.cloud.bigquery.job.QueryJob`,
                :class:`google.cloud.bigquery.job.RunSyncQueryJob`
        :returns: the job instance, constructed via the resource
        """
        config = resource['configuration']
        if 'load' in config:
            return LoadTableFromStorageJob.from_api_repr(resource, self)
        elif 'copy' in config:
            return CopyJob.from_api_repr(resource, self)
        elif 'extract' in config:
            return ExtractTableToStorageJob.from_api_repr(resource, self)
        elif 'query' in config:
            return QueryJob.from_api_repr(resource, self)
        raise ValueError('Cannot parse job resource')

    def list_jobs(self, max_results=None, page_token=None, all_users=None,
                  state_filter=None):
        """List jobs for the project associated with this client.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/list

        :type max_results: int
        :param max_results: maximum number of jobs to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of jobs. If
                           not passed, the API will return the first page of
                           jobs.

        :type all_users: bool
        :param all_users: if true, include jobs owned by all users in the
                          project.

        :type state_filter: str
        :param state_filter: if passed, include only jobs matching the given
                             state.  One of

                             * ``"done"``
                             * ``"pending"``
                             * ``"running"``

        :rtype: :class:`~google.cloud.iterator.Iterator`
        :returns: Iterable of job instances.
        """
        extra_params = {'projection': 'full'}

        if all_users is not None:
            extra_params['allUsers'] = all_users

        if state_filter is not None:
            extra_params['stateFilter'] = state_filter

        path = '/projects/%s/jobs' % (self.project,)
        return HTTPIterator(
            client=self, path=path, item_to_value=_item_to_job,
            items_key='jobs', page_token=page_token,
            max_results=max_results, extra_params=extra_params)

    def load_table_from_storage(self, job_name, destination, *source_uris):
        """Construct a job for loading data into a table from CloudStorage.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load

        :type job_name: str
        :param job_name: Name of the job.

        :type destination: :class:`google.cloud.bigquery.table.Table`
        :param destination: Table into which data is to be loaded.

        :type source_uris: sequence of string
        :param source_uris: URIs of data files to be loaded; in format
                            ``gs://<bucket_name>/<object_name_or_glob>``.

        :rtype: :class:`google.cloud.bigquery.job.LoadTableFromStorageJob`
        :returns: a new ``LoadTableFromStorageJob`` instance
        """
        return LoadTableFromStorageJob(job_name, destination, source_uris,
                                       client=self)

    def copy_table(self, job_name, destination, *sources):
        """Construct a job for copying one or more tables into another table.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy

        :type job_name: str
        :param job_name: Name of the job.

        :type destination: :class:`google.cloud.bigquery.table.Table`
        :param destination: Table into which data is to be copied.

        :type sources: sequence of :class:`google.cloud.bigquery.table.Table`
        :param sources: tables to be copied.

        :rtype: :class:`google.cloud.bigquery.job.CopyJob`
        :returns: a new ``CopyJob`` instance
        """
        return CopyJob(job_name, destination, sources, client=self)

    def extract_table_to_storage(self, job_name, source, *destination_uris):
        """Construct a job for extracting a table into Cloud Storage files.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract

        :type job_name: str
        :param job_name: Name of the job.

        :type source: :class:`google.cloud.bigquery.table.Table`
        :param source: table to be extracted.

        :type destination_uris: sequence of string
        :param destination_uris: URIs of CloudStorage file(s) into which
                                 table data is to be extracted; in format
                                 ``gs://<bucket_name>/<object_name_or_glob>``.

        :rtype: :class:`google.cloud.bigquery.job.ExtractTableToStorageJob`
        :returns: a new ``ExtractTableToStorageJob`` instance
        """
        return ExtractTableToStorageJob(job_name, source, destination_uris,
                                        client=self)

    def run_async_query(self, job_name, query,
                        udf_resources=(), query_parameters=()):
        """Construct a job for running a SQL query asynchronously.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query

        :type job_name: str
        :param job_name: Name of the job.

        :type query: str
        :param query: SQL query to be executed

        :type udf_resources: tuple
        :param udf_resources: An iterable of
                            :class:`google.cloud.bigquery._helpers.UDFResource`
                            (empty by default)

        :type query_parameters: tuple
        :param query_parameters:
            An iterable of
            :class:`google.cloud.bigquery._helpers.AbstractQueryParameter`
            (empty by default)

        :rtype: :class:`google.cloud.bigquery.job.QueryJob`
        :returns: a new ``QueryJob`` instance
        """
        return QueryJob(job_name, query, client=self,
                        udf_resources=udf_resources,
                        query_parameters=query_parameters)

    def run_sync_query(self, query, udf_resources=(), query_parameters=()):
        """Run a SQL query synchronously.

        :type query: str
        :param query: SQL query to be executed

        :type udf_resources: tuple
        :param udf_resources: An iterable of
                            :class:`google.cloud.bigquery._helpers.UDFResource`
                            (empty by default)

        :type query_parameters: tuple
        :param query_parameters:
            An iterable of
            :class:`google.cloud.bigquery._helpers.AbstractQueryParameter`
            (empty by default)

        :rtype: :class:`google.cloud.bigquery.query.QueryResults`
        :returns: a new ``QueryResults`` instance
        """
        return QueryResults(query, client=self,
                            udf_resources=udf_resources,
                            query_parameters=query_parameters)


# pylint: disable=unused-argument
def _item_to_project(iterator, resource):
    """Convert a JSON project to the native object.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a project.

    :rtype: :class:`.Project`
    :returns: The next project in the page.
    """
    return Project.from_api_repr(resource)
# pylint: enable=unused-argument


def _item_to_dataset(iterator, resource):
    """Convert a JSON dataset to the native object.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a dataset.

    :rtype: :class:`.Dataset`
    :returns: The next dataset in the page.
    """
    return Dataset.from_api_repr(resource, iterator.client)


def _item_to_job(iterator, resource):
    """Convert a JSON job to the native object.

    :type iterator: :class:`~google.cloud.iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a job.

    :rtype: job instance.
    :returns: The next job in the page.
    """
    return iterator.client.job_from_resource(resource)
