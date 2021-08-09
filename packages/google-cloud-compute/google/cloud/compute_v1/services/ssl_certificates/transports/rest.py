# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import gapic_v1  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.auth.transport.requests import AuthorizedSession

from google.cloud.compute_v1.types import compute

from .base import SslCertificatesTransport, DEFAULT_CLIENT_INFO


class SslCertificatesRestTransport(SslCertificatesTransport):
    """REST backend transport for SslCertificates.

    The SslCertificates API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._prep_wrapped_messages(client_info)

    def aggregated_list(
        self,
        request: compute.AggregatedListSslCertificatesRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SslCertificateAggregatedList:
        r"""Call the aggregated list method over HTTP.

        Args:
            request (~.compute.AggregatedListSslCertificatesRequest):
                The request object. A request message for
                SslCertificates.AggregatedList. See the
                method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.SslCertificateAggregatedList:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/aggregated/sslCertificates".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.AggregatedListSslCertificatesRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.AggregatedListSslCertificatesRequest.include_all_scopes in request:
            query_params["includeAllScopes"] = request.include_all_scopes
        if compute.AggregatedListSslCertificatesRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.AggregatedListSslCertificatesRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.AggregatedListSslCertificatesRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if (
            compute.AggregatedListSslCertificatesRequest.return_partial_success
            in request
        ):
            query_params["returnPartialSuccess"] = request.return_partial_success

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.get(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.SslCertificateAggregatedList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def delete(
        self,
        request: compute.DeleteSslCertificateRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the delete method over HTTP.

        Args:
            request (~.compute.DeleteSslCertificateRequest):
                The request object. A request message for
                SslCertificates.Delete. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource.

                Google Compute Engine has three Operation resources:

                -  `Global </compute/docs/reference/rest/{$api_version}/globalOperations>`__
                   \*
                   `Regional </compute/docs/reference/rest/{$api_version}/regionOperations>`__
                   \*
                   `Zonal </compute/docs/reference/rest/{$api_version}/zoneOperations>`__

                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses.

                Operations can be global, regional or zonal.

                -  For global operations, use the ``globalOperations``
                   resource.
                -  For regional operations, use the ``regionOperations``
                   resource.
                -  For zonal operations, use the ``zonalOperations``
                   resource.

                For more information, read Global, Regional, and Zonal
                Resources. (== resource_for
                {$api_version}.globalOperations ==) (== resource_for
                {$api_version}.regionOperations ==) (== resource_for
                {$api_version}.zoneOperations ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/sslCertificates/{ssl_certificate}".format(
            host=self._host,
            project=request.project,
            ssl_certificate=request.ssl_certificate,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.DeleteSslCertificateRequest.request_id in request:
            query_params["requestId"] = request.request_id

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.delete(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def get(
        self,
        request: compute.GetSslCertificateRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SslCertificate:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetSslCertificateRequest):
                The request object. A request message for
                SslCertificates.Get. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.SslCertificate:
                Represents an SSL Certificate resource.

                Google Compute Engine has two SSL Certificate resources:

                -  `Global </compute/docs/reference/rest/{$api_version}/sslCertificates>`__
                   \*
                   `Regional </compute/docs/reference/rest/{$api_version}/regionSslCertificates>`__

                The sslCertificates are used by:

                -  external HTTPS load balancers
                -  SSL proxy load balancers

                The regionSslCertificates are used by internal HTTPS
                load balancers.

                Optionally, certificate file contents that you upload
                can contain a set of up to five PEM-encoded
                certificates. The API call creates an object
                (sslCertificate) that holds this data. You can use SSL
                keys and certificates to secure connections to a load
                balancer. For more information, read Creating and using
                SSL certificates, SSL certificates quotas and limits,
                and Troubleshooting SSL certificates. (== resource_for
                {$api_version}.sslCertificates ==) (== resource_for
                {$api_version}.regionSslCertificates ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/sslCertificates/{ssl_certificate}".format(
            host=self._host,
            project=request.project,
            ssl_certificate=request.ssl_certificate,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.get(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.SslCertificate.from_json(
            response.content, ignore_unknown_fields=True
        )

    def insert(
        self,
        request: compute.InsertSslCertificateRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.Operation:
        r"""Call the insert method over HTTP.

        Args:
            request (~.compute.InsertSslCertificateRequest):
                The request object. A request message for
                SslCertificates.Insert. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.Operation:
                Represents an Operation resource.

                Google Compute Engine has three Operation resources:

                -  `Global </compute/docs/reference/rest/{$api_version}/globalOperations>`__
                   \*
                   `Regional </compute/docs/reference/rest/{$api_version}/regionOperations>`__
                   \*
                   `Zonal </compute/docs/reference/rest/{$api_version}/zoneOperations>`__

                You can use an operation resource to manage asynchronous
                API requests. For more information, read Handling API
                responses.

                Operations can be global, regional or zonal.

                -  For global operations, use the ``globalOperations``
                   resource.
                -  For regional operations, use the ``regionOperations``
                   resource.
                -  For zonal operations, use the ``zonalOperations``
                   resource.

                For more information, read Global, Regional, and Zonal
                Resources. (== resource_for
                {$api_version}.globalOperations ==) (== resource_for
                {$api_version}.regionOperations ==) (== resource_for
                {$api_version}.zoneOperations ==)

        """

        # Jsonify the request body
        body = compute.SslCertificate.to_json(
            request.ssl_certificate_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        )

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/sslCertificates".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.InsertSslCertificateRequest.request_id in request:
            query_params["requestId"] = request.request_id

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.post(
            url, headers=headers, params=query_params, data=body,
        )

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.Operation.from_json(response.content, ignore_unknown_fields=True)

    def list(
        self,
        request: compute.ListSslCertificatesRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.SslCertificateList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListSslCertificatesRequest):
                The request object. A request message for
                SslCertificates.List. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.SslCertificateList:
                Contains a list of SslCertificate
                resources.

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/global/sslCertificates".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListSslCertificatesRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListSslCertificatesRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListSslCertificatesRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListSslCertificatesRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.ListSslCertificatesRequest.return_partial_success in request:
            query_params["returnPartialSuccess"] = request.return_partial_success

        # Send the request
        headers = dict(metadata)
        headers["Content-Type"] = "application/json"
        response = self._session.get(url, headers=headers, params=query_params,)

        # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
        # subclass.
        if response.status_code >= 400:
            raise core_exceptions.from_http_response(response)

        # Return the response
        return compute.SslCertificateList.from_json(
            response.content, ignore_unknown_fields=True
        )


__all__ = ("SslCertificatesRestTransport",)
