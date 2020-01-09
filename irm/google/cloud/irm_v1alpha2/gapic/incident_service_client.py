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

"""Accesses the google.cloud.irm.v1alpha2 IncidentService API."""

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
import google.api_core.page_iterator
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.cloud.irm_v1alpha2.gapic import enums
from google.cloud.irm_v1alpha2.gapic import incident_service_client_config
from google.cloud.irm_v1alpha2.gapic.transports import incident_service_grpc_transport
from google.cloud.irm_v1alpha2.proto import incidents_pb2
from google.cloud.irm_v1alpha2.proto import incidents_service_pb2
from google.cloud.irm_v1alpha2.proto import incidents_service_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-irm").version


class IncidentServiceClient(object):
    """The Incident API for Incident Response & Management."""

    SERVICE_ADDRESS = "irm.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.irm.v1alpha2.IncidentService"

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
            IncidentServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def annotation_path(cls, project, incident, annotation):
        """Return a fully-qualified annotation string."""
        return google.api_core.path_template.expand(
            "projects/{project}/incidents/{incident}/annotations/{annotation}",
            project=project,
            incident=incident,
            annotation=annotation,
        )

    @classmethod
    def artifact_path(cls, project, incident, artifact):
        """Return a fully-qualified artifact string."""
        return google.api_core.path_template.expand(
            "projects/{project}/incidents/{incident}/artifacts/{artifact}",
            project=project,
            incident=incident,
            artifact=artifact,
        )

    @classmethod
    def incident_path(cls, project, incident):
        """Return a fully-qualified incident string."""
        return google.api_core.path_template.expand(
            "projects/{project}/incidents/{incident}",
            project=project,
            incident=incident,
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def role_assignment_path(cls, project, incident, role_assignment):
        """Return a fully-qualified role_assignment string."""
        return google.api_core.path_template.expand(
            "projects/{project}/incidents/{incident}/roleAssignments/{role_assignment}",
            project=project,
            incident=incident,
            role_assignment=role_assignment,
        )

    @classmethod
    def signal_path(cls, project, signal):
        """Return a fully-qualified signal string."""
        return google.api_core.path_template.expand(
            "projects/{project}/signals/{signal}", project=project, signal=signal
        )

    @classmethod
    def subscription_path(cls, project, incident, subscription):
        """Return a fully-qualified subscription string."""
        return google.api_core.path_template.expand(
            "projects/{project}/incidents/{incident}/subscriptions/{subscription}",
            project=project,
            incident=incident,
            subscription=subscription,
        )

    @classmethod
    def tag_path(cls, project, incident, tag):
        """Return a fully-qualified tag string."""
        return google.api_core.path_template.expand(
            "projects/{project}/incidents/{incident}/tags/{tag}",
            project=project,
            incident=incident,
            tag=tag,
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
            transport (Union[~.IncidentServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.IncidentServiceGrpcTransport]): A transport
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
            client_config = incident_service_client_config.config

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
                    default_class=incident_service_grpc_transport.IncidentServiceGrpcTransport,
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
            self.transport = incident_service_grpc_transport.IncidentServiceGrpcTransport(
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
    def create_incident(
        self,
        incident,
        parent,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new incident.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> # TODO: Initialize `incident`:
            >>> incident = {}
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> response = client.create_incident(incident, parent)

        Args:
            incident (Union[dict, ~google.cloud.irm_v1alpha2.types.Incident]): The incident to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Incident`
            parent (str): The resource name of the hosting Stackdriver project which the incident
                belongs to. The name is of the form ``projects/{project_id_or_number}``
                .
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Incident` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_incident" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_incident"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_incident,
                default_retry=self._method_configs["CreateIncident"].retry,
                default_timeout=self._method_configs["CreateIncident"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.CreateIncidentRequest(
            incident=incident, parent=parent
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

        return self._inner_api_calls["create_incident"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_incident(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns an incident by name.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> response = client.get_incident(name)

        Args:
            name (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Incident` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_incident" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_incident"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_incident,
                default_retry=self._method_configs["GetIncident"].retry,
                default_timeout=self._method_configs["GetIncident"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.GetIncidentRequest(name=name)
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

        return self._inner_api_calls["get_incident"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def search_incidents(
        self,
        parent,
        query=None,
        page_size=None,
        time_zone=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns a list of incidents.
        Incidents are ordered by start time, with the most recent incidents first.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_incidents(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_incidents(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The resource name of the hosting Stackdriver project which requested
                incidents belong to.
            query (str): An expression that defines which incidents to return.

                Search atoms can be used to match certain specific fields. Otherwise,
                plain text will match text fields in the incident.

                Search atoms:

                -  ``start`` - (timestamp) The time the incident started.
                -  ``stage`` - The stage of the incident, one of detected, triaged,
                   mitigated, resolved, documented, or duplicate (which correspond to
                   values in the Incident.Stage enum). These are ordered, so
                   ``stage<resolved`` is equivalent to
                   ``stage:detected OR stage:triaged OR stage:mitigated``.
                -  ``severity`` - (Incident.Severity) The severity of the incident.

                   -  Supports matching on a specific severity (for example,
                      ``severity:major``) or on a range (for example,
                      ``severity>medium``, ``severity<=minor``, etc.).

                Timestamp formats:

                -  yyyy-MM-dd - an absolute date, treated as a calendar-day-wide window.
                   In other words, the "<" operator will match dates before that date,
                   the ">" operator will match dates after that date, and the ":" or "="
                   operators will match the entire day.
                -  Nd (for example, 7d) - a relative number of days ago, treated as a
                   moment in time (as opposed to a day-wide span). A multiple of 24
                   hours ago (as opposed to calendar days). In the case of daylight
                   savings time, it will apply the current timezone to both ends of the
                   range. Note that exact matching (for example, ``start:7d``) is
                   unlikely to be useful because that would only match incidents created
                   precisely at a particular instant in time.

                Examples:

                -  ``foo`` - matches incidents containing the word "foo"
                -  ``"foo bar"`` - matches incidents containing the phrase "foo bar"
                -  ``foo bar`` or ``foo AND bar`` - matches incidents containing the
                   words "foo" and "bar"
                -  ``foo -bar`` or ``foo AND NOT bar`` - matches incidents containing
                   the word "foo" but not the word "bar"
                -  ``foo OR bar`` - matches incidents containing the word "foo" or the
                   word "bar"
                -  ``start>2018-11-28`` - matches incidents which started after November
                   11,

                   2018.

                -  ``start<=2018-11-28`` - matches incidents which started on or before
                   November 11, 2018.
                -  ``start:2018-11-28`` - matches incidents which started on November
                   11,

                   2018.

                -  ``start>7d`` - matches incidents which started after the point in
                   time 7*24 hours ago
                -  ``start>180d`` - similar to 7d, but likely to cross the daylight
                   savings time boundary, so the end time will be 1 hour different from
                   "now."
                -  ``foo AND start>90d AND stage<resolved`` - unresolved incidents from
                   the past 90 days containing the word "foo"
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            time_zone (str): The time zone name. It should be an IANA TZ name, such as
                "America/Los_Angeles". For more information, see
                https://en.wikipedia.org/wiki/List_of_tz_database_time_zones. If no
                time zone is specified, the default is UTC.
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
            An iterable of :class:`~google.cloud.irm_v1alpha2.types.Incident` instances.
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
        if "search_incidents" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_incidents"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_incidents,
                default_retry=self._method_configs["SearchIncidents"].retry,
                default_timeout=self._method_configs["SearchIncidents"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.SearchIncidentsRequest(
            parent=parent, query=query, page_size=page_size, time_zone=time_zone
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
                self._inner_api_calls["search_incidents"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="incidents",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_incident(
        self,
        incident,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing incident.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> # TODO: Initialize `incident`:
            >>> incident = {}
            >>>
            >>> response = client.update_incident(incident)

        Args:
            incident (Union[dict, ~google.cloud.irm_v1alpha2.types.Incident]): The incident to update with the new values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Incident`
            update_mask (Union[dict, ~google.cloud.irm_v1alpha2.types.FieldMask]): List of fields that should be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Incident` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_incident" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_incident"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_incident,
                default_retry=self._method_configs["UpdateIncident"].retry,
                default_timeout=self._method_configs["UpdateIncident"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.UpdateIncidentRequest(
            incident=incident, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("incident.name", incident.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_incident"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def search_similar_incidents(
        self,
        name,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns a list of incidents that are "similar" to the specified incident
        or signal. This functionality is provided on a best-effort basis and the
        definition of "similar" is subject to change.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_similar_incidents(name):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_similar_incidents(name).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            name (str): Resource name of the incident or signal, for example,
                "projects/{project_id}/incidents/{incident_id}".
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
            An iterable of :class:`~google.cloud.irm_v1alpha2.types.Result` instances.
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
        if "search_similar_incidents" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_similar_incidents"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_similar_incidents,
                default_retry=self._method_configs["SearchSimilarIncidents"].retry,
                default_timeout=self._method_configs["SearchSimilarIncidents"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.SearchSimilarIncidentsRequest(
            name=name, page_size=page_size
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
                self._inner_api_calls["search_similar_incidents"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="results",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_annotation(
        self,
        parent,
        annotation,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates an annotation on an existing incident. Only 'text/plain' and
        'text/markdown' annotations can be created via this method.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # TODO: Initialize `annotation`:
            >>> annotation = {}
            >>>
            >>> response = client.create_annotation(parent, annotation)

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
            annotation (Union[dict, ~google.cloud.irm_v1alpha2.types.Annotation]): Only annotation.content is an input argument.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Annotation`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Annotation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_annotation" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_annotation"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_annotation,
                default_retry=self._method_configs["CreateAnnotation"].retry,
                default_timeout=self._method_configs["CreateAnnotation"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.CreateAnnotationRequest(
            parent=parent, annotation=annotation
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

        return self._inner_api_calls["create_annotation"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_annotations(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists annotations that are part of an incident. No assumptions should be
        made on the content-type of the annotation returned.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_annotations(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_annotations(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
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
            An iterable of :class:`~google.cloud.irm_v1alpha2.types.Annotation` instances.
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
        if "list_annotations" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_annotations"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_annotations,
                default_retry=self._method_configs["ListAnnotations"].retry,
                default_timeout=self._method_configs["ListAnnotations"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.ListAnnotationsRequest(
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
                self._inner_api_calls["list_annotations"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="annotations",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_tag(
        self,
        parent,
        tag,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a tag on an existing incident.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # TODO: Initialize `tag`:
            >>> tag = {}
            >>>
            >>> response = client.create_tag(parent, tag)

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
            tag (Union[dict, ~google.cloud.irm_v1alpha2.types.Tag]): Tag to create. Only tag.display_name is an input argument.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Tag`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Tag` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_tag" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_tag"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_tag,
                default_retry=self._method_configs["CreateTag"].retry,
                default_timeout=self._method_configs["CreateTag"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.CreateTagRequest(parent=parent, tag=tag)
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

        return self._inner_api_calls["create_tag"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_tag(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an existing tag.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.tag_path('[PROJECT]', '[INCIDENT]', '[TAG]')
            >>>
            >>> client.delete_tag(name)

        Args:
            name (str): Resource name of the tag.
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
        if "delete_tag" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_tag"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_tag,
                default_retry=self._method_configs["DeleteTag"].retry,
                default_timeout=self._method_configs["DeleteTag"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.DeleteTagRequest(name=name)
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

        self._inner_api_calls["delete_tag"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_tags(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists tags that are part of an incident.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_tags(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_tags(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
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
            An iterable of :class:`~google.cloud.irm_v1alpha2.types.Tag` instances.
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
        if "list_tags" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_tags"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_tags,
                default_retry=self._method_configs["ListTags"].retry,
                default_timeout=self._method_configs["ListTags"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.ListTagsRequest(
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
                self._inner_api_calls["list_tags"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="tags",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_signal(
        self,
        parent,
        signal,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new signal.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `signal`:
            >>> signal = {}
            >>>
            >>> response = client.create_signal(parent, signal)

        Args:
            parent (str): The resource name of the hosting Stackdriver project which requested
                signal belongs to.
            signal (Union[dict, ~google.cloud.irm_v1alpha2.types.Signal]): The signal to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Signal`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Signal` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_signal" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_signal"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_signal,
                default_retry=self._method_configs["CreateSignal"].retry,
                default_timeout=self._method_configs["CreateSignal"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.CreateSignalRequest(
            parent=parent, signal=signal
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

        return self._inner_api_calls["create_signal"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def search_signals(
        self,
        parent,
        query=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists signals that are part of an incident.
        Signals are returned in reverse chronological order.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.search_signals(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.search_signals(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The resource name of the hosting Stackdriver project which requested
                incidents belong to.
            query (str): An expression that defines which signals to return.

                Search atoms can be used to match certain specific fields. Otherwise,
                plain text will match text fields in the signal.

                Search atoms:

                -  ``start`` - (timestamp) The time the signal was created.
                -  ``title`` - The title of the signal.
                -  ``signal_state`` - ``open`` or ``closed``. State of the signal.
                   (e.g., ``signal_state:open``)

                Timestamp formats:

                -  yyyy-MM-dd - an absolute date, treated as a calendar-day-wide window.
                   In other words, the "<" operator will match dates before that date,
                   the ">" operator will match dates after that date, and the ":"
                   operator will match the entire day.
                -  yyyy-MM-ddTHH:mm - Same as above, but with minute resolution.
                -  yyyy-MM-ddTHH:mm:ss - Same as above, but with second resolution.
                -  Nd (e.g. 7d) - a relative number of days ago, treated as a moment in
                   time (as opposed to a day-wide span) a multiple of 24 hours ago (as
                   opposed to calendar days). In the case of daylight savings time, it
                   will apply the current timezone to both ends of the range. Note that
                   exact matching (e.g. ``start:7d``) is unlikely to be useful because
                   that would only match signals created precisely at a particular
                   instant in time.

                The absolute timestamp formats (everything starting with a year) can
                optionally be followed with a UTC offset in +/-hh:mm format. Also, the
                'T' separating dates and times can optionally be replaced with a space.
                Note that any timestamp containing a space or colon will need to be
                quoted.

                Examples:

                -  ``foo`` - matches signals containing the word "foo"
                -  ``"foo bar"`` - matches signals containing the phrase "foo bar"
                -  ``foo bar`` or ``foo AND bar`` - matches signals containing the words
                   "foo" and "bar"
                -  ``foo -bar`` or ``foo AND NOT bar`` - matches signals containing the
                   word "foo" but not the word "bar"
                -  ``foo OR bar`` - matches signals containing the word "foo" or the
                   word "bar"
                -  ``start>2018-11-28`` - matches signals which started after November
                   11, 2018.
                -  ``start<=2018-11-28`` - matches signals which started on or before
                   November 11, 2018.
                -  ``start:2018-11-28`` - matches signals which started on November 11,

                   2018.

                -  ``start>"2018-11-28 01:02:03+04:00"`` - matches signals which started
                   after November 11, 2018 at 1:02:03 AM according to the UTC+04 time
                   zone.
                -  ``start>7d`` - matches signals which started after the point in time
                   7*24 hours ago
                -  ``start>180d`` - similar to 7d, but likely to cross the daylight
                   savings time boundary, so the end time will be 1 hour different from
                   "now."
                -  ``foo AND start>90d AND stage<resolved`` - unresolved signals from
                   the past 90 days containing the word "foo"
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
            An iterable of :class:`~google.cloud.irm_v1alpha2.types.Signal` instances.
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
        if "search_signals" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_signals"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_signals,
                default_retry=self._method_configs["SearchSignals"].retry,
                default_timeout=self._method_configs["SearchSignals"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.SearchSignalsRequest(
            parent=parent, query=query, page_size=page_size
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
                self._inner_api_calls["search_signals"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="signals",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def get_signal(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns a signal by name.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.signal_path('[PROJECT]', '[SIGNAL]')
            >>>
            >>> response = client.get_signal(name)

        Args:
            name (str): Resource name of the Signal resource, for example,
                "projects/{project_id}/signals/{signal_id}".
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Signal` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_signal" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_signal"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_signal,
                default_retry=self._method_configs["GetSignal"].retry,
                default_timeout=self._method_configs["GetSignal"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.GetSignalRequest(name=name)
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

        return self._inner_api_calls["get_signal"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def lookup_signal(
        self,
        cscc_finding=None,
        stackdriver_notification_id=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Finds a signal by other unique IDs.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> response = client.lookup_signal()

        Args:
            cscc_finding (str): Full resource name of the CSCC finding id this signal refers to (e.g.
                "organizations/abc/sources/123/findings/xyz")
            stackdriver_notification_id (str): The ID from the Stackdriver Alerting notification.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Signal` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "lookup_signal" not in self._inner_api_calls:
            self._inner_api_calls[
                "lookup_signal"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.lookup_signal,
                default_retry=self._method_configs["LookupSignal"].retry,
                default_timeout=self._method_configs["LookupSignal"].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            cscc_finding=cscc_finding,
            stackdriver_notification_id=stackdriver_notification_id,
        )

        request = incidents_service_pb2.LookupSignalRequest(
            cscc_finding=cscc_finding,
            stackdriver_notification_id=stackdriver_notification_id,
        )
        return self._inner_api_calls["lookup_signal"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_signal(
        self,
        signal,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing signal (for example, to assign/unassign it to an
        incident).

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> # TODO: Initialize `signal`:
            >>> signal = {}
            >>>
            >>> response = client.update_signal(signal)

        Args:
            signal (Union[dict, ~google.cloud.irm_v1alpha2.types.Signal]): The signal to update with the new values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Signal`
            update_mask (Union[dict, ~google.cloud.irm_v1alpha2.types.FieldMask]): List of fields that should be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Signal` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_signal" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_signal"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_signal,
                default_retry=self._method_configs["UpdateSignal"].retry,
                default_timeout=self._method_configs["UpdateSignal"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.UpdateSignalRequest(
            signal=signal, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("signal.name", signal.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_signal"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def escalate_incident(
        self,
        incident,
        update_mask=None,
        subscriptions=None,
        tags=None,
        roles=None,
        artifacts=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Escalates an incident.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> # TODO: Initialize `incident`:
            >>> incident = {}
            >>>
            >>> response = client.escalate_incident(incident)

        Args:
            incident (Union[dict, ~google.cloud.irm_v1alpha2.types.Incident]): The incident to escalate with the new values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Incident`
            update_mask (Union[dict, ~google.cloud.irm_v1alpha2.types.FieldMask]): List of fields that should be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.FieldMask`
            subscriptions (list[Union[dict, ~google.cloud.irm_v1alpha2.types.Subscription]]): Subscriptions to add or update. Existing subscriptions with the same
                channel and address as a subscription in the list will be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Subscription`
            tags (list[Union[dict, ~google.cloud.irm_v1alpha2.types.Tag]]): Tags to add. Tags identical to existing tags will be ignored.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Tag`
            roles (list[Union[dict, ~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment]]): Roles to add or update. Existing roles with the same type (and title,
                for TYPE_OTHER roles) will be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment`
            artifacts (list[Union[dict, ~google.cloud.irm_v1alpha2.types.Artifact]]): Artifacts to add. All artifacts are added without checking for duplicates.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Artifact`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.EscalateIncidentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "escalate_incident" not in self._inner_api_calls:
            self._inner_api_calls[
                "escalate_incident"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.escalate_incident,
                default_retry=self._method_configs["EscalateIncident"].retry,
                default_timeout=self._method_configs["EscalateIncident"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.EscalateIncidentRequest(
            incident=incident,
            update_mask=update_mask,
            subscriptions=subscriptions,
            tags=tags,
            roles=roles,
            artifacts=artifacts,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("incident.name", incident.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["escalate_incident"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_artifact(
        self,
        parent,
        artifact,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new artifact.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # TODO: Initialize `artifact`:
            >>> artifact = {}
            >>>
            >>> response = client.create_artifact(parent, artifact)

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
            artifact (Union[dict, ~google.cloud.irm_v1alpha2.types.Artifact]): The artifact to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Artifact`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Artifact` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_artifact" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_artifact"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_artifact,
                default_retry=self._method_configs["CreateArtifact"].retry,
                default_timeout=self._method_configs["CreateArtifact"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.CreateArtifactRequest(
            parent=parent, artifact=artifact
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

        return self._inner_api_calls["create_artifact"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_artifacts(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns a list of artifacts for an incident.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_artifacts(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_artifacts(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
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
            An iterable of :class:`~google.cloud.irm_v1alpha2.types.Artifact` instances.
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
        if "list_artifacts" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_artifacts"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_artifacts,
                default_retry=self._method_configs["ListArtifacts"].retry,
                default_timeout=self._method_configs["ListArtifacts"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.ListArtifactsRequest(
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
                self._inner_api_calls["list_artifacts"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="artifacts",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def update_artifact(
        self,
        artifact,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates an existing artifact.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> # TODO: Initialize `artifact`:
            >>> artifact = {}
            >>>
            >>> response = client.update_artifact(artifact)

        Args:
            artifact (Union[dict, ~google.cloud.irm_v1alpha2.types.Artifact]): The artifact to update with the new values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Artifact`
            update_mask (Union[dict, ~google.cloud.irm_v1alpha2.types.FieldMask]): List of fields that should be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Artifact` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_artifact" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_artifact"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_artifact,
                default_retry=self._method_configs["UpdateArtifact"].retry,
                default_timeout=self._method_configs["UpdateArtifact"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.UpdateArtifactRequest(
            artifact=artifact, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("artifact.name", artifact.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_artifact"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_artifact(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an existing artifact.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.artifact_path('[PROJECT]', '[INCIDENT]', '[ARTIFACT]')
            >>>
            >>> client.delete_artifact(name)

        Args:
            name (str): Resource name of the artifact.
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
        if "delete_artifact" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_artifact"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_artifact,
                default_retry=self._method_configs["DeleteArtifact"].retry,
                default_timeout=self._method_configs["DeleteArtifact"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.DeleteArtifactRequest(name=name)
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

        self._inner_api_calls["delete_artifact"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def send_shift_handoff(
        self,
        parent,
        recipients,
        subject,
        cc=None,
        notes_content_type=None,
        notes_content=None,
        incidents=None,
        preview_only=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sends a summary of the shift for oncall handoff.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `recipients`:
            >>> recipients = []
            >>>
            >>> # TODO: Initialize `subject`:
            >>> subject = ''
            >>>
            >>> response = client.send_shift_handoff(parent, recipients, subject)

        Args:
            parent (str): The resource name of the Stackdriver project that the handoff is being
                sent from. for example, ``projects/{project_id}``
            recipients (list[str]): Email addresses of the recipients of the handoff, for example,
                "user@example.com". Must contain at least one entry.
            subject (str): The subject of the email. Required.
            cc (list[str]): Email addresses that should be CC'd on the handoff. Optional.
            notes_content_type (str): Content type string, for example, 'text/plain' or 'text/html'.
            notes_content (str): Additional notes to be included in the handoff. Optional.
            incidents (list[Union[dict, ~google.cloud.irm_v1alpha2.types.Incident]]): The set of incidents that should be included in the handoff. Optional.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Incident`
            preview_only (bool): If set to true a ShiftHandoffResponse will be returned but the handoff
                will not actually be sent.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.SendShiftHandoffResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "send_shift_handoff" not in self._inner_api_calls:
            self._inner_api_calls[
                "send_shift_handoff"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.send_shift_handoff,
                default_retry=self._method_configs["SendShiftHandoff"].retry,
                default_timeout=self._method_configs["SendShiftHandoff"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.SendShiftHandoffRequest(
            parent=parent,
            recipients=recipients,
            subject=subject,
            cc=cc,
            notes_content_type=notes_content_type,
            notes_content=notes_content,
            incidents=incidents,
            preview_only=preview_only,
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

        return self._inner_api_calls["send_shift_handoff"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_subscription(
        self,
        parent,
        subscription,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new subscription.
        This will fail if:
        a. there are too many (50) subscriptions in the incident already
        b. a subscription using the given channel already exists

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # TODO: Initialize `subscription`:
            >>> subscription = {}
            >>>
            >>> response = client.create_subscription(parent, subscription)

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
            subscription (Union[dict, ~google.cloud.irm_v1alpha2.types.Subscription]): The subscription to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Subscription`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_subscription,
                default_retry=self._method_configs["CreateSubscription"].retry,
                default_timeout=self._method_configs["CreateSubscription"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.CreateSubscriptionRequest(
            parent=parent, subscription=subscription
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

        return self._inner_api_calls["create_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_subscription(
        self,
        subscription,
        update_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a subscription.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> # TODO: Initialize `subscription`:
            >>> subscription = {}
            >>>
            >>> response = client.update_subscription(subscription)

        Args:
            subscription (Union[dict, ~google.cloud.irm_v1alpha2.types.Subscription]): The subscription to update, with new values.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.Subscription`
            update_mask (Union[dict, ~google.cloud.irm_v1alpha2.types.FieldMask]): List of fields that should be updated.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.Subscription` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_subscription,
                default_retry=self._method_configs["UpdateSubscription"].retry,
                default_timeout=self._method_configs["UpdateSubscription"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.UpdateSubscriptionRequest(
            subscription=subscription, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("subscription.name", subscription.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_subscriptions(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns a list of subscriptions for an incident.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_subscriptions(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_subscriptions(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
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
            An iterable of :class:`~google.cloud.irm_v1alpha2.types.Subscription` instances.
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
        if "list_subscriptions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_subscriptions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_subscriptions,
                default_retry=self._method_configs["ListSubscriptions"].retry,
                default_timeout=self._method_configs["ListSubscriptions"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.ListSubscriptionsRequest(
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
                self._inner_api_calls["list_subscriptions"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="subscriptions",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def delete_subscription(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an existing subscription.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.subscription_path('[PROJECT]', '[INCIDENT]', '[SUBSCRIPTION]')
            >>>
            >>> client.delete_subscription(name)

        Args:
            name (str): Resource name of the subscription.
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
        if "delete_subscription" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_subscription"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_subscription,
                default_retry=self._method_configs["DeleteSubscription"].retry,
                default_timeout=self._method_configs["DeleteSubscription"].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.DeleteSubscriptionRequest(name=name)
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

        self._inner_api_calls["delete_subscription"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_incident_role_assignment(
        self,
        parent,
        incident_role_assignment,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a role assignment on an existing incident. Normally, the user field
        will be set when assigning a role to oneself, and the next field will be
        set when proposing another user as the assignee. Setting the next field
        directly to a user other than oneself is equivalent to proposing and
        force-assigning the role to the user.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # TODO: Initialize `incident_role_assignment`:
            >>> incident_role_assignment = {}
            >>>
            >>> response = client.create_incident_role_assignment(parent, incident_role_assignment)

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
            incident_role_assignment (Union[dict, ~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment]): Role assignment to create.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_incident_role_assignment" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_incident_role_assignment"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_incident_role_assignment,
                default_retry=self._method_configs[
                    "CreateIncidentRoleAssignment"
                ].retry,
                default_timeout=self._method_configs[
                    "CreateIncidentRoleAssignment"
                ].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.CreateIncidentRoleAssignmentRequest(
            parent=parent, incident_role_assignment=incident_role_assignment
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

        return self._inner_api_calls["create_incident_role_assignment"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_incident_role_assignment(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes an existing role assignment.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.role_assignment_path('[PROJECT]', '[INCIDENT]', '[ROLE_ASSIGNMENT]')
            >>>
            >>> client.delete_incident_role_assignment(name)

        Args:
            name (str): Resource name of the role assignment.
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
        if "delete_incident_role_assignment" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_incident_role_assignment"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_incident_role_assignment,
                default_retry=self._method_configs[
                    "DeleteIncidentRoleAssignment"
                ].retry,
                default_timeout=self._method_configs[
                    "DeleteIncidentRoleAssignment"
                ].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.DeleteIncidentRoleAssignmentRequest(name=name)
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

        self._inner_api_calls["delete_incident_role_assignment"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_incident_role_assignments(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists role assignments that are part of an incident.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> parent = client.incident_path('[PROJECT]', '[INCIDENT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_incident_role_assignments(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_incident_role_assignments(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): Resource name of the incident, for example,
                "projects/{project_id}/incidents/{incident_id}".
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
            An iterable of :class:`~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment` instances.
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
        if "list_incident_role_assignments" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_incident_role_assignments"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_incident_role_assignments,
                default_retry=self._method_configs["ListIncidentRoleAssignments"].retry,
                default_timeout=self._method_configs[
                    "ListIncidentRoleAssignments"
                ].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.ListIncidentRoleAssignmentsRequest(
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
                self._inner_api_calls["list_incident_role_assignments"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="incident_role_assignments",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def request_incident_role_handover(
        self,
        name,
        new_assignee,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Starts a role handover. The proposed assignee will receive an email
        notifying them of the assignment. This will fail if a role handover is
        already pending.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.role_assignment_path('[PROJECT]', '[INCIDENT]', '[ROLE_ASSIGNMENT]')
            >>>
            >>> # TODO: Initialize `new_assignee`:
            >>> new_assignee = {}
            >>>
            >>> response = client.request_incident_role_handover(name, new_assignee)

        Args:
            name (str): Resource name of the role assignment.
            new_assignee (Union[dict, ~google.cloud.irm_v1alpha2.types.User]): The proposed assignee.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.User`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "request_incident_role_handover" not in self._inner_api_calls:
            self._inner_api_calls[
                "request_incident_role_handover"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.request_incident_role_handover,
                default_retry=self._method_configs["RequestIncidentRoleHandover"].retry,
                default_timeout=self._method_configs[
                    "RequestIncidentRoleHandover"
                ].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.RequestIncidentRoleHandoverRequest(
            name=name, new_assignee=new_assignee
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

        return self._inner_api_calls["request_incident_role_handover"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def confirm_incident_role_handover(
        self,
        name,
        new_assignee,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Confirms a role handover. This will fail if the 'proposed_assignee'
        field of the IncidentRoleAssignment is not equal to the 'new_assignee'
        field of the request. If the caller is not the new_assignee,
        ForceIncidentRoleHandover should be used instead.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.role_assignment_path('[PROJECT]', '[INCIDENT]', '[ROLE_ASSIGNMENT]')
            >>>
            >>> # TODO: Initialize `new_assignee`:
            >>> new_assignee = {}
            >>>
            >>> response = client.confirm_incident_role_handover(name, new_assignee)

        Args:
            name (str): Resource name of the role assignment.
            new_assignee (Union[dict, ~google.cloud.irm_v1alpha2.types.User]): The proposed assignee, who will now be the assignee. This should be the
                current user; otherwise ForceRoleHandover should be called.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.User`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "confirm_incident_role_handover" not in self._inner_api_calls:
            self._inner_api_calls[
                "confirm_incident_role_handover"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.confirm_incident_role_handover,
                default_retry=self._method_configs["ConfirmIncidentRoleHandover"].retry,
                default_timeout=self._method_configs[
                    "ConfirmIncidentRoleHandover"
                ].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.ConfirmIncidentRoleHandoverRequest(
            name=name, new_assignee=new_assignee
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

        return self._inner_api_calls["confirm_incident_role_handover"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def force_incident_role_handover(
        self,
        name,
        new_assignee,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Forces a role handover. This will fail if the 'proposed_assignee' field
        of the IncidentRoleAssignment is not equal to the 'new_assignee' field
        of the request. If the caller is the new_assignee,
        ConfirmIncidentRoleHandover should be used instead.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.role_assignment_path('[PROJECT]', '[INCIDENT]', '[ROLE_ASSIGNMENT]')
            >>>
            >>> # TODO: Initialize `new_assignee`:
            >>> new_assignee = {}
            >>>
            >>> response = client.force_incident_role_handover(name, new_assignee)

        Args:
            name (str): Resource name of the role assignment.
            new_assignee (Union[dict, ~google.cloud.irm_v1alpha2.types.User]): The proposed assignee, who will now be the assignee. This should not be
                the current user; otherwise ConfirmRoleHandover should be called.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.User`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "force_incident_role_handover" not in self._inner_api_calls:
            self._inner_api_calls[
                "force_incident_role_handover"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.force_incident_role_handover,
                default_retry=self._method_configs["ForceIncidentRoleHandover"].retry,
                default_timeout=self._method_configs[
                    "ForceIncidentRoleHandover"
                ].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.ForceIncidentRoleHandoverRequest(
            name=name, new_assignee=new_assignee
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

        return self._inner_api_calls["force_incident_role_handover"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def cancel_incident_role_handover(
        self,
        name,
        new_assignee,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Cancels a role handover. This will fail if the 'proposed_assignee'
        field of the IncidentRoleAssignment is not equal to the 'new_assignee'
        field of the request.

        Example:
            >>> from google.cloud import irm_v1alpha2
            >>>
            >>> client = irm_v1alpha2.IncidentServiceClient()
            >>>
            >>> name = client.role_assignment_path('[PROJECT]', '[INCIDENT]', '[ROLE_ASSIGNMENT]')
            >>>
            >>> # TODO: Initialize `new_assignee`:
            >>> new_assignee = {}
            >>>
            >>> response = client.cancel_incident_role_handover(name, new_assignee)

        Args:
            name (str): Resource name of the role assignment.
            new_assignee (Union[dict, ~google.cloud.irm_v1alpha2.types.User]): Person who was proposed as the next assignee (i.e.
                IncidentRoleAssignment.proposed_assignee) and whose proposal is being
                cancelled.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.irm_v1alpha2.types.User`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.irm_v1alpha2.types.IncidentRoleAssignment` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "cancel_incident_role_handover" not in self._inner_api_calls:
            self._inner_api_calls[
                "cancel_incident_role_handover"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.cancel_incident_role_handover,
                default_retry=self._method_configs["CancelIncidentRoleHandover"].retry,
                default_timeout=self._method_configs[
                    "CancelIncidentRoleHandover"
                ].timeout,
                client_info=self._client_info,
            )

        request = incidents_service_pb2.CancelIncidentRoleHandoverRequest(
            name=name, new_assignee=new_assignee
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

        return self._inner_api_calls["cancel_incident_role_handover"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
