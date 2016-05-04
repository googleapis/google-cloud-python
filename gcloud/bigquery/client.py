# Copyright 2015 Google Inc. All rights reserved.
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


from gcloud.client import JSONClient
from gcloud.bigquery.connection import Connection
from gcloud.bigquery.dataset import Dataset
from gcloud.bigquery.job import CopyJob
from gcloud.bigquery.job import ExtractTableToStorageJob
from gcloud.bigquery.job import LoadTableFromStorageJob
from gcloud.bigquery.job import QueryJob
from gcloud.bigquery.query import QueryResults


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a dataset / job.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def list_datasets(self, include_all=False, max_results=None,
                      page_token=None):
        """List datasets for the project associated with this client.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/datasets/list

        :type include_all: boolean
        :param include_all: True if results include hidden datasets.

        :type max_results: int
        :param max_results: maximum number of datasets to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of datasets. If
                           not passed, the API will return the first page of
                           datasets.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.bigquery.dataset.Dataset`, plus a
                  "next page token" string:  if the token is not None,
                  indicates that more datasets can be retrieved with another
                  call (pass that value as ``page_token``).
        """
        params = {}

        if include_all:
            params['all'] = True

        if max_results is not None:
            params['maxResults'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/datasets' % (self.project,)
        resp = self.connection.api_request(method='GET', path=path,
                                           query_params=params)
        datasets = [Dataset.from_api_repr(resource, self)
                    for resource in resp.get('datasets', ())]
        return datasets, resp.get('nextPageToken')

    def dataset(self, dataset_name):
        """Construct a dataset bound to this client.

        :type dataset_name: str
        :param dataset_name: Name of the dataset.

        :rtype: :class:`gcloud.bigquery.dataset.Dataset`
        :returns: a new ``Dataset`` instance
        """
        return Dataset(dataset_name, client=self)

    def job_from_resource(self, resource):
        """Detect correct job type from resource and instantiate.

        :type resource: dict
        :param resource: one job resource from API response

        :rtype: One of:
                :class:`gcloud.bigquery.job.LoadTableFromStorageJob`,
                :class:`gcloud.bigquery.job.CopyJob`,
                :class:`gcloud.bigquery.job.ExtractTableToStorageJob`,
                :class:`gcloud.bigquery.job.QueryJob`,
                :class:`gcloud.bigquery.job.RunSyncQueryJob`
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
        https://cloud.google.com/bigquery/docs/reference/v2/jobs/list

        :type max_results: int
        :param max_results: maximum number of jobs to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of jobs. If
                           not passed, the API will return the first page of
                           jobs.

        :type all_users: boolean
        :param all_users: if true, include jobs owned by all users in the
                          project.

        :type state_filter: str
        :param state_filter: if passed, include only jobs matching the given
                             state.  One of

                             * ``"done"``
                             * ``"pending"``
                             * ``"running"``

        :rtype: tuple, (list, str)
        :returns: list of job instances, plus a "next page token" string:
                  if the token is not ``None``, indicates that more jobs can be
                  retrieved with another call, passing that value as
                  ``page_token``).
        """
        params = {'projection': 'full'}

        if max_results is not None:
            params['maxResults'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        if all_users is not None:
            params['allUsers'] = all_users

        if state_filter is not None:
            params['stateFilter'] = state_filter

        path = '/projects/%s/jobs' % (self.project,)
        resp = self.connection.api_request(method='GET', path=path,
                                           query_params=params)
        jobs = [self.job_from_resource(resource) for resource in resp['jobs']]
        return jobs, resp.get('nextPageToken')

    def load_table_from_storage(self, job_name, destination, *source_uris):
        """Construct a job for loading data into a table from CloudStorage.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.load

        :type job_name: str
        :param job_name: Name of the job.

        :type destination: :class:`gcloud.bigquery.table.Table`
        :param destination: Table into which data is to be loaded.

        :type source_uris: sequence of string
        :param source_uris: URIs of data files to be loaded; in format
                            ``gs://<bucket_name>/<object_name_or_glob>``.

        :rtype: :class:`gcloud.bigquery.job.LoadTableFromStorageJob`
        :returns: a new ``LoadTableFromStorageJob`` instance
        """
        return LoadTableFromStorageJob(job_name, destination, source_uris,
                                       client=self)

    def copy_table(self, job_name, destination, *sources):
        """Construct a job for copying one or more tables into another table.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.copy

        :type job_name: str
        :param job_name: Name of the job.

        :type destination: :class:`gcloud.bigquery.table.Table`
        :param destination: Table into which data is to be copied.

        :type sources: sequence of :class:`gcloud.bigquery.table.Table`
        :param sources: tables to be copied.

        :rtype: :class:`gcloud.bigquery.job.CopyJob`
        :returns: a new ``CopyJob`` instance
        """
        return CopyJob(job_name, destination, sources, client=self)

    def extract_table_to_storage(self, job_name, source, *destination_uris):
        """Construct a job for extracting a table into Cloud Storage files.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.extract

        :type job_name: str
        :param job_name: Name of the job.

        :type source: :class:`gcloud.bigquery.table.Table`
        :param source: table to be extracted.

        :type destination_uris: sequence of string
        :param destination_uris: URIs of CloudStorage file(s) into which
                                 table data is to be extracted; in format
                                 ``gs://<bucket_name>/<object_name_or_glob>``.

        :rtype: :class:`gcloud.bigquery.job.ExtractTableToStorageJob`
        :returns: a new ``ExtractTableToStorageJob`` instance
        """
        return ExtractTableToStorageJob(job_name, source, destination_uris,
                                        client=self)

    def run_async_query(self, job_name, query):
        """Construct a job for running a SQL query asynchronously.

        See:
        https://cloud.google.com/bigquery/docs/reference/v2/jobs#configuration.query

        :type job_name: str
        :param job_name: Name of the job.

        :type query: str
        :param query: SQL query to be executed

        :rtype: :class:`gcloud.bigquery.job.QueryJob`
        :returns: a new ``QueryJob`` instance
        """
        return QueryJob(job_name, query, client=self)

    def run_sync_query(self, query):
        """Run a SQL query synchronously.

        :type query: str
        :param query: SQL query to be executed

        :rtype: :class:`gcloud.bigquery.query.QueryResults`
        :returns: a new ``QueryResults`` instance
        """
        return QueryResults(query, client=self)
