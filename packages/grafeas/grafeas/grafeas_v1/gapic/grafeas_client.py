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

"""Accesses the grafeas.v1 Grafeas API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from grafeas.grafeas_v1.gapic import enums
from grafeas.grafeas_v1.gapic import grafeas_client_config
from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
from grafeas.grafeas_v1.proto import grafeas_pb2
from grafeas.grafeas_v1.proto import grafeas_pb2_grpc


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("grafeas").version


class GrafeasClient(object):
    """
    `Grafeas <https://grafeas.io>`__ API.

    Retrieves analysis results of Cloud components such as Docker container
    images.

    Analysis results are stored as a series of occurrences. An
    ``Occurrence`` contains information about a specific analysis instance
    on a resource. An occurrence refers to a ``Note``. A note contains
    details describing the analysis and is generally stored in a separate
    project, called a ``Provider``. Multiple occurrences can refer to the
    same note.

    For example, an SSL vulnerability could affect multiple images. In this
    case, there would be one note for the vulnerability and an occurrence
    for each image with the vulnerability referring to that note.
    """

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "grafeas.v1.Grafeas"

    @classmethod
    def note_path(cls, project, note):
        """Return a fully-qualified note string."""
        return google.api_core.path_template.expand(
            "projects/{project}/notes/{note}", project=project, note=note
        )

    @classmethod
    def occurrence_path(cls, project, occurrence):
        """Return a fully-qualified occurrence string."""
        return google.api_core.path_template.expand(
            "projects/{project}/occurrences/{occurrence}",
            project=project,
            occurrence=occurrence,
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    def __init__(self, transport, client_config=None, client_info=None):
        """Constructor.

        Args:
            transport (~.GrafeasGrpcTransport): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.

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
            client_config = grafeas_client_config.config

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        self.transport = transport

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
    def get_occurrence(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the specified occurrence.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> name = client.occurrence_path('[PROJECT]', '[OCCURRENCE]')
            >>>
            >>> response = client.get_occurrence(name)

        Args:
            name (str): The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~grafeas.grafeas_v1.types.Occurrence` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_occurrence" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_occurrence"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_occurrence,
                default_retry=self._method_configs["GetOccurrence"].retry,
                default_timeout=self._method_configs["GetOccurrence"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.GetOccurrenceRequest(name=name)
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

        return self._inner_api_calls["get_occurrence"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_occurrences(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists occurrences for the specified project.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_occurrences(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_occurrences(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The name of the project to list occurrences for in the form of
                ``projects/[PROJECT_ID]``.
            filter_ (str): The filter expression.
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~grafeas.grafeas_v1.types.Occurrence` instances.
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
        if "list_occurrences" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_occurrences"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_occurrences,
                default_retry=self._method_configs["ListOccurrences"].retry,
                default_timeout=self._method_configs["ListOccurrences"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.ListOccurrencesRequest(
            parent=parent, filter=filter_, page_size=page_size
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
                self._inner_api_calls["list_occurrences"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="occurrences",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_occurrence(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the specified occurrence. For example, use this method to delete an
        occurrence when the occurrence is no longer applicable for the given
        resource.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> name = client.occurrence_path('[PROJECT]', '[OCCURRENCE]')
            >>>
            >>> client.delete_occurrence(name)

        Args:
            name (str): The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
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
        if "delete_occurrence" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_occurrence"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_occurrence,
                default_retry=self._method_configs["DeleteOccurrence"].retry,
                default_timeout=self._method_configs["DeleteOccurrence"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.DeleteOccurrenceRequest(name=name)
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

        self._inner_api_calls["delete_occurrence"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_occurrence(
        self,
        parent,
        occurrence,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new occurrence.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `occurrence`:
            >>> occurrence = {}
            >>>
            >>> response = client.create_occurrence(parent, occurrence)

        Args:
            parent (str): The name of the project in the form of ``projects/[PROJECT_ID]``, under
                which the occurrence is to be created.
            occurrence (Union[dict, ~grafeas.grafeas_v1.types.Occurrence]): The occurrence to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~grafeas.grafeas_v1.types.Occurrence`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~grafeas.grafeas_v1.types.Occurrence` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_occurrence" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_occurrence"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_occurrence,
                default_retry=self._method_configs["CreateOccurrence"].retry,
                default_timeout=self._method_configs["CreateOccurrence"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.CreateOccurrenceRequest(
            parent=parent, occurrence=occurrence
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

        return self._inner_api_calls["create_occurrence"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def batch_create_occurrences(
        self,
        parent,
        occurrences,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates new occurrences in batch.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `occurrences`:
            >>> occurrences = []
            >>>
            >>> response = client.batch_create_occurrences(parent, occurrences)

        Args:
            parent (str): The name of the project in the form of ``projects/[PROJECT_ID]``, under
                which the occurrences are to be created.
            occurrences (list[Union[dict, ~grafeas.grafeas_v1.types.Occurrence]]): The occurrences to create. Max allowed length is 1000.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~grafeas.grafeas_v1.types.Occurrence`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~grafeas.grafeas_v1.types.BatchCreateOccurrencesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_create_occurrences" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_create_occurrences"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_create_occurrences,
                default_retry=self._method_configs["BatchCreateOccurrences"].retry,
                default_timeout=self._method_configs["BatchCreateOccurrences"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.BatchCreateOccurrencesRequest(
            parent=parent, occurrences=occurrences
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

        return self._inner_api_calls["batch_create_occurrences"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_occurrence(
        self,
        name,
        occurrence,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates the specified occurrence.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> name = client.occurrence_path('[PROJECT]', '[OCCURRENCE]')
            >>>
            >>> # TODO: Initialize `occurrence`:
            >>> occurrence = {}
            >>>
            >>> response = client.update_occurrence(name, occurrence)

        Args:
            name (str): The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
            occurrence (Union[dict, ~grafeas.grafeas_v1.types.Occurrence]): The updated occurrence.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~grafeas.grafeas_v1.types.Occurrence`
            update_mask (Union[dict, ~grafeas.grafeas_v1.types.FieldMask]): The fields to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~grafeas.grafeas_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~grafeas.grafeas_v1.types.Occurrence` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_occurrence" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_occurrence"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_occurrence,
                default_retry=self._method_configs["UpdateOccurrence"].retry,
                default_timeout=self._method_configs["UpdateOccurrence"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.UpdateOccurrenceRequest(
            name=name, occurrence=occurrence, update_mask=update_mask
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

        return self._inner_api_calls["update_occurrence"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_occurrence_note(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the note attached to the specified occurrence. Consumer projects can
        use this method to get a note that belongs to a provider project.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> name = client.occurrence_path('[PROJECT]', '[OCCURRENCE]')
            >>>
            >>> response = client.get_occurrence_note(name)

        Args:
            name (str): The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~grafeas.grafeas_v1.types.Note` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_occurrence_note" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_occurrence_note"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_occurrence_note,
                default_retry=self._method_configs["GetOccurrenceNote"].retry,
                default_timeout=self._method_configs["GetOccurrenceNote"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.GetOccurrenceNoteRequest(name=name)
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

        return self._inner_api_calls["get_occurrence_note"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_note(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the specified note.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> name = client.note_path('[PROJECT]', '[NOTE]')
            >>>
            >>> response = client.get_note(name)

        Args:
            name (str): The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~grafeas.grafeas_v1.types.Note` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_note" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_note"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_note,
                default_retry=self._method_configs["GetNote"].retry,
                default_timeout=self._method_configs["GetNote"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.GetNoteRequest(name=name)
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

        return self._inner_api_calls["get_note"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_notes(
        self,
        parent,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists notes for the specified project.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_notes(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_notes(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The name of the project to list notes for in the form of
                ``projects/[PROJECT_ID]``.
            filter_ (str): The filter expression.
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~grafeas.grafeas_v1.types.Note` instances.
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
        if "list_notes" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_notes"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_notes,
                default_retry=self._method_configs["ListNotes"].retry,
                default_timeout=self._method_configs["ListNotes"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.ListNotesRequest(
            parent=parent, filter=filter_, page_size=page_size
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
                self._inner_api_calls["list_notes"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="notes",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_note(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the specified note.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> name = client.note_path('[PROJECT]', '[NOTE]')
            >>>
            >>> client.delete_note(name)

        Args:
            name (str): The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
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
        if "delete_note" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_note"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_note,
                default_retry=self._method_configs["DeleteNote"].retry,
                default_timeout=self._method_configs["DeleteNote"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.DeleteNoteRequest(name=name)
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

        self._inner_api_calls["delete_note"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_note(
        self,
        parent,
        note_id,
        note,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new note.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `note_id`:
            >>> note_id = ''
            >>>
            >>> # TODO: Initialize `note`:
            >>> note = {}
            >>>
            >>> response = client.create_note(parent, note_id, note)

        Args:
            parent (str): The name of the project in the form of ``projects/[PROJECT_ID]``, under
                which the note is to be created.
            note_id (str): The ID to use for this note.
            note (Union[dict, ~grafeas.grafeas_v1.types.Note]): The note to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~grafeas.grafeas_v1.types.Note`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~grafeas.grafeas_v1.types.Note` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_note" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_note"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_note,
                default_retry=self._method_configs["CreateNote"].retry,
                default_timeout=self._method_configs["CreateNote"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.CreateNoteRequest(
            parent=parent, note_id=note_id, note=note
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

        return self._inner_api_calls["create_note"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def batch_create_notes(
        self,
        parent,
        notes,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates new notes in batch.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `notes`:
            >>> notes = {}
            >>>
            >>> response = client.batch_create_notes(parent, notes)

        Args:
            parent (str): The name of the project in the form of ``projects/[PROJECT_ID]``, under
                which the notes are to be created.
            notes (dict[str -> Union[dict, ~grafeas.grafeas_v1.types.Note]]): The notes to create. Max allowed length is 1000.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~grafeas.grafeas_v1.types.Note`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~grafeas.grafeas_v1.types.BatchCreateNotesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_create_notes" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_create_notes"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_create_notes,
                default_retry=self._method_configs["BatchCreateNotes"].retry,
                default_timeout=self._method_configs["BatchCreateNotes"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.BatchCreateNotesRequest(parent=parent, notes=notes)
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

        return self._inner_api_calls["batch_create_notes"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_note(
        self,
        name,
        note,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates the specified note.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> name = client.note_path('[PROJECT]', '[NOTE]')
            >>>
            >>> # TODO: Initialize `note`:
            >>> note = {}
            >>>
            >>> response = client.update_note(name, note)

        Args:
            name (str): The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
            note (Union[dict, ~grafeas.grafeas_v1.types.Note]): The updated note.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~grafeas.grafeas_v1.types.Note`
            update_mask (Union[dict, ~grafeas.grafeas_v1.types.FieldMask]): The fields to update.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~grafeas.grafeas_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~grafeas.grafeas_v1.types.Note` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_note" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_note"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_note,
                default_retry=self._method_configs["UpdateNote"].retry,
                default_timeout=self._method_configs["UpdateNote"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.UpdateNoteRequest(
            name=name, note=note, update_mask=update_mask
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

        return self._inner_api_calls["update_note"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_note_occurrences(
        self,
        name,
        filter_=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists occurrences referencing the specified note. Provider projects can use
        this method to get all occurrences across consumer projects referencing the
        specified note.

        Example:
            >>> from grafeas import grafeas_v1
            >>> from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport
            >>> 
            >>> address = "[SERVICE_ADDRESS]"
            >>> scopes = ("[SCOPE]")
            >>> transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)
            >>> client = grafeas_v1.GrafeasClient(transport)
            >>>
            >>> name = client.note_path('[PROJECT]', '[NOTE]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_note_occurrences(name):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_note_occurrences(name).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            name (str): The name of the note to list occurrences for in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
            filter_ (str): The filter expression.
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
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~grafeas.grafeas_v1.types.Occurrence` instances.
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
        if "list_note_occurrences" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_note_occurrences"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_note_occurrences,
                default_retry=self._method_configs["ListNoteOccurrences"].retry,
                default_timeout=self._method_configs["ListNoteOccurrences"].timeout,
                client_info=self._client_info,
            )

        request = grafeas_pb2.ListNoteOccurrencesRequest(
            name=name, filter=filter_, page_size=page_size
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

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_note_occurrences"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="occurrences",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator
