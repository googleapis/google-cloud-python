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

"""Accesses the google.bigtable.admin.v2 BigtableTableAdmin API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client_config
from google.cloud.bigtable_admin_v2.gapic import enums
from google.cloud.bigtable_admin_v2.gapic.transports import (
    bigtable_table_admin_grpc_transport,
)
from google.cloud.bigtable_admin_v2.proto import bigtable_instance_admin_pb2
from google.cloud.bigtable_admin_v2.proto import bigtable_instance_admin_pb2_grpc
from google.cloud.bigtable_admin_v2.proto import bigtable_table_admin_pb2
from google.cloud.bigtable_admin_v2.proto import bigtable_table_admin_pb2_grpc
from google.cloud.bigtable_admin_v2.proto import instance_pb2
from google.cloud.bigtable_admin_v2.proto import table_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import options_pb2
from google.iam.v1 import policy_pb2
from google.longrunning import operations_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-bigtable").version


class BigtableTableAdminClient(object):
    """
    Service for creating, configuring, and deleting Cloud Bigtable tables.


    Provides access to the table schemas only, not the data stored within
    the tables.
    """

    SERVICE_ADDRESS = "bigtableadmin.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.bigtable.admin.v2.BigtableTableAdmin"

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
            BigtableTableAdminClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def cluster_path(cls, project, instance, cluster):
        """Return a fully-qualified cluster string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}/clusters/{cluster}",
            project=project,
            instance=instance,
            cluster=cluster,
        )

    @classmethod
    def instance_path(cls, project, instance):
        """Return a fully-qualified instance string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}",
            project=project,
            instance=instance,
        )

    @classmethod
    def snapshot_path(cls, project, instance, cluster, snapshot):
        """Return a fully-qualified snapshot string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}/clusters/{cluster}/snapshots/{snapshot}",
            project=project,
            instance=instance,
            cluster=cluster,
            snapshot=snapshot,
        )

    @classmethod
    def table_path(cls, project, instance, table):
        """Return a fully-qualified table string."""
        return google.api_core.path_template.expand(
            "projects/{project}/instances/{instance}/tables/{table}",
            project=project,
            instance=instance,
            table=table,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.BigtableTableAdminGrpcTransport,
                    Callable[[~.Credentials, type], ~.BigtableTableAdminGrpcTransport]): A transport
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
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = bigtable_table_admin_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=bigtable_table_admin_grpc_transport.BigtableTableAdminGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = bigtable_table_admin_grpc_transport.BigtableTableAdminGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
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
    def create_table(
        self,
        parent,
        table_id,
        table,
        initial_splits=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new table in the specified instance.
        The table can be created with a full set of initial column families,
        specified in the request.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize `table_id`:
            >>> table_id = ''
            >>>
            >>> # TODO: Initialize `table`:
            >>> table = {}
            >>>
            >>> response = client.create_table(parent, table_id, table)

        Args:
            parent (str): The unique name of the instance in which to create the table. Values are
                of the form ``projects/<project>/instances/<instance>``.
            table_id (str): The name by which the new table should be referred to within the parent
                instance, e.g., ``foobar`` rather than ``<parent>/tables/foobar``.
            table (Union[dict, ~google.cloud.bigtable_admin_v2.types.Table]): The Table to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Table`
            initial_splits (list[Union[dict, ~google.cloud.bigtable_admin_v2.types.Split]]): The optional list of row keys that will be used to initially split the
                table into several tablets (tablets are similar to HBase regions). Given
                two split keys, ``s1`` and ``s2``, three tablets will be created,
                spanning the key ranges: ``[, s1), [s1, s2), [s2, )``.

                Example:

                -  Row keys := ``["a", "apple", "custom", "customer_1", "customer_2",``
                   ``"other", "zz"]``
                -  initial\_split\_keys :=
                   ``["apple", "customer_1", "customer_2", "other"]``
                -  Key assignment:

                   -  Tablet 1 ``[, apple) => {"a"}.``
                   -  Tablet 2 ``[apple, customer_1) => {"apple", "custom"}.``
                   -  Tablet 3 ``[customer_1, customer_2) => {"customer_1"}.``
                   -  Tablet 4 ``[customer_2, other) => {"customer_2"}.``
                   -  Tablet 5 ``[other, ) => {"other", "zz"}.``

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Split`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Table` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_table" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_table"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_table,
                default_retry=self._method_configs["CreateTable"].retry,
                default_timeout=self._method_configs["CreateTable"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.CreateTableRequest(
            parent=parent, table_id=table_id, table=table, initial_splits=initial_splits
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_table"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_table_from_snapshot(
        self,
        parent,
        table_id,
        source_snapshot,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new table from the specified snapshot. The target table must
        not exist. The snapshot and the table must be in the same instance.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # TODO: Initialize `table_id`:
            >>> table_id = ''
            >>>
            >>> # TODO: Initialize `source_snapshot`:
            >>> source_snapshot = ''
            >>>
            >>> response = client.create_table_from_snapshot(parent, table_id, source_snapshot)
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
            parent (str): The unique name of the instance in which to create the table. Values are
                of the form ``projects/<project>/instances/<instance>``.
            table_id (str): The name by which the new table should be referred to within the parent
                instance, e.g., ``foobar`` rather than ``<parent>/tables/foobar``.
            source_snapshot (str): The unique name of the snapshot from which to restore the table. The
                snapshot and the table must be in the same instance. Values are of the
                form
                ``projects/<project>/instances/<instance>/clusters/<cluster>/snapshots/<snapshot>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_table_from_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_table_from_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_table_from_snapshot,
                default_retry=self._method_configs["CreateTableFromSnapshot"].retry,
                default_timeout=self._method_configs["CreateTableFromSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.CreateTableFromSnapshotRequest(
            parent=parent, table_id=table_id, source_snapshot=source_snapshot
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["create_table_from_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            table_pb2.Table,
            metadata_type=bigtable_table_admin_pb2.CreateTableFromSnapshotMetadata,
        )

    def list_tables(
        self,
        parent,
        view=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all tables served from a specified instance.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> parent = client.instance_path('[PROJECT]', '[INSTANCE]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_tables(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_tables(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The unique name of the instance for which tables should be listed.
                Values are of the form ``projects/<project>/instances/<instance>``.
            view (~google.cloud.bigtable_admin_v2.types.View): The view to be applied to the returned tables' fields. Defaults to
                ``NAME_ONLY`` if unspecified; no others are currently supported.
            page_size (int): Maximum number of results per page.
                CURRENTLY UNIMPLEMENTED AND IGNORED.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.bigtable_admin_v2.types.Table` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_tables" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_tables"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_tables,
                default_retry=self._method_configs["ListTables"].retry,
                default_timeout=self._method_configs["ListTables"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.ListTablesRequest(
            parent=parent, view=view, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_tables"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="tables",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_table(
        self,
        name,
        view=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets metadata information about the specified table.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> response = client.get_table(name)

        Args:
            name (str): The unique name of the requested table. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            view (~google.cloud.bigtable_admin_v2.types.View): The view to be applied to the returned table's fields. Defaults to
                ``SCHEMA_VIEW`` if unspecified.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Table` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_table" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_table"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_table,
                default_retry=self._method_configs["GetTable"].retry,
                default_timeout=self._method_configs["GetTable"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.GetTableRequest(name=name, view=view)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_table"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_table(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Permanently deletes a specified table and all of its data.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> client.delete_table(name)

        Args:
            name (str): The unique name of the table to be deleted. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "delete_table" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_table"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_table,
                default_retry=self._method_configs["DeleteTable"].retry,
                default_timeout=self._method_configs["DeleteTable"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.DeleteTableRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_table"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def modify_column_families(
        self,
        name,
        modifications,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Performs a series of column family modifications on the specified table.
        Either all or none of the modifications will occur before this method
        returns, but data requests received prior to that point may see a table
        where only some modifications have taken effect.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> # TODO: Initialize `modifications`:
            >>> modifications = []
            >>>
            >>> response = client.modify_column_families(name, modifications)

        Args:
            name (str): The unique name of the table whose families should be modified. Values
                are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            modifications (list[Union[dict, ~google.cloud.bigtable_admin_v2.types.Modification]]): Modifications to be atomically applied to the specified table's families.
                Entries are applied in order, meaning that earlier modifications can be
                masked by later ones (in the case of repeated updates to the same family,
                for example).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Modification`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Table` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "modify_column_families" not in self._inner_api_calls:
            self._inner_api_calls[
                "modify_column_families"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.modify_column_families,
                default_retry=self._method_configs["ModifyColumnFamilies"].retry,
                default_timeout=self._method_configs["ModifyColumnFamilies"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.ModifyColumnFamiliesRequest(
            name=name, modifications=modifications
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["modify_column_families"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def drop_row_range(
        self,
        name,
        row_key_prefix=None,
        delete_all_data_from_table=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Permanently drop/delete a row range from a specified table. The request can
        specify whether to delete all rows in a table, or only those that match a
        particular prefix.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> client.drop_row_range(name)

        Args:
            name (str): The unique name of the table on which to drop a range of rows. Values
                are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            row_key_prefix (bytes): Delete all rows that start with this row key prefix. Prefix cannot be
                zero length.
            delete_all_data_from_table (bool): Delete all rows in the table. Setting this to false is a no-op.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "drop_row_range" not in self._inner_api_calls:
            self._inner_api_calls[
                "drop_row_range"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.drop_row_range,
                default_retry=self._method_configs["DropRowRange"].retry,
                default_timeout=self._method_configs["DropRowRange"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            row_key_prefix=row_key_prefix,
            delete_all_data_from_table=delete_all_data_from_table,
        )

        request = bigtable_table_admin_pb2.DropRowRangeRequest(
            name=name,
            row_key_prefix=row_key_prefix,
            delete_all_data_from_table=delete_all_data_from_table,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["drop_row_range"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def generate_consistency_token(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Generates a consistency token for a Table, which can be used in
        CheckConsistency to check whether mutations to the table that finished
        before this call started have been replicated. The tokens will be available
        for 90 days.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> response = client.generate_consistency_token(name)

        Args:
            name (str): The unique name of the Table for which to create a consistency token.
                Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.GenerateConsistencyTokenResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "generate_consistency_token" not in self._inner_api_calls:
            self._inner_api_calls[
                "generate_consistency_token"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.generate_consistency_token,
                default_retry=self._method_configs["GenerateConsistencyToken"].retry,
                default_timeout=self._method_configs[
                    "GenerateConsistencyToken"
                ].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.GenerateConsistencyTokenRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["generate_consistency_token"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def check_consistency(
        self,
        name,
        consistency_token,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Checks replication consistency based on a consistency token, that is, if
        replication has caught up based on the conditions specified in the token
        and the check request.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> # TODO: Initialize `consistency_token`:
            >>> consistency_token = ''
            >>>
            >>> response = client.check_consistency(name, consistency_token)

        Args:
            name (str): The unique name of the Table for which to check replication consistency.
                Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            consistency_token (str): The token created using GenerateConsistencyToken for the Table.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.CheckConsistencyResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "check_consistency" not in self._inner_api_calls:
            self._inner_api_calls[
                "check_consistency"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.check_consistency,
                default_retry=self._method_configs["CheckConsistency"].retry,
                default_timeout=self._method_configs["CheckConsistency"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.CheckConsistencyRequest(
            name=name, consistency_token=consistency_token
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["check_consistency"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource,
        options_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the access control policy for an instance resource. Returns an empty
        policy if an table exists but does not have a policy set.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> resource = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                See the operation documentation for the appropriate value for this field.
            options_ (Union[dict, ~google.cloud.bigtable_admin_v2.types.GetPolicyOptions]): OPTIONAL: A ``GetPolicyOptions`` object for specifying options to
                ``GetIamPolicy``. This field is only used by Cloud IAM.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.GetPolicyOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Policy` instance.

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

        request = iam_policy_pb2.GetIamPolicyRequest(
            resource=resource, options=options_
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_iam_policy"](
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
        Sets the access control policy on a table resource. Replaces any existing
        policy.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> resource = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                See the operation documentation for the appropriate value for this field.
            policy (Union[dict, ~google.cloud.bigtable_admin_v2.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Policy` instance.

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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_iam_policy"](
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
        Returns permissions that the caller has on the specified table resource.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> resource = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                See the operation documentation for the appropriate value for this field.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.TestIamPermissionsResponse` instance.

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
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def snapshot_table(
        self,
        name,
        cluster,
        snapshot_id,
        description,
        ttl=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new snapshot in the specified cluster from the specified
        source table. The cluster and the table must be in the same instance.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> # TODO: Initialize `cluster`:
            >>> cluster = ''
            >>>
            >>> # TODO: Initialize `snapshot_id`:
            >>> snapshot_id = ''
            >>>
            >>> # TODO: Initialize `description`:
            >>> description = ''
            >>>
            >>> response = client.snapshot_table(name, cluster, snapshot_id, description)
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
            name (str): The unique name of the table to have the snapshot taken. Values are of
                the form ``projects/<project>/instances/<instance>/tables/<table>``.
            cluster (str): The name of the cluster where the snapshot will be created in. Values
                are of the form
                ``projects/<project>/instances/<instance>/clusters/<cluster>``.
            snapshot_id (str): The ID by which the new snapshot should be referred to within the parent
                cluster, e.g., ``mysnapshot`` of the form:
                ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*`` rather than
                ``projects/<project>/instances/<instance>/clusters/<cluster>/snapshots/mysnapshot``.
            description (str): Description of the snapshot.
            ttl (Union[dict, ~google.cloud.bigtable_admin_v2.types.Duration]): The amount of time that the new snapshot can stay active after it is
                created. Once 'ttl' expires, the snapshot will get deleted. The maximum
                amount of time a snapshot can stay active is 7 days. If 'ttl' is not
                specified, the default value of 24 hours will be used.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_admin_v2.types.Duration`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "snapshot_table" not in self._inner_api_calls:
            self._inner_api_calls[
                "snapshot_table"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.snapshot_table,
                default_retry=self._method_configs["SnapshotTable"].retry,
                default_timeout=self._method_configs["SnapshotTable"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.SnapshotTableRequest(
            name=name,
            cluster=cluster,
            snapshot_id=snapshot_id,
            description=description,
            ttl=ttl,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["snapshot_table"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            table_pb2.Snapshot,
            metadata_type=bigtable_table_admin_pb2.SnapshotTableMetadata,
        )

    def get_snapshot(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets metadata information about the specified snapshot.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> name = client.snapshot_path('[PROJECT]', '[INSTANCE]', '[CLUSTER]', '[SNAPSHOT]')
            >>>
            >>> response = client.get_snapshot(name)

        Args:
            name (str): The unique name of the requested snapshot. Values are of the form
                ``projects/<project>/instances/<instance>/clusters/<cluster>/snapshots/<snapshot>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_admin_v2.types.Snapshot` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_snapshot,
                default_retry=self._method_configs["GetSnapshot"].retry,
                default_timeout=self._method_configs["GetSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.GetSnapshotRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_snapshots(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists all snapshots associated with the specified cluster.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> parent = client.cluster_path('[PROJECT]', '[INSTANCE]', '[CLUSTER]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_snapshots(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_snapshots(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The unique name of the cluster for which snapshots should be listed.
                Values are of the form
                ``projects/<project>/instances/<instance>/clusters/<cluster>``. Use
                ``<cluster> = '-'`` to list snapshots for all clusters in an instance,
                e.g., ``projects/<project>/instances/<instance>/clusters/-``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.bigtable_admin_v2.types.Snapshot` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_snapshots" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_snapshots"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_snapshots,
                default_retry=self._method_configs["ListSnapshots"].retry,
                default_timeout=self._method_configs["ListSnapshots"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.ListSnapshotsRequest(
            parent=parent, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_snapshots"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="snapshots",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_snapshot(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Permanently deletes the specified snapshot.

        Note: This is a private alpha release of Cloud Bigtable snapshots. This
        feature is not currently available to most Cloud Bigtable customers. This
        feature might be changed in backward-incompatible ways and is not
        recommended for production use. It is not subject to any SLA or deprecation
        policy.

        Example:
            >>> from google.cloud import bigtable_admin_v2
            >>>
            >>> client = bigtable_admin_v2.BigtableTableAdminClient()
            >>>
            >>> name = client.snapshot_path('[PROJECT]', '[INSTANCE]', '[CLUSTER]', '[SNAPSHOT]')
            >>>
            >>> client.delete_snapshot(name)

        Args:
            name (str): The unique name of the snapshot to be deleted. Values are of the form
                ``projects/<project>/instances/<instance>/clusters/<cluster>/snapshots/<snapshot>``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
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
        if "delete_snapshot" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_snapshot"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_snapshot,
                default_retry=self._method_configs["DeleteSnapshot"].retry,
                default_timeout=self._method_configs["DeleteSnapshot"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_table_admin_pb2.DeleteSnapshotRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_snapshot"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
