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

"""Accesses the google.cloud.webrisk.v1beta1 WebRiskServiceV1Beta1 API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import grpc

from google.cloud.webrisk_v1beta1.gapic import enums
from google.cloud.webrisk_v1beta1.gapic import web_risk_service_v1_beta1_client_config
from google.cloud.webrisk_v1beta1.gapic.transports import (
    web_risk_service_v1_beta1_grpc_transport,
)
from google.cloud.webrisk_v1beta1.proto import webrisk_pb2
from google.cloud.webrisk_v1beta1.proto import webrisk_pb2_grpc


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-webrisk").version


class WebRiskServiceV1Beta1Client(object):
    """
    Web Risk v1beta1 API defines an interface to detect malicious URLs on your
    website and in client applications.
    """

    SERVICE_ADDRESS = "webrisk.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.webrisk.v1beta1.WebRiskServiceV1Beta1"

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
            WebRiskServiceV1Beta1Client: The constructed client.
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
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.WebRiskServiceV1Beta1GrpcTransport,
                    Callable[[~.Credentials, type], ~.WebRiskServiceV1Beta1GrpcTransport]): A transport
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
            client_config = web_risk_service_v1_beta1_client_config.config

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
                    default_class=web_risk_service_v1_beta1_grpc_transport.WebRiskServiceV1Beta1GrpcTransport,
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
            self.transport = web_risk_service_v1_beta1_grpc_transport.WebRiskServiceV1Beta1GrpcTransport(
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
    def compute_threat_list_diff(
        self,
        threat_type,
        constraints,
        version_token=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the most recent threat list diffs.

        Example:
            >>> from google.cloud import webrisk_v1beta1
            >>> from google.cloud.webrisk_v1beta1 import enums
            >>>
            >>> client = webrisk_v1beta1.WebRiskServiceV1Beta1Client()
            >>>
            >>> # TODO: Initialize `threat_type`:
            >>> threat_type = enums.ThreatType.THREAT_TYPE_UNSPECIFIED
            >>>
            >>> # TODO: Initialize `constraints`:
            >>> constraints = {}
            >>>
            >>> response = client.compute_threat_list_diff(threat_type, constraints)

        Args:
            threat_type (~google.cloud.webrisk_v1beta1.types.ThreatType): Required. The ThreatList to update.
            constraints (Union[dict, ~google.cloud.webrisk_v1beta1.types.Constraints]): The constraints associated with this request.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.webrisk_v1beta1.types.Constraints`
            version_token (bytes): The current version token of the client for the requested list (the
                client version that was received from the last successful diff).
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.webrisk_v1beta1.types.ComputeThreatListDiffResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "compute_threat_list_diff" not in self._inner_api_calls:
            self._inner_api_calls[
                "compute_threat_list_diff"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.compute_threat_list_diff,
                default_retry=self._method_configs["ComputeThreatListDiff"].retry,
                default_timeout=self._method_configs["ComputeThreatListDiff"].timeout,
                client_info=self._client_info,
            )

        request = webrisk_pb2.ComputeThreatListDiffRequest(
            threat_type=threat_type,
            constraints=constraints,
            version_token=version_token,
        )
        return self._inner_api_calls["compute_threat_list_diff"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def search_uris(
        self,
        uri,
        threat_types,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        This method is used to check whether a URI is on a given threatList.

        Example:
            >>> from google.cloud import webrisk_v1beta1
            >>> from google.cloud.webrisk_v1beta1 import enums
            >>>
            >>> client = webrisk_v1beta1.WebRiskServiceV1Beta1Client()
            >>>
            >>> # TODO: Initialize `uri`:
            >>> uri = ''
            >>>
            >>> # TODO: Initialize `threat_types`:
            >>> threat_types = []
            >>>
            >>> response = client.search_uris(uri, threat_types)

        Args:
            uri (str): The URI to be checked for matches.
            threat_types (list[~google.cloud.webrisk_v1beta1.types.ThreatType]): Required. The ThreatLists to search in.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.webrisk_v1beta1.types.SearchUrisResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "search_uris" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_uris"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_uris,
                default_retry=self._method_configs["SearchUris"].retry,
                default_timeout=self._method_configs["SearchUris"].timeout,
                client_info=self._client_info,
            )

        request = webrisk_pb2.SearchUrisRequest(uri=uri, threat_types=threat_types)
        return self._inner_api_calls["search_uris"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def search_hashes(
        self,
        threat_types,
        hash_prefix=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the full hashes that match the requested hash prefix.
        This is used after a hash prefix is looked up in a threatList
        and there is a match. The client side threatList only holds partial hashes
        so the client must query this method to determine if there is a full
        hash match of a threat.

        Example:
            >>> from google.cloud import webrisk_v1beta1
            >>> from google.cloud.webrisk_v1beta1 import enums
            >>>
            >>> client = webrisk_v1beta1.WebRiskServiceV1Beta1Client()
            >>>
            >>> # TODO: Initialize `threat_types`:
            >>> threat_types = []
            >>>
            >>> response = client.search_hashes(threat_types)

        Args:
            threat_types (list[~google.cloud.webrisk_v1beta1.types.ThreatType]): Required. The ThreatLists to search in.
            hash_prefix (bytes): A hash prefix, consisting of the most significant 4-32 bytes of a SHA256
                hash. For JSON requests, this field is base64-encoded.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.webrisk_v1beta1.types.SearchHashesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "search_hashes" not in self._inner_api_calls:
            self._inner_api_calls[
                "search_hashes"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_hashes,
                default_retry=self._method_configs["SearchHashes"].retry,
                default_timeout=self._method_configs["SearchHashes"].timeout,
                client_info=self._client_info,
            )

        request = webrisk_pb2.SearchHashesRequest(
            threat_types=threat_types, hash_prefix=hash_prefix
        )
        return self._inner_api_calls["search_hashes"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
