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

try:
    from collections import abc as collections_abc
except ImportError:  # Python 2.7
    import collections as collections_abc

import copy
import functools
import gzip
import io
import json
import os
import tempfile
import uuid
import warnings

try:
    import pyarrow
except ImportError:  # pragma: NO COVER
    pyarrow = None
import six

from google import resumable_media
from google.resumable_media.requests import MultipartUpload
from google.resumable_media.requests import ResumableUpload

import google.api_core.client_options
import google.api_core.exceptions
from google.api_core import page_iterator
import google.cloud._helpers
from google.cloud import exceptions
from google.cloud.client import ClientWithProject

from google.cloud.bigquery._helpers import _record_field_to_json
from google.cloud.bigquery._helpers import _str_or_none
from google.cloud.bigquery._http import Connection
from google.cloud.bigquery import _pandas_helpers
from google.cloud.bigquery.dataset import Dataset
from google.cloud.bigquery.dataset import DatasetListItem
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.bigquery import job
from google.cloud.bigquery.model import Model
from google.cloud.bigquery.model import ModelReference
from google.cloud.bigquery.query import _QueryResults
from google.cloud.bigquery.retry import DEFAULT_RETRY
from google.cloud.bigquery.routine import Routine
from google.cloud.bigquery.routine import RoutineReference
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.table import _table_arg_to_table
from google.cloud.bigquery.table import _table_arg_to_table_ref
from google.cloud.bigquery.table import Table
from google.cloud.bigquery.table import TableListItem
from google.cloud.bigquery.table import TableReference
from google.cloud.bigquery.table import RowIterator


_DEFAULT_CHUNKSIZE = 1048576  # 1024 * 1024 B = 1 MB
_MAX_MULTIPART_SIZE = 5 * 1024 * 1024
_DEFAULT_NUM_RETRIES = 6
_BASE_UPLOAD_TEMPLATE = (
    u"https://www.googleapis.com/upload/bigquery/v2/projects/"
    u"{project}/jobs?uploadType="
)
_MULTIPART_URL_TEMPLATE = _BASE_UPLOAD_TEMPLATE + u"multipart"
_RESUMABLE_URL_TEMPLATE = _BASE_UPLOAD_TEMPLATE + u"resumable"
_GENERIC_CONTENT_TYPE = u"*/*"
_READ_LESS_THAN_SIZE = (
    "Size {:d} was specified but the file-like object only had " "{:d} bytes remaining."
)
_NEED_TABLE_ARGUMENT = (
    "The table argument should be a table ID string, Table, or TableReference"
)


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
        return cls(resource["id"], resource["numericId"], resource["friendlyName"])


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
        client_info (google.api_core.client_info.ClientInfo):
            The client info used to send a user-agent string along with API
            requests. If ``None``, then default info will be used. Generally,
            you only need to set this if you're developing your own library
            or partner tool.
        client_options (Union[~google.api_core.client_options.ClientOptions, dict]):
            (Optional) Client options used to set user options on the client.
            API Endpoint should be set through client_options.

    Raises:
        google.auth.exceptions.DefaultCredentialsError:
            Raised if ``credentials`` is not specified and the library fails
            to acquire default credentials.
    """

    SCOPE = (
        "https://www.googleapis.com/auth/bigquery",
        "https://www.googleapis.com/auth/cloud-platform",
    )
    """The scopes required for authenticating as a BigQuery consumer."""

    def __init__(
        self,
        project=None,
        credentials=None,
        _http=None,
        location=None,
        default_query_job_config=None,
        client_info=None,
        client_options=None,
    ):
        super(Client, self).__init__(
            project=project, credentials=credentials, _http=_http
        )

        kw_args = {"client_info": client_info}
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint
                kw_args["api_endpoint"] = api_endpoint

        self._connection = Connection(self, **kw_args)
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
        path = "/projects/%s/serviceAccount" % (project,)
        api_response = self._connection.api_request(method="GET", path=path)
        return api_response["email"]

    def list_projects(self, max_results=None, page_token=None, retry=DEFAULT_RETRY):
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
            path="/projects",
            item_to_value=_item_to_project,
            items_key="projects",
            page_token=page_token,
            max_results=max_results,
        )

    def list_datasets(
        self,
        project=None,
        include_all=False,
        filter=None,
        max_results=None,
        page_token=None,
        retry=DEFAULT_RETRY,
    ):
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
            extra_params["all"] = True
        if filter:
            # TODO: consider supporting a dict of label -> value for filter,
            # and converting it into a string here.
            extra_params["filter"] = filter
        path = "/projects/%s/datasets" % (project,)
        return page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path=path,
            item_to_value=_item_to_dataset,
            items_key="datasets",
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params,
        )

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

    def create_dataset(self, dataset, exists_ok=False, retry=DEFAULT_RETRY):
        """API call: create the dataset via a POST request.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert

        Args:
            dataset (Union[ \
                :class:`~google.cloud.bigquery.dataset.Dataset`, \
                :class:`~google.cloud.bigquery.dataset.DatasetReference`, \
                str, \
            ]):
                A :class:`~google.cloud.bigquery.dataset.Dataset` to create.
                If ``dataset`` is a reference, an empty dataset is created
                with the specified ID and client's default location.
            exists_ok (bool):
                Defaults to ``False``. If ``True``, ignore "already exists"
                errors when creating the dataset.
            retry (google.api_core.retry.Retry):
                Optional. How to retry the RPC.

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
                dataset, default_project=self.project
            )
        if isinstance(dataset, DatasetReference):
            dataset = Dataset(dataset)

        path = "/projects/%s/datasets" % (dataset.project,)

        data = dataset.to_api_repr()
        if data.get("location") is None and self.location is not None:
            data["location"] = self.location

        try:
            api_response = self._call_api(retry, method="POST", path=path, data=data)
            return Dataset.from_api_repr(api_response)
        except google.api_core.exceptions.Conflict:
            if not exists_ok:
                raise
            return self.get_dataset(dataset.reference, retry=retry)

    def create_routine(self, routine, exists_ok=False, retry=DEFAULT_RETRY):
        """[Beta] Create a routine via a POST request.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/routines/insert

        Args:
            routine (:class:`~google.cloud.bigquery.routine.Routine`):
                A :class:`~google.cloud.bigquery.routine.Routine` to create.
                The dataset that the routine belongs to must already exist.
            exists_ok (bool):
                Defaults to ``False``. If ``True``, ignore "already exists"
                errors when creating the routine.
            retry (google.api_core.retry.Retry):
                Optional. How to retry the RPC.

        Returns:
            google.cloud.bigquery.routine.Routine:
                A new ``Routine`` returned from the service.
        """
        reference = routine.reference
        path = "/projects/{}/datasets/{}/routines".format(
            reference.project, reference.dataset_id
        )
        resource = routine.to_api_repr()
        try:
            api_response = self._call_api(
                retry, method="POST", path=path, data=resource
            )
            return Routine.from_api_repr(api_response)
        except google.api_core.exceptions.Conflict:
            if not exists_ok:
                raise
            return self.get_routine(routine.reference, retry=retry)

    def create_table(self, table, exists_ok=False, retry=DEFAULT_RETRY):
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
            exists_ok (bool):
                Defaults to ``False``. If ``True``, ignore "already exists"
                errors when creating the table.
            retry (google.api_core.retry.Retry):
                Optional. How to retry the RPC.

        Returns:
            google.cloud.bigquery.table.Table:
                A new ``Table`` returned from the service.
        """
        table = _table_arg_to_table(table, default_project=self.project)

        path = "/projects/%s/datasets/%s/tables" % (table.project, table.dataset_id)
        data = table.to_api_repr()
        try:
            api_response = self._call_api(retry, method="POST", path=path, data=data)
            return Table.from_api_repr(api_response)
        except google.api_core.exceptions.Conflict:
            if not exists_ok:
                raise
            return self.get_table(table.reference, retry=retry)

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
                dataset_ref, default_project=self.project
            )

        api_response = self._call_api(retry, method="GET", path=dataset_ref.path)
        return Dataset.from_api_repr(api_response)

    def get_model(self, model_ref, retry=DEFAULT_RETRY):
        """[Beta] Fetch the model referenced by ``model_ref``.

         Args:
            model_ref (Union[ \
                :class:`~google.cloud.bigquery.model.ModelReference`, \
                str, \
            ]):
                A reference to the model to fetch from the BigQuery API.
                If a string is passed in, this method attempts to create a
                model reference from a string using
                :func:`google.cloud.bigquery.model.ModelReference.from_string`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.

         Returns:
            google.cloud.bigquery.model.Model:
                A ``Model`` instance.
        """
        if isinstance(model_ref, str):
            model_ref = ModelReference.from_string(
                model_ref, default_project=self.project
            )

        api_response = self._call_api(retry, method="GET", path=model_ref.path)
        return Model.from_api_repr(api_response)

    def get_routine(self, routine_ref, retry=DEFAULT_RETRY):
        """[Beta] Get the routine referenced by ``routine_ref``.

         Args:
            routine_ref (Union[ \
                :class:`~google.cloud.bigquery.routine.Routine`, \
                :class:`~google.cloud.bigquery.routine.RoutineReference`, \
                str, \
            ]):
                A reference to the routine to fetch from the BigQuery API. If
                a string is passed in, this method attempts to create a
                reference from a string using
                :func:`google.cloud.bigquery.routine.RoutineReference.from_string`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the API call.

         Returns:
            google.cloud.bigquery.routine.Routine:
                A ``Routine`` instance.
        """
        if isinstance(routine_ref, str):
            routine_ref = RoutineReference.from_string(
                routine_ref, default_project=self.project
            )

        api_response = self._call_api(retry, method="GET", path=routine_ref.path)
        return Routine.from_api_repr(api_response)

    def get_table(self, table, retry=DEFAULT_RETRY):
        """Fetch the table referenced by ``table``.

        Args:
            table (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
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
        table_ref = _table_arg_to_table_ref(table, default_project=self.project)
        api_response = self._call_api(retry, method="GET", path=table_ref.path)
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
            headers = {"If-Match": dataset.etag}
        else:
            headers = None
        api_response = self._call_api(
            retry, method="PATCH", path=dataset.path, data=partial, headers=headers
        )
        return Dataset.from_api_repr(api_response)

    def update_model(self, model, fields, retry=DEFAULT_RETRY):
        """[Beta] Change some fields of a model.

        Use ``fields`` to specify which fields to update. At least one field
        must be provided. If a field is listed in ``fields`` and is ``None``
        in ``model``, the field value will be deleted.

        If ``model.etag`` is not ``None``, the update will only succeed if
        the model on the server has the same ETag. Thus reading a model with
        ``get_model``, changing its fields, and then passing it to
        ``update_model`` will ensure that the changes will only be saved if
        no modifications to the model occurred since the read.

        Args:
            model (google.cloud.bigquery.model.Model): The model to update.
            fields (Sequence[str]):
                The fields of ``model`` to change, spelled as the Model
                properties (e.g. "friendly_name").
            retry (google.api_core.retry.Retry):
                (Optional) A description of how to retry the API call.

        Returns:
            google.cloud.bigquery.model.Model:
                The model resource returned from the API call.
        """
        partial = model._build_resource(fields)
        if model.etag:
            headers = {"If-Match": model.etag}
        else:
            headers = None
        api_response = self._call_api(
            retry, method="PATCH", path=model.path, data=partial, headers=headers
        )
        return Model.from_api_repr(api_response)

    def update_routine(self, routine, fields, retry=DEFAULT_RETRY):
        """[Beta] Change some fields of a routine.

        Use ``fields`` to specify which fields to update. At least one field
        must be provided. If a field is listed in ``fields`` and is ``None``
        in ``routine``, the field value will be deleted.

        .. warning::
           During beta, partial updates are not supported. You must provide
           all fields in the resource.

        If :attr:`~google.cloud.bigquery.routine.Routine.etag` is not
        ``None``, the update will only succeed if the resource on the server
        has the same ETag. Thus reading a routine with
        :func:`~google.cloud.bigquery.client.Client.get_routine`, changing
        its fields, and then passing it to this method will ensure that the
        changes will only be saved if no modifications to the resource
        occurred since the read.

        Args:
            routine (google.cloud.bigquery.routine.Routine): The routine to update.
            fields (Sequence[str]):
                The fields of ``routine`` to change, spelled as the
                :class:`~google.cloud.bigquery.routine.Routine` properties
                (e.g. ``type_``).
            retry (google.api_core.retry.Retry):
                (Optional) A description of how to retry the API call.

        Returns:
            google.cloud.bigquery.routine.Routine:
                The routine resource returned from the API call.
        """
        partial = routine._build_resource(fields)
        if routine.etag:
            headers = {"If-Match": routine.etag}
        else:
            headers = None

        # TODO: remove when routines update supports partial requests.
        partial["routineReference"] = routine.reference.to_api_repr()

        api_response = self._call_api(
            retry, method="PUT", path=routine.path, data=partial, headers=headers
        )
        return Routine.from_api_repr(api_response)

    def update_table(self, table, fields, retry=DEFAULT_RETRY):
        """Change some fields of a table.

        Use ``fields`` to specify which fields to update. At least one field
        must be provided. If a field is listed in ``fields`` and is ``None``
        in ``table``, the field value will be deleted.

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
            headers = {"If-Match": table.etag}
        else:
            headers = None
        api_response = self._call_api(
            retry, method="PATCH", path=table.path, data=partial, headers=headers
        )
        return Table.from_api_repr(api_response)

    def list_models(
        self, dataset, max_results=None, page_token=None, retry=DEFAULT_RETRY
    ):
        """[Beta] List models in the dataset.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/models/list

        Args:
            dataset (Union[ \
                :class:`~google.cloud.bigquery.dataset.Dataset`, \
                :class:`~google.cloud.bigquery.dataset.DatasetReference`, \
                str, \
            ]):
                A reference to the dataset whose models to list from the
                BigQuery API. If a string is passed in, this method attempts
                to create a dataset reference from a string using
                :func:`google.cloud.bigquery.dataset.DatasetReference.from_string`.
            max_results (int):
                (Optional) Maximum number of models to return. If not passed,
                defaults to a value set by the API.
            page_token (str):
                (Optional) Token representing a cursor into the models. If
                not passed, the API will return the first page of models. The
                token marks the beginning of the iterator to be returned and
                the value of the ``page_token`` can be accessed at
                ``next_page_token`` of the
                :class:`~google.api_core.page_iterator.HTTPIterator`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.

         Returns:
            google.api_core.page_iterator.Iterator:
                Iterator of
                :class:`~google.cloud.bigquery.model.Model` contained
                within the requested dataset.
        """
        if isinstance(dataset, str):
            dataset = DatasetReference.from_string(
                dataset, default_project=self.project
            )

        if not isinstance(dataset, (Dataset, DatasetReference)):
            raise TypeError("dataset must be a Dataset, DatasetReference, or string")

        path = "%s/models" % dataset.path
        result = page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path=path,
            item_to_value=_item_to_model,
            items_key="models",
            page_token=page_token,
            max_results=max_results,
        )
        result.dataset = dataset
        return result

    def list_routines(
        self, dataset, max_results=None, page_token=None, retry=DEFAULT_RETRY
    ):
        """[Beta] List routines in the dataset.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/routines/list

        Args:
            dataset (Union[ \
                :class:`~google.cloud.bigquery.dataset.Dataset`, \
                :class:`~google.cloud.bigquery.dataset.DatasetReference`, \
                str, \
            ]):
                A reference to the dataset whose routines to list from the
                BigQuery API. If a string is passed in, this method attempts
                to create a dataset reference from a string using
                :func:`google.cloud.bigquery.dataset.DatasetReference.from_string`.
            max_results (int):
                (Optional) Maximum number of routines to return. If not passed,
                defaults to a value set by the API.
            page_token (str):
                (Optional) Token representing a cursor into the routines. If
                not passed, the API will return the first page of routines. The
                token marks the beginning of the iterator to be returned and
                the value of the ``page_token`` can be accessed at
                ``next_page_token`` of the
                :class:`~google.api_core.page_iterator.HTTPIterator`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.

         Returns:
            google.api_core.page_iterator.Iterator:
                Iterator of all
                :class:`~google.cloud.bigquery.routine.Routine`s contained
                within the requested dataset, limited by ``max_results``.
        """
        if isinstance(dataset, str):
            dataset = DatasetReference.from_string(
                dataset, default_project=self.project
            )

        if not isinstance(dataset, (Dataset, DatasetReference)):
            raise TypeError("dataset must be a Dataset, DatasetReference, or string")

        path = "{}/routines".format(dataset.path)
        result = page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path=path,
            item_to_value=_item_to_routine,
            items_key="routines",
            page_token=page_token,
            max_results=max_results,
        )
        result.dataset = dataset
        return result

    def list_tables(
        self, dataset, max_results=None, page_token=None, retry=DEFAULT_RETRY
    ):
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
                dataset, default_project=self.project
            )

        if not isinstance(dataset, (Dataset, DatasetReference)):
            raise TypeError("dataset must be a Dataset, DatasetReference, or string")

        path = "%s/tables" % dataset.path
        result = page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path=path,
            item_to_value=_item_to_table,
            items_key="tables",
            page_token=page_token,
            max_results=max_results,
        )
        result.dataset = dataset
        return result

    def delete_dataset(
        self, dataset, delete_contents=False, retry=DEFAULT_RETRY, not_found_ok=False
    ):
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
            delete_contents (boolean):
                (Optional) If True, delete all the tables in the dataset. If
                False and the dataset contains tables, the request will fail.
                Default is False.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.
            not_found_ok (bool):
                Defaults to ``False``. If ``True``, ignore "not found" errors
                when deleting the dataset.
        """
        if isinstance(dataset, str):
            dataset = DatasetReference.from_string(
                dataset, default_project=self.project
            )

        if not isinstance(dataset, (Dataset, DatasetReference)):
            raise TypeError("dataset must be a Dataset or a DatasetReference")

        params = {}
        if delete_contents:
            params["deleteContents"] = "true"

        try:
            self._call_api(
                retry, method="DELETE", path=dataset.path, query_params=params
            )
        except google.api_core.exceptions.NotFound:
            if not not_found_ok:
                raise

    def delete_model(self, model, retry=DEFAULT_RETRY, not_found_ok=False):
        """[Beta] Delete a model

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/models/delete

        Args:
            model (Union[ \
                :class:`~google.cloud.bigquery.model.Model`, \
                :class:`~google.cloud.bigquery.model.ModelReference`, \
                str, \
            ]):
                A reference to the model to delete. If a string is passed in,
                this method attempts to create a model reference from a
                string using
                :func:`google.cloud.bigquery.model.ModelReference.from_string`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.
            not_found_ok (bool):
                Defaults to ``False``. If ``True``, ignore "not found" errors
                when deleting the model.
        """
        if isinstance(model, str):
            model = ModelReference.from_string(model, default_project=self.project)

        if not isinstance(model, (Model, ModelReference)):
            raise TypeError("model must be a Model or a ModelReference")

        try:
            self._call_api(retry, method="DELETE", path=model.path)
        except google.api_core.exceptions.NotFound:
            if not not_found_ok:
                raise

    def delete_routine(self, routine, retry=DEFAULT_RETRY, not_found_ok=False):
        """[Beta] Delete a routine.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/routines/delete

        Args:
            model (Union[ \
                :class:`~google.cloud.bigquery.routine.Routine`, \
                :class:`~google.cloud.bigquery.routine.RoutineReference`, \
                str, \
            ]):
                A reference to the routine to delete. If a string is passed
                in, this method attempts to create a routine reference from a
                string using
                :func:`google.cloud.bigquery.routine.RoutineReference.from_string`.
            retry (:class:`google.api_core.retry.Retry`):
                (Optional) How to retry the RPC.
            not_found_ok (bool):
                Defaults to ``False``. If ``True``, ignore "not found" errors
                when deleting the routine.
        """
        if isinstance(routine, str):
            routine = RoutineReference.from_string(
                routine, default_project=self.project
            )

        if not isinstance(routine, (Routine, RoutineReference)):
            raise TypeError("routine must be a Routine or a RoutineReference")

        try:
            self._call_api(retry, method="DELETE", path=routine.path)
        except google.api_core.exceptions.NotFound:
            if not not_found_ok:
                raise

    def delete_table(self, table, retry=DEFAULT_RETRY, not_found_ok=False):
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
            not_found_ok (bool):
                Defaults to ``False``. If ``True``, ignore "not found" errors
                when deleting the table.
        """
        table = _table_arg_to_table_ref(table, default_project=self.project)
        if not isinstance(table, TableReference):
            raise TypeError("Unable to get TableReference for table '{}'".format(table))

        try:
            self._call_api(retry, method="DELETE", path=table.path)
        except google.api_core.exceptions.NotFound:
            if not not_found_ok:
                raise

    def _get_query_results(
        self, job_id, retry, project=None, timeout_ms=None, location=None
    ):
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

        extra_params = {"maxResults": 0}

        if project is None:
            project = self.project

        if timeout_ms is not None:
            extra_params["timeoutMs"] = timeout_ms

        if location is None:
            location = self.location

        if location is not None:
            extra_params["location"] = location

        path = "/projects/{}/queries/{}".format(project, job_id)

        # This call is typically made in a polling loop that checks whether the
        # job is complete (from QueryJob.done(), called ultimately from
        # QueryJob.result()). So we don't need to poll here.
        resource = self._call_api(
            retry, method="GET", path=path, query_params=extra_params
        )
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
        config = resource.get("configuration", {})
        if "load" in config:
            return job.LoadJob.from_api_repr(resource, self)
        elif "copy" in config:
            return job.CopyJob.from_api_repr(resource, self)
        elif "extract" in config:
            return job.ExtractJob.from_api_repr(resource, self)
        elif "query" in config:
            return job.QueryJob.from_api_repr(resource, self)
        return job.UnknownJob.from_api_repr(resource, self)

    def get_job(self, job_id, project=None, location=None, retry=DEFAULT_RETRY):
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
        extra_params = {"projection": "full"}

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        if location is not None:
            extra_params["location"] = location

        path = "/projects/{}/jobs/{}".format(project, job_id)

        resource = self._call_api(
            retry, method="GET", path=path, query_params=extra_params
        )

        return self.job_from_resource(resource)

    def cancel_job(self, job_id, project=None, location=None, retry=DEFAULT_RETRY):
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
        extra_params = {"projection": "full"}

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        if location is not None:
            extra_params["location"] = location

        path = "/projects/{}/jobs/{}/cancel".format(project, job_id)

        resource = self._call_api(
            retry, method="POST", path=path, query_params=extra_params
        )

        return self.job_from_resource(resource["job"])

    def list_jobs(
        self,
        project=None,
        max_results=None,
        page_token=None,
        all_users=None,
        state_filter=None,
        retry=DEFAULT_RETRY,
        min_creation_time=None,
        max_creation_time=None,
    ):
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
            "allUsers": all_users,
            "stateFilter": state_filter,
            "minCreationTime": _str_or_none(
                google.cloud._helpers._millis_from_datetime(min_creation_time)
            ),
            "maxCreationTime": _str_or_none(
                google.cloud._helpers._millis_from_datetime(max_creation_time)
            ),
            "projection": "full",
        }

        extra_params = {
            param: value for param, value in extra_params.items() if value is not None
        }

        if project is None:
            project = self.project

        path = "/projects/%s/jobs" % (project,)
        return page_iterator.HTTPIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path=path,
            item_to_value=_item_to_job,
            items_key="jobs",
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params,
        )

    def load_table_from_uri(
        self,
        source_uris,
        destination,
        job_id=None,
        job_id_prefix=None,
        location=None,
        project=None,
        job_config=None,
        retry=DEFAULT_RETRY,
    ):
        """Starts a job for loading data into a table from CloudStorage.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load

        Arguments:
            source_uris (Union[str, Sequence[str]]):
                URIs of data files to be loaded; in format
                ``gs://<bucket_name>/<object_name_or_glob>``.
            destination (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
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

        destination = _table_arg_to_table_ref(destination, default_project=self.project)
        load_job = job.LoadJob(job_ref, source_uris, destination, self, job_config)
        load_job._begin(retry=retry)

        return load_job

    def load_table_from_file(
        self,
        file_obj,
        destination,
        rewind=False,
        size=None,
        num_retries=_DEFAULT_NUM_RETRIES,
        job_id=None,
        job_id_prefix=None,
        location=None,
        project=None,
        job_config=None,
    ):
        """Upload the contents of this table from a file-like object.

        Similar to :meth:`load_table_from_uri`, this method creates, starts and
        returns a :class:`~google.cloud.bigquery.job.LoadJob`.

        Arguments:
            file_obj (file): A file handle opened in binary mode for reading.
            destination (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
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

        destination = _table_arg_to_table_ref(destination, default_project=self.project)
        job_ref = job._JobReference(job_id, project=project, location=location)
        load_job = job.LoadJob(job_ref, None, destination, self, job_config)
        job_resource = load_job.to_api_repr()

        if rewind:
            file_obj.seek(0, os.SEEK_SET)

        _check_mode(file_obj)

        try:
            if size is None or size >= _MAX_MULTIPART_SIZE:
                response = self._do_resumable_upload(
                    file_obj, job_resource, num_retries
                )
            else:
                response = self._do_multipart_upload(
                    file_obj, job_resource, size, num_retries
                )
        except resumable_media.InvalidResponse as exc:
            raise exceptions.from_http_response(exc.response)

        return self.job_from_resource(response.json())

    def load_table_from_dataframe(
        self,
        dataframe,
        destination,
        num_retries=_DEFAULT_NUM_RETRIES,
        job_id=None,
        job_id_prefix=None,
        location=None,
        project=None,
        job_config=None,
        parquet_compression="snappy",
    ):
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
            job_config (~google.cloud.bigquery.job.LoadJobConfig, optional):
                Extra configuration options for the job.

                To override the default pandas data type conversions, supply
                a value for
                :attr:`~google.cloud.bigquery.job.LoadJobConfig.schema` with
                column names matching those of the dataframe. The BigQuery
                schema is used to determine the correct data type conversion.
                Indexes are not loaded. Requires the :mod:`pyarrow` library.
            parquet_compression (str):
                 [Beta] The compression method to use if intermittently
                 serializing ``dataframe`` to a parquet file.

                 If ``pyarrow`` and job config schema are used, the argument
                 is directly passed as the ``compression`` argument to the
                 underlying ``pyarrow.parquet.write_table()`` method (the
                 default value "snappy" gets converted to uppercase).
                 https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html#pyarrow-parquet-write-table

                 If either ``pyarrow`` or job config schema are missing, the
                 argument is directly passed as the ``compression`` argument
                 to the underlying ``DataFrame.to_parquet()`` method.
                 https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_parquet.html#pandas.DataFrame.to_parquet

        Returns:
            google.cloud.bigquery.job.LoadJob: A new load job.

        Raises:
            ImportError:
                If a usable parquet engine cannot be found. This method
                requires :mod:`pyarrow` or :mod:`fastparquet` to be
                installed.
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        if job_config is None:
            job_config = job.LoadJobConfig()
        else:
            # Make a copy so that the job config isn't modified in-place.
            job_config_properties = copy.deepcopy(job_config._properties)
            job_config = job.LoadJobConfig()
            job_config._properties = job_config_properties
        job_config.source_format = job.SourceFormat.PARQUET

        if location is None:
            location = self.location

        job_config.schema = _pandas_helpers.dataframe_to_bq_schema(
            dataframe, job_config.schema
        )

        tmpfd, tmppath = tempfile.mkstemp(suffix="_job_{}.parquet".format(job_id[:8]))
        os.close(tmpfd)

        try:
            if pyarrow and job_config.schema:
                if parquet_compression == "snappy":  # adjust the default value
                    parquet_compression = parquet_compression.upper()

                _pandas_helpers.dataframe_to_parquet(
                    dataframe,
                    job_config.schema,
                    tmppath,
                    parquet_compression=parquet_compression,
                )
            else:
                if job_config.schema:
                    warnings.warn(
                        "job_config.schema is set, but not used to assist in "
                        "identifying correct types for data serialization. "
                        "Please install the pyarrow package.",
                        PendingDeprecationWarning,
                        stacklevel=2,
                    )

                dataframe.to_parquet(tmppath, compression=parquet_compression)

            with open(tmppath, "rb") as parquet_file:
                return self.load_table_from_file(
                    parquet_file,
                    destination,
                    num_retries=num_retries,
                    rewind=True,
                    job_id=job_id,
                    job_id_prefix=job_id_prefix,
                    location=location,
                    project=project,
                    job_config=job_config,
                )

        finally:
            os.remove(tmppath)

    def load_table_from_json(
        self,
        json_rows,
        destination,
        num_retries=_DEFAULT_NUM_RETRIES,
        job_id=None,
        job_id_prefix=None,
        location=None,
        project=None,
        job_config=None,
    ):
        """Upload the contents of a table from a JSON string or dict.

        Arguments:
            json_rows (Iterable[Dict[str, Any]]):
                Row data to be inserted. Keys must match the table schema fields
                and values must be JSON-compatible representations.
            destination (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                Table into which data is to be loaded. If a string is passed
                in, this method attempts to create a table reference from a
                string using
                :func:`google.cloud.bigquery.table.TableReference.from_string`.

        Keyword Arguments:
            num_retries (int, optional): Number of upload retries.
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
                (Optional) Extra configuration options for the job. The
                ``source_format`` setting is always set to
                :attr:`~google.cloud.bigquery.job.SourceFormat.NEWLINE_DELIMITED_JSON`.

        Returns:
            google.cloud.bigquery.job.LoadJob: A new load job.
        """
        job_id = _make_job_id(job_id, job_id_prefix)

        if job_config is None:
            job_config = job.LoadJobConfig()
        else:
            # Make a copy so that the job config isn't modified in-place.
            job_config = copy.deepcopy(job_config)
        job_config.source_format = job.SourceFormat.NEWLINE_DELIMITED_JSON

        if job_config.schema is None:
            job_config.autodetect = True

        if project is None:
            project = self.project

        if location is None:
            location = self.location

        destination = _table_arg_to_table_ref(destination, default_project=self.project)

        data_str = u"\n".join(json.dumps(item) for item in json_rows)
        data_file = io.BytesIO(data_str.encode())

        return self.load_table_from_file(
            data_file,
            destination,
            num_retries=num_retries,
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
            stream, metadata, num_retries
        )

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
        headers = _get_upload_headers(self._connection.user_agent)
        upload_url = _RESUMABLE_URL_TEMPLATE.format(project=self.project)
        # TODO: modify ResumableUpload to take a retry.Retry object
        # that it can use for the initial RPC.
        upload = ResumableUpload(upload_url, chunk_size, headers=headers)

        if num_retries is not None:
            upload._retry_strategy = resumable_media.RetryStrategy(
                max_retries=num_retries
            )

        upload.initiate(
            transport, stream, metadata, _GENERIC_CONTENT_TYPE, stream_final=False
        )

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

        headers = _get_upload_headers(self._connection.user_agent)

        upload_url = _MULTIPART_URL_TEMPLATE.format(project=self.project)
        upload = MultipartUpload(upload_url, headers=headers)

        if num_retries is not None:
            upload._retry_strategy = resumable_media.RetryStrategy(
                max_retries=num_retries
            )

        response = upload.transmit(self._http, data, metadata, _GENERIC_CONTENT_TYPE)

        return response

    def copy_table(
        self,
        sources,
        destination,
        job_id=None,
        job_id_prefix=None,
        location=None,
        project=None,
        job_config=None,
        retry=DEFAULT_RETRY,
    ):
        """Copy one or more tables to another table.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.copy

        Arguments:
            sources (Union[ \
                :class:`~google.cloud.bigquery.table.Table`, \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
                Sequence[ \
                    Union[ \
                        :class:`~google.cloud.bigquery.table.Table`, \
                        :class:`~google.cloud.bigquery.table.TableReference`, \
                        str, \
                    ] \
                ], \
            ]):
                Table or tables to be copied.
            destination (Union[
                :class:`~google.cloud.bigquery.table.Table`, \
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

        # sources can be one of many different input types. (string, Table,
        # TableReference, or a sequence of any of those.) Convert them all to a
        # list of TableReferences.
        #
        # _table_arg_to_table_ref leaves lists unmodified.
        sources = _table_arg_to_table_ref(sources, default_project=self.project)

        if not isinstance(sources, collections_abc.Sequence):
            sources = [sources]

        sources = [
            _table_arg_to_table_ref(source, default_project=self.project)
            for source in sources
        ]

        destination = _table_arg_to_table_ref(destination, default_project=self.project)

        copy_job = job.CopyJob(
            job_ref, sources, destination, client=self, job_config=job_config
        )
        copy_job._begin(retry=retry)

        return copy_job

    def extract_table(
        self,
        source,
        destination_uris,
        job_id=None,
        job_id_prefix=None,
        location=None,
        project=None,
        job_config=None,
        retry=DEFAULT_RETRY,
    ):
        """Start a job to extract a table into Cloud Storage files.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.extract

        Arguments:
            source (Union[ \
                :class:`google.cloud.bigquery.table.Table`, \
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
        source = _table_arg_to_table_ref(source, default_project=self.project)

        if isinstance(destination_uris, six.string_types):
            destination_uris = [destination_uris]

        extract_job = job.ExtractJob(
            job_ref, source, destination_uris, client=self, job_config=job_config
        )
        extract_job._begin(retry=retry)

        return extract_job

    def query(
        self,
        query,
        job_config=None,
        job_id=None,
        job_id_prefix=None,
        location=None,
        project=None,
        retry=DEFAULT_RETRY,
    ):
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
                    self._default_query_job_config
                )
            else:
                job_config = self._default_query_job_config

        job_ref = job._JobReference(job_id, project=project, location=location)
        query_job = job.QueryJob(job_ref, query, client=self, job_config=job_config)
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
        table = _table_arg_to_table(table, default_project=self.project)

        if not isinstance(table, Table):
            raise TypeError(_NEED_TABLE_ARGUMENT)

        schema = table.schema

        # selected_fields can override the table schema.
        if selected_fields is not None:
            schema = selected_fields

        if len(schema) == 0:
            raise ValueError(
                (
                    "Could not determine schema for table '{}'. Call client.get_table() "
                    "or pass in a list of schema fields to the selected_fields argument."
                ).format(table)
            )

        json_rows = [_record_field_to_json(schema, row) for row in rows]

        return self.insert_rows_json(table, json_rows, **kwargs)

    def insert_rows_json(
        self,
        table,
        json_rows,
        row_ids=None,
        skip_invalid_rows=None,
        ignore_unknown_values=None,
        template_suffix=None,
        retry=DEFAULT_RETRY,
    ):
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
        # Convert table to just a reference because unlike insert_rows,
        # insert_rows_json doesn't need the table schema. It's not doing any
        # type conversions.
        table = _table_arg_to_table_ref(table, default_project=self.project)
        rows_info = []
        data = {"rows": rows_info}

        for index, row in enumerate(json_rows):
            info = {"json": row}
            if row_ids is not None:
                info["insertId"] = row_ids[index]
            else:
                info["insertId"] = str(uuid.uuid4())
            rows_info.append(info)

        if skip_invalid_rows is not None:
            data["skipInvalidRows"] = skip_invalid_rows

        if ignore_unknown_values is not None:
            data["ignoreUnknownValues"] = ignore_unknown_values

        if template_suffix is not None:
            data["templateSuffix"] = template_suffix

        # We can always retry, because every row has an insert ID.
        response = self._call_api(
            retry, method="POST", path="%s/insertAll" % table.path, data=data
        )
        errors = []

        for error in response.get("insertErrors", ()):
            errors.append({"index": int(error["index"]), "errors": error["errors"]})

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
        table = _table_arg_to_table_ref(table, default_project=self.project)
        meta_table = self.get_table(
            TableReference(
                self.dataset(table.dataset_id, project=table.project),
                "%s$__PARTITIONS_SUMMARY__" % table.table_id,
            )
        )

        subset = [col for col in meta_table.schema if col.name == "partition_id"]
        return [
            row[0]
            for row in self.list_rows(meta_table, selected_fields=subset, retry=retry)
        ]

    def list_rows(
        self,
        table,
        selected_fields=None,
        max_results=None,
        page_token=None,
        start_index=None,
        page_size=None,
        retry=DEFAULT_RETRY,
    ):
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
                :class:`~google.cloud.bigquery.table.TableListItem`, \
                :class:`~google.cloud.bigquery.table.TableReference`, \
                str, \
            ]):
                The table to list, or a reference to it. When the table
                object does not contain a schema and ``selected_fields`` is
                not supplied, this method calls ``get_table`` to fetch the
                table schema.
            selected_fields (Sequence[ \
                :class:`~google.cloud.bigquery.schema.SchemaField` \
            ]):
                The fields to return. If not supplied, data for all columns
                are downloaded.
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
                Optional. The maximum number of rows in each page of results
                from this request. Non-positive values are ignored. Defaults
                to a sensible value set by the API.
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
        table = _table_arg_to_table(table, default_project=self.project)

        if not isinstance(table, Table):
            raise TypeError(_NEED_TABLE_ARGUMENT)

        schema = table.schema

        # selected_fields can override the table schema.
        if selected_fields is not None:
            schema = selected_fields

        # No schema, but no selected_fields. Assume the developer wants all
        # columns, so get the table resource for them rather than failing.
        elif len(schema) == 0:
            table = self.get_table(table.reference, retry=retry)
            schema = table.schema

        params = {}
        if selected_fields is not None:
            params["selectedFields"] = ",".join(field.name for field in selected_fields)
        if start_index is not None:
            params["startIndex"] = start_index

        row_iterator = RowIterator(
            client=self,
            api_request=functools.partial(self._call_api, retry),
            path="%s/data" % (table.path,),
            schema=schema,
            page_token=page_token,
            max_results=max_results,
            page_size=page_size,
            extra_params=params,
            table=table,
            # Pass in selected_fields separately from schema so that full
            # tables can be fetched without a column filter.
            selected_fields=selected_fields,
        )
        return row_iterator

    def _schema_from_json_file_object(self, file_obj):
        """Helper function for schema_from_json that takes a
       file object that describes a table schema.

       Returns:
            List of schema field objects.
        """
        json_data = json.load(file_obj)
        return [SchemaField.from_api_repr(field) for field in json_data]

    def _schema_to_json_file_object(self, schema_list, file_obj):
        """Helper function for schema_to_json that takes a schema list and file
        object and writes the schema list to the file object with json.dump
        """
        json.dump(schema_list, file_obj, indent=2, sort_keys=True)

    def schema_from_json(self, file_or_path):
        """Takes a file object or file path that contains json that describes
        a table schema.

        Returns:
            List of schema field objects.
        """
        if isinstance(file_or_path, io.IOBase):
            return self._schema_from_json_file_object(file_or_path)

        with open(file_or_path) as file_obj:
            return self._schema_from_json_file_object(file_obj)

    def schema_to_json(self, schema_list, destination):
        """Takes a list of schema field objects.

        Serializes the list of schema field objects as json to a file.

        Destination is a file path or a file object.
        """
        json_schema_list = [f.to_api_repr() for f in schema_list]

        if isinstance(destination, io.IOBase):
            return self._schema_to_json_file_object(json_schema_list, destination)

        with open(destination, mode="w") as file_obj:
            return self._schema_to_json_file_object(json_schema_list, file_obj)


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


def _item_to_model(iterator, resource):
    """Convert a JSON model to the native object.

    Args:
        iterator (google.api_core.page_iterator.Iterator):
            The iterator that is currently in use.
        resource (dict):
            An item to be converted to a model.

    Returns:
        google.cloud.bigquery.model.Model: The next model in the page.
    """
    return Model.from_api_repr(resource)


def _item_to_routine(iterator, resource):
    """Convert a JSON model to the native object.

    Args:
        iterator (google.api_core.page_iterator.Iterator):
            The iterator that is currently in use.
        resource (dict):
            An item to be converted to a routine.

    Returns:
        google.cloud.bigquery.routine.Routine: The next routine in the page.
    """
    return Routine.from_api_repr(resource)


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
    mode = getattr(stream, "mode", None)

    if isinstance(stream, gzip.GzipFile):
        if mode != gzip.READ:
            raise ValueError(
                "Cannot upload gzip files opened in write mode:  use "
                "gzip.GzipFile(filename, mode='rb')"
            )
    else:
        if mode is not None and mode not in ("rb", "r+b", "rb+"):
            raise ValueError(
                "Cannot upload files opened in text mode:  use "
                "open(filename, mode='rb') or open(filename, mode='r+b')"
            )


def _get_upload_headers(user_agent):
    """Get the headers for an upload request.

    :type user_agent: str
    :param user_agent: The user-agent for requests.

    :rtype: dict
    :returns: The headers to be used for the request.
    """
    return {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": user_agent,
        "content-type": "application/json",
    }
