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

from google.api_core import gapic_v1, path_template, rest_helpers, rest_streaming
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


from google.protobuf import empty_pb2  # type: ignore

from google.cloud.appengine_admin_v1.types import appengine, certificate

from .base import AuthorizedCertificatesTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class AuthorizedCertificatesRestInterceptor:
    """Interceptor for AuthorizedCertificates.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the AuthorizedCertificatesRestTransport.

    .. code-block:: python
        class MyCustomAuthorizedCertificatesInterceptor(AuthorizedCertificatesRestInterceptor):
            def pre_create_authorized_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_authorized_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_authorized_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_authorized_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_authorized_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_authorized_certificates(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_authorized_certificates(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_authorized_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_authorized_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = AuthorizedCertificatesRestTransport(interceptor=MyCustomAuthorizedCertificatesInterceptor())
        client = AuthorizedCertificatesClient(transport=transport)


    """

    def pre_create_authorized_certificate(
        self,
        request: appengine.CreateAuthorizedCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.CreateAuthorizedCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_authorized_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AuthorizedCertificates server.
        """
        return request, metadata

    def post_create_authorized_certificate(
        self, response: certificate.AuthorizedCertificate
    ) -> certificate.AuthorizedCertificate:
        """Post-rpc interceptor for create_authorized_certificate

        Override in a subclass to manipulate the response
        after it is returned by the AuthorizedCertificates server but before
        it is returned to user code.
        """
        return response

    def pre_delete_authorized_certificate(
        self,
        request: appengine.DeleteAuthorizedCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.DeleteAuthorizedCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_authorized_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AuthorizedCertificates server.
        """
        return request, metadata

    def pre_get_authorized_certificate(
        self,
        request: appengine.GetAuthorizedCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.GetAuthorizedCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_authorized_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AuthorizedCertificates server.
        """
        return request, metadata

    def post_get_authorized_certificate(
        self, response: certificate.AuthorizedCertificate
    ) -> certificate.AuthorizedCertificate:
        """Post-rpc interceptor for get_authorized_certificate

        Override in a subclass to manipulate the response
        after it is returned by the AuthorizedCertificates server but before
        it is returned to user code.
        """
        return response

    def pre_list_authorized_certificates(
        self,
        request: appengine.ListAuthorizedCertificatesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.ListAuthorizedCertificatesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_authorized_certificates

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AuthorizedCertificates server.
        """
        return request, metadata

    def post_list_authorized_certificates(
        self, response: appengine.ListAuthorizedCertificatesResponse
    ) -> appengine.ListAuthorizedCertificatesResponse:
        """Post-rpc interceptor for list_authorized_certificates

        Override in a subclass to manipulate the response
        after it is returned by the AuthorizedCertificates server but before
        it is returned to user code.
        """
        return response

    def pre_update_authorized_certificate(
        self,
        request: appengine.UpdateAuthorizedCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[appengine.UpdateAuthorizedCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_authorized_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the AuthorizedCertificates server.
        """
        return request, metadata

    def post_update_authorized_certificate(
        self, response: certificate.AuthorizedCertificate
    ) -> certificate.AuthorizedCertificate:
        """Post-rpc interceptor for update_authorized_certificate

        Override in a subclass to manipulate the response
        after it is returned by the AuthorizedCertificates server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class AuthorizedCertificatesRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: AuthorizedCertificatesRestInterceptor


class AuthorizedCertificatesRestTransport(AuthorizedCertificatesTransport):
    """REST backend transport for AuthorizedCertificates.

    Manages SSL certificates a user is authorized to administer.
    A user can administer any SSL certificates applicable to their
    authorized domains.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "appengine.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[AuthorizedCertificatesRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'appengine.googleapis.com').
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
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or AuthorizedCertificatesRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _CreateAuthorizedCertificate(AuthorizedCertificatesRestStub):
        def __hash__(self):
            return hash("CreateAuthorizedCertificate")

        def __call__(
            self,
            request: appengine.CreateAuthorizedCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> certificate.AuthorizedCertificate:
            r"""Call the create authorized
            certificate method over HTTP.

                Args:
                    request (~.appengine.CreateAuthorizedCertificateRequest):
                        The request object. Request message for
                    ``AuthorizedCertificates.CreateAuthorizedCertificate``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.certificate.AuthorizedCertificate:
                        An SSL certificate that a user has
                    been authorized to administer. A user is
                    authorized to administer any certificate
                    that applies to one of their authorized
                    domains.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=apps/*}/authorizedCertificates",
                    "body": "certificate",
                },
            ]
            request, metadata = self._interceptor.pre_create_authorized_certificate(
                request, metadata
            )
            pb_request = appengine.CreateAuthorizedCertificateRequest.pb(request)
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
            resp = certificate.AuthorizedCertificate()
            pb_resp = certificate.AuthorizedCertificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_authorized_certificate(resp)
            return resp

    class _DeleteAuthorizedCertificate(AuthorizedCertificatesRestStub):
        def __hash__(self):
            return hash("DeleteAuthorizedCertificate")

        def __call__(
            self,
            request: appengine.DeleteAuthorizedCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete authorized
            certificate method over HTTP.

                Args:
                    request (~.appengine.DeleteAuthorizedCertificateRequest):
                        The request object. Request message for
                    ``AuthorizedCertificates.DeleteAuthorizedCertificate``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=apps/*/authorizedCertificates/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_authorized_certificate(
                request, metadata
            )
            pb_request = appengine.DeleteAuthorizedCertificateRequest.pb(request)
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

    class _GetAuthorizedCertificate(AuthorizedCertificatesRestStub):
        def __hash__(self):
            return hash("GetAuthorizedCertificate")

        def __call__(
            self,
            request: appengine.GetAuthorizedCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> certificate.AuthorizedCertificate:
            r"""Call the get authorized
            certificate method over HTTP.

                Args:
                    request (~.appengine.GetAuthorizedCertificateRequest):
                        The request object. Request message for
                    ``AuthorizedCertificates.GetAuthorizedCertificate``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.certificate.AuthorizedCertificate:
                        An SSL certificate that a user has
                    been authorized to administer. A user is
                    authorized to administer any certificate
                    that applies to one of their authorized
                    domains.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=apps/*/authorizedCertificates/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_authorized_certificate(
                request, metadata
            )
            pb_request = appengine.GetAuthorizedCertificateRequest.pb(request)
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
            resp = certificate.AuthorizedCertificate()
            pb_resp = certificate.AuthorizedCertificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_authorized_certificate(resp)
            return resp

    class _ListAuthorizedCertificates(AuthorizedCertificatesRestStub):
        def __hash__(self):
            return hash("ListAuthorizedCertificates")

        def __call__(
            self,
            request: appengine.ListAuthorizedCertificatesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> appengine.ListAuthorizedCertificatesResponse:
            r"""Call the list authorized
            certificates method over HTTP.

                Args:
                    request (~.appengine.ListAuthorizedCertificatesRequest):
                        The request object. Request message for
                    ``AuthorizedCertificates.ListAuthorizedCertificates``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.appengine.ListAuthorizedCertificatesResponse:
                        Response message for
                    ``AuthorizedCertificates.ListAuthorizedCertificates``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=apps/*}/authorizedCertificates",
                },
            ]
            request, metadata = self._interceptor.pre_list_authorized_certificates(
                request, metadata
            )
            pb_request = appengine.ListAuthorizedCertificatesRequest.pb(request)
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
            resp = appengine.ListAuthorizedCertificatesResponse()
            pb_resp = appengine.ListAuthorizedCertificatesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_authorized_certificates(resp)
            return resp

    class _UpdateAuthorizedCertificate(AuthorizedCertificatesRestStub):
        def __hash__(self):
            return hash("UpdateAuthorizedCertificate")

        def __call__(
            self,
            request: appengine.UpdateAuthorizedCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> certificate.AuthorizedCertificate:
            r"""Call the update authorized
            certificate method over HTTP.

                Args:
                    request (~.appengine.UpdateAuthorizedCertificateRequest):
                        The request object. Request message for
                    ``AuthorizedCertificates.UpdateAuthorizedCertificate``.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.certificate.AuthorizedCertificate:
                        An SSL certificate that a user has
                    been authorized to administer. A user is
                    authorized to administer any certificate
                    that applies to one of their authorized
                    domains.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{name=apps/*/authorizedCertificates/*}",
                    "body": "certificate",
                },
            ]
            request, metadata = self._interceptor.pre_update_authorized_certificate(
                request, metadata
            )
            pb_request = appengine.UpdateAuthorizedCertificateRequest.pb(request)
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
            resp = certificate.AuthorizedCertificate()
            pb_resp = certificate.AuthorizedCertificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_authorized_certificate(resp)
            return resp

    @property
    def create_authorized_certificate(
        self,
    ) -> Callable[
        [appengine.CreateAuthorizedCertificateRequest],
        certificate.AuthorizedCertificate,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAuthorizedCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_authorized_certificate(
        self,
    ) -> Callable[[appengine.DeleteAuthorizedCertificateRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAuthorizedCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_authorized_certificate(
        self,
    ) -> Callable[
        [appengine.GetAuthorizedCertificateRequest], certificate.AuthorizedCertificate
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAuthorizedCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_authorized_certificates(
        self,
    ) -> Callable[
        [appengine.ListAuthorizedCertificatesRequest],
        appengine.ListAuthorizedCertificatesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAuthorizedCertificates(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_authorized_certificate(
        self,
    ) -> Callable[
        [appengine.UpdateAuthorizedCertificateRequest],
        certificate.AuthorizedCertificate,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAuthorizedCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("AuthorizedCertificatesRestTransport",)
