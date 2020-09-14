# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

"""Accesses the google.cloud.bigquery.storage.v1 BigQueryRead API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.path_template
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.bigquery_storage_v1.gapic import big_query_read_client_config
from google.cloud.bigquery_storage_v1.gapic import enums
from google.cloud.bigquery_storage_v1.gapic.transports import (
    big_query_read_grpc_transport,
)
from google.cloud.bigquery_storage_v1.proto import storage_pb2
from google.cloud.bigquery_storage_v1.proto import storage_pb2_grpc
from google.cloud.bigquery_storage_v1.proto import stream_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    "google-cloud-bigquery-storage",
).version


class BigQueryReadClient(object):
    """
    BigQuery Read API.

    The Read API can be used to read data from BigQuery.
    """

    SERVICE_ADDRESS = "bigquerystorage.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.bigquery.storage.v1.BigQueryRead"

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
            BigQueryReadClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project,
        )

    @classmethod
    def read_session_path(cls, project, location, session):
        """Return a fully-qualified read_session string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/sessions/{session}",
            project=project,
            location=location,
            session=session,
        )

    @classmethod
    def read_stream_path(cls, project, location, session, stream):
        """Return a fully-qualified read_stream string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/sessions/{session}/streams/{stream}",
            project=project,
            location=location,
            session=session,
            stream=stream,
        )

    @classmethod
    def table_path(cls, project, dataset, table):
        """Return a fully-qualified table string."""
        return google.api_core.path_template.expand(
            "projects/{project}/datasets/{dataset}/tables/{table}",
            project=project,
            dataset=dataset,
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
            transport (Union[~.BigQueryReadGrpcTransport,
                    Callable[[~.Credentials, type], ~.BigQueryReadGrpcTransport]): A transport
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
            client_config = big_query_read_client_config.config

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
        if transport:  # pragma: no cover
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=big_query_read_grpc_transport.BigQueryReadGrpcTransport,
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
            self.transport = big_query_read_grpc_transport.BigQueryReadGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials,
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION,
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME],
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def create_read_session(
        self,
        parent,
        read_session,
        max_stream_count=None,
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

        Data is assigned to each stream such that roughly the same number of
        rows can be read from each stream. Because the server-side unit for
        assigning data is collections of rows, the API does not guarantee that
        each stream will return the same number or rows. Additionally, the
        limits are enforced based on the number of pre-filtered rows, so some
        filters can lead to lopsided assignments.

        Read sessions automatically expire 24 hours after they are created and do
        not require manual clean-up by the caller.

        Example:
            >>> from google.cloud import bigquery_storage_v1
            >>>
            >>> client = bigquery_storage_v1.BigQueryReadClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `read_session`:
            >>> read_session = {}
            >>>
            >>> response = client.create_read_session(parent, read_session)

        Args:
            parent (str): The resource has one pattern, but the API owner expects to add more
                later. (This is the inverse of ORIGINALLY_SINGLE_PATTERN, and prevents
                that from being necessary once there are multiple patterns.)
            read_session (Union[dict, ~google.cloud.bigquery_storage_v1.types.ReadSession]): Required. Session to be created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.bigquery_storage_v1.types.ReadSession`
            max_stream_count (int): Max initial number of streams. If unset or zero, the server will
                provide a value of streams so as to produce reasonable throughput. Must be
                non-negative. The number of streams may be lower than the requested number,
                depending on the amount parallelism that is reasonable for the table. Error
                will be returned if the max count is greater than the current system
                max limit of 1,000.

                Streams must be read starting from offset 0.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_storage_v1.types.ReadSession` instance.

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
            parent=parent, read_session=read_session, max_stream_count=max_stream_count,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("read_session.table", read_session.table)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)  # pragma: no cover

        return self._inner_api_calls["create_read_session"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def read_rows(
        self,
        read_stream,
        offset=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Reads rows from the stream in the format prescribed by the ReadSession.
        Each response contains one or more table rows, up to a maximum of 100 MiB
        per response; read requests which attempt to read individual rows larger
        than 100 MiB will fail.

        Each request also returns a set of stream statistics reflecting the current
        state of the stream.

        Example:
            >>> from google.cloud import bigquery_storage_v1
            >>>
            >>> client = bigquery_storage_v1.BigQueryReadClient()
            >>>
            >>> read_stream = client.read_stream_path('[PROJECT]', '[LOCATION]', '[SESSION]', '[STREAM]')
            >>>
            >>> for element in client.read_rows(read_stream):
            ...     # process element
            ...     pass

        Args:
            read_stream (str): Required. Stream to read rows from.
            offset (long): The offset requested must be less than the last row read from Read.
                Requesting a larger offset is undefined. If not specified, start reading
                from offset zero.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.cloud.bigquery_storage_v1.types.ReadRowsResponse].

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

        request = storage_pb2.ReadRowsRequest(read_stream=read_stream, offset=offset,)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("read_stream", read_stream)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)  # pragma: no cover

        return self._inner_api_calls["read_rows"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def split_read_stream(
        self,
        name,
        fraction=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        An indicator of the behavior of a given field (for example, that a
        field is required in requests, or given as output but ignored as input).
        This **does not** change the behavior in protocol buffers itself; it
        only denotes the behavior and may affect how API tooling handles the
        field.

        Note: This enum **may** receive new values in the future.

        Example:
            >>> from google.cloud import bigquery_storage_v1
            >>>
            >>> client = bigquery_storage_v1.BigQueryReadClient()
            >>>
            >>> name = client.read_stream_path('[PROJECT]', '[LOCATION]', '[SESSION]', '[STREAM]')
            >>>
            >>> response = client.split_read_stream(name)

        Args:
            name (str): Required. Name of the stream to split.
            fraction (float): A value in the range (0.0, 1.0) that specifies the fractional point at
                which the original stream should be split. The actual split point is
                evaluated on pre-filtered rows, so if a filter is provided, then there is
                no guarantee that the division of the rows between the new child streams
                will be proportional to this fractional value. Additionally, because the
                server-side unit for assigning data is collections of rows, this fraction
                will always map to a data storage boundary on the server side.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse` instance.

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

        request = storage_pb2.SplitReadStreamRequest(name=name, fraction=fraction,)
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
            metadata.append(routing_metadata)  # pragma: no cover

        return self._inner_api_calls["split_read_stream"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
