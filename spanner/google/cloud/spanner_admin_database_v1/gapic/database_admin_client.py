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
# https://github.com/google/googleapis/blob/master/google/spanner/admin/database/v1/spanner_database_admin.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.spanner.admin.database.v1 DatabaseAdmin API."""

import collections
import json
import os
import pkg_resources
import platform

from google.gapic.longrunning import operations_client
from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.cloud.spanner_admin_database_v1.gapic import database_admin_client_config
from google.cloud.spanner_admin_database_v1.gapic import enums
from google.cloud.spanner_admin_database_v1.proto import spanner_database_admin_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import empty_pb2

_PageDesc = google.gax.PageDescriptor


class DatabaseAdminClient(object):
    """
    Cloud Spanner Database Admin API

    The Cloud Spanner Database Admin API can be used to create, drop, and
    list databases. It also enables updating the schema of pre-existing
    databases.
    """

    SERVICE_ADDRESS = 'spanner.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    _PAGE_DESCRIPTORS = {
        'list_databases': _PageDesc('page_token', 'next_page_token',
                                    'databases')
    }

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/spanner.admin', )

    _INSTANCE_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/instances/{instance}')
    _DATABASE_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/instances/{instance}/databases/{database}')

    @classmethod
    def instance_path(cls, project, instance):
        """Returns a fully-qualified instance resource name string."""
        return cls._INSTANCE_PATH_TEMPLATE.render({
            'project': project,
            'instance': instance,
        })

    @classmethod
    def database_path(cls, project, instance, database):
        """Returns a fully-qualified database resource name string."""
        return cls._DATABASE_PATH_TEMPLATE.render({
            'project': project,
            'instance': instance,
            'database': database,
        })

    @classmethod
    def match_project_from_instance_name(cls, instance_name):
        """Parses the project from a instance resource.

        Args:
            instance_name (str): A fully-qualified path representing a instance
                resource.

        Returns:
            A string representing the project.
        """
        return cls._INSTANCE_PATH_TEMPLATE.match(instance_name).get('project')

    @classmethod
    def match_instance_from_instance_name(cls, instance_name):
        """Parses the instance from a instance resource.

        Args:
            instance_name (str): A fully-qualified path representing a instance
                resource.

        Returns:
            A string representing the instance.
        """
        return cls._INSTANCE_PATH_TEMPLATE.match(instance_name).get('instance')

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
    def match_instance_from_database_name(cls, database_name):
        """Parses the instance from a database resource.

        Args:
            database_name (str): A fully-qualified path representing a database
                resource.

        Returns:
            A string representing the instance.
        """
        return cls._DATABASE_PATH_TEMPLATE.match(database_name).get('instance')

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
            'google-cloud-spanner', ).version

        # Load the configuration defaults.
        defaults = api_callable.construct_settings(
            'google.spanner.admin.database.v1.DatabaseAdmin',
            database_admin_client_config.config,
            client_config,
            config.STATUS_CODE_NAMES,
            metrics_headers=metrics_headers,
            page_descriptors=self._PAGE_DESCRIPTORS, )
        self.database_admin_stub = config.create_stub(
            spanner_database_admin_pb2.DatabaseAdminStub,
            channel=channel,
            service_path=self.SERVICE_ADDRESS,
            service_port=self.DEFAULT_SERVICE_PORT,
            credentials=credentials,
            scopes=scopes,
            ssl_credentials=ssl_credentials)

        self.operations_client = operations_client.OperationsClient(
            service_path=self.SERVICE_ADDRESS,
            channel=channel,
            credentials=credentials,
            ssl_credentials=ssl_credentials,
            scopes=scopes,
            client_config=client_config,
            metrics_headers=metrics_headers, )

        self._list_databases = api_callable.create_api_call(
            self.database_admin_stub.ListDatabases,
            settings=defaults['list_databases'])
        self._create_database = api_callable.create_api_call(
            self.database_admin_stub.CreateDatabase,
            settings=defaults['create_database'])
        self._get_database = api_callable.create_api_call(
            self.database_admin_stub.GetDatabase,
            settings=defaults['get_database'])
        self._update_database_ddl = api_callable.create_api_call(
            self.database_admin_stub.UpdateDatabaseDdl,
            settings=defaults['update_database_ddl'])
        self._drop_database = api_callable.create_api_call(
            self.database_admin_stub.DropDatabase,
            settings=defaults['drop_database'])
        self._get_database_ddl = api_callable.create_api_call(
            self.database_admin_stub.GetDatabaseDdl,
            settings=defaults['get_database_ddl'])
        self._set_iam_policy = api_callable.create_api_call(
            self.database_admin_stub.SetIamPolicy,
            settings=defaults['set_iam_policy'])
        self._get_iam_policy = api_callable.create_api_call(
            self.database_admin_stub.GetIamPolicy,
            settings=defaults['get_iam_policy'])
        self._test_iam_permissions = api_callable.create_api_call(
            self.database_admin_stub.TestIamPermissions,
            settings=defaults['test_iam_permissions'])

    # Service calls
    def list_databases(self, parent, page_size=None, options=None):
        """
        Lists Cloud Spanner databases.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>> from google.gax import CallOptions, INITIAL_PAGE
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_databases(parent):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_databases(parent, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The instance whose databases should be listed.
                Values are of the form ``projects/<project>/instances/<instance>``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.spanner_admin_database_v1.types.Database` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_database_admin_pb2.ListDatabasesRequest(
            parent=parent, page_size=page_size)
        return self._list_databases(request, options)

    def create_database(self,
                        parent,
                        create_statement,
                        extra_statements=None,
                        options=None):
        """
        Creates a new Cloud Spanner database and starts to prepare it for serving.
        The returned ``long-running operation`` will
        have a name of the format ``<database_name>/operations/<operation_id>`` and
        can be used to track preparation of the database. The
        ``metadata`` field type is
        ``CreateDatabaseMetadata``. The
        ``response`` field type is
        ``Database``, if successful.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>> create_statement = ''
            >>>
            >>> response = client.create_database(parent, create_statement)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            parent (str): Required. The name of the instance that will serve the new database.
                Values are of the form ``projects/<project>/instances/<instance>``.
            create_statement (str): Required. A ``CREATE DATABASE`` statement, which specifies the ID of the
                new database.  The database ID must conform to the regular expression
                ``[a-z][a-z0-9_\-]*[a-z0-9]`` and be between 2 and 30 characters in length.
            extra_statements (list[str]): An optional list of DDL statements to run inside the newly created
                database. Statements can create tables, indexes, etc. These
                statements execute atomically with the creation of the database:
                if there is an error in any statement, the database is not created.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types._OperationFuture` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_database_admin_pb2.CreateDatabaseRequest(
            parent=parent,
            create_statement=create_statement,
            extra_statements=extra_statements)
        return google.gax._OperationFuture(
            self._create_database(request, options), self.operations_client,
            spanner_database_admin_pb2.Database,
            spanner_database_admin_pb2.CreateDatabaseMetadata, options)

    def get_database(self, name, options=None):
        """
        Gets the state of a Cloud Spanner database.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> name = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>>
            >>> response = client.get_database(name)

        Args:
            name (str): Required. The name of the requested database. Values are of the form
                ``projects/<project>/instances/<instance>/databases/<database>``.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.Database` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_database_admin_pb2.GetDatabaseRequest(name=name)
        return self._get_database(request, options)

    def update_database_ddl(self,
                            database,
                            statements,
                            operation_id=None,
                            options=None):
        """
        Updates the schema of a Cloud Spanner database by
        creating/altering/dropping tables, columns, indexes, etc. The returned
        ``long-running operation`` will have a name of
        the format ``<database_name>/operations/<operation_id>`` and can be used to
        track execution of the schema change(s). The
        ``metadata`` field type is
        ``UpdateDatabaseDdlMetadata``.  The operation has no response.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> database = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>> statements = []
            >>>
            >>> response = client.update_database_ddl(database, statements)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            database (str): Required. The database to update.
            statements (list[str]): DDL statements to be applied to the database.
            operation_id (str): If empty, the new update request is assigned an
                automatically-generated operation ID. Otherwise, ``operation_id``
                is used to construct the name of the resulting
                ``Operation``.

                Specifying an explicit operation ID simplifies determining
                whether the statements were executed in the event that the
                ``UpdateDatabaseDdl`` call is replayed,
                or the return value is otherwise lost: the ``database`` and
                ``operation_id`` fields can be combined to form the
                ``name`` of the resulting
                ``longrunning.Operation``: ``<database>/operations/<operation_id>``.

                ``operation_id`` should be unique within the database, and must be
                a valid identifier: ``[a-z][a-z0-9_]*``. Note that
                automatically-generated operation IDs always begin with an
                underscore. If the named operation already exists,
                ``UpdateDatabaseDdl`` returns
                ``ALREADY_EXISTS``.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types._OperationFuture` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_database_admin_pb2.UpdateDatabaseDdlRequest(
            database=database,
            statements=statements,
            operation_id=operation_id)
        return google.gax._OperationFuture(
            self._update_database_ddl(request, options),
            self.operations_client, empty_pb2.Empty,
            spanner_database_admin_pb2.UpdateDatabaseDdlMetadata, options)

    def drop_database(self, database, options=None):
        """
        Drops (aka deletes) a Cloud Spanner database.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> database = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>>
            >>> client.drop_database(database)

        Args:
            database (str): Required. The database to be dropped.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_database_admin_pb2.DropDatabaseRequest(
            database=database)
        self._drop_database(request, options)

    def get_database_ddl(self, database, options=None):
        """
        Returns the schema of a Cloud Spanner database as a list of formatted
        DDL statements. This method does not show pending schema updates, those may
        be queried using the ``Operations`` API.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> database = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>>
            >>> response = client.get_database_ddl(database)

        Args:
            database (str): Required. The database whose schema we wish to get.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.GetDatabaseDdlResponse` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = spanner_database_admin_pb2.GetDatabaseDdlRequest(
            database=database)
        return self._get_database_ddl(request, options)

    def set_iam_policy(self, resource, policy, options=None):
        """
        Sets the access control policy on a database resource. Replaces any
        existing policy.

        Authorization requires ``spanner.databases.setIamPolicy`` permission on
        ``resource``.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> resource = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.spanner_admin_database_v1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The size of
                the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_admin_database_v1.types.Policy`
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.Policy` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy)
        return self._set_iam_policy(request, options)

    def get_iam_policy(self, resource, options=None):
        """
        Gets the access control policy for a database resource. Returns an empty
        policy if a database exists but does not have a policy set.

        Authorization requires ``spanner.databases.getIamPolicy`` permission on
        ``resource``.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> resource = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.Policy` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        return self._get_iam_policy(request, options)

    def test_iam_permissions(self, resource, permissions, options=None):
        """
        Returns permissions that the caller has on the specified database resource.

        Attempting this RPC on a non-existent Cloud Spanner database will result in
        a NOT_FOUND error if the user has ``spanner.databases.list`` permission on
        the containing Cloud Spanner instance. Otherwise returns an empty set of
        permissions.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> resource = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see
                `IAM Overview <https://cloud.google.com/iam/docs/overview#permissions>`_.
            options (~google.gax.CallOptions): Overrides the default
                settings for this call, e.g, timeout, retries etc.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            :exc:`google.gax.errors.GaxError` if the RPC is aborted.
            :exc:`ValueError` if the parameters are invalid.
        """
        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions)
        return self._test_iam_permissions(request, options)
