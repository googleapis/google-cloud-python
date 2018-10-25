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
import functools
import gzip
import os
import uuid

import six

from google import resumable_media
from google.resumable_media.requests import MultipartUpload
from google.resumable_media.requests import ResumableUpload

from google.api_core import page_iterator
import google.cloud._helpers
from google.cloud import exceptions
from google.cloud.client import ClientWithProject

from google.cloud.bigquery._helpers import _SCALAR_VALUE_TO_JSON_ROW
from google.cloud.bigquery._helpers import _str_or_none
from google.cloud.bigquery._http import Connection
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.dataset import DatasetListItem
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery import job
from google.cloud.bigquery.query import _QueryResults
from google.cloud.bigquery.retry import DEFAULT_RETRY
from google.cloud.bigquery.table import Table
from google.cloud.bigquery.table import TableListItem
from google.cloud.bigquery.table import TableReference
from google.cloud.bigquery.table import RowIterator
from google.cloud.bigquery.table import _TABLE_HAS_NO_SCHEMA
from google.cloud.bigquery.table import _row_from_mapping


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

    Args:
        project (str):
            Project ID for the project which the client acts on behalf of.
            Will be passed when creating a dataset / job. If not passed,
            falls back to the default inferred from the environment.
        credentials (google.auth.credentials.Credentials):
            (Optional) The OAuth2 Credentials to use for this client. If not
            passed (and if no ``_http`` object is passed), falls back to the
            default inferred from the environment.
        _http (requests.Session):
            (Optional) HTTP object to make requests. Can be any object that
            defines ``request()`` with the same interface as
            :meth:`requests.Session.request`. If not passed, an ``_http``
            object is created that is bound to the ``credentials`` for the
            current object.
            This parameter should be considered private, and could change in
            the future.
        location (str):
            (Optional) Default location for jobs / datasets / tables.
        default_query_job_config (google.cloud.bigquery.job.QueryJobConfig):
            (Optional) Default ``QueryJobConfig``.
            Will be merged into job configs passed into the ``query`` method.

    Raises:
        google.auth.exceptions.DefaultCredentialsError:
            Raised if ``credentials`` is not specified and the library fails
            to acquire default credentials.
    """

    SCOPE = ('https://www.googleapis.com/auth/bigquery',
             'https://www.googleapis.com/auth/cloud-platform')
    """The scopes required for authenticating as a BigQuery consumer."""

    def __init__(
            self, project=None, credentials=None, _http=None,
            location=None, default_query_job_config=None):
        super(Client, self).__init__(
            project=project, credentials=credentials, _http=_http)
        self._connection = Connection(self)
        self._location = location
        self._default_query_job_config = default_query_job_config

    @property
    def location(self):
        """Default location for jobs / datasets / tables."""
        return self._location

    def get_service_account_email(self, project=None):
        """Get the email address of the project's BigQuery service account

        Note:
            This is the service account that BigQuery uses to manage tables
            encrypted by a key in KMS.

        Args:
            project (str, optional):
                Project ID to use for retreiving service account email.
                Defaults to the client's project.

        Returns:
            str: service account email address

        Example:

            >>> from google.cloud import bigquery
            >>> client = bigquery.Client()
            >>> client.get_service_account_email()
            my_service_account@my-project.iam.gserviceaccount.com

        """
        if project is None:
            project = self.project
        path = '/projects/%s/serviceAccount' % (project,)
        api_response = self._connection.api_request(method='GET', path=path)
        return api_response['email']

    def list_projects(self, max_results=None, page_token=None,
                      retry=DEFAULT_RETRY):
        """List projects for the project associated with this client.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/projects/list

        :type max_results: int
        :param max_results: (Optional) maximum number of projects to return,
                            If not passed, defaults to a value set by the API.

        :type page_token: str
        :param page_token:
            (Optional) Token representing a cursor into the projects. If
            not passed, the API will return the first page of projects.
            The token marks the beginning of the iterator to be returned
            and the value of the ``page_token`` can be accessed at
            ``next_page_token`` of the
            :class:`~google.api_core.page_iterator.HTTPIterator`.

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

    def list_datasets(
            self, project=None, include_all=False, filter=None,
            max_results=None, page_token=None, retry=DEFAULT_RETRY):
        """List datasets for the project associated with this client.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list

        Args:
            project (str):
                Optional. Project ID to use for retreiving datasets. Defaults
                to the client's project.
            include_all (bool):
                Optional. True if results include hidden datasets. Defaults
                to False.
            filter (str):
                Optional. An expression for filtering the results by label.
                For syntax, see
                https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list#filter.
            max_results (int):
                Optional. Maximum number of datasets to return.
            page_token (str):
                Optional. Token representing a cursor into the datasets. If
                not passed, the API will return the first page of datasets.
                The token marks the beginning of the iterator to be returned
                and the value of the ``page_token`` can be accessed at
                ``next_page_token`` of the
                :class:`~google.api_core.page_iterator.HTTPIterator`.
            retry (google.api_core.retry.Retry):
                Optional. How to retry the RPC.

        Returns:
            google.api_core.page_iterator.Iterator:
                Iterator of
                :class:`~google.cloud.bigquery.dataset.DatasetListItem`.
                associated with the project.
        """
        extra_params = {}
        if project is None:
            project = self.project
        if include_all:
            extra_params['all'] = True
        if filter:
            # TODO: consider supporting a dict of label -> value for filter,
            # and converting it into a string here.
            extra_params['filter'] = filter
        path = '/projects/%s/datasets' % (project,)
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
        """API call: create the dataset via a POST request.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert

        Args:
            dataset (Union[ \
                :class:`~google.cloud.bigquery.dataset.Dataset`, \
                :class:`~google.cloud.bigquery.dataset.DatasetReference`, \
                str, \
            ]):
                A :class:`~google.cloud.bigquery.dataset.Dataset` to create.
                If ``dataset`` is a reference, an empty dataset is created
                with the specified ID and client's default location.

        Returns:
            google.cloud.bigquery.dataset.Dataset:
                A new ``Dataset`` returned from the API.

        Example:

            >>> from google.cloud import bigquery
            >>> client = bigquery.Client()
            >>> dataset = bigquery.Dataset(client.dataset('my_dataset'))
            >>> dataset = client.create_dataset(dataset)

        """
        if isinstance(dataset, str):
            dataset = DatasetReference.from_string(
                dataset, default_project=self.project)
        if isinstance(dataset, DatasetReference):
            dataset = Dataset(dataset)

        path = '/projects/%s/datasets' % (dataset.project,)

        data = dataset.to_api_repr()
        if data.get('location') is None and self.location is not None:
            data['location'] = self.location

        api_response = self._connection.api_request(
            method='POST', path=path, data=data)

        return Dataset.from_api_repr(api_response)

    def create_table(self, table):
        """API call:  create a table via a PUT request

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert

        Args:
            table (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                A :class:`~google.cloud.bigquery.table.Table` to create.
                If ``table`` is a reference, an empty table is created
                with the specified ID. The dataset that the table belongs to
                must already exist.

        Returns:
            google.cloud.bigquery.table.Table:
                A new ``Table`` returned from the service.
        """
        if isinstance(table, str):
            table = TableReference.from_string(
                table, default_project=self.project)
        if isinstance(table, TableReference):
            table = Table(table)

        path = '/projects/%s/datasets/%s/tables' % (
            table.project, table.dataset_id)
        api_response = self._connection.api_request(
            method='POST', path=path, data=table.to_api_repr())
        return Table.from_api_repr(api_response)

    def _call_api(self, retry, **kwargs):
        call = functools.partial(self._connection.api_request, **kwargs)
        if retry:
            call = retry(call)
        return call()

    def get_dataset(self, dataset_ref, retry=DEFAULT_RETRY):
        """Fetch the dataset referenced by ``dataset_ref``

        Args:
            dataset_ref (Union[ \
                :class:`~google.cloud.bigquery.dataset.DatasetReference`, \
                str, \
            ]):
                A reference to the dataset to fetch from the BigQuery API.
                If a string is passed in, this method attempts to create a
                dataset reference from a string using
                :func:`~google.cloud.bigquery.dataset.DatasetReference.from_string`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.

        Returns:
            google.cloud.bigquery.dataset.Dataset:
                A ``Dataset`` instance.
        """
        if isinstance(dataset_ref, str):
            dataset_ref = DatasetReference.from_string(
                dataset_ref, default_project=self.project)

        api_response = self._call_api(
            retry, method='GET', path=dataset_ref.path)
        return Dataset.from_api_repr(api_response)

    def get_table(self, table_ref, retry=DEFAULT_RETRY):
        """Fetch the table referenced by ``table_ref``.

        Args:
            table_ref (Union[ \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                A reference to the table to fetch from the BigQuery API.
                If a string is passed in, this method attempts to create a
                table reference from a string using
                :func:`google.cloud.bigquery.table.TableReference.from_string`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.

        Returns:
            google.cloud.bigquery.table.Table:
                A ``Table`` instance.
        """
        if isinstance(table_ref, str):
            table_ref = TableReference.from_string(
                table_ref, default_project=self.project)

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
        and then passing it to ``update_dataset`` will ensure that the changes
        will only be saved if no modifications to the dataset occurred
        since the read.

        Args:
            dataset (google.cloud.bigquery.dataset.Dataset):
                The dataset to update.
            fields (Sequence[str]):
                The properties of ``dataset`` to change (e.g. "friendly_name").
            retry (google.api_core.retry.Retry, optional):
                How to retry the RPC.

        Returns:
            google.cloud.bigquery.dataset.Dataset:
                The modified ``Dataset`` instance.
        """
        partial = dataset._build_resource(fields)
        if dataset.etag is not None:
            headers = {'If-Match': dataset.etag}
        else:
            headers = None
        api_response = self._call_api(
            retry,
            method='PATCH',
            path=dataset.path,
            data=partial,
            headers=headers)
        return Dataset.from_api_repr(api_response)

    def update_table(self, table, fields, retry=DEFAULT_RETRY):
        """Change some fields of a table.

        Use ``fields`` to specify which fields to update. At least one field
        must be provided. If a field is listed in ``fields`` and is ``None``
        in ``table``, it will be deleted.

        If ``table.etag`` is not ``None``, the update will only succeed if
        the table on the server has the same ETag. Thus reading a table with
        ``get_table``, changing its fields, and then passing it to
        ``update_table`` will ensure that the changes will only be saved if
        no modifications to the table occurred since the read.

        Args:
            table (google.cloud.bigquery.table.Table): The table to update.
            fields (Sequence[str]):
                The fields of ``table`` to change, spelled as the Table
                properties (e.g. "friendly_name").
            retry (google.api_core.retry.Retry):
                (Optional) A description of how to retry the API call.

        Returns:
            google.cloud.bigquery.table.Table:
                The table resource returned from the API call.
        """
        partial = table._build_resource(fields)
        if table.etag is not None:
            headers = {'If-Match': table.etag}
        else:
            headers = None
        api_response = self._call_api(
            retry,
            method='PATCH', path=table.path, data=partial, headers=headers)
        return Table.from_api_repr(api_response)

    def list_tables(self, dataset, max_results=None, page_token=None,
                    retry=DEFAULT_RETRY):
        """List tables in the dataset.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/list

        Args:
            dataset (Union[ \
                :class:`~google.cloud.bigquery.dataset.Dataset`, \
                :class:`~google.cloud.bigquery.dataset.DatasetReference`, \
                str, \
            ]):
                A reference to the dataset whose tables to list from the
                BigQuery API. If a string is passed in, this method attempts
                to create a dataset reference from a string using
                :func:`google.cloud.bigquery.dataset.DatasetReference.from_string`.
            max_results (int):
                (Optional) Maximum number of tables to return. If not passed,
                defaults to a value set by the API.
            page_token (str):
                (Optional) Token representing a cursor into the tables. If
                not passed, the API will return the first page of tables. The
                token marks the beginning of the iterator to be returned and
                the value of the ``page_token`` can be accessed at
                ``next_page_token`` of the
                :class:`~google.api_core.page_iterator.HTTPIterator`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.

        Returns:
            google.api_core.page_iterator.Iterator:
                Iterator of
                :class:`~google.cloud.bigquery.table.TableListItem` contained
                within the requested dataset.
        """
        if isinstance(dataset, str):
            dataset = DatasetReference.from_string(
                dataset, default_project=self.project)

        if not isinstance(dataset, (Dataset, DatasetReference)):
            raise TypeError(
                'dataset must be a Dataset, DatasetReference, or string')

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

    def delete_dataset(self, dataset, delete_contents=False,
                       retry=DEFAULT_RETRY):
        """Delete a dataset.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/delete

        Args
            dataset (Union[ \
                :class:`~google.cloud.bigquery.dataset.Dataset`, \
                :class:`~google.cloud.bigquery.dataset.DatasetReference`, \
                str, \
            ]):
                A reference to the dataset to delete. If a string is passed
                in, this method attempts to create a dataset reference from a
                string using
                :func:`google.cloud.bigquery.dataset.DatasetReference.from_string`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.
            delete_contents (boolean):
                (Optional) If True, delete all the tables in the dataset. If
                False and the dataset contains tables, the request will fail.
                Default is False.
        """
        if isinstance(dataset, str):
            dataset = DatasetReference.from_string(
                dataset, default_project=self.project)

        if not isinstance(dataset, (Dataset, DatasetReference)):
            raise TypeError('dataset must be a Dataset or a DatasetReference')

        params = {}
        if delete_contents:
            params['deleteContents'] = 'true'

        self._call_api(retry,
                       method='DELETE',
                       path=dataset.path,
                       query_params=params)

    def delete_table(self, table, retry=DEFAULT_RETRY):
        """Delete a table

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables/delete

        Args:
            table (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                A reference to the table to delete. If a string is passed in,
                this method attempts to create a table reference from a
                string using
                :func:`google.cloud.bigquery.table.TableReference.from_string`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.
        """
        if isinstance(table, str):
            table = TableReference.from_string(
                table, default_project=self.project)

        if not isinstance(table, (Table, TableReference)):
            raise TypeError('table must be a Table or a TableReference')
        self._call_api(retry, method='DELETE', path=table.path)

    def _get_query_results(
            self, job_id, retry, project=None, timeout_ms=None, location=None):
        """Get the query results object for a query job.

        Arguments:
            job_id (str): Name of the query job.
            retry (google.api_core.retry.Retry):
                (Optional) How to retry the RPC.
            project (str):
                (Optional) project ID for the query job (defaults to the
                project of the client).
            timeout_ms (int):
                (Optional) number of milliseconds the the API call should
                wait for the query to complete before the request times out.
            location (str): Location of the query job.

        Returns:
            google.cloud.bigquery.query._QueryResults:
                A new ``_QueryResults`` instance.
        """

        extra_params = {'maxResults': 0}

        if project is None:
            project = self.project

        if timeout_ms is not None:
            extra_params['timeoutMs'] = timeout_ms

        if location is None:
            location = self.location

        if location is not None:
            extra_params['location'] = location

        path = '/projects/{}/queries/{}'.format(project, job_id)

        # This call is typically made in a polling loop that checks whether the
        # job is complete (from QueryJob.done(), called ultimately from
        # QueryJob.result()). So we don't need to poll here.
        resource = self._call_api(
            retry, method='GET', path=path, query_params=extra_params)
        return _QueryResults.from_api_repr(resource)

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
        config = resource.get('configuration', {})
        if 'load' in config:
            return job.LoadJob.from_api_repr(resource, self)
        elif 'copy' in config:
            return job.CopyJob.from_api_repr(resource, self)
        elif 'extract' in config:
            return job.ExtractJob.from_api_repr(resource, self)
        elif 'query' in config:
            return job.QueryJob.from_api_repr(resource, self)
        return job.UnknownJob.from_api_repr(resource, self)

    def get_job(
            self, job_id, project=None, location=None, retry=DEFAULT_RETRY):
        """Fetch a job for the project associated with this client.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get

        Arguments:
            job_id (str): Unique job identifier.

        Keyword Arguments:
            project (str):
                (Optional) ID of the project which ownsthe job (defaults to
                the client's project).
            location (str): Location where the job was run.
            retry (google.api_core.retry.Retry):
                (Optional) How to retry the RPC.

        Returns:
            Union[google.cloud.bigquery.job.LoadJob, \
                  google.cloud.bigquery.job.CopyJob, \
                  google.cloud.bigquery.job.ExtractJob, \
                  google.cloud.bigquery.job.QueryJob]:
                Job instance, based on the resource returned by the API.
        """
        extra_params = {'projection': 'full'}

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        if location is not None:
            extra_params['location'] = location

        path = '/projects/{}/jobs/{}'.format(project, job_id)

        resource = self._call_api(
            retry, method='GET', path=path, query_params=extra_params)

        return self.job_from_resource(resource)

    def cancel_job(
            self, job_id, project=None, location=None, retry=DEFAULT_RETRY):
        """Attempt to cancel a job from a job ID.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/cancel

        Arguments:
            job_id (str): Unique job identifier.

        Keyword Arguments:
            project (str):
                (Optional) ID of the project which owns the job (defaults to
                the client's project).
            location (str): Location where the job was run.
            retry (google.api_core.retry.Retry):
                (Optional) How to retry the RPC.

        Returns:
            Union[google.cloud.bigquery.job.LoadJob, \
                  google.cloud.bigquery.job.CopyJob, \
                  google.cloud.bigquery.job.ExtractJob, \
                  google.cloud.bigquery.job.QueryJob]:
                Job instance, based on the resource returned by the API.
        """
        extra_params = {'projection': 'full'}

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        if location is not None:
            extra_params['location'] = location

        path = '/projects/{}/jobs/{}/cancel'.format(project, job_id)

        resource = self._call_api(
            retry, method='POST', path=path, query_params=extra_params)

        return self.job_from_resource(resource['job'])

    def list_jobs(
            self, project=None, max_results=None, page_token=None,
            all_users=None, state_filter=None, retry=DEFAULT_RETRY,
            min_creation_time=None, max_creation_time=None):
        """List jobs for the project associated with this client.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/list

        Args:
            project (str, optional):
                Project ID to use for retreiving datasets. Defaults
                to the client's project.
            max_results (int, optional):
                Maximum number of jobs to return.
            page_token (str, optional):
                Opaque marker for the next "page" of jobs. If not
                passed, the API will return the first page of jobs. The token
                marks the beginning of the iterator to be returned and the
                value of the ``page_token`` can be accessed at
                ``next_page_token`` of
                :class:`~google.api_core.page_iterator.HTTPIterator`.
            all_users (bool, optional):
                If true, include jobs owned by all users in the project.
                Defaults to :data:`False`.
            state_filter (str, optional):
                If set, include only jobs matching the given state. One of:
                    * ``"done"``
                    * ``"pending"``
                    * ``"running"``
            retry (google.api_core.retry.Retry, optional):
                How to retry the RPC.
            min_creation_time (datetime.datetime, optional):
                Min value for job creation time. If set, only jobs created
                after or at this timestamp are returned. If the datetime has
                no time zone assumes UTC time.
            max_creation_time (datetime.datetime, optional):
                Max value for job creation time. If set, only jobs created
                before or at this timestamp are returned. If the datetime has
                no time zone assumes UTC time.

        Returns:
            google.api_core.page_iterator.Iterator:
                Iterable of job instances.
        """
        extra_params = {
            'allUsers': all_users,
            'stateFilter': state_filter,
            'minCreationTime': _str_or_none(
                google.cloud._helpers._millis_from_datetime(
                    min_creation_time)),
            'maxCreationTime': _str_or_none(
                google.cloud._helpers._millis_from_datetime(
                    max_creation_time)),
            'projection': 'full'
        }

        extra_params = {param: value for param, value in extra_params.items()
                        if value is not None}

        if project is None:
            project = self.project

        path = '/projects/%s/jobs' % (project,)
        return page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path=path,
            item_to_value=_item_to_job,
            items_key='jobs',
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params)

    def load_table_from_uri(
            self, source_uris, destination,
            job_id=None,
            job_id_prefix=None,
            location=None,
            project=None,
            job_config=None,
            retry=DEFAULT_RETRY):
        """Starts a job for loading data into a table from CloudStorage.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load

        Arguments:
            source_uris (Union[str, Sequence[str]]):
                URIs of data files to be loaded; in format
                ``gs://<bucket_name>/<object_name_or_glob>``.
            destination (Union[ \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                Table into which data is to be loaded. If a string is passed
                in, this method attempts to create a table reference from a
                string using
                :func:`google.cloud.bigquery.table.TableReference.from_string`.

        Keyword Arguments:
            job_id (str): (Optional) Name of the job.
            job_id_prefix (str):
                (Optional) the user-provided prefix for a randomly generated
                job ID. This parameter will be ignored if a ``job_id`` is
                also given.
            location (str):
                Location where to run the job. Must match the location of the
                destination table.
            project (str):
                Project ID of the project of where to run the job. Defaults
                to the client's project.
            job_config (google.cloud.bigquery.job.LoadJobConfig):
                (Optional) Extra configuration options for the job.
            retry (google.api_core.retry.Retry):
                (Optional) How to retry the RPC.

        Returns:
            google.cloud.bigquery.job.LoadJob: A new load job.
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        job_ref = job._JobReference(job_id, project=project, location=location)

        if isinstance(source_uris, six.string_types):
            source_uris = [source_uris]

        if isinstance(destination, str):
            destination = TableReference.from_string(
                destination, default_project=self.project)

        load_job = job.LoadJob(
            job_ref, source_uris, destination, self, job_config)
        load_job._begin(retry=retry)

        return load_job

    def load_table_from_file(
            self, file_obj, destination, rewind=False, size=None,
            num_retries=_DEFAULT_NUM_RETRIES, job_id=None,
            job_id_prefix=None, location=None, project=None,
            job_config=None):
        """Upload the contents of this table from a file-like object.

        Similar to :meth:`load_table_from_uri`, this method creates, starts and
        returns a :class:`~google.cloud.bigquery.job.LoadJob`.

        Arguments:
            file_obj (file): A file handle opened in binary mode for reading.
            destination (Union[ \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                Table into which data is to be loaded. If a string is passed
                in, this method attempts to create a table reference from a
                string using
                :func:`google.cloud.bigquery.table.TableReference.from_string`.

        Keyword Arguments:
            rewind (bool):
                If True, seek to the beginning of the file handle before
                reading the file.
            size (int):
                The number of bytes to read from the file handle. If size is
                ``None`` or large, resumable upload will be used. Otherwise,
                multipart upload will be used.
            num_retries (int): Number of upload retries. Defaults to 6.
            job_id (str): (Optional) Name of the job.
            job_id_prefix (str):
                (Optional) the user-provided prefix for a randomly generated
                job ID. This parameter will be ignored if a ``job_id`` is
                also given.
            location (str):
                Location where to run the job. Must match the location of the
                destination table.
            project (str):
                Project ID of the project of where to run the job. Defaults
                to the client's project.
            job_config (google.cloud.bigquery.job.LoadJobConfig):
                (Optional) Extra configuration options for the job.

        Returns:
            google.cloud.bigquery.job.LoadJob: A new load job.

        Raises:
            ValueError:
                If ``size`` is not passed in and can not be determined, or if
                the ``file_obj`` can be detected to be a file opened in text
                mode.
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        if isinstance(destination, str):
            destination = TableReference.from_string(
                destination, default_project=self.project)

        job_ref = job._JobReference(job_id, project=project, location=location)
        load_job = job.LoadJob(job_ref, None, destination, self, job_config)
        job_resource = load_job.to_api_repr()

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

    def load_table_from_dataframe(self, dataframe, destination,
                                  num_retries=_DEFAULT_NUM_RETRIES,
                                  job_id=None, job_id_prefix=None,
                                  location=None, project=None,
                                  job_config=None):
        """Upload the contents of a table from a pandas DataFrame.

        Similar to :meth:`load_table_from_uri`, this method creates, starts and
        returns a :class:`~google.cloud.bigquery.job.LoadJob`.

        Arguments:
            dataframe (pandas.DataFrame):
                A :class:`~pandas.DataFrame` containing the data to load.
            destination (google.cloud.bigquery.table.TableReference):
                The destination table to use for loading the data. If it is an
                existing table, the schema of the :class:`~pandas.DataFrame`
                must match the schema of the destination table. If the table
                does not yet exist, the schema is inferred from the
                :class:`~pandas.DataFrame`.

                If a string is passed in, this method attempts to create a
                table reference from a string using
                :func:`google.cloud.bigquery.table.TableReference.from_string`.

        Keyword Arguments:
            num_retries (int, optional): Number of upload retries.
            job_id (str, optional): Name of the job.
            job_id_prefix (str, optional):
                The user-provided prefix for a randomly generated
                job ID. This parameter will be ignored if a ``job_id`` is
                also given.
            location (str):
                Location where to run the job. Must match the location of the
                destination table.
            project (str, optional):
                Project ID of the project of where to run the job. Defaults
                to the client's project.
            job_config (google.cloud.bigquery.job.LoadJobConfig, optional):
                Extra configuration options for the job.

        Returns:
            google.cloud.bigquery.job.LoadJob: A new load job.

        Raises:
            ImportError:
                If a usable parquet engine cannot be found. This method
                requires :mod:`pyarrow` to be installed.
        """
        buffer = six.BytesIO()
        dataframe.to_parquet(buffer)

        if job_config is None:
            job_config = job.LoadJobConfig()
        job_config.source_format = job.SourceFormat.PARQUET

        if location is None:
            location = self.location

        return self.load_table_from_file(
            buffer, destination,
            num_retries=num_retries,
            rewind=True,
            job_id=job_id,
            job_id_prefix=job_id_prefix,
            location=location,
            project=project,
            job_config=job_config,
        )

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

    def copy_table(
            self, sources, destination, job_id=None, job_id_prefix=None,
            location=None, project=None, job_config=None,
            retry=DEFAULT_RETRY):
        """Copy one or more tables to another table.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy

        Arguments:
            sources (Union[ \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
                Sequence[ \
                    :class:`~google.cloud.bigquery.table.TableReference`], \
            ]):
                Table or tables to be copied.
            destination (Union[
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                Table into which data is to be copied.

        Keyword Arguments:
            job_id (str): (Optional) The ID of the job.
            job_id_prefix (str)
                (Optional) the user-provided prefix for a randomly generated
                job ID. This parameter will be ignored if a ``job_id`` is
                also given.
            location (str):
                Location where to run the job. Must match the location of any
                source table as well as the destination table.
            project (str):
                Project ID of the project of where to run the job. Defaults
                to the client's project.
            job_config (google.cloud.bigquery.job.CopyJobConfig):
                (Optional) Extra configuration options for the job.
            retry (google.api_core.retry.Retry):
                (Optional) How to retry the RPC.

        Returns:
            google.cloud.bigquery.job.CopyJob: A new copy job instance.
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        job_ref = job._JobReference(job_id, project=project, location=location)

        if isinstance(sources, str):
            sources = TableReference.from_string(
                sources, default_project=self.project)

        if isinstance(destination, str):
            destination = TableReference.from_string(
                destination, default_project=self.project)

        if not isinstance(sources, collections.Sequence):
            sources = [sources]

        copy_job = job.CopyJob(
            job_ref, sources, destination, client=self,
            job_config=job_config)
        copy_job._begin(retry=retry)

        return copy_job

    def extract_table(
            self, source, destination_uris, job_id=None, job_id_prefix=None,
            location=None, project=None, job_config=None,
            retry=DEFAULT_RETRY):
        """Start a job to extract a table into Cloud Storage files.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract

        Arguments:
            source (Union[ \
                :class:`google.cloud.bigquery.table.TableReference`, \
                src, \
            ]):
                Table to be extracted.
            destination_uris (Union[str, Sequence[str]]):
                URIs of Cloud Storage file(s) into which table data is to be
                extracted; in format
                ``gs://<bucket_name>/<object_name_or_glob>``.

        Keyword Arguments:
            job_id (str): (Optional) The ID of the job.
            job_id_prefix (str)
                (Optional) the user-provided prefix for a randomly generated
                job ID. This parameter will be ignored if a ``job_id`` is
                also given.
            location (str):
                Location where to run the job. Must match the location of the
                source table.
            project (str):
                Project ID of the project of where to run the job. Defaults
                to the client's project.
            job_config (google.cloud.bigquery.job.ExtractJobConfig):
                (Optional) Extra configuration options for the job.
            retry (google.api_core.retry.Retry):
                (Optional) How to retry the RPC.
        :type source: :class:`google.cloud.bigquery.table.TableReference`
        :param source: table to be extracted.


        Returns:
            google.cloud.bigquery.job.ExtractJob: A new extract job instance.
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        job_ref = job._JobReference(job_id, project=project, location=location)

        if isinstance(source, str):
            source = TableReference.from_string(
                source, default_project=self.project)

        if isinstance(destination_uris, six.string_types):
            destination_uris = [destination_uris]

        extract_job = job.ExtractJob(
            job_ref, source, destination_uris, client=self,
            job_config=job_config)
        extract_job._begin(retry=retry)

        return extract_job

    def query(
            self, query,
            job_config=None,
            job_id=None, job_id_prefix=None,
            location=None, project=None, retry=DEFAULT_RETRY):
        """Run a SQL query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query

        Arguments:
            query (str):
                SQL query to be executed. Defaults to the standard SQL
                dialect. Use the ``job_config`` parameter to change dialects.

        Keyword Arguments:
            job_config (google.cloud.bigquery.job.QueryJobConfig):
                (Optional) Extra configuration options for the job.
                To override any options that were previously set in
                the ``default_query_job_config`` given to the
                ``Client`` constructor, manually set those options to ``None``,
                or whatever value is preferred.
            job_id (str): (Optional) ID to use for the query job.
            job_id_prefix (str):
                (Optional) The prefix to use for a randomly generated job ID.
                This parameter will be ignored if a ``job_id`` is also given.
            location (str):
                Location where to run the job. Must match the location of the
                any table used in the query as well as the destination table.
            project (str):
                Project ID of the project of where to run the job. Defaults
                to the client's project.
            retry (google.api_core.retry.Retry):
                (Optional) How to retry the RPC.

        Returns:
            google.cloud.bigquery.job.QueryJob: A new query job instance.
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        if self._default_query_job_config:
            if job_config:
                # anything that's not defined on the incoming
                # that is in the default,
                # should be filled in with the default
                # the incoming therefore has precedence
                job_config = job_config._fill_from_default(
                    self._default_query_job_config)
            else:
                job_config = self._default_query_job_config

        job_ref = job._JobReference(job_id, project=project, location=location)
        query_job = job.QueryJob(
            job_ref, query, client=self, job_config=job_config)
        query_job._begin(retry=retry)

        return query_job

    def insert_rows(self, table, rows, selected_fields=None, **kwargs):
        """Insert rows into a table via the streaming API.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll

        Args:
            table (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                The destination table for the row data, or a reference to it.
            rows (Union[ \
                Sequence[Tuple], \
                Sequence[dict], \
            ]):
                Row data to be inserted. If a list of tuples is given, each
                tuple should contain data for each schema field on the
                current table and in the same order as the schema fields. If
                a list of dictionaries is given, the keys must include all
                required fields in the schema. Keys which do not correspond
                to a field in the schema are ignored.
            selected_fields (Sequence[ \
                :class:`~google.cloud.bigquery.schema.SchemaField`, \
            ]):
                The fields to return. Required if ``table`` is a
                :class:`~google.cloud.bigquery.table.TableReference`.
            kwargs (dict):
                Keyword arguments to
                :meth:`~google.cloud.bigquery.client.Client.insert_rows_json`.

        Returns:
            Sequence[Mappings]:
                One mapping per row with insert errors: the "index" key
                identifies the row, and the "errors" key contains a list of
                the mappings describing one or more problems with the row.

        Raises:
            ValueError: if table's schema is not set
        """
        if isinstance(table, str):
            table = TableReference.from_string(
                table, default_project=self.project)

        if selected_fields is not None:
            schema = selected_fields
        elif isinstance(table, TableReference):
            raise ValueError('need selected_fields with TableReference')
        elif isinstance(table, Table):
            if len(table.schema) == 0:
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

        return self.insert_rows_json(table, json_rows, **kwargs)

    def insert_rows_json(self, table, json_rows, row_ids=None,
                         skip_invalid_rows=None, ignore_unknown_values=None,
                         template_suffix=None, retry=DEFAULT_RETRY):
        """Insert rows into a table without applying local type conversions.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll

        table (Union[ \
            :class:`~google.cloud.bigquery.table.Table` \
            :class:`~google.cloud.bigquery.table.TableReference`, \
            str, \
        ]):
            The destination table for the row data, or a reference to it.
        json_rows (Sequence[dict]):
            Row data to be inserted. Keys must match the table schema fields
            and values must be JSON-compatible representations.
        row_ids (Sequence[str]):
            (Optional) Unique ids, one per row being inserted. If omitted,
            unique IDs are created.
        skip_invalid_rows (bool):
            (Optional) Insert all valid rows of a request, even if invalid
            rows exist. The default value is False, which causes the entire
            request to fail if any invalid rows exist.
        ignore_unknown_values (bool):
            (Optional) Accept rows that contain values that do not match the
            schema. The unknown values are ignored. Default is False, which
            treats unknown values as errors.
        template_suffix (str):
            (Optional) treat ``name`` as a template table and provide a suffix.
            BigQuery will create the table ``<name> + <template_suffix>`` based
            on the schema of the template table. See
            https://cloud.google.com/bigquery/streaming-data-into-bigquery#template-tables
        retry (:class:`google.api_core.retry.Retry`):
            (Optional) How to retry the RPC.

        Returns:
            Sequence[Mappings]:
                One mapping per row with insert errors: the "index" key
                identifies the row, and the "errors" key contains a list of
                the mappings describing one or more problems with the row.
        """
        if isinstance(table, str):
            table = TableReference.from_string(
                table, default_project=self.project)

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

    def list_partitions(self, table, retry=DEFAULT_RETRY):
        """List the partitions in a table.

        Arguments:
            table (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                The table or reference from which to get partition info
            retry (google.api_core.retry.Retry):
                (Optional) How to retry the RPC.

        Returns:
            List[str]:
                A list of the partition ids present in the partitioned table
        """
        if isinstance(table, str):
            table = TableReference.from_string(
                table, default_project=self.project)

        meta_table = self.get_table(
            TableReference(
                self.dataset(table.dataset_id, project=table.project),
                '%s$__PARTITIONS_SUMMARY__' % table.table_id))

        subset = [col for col in
                  meta_table.schema if col.name == 'partition_id']
        return [row[0] for row in self.list_rows(meta_table,
                selected_fields=subset,
                retry=retry)]

    def list_rows(self, table, selected_fields=None, max_results=None,
                  page_token=None, start_index=None, page_size=None,
                  retry=DEFAULT_RETRY):
        """List the rows of the table.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list

        .. note::

           This method assumes that the provided schema is up-to-date with the
           schema as defined on the back-end: if the two schemas are not
           identical, the values returned may be incomplete. To ensure that the
           local copy of the schema is up-to-date, call ``client.get_table``.

        Args:
            table (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                The table to list, or a reference to it.
            selected_fields (Sequence[ \
                :class:`~google.cloud.bigquery.schema.SchemaField` \
            ]):
                The fields to return. Required if ``table`` is a
                :class:`~google.cloud.bigquery.table.TableReference`.
            max_results (int):
                (Optional) maximum number of rows to return.
            page_token (str):
                (Optional) Token representing a cursor into the table's rows.
                If not passed, the API will return the first page of the
                rows. The token marks the beginning of the iterator to be
                returned and the value of the ``page_token`` can be accessed
                at ``next_page_token`` of the
                :class:`~google.cloud.bigquery.table.RowIterator`.
            start_index (int):
                (Optional) The zero-based index of the starting row to read.
            page_size (int):
                (Optional) The maximum number of items to return per page in
                the iterator.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.

        Returns:
            google.cloud.bigquery.table.RowIterator:
                Iterator of row data
                :class:`~google.cloud.bigquery.table.Row`-s. During each
                page, the iterator will have the ``total_rows`` attribute
                set, which counts the total number of rows **in the table**
                (this is distinct from the total number of rows in the
                current page: ``iterator.page.num_items``).
        """
        if isinstance(table, str):
            table = TableReference.from_string(
                table, default_project=self.project)

        if selected_fields is not None:
            schema = selected_fields
        elif isinstance(table, TableReference):
            raise ValueError('need selected_fields with TableReference')
        elif isinstance(table, Table):
            if len(table.schema) == 0 and table.created is None:
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

        row_iterator = RowIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path='%s/data' % (table.path,),
            schema=schema,
            page_token=page_token,
            max_results=max_results,
            page_size=page_size,
            extra_params=params)
        return row_iterator


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

    :rtype: :class:`.DatasetListItem`
    :returns: The next dataset in the page.
    """
    return DatasetListItem(resource)


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
    return TableListItem(resource)


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

    if isinstance(stream, gzip.GzipFile):
        if mode != gzip.READ:
            raise ValueError(
                "Cannot upload gzip files opened in write mode:  use "
                "gzip.GzipFile(filename, mode='rb')")
    else:
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
