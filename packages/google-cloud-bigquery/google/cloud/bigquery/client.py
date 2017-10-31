# Copyright 2015 Google LLC
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

from __future__ import absolute_import

import collections
import concurrent.futures
import functools
import os
import uuid

import six

from google import resumable_media
from google.resumable_media.requests import MultipartUpload
from google.resumable_media.requests import ResumableUpload

from google.api_core import page_iterator
from google.api_core.exceptions import GoogleAPICallError
from google.api_core.exceptions import NotFound

from google.cloud import exceptions
from google.cloud.client import ClientWithProject
from google.cloud.bigquery._http import Connection
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery.table import Table, _TABLE_HAS_NO_SCHEMA
from google.cloud.bigquery.table import TableReference
from google.cloud.bigquery.table import _row_from_mapping
from google.cloud.bigquery.job import CopyJob
from google.cloud.bigquery.job import ExtractJob
from google.cloud.bigquery.job import LoadJob
from google.cloud.bigquery.job import QueryJob, QueryJobConfig
from google.cloud.bigquery.query import QueryResults
from google.cloud.bigquery._helpers import _item_to_row
from google.cloud.bigquery._helpers import _rows_page_start
from google.cloud.bigquery._helpers import _field_to_index_mapping
from google.cloud.bigquery._helpers import _SCALAR_VALUE_TO_JSON_ROW
from google.cloud.bigquery._helpers import DEFAULT_RETRY
from google.cloud.bigquery._helpers import _snake_to_camel_case


_DEFAULT_CHUNKSIZE = 1048576  # 1024 * 1024 B = 1 MB
_MAX_MULTIPART_SIZE = 5 * 1024 * 1024
_DEFAULT_NUM_RETRIES = 6
_BASE_UPLOAD_TEMPLATE = (
    u'https://www.googleapis.com/upload/bigquery/v2/projects/'
    u'{project}/jobs?uploadType=')
_MULTIPART_URL_TEMPLATE = _BASE_UPLOAD_TEMPLATE + u'multipart'
_RESUMABLE_URL_TEMPLATE = _BASE_UPLOAD_TEMPLATE + u'resumable'
_GENERIC_CONTENT_TYPE = u'*/*'
_READ_LESS_THAN_SIZE = (
    'Size {:d} was specified but the file-like object only had '
    '{:d} bytes remaining.')


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
                        client. If not passed (and if no ``_http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type _http: :class:`~requests.Session`
    :param _http: (Optional) HTTP object to make requests. Can be any object
                  that defines ``request()`` with the same interface as
                  :meth:`requests.Session.request`. If not passed, an
                  ``_http`` object is created that is bound to the
                  ``credentials`` for the current object.
                  This parameter should be considered private, and could
                  change in the future.
    """

    SCOPE = ('https://www.googleapis.com/auth/bigquery',
             'https://www.googleapis.com/auth/cloud-platform')
    """The scopes required for authenticating as a BigQuery consumer."""

    def __init__(self, project=None, credentials=None, _http=None):
        super(Client, self).__init__(
            project=project, credentials=credentials, _http=_http)
        self._connection = Connection(self)

    def list_projects(self, max_results=None, page_token=None,
                      retry=DEFAULT_RETRY):
        """List projects for the project associated with this client.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/projects/list

        :type max_results: int
        :param max_results: maximum number of projects to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of projects. If
                           not passed, the API will return the first page of
                           projects.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.bigquery.client.Project`
                  accessible to the current client.
        """
        return page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path='/projects',
            item_to_value=_item_to_project,
            items_key='projects',
            page_token=page_token,
            max_results=max_results)

    def list_datasets(self, include_all=False, filter=None, max_results=None,
                      page_token=None, retry=DEFAULT_RETRY):
        """List datasets for the project associated with this client.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list

        :type include_all: bool
        :param include_all: True if results include hidden datasets.

        :type filter: str
        :param filter: an expression for filtering the results by label.
                       For syntax, see
                       https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list#filter.

        :type max_results: int
        :param max_results: maximum number of datasets to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: opaque marker for the next "page" of datasets. If
                           not passed, the API will return the first page of
                           datasets.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.bigquery.dataset.Dataset`.
                  accessible to the current client.
        """
        extra_params = {}
        if include_all:
            extra_params['all'] = True
        if filter:
            # TODO: consider supporting a dict of label -> value for filter,
            # and converting it into a string here.
            extra_params['filter'] = filter
        path = '/projects/%s/datasets' % (self.project,)
        return page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path=path,
            item_to_value=_item_to_dataset,
            items_key='datasets',
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params)

    def dataset(self, dataset_id, project=None):
        """Construct a reference to a dataset.

        :type dataset_id: str
        :param dataset_id: ID of the dataset.

        :type project: str
        :param project: (Optional) project ID for the dataset (defaults to
                        the project of the client).

        :rtype: :class:`google.cloud.bigquery.dataset.DatasetReference`
        :returns: a new ``DatasetReference`` instance
        """
        if project is None:
            project = self.project

        return DatasetReference(project, dataset_id)

    def create_dataset(self, dataset):
        """API call:  create the dataset via a PUT request.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert

        :type dataset: :class:`~google.cloud.bigquery.dataset.Dataset`
        :param dataset: A ``Dataset`` populated with the desired initial state.
                        If project is missing, it defaults to the project of
                        the client.

        :rtype: ":class:`~google.cloud.bigquery.dataset.Dataset`"
        :returns: a new ``Dataset`` returned from the service.
        """
        path = '/projects/%s/datasets' % (dataset.project,)
        api_response = self._connection.api_request(
            method='POST', path=path, data=dataset._build_resource())
        return Dataset.from_api_repr(api_response)

    def create_table(self, table):
        """API call:  create a table via a PUT request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert

        :type table: :class:`~google.cloud.bigquery.table.Table`
        :param table: A ``Table`` populated with the desired initial state.

        :rtype: ":class:`~google.cloud.bigquery.table.Table`"
        :returns: a new ``Table`` returned from the service.
        """
        path = '/projects/%s/datasets/%s/tables' % (
            table.project, table.dataset_id)
        resource = table._build_resource(Table.all_fields)
        doomed = [field for field in resource if resource[field] is None]
        for field in doomed:
            del resource[field]
        api_response = self._connection.api_request(
            method='POST', path=path, data=resource)
        return Table.from_api_repr(api_response)

    def _call_api(self, retry, **kwargs):
        call = functools.partial(self._connection.api_request, **kwargs)
        if retry:
            call = retry(call)
        return call()

    def get_dataset(self, dataset_ref, retry=DEFAULT_RETRY):
        """Fetch the dataset referenced by ``dataset_ref``

        :type dataset_ref:
            :class:`google.cloud.bigquery.dataset.DatasetReference`
        :param dataset_ref: the dataset to use.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`google.cloud.bigquery.dataset.Dataset`
        :returns: a ``Dataset`` instance
        """
        api_response = self._call_api(retry,
                                      method='GET',
                                      path=dataset_ref.path)
        return Dataset.from_api_repr(api_response)

    def get_table(self, table_ref, retry=DEFAULT_RETRY):
        """Fetch the table referenced by ``table_ref``

        :type table_ref:
            :class:`google.cloud.bigquery.table.TableReference`
        :param table_ref: the table to use.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`google.cloud.bigquery.table.Table`
        :returns: a ``Table`` instance
        """
        api_response = self._call_api(retry, method='GET', path=table_ref.path)
        return Table.from_api_repr(api_response)

    def update_dataset(self, dataset, fields, retry=DEFAULT_RETRY):
        """Change some fields of a dataset.

        Use ``fields`` to specify which fields to update. At least one field
        must be provided. If a field is listed in ``fields`` and is ``None`` in
        ``dataset``, it will be deleted.

        If ``dataset.etag`` is not ``None``, the update will only
        succeed if the dataset on the server has the same ETag. Thus
        reading a dataset with ``get_dataset``, changing its fields,
        and then passing it ``update_dataset`` will ensure that the changes
        will only be saved if no modifications to the dataset occurred
        since the read.

        :type dataset: :class:`google.cloud.bigquery.dataset.Dataset`
        :param dataset: the dataset to update.

        :type fields: sequence of string
        :param fields: the fields of ``dataset`` to change, spelled as the
                       Dataset properties (e.g. "friendly_name").

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`google.cloud.bigquery.dataset.Dataset`
        :returns: the modified ``Dataset`` instance
        """
        path = '/projects/%s/datasets/%s' % (dataset.project,
                                             dataset.dataset_id)
        partial = {}
        for f in fields:
            if not hasattr(dataset, f):
                raise ValueError('No Dataset field %s' % f)
            # All dataset attributes are trivially convertible to JSON except
            # for access entries.
            if f == 'access_entries':
                attr = dataset._build_access_resource()
                api_field = 'access'
            else:
                attr = getattr(dataset, f)
                api_field = _snake_to_camel_case(f)
            partial[api_field] = attr
        if dataset.etag is not None:
            headers = {'If-Match': dataset.etag}
        else:
            headers = None
        api_response = self._call_api(
            retry, method='PATCH', path=path, data=partial, headers=headers)
        return Dataset.from_api_repr(api_response)

    def update_table(self, table, properties, retry=DEFAULT_RETRY):
        """API call:  update table properties via a PUT request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/update

        :type table:
            :class:`google.cloud.bigquery.table.Table`
        :param table_ref: the table to update.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`google.cloud.bigquery.table.Table`
        :returns: a ``Table`` instance
        """
        partial = table._build_resource(properties)
        if table.etag is not None:
            headers = {'If-Match': table.etag}
        else:
            headers = None
        api_response = self._call_api(
            retry,
            method='PATCH', path=table.path, data=partial, headers=headers)
        return Table.from_api_repr(api_response)

    def list_dataset_tables(self, dataset, max_results=None, page_token=None,
                            retry=DEFAULT_RETRY):
        """List tables in the dataset.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/list

        :type dataset: One of:
                       :class:`~google.cloud.bigquery.dataset.Dataset`
                       :class:`~google.cloud.bigquery.dataset.DatasetReference`
        :param dataset: the dataset whose tables to list, or a reference to it.

        :type max_results: int
        :param max_results: (Optional) Maximum number of tables to return.
                            If not passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token: (Optional) Opaque marker for the next "page" of
                           datasets. If not passed, the API will return the
                           first page of datasets.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of :class:`~google.cloud.bigquery.table.Table`
                  contained within the current dataset.
        """
        if not isinstance(dataset, (Dataset, DatasetReference)):
            raise TypeError('dataset must be a Dataset or a DatasetReference')
        path = '%s/tables' % dataset.path
        result = page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path=path,
            item_to_value=_item_to_table,
            items_key='tables',
            page_token=page_token,
            max_results=max_results)
        result.dataset = dataset
        return result

    def delete_dataset(self, dataset, retry=DEFAULT_RETRY):
        """Delete a dataset.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/delete

        :type dataset: One of:
                       :class:`~google.cloud.bigquery.dataset.Dataset`
                       :class:`~google.cloud.bigquery.dataset.DatasetReference`

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :param dataset: the dataset to delete, or a reference to it.
        """
        if not isinstance(dataset, (Dataset, DatasetReference)):
            raise TypeError('dataset must be a Dataset or a DatasetReference')
        self._call_api(retry, method='DELETE', path=dataset.path)

    def delete_table(self, table, retry=DEFAULT_RETRY):
        """Delete a table

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete

        :type table: One of:
                     :class:`~google.cloud.bigquery.table.Table`
                     :class:`~google.cloud.bigquery.table.TableReference`
        :param table: the table to delete, or a reference to it.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.
        """
        if not isinstance(table, (Table, TableReference)):
            raise TypeError('table must be a Table or a TableReference')
        self._call_api(retry, method='DELETE', path=table.path)

    def _get_query_results(self, job_id, retry, project=None, timeout_ms=None):
        """Get the query results object for a query job.

        :type job_id: str
        :param job_id: Name of the query job.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :type project: str
        :param project:
            (Optional) project ID for the query job (defaults to the project of
            the client).

        :type timeout_ms: int
        :param timeout_ms:
            (Optional) number of milliseconds the the API call should wait for
            the query to complete before the request times out.

        :rtype: :class:`google.cloud.bigquery.query.QueryResults`
        :returns: a new ``QueryResults`` instance
        """

        extra_params = {'maxResults': 0}

        if project is None:
            project = self.project

        if timeout_ms is not None:
            extra_params['timeoutMs'] = timeout_ms

        path = '/projects/{}/queries/{}'.format(project, job_id)

        # This call is typically made in a polling loop that checks whether the
        # job is complete (from QueryJob.done(), called ultimately from
        # QueryJob.result()). So we don't need to poll here.
        resource = self._call_api(
            retry, method='GET', path=path, query_params=extra_params)
        return QueryResults.from_api_repr(resource)

    def job_from_resource(self, resource):
        """Detect correct job type from resource and instantiate.

        :type resource: dict
        :param resource: one job resource from API response

        :rtype: One of:
                :class:`google.cloud.bigquery.job.LoadJob`,
                :class:`google.cloud.bigquery.job.CopyJob`,
                :class:`google.cloud.bigquery.job.ExtractJob`,
                or :class:`google.cloud.bigquery.job.QueryJob`
        :returns: the job instance, constructed via the resource
        """
        config = resource['configuration']
        if 'load' in config:
            return LoadJob.from_api_repr(resource, self)
        elif 'copy' in config:
            return CopyJob.from_api_repr(resource, self)
        elif 'extract' in config:
            return ExtractJob.from_api_repr(resource, self)
        elif 'query' in config:
            return QueryJob.from_api_repr(resource, self)
        raise ValueError('Cannot parse job resource')

    def get_job(self, job_id, project=None, retry=DEFAULT_RETRY):
        """Fetch a job for the project associated with this client.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get

        :type job_id: str
        :param job_id: Name of the job.

        :type project: str
        :param project:
            project ID owning the job (defaults to the client's project)

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: One of:
                :class:`google.cloud.bigquery.job.LoadJob`,
                :class:`google.cloud.bigquery.job.CopyJob`,
                :class:`google.cloud.bigquery.job.ExtractJob`,
                or :class:`google.cloud.bigquery.job.QueryJob`
        :returns:
            Concrete job instance, based on the resource returned by the API.
        """
        extra_params = {'projection': 'full'}

        if project is None:
            project = self.project

        path = '/projects/{}/jobs/{}'.format(project, job_id)

        resource = self._call_api(
            retry, method='GET', path=path, query_params=extra_params)

        return self.job_from_resource(resource)

    def cancel_job(self, job_id, project=None, retry=DEFAULT_RETRY):
        """Attempt to cancel a job from a job ID.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/cancel

        :type job_id: str
        :param job_id: Name of the job.

        :type project: str
        :param project:
            project ID owning the job (defaults to the client's project)

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: One of:
                :class:`google.cloud.bigquery.job.LoadJob`,
                :class:`google.cloud.bigquery.job.CopyJob`,
                :class:`google.cloud.bigquery.job.ExtractJob`,
                or :class:`google.cloud.bigquery.job.QueryJob`
        :returns:
            Concrete job instance, based on the resource returned by the API.
        """
        extra_params = {'projection': 'full'}

        if project is None:
            project = self.project

        path = '/projects/{}/jobs/{}/cancel'.format(project, job_id)

        resource = self._call_api(
            retry, method='POST', path=path, query_params=extra_params)

        return self.job_from_resource(resource['job'])

    def list_jobs(self, max_results=None, page_token=None, all_users=None,
                  state_filter=None, retry=DEFAULT_RETRY):
        """List jobs for the project associated with this client.

        See
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

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterable of job instances.
        """
        extra_params = {'projection': 'full'}

        if all_users is not None:
            extra_params['allUsers'] = all_users

        if state_filter is not None:
            extra_params['stateFilter'] = state_filter

        path = '/projects/%s/jobs' % (self.project,)
        return page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path=path,
            item_to_value=_item_to_job,
            items_key='jobs',
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params)

    def load_table_from_uri(self, source_uris, destination,
                            job_id=None, job_id_prefix=None,
                            job_config=None, retry=DEFAULT_RETRY):
        """Starts a job for loading data into a table from CloudStorage.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load

        :type source_uris: One of:
                           str
                           sequence of string
        :param source_uris: URIs of data files to be loaded; in format
                            ``gs://<bucket_name>/<object_name_or_glob>``.

        :type destination: :class:`google.cloud.bigquery.table.TableReference`
        :param destination: Table into which data is to be loaded.

        :type job_id: str
        :param job_id: (Optional) Name of the job.

        :type job_id_prefix: str or ``NoneType``
        :param job_id_prefix: (Optional) the user-provided prefix for a
                              randomly generated job ID. This parameter will be
                              ignored if a ``job_id`` is also given.

        :type job_config: :class:`google.cloud.bigquery.job.LoadJobConfig`
        :param job_config: (Optional) Extra configuration options for the job.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`google.cloud.bigquery.job.LoadJob`
        :returns: a new :class:`~google.cloud.bigquery.job.LoadJob` instance
        """
        job_id = _make_job_id(job_id, job_id_prefix)
        if isinstance(source_uris, six.string_types):
            source_uris = [source_uris]
        job = LoadJob(job_id, source_uris, destination, self, job_config)
        job._begin(retry=retry)
        return job

    def load_table_from_file(self, file_obj, destination,
                             rewind=False,
                             size=None,
                             num_retries=_DEFAULT_NUM_RETRIES,
                             job_id=None, job_id_prefix=None, job_config=None):
        """Upload the contents of this table from a file-like object.

        Like load_table_from_uri, this creates, starts and returns
        a ``LoadJob``.

        :type file_obj: file
        :param file_obj: A file handle opened in binary mode for reading.

        :type destination: :class:`google.cloud.bigquery.table.TableReference`
        :param destination: Table into which data is to be loaded.

        :type rewind: bool
        :param rewind: If True, seek to the beginning of the file handle before
                       reading the file.

        :type size: int
        :param size: The number of bytes to read from the file handle.
                     If size is ``None`` or large, resumable upload will be
                     used. Otherwise, multipart upload will be used.

        :type num_retries: int
        :param num_retries: Number of upload retries. Defaults to 6.

        :type job_id: str
        :param job_id: (Optional) Name of the job.

        :type job_id_prefix: str or ``NoneType``
        :param job_id_prefix: (Optional) the user-provided prefix for a
                              randomly generated job ID. This parameter will be
                              ignored if a ``job_id`` is also given.

        :type job_config: :class:`google.cloud.bigquery.job.LoadJobConfig`
        :param job_config: (Optional) Extra configuration options for the job.

        :rtype: :class:`~google.cloud.bigquery.job.LoadJob`

        :returns: the job instance used to load the data (e.g., for
                  querying status).
        :raises: :class:`ValueError` if ``size`` is not passed in and can not
                 be determined, or if the ``file_obj`` can be detected to be
                 a file opened in text mode.
        """
        job_id = _make_job_id(job_id, job_id_prefix)
        job = LoadJob(job_id, None, destination, self, job_config)
        job_resource = job._build_resource()
        if rewind:
            file_obj.seek(0, os.SEEK_SET)
        _check_mode(file_obj)
        try:
            if size is None or size >= _MAX_MULTIPART_SIZE:
                response = self._do_resumable_upload(
                    file_obj, job_resource, num_retries)
            else:
                response = self._do_multipart_upload(
                    file_obj, job_resource, size, num_retries)
        except resumable_media.InvalidResponse as exc:
            raise exceptions.from_http_response(exc.response)
        return self.job_from_resource(response.json())

    def _do_resumable_upload(self, stream, metadata, num_retries):
        """Perform a resumable upload.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type metadata: dict
        :param metadata: The metadata associated with the upload.

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :rtype: :class:`~requests.Response`
        :returns: The "200 OK" response object returned after the final chunk
                  is uploaded.
        """
        upload, transport = self._initiate_resumable_upload(
            stream, metadata, num_retries)

        while not upload.finished:
            response = upload.transmit_next_chunk(transport)

        return response

    def _initiate_resumable_upload(self, stream, metadata, num_retries):
        """Initiate a resumable upload.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type metadata: dict
        :param metadata: The metadata associated with the upload.

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :rtype: tuple
        :returns:
            Pair of

            * The :class:`~google.resumable_media.requests.ResumableUpload`
              that was created
            * The ``transport`` used to initiate the upload.
        """
        chunk_size = _DEFAULT_CHUNKSIZE
        transport = self._http
        headers = _get_upload_headers(self._connection.USER_AGENT)
        upload_url = _RESUMABLE_URL_TEMPLATE.format(project=self.project)
        # TODO: modify ResumableUpload to take a retry.Retry object
        # that it can use for the initial RPC.
        upload = ResumableUpload(upload_url, chunk_size, headers=headers)

        if num_retries is not None:
            upload._retry_strategy = resumable_media.RetryStrategy(
                max_retries=num_retries)

        upload.initiate(
            transport, stream, metadata, _GENERIC_CONTENT_TYPE,
            stream_final=False)

        return upload, transport

    def _do_multipart_upload(self, stream, metadata, size, num_retries):
        """Perform a multipart upload.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type metadata: dict
        :param metadata: The metadata associated with the upload.

        :type size: int
        :param size: The number of bytes to be uploaded (which will be read
                     from ``stream``). If not provided, the upload will be
                     concluded once ``stream`` is exhausted (or :data:`None`).

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :rtype: :class:`~requests.Response`
        :returns: The "200 OK" response object returned after the multipart
                  upload request.
        :raises: :exc:`ValueError` if the ``stream`` has fewer than ``size``
                 bytes remaining.
        """
        data = stream.read(size)
        if len(data) < size:
            msg = _READ_LESS_THAN_SIZE.format(size, len(data))
            raise ValueError(msg)

        headers = _get_upload_headers(self._connection.USER_AGENT)

        upload_url = _MULTIPART_URL_TEMPLATE.format(project=self.project)
        upload = MultipartUpload(upload_url, headers=headers)

        if num_retries is not None:
            upload._retry_strategy = resumable_media.RetryStrategy(
                max_retries=num_retries)

        response = upload.transmit(
            self._http, data, metadata, _GENERIC_CONTENT_TYPE)

        return response

    def copy_table(self, sources, destination, job_id=None, job_id_prefix=None,
                   job_config=None, retry=DEFAULT_RETRY):
        """Start a job for copying one or more tables into another table.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy

        :type sources: One of:
                       :class:`~google.cloud.bigquery.table.TableReference`
                       sequence of
                       :class:`~google.cloud.bigquery.table.TableReference`
        :param sources: Table or tables to be copied.


        :type destination: :class:`google.cloud.bigquery.table.TableReference`
        :param destination: Table into which data is to be copied.

        :type job_id: str
        :param job_id: (Optional) The ID of the job.

        :type job_id_prefix: str or ``NoneType``
        :param job_id_prefix: (Optional) the user-provided prefix for a
                              randomly generated job ID. This parameter will be
                              ignored if a ``job_id`` is also given.

        :type job_config: :class:`google.cloud.bigquery.job.CopyJobConfig`
        :param job_config: (Optional) Extra configuration options for the job.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`google.cloud.bigquery.job.copyjob`
        :returns: a new :class:`google.cloud.bigquery.job.copyjob` instance
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        if not isinstance(sources, collections.Sequence):
            sources = [sources]
        job = CopyJob(job_id, sources, destination, client=self,
                      job_config=job_config)
        job._begin(retry=retry)
        return job

    def extract_table(
            self, source, destination_uris, job_config=None, job_id=None,
            job_id_prefix=None, retry=DEFAULT_RETRY):
        """Start a job to extract a table into Cloud Storage files.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract

        :type source: :class:`google.cloud.bigquery.table.TableReference`
        :param source: table to be extracted.

        :type destination_uris: One of:
                                str or
                                sequence of str
        :param destination_uris:
            URIs of Cloud Storage file(s) into which table data is to be
            extracted; in format ``gs://<bucket_name>/<object_name_or_glob>``.

        :type kwargs: dict
        :param kwargs: Additional keyword arguments.

        :type job_id: str
        :param job_id: (Optional) The ID of the job.

        :type job_id_prefix: str or ``NoneType``
        :param job_id_prefix: (Optional) the user-provided prefix for a
                              randomly generated job ID. This parameter will be
                              ignored if a ``job_id`` is also given.

        :type job_config: :class:`google.cloud.bigquery.job.ExtractJobConfig`
        :param job_config: (Optional) Extra configuration options for the job.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`google.cloud.bigquery.job.ExtractJob`
        :returns: a new :class:`google.cloud.bigquery.job.ExtractJob` instance
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        if isinstance(destination_uris, six.string_types):
            destination_uris = [destination_uris]

        job = ExtractJob(
            job_id, source, destination_uris, client=self,
            job_config=job_config)
        job._begin(retry=retry)
        return job

    def query(self, query, job_config=None, job_id=None, job_id_prefix=None,
              retry=DEFAULT_RETRY):
        """Start a job that runs a SQL query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query

        :type query: str
        :param query:
            SQL query to be executed. Defaults to the standard SQL dialect.
            Use the ``job_config`` parameter to change dialects.

        :type job_config: :class:`google.cloud.bigquery.job.QueryJobConfig`
        :param job_config: (Optional) Extra configuration options for the job.

        :type job_id: str
        :param job_id: (Optional) ID to use for the query job.

        :type job_id_prefix: str or ``NoneType``
        :param job_id_prefix: (Optional) the user-provided prefix for a
                              randomly generated job ID. This parameter will be
                              ignored if a ``job_id`` is also given.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`google.cloud.bigquery.job.QueryJob`
        :returns: a new :class:`google.cloud.bigquery.job.QueryJob` instance
        """
        job_id = _make_job_id(job_id, job_id_prefix)
        job = QueryJob(job_id, query, client=self, job_config=job_config)
        job._begin(retry=retry)
        return job

    def create_rows(self, table, rows, selected_fields=None, **kwargs):
        """API call:  insert table data via a POST request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll

        :type table: One of:
                     :class:`~google.cloud.bigquery.table.Table`
                     :class:`~google.cloud.bigquery.table.TableReference`
        :param table: the destination table for the row data, or a reference
                      to it.

        :type rows: One of:
                    list of tuples
                    list of dictionaries
        :param rows: Row data to be inserted. If a list of tuples is given,
                     each tuple should contain data for each schema field on
                     the current table and in the same order as the schema
                     fields.  If a list of dictionaries is given, the keys must
                     include all required fields in the schema.  Keys which do
                     not correspond to a field in the schema are ignored.

        :type selected_fields:
            list of :class:`~google.cloud.bigquery.schema.SchemaField`
        :param selected_fields:
            The fields to return. Required if ``table`` is a
            :class:`~google.cloud.bigquery.table.TableReference`.

        :type kwargs: dict
        :param kwargs:
            Keyword arguments to
            :meth:`~google.cloud.bigquery.client.Client.create_rows_json`

        :rtype: list of mappings
        :returns: One mapping per row with insert errors:  the "index" key
                  identifies the row, and the "errors" key contains a list
                  of the mappings describing one or more problems with the
                  row.
        :raises: ValueError if table's schema is not set
        """
        if selected_fields is not None:
            schema = selected_fields
        elif isinstance(table, TableReference):
            raise ValueError('need selected_fields with TableReference')
        elif isinstance(table, Table):
            if len(table._schema) == 0:
                raise ValueError(_TABLE_HAS_NO_SCHEMA)
            schema = table.schema
        else:
            raise TypeError('table should be Table or TableReference')

        json_rows = []

        for index, row in enumerate(rows):
            if isinstance(row, dict):
                row = _row_from_mapping(row, schema)
            json_row = {}

            for field, value in zip(schema, row):
                converter = _SCALAR_VALUE_TO_JSON_ROW.get(field.field_type)
                if converter is not None:  # STRING doesn't need converting
                    value = converter(value)
                json_row[field.name] = value

            json_rows.append(json_row)

        return self.create_rows_json(table, json_rows, **kwargs)

    def create_rows_json(self, table, json_rows, row_ids=None,
                         skip_invalid_rows=None, ignore_unknown_values=None,
                         template_suffix=None, retry=DEFAULT_RETRY):
        """API call:  insert table data via a POST request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll

        :type table: One of:
                     :class:`~google.cloud.bigquery.table.Table`
                     :class:`~google.cloud.bigquery.table.TableReference`
        :param table: the destination table for the row data, or a reference
                      to it.

        :type json_rows: list of dictionaries
        :param json_rows: Row data to be inserted. Keys must match the table
                          schema fields and values must be JSON-compatible
                          representations.

        :type row_ids: list of string
        :param row_ids: (Optional)  Unique ids, one per row being inserted.
                        If omitted, unique IDs are created.

        :type skip_invalid_rows: bool
        :param skip_invalid_rows: (Optional)  Insert all valid rows of a
                                  request, even if invalid rows exist.
                                  The default value is False, which causes
                                  the entire request to fail if any invalid
                                  rows exist.

        :type ignore_unknown_values: bool
        :param ignore_unknown_values: (Optional) Accept rows that contain
                                      values that do not match the schema.
                                      The unknown values are ignored. Default
                                      is False, which treats unknown values as
                                      errors.

        :type template_suffix: str
        :param template_suffix:
            (Optional) treat ``name`` as a template table and provide a suffix.
            BigQuery will create the table ``<name> + <template_suffix>`` based
            on the schema of the template table. See
            https://cloud.google.com/bigquery/streaming-data-into-bigquery#template-tables

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: list of mappings
        :returns: One mapping per row with insert errors:  the "index" key
                  identifies the row, and the "errors" key contains a list
                  of the mappings describing one or more problems with the
                  row.
        """
        rows_info = []
        data = {'rows': rows_info}

        for index, row in enumerate(json_rows):
            info = {'json': row}
            if row_ids is not None:
                info['insertId'] = row_ids[index]
            else:
                info['insertId'] = str(uuid.uuid4())
            rows_info.append(info)

        if skip_invalid_rows is not None:
            data['skipInvalidRows'] = skip_invalid_rows

        if ignore_unknown_values is not None:
            data['ignoreUnknownValues'] = ignore_unknown_values

        if template_suffix is not None:
            data['templateSuffix'] = template_suffix

        # We can always retry, because every row has an insert ID.
        response = self._call_api(
            retry,
            method='POST',
            path='%s/insertAll' % table.path,
            data=data)
        errors = []

        for error in response.get('insertErrors', ()):
            errors.append({'index': int(error['index']),
                           'errors': error['errors']})

        return errors

    def query_rows(
            self, query, job_config=None, job_id=None, job_id_prefix=None,
            timeout=None, retry=DEFAULT_RETRY):
        """Start a query job and wait for the results.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query

        :type query: str
        :param query:
            SQL query to be executed. Defaults to the standard SQL dialect.
            Use the ``job_config`` parameter to change dialects.

        :type job_config: :class:`google.cloud.bigquery.job.QueryJobConfig`
        :param job_config: (Optional) Extra configuration options for the job.

        :type job_id: str
        :param job_id: (Optional) ID to use for the query job.

        :type job_id_prefix: str or ``NoneType``
        :param job_id_prefix: (Optional) the user-provided prefix for a
                              randomly generated job ID. This parameter will be
                              ignored if a ``job_id`` is also given.

        :type timeout: float
        :param timeout:
            (Optional) How long (in seconds) to wait for job to complete
            before raising a :class:`concurrent.futures.TimeoutError`.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns:
            Iterator of row data :class:`tuple`s. During each page, the
            iterator will have the ``total_rows`` attribute set, which counts
            the total number of rows **in the result set** (this is distinct
            from the total number of rows in the current page:
            ``iterator.page.num_items``).

        :raises:
            :class:`~google.api_core.exceptions.GoogleAPICallError` if the
            job failed or :class:`concurrent.futures.TimeoutError` if the job
            did not complete in the given timeout.

            When an exception happens, the query job will be cancelled on a
            best-effort basis.
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        try:
            job = self.query(
                query, job_config=job_config, job_id=job_id, retry=retry)
            rows_iterator = job.result(timeout=timeout)
        except (GoogleAPICallError, concurrent.futures.TimeoutError):
            try:
                self.cancel_job(job_id)
            except NotFound:
                # It's OK if couldn't cancel because job never got created.
                pass
            raise

        return rows_iterator

    def list_rows(self, table, selected_fields=None, max_results=None,
                  page_token=None, start_index=None, retry=DEFAULT_RETRY):
        """List the rows of the table.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list

        .. note::

           This method assumes that the provided schema is up-to-date with the
           schema as defined on the back-end: if the two schemas are not
           identical, the values returned may be incomplete. To ensure that the
           local copy of the schema is up-to-date, call ``client.get_table``.

        :type table: One of:
                     :class:`~google.cloud.bigquery.table.Table`
                     :class:`~google.cloud.bigquery.table.TableReference`
        :param table: the table to list, or a reference to it.

        :type selected_fields:
            list of :class:`~google.cloud.bigquery.schema.SchemaField`
        :param selected_fields:
            The fields to return. Required if ``table`` is a
            :class:`~google.cloud.bigquery.table.TableReference`.

        :type max_results: int
        :param max_results: maximum number of rows to return.

        :type page_token: str
        :param page_token: (Optional) Token representing a cursor into the
                           table's rows.

        :type start_index: int
        :param page_token: (Optional) The zero-based index of the starting
                           row to read.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :returns: Iterator of row data :class:`tuple`s. During each page, the
                  iterator will have the ``total_rows`` attribute set,
                  which counts the total number of rows **in the table**
                  (this is distinct from the total number of rows in the
                  current page: ``iterator.page.num_items``).

        """
        if selected_fields is not None:
            schema = selected_fields
        elif isinstance(table, TableReference):
            raise ValueError('need selected_fields with TableReference')
        elif isinstance(table, Table):
            if len(table._schema) == 0:
                raise ValueError(_TABLE_HAS_NO_SCHEMA)
            schema = table.schema
        else:
            raise TypeError('table should be Table or TableReference')

        params = {}
        if selected_fields is not None:
            params['selectedFields'] = ','.join(
                field.name for field in selected_fields)

        if start_index is not None:
            params['startIndex'] = start_index

        iterator = page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path='%s/data' % (table.path,),
            item_to_value=_item_to_row,
            items_key='rows',
            page_token=page_token,
            next_token='pageToken',
            max_results=max_results,
            page_start=_rows_page_start,
            extra_params=params)
        iterator.schema = schema
        iterator._field_to_index = _field_to_index_mapping(schema)
        return iterator

    def list_partitions(self, table, retry=DEFAULT_RETRY):
        """List the partitions in a table.

        :type table: One of:
                     :class:`~google.cloud.bigquery.table.Table`
                     :class:`~google.cloud.bigquery.table.TableReference`
        :param table: the table to list, or a reference to it.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry: (Optional) How to retry the RPC.

        :rtype: list
        :returns: a list of time partitions
        """
        config = QueryJobConfig()
        config.use_legacy_sql = True  # required for '$' syntax
        rows = self.query_rows(
            'SELECT partition_id from [%s:%s.%s$__PARTITIONS_SUMMARY__]' %
            (table.project, table.dataset_id, table.table_id),
            job_config=config,
            retry=retry)
        return [row[0] for row in rows]


# pylint: disable=unused-argument
def _item_to_project(iterator, resource):
    """Convert a JSON project to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
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

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a dataset.

    :rtype: :class:`.Dataset`
    :returns: The next dataset in the page.
    """
    return Dataset.from_api_repr(resource)


def _item_to_job(iterator, resource):
    """Convert a JSON job to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a job.

    :rtype: job instance.
    :returns: The next job in the page.
    """
    return iterator.client.job_from_resource(resource)


def _item_to_table(iterator, resource):
    """Convert a JSON table to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a table.

    :rtype: :class:`~google.cloud.bigquery.table.Table`
    :returns: The next table in the page.
    """
    return Table.from_api_repr(resource)


def _make_job_id(job_id, prefix=None):
    """Construct an ID for a new job.

    :type job_id: str or ``NoneType``
    :param job_id: the user-provided job ID

    :type prefix: str or ``NoneType``
    :param prefix: (Optional) the user-provided prefix for a job ID

    :rtype: str
    :returns: A job ID
    """
    if job_id is not None:
        return job_id
    elif prefix is not None:
        return str(prefix) + str(uuid.uuid4())
    else:
        return str(uuid.uuid4())


def _check_mode(stream):
    """Check that a stream was opened in read-binary mode.

    :type stream: IO[bytes]
    :param stream: A bytes IO object open for reading.

    :raises: :exc:`ValueError` if the ``stream.mode`` is a valid attribute
             and is not among ``rb``, ``r+b`` or ``rb+``.
    """
    mode = getattr(stream, 'mode', None)

    if mode is not None and mode not in ('rb', 'r+b', 'rb+'):
        raise ValueError(
            "Cannot upload files opened in text mode:  use "
            "open(filename, mode='rb') or open(filename, mode='r+b')")


def _get_upload_headers(user_agent):
    """Get the headers for an upload request.

    :type user_agent: str
    :param user_agent: The user-agent for requests.

    :rtype: dict
    :returns: The headers to be used for the request.
    """
    return {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': user_agent,
        'content-type': 'application/json',
    }
