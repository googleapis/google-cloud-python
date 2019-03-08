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
"""Accesses the google.bigtable.v2 Bigtable API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.bigtable_v2.gapic import bigtable_client_config
from google.cloud.bigtable_v2.gapic.transports import bigtable_grpc_transport
from google.cloud.bigtable_v2.proto import bigtable_pb2
from google.cloud.bigtable_v2.proto import bigtable_pb2_grpc
from google.cloud.bigtable_v2.proto import data_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-bigtable").version


class BigtableClient(object):
    """Service for reading from and writing to existing Bigtable tables."""

    SERVICE_ADDRESS = "bigtable.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.bigtable.v2.Bigtable"

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
            BigtableClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

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
    ):
        """Constructor.

        Args:
            transport (Union[~.BigtableGrpcTransport,
                    Callable[[~.Credentials, type], ~.BigtableGrpcTransport]): A transport
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
            client_config = bigtable_client_config.config

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
                    default_class=bigtable_grpc_transport.BigtableGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = bigtable_grpc_transport.BigtableGrpcTransport(
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
    def read_rows(
        self,
        table_name,
        app_profile_id=None,
        rows=None,
        filter_=None,
        rows_limit=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Streams back the contents of all requested rows in key order, optionally
        applying the same Reader filter to each. Depending on their size,
        rows and cells may be broken up across multiple responses, but
        atomicity of each row will still be preserved. See the
        ReadRowsResponse documentation for details.

        Example:
            >>> from google.cloud import bigtable_v2
            >>>
            >>> client = bigtable_v2.BigtableClient()
            >>>
            >>> table_name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> for element in client.read_rows(table_name):
            ...     # process element
            ...     pass

        Args:
            table_name (str): The unique name of the table from which to read. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            app_profile_id (str): This value specifies routing for replication. If not specified, the
                "default" application profile will be used.
            rows (Union[dict, ~google.cloud.bigtable_v2.types.RowSet]): The row keys and/or ranges to read. If not specified, reads from all rows.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_v2.types.RowSet`
            filter_ (Union[dict, ~google.cloud.bigtable_v2.types.RowFilter]): The filter to apply to the contents of the specified row(s). If unset,
                reads the entirety of each row.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_v2.types.RowFilter`
            rows_limit (long): The read will terminate after committing to N rows' worth of results. The
                default (zero) is to return all results.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.bigtable_v2.types.ReadRowsResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "read_rows" not in self._inner_api_calls:
            self._inner_api_calls[
                "read_rows"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.read_rows,
                default_retry=self._method_configs["ReadRows"].retry,
                default_timeout=self._method_configs["ReadRows"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_pb2.ReadRowsRequest(
            table_name=table_name,
            app_profile_id=app_profile_id,
            rows=rows,
            filter=filter_,
            rows_limit=rows_limit,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("table_name", table_name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["read_rows"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def sample_row_keys(
        self,
        table_name,
        app_profile_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns a sample of row keys in the table. The returned row keys will
        delimit contiguous sections of the table of approximately equal size,
        which can be used to break up the data for distributed tasks like
        mapreduces.

        Example:
            >>> from google.cloud import bigtable_v2
            >>>
            >>> client = bigtable_v2.BigtableClient()
            >>>
            >>> table_name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> for element in client.sample_row_keys(table_name):
            ...     # process element
            ...     pass

        Args:
            table_name (str): The unique name of the table from which to sample row keys. Values are
                of the form ``projects/<project>/instances/<instance>/tables/<table>``.
            app_profile_id (str): This value specifies routing for replication. If not specified, the
                "default" application profile will be used.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.bigtable_v2.types.SampleRowKeysResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "sample_row_keys" not in self._inner_api_calls:
            self._inner_api_calls[
                "sample_row_keys"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.sample_row_keys,
                default_retry=self._method_configs["SampleRowKeys"].retry,
                default_timeout=self._method_configs["SampleRowKeys"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_pb2.SampleRowKeysRequest(
            table_name=table_name, app_profile_id=app_profile_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("table_name", table_name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["sample_row_keys"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def mutate_row(
        self,
        table_name,
        row_key,
        mutations,
        app_profile_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Mutates a row atomically. Cells already present in the row are left
        unchanged unless explicitly changed by ``mutation``.

        Example:
            >>> from google.cloud import bigtable_v2
            >>>
            >>> client = bigtable_v2.BigtableClient()
            >>>
            >>> table_name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> # TODO: Initialize `row_key`:
            >>> row_key = b''
            >>>
            >>> # TODO: Initialize `mutations`:
            >>> mutations = []
            >>>
            >>> response = client.mutate_row(table_name, row_key, mutations)

        Args:
            table_name (str): The unique name of the table to which the mutation should be applied.
                Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            row_key (bytes): The key of the row to which the mutation should be applied.
            mutations (list[Union[dict, ~google.cloud.bigtable_v2.types.Mutation]]): Changes to be atomically applied to the specified row. Entries are applied
                in order, meaning that earlier mutations can be masked by later ones.
                Must contain at least one entry and at most 100000.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_v2.types.Mutation`
            app_profile_id (str): This value specifies routing for replication. If not specified, the
                "default" application profile will be used.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_v2.types.MutateRowResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "mutate_row" not in self._inner_api_calls:
            self._inner_api_calls[
                "mutate_row"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mutate_row,
                default_retry=self._method_configs["MutateRow"].retry,
                default_timeout=self._method_configs["MutateRow"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_pb2.MutateRowRequest(
            table_name=table_name,
            row_key=row_key,
            mutations=mutations,
            app_profile_id=app_profile_id,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("table_name", table_name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["mutate_row"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def mutate_rows(
        self,
        table_name,
        entries,
        app_profile_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Mutates multiple rows in a batch. Each individual row is mutated
        atomically as in MutateRow, but the entire batch is not executed
        atomically.

        Example:
            >>> from google.cloud import bigtable_v2
            >>>
            >>> client = bigtable_v2.BigtableClient()
            >>>
            >>> table_name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> # TODO: Initialize `entries`:
            >>> entries = []
            >>>
            >>> for element in client.mutate_rows(table_name, entries):
            ...     # process element
            ...     pass

        Args:
            table_name (str): The unique name of the table to which the mutations should be applied.
            entries (list[Union[dict, ~google.cloud.bigtable_v2.types.Entry]]): The row keys and corresponding mutations to be applied in bulk.
                Each entry is applied as an atomic mutation, but the entries may be
                applied in arbitrary order (even between entries for the same row).
                At least one entry must be specified, and in total the entries can
                contain at most 100000 mutations.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_v2.types.Entry`
            app_profile_id (str): This value specifies routing for replication. If not specified, the
                "default" application profile will be used.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.bigtable_v2.types.MutateRowsResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "mutate_rows" not in self._inner_api_calls:
            self._inner_api_calls[
                "mutate_rows"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mutate_rows,
                default_retry=self._method_configs["MutateRows"].retry,
                default_timeout=self._method_configs["MutateRows"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_pb2.MutateRowsRequest(
            table_name=table_name, entries=entries, app_profile_id=app_profile_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("table_name", table_name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["mutate_rows"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def check_and_mutate_row(
        self,
        table_name,
        row_key,
        app_profile_id=None,
        predicate_filter=None,
        true_mutations=None,
        false_mutations=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Mutates a row atomically based on the output of a predicate Reader filter.

        Example:
            >>> from google.cloud import bigtable_v2
            >>>
            >>> client = bigtable_v2.BigtableClient()
            >>>
            >>> table_name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> # TODO: Initialize `row_key`:
            >>> row_key = b''
            >>>
            >>> response = client.check_and_mutate_row(table_name, row_key)

        Args:
            table_name (str): The unique name of the table to which the conditional mutation should be
                applied. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            row_key (bytes): The key of the row to which the conditional mutation should be applied.
            app_profile_id (str): This value specifies routing for replication. If not specified, the
                "default" application profile will be used.
            predicate_filter (Union[dict, ~google.cloud.bigtable_v2.types.RowFilter]): The filter to be applied to the contents of the specified row. Depending
                on whether or not any results are yielded, either ``true_mutations`` or
                ``false_mutations`` will be executed. If unset, checks that the row
                contains any values at all.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_v2.types.RowFilter`
            true_mutations (list[Union[dict, ~google.cloud.bigtable_v2.types.Mutation]]): Changes to be atomically applied to the specified row if
                ``predicate_filter`` yields at least one cell when applied to
                ``row_key``. Entries are applied in order, meaning that earlier
                mutations can be masked by later ones. Must contain at least one entry
                if ``false_mutations`` is empty, and at most 100000.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_v2.types.Mutation`
            false_mutations (list[Union[dict, ~google.cloud.bigtable_v2.types.Mutation]]): Changes to be atomically applied to the specified row if
                ``predicate_filter`` does not yield any cells when applied to
                ``row_key``. Entries are applied in order, meaning that earlier
                mutations can be masked by later ones. Must contain at least one entry
                if ``true_mutations`` is empty, and at most 100000.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_v2.types.Mutation`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_v2.types.CheckAndMutateRowResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "check_and_mutate_row" not in self._inner_api_calls:
            self._inner_api_calls[
                "check_and_mutate_row"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.check_and_mutate_row,
                default_retry=self._method_configs["CheckAndMutateRow"].retry,
                default_timeout=self._method_configs["CheckAndMutateRow"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_pb2.CheckAndMutateRowRequest(
            table_name=table_name,
            row_key=row_key,
            app_profile_id=app_profile_id,
            predicate_filter=predicate_filter,
            true_mutations=true_mutations,
            false_mutations=false_mutations,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("table_name", table_name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["check_and_mutate_row"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def read_modify_write_row(
        self,
        table_name,
        row_key,
        rules,
        app_profile_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Modifies a row atomically on the server. The method reads the latest
        existing timestamp and value from the specified columns and writes a new
        entry based on pre-defined read/modify/write rules. The new value for the
        timestamp is the greater of the existing timestamp or the current server
        time. The method returns the new contents of all modified cells.

        Example:
            >>> from google.cloud import bigtable_v2
            >>>
            >>> client = bigtable_v2.BigtableClient()
            >>>
            >>> table_name = client.table_path('[PROJECT]', '[INSTANCE]', '[TABLE]')
            >>>
            >>> # TODO: Initialize `row_key`:
            >>> row_key = b''
            >>>
            >>> # TODO: Initialize `rules`:
            >>> rules = []
            >>>
            >>> response = client.read_modify_write_row(table_name, row_key, rules)

        Args:
            table_name (str): The unique name of the table to which the read/modify/write rules should
                be applied. Values are of the form
                ``projects/<project>/instances/<instance>/tables/<table>``.
            row_key (bytes): The key of the row to which the read/modify/write rules should be applied.
            rules (list[Union[dict, ~google.cloud.bigtable_v2.types.ReadModifyWriteRule]]): Rules specifying how the specified row's contents are to be transformed
                into writes. Entries are applied in order, meaning that earlier rules will
                affect the results of later ones.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigtable_v2.types.ReadModifyWriteRule`
            app_profile_id (str): This value specifies routing for replication. If not specified, the
                "default" application profile will be used.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigtable_v2.types.ReadModifyWriteRowResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "read_modify_write_row" not in self._inner_api_calls:
            self._inner_api_calls[
                "read_modify_write_row"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.read_modify_write_row,
                default_retry=self._method_configs["ReadModifyWriteRow"].retry,
                default_timeout=self._method_configs["ReadModifyWriteRow"].timeout,
                client_info=self._client_info,
            )

        request = bigtable_pb2.ReadModifyWriteRowRequest(
            table_name=table_name,
            row_key=row_key,
            rules=rules,
            app_profile_id=app_profile_id,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("table_name", table_name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["read_modify_write_row"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
