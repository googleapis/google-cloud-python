# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Accesses the google.spanner.admin.database.v1 DatabaseAdmin API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.spanner_admin_database_v1.gapic import database_admin_client_config
from google.cloud.spanner_admin_database_v1.gapic import enums
from google.cloud.spanner_admin_database_v1.gapic.transports import (
    database_admin_grpc_transport,
)
from google.cloud.spanner_admin_database_v1.proto import spanner_database_admin_pb2
from google.cloud.spanner_admin_database_v1.proto import spanner_database_admin_pb2_grpc
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-spanner").version


class DatabaseAdminClient(object):
    """
    Cloud Spanner Database Admin API

    The Cloud Spanner Database Admin API can be used to create, drop, and
    list databases. It also enables updating the schema of pre-existing
    databases.
    """

    SERVICE_ADDRESS = "spanner.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.spanner.admin.database.v1.DatabaseAdmin"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DatabaseAdminClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def instance_path(cls, project, instance):
        """Return a fully-qualified instance string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}",
            project=project,
            instance=instance,
        )

    @classmethod
    def database_path(cls, project, instance, database):
        """Return a fully-qualified database string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}/databases/{database}",
            project=project,
            instance=instance,
            database=database,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.DatabaseAdminGrpcTransport,
                    Callable[[~.Credentials, type], ~.DatabaseAdminGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = database_admin_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=database_admin_grpc_transport.DatabaseAdminGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = database_admin_grpc_transport.DatabaseAdminGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def list_databases(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists Cloud Spanner databases.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_databases(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_databases(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Required. The instance whose databases should be listed. Values are of
                the form ``projects/<project>/instances/<instance>``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.spanner_admin_database_v1.types.Database` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_databases" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_databases"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_databases,
                default_retry=self._method_configs["ListDatabases"].retry,
                default_timeout=self._method_configs["ListDatabases"].timeout,
                client_info=self._client_info,
            )

        request = spanner_database_admin_pb2.ListDatabasesRequest(
            parent=parent, page_size=page_size
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_databases"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="databases",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_database(
        self,
        parent,
        create_statement,
        extra_statements=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new Cloud Spanner database and starts to prepare it for
        serving. The returned ``long-running operation`` will have a name of the
        format ``<database_name>/operations/<operation_id>`` and can be used to
        track preparation of the database. The ``metadata`` field type is
        ``CreateDatabaseMetadata``. The ``response`` field type is ``Database``,
        if successful.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize `create_statement`:
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
                new database. The database ID must conform to the regular expression
                ``[a-z][a-z0-9_\-]*[a-z0-9]`` and be between 2 and 30 characters in
                length. If the database ID is a reserved word or if it contains a
                hyphen, the database ID must be enclosed in backticks (`````).
            extra_statements (list[str]): An optional list of DDL statements to run inside the newly created
                database. Statements can create tables, indexes, etc. These
                statements execute atomically with the creation of the database:
                if there is an error in any statement, the database is not created.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_database" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_database"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_database,
                default_retry=self._method_configs["CreateDatabase"].retry,
                default_timeout=self._method_configs["CreateDatabase"].timeout,
                client_info=self._client_info,
            )

        request = spanner_database_admin_pb2.CreateDatabaseRequest(
            parent=parent,
            create_statement=create_statement,
            extra_statements=extra_statements,
        )
        operation = self._inner_api_calls["create_database"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            spanner_database_admin_pb2.Database,
            metadata_type=spanner_database_admin_pb2.CreateDatabaseMetadata,
        )

    def get_database(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.Database` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_database" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_database"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_database,
                default_retry=self._method_configs["GetDatabase"].retry,
                default_timeout=self._method_configs["GetDatabase"].timeout,
                client_info=self._client_info,
            )

        request = spanner_database_admin_pb2.GetDatabaseRequest(name=name)
        return self._inner_api_calls["get_database"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_database_ddl(
        self,
        database,
        statements,
        operation_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates the schema of a Cloud Spanner database by
        creating/altering/dropping tables, columns, indexes, etc. The returned
        ``long-running operation`` will have a name of the format
        ``<database_name>/operations/<operation_id>`` and can be used to track
        execution of the schema change(s). The ``metadata`` field type is
        ``UpdateDatabaseDdlMetadata``. The operation has no response.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> database = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>>
            >>> # TODO: Initialize `statements`:
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
            operation_id (str): If empty, the new update request is assigned an automatically-generated
                operation ID. Otherwise, ``operation_id`` is used to construct the name
                of the resulting ``Operation``.

                Specifying an explicit operation ID simplifies determining whether the
                statements were executed in the event that the ``UpdateDatabaseDdl``
                call is replayed, or the return value is otherwise lost: the
                ``database`` and ``operation_id`` fields can be combined to form the
                ``name`` of the resulting ``longrunning.Operation``:
                ``<database>/operations/<operation_id>``.

                ``operation_id`` should be unique within the database, and must be a
                valid identifier: ``[a-z][a-z0-9_]*``. Note that automatically-generated
                operation IDs always begin with an underscore. If the named operation
                already exists, ``UpdateDatabaseDdl`` returns ``ALREADY_EXISTS``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_database_ddl" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_database_ddl"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_database_ddl,
                default_retry=self._method_configs["UpdateDatabaseDdl"].retry,
                default_timeout=self._method_configs["UpdateDatabaseDdl"].timeout,
                client_info=self._client_info,
            )

        request = spanner_database_admin_pb2.UpdateDatabaseDdlRequest(
            database=database, statements=statements, operation_id=operation_id
        )
        operation = self._inner_api_calls["update_database_ddl"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=spanner_database_admin_pb2.UpdateDatabaseDdlMetadata,
        )

    def drop_database(
        self,
        database,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "drop_database" not in self._inner_api_calls:
            self._inner_api_calls[
                "drop_database"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.drop_database,
                default_retry=self._method_configs["DropDatabase"].retry,
                default_timeout=self._method_configs["DropDatabase"].timeout,
                client_info=self._client_info,
            )

        request = spanner_database_admin_pb2.DropDatabaseRequest(database=database)
        self._inner_api_calls["drop_database"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_database_ddl(
        self,
        database,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns the schema of a Cloud Spanner database as a list of formatted
        DDL statements. This method does not show pending schema updates, those
        may be queried using the ``Operations`` API.

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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.GetDatabaseDdlResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_database_ddl" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_database_ddl"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_database_ddl,
                default_retry=self._method_configs["GetDatabaseDdl"].retry,
                default_timeout=self._method_configs["GetDatabaseDdl"].timeout,
                client_info=self._client_info,
            )

        request = spanner_database_admin_pb2.GetDatabaseDdlRequest(database=database)
        return self._inner_api_calls["get_database_ddl"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_iam_policy(
        self,
        resource,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.spanner_admin_database_v1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.spanner_admin_database_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_iam_policy,
                default_retry=self._method_configs["SetIamPolicy"].retry,
                default_timeout=self._method_configs["SetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy)
        return self._inner_api_calls["set_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
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
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_iam_policy,
                default_retry=self._method_configs["GetIamPolicy"].retry,
                default_timeout=self._method_configs["GetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        return self._inner_api_calls["get_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns permissions that the caller has on the specified database
        resource.

        Attempting this RPC on a non-existent Cloud Spanner database will result
        in a NOT\_FOUND error if the user has ``spanner.databases.list``
        permission on the containing Cloud Spanner instance. Otherwise returns
        an empty set of permissions.

        Example:
            >>> from google.cloud import spanner_admin_database_v1
            >>>
            >>> client = spanner_admin_database_v1.DatabaseAdminClient()
            >>>
            >>> resource = client.database_path('[PROJECT]', '[INSTANCE]', '[DATABASE]')
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.spanner_admin_database_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "test_iam_permissions" not in self._inner_api_calls:
            self._inner_api_calls[
                "test_iam_permissions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.test_iam_permissions,
                default_retry=self._method_configs["TestIamPermissions"].retry,
                default_timeout=self._method_configs["TestIamPermissions"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
