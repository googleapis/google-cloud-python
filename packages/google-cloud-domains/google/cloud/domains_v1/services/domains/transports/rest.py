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
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.domains_v1.types import domains

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import DomainsTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class DomainsRestInterceptor:
    """Interceptor for Domains.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the DomainsRestTransport.

    .. code-block:: python
        class MyCustomDomainsInterceptor(DomainsRestInterceptor):
            def pre_configure_contact_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_configure_contact_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_configure_dns_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_configure_dns_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_configure_management_settings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_configure_management_settings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_registration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_registration(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_export_registration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_export_registration(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_registration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_registration(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_registrations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_registrations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_register_domain(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_register_domain(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_reset_authorization_code(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_reset_authorization_code(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_retrieve_authorization_code(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retrieve_authorization_code(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_retrieve_register_parameters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retrieve_register_parameters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_retrieve_transfer_parameters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retrieve_transfer_parameters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_search_domains(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_search_domains(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_transfer_domain(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_transfer_domain(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_registration(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_registration(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = DomainsRestTransport(interceptor=MyCustomDomainsInterceptor())
        client = DomainsClient(transport=transport)


    """

    def pre_configure_contact_settings(
        self,
        request: domains.ConfigureContactSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.ConfigureContactSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for configure_contact_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_configure_contact_settings(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for configure_contact_settings

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_configure_dns_settings(
        self,
        request: domains.ConfigureDnsSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.ConfigureDnsSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for configure_dns_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_configure_dns_settings(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for configure_dns_settings

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_configure_management_settings(
        self,
        request: domains.ConfigureManagementSettingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.ConfigureManagementSettingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for configure_management_settings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_configure_management_settings(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for configure_management_settings

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_delete_registration(
        self,
        request: domains.DeleteRegistrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.DeleteRegistrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_registration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_delete_registration(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_registration

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_export_registration(
        self,
        request: domains.ExportRegistrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.ExportRegistrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for export_registration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_export_registration(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for export_registration

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_get_registration(
        self,
        request: domains.GetRegistrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.GetRegistrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_registration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_get_registration(
        self, response: domains.Registration
    ) -> domains.Registration:
        """Post-rpc interceptor for get_registration

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_list_registrations(
        self,
        request: domains.ListRegistrationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.ListRegistrationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_registrations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_list_registrations(
        self, response: domains.ListRegistrationsResponse
    ) -> domains.ListRegistrationsResponse:
        """Post-rpc interceptor for list_registrations

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_register_domain(
        self,
        request: domains.RegisterDomainRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.RegisterDomainRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for register_domain

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_register_domain(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for register_domain

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_reset_authorization_code(
        self,
        request: domains.ResetAuthorizationCodeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.ResetAuthorizationCodeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for reset_authorization_code

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_reset_authorization_code(
        self, response: domains.AuthorizationCode
    ) -> domains.AuthorizationCode:
        """Post-rpc interceptor for reset_authorization_code

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_retrieve_authorization_code(
        self,
        request: domains.RetrieveAuthorizationCodeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.RetrieveAuthorizationCodeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for retrieve_authorization_code

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_retrieve_authorization_code(
        self, response: domains.AuthorizationCode
    ) -> domains.AuthorizationCode:
        """Post-rpc interceptor for retrieve_authorization_code

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_retrieve_register_parameters(
        self,
        request: domains.RetrieveRegisterParametersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.RetrieveRegisterParametersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for retrieve_register_parameters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_retrieve_register_parameters(
        self, response: domains.RetrieveRegisterParametersResponse
    ) -> domains.RetrieveRegisterParametersResponse:
        """Post-rpc interceptor for retrieve_register_parameters

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_retrieve_transfer_parameters(
        self,
        request: domains.RetrieveTransferParametersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.RetrieveTransferParametersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for retrieve_transfer_parameters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_retrieve_transfer_parameters(
        self, response: domains.RetrieveTransferParametersResponse
    ) -> domains.RetrieveTransferParametersResponse:
        """Post-rpc interceptor for retrieve_transfer_parameters

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_search_domains(
        self, request: domains.SearchDomainsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[domains.SearchDomainsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for search_domains

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_search_domains(
        self, response: domains.SearchDomainsResponse
    ) -> domains.SearchDomainsResponse:
        """Post-rpc interceptor for search_domains

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_transfer_domain(
        self,
        request: domains.TransferDomainRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.TransferDomainRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for transfer_domain

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_transfer_domain(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for transfer_domain

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response

    def pre_update_registration(
        self,
        request: domains.UpdateRegistrationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[domains.UpdateRegistrationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_registration

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Domains server.
        """
        return request, metadata

    def post_update_registration(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_registration

        Override in a subclass to manipulate the response
        after it is returned by the Domains server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class DomainsRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: DomainsRestInterceptor


class DomainsRestTransport(DomainsTransport):
    """REST backend transport for Domains.

    The Cloud Domains API enables management and configuration of
    domain names.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "domains.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[DomainsRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'domains.googleapis.com').
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
        self._interceptor = interceptor or DomainsRestInterceptor()
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
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _ConfigureContactSettings(DomainsRestStub):
        def __hash__(self):
            return hash("ConfigureContactSettings")

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
            request: domains.ConfigureContactSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the configure contact
            settings method over HTTP.

                Args:
                    request (~.domains.ConfigureContactSettingsRequest):
                        The request object. Request for the ``ConfigureContactSettings`` method.
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
                    "uri": "/v1/{registration=projects/*/locations/*/registrations/*}:configureContactSettings",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_configure_contact_settings(
                request, metadata
            )
            pb_request = domains.ConfigureContactSettingsRequest.pb(request)
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
            resp = self._interceptor.post_configure_contact_settings(resp)
            return resp

    class _ConfigureDnsSettings(DomainsRestStub):
        def __hash__(self):
            return hash("ConfigureDnsSettings")

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
            request: domains.ConfigureDnsSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the configure dns settings method over HTTP.

            Args:
                request (~.domains.ConfigureDnsSettingsRequest):
                    The request object. Request for the ``ConfigureDnsSettings`` method.
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
                    "uri": "/v1/{registration=projects/*/locations/*/registrations/*}:configureDnsSettings",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_configure_dns_settings(
                request, metadata
            )
            pb_request = domains.ConfigureDnsSettingsRequest.pb(request)
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
            resp = self._interceptor.post_configure_dns_settings(resp)
            return resp

    class _ConfigureManagementSettings(DomainsRestStub):
        def __hash__(self):
            return hash("ConfigureManagementSettings")

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
            request: domains.ConfigureManagementSettingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the configure management
            settings method over HTTP.

                Args:
                    request (~.domains.ConfigureManagementSettingsRequest):
                        The request object. Request for the ``ConfigureManagementSettings`` method.
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
                    "uri": "/v1/{registration=projects/*/locations/*/registrations/*}:configureManagementSettings",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_configure_management_settings(
                request, metadata
            )
            pb_request = domains.ConfigureManagementSettingsRequest.pb(request)
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
            resp = self._interceptor.post_configure_management_settings(resp)
            return resp

    class _DeleteRegistration(DomainsRestStub):
        def __hash__(self):
            return hash("DeleteRegistration")

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
            request: domains.DeleteRegistrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete registration method over HTTP.

            Args:
                request (~.domains.DeleteRegistrationRequest):
                    The request object. Request for the ``DeleteRegistration`` method.
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
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/registrations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_registration(
                request, metadata
            )
            pb_request = domains.DeleteRegistrationRequest.pb(request)
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
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_registration(resp)
            return resp

    class _ExportRegistration(DomainsRestStub):
        def __hash__(self):
            return hash("ExportRegistration")

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
            request: domains.ExportRegistrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the export registration method over HTTP.

            Args:
                request (~.domains.ExportRegistrationRequest):
                    The request object. Request for the ``ExportRegistration`` method.
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
                    "uri": "/v1/{name=projects/*/locations/*/registrations/*}:export",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_export_registration(
                request, metadata
            )
            pb_request = domains.ExportRegistrationRequest.pb(request)
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
            resp = self._interceptor.post_export_registration(resp)
            return resp

    class _GetRegistration(DomainsRestStub):
        def __hash__(self):
            return hash("GetRegistration")

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
            request: domains.GetRegistrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> domains.Registration:
            r"""Call the get registration method over HTTP.

            Args:
                request (~.domains.GetRegistrationRequest):
                    The request object. Request for the ``GetRegistration`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.domains.Registration:
                    The ``Registration`` resource facilitates managing and
                configuring domain name registrations.

                There are several ways to create a new ``Registration``
                resource:

                To create a new ``Registration`` resource, find a
                suitable domain name by calling the ``SearchDomains``
                method with a query to see available domain name
                options. After choosing a name, call
                ``RetrieveRegisterParameters`` to ensure availability
                and obtain information like pricing, which is needed to
                build a call to ``RegisterDomain``.

                Another way to create a new ``Registration`` is to
                transfer an existing domain from another registrar.
                First, go to the current registrar to unlock the domain
                for transfer and retrieve the domain's transfer
                authorization code. Then call
                ``RetrieveTransferParameters`` to confirm that the
                domain is unlocked and to get values needed to build a
                call to ``TransferDomain``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/registrations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_registration(
                request, metadata
            )
            pb_request = domains.GetRegistrationRequest.pb(request)
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
            resp = domains.Registration()
            pb_resp = domains.Registration.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_registration(resp)
            return resp

    class _ListRegistrations(DomainsRestStub):
        def __hash__(self):
            return hash("ListRegistrations")

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
            request: domains.ListRegistrationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> domains.ListRegistrationsResponse:
            r"""Call the list registrations method over HTTP.

            Args:
                request (~.domains.ListRegistrationsRequest):
                    The request object. Request for the ``ListRegistrations`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.domains.ListRegistrationsResponse:
                    Response for the ``ListRegistrations`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/registrations",
                },
            ]
            request, metadata = self._interceptor.pre_list_registrations(
                request, metadata
            )
            pb_request = domains.ListRegistrationsRequest.pb(request)
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
            resp = domains.ListRegistrationsResponse()
            pb_resp = domains.ListRegistrationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_registrations(resp)
            return resp

    class _RegisterDomain(DomainsRestStub):
        def __hash__(self):
            return hash("RegisterDomain")

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
            request: domains.RegisterDomainRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the register domain method over HTTP.

            Args:
                request (~.domains.RegisterDomainRequest):
                    The request object. Request for the ``RegisterDomain`` method.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/registrations:register",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_register_domain(request, metadata)
            pb_request = domains.RegisterDomainRequest.pb(request)
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
            resp = self._interceptor.post_register_domain(resp)
            return resp

    class _ResetAuthorizationCode(DomainsRestStub):
        def __hash__(self):
            return hash("ResetAuthorizationCode")

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
            request: domains.ResetAuthorizationCodeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> domains.AuthorizationCode:
            r"""Call the reset authorization code method over HTTP.

            Args:
                request (~.domains.ResetAuthorizationCodeRequest):
                    The request object. Request for the ``ResetAuthorizationCode`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.domains.AuthorizationCode:
                    Defines an authorization code.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{registration=projects/*/locations/*/registrations/*}:resetAuthorizationCode",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_reset_authorization_code(
                request, metadata
            )
            pb_request = domains.ResetAuthorizationCodeRequest.pb(request)
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
            resp = domains.AuthorizationCode()
            pb_resp = domains.AuthorizationCode.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_reset_authorization_code(resp)
            return resp

    class _RetrieveAuthorizationCode(DomainsRestStub):
        def __hash__(self):
            return hash("RetrieveAuthorizationCode")

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
            request: domains.RetrieveAuthorizationCodeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> domains.AuthorizationCode:
            r"""Call the retrieve authorization
            code method over HTTP.

                Args:
                    request (~.domains.RetrieveAuthorizationCodeRequest):
                        The request object. Request for the ``RetrieveAuthorizationCode`` method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.domains.AuthorizationCode:
                        Defines an authorization code.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{registration=projects/*/locations/*/registrations/*}:retrieveAuthorizationCode",
                },
            ]
            request, metadata = self._interceptor.pre_retrieve_authorization_code(
                request, metadata
            )
            pb_request = domains.RetrieveAuthorizationCodeRequest.pb(request)
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
            resp = domains.AuthorizationCode()
            pb_resp = domains.AuthorizationCode.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_retrieve_authorization_code(resp)
            return resp

    class _RetrieveRegisterParameters(DomainsRestStub):
        def __hash__(self):
            return hash("RetrieveRegisterParameters")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "domainName": "",
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
            request: domains.RetrieveRegisterParametersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> domains.RetrieveRegisterParametersResponse:
            r"""Call the retrieve register
            parameters method over HTTP.

                Args:
                    request (~.domains.RetrieveRegisterParametersRequest):
                        The request object. Request for the ``RetrieveRegisterParameters`` method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.domains.RetrieveRegisterParametersResponse:
                        Response for the ``RetrieveRegisterParameters`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{location=projects/*/locations/*}/registrations:retrieveRegisterParameters",
                },
            ]
            request, metadata = self._interceptor.pre_retrieve_register_parameters(
                request, metadata
            )
            pb_request = domains.RetrieveRegisterParametersRequest.pb(request)
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
            resp = domains.RetrieveRegisterParametersResponse()
            pb_resp = domains.RetrieveRegisterParametersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_retrieve_register_parameters(resp)
            return resp

    class _RetrieveTransferParameters(DomainsRestStub):
        def __hash__(self):
            return hash("RetrieveTransferParameters")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "domainName": "",
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
            request: domains.RetrieveTransferParametersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> domains.RetrieveTransferParametersResponse:
            r"""Call the retrieve transfer
            parameters method over HTTP.

                Args:
                    request (~.domains.RetrieveTransferParametersRequest):
                        The request object. Request for the ``RetrieveTransferParameters`` method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.domains.RetrieveTransferParametersResponse:
                        Response for the ``RetrieveTransferParameters`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{location=projects/*/locations/*}/registrations:retrieveTransferParameters",
                },
            ]
            request, metadata = self._interceptor.pre_retrieve_transfer_parameters(
                request, metadata
            )
            pb_request = domains.RetrieveTransferParametersRequest.pb(request)
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
            resp = domains.RetrieveTransferParametersResponse()
            pb_resp = domains.RetrieveTransferParametersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_retrieve_transfer_parameters(resp)
            return resp

    class _SearchDomains(DomainsRestStub):
        def __hash__(self):
            return hash("SearchDomains")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "query": "",
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
            request: domains.SearchDomainsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> domains.SearchDomainsResponse:
            r"""Call the search domains method over HTTP.

            Args:
                request (~.domains.SearchDomainsRequest):
                    The request object. Request for the ``SearchDomains`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.domains.SearchDomainsResponse:
                    Response for the ``SearchDomains`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{location=projects/*/locations/*}/registrations:searchDomains",
                },
            ]
            request, metadata = self._interceptor.pre_search_domains(request, metadata)
            pb_request = domains.SearchDomainsRequest.pb(request)
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
            resp = domains.SearchDomainsResponse()
            pb_resp = domains.SearchDomainsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_search_domains(resp)
            return resp

    class _TransferDomain(DomainsRestStub):
        def __hash__(self):
            return hash("TransferDomain")

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
            request: domains.TransferDomainRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the transfer domain method over HTTP.

            Args:
                request (~.domains.TransferDomainRequest):
                    The request object. Request for the ``TransferDomain`` method.
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
                    "uri": "/v1/{parent=projects/*/locations/*}/registrations:transfer",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_transfer_domain(request, metadata)
            pb_request = domains.TransferDomainRequest.pb(request)
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
            resp = self._interceptor.post_transfer_domain(resp)
            return resp

    class _UpdateRegistration(DomainsRestStub):
        def __hash__(self):
            return hash("UpdateRegistration")

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
            request: domains.UpdateRegistrationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update registration method over HTTP.

            Args:
                request (~.domains.UpdateRegistrationRequest):
                    The request object. Request for the ``UpdateRegistration`` method.
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
                    "method": "patch",
                    "uri": "/v1/{registration.name=projects/*/locations/*/registrations/*}",
                    "body": "registration",
                },
            ]
            request, metadata = self._interceptor.pre_update_registration(
                request, metadata
            )
            pb_request = domains.UpdateRegistrationRequest.pb(request)
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
            resp = self._interceptor.post_update_registration(resp)
            return resp

    @property
    def configure_contact_settings(
        self,
    ) -> Callable[[domains.ConfigureContactSettingsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ConfigureContactSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def configure_dns_settings(
        self,
    ) -> Callable[[domains.ConfigureDnsSettingsRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ConfigureDnsSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def configure_management_settings(
        self,
    ) -> Callable[
        [domains.ConfigureManagementSettingsRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ConfigureManagementSettings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_registration(
        self,
    ) -> Callable[[domains.DeleteRegistrationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRegistration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def export_registration(
        self,
    ) -> Callable[[domains.ExportRegistrationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ExportRegistration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_registration(
        self,
    ) -> Callable[[domains.GetRegistrationRequest], domains.Registration]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRegistration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_registrations(
        self,
    ) -> Callable[
        [domains.ListRegistrationsRequest], domains.ListRegistrationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRegistrations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def register_domain(
        self,
    ) -> Callable[[domains.RegisterDomainRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RegisterDomain(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reset_authorization_code(
        self,
    ) -> Callable[[domains.ResetAuthorizationCodeRequest], domains.AuthorizationCode]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResetAuthorizationCode(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def retrieve_authorization_code(
        self,
    ) -> Callable[
        [domains.RetrieveAuthorizationCodeRequest], domains.AuthorizationCode
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetrieveAuthorizationCode(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def retrieve_register_parameters(
        self,
    ) -> Callable[
        [domains.RetrieveRegisterParametersRequest],
        domains.RetrieveRegisterParametersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetrieveRegisterParameters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def retrieve_transfer_parameters(
        self,
    ) -> Callable[
        [domains.RetrieveTransferParametersRequest],
        domains.RetrieveTransferParametersResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetrieveTransferParameters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def search_domains(
        self,
    ) -> Callable[[domains.SearchDomainsRequest], domains.SearchDomainsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SearchDomains(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def transfer_domain(
        self,
    ) -> Callable[[domains.TransferDomainRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TransferDomain(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_registration(
        self,
    ) -> Callable[[domains.UpdateRegistrationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRegistration(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("DomainsRestTransport",)
