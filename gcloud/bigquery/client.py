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
from gcloud.bigquery.job import RunAsyncQueryJob
from gcloud.bigquery.job import RunSyncQueryJob


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: string
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

        :type page_token: string
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
                    for resource in resp['datasets']]
        return datasets, resp.get('nextPageToken')

    def dataset(self, name):
        """Construct a dataset bound to this client.

        :type name: string
        :param name: Name of the dataset.

        :rtype: :class:`gcloud.bigquery.dataset.Dataset`
        :returns: a new ``Dataset`` instance
        """
        return Dataset(name, client=self)

    def load_table_from_storage(self, name, destination, *source_uris):
        """Construct a job for loading data into a table from CloudStorage.

        :type name: string
        :param name: Name of the job.

        :type destination: :class:`gcloud.bigquery.table.Table`
        :param destination: Table into which data is to be loaded.

        :type source_uris: sequence of string
        :param source_uris: URIs of data files to be loaded.

        :rtype: :class:`gcloud.bigquery.job.LoadTableFromStorageJob`
        :returns: a new ``LoadTableFromStorageJob`` instance
        """
        return LoadTableFromStorageJob(name, destination, source_uris,
                                       client=self)

    def copy_table(self, name, destination, *sources):
        """Construct a job for copying one or more tables into another table.

        :type name: string
        :param name: Name of the job.

        :type destination: :class:`gcloud.bigquery.table.Table`
        :param destination: Table into which data is to be copied.

        :type sources: sequence of :class:`gcloud.bigquery.table.Table`
        :param sources: tables to be copied.

        :rtype: :class:`gcloud.bigquery.job.CopyJob`
        :returns: a new ``CopyJob`` instance
        """
        return CopyJob(name, destination, sources, client=self)

    def extract_table_to_storage(self, name, source, *destination_uris):
        """Construct a job for extracting a table into Cloud Storage files.

        :type name: string
        :param name: Name of the job.

        :type source: :class:`gcloud.bigquery.table.Table`
        :param source: table to be extracted.

        :type destination_uris: sequence of string
        :param destination_uris: URIs of CloudStorage file(s) into which
                                 table data is to be extracted.

        :rtype: :class:`gcloud.bigquery.job.ExtractTableToStorageJob`
        :returns: a new ``ExtractTableToStorageJob`` instance
        """
        return ExtractTableToStorageJob(name, source, destination_uris,
                                        client=self)

    def run_async_query(self, name, query):
        """Construct a job for running a SQL query asynchronously.

        :type name: string
        :param name: Name of the job.

        :type query: string
        :param query: SQL query to be executed

        :rtype: :class:`gcloud.bigquery.job.RunAsyncQueryJob`
        :returns: a new ``RunAsyncQueryJob`` instance
        """
        return RunAsyncQueryJob(name, query, client=self)

    def run_sync_query(self, query):
        """Construct a job for running a SQL query synchronously.

        :type query: string
        :param query: SQL query to be executed

        :rtype: :class:`gcloud.bigquery.job.RunSyncQueryJob`
        :returns: a new ``RunSyncQueryJob`` instance
        """
        return RunSyncQueryJob(query, client=self)
