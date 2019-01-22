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
"""Accesses the google.cloud.bigquery.storage.v1beta1 BigQueryStorage API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.path_template
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import grpc

from google.cloud.bigquery_storage_v1beta1.gapic import big_query_storage_client_config
from google.cloud.bigquery_storage_v1beta1.gapic import enums
from google.cloud.bigquery_storage_v1beta1.gapic.transports import (
    big_query_storage_grpc_transport,
)
from google.cloud.bigquery_storage_v1beta1.proto import read_options_pb2
from google.cloud.bigquery_storage_v1beta1.proto import storage_pb2
from google.cloud.bigquery_storage_v1beta1.proto import storage_pb2_grpc
from google.cloud.bigquery_storage_v1beta1.proto import table_reference_pb2
from google.protobuf import empty_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-bigquery-storage"
).version


class BigQueryStorageClient(object):
    """
    BigQuery storage API.

    The BigQuery storage API can be used to read data stored in BigQuery.
    """

    SERVICE_ADDRESS = "bigquerystorage.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.bigquery.storage.v1beta1.BigQueryStorage"

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
            BigQueryStorageClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

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
            transport (Union[~.BigQueryStorageGrpcTransport,
                    Callable[[~.Credentials, type], ~.BigQueryStorageGrpcTransport]): A transport
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
            client_config = big_query_storage_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:  # pragma: no cover
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=big_query_storage_grpc_transport.BigQueryStorageGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = big_query_storage_grpc_transport.BigQueryStorageGrpcTransport(
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
    def create_read_session(
        self,
        table_reference,
        parent,
        table_modifiers=None,
        requested_streams=None,
        read_options=None,
        format_=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new read session. A read session divides the contents of a
        BigQuery table into one or more streams, which can then be used to read
        data from the table. The read session also specifies properties of the
        data to be read, such as a list of columns or a push-down filter describing
        the rows to be returned.

        A particular row can be read by at most one stream. When the caller has
        reached the end of each stream in the session, then all the data in the
        table has been read.

        Read sessions automatically expire 24 hours after they are created and do
        not require manual clean-up by the caller.

        Example:
            >>> from google.cloud import bigquery_storage_v1beta1
            >>>
            >>> client = bigquery_storage_v1beta1.BigQueryStorageClient()
            >>>
            >>> # TODO: Initialize `table_reference`:
            >>> table_reference = {}
            >>>
            >>> # TODO: Initialize `parent`:
            >>> parent = ''
            >>>
            >>> response = client.create_read_session(table_reference, parent)

        Args:
            table_reference (Union[dict, ~google.cloud.bigquery_storage_v1beta1.types.TableReference]): Required. Reference to the table to read.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_storage_v1beta1.types.TableReference`
            parent (str): Required. String of the form "projects/your-project-id" indicating the
                project this ReadSession is associated with. This is the project that will
                be billed for usage.
            table_modifiers (Union[dict, ~google.cloud.bigquery_storage_v1beta1.types.TableModifiers]): Optional. Any modifiers to the Table (e.g. snapshot timestamp).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_storage_v1beta1.types.TableModifiers`
            requested_streams (int): Optional. Initial number of streams. If unset or 0, we will
                provide a value of streams so as to produce reasonable throughput. Must be
                non-negative. The number of streams may be lower than the requested number,
                depending on the amount parallelism that is reasonable for the table and
                the maximum amount of parallelism allowed by the system.

                Streams must be read starting from offset 0.
            read_options (Union[dict, ~google.cloud.bigquery_storage_v1beta1.types.TableReadOptions]): Optional. Read options for this session (e.g. column selection, filters).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_storage_v1beta1.types.TableReadOptions`
            format_ (~google.cloud.bigquery_storage_v1beta1.types.DataFormat): Data output format. Currently default to Avro.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_storage_v1beta1.types.ReadSession` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_read_session" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_read_session"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_read_session,
                default_retry=self._method_configs["CreateReadSession"].retry,
                default_timeout=self._method_configs["CreateReadSession"].timeout,
                client_info=self._client_info,
            )

        request = storage_pb2.CreateReadSessionRequest(
            table_reference=table_reference,
            parent=parent,
            table_modifiers=table_modifiers,
            requested_streams=requested_streams,
            read_options=read_options,
            format=format_,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [
                ("table_reference.project_id", table_reference.project_id),
                ("table_reference.dataset_id", table_reference.dataset_id),
            ]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(  # pragma: no cover
                routing_header
            )
            metadata.append(routing_metadata)  # pragma: no cover

        return self._inner_api_calls["create_read_session"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def read_rows(
        self,
        read_position,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Reads rows from the table in the format prescribed by the read session.
        Each response contains one or more table rows, up to a maximum of 10 MiB
        per response; read requests which attempt to read individual rows larger
        than this will fail.

        Each request also returns a set of stream statistics reflecting the
        estimated total number of rows in the read stream. This number is computed
        based on the total table size and the number of active streams in the read
        session, and may change as other streams continue to read data.

        Example:
            >>> from google.cloud import bigquery_storage_v1beta1
            >>>
            >>> client = bigquery_storage_v1beta1.BigQueryStorageClient()
            >>>
            >>> # TODO: Initialize `read_position`:
            >>> read_position = {}
            >>>
            >>> for element in client.read_rows(read_position):
            ...     # process element
            ...     pass

        Args:
            read_position (Union[dict, ~google.cloud.bigquery_storage_v1beta1.types.StreamPosition]): Required. Identifier of the position in the stream to start reading from.
                The offset requested must be less than the last row read from ReadRows.
                Requesting a larger offset is undefined.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_storage_v1beta1.types.StreamPosition`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.bigquery_storage_v1beta1.types.ReadRowsResponse].

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

        request = storage_pb2.ReadRowsRequest(read_position=read_position)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("read_position.stream.name", read_position.stream.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(  # pragma: no cover
                routing_header
            )
            metadata.append(routing_metadata)  # pragma: no cover

        return self._inner_api_calls["read_rows"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def batch_create_read_session_streams(
        self,
        session,
        requested_streams,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates additional streams for a ReadSession. This API can be used to
        dynamically adjust the parallelism of a batch processing task upwards by
        adding additional workers.

        Example:
            >>> from google.cloud import bigquery_storage_v1beta1
            >>>
            >>> client = bigquery_storage_v1beta1.BigQueryStorageClient()
            >>>
            >>> # TODO: Initialize `session`:
            >>> session = {}
            >>>
            >>> # TODO: Initialize `requested_streams`:
            >>> requested_streams = 0
            >>>
            >>> response = client.batch_create_read_session_streams(session, requested_streams)

        Args:
            session (Union[dict, ~google.cloud.bigquery_storage_v1beta1.types.ReadSession]): Required. Must be a non-expired session obtained from a call to
                CreateReadSession. Only the name field needs to be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_storage_v1beta1.types.ReadSession`
            requested_streams (int): Required. Number of new streams requested. Must be positive.
                Number of added streams may be less than this, see CreateReadSessionRequest
                for more information.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_storage_v1beta1.types.BatchCreateReadSessionStreamsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_create_read_session_streams" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_create_read_session_streams"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_create_read_session_streams,
                default_retry=self._method_configs[
                    "BatchCreateReadSessionStreams"
                ].retry,
                default_timeout=self._method_configs[
                    "BatchCreateReadSessionStreams"
                ].timeout,
                client_info=self._client_info,
            )

        request = storage_pb2.BatchCreateReadSessionStreamsRequest(
            session=session, requested_streams=requested_streams
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("session.name", session.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(  # pragma: no cover
                routing_header
            )
            metadata.append(routing_metadata)  # pragma: no cover

        return self._inner_api_calls["batch_create_read_session_streams"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def finalize_stream(
        self,
        stream,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Triggers the graceful termination of a single stream in a ReadSession. This
        API can be used to dynamically adjust the parallelism of a batch processing
        task downwards without losing data.

        This API does not delete the stream -- it remains visible in the
        ReadSession, and any data processed by the stream is not released to other
        streams. However, no additional data will be assigned to the stream once
        this call completes. Callers must continue reading data on the stream until
        the end of the stream is reached so that data which has already been
        assigned to the stream will be processed.

        This method will return an error if there are no other live streams
        in the Session, or if SplitReadStream() has been called on the given
        Stream.

        Example:
            >>> from google.cloud import bigquery_storage_v1beta1
            >>>
            >>> client = bigquery_storage_v1beta1.BigQueryStorageClient()
            >>>
            >>> # TODO: Initialize `stream`:
            >>> stream = {}
            >>>
            >>> client.finalize_stream(stream)

        Args:
            stream (Union[dict, ~google.cloud.bigquery_storage_v1beta1.types.Stream]): Stream to finalize.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_storage_v1beta1.types.Stream`
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
        if "finalize_stream" not in self._inner_api_calls:
            self._inner_api_calls[
                "finalize_stream"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.finalize_stream,
                default_retry=self._method_configs["FinalizeStream"].retry,
                default_timeout=self._method_configs["FinalizeStream"].timeout,
                client_info=self._client_info,
            )

        request = storage_pb2.FinalizeStreamRequest(stream=stream)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("stream.name", stream.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(  # pragma: no cover
                routing_header
            )
            metadata.append(routing_metadata)  # pragma: no cover

        self._inner_api_calls["finalize_stream"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def split_read_stream(
        self,
        original_stream,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Splits a given read stream into two Streams. These streams are referred
        to as the primary and the residual of the split. The original stream can
        still be read from in the same manner as before. Both of the returned
        streams can also be read from, and the total rows return by both child
        streams will be the same as the rows read from the original stream.

        Moreover, the two child streams will be allocated back to back in the
        original Stream. Concretely, it is guaranteed that for streams Original,
        Primary, and Residual, that Original[0-j] = Primary[0-j] and
        Original[j-n] = Residual[0-m] once the streams have been read to
        completion.

        This method is guaranteed to be idempotent.

        Example:
            >>> from google.cloud import bigquery_storage_v1beta1
            >>>
            >>> client = bigquery_storage_v1beta1.BigQueryStorageClient()
            >>>
            >>> # TODO: Initialize `original_stream`:
            >>> original_stream = {}
            >>>
            >>> response = client.split_read_stream(original_stream)

        Args:
            original_stream (Union[dict, ~google.cloud.bigquery_storage_v1beta1.types.Stream]): Stream to split.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_storage_v1beta1.types.Stream`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_storage_v1beta1.types.SplitReadStreamResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "split_read_stream" not in self._inner_api_calls:
            self._inner_api_calls[
                "split_read_stream"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.split_read_stream,
                default_retry=self._method_configs["SplitReadStream"].retry,
                default_timeout=self._method_configs["SplitReadStream"].timeout,
                client_info=self._client_info,
            )

        request = storage_pb2.SplitReadStreamRequest(original_stream=original_stream)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("original_stream.name", original_stream.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(  # pragma: no cover
                routing_header
            )
            metadata.append(routing_metadata)  # pragma: no cover

        return self._inner_api_calls["split_read_stream"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
