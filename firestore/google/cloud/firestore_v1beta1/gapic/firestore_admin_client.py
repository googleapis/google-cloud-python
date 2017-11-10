# Copyright 2017, Google LLC All rights reserved.
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
#
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/firestore/admin/v1beta1/firestore_admin.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.firestore.admin.v1beta1 FirestoreAdmin API."""

import collections
import json
import os
import pkg_resources
import platform

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.cloud.firestore_v1beta1.gapic import enums
from google.cloud.firestore_v1beta1.gapic import firestore_admin_client_config
from google.cloud.firestore_v1beta1.proto.admin import firestore_admin_pb2
from google.cloud.firestore_v1beta1.proto.admin import index_pb2

_PageDesc = google.gax.PageDescriptor


class FirestoreAdminClient(object):
    """
    The Cloud Firestore Admin API.

    This API provides several administrative services for Cloud Firestore.

    # Concepts

    Project, Database, Namespace, Collection, and Document are used as defined in
    the Google Cloud Firestore API.

    Operation: An Operation represents work being performed in the background.


    # Services

    ## Index

    The index service manages Cloud Firestore indexes.

    Index creation is performed asynchronously.
    An Operation resource is created for each such asynchronous operation.
    The state of the operation (including any errors encountered)
    may be queried via the Operation resource.

    ## Metadata

    Provides metadata and statistical information about data in Cloud Firestore.
    The data provided as part of this API may be stale.

    ## Operation

    The Operations collection provides a record of actions performed for the
    specified Project (including any Operations in progress). Operations are not
    created directly but through calls on other collections or resources.

    An Operation that is not yet done may be cancelled. The request to cancel is
    asynchronous and the Operation may continue to run for some time after the
    request to cancel is made.

    An Operation that is done may be deleted so that it is no longer listed as
    part of the Operation collection.

    Operations are created by service ``FirestoreAdmin``, but are accessed via
    service ``google.longrunning.Operations``.
    """

    SERVICE_ADDRESS = 'firestore.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    _PAGE_DESCRIPTORS = {
        'list_indexes': _PageDesc('page_token', 'next_page_token', 'indexes')
    }

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/datastore', )

    _DATABASE_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/databases/{database}')
    _INDEX_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/databases/{database}/indexes/{index}')

    @classmethod
    def database_path(cls, project, database):
        """Returns a fully-qualified database resource name string."""
        return cls._DATABASE_PATH_TEMPLATE.render({
            'project': project,
            'database': database,
        })

    @classmethod
    def index_path(cls, project, database, index):
        """Returns a fully-qualified index resource name string."""
        return cls._INDEX_PATH_TEMPLATE.render({
            'project': project,
            'database': database,
            'index': index,
        })

    @classmethod
    def match_project_from_database_name(cls, database_name):
        """Parses the project from a database resource.

        Args:
            database_name (str): A fully-qualified path representing a database
                resource.

        Returns:
            A string representing the project.
        """
        return cls._DATABASE_PATH_TEMPLATE.match(database_name).get('project')

    @classmethod
    def match_database_from_database_name(cls, database_name):
        """Parses the database from a database resource.

        Args:
            database_name (str): A fully-qualified path representing a database
                resource.

        Returns:
            A string representing the database.
        """
        return cls._DATABASE_PATH_TEMPLATE.match(database_name).get('database')

    @classmethod
    def match_project_from_index_name(cls, index_name):
        """Parses the project from a index resource.

        Args:
            index_name (str): A fully-qualified path representing a index
                resource.

        Returns:
            A string representing the project.
        """
        return cls._INDEX_PATH_TEMPLATE.match(index_name).get('project')

    @classmethod
    def match_database_from_index_name(cls, index_name):
        """Parses the database from a index resource.

        Args:
            index_name (str): A fully-qualified path representing a index
                resource.

        Returns:
            A string representing the database.
        """
        return cls._INDEX_PATH_TEMPLATE.match(index_name).get('database')

    @classmethod
    def match_index_from_index_name(cls, index_name):
        """Parses the index from a index resource.

        Args:
            index_name (str): A fully-qualified path representing a index
                resource.

        Returns:
            A string representing the index.
        """
        return cls._INDEX_PATH_TEMPLATE.match(index_name).get('index')

    def __init__(self,
                 channel=None,
                 credentials=None,
                 ssl_credentials=None,
                 scopes=None,
                 client_config=None,
                 lib_name=None,
                 lib_version='',
                 metrics_headers=()):
        """Constructor.

        Args:
            channel (~grpc.Channel): A ``Channel`` instance through
                which to make calls.
            credentials (~google.auth.credentials.Credentials): The authorization
                credentials to attach to requests. These credentials identify this
                application to the service.
            ssl_credentials (~grpc.ChannelCredentials): A
                ``ChannelCredentials`` instance for use with an SSL-enabled
                channel.
            scopes (Sequence[str]): A list of OAuth2 scopes to attach to requests.
            client_config (dict):
                A dictionary for call options for each method. See
                :func:`google.gax.construct_settings` for the structure of
                this data. Falls back to the default config if not specified
                or the specified config is missing data points.
            lib_name (str): The API library software used for calling
                the service. (Unless you are writing an API client itself,
                leave this as default.)
            lib_version (str): The API library software version used
                for calling the service. (Unless you are writing an API client
                itself, leave this as default.)
            metrics_headers (dict): A dictionary of values for tracking
                client library metrics. Ultimately serializes to a string
                (e.g. 'foo/1.2.3 bar/3.14.1'). This argument should be
                considered private.
        """
        # Unless the calling application specifically requested
        # OAuth scopes, request everything.
        if scopes is None:
            scopes = self._ALL_SCOPES

        # Initialize an empty client config, if none is set.
        if client_config is None:
            client_config = {}

        # Initialize metrics_headers as an ordered dictionary
        # (cuts down on cardinality of the resulting string slightly).
        metrics_headers = collections.OrderedDict(metrics_headers)
        metrics_headers['gl-python'] = platform.python_version()

        # The library may or may not be set, depending on what is
        # calling this client. Newer client libraries set the library name
        # and version.
        if lib_name:
            metrics_headers[lib_name] = lib_version

        # Finally, track the GAPIC package version.
        metrics_headers['gapic'] = pkg_resources.get_distribution(
            'google-cloud-firestore', ).version

        # Load the configuration defaults.
        defaults = api_callable.construct_settings(
            'google.firestore.admin.v1beta1.FirestoreAdmin',
            firestore_admin_client_config.config,
            client_config,
            config.STATUS_CODE_NAMES,
            metrics_headers=metrics_headers,
            page_descriptors=self._PAGE_DESCRIPTORS, )
        self.firestore_admin_stub = config.create_stub(
            firestore_admin_pb2.FirestoreAdminStub,
            channel=channel,
            service_path=self.SERVICE_ADDRESS,
            service_port=self.DEFAULT_SERVICE_PORT,
            credentials=credentials,
            scopes=scopes,
            ssl_credentials=ssl_credentials)

        self._create_index = api_callable.create_api_call(
            self.firestore_admin_stub.CreateIndex,
            settings=defaults['create_index'])
        self._list_indexes = api_callable.create_api_call(
            self.firestore_admin_stub.ListIndexes,
            settings=defaults['list_indexes'])
        self._get_index = api_callable.create_api_call(
            self.firestore_admin_stub.GetIndex, settings=defaults['get_index'])
        self._delete_index = api_callable.create_api_call(
            self.firestore_admin_stub.DeleteIndex,
            settings=defaults['delete_index'])

    # Service calls
    def create_index(self, parent, index, options=None):
        """
        Creates the specified index.
        A newly created index's initial state is ``CREATING``. On completion of the
        returned ``google.longrunning.Operation``, the state will be ``READY``.
        If the index already exists, the call will return an ``ALREADY_EXISTS``
        status.

        During creation, the process could result in an error, in which case the
        index will move to the ``ERROR`` state. The process can be recovered by
        fixing the data that caused the error, removing the index with
        ``delete``, then re-creating the index with
        ``create``.

        Indexes with a single field cannot be created.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreAdminClient()
            >>>
            >>> parent = client.database_path('[PROJECT]', '[DATABASE]')
            >>> index = {}
            >>>
            >>> response = client.create_index(parent, index)

        Args:
            parent (str): The name of the database this index will apply to. For example:
                ``projects/{project_id}/databases/{database_id}``
            index (Union[dict, ~google.cloud.firestore_v1beta1.types.Index]): The index to create. The name and state should not be specified.
                Certain single field indexes cannot be created or deleted.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.firestore_v1beta1.types.Index`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.Operation` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_admin_pb2.CreateIndexRequest(
            parent=parent, index=index)
        return self._create_index(request, options)

    def list_indexes(self, parent, filter_=None, page_size=None, options=None):
        """
        Lists the indexes that match the specified filters.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>> from google.gax import CallOptions, INITIAL_PAGE
            >>>
            >>> client = firestore_v1beta1.FirestoreAdminClient()
            >>>
            >>> parent = client.database_path('[PROJECT]', '[DATABASE]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_indexes(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_indexes(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The database name. For example:
                ``projects/{project_id}/databases/{database_id}``
            filter_ (str)
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.firestore_v1beta1.types.Index` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_admin_pb2.ListIndexesRequest(
            parent=parent, filter=filter_, page_size=page_size)
        return self._list_indexes(request, options)

    def get_index(self, name, options=None):
        """
        Gets an index.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreAdminClient()
            >>>
            >>> name = client.index_path('[PROJECT]', '[DATABASE]', '[INDEX]')
            >>>
            >>> response = client.get_index(name)

        Args:
            name (str): The name of the index. For example:
                ``projects/{project_id}/databases/{database_id}/indexes/{index_id}``
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.firestore_v1beta1.types.Index` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_admin_pb2.GetIndexRequest(name=name)
        return self._get_index(request, options)

    def delete_index(self, name, options=None):
        """
        Deletes an index.

        Example:
            >>> from google.cloud import firestore_v1beta1
            >>>
            >>> client = firestore_v1beta1.FirestoreAdminClient()
            >>>
            >>> name = client.index_path('[PROJECT]', '[DATABASE]', '[INDEX]')
            >>>
            >>> client.delete_index(name)

        Args:
            name (str): The index name. For example:
                ``projects/{project_id}/databases/{database_id}/indexes/{index_id}``
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = firestore_admin_pb2.DeleteIndexRequest(name=name)
        self._delete_index(request, options)
