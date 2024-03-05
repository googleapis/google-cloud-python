# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.dialogflow_v2beta1.types import (
    conversation_profile as gcd_conversation_profile,
)
from google.cloud.dialogflow_v2beta1.types import conversation_profile

from .base import ConversationProfilesTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class ConversationProfilesRestInterceptor:
    """Interceptor for ConversationProfiles.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ConversationProfilesRestTransport.

    .. code-block:: python
        class MyCustomConversationProfilesInterceptor(ConversationProfilesRestInterceptor):
            def pre_clear_suggestion_feature_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_clear_suggestion_feature_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_conversation_profile(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_conversation_profile(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_conversation_profile(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_conversation_profile(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_conversation_profile(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_conversation_profiles(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_conversation_profiles(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_suggestion_feature_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_suggestion_feature_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_conversation_profile(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_conversation_profile(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ConversationProfilesRestTransport(interceptor=MyCustomConversationProfilesInterceptor())
        client = ConversationProfilesClient(transport=transport)


    """

    def pre_clear_suggestion_feature_config(
        self,
        request: gcd_conversation_profile.ClearSuggestionFeatureConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcd_conversation_profile.ClearSuggestionFeatureConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for clear_suggestion_feature_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_clear_suggestion_feature_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for clear_suggestion_feature_config

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_create_conversation_profile(
        self,
        request: gcd_conversation_profile.CreateConversationProfileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcd_conversation_profile.CreateConversationProfileRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_conversation_profile

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_create_conversation_profile(
        self, response: gcd_conversation_profile.ConversationProfile
    ) -> gcd_conversation_profile.ConversationProfile:
        """Post-rpc interceptor for create_conversation_profile

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_delete_conversation_profile(
        self,
        request: conversation_profile.DeleteConversationProfileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        conversation_profile.DeleteConversationProfileRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_conversation_profile

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def pre_get_conversation_profile(
        self,
        request: conversation_profile.GetConversationProfileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        conversation_profile.GetConversationProfileRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_conversation_profile

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_get_conversation_profile(
        self, response: conversation_profile.ConversationProfile
    ) -> conversation_profile.ConversationProfile:
        """Post-rpc interceptor for get_conversation_profile

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_list_conversation_profiles(
        self,
        request: conversation_profile.ListConversationProfilesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        conversation_profile.ListConversationProfilesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_conversation_profiles

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_list_conversation_profiles(
        self, response: conversation_profile.ListConversationProfilesResponse
    ) -> conversation_profile.ListConversationProfilesResponse:
        """Post-rpc interceptor for list_conversation_profiles

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_set_suggestion_feature_config(
        self,
        request: gcd_conversation_profile.SetSuggestionFeatureConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcd_conversation_profile.SetSuggestionFeatureConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for set_suggestion_feature_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_set_suggestion_feature_config(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for set_suggestion_feature_config

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_update_conversation_profile(
        self,
        request: gcd_conversation_profile.UpdateConversationProfileRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcd_conversation_profile.UpdateConversationProfileRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_conversation_profile

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_update_conversation_profile(
        self, response: gcd_conversation_profile.ConversationProfile
    ) -> gcd_conversation_profile.ConversationProfile:
        """Post-rpc interceptor for update_conversation_profile

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConversationProfiles server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the ConversationProfiles server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ConversationProfilesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ConversationProfilesRestInterceptor


class ConversationProfilesRestTransport(ConversationProfilesTransport):
    """REST backend transport for ConversationProfiles.

    Service for managing
    [ConversationProfiles][google.cloud.dialogflow.v2beta1.ConversationProfile].

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "dialogflow.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ConversationProfilesRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'dialogflow.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ConversationProfilesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v2beta1/{name=projects/*/operations/*}:cancel",
                    },
                    {
                        "method": "post",
                        "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}:cancel",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*}/operations",
                    },
                    {
                        "method": "get",
                        "uri": "/v2beta1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2beta1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _ClearSuggestionFeatureConfig(ConversationProfilesRestStub):
        def __hash__(self):
            return hash("ClearSuggestionFeatureConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcd_conversation_profile.ClearSuggestionFeatureConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the clear suggestion feature
            config method over HTTP.

                Args:
                    request (~.gcd_conversation_profile.ClearSuggestionFeatureConfigRequest):
                        The request object. The request message for
                    [ConversationProfiles.ClearFeature][].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2beta1/{conversation_profile=projects/*/conversationProfiles/*}:clearSuggestionFeatureConfig",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2beta1/{conversation_profile=projects/*/locations/*/conversationProfiles/*}:clearSuggestionFeatureConfig",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_clear_suggestion_feature_config(
                request, metadata
            )
            pb_request = (
                gcd_conversation_profile.ClearSuggestionFeatureConfigRequest.pb(request)
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_clear_suggestion_feature_config(resp)
            return resp

    class _CreateConversationProfile(ConversationProfilesRestStub):
        def __hash__(self):
            return hash("CreateConversationProfile")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcd_conversation_profile.CreateConversationProfileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_conversation_profile.ConversationProfile:
            r"""Call the create conversation
            profile method over HTTP.

                Args:
                    request (~.gcd_conversation_profile.CreateConversationProfileRequest):
                        The request object. The request message for
                    [ConversationProfiles.CreateConversationProfile][google.cloud.dialogflow.v2beta1.ConversationProfiles.CreateConversationProfile].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcd_conversation_profile.ConversationProfile:
                        Defines the services to connect to
                    incoming Dialogflow conversations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2beta1/{parent=projects/*}/conversationProfiles",
                    "body": "conversation_profile",
                },
                {
                    "method": "post",
                    "uri": "/v2beta1/{parent=projects/*/locations/*}/conversationProfiles",
                    "body": "conversation_profile",
                },
            ]
            request, metadata = self._interceptor.pre_create_conversation_profile(
                request, metadata
            )
            pb_request = gcd_conversation_profile.CreateConversationProfileRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcd_conversation_profile.ConversationProfile()
            pb_resp = gcd_conversation_profile.ConversationProfile.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_conversation_profile(resp)
            return resp

    class _DeleteConversationProfile(ConversationProfilesRestStub):
        def __hash__(self):
            return hash("DeleteConversationProfile")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: conversation_profile.DeleteConversationProfileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete conversation
            profile method over HTTP.

                Args:
                    request (~.conversation_profile.DeleteConversationProfileRequest):
                        The request object. The request message for
                    [ConversationProfiles.DeleteConversationProfile][google.cloud.dialogflow.v2beta1.ConversationProfiles.DeleteConversationProfile].

                    This operation fails if the conversation profile is
                    still referenced from a phone number.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2beta1/{name=projects/*/conversationProfiles/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2beta1/{name=projects/*/locations/*/conversationProfiles/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_conversation_profile(
                request, metadata
            )
            pb_request = conversation_profile.DeleteConversationProfileRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _GetConversationProfile(ConversationProfilesRestStub):
        def __hash__(self):
            return hash("GetConversationProfile")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: conversation_profile.GetConversationProfileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversation_profile.ConversationProfile:
            r"""Call the get conversation profile method over HTTP.

            Args:
                request (~.conversation_profile.GetConversationProfileRequest):
                    The request object. The request message for
                [ConversationProfiles.GetConversationProfile][google.cloud.dialogflow.v2beta1.ConversationProfiles.GetConversationProfile].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.conversation_profile.ConversationProfile:
                    Defines the services to connect to
                incoming Dialogflow conversations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/conversationProfiles/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/locations/*/conversationProfiles/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_conversation_profile(
                request, metadata
            )
            pb_request = conversation_profile.GetConversationProfileRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = conversation_profile.ConversationProfile()
            pb_resp = conversation_profile.ConversationProfile.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_conversation_profile(resp)
            return resp

    class _ListConversationProfiles(ConversationProfilesRestStub):
        def __hash__(self):
            return hash("ListConversationProfiles")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: conversation_profile.ListConversationProfilesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> conversation_profile.ListConversationProfilesResponse:
            r"""Call the list conversation
            profiles method over HTTP.

                Args:
                    request (~.conversation_profile.ListConversationProfilesRequest):
                        The request object. The request message for
                    [ConversationProfiles.ListConversationProfiles][google.cloud.dialogflow.v2beta1.ConversationProfiles.ListConversationProfiles].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.conversation_profile.ListConversationProfilesResponse:
                        The response message for
                    [ConversationProfiles.ListConversationProfiles][google.cloud.dialogflow.v2beta1.ConversationProfiles.ListConversationProfiles].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2beta1/{parent=projects/*}/conversationProfiles",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{parent=projects/*/locations/*}/conversationProfiles",
                },
            ]
            request, metadata = self._interceptor.pre_list_conversation_profiles(
                request, metadata
            )
            pb_request = conversation_profile.ListConversationProfilesRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = conversation_profile.ListConversationProfilesResponse()
            pb_resp = conversation_profile.ListConversationProfilesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_conversation_profiles(resp)
            return resp

    class _SetSuggestionFeatureConfig(ConversationProfilesRestStub):
        def __hash__(self):
            return hash("SetSuggestionFeatureConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcd_conversation_profile.SetSuggestionFeatureConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the set suggestion feature
            config method over HTTP.

                Args:
                    request (~.gcd_conversation_profile.SetSuggestionFeatureConfigRequest):
                        The request object. The request message for
                    [ConversationProfiles.SetSuggestionFeature][].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2beta1/{conversation_profile=projects/*/conversationProfiles/*}:setSuggestionFeatureConfig",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2beta1/{conversation_profile=projects/*/locations/*/conversationProfiles/*}:setSuggestionFeatureConfig",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_suggestion_feature_config(
                request, metadata
            )
            pb_request = gcd_conversation_profile.SetSuggestionFeatureConfigRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_suggestion_feature_config(resp)
            return resp

    class _UpdateConversationProfile(ConversationProfilesRestStub):
        def __hash__(self):
            return hash("UpdateConversationProfile")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcd_conversation_profile.UpdateConversationProfileRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcd_conversation_profile.ConversationProfile:
            r"""Call the update conversation
            profile method over HTTP.

                Args:
                    request (~.gcd_conversation_profile.UpdateConversationProfileRequest):
                        The request object. The request message for
                    [ConversationProfiles.UpdateConversationProfile][google.cloud.dialogflow.v2beta1.ConversationProfiles.UpdateConversationProfile].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcd_conversation_profile.ConversationProfile:
                        Defines the services to connect to
                    incoming Dialogflow conversations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2beta1/{conversation_profile.name=projects/*/conversationProfiles/*}",
                    "body": "conversation_profile",
                },
                {
                    "method": "patch",
                    "uri": "/v2beta1/{conversation_profile.name=projects/*/locations/*/conversationProfiles/*}",
                    "body": "conversation_profile",
                },
            ]
            request, metadata = self._interceptor.pre_update_conversation_profile(
                request, metadata
            )
            pb_request = gcd_conversation_profile.UpdateConversationProfileRequest.pb(
                request
            )
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcd_conversation_profile.ConversationProfile()
            pb_resp = gcd_conversation_profile.ConversationProfile.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_conversation_profile(resp)
            return resp

    @property
    def clear_suggestion_feature_config(
        self,
    ) -> Callable[
        [gcd_conversation_profile.ClearSuggestionFeatureConfigRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ClearSuggestionFeatureConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_conversation_profile(
        self,
    ) -> Callable[
        [gcd_conversation_profile.CreateConversationProfileRequest],
        gcd_conversation_profile.ConversationProfile,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateConversationProfile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_conversation_profile(
        self,
    ) -> Callable[
        [conversation_profile.DeleteConversationProfileRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteConversationProfile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_conversation_profile(
        self,
    ) -> Callable[
        [conversation_profile.GetConversationProfileRequest],
        conversation_profile.ConversationProfile,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConversationProfile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_conversation_profiles(
        self,
    ) -> Callable[
        [conversation_profile.ListConversationProfilesRequest],
        conversation_profile.ListConversationProfilesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConversationProfiles(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_suggestion_feature_config(
        self,
    ) -> Callable[
        [gcd_conversation_profile.SetSuggestionFeatureConfigRequest],
        operations_pb2.Operation,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetSuggestionFeatureConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_conversation_profile(
        self,
    ) -> Callable[
        [gcd_conversation_profile.UpdateConversationProfileRequest],
        gcd_conversation_profile.ConversationProfile,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateConversationProfile(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(ConversationProfilesRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(ConversationProfilesRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(ConversationProfilesRestStub):
        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2beta1/{name=projects/*/operations/*}:cancel",
                },
                {
                    "method": "post",
                    "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}:cancel",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(ConversationProfilesRestStub):
        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(ConversationProfilesRestStub):
        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*}/operations",
                },
                {
                    "method": "get",
                    "uri": "/v2beta1/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ConversationProfilesRestTransport",)
