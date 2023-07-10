# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.security.privateca_v1.types import resources, service

from .base import CertificateAuthorityServiceTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class CertificateAuthorityServiceRestInterceptor:
    """Interceptor for CertificateAuthorityService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CertificateAuthorityServiceRestTransport.

    .. code-block:: python
        class MyCustomCertificateAuthorityServiceInterceptor(CertificateAuthorityServiceRestInterceptor):
            def pre_activate_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_activate_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_ca_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_ca_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_certificate_template(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_certificate_template(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_ca_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_ca_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_certificate_template(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_certificate_template(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_disable_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_disable_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enable_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enable_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_ca_certs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_ca_certs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_fetch_certificate_authority_csr(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_fetch_certificate_authority_csr(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_ca_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_ca_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_certificate_revocation_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_certificate_revocation_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_certificate_template(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_certificate_template(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_ca_pools(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_ca_pools(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_certificate_authorities(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_certificate_authorities(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_certificate_revocation_lists(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_certificate_revocation_lists(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_certificates(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_certificates(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_certificate_templates(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_certificate_templates(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_revoke_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_revoke_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_undelete_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_undelete_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_ca_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_ca_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_certificate(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_certificate(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_certificate_authority(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_certificate_authority(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_certificate_revocation_list(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_certificate_revocation_list(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_certificate_template(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_certificate_template(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CertificateAuthorityServiceRestTransport(interceptor=MyCustomCertificateAuthorityServiceInterceptor())
        client = CertificateAuthorityServiceClient(transport=transport)


    """

    def pre_activate_certificate_authority(
        self,
        request: service.ActivateCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ActivateCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for activate_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_activate_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for activate_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_create_ca_pool(
        self, request: service.CreateCaPoolRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateCaPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_ca_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_create_ca_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_ca_pool

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_create_certificate(
        self,
        request: service.CreateCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_create_certificate(
        self, response: resources.Certificate
    ) -> resources.Certificate:
        """Post-rpc interceptor for create_certificate

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_create_certificate_authority(
        self,
        request: service.CreateCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_create_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_create_certificate_template(
        self,
        request: service.CreateCertificateTemplateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateCertificateTemplateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_certificate_template

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_create_certificate_template(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_certificate_template

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_ca_pool(
        self, request: service.DeleteCaPoolRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteCaPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_ca_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_delete_ca_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_ca_pool

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_certificate_authority(
        self,
        request: service.DeleteCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DeleteCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_delete_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_certificate_template(
        self,
        request: service.DeleteCertificateTemplateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DeleteCertificateTemplateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_certificate_template

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_delete_certificate_template(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_certificate_template

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_disable_certificate_authority(
        self,
        request: service.DisableCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DisableCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for disable_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_disable_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for disable_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_enable_certificate_authority(
        self,
        request: service.EnableCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.EnableCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for enable_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_enable_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for enable_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_ca_certs(
        self, request: service.FetchCaCertsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.FetchCaCertsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_ca_certs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_fetch_ca_certs(
        self, response: service.FetchCaCertsResponse
    ) -> service.FetchCaCertsResponse:
        """Post-rpc interceptor for fetch_ca_certs

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_fetch_certificate_authority_csr(
        self,
        request: service.FetchCertificateAuthorityCsrRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.FetchCertificateAuthorityCsrRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for fetch_certificate_authority_csr

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_fetch_certificate_authority_csr(
        self, response: service.FetchCertificateAuthorityCsrResponse
    ) -> service.FetchCertificateAuthorityCsrResponse:
        """Post-rpc interceptor for fetch_certificate_authority_csr

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_ca_pool(
        self, request: service.GetCaPoolRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetCaPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_ca_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_ca_pool(self, response: resources.CaPool) -> resources.CaPool:
        """Post-rpc interceptor for get_ca_pool

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_certificate(
        self,
        request: service.GetCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_certificate(
        self, response: resources.Certificate
    ) -> resources.Certificate:
        """Post-rpc interceptor for get_certificate

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_certificate_authority(
        self,
        request: service.GetCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_certificate_authority(
        self, response: resources.CertificateAuthority
    ) -> resources.CertificateAuthority:
        """Post-rpc interceptor for get_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_certificate_revocation_list(
        self,
        request: service.GetCertificateRevocationListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetCertificateRevocationListRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_certificate_revocation_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_certificate_revocation_list(
        self, response: resources.CertificateRevocationList
    ) -> resources.CertificateRevocationList:
        """Post-rpc interceptor for get_certificate_revocation_list

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_certificate_template(
        self,
        request: service.GetCertificateTemplateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetCertificateTemplateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_certificate_template

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_certificate_template(
        self, response: resources.CertificateTemplate
    ) -> resources.CertificateTemplate:
        """Post-rpc interceptor for get_certificate_template

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_list_ca_pools(
        self, request: service.ListCaPoolsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListCaPoolsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_ca_pools

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_ca_pools(
        self, response: service.ListCaPoolsResponse
    ) -> service.ListCaPoolsResponse:
        """Post-rpc interceptor for list_ca_pools

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_list_certificate_authorities(
        self,
        request: service.ListCertificateAuthoritiesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListCertificateAuthoritiesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_certificate_authorities

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_certificate_authorities(
        self, response: service.ListCertificateAuthoritiesResponse
    ) -> service.ListCertificateAuthoritiesResponse:
        """Post-rpc interceptor for list_certificate_authorities

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_list_certificate_revocation_lists(
        self,
        request: service.ListCertificateRevocationListsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        service.ListCertificateRevocationListsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_certificate_revocation_lists

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_certificate_revocation_lists(
        self, response: service.ListCertificateRevocationListsResponse
    ) -> service.ListCertificateRevocationListsResponse:
        """Post-rpc interceptor for list_certificate_revocation_lists

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_list_certificates(
        self,
        request: service.ListCertificatesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListCertificatesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_certificates

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_certificates(
        self, response: service.ListCertificatesResponse
    ) -> service.ListCertificatesResponse:
        """Post-rpc interceptor for list_certificates

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_list_certificate_templates(
        self,
        request: service.ListCertificateTemplatesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListCertificateTemplatesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_certificate_templates

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_certificate_templates(
        self, response: service.ListCertificateTemplatesResponse
    ) -> service.ListCertificateTemplatesResponse:
        """Post-rpc interceptor for list_certificate_templates

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_revoke_certificate(
        self,
        request: service.RevokeCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.RevokeCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for revoke_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_revoke_certificate(
        self, response: resources.Certificate
    ) -> resources.Certificate:
        """Post-rpc interceptor for revoke_certificate

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_undelete_certificate_authority(
        self,
        request: service.UndeleteCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UndeleteCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for undelete_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_undelete_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for undelete_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_update_ca_pool(
        self, request: service.UpdateCaPoolRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateCaPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_ca_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_update_ca_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_ca_pool

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_update_certificate(
        self,
        request: service.UpdateCertificateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateCertificateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_certificate

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_update_certificate(
        self, response: resources.Certificate
    ) -> resources.Certificate:
        """Post-rpc interceptor for update_certificate

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_update_certificate_authority(
        self,
        request: service.UpdateCertificateAuthorityRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateCertificateAuthorityRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_certificate_authority

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_update_certificate_authority(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_certificate_authority

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_update_certificate_revocation_list(
        self,
        request: service.UpdateCertificateRevocationListRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        service.UpdateCertificateRevocationListRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_certificate_revocation_list

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_update_certificate_revocation_list(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_certificate_revocation_list

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_update_certificate_template(
        self,
        request: service.UpdateCertificateTemplateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateCertificateTemplateRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_certificate_template

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_update_certificate_template(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_certificate_template

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
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
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
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
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
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
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
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
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
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
        before they are sent to the CertificateAuthorityService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the CertificateAuthorityService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CertificateAuthorityServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CertificateAuthorityServiceRestInterceptor


class CertificateAuthorityServiceRestTransport(CertificateAuthorityServiceTransport):
    """REST backend transport for CertificateAuthorityService.

    [Certificate Authority
    Service][google.cloud.security.privateca.v1.CertificateAuthorityService]
    manages private certificate authorities and issued certificates.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "privateca.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CertificateAuthorityServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
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
        self._interceptor = interceptor or CertificateAuthorityServiceRestInterceptor()
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
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
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

    class _ActivateCertificateAuthority(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("ActivateCertificateAuthority")

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
            request: service.ActivateCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the activate certificate
            authority method over HTTP.

                Args:
                    request (~.service.ActivateCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.ActivateCertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthorityService.ActivateCertificateAuthority].
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
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificateAuthorities/*}:activate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_activate_certificate_authority(
                request, metadata
            )
            pb_request = service.ActivateCertificateAuthorityRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_activate_certificate_authority(resp)
            return resp

    class _CreateCaPool(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("CreateCaPool")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "caPoolId": "",
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
            request: service.CreateCaPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create ca pool method over HTTP.

            Args:
                request (~.service.CreateCaPoolRequest):
                    The request object. Request message for
                [CertificateAuthorityService.CreateCaPool][google.cloud.security.privateca.v1.CertificateAuthorityService.CreateCaPool].
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
                    "uri": "/v1/{parent=projects/*/locations/*}/caPools",
                    "body": "ca_pool",
                },
            ]
            request, metadata = self._interceptor.pre_create_ca_pool(request, metadata)
            pb_request = service.CreateCaPoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_create_ca_pool(resp)
            return resp

    class _CreateCertificate(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("CreateCertificate")

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
            request: service.CreateCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Certificate:
            r"""Call the create certificate method over HTTP.

            Args:
                request (~.service.CreateCertificateRequest):
                    The request object. Request message for
                [CertificateAuthorityService.CreateCertificate][google.cloud.security.privateca.v1.CertificateAuthorityService.CreateCertificate].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Certificate:
                    A
                [Certificate][google.cloud.security.privateca.v1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/caPools/*}/certificates",
                    "body": "certificate",
                },
            ]
            request, metadata = self._interceptor.pre_create_certificate(
                request, metadata
            )
            pb_request = service.CreateCertificateRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.Certificate()
            pb_resp = resources.Certificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_certificate(resp)
            return resp

    class _CreateCertificateAuthority(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("CreateCertificateAuthority")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "certificateAuthorityId": "",
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
            request: service.CreateCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create certificate
            authority method over HTTP.

                Args:
                    request (~.service.CreateCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.CreateCertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthorityService.CreateCertificateAuthority].
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
                    "uri": "/v1/{parent=projects/*/locations/*/caPools/*}/certificateAuthorities",
                    "body": "certificate_authority",
                },
            ]
            request, metadata = self._interceptor.pre_create_certificate_authority(
                request, metadata
            )
            pb_request = service.CreateCertificateAuthorityRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_create_certificate_authority(resp)
            return resp

    class _CreateCertificateTemplate(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("CreateCertificateTemplate")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "certificateTemplateId": "",
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
            request: service.CreateCertificateTemplateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create certificate
            template method over HTTP.

                Args:
                    request (~.service.CreateCertificateTemplateRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.CreateCertificateTemplate][google.cloud.security.privateca.v1.CertificateAuthorityService.CreateCertificateTemplate].
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
                    "uri": "/v1/{parent=projects/*/locations/*}/certificateTemplates",
                    "body": "certificate_template",
                },
            ]
            request, metadata = self._interceptor.pre_create_certificate_template(
                request, metadata
            )
            pb_request = service.CreateCertificateTemplateRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_create_certificate_template(resp)
            return resp

    class _DeleteCaPool(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("DeleteCaPool")

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
            request: service.DeleteCaPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete ca pool method over HTTP.

            Args:
                request (~.service.DeleteCaPoolRequest):
                    The request object. Request message for
                [CertificateAuthorityService.DeleteCaPool][google.cloud.security.privateca.v1.CertificateAuthorityService.DeleteCaPool].
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
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_ca_pool(request, metadata)
            pb_request = service.DeleteCaPoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_delete_ca_pool(resp)
            return resp

    class _DeleteCertificateAuthority(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("DeleteCertificateAuthority")

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
            request: service.DeleteCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete certificate
            authority method over HTTP.

                Args:
                    request (~.service.DeleteCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.DeleteCertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthorityService.DeleteCertificateAuthority].
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
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificateAuthorities/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_certificate_authority(
                request, metadata
            )
            pb_request = service.DeleteCertificateAuthorityRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_delete_certificate_authority(resp)
            return resp

    class _DeleteCertificateTemplate(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("DeleteCertificateTemplate")

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
            request: service.DeleteCertificateTemplateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete certificate
            template method over HTTP.

                Args:
                    request (~.service.DeleteCertificateTemplateRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.DeleteCertificateTemplate][google.cloud.security.privateca.v1.CertificateAuthorityService.DeleteCertificateTemplate].
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
                    "uri": "/v1/{name=projects/*/locations/*/certificateTemplates/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_certificate_template(
                request, metadata
            )
            pb_request = service.DeleteCertificateTemplateRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_delete_certificate_template(resp)
            return resp

    class _DisableCertificateAuthority(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("DisableCertificateAuthority")

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
            request: service.DisableCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the disable certificate
            authority method over HTTP.

                Args:
                    request (~.service.DisableCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.DisableCertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthorityService.DisableCertificateAuthority].
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
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificateAuthorities/*}:disable",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_disable_certificate_authority(
                request, metadata
            )
            pb_request = service.DisableCertificateAuthorityRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_disable_certificate_authority(resp)
            return resp

    class _EnableCertificateAuthority(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("EnableCertificateAuthority")

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
            request: service.EnableCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the enable certificate
            authority method over HTTP.

                Args:
                    request (~.service.EnableCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.EnableCertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthorityService.EnableCertificateAuthority].
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
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificateAuthorities/*}:enable",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_enable_certificate_authority(
                request, metadata
            )
            pb_request = service.EnableCertificateAuthorityRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_enable_certificate_authority(resp)
            return resp

    class _FetchCaCerts(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("FetchCaCerts")

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
            request: service.FetchCaCertsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.FetchCaCertsResponse:
            r"""Call the fetch ca certs method over HTTP.

            Args:
                request (~.service.FetchCaCertsRequest):
                    The request object. Request message for
                [CertificateAuthorityService.FetchCaCerts][google.cloud.security.privateca.v1.CertificateAuthorityService.FetchCaCerts].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.FetchCaCertsResponse:
                    Response message for
                [CertificateAuthorityService.FetchCaCerts][google.cloud.security.privateca.v1.CertificateAuthorityService.FetchCaCerts].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{ca_pool=projects/*/locations/*/caPools/*}:fetchCaCerts",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_ca_certs(request, metadata)
            pb_request = service.FetchCaCertsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.FetchCaCertsResponse()
            pb_resp = service.FetchCaCertsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_ca_certs(resp)
            return resp

    class _FetchCertificateAuthorityCsr(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("FetchCertificateAuthorityCsr")

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
            request: service.FetchCertificateAuthorityCsrRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.FetchCertificateAuthorityCsrResponse:
            r"""Call the fetch certificate
            authority csr method over HTTP.

                Args:
                    request (~.service.FetchCertificateAuthorityCsrRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.FetchCertificateAuthorityCsr][google.cloud.security.privateca.v1.CertificateAuthorityService.FetchCertificateAuthorityCsr].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.FetchCertificateAuthorityCsrResponse:
                        Response message for
                    [CertificateAuthorityService.FetchCertificateAuthorityCsr][google.cloud.security.privateca.v1.CertificateAuthorityService.FetchCertificateAuthorityCsr].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificateAuthorities/*}:fetch",
                },
            ]
            request, metadata = self._interceptor.pre_fetch_certificate_authority_csr(
                request, metadata
            )
            pb_request = service.FetchCertificateAuthorityCsrRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.FetchCertificateAuthorityCsrResponse()
            pb_resp = service.FetchCertificateAuthorityCsrResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_fetch_certificate_authority_csr(resp)
            return resp

    class _GetCaPool(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("GetCaPool")

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
            request: service.GetCaPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CaPool:
            r"""Call the get ca pool method over HTTP.

            Args:
                request (~.service.GetCaPoolRequest):
                    The request object. Request message for
                [CertificateAuthorityService.GetCaPool][google.cloud.security.privateca.v1.CertificateAuthorityService.GetCaPool].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CaPool:
                    A [CaPool][google.cloud.security.privateca.v1.CaPool]
                represents a group of
                [CertificateAuthorities][google.cloud.security.privateca.v1.CertificateAuthority]
                that form a trust anchor. A
                [CaPool][google.cloud.security.privateca.v1.CaPool] can
                be used to manage issuance policies for one or more
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
                resources and to rotate CA certificates in and out of
                the trust anchor.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_ca_pool(request, metadata)
            pb_request = service.GetCaPoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.CaPool()
            pb_resp = resources.CaPool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_ca_pool(resp)
            return resp

    class _GetCertificate(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("GetCertificate")

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
            request: service.GetCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Certificate:
            r"""Call the get certificate method over HTTP.

            Args:
                request (~.service.GetCertificateRequest):
                    The request object. Request message for
                [CertificateAuthorityService.GetCertificate][google.cloud.security.privateca.v1.CertificateAuthorityService.GetCertificate].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Certificate:
                    A
                [Certificate][google.cloud.security.privateca.v1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificates/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_certificate(request, metadata)
            pb_request = service.GetCertificateRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.Certificate()
            pb_resp = resources.Certificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_certificate(resp)
            return resp

    class _GetCertificateAuthority(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("GetCertificateAuthority")

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
            request: service.GetCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CertificateAuthority:
            r"""Call the get certificate authority method over HTTP.

            Args:
                request (~.service.GetCertificateAuthorityRequest):
                    The request object. Request message for
                [CertificateAuthorityService.GetCertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthorityService.GetCertificateAuthority].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CertificateAuthority:
                    A
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
                represents an individual Certificate Authority. A
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
                can be used to create
                [Certificates][google.cloud.security.privateca.v1.Certificate].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificateAuthorities/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_certificate_authority(
                request, metadata
            )
            pb_request = service.GetCertificateAuthorityRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.CertificateAuthority()
            pb_resp = resources.CertificateAuthority.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_certificate_authority(resp)
            return resp

    class _GetCertificateRevocationList(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("GetCertificateRevocationList")

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
            request: service.GetCertificateRevocationListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CertificateRevocationList:
            r"""Call the get certificate
            revocation list method over HTTP.

                Args:
                    request (~.service.GetCertificateRevocationListRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.GetCertificateRevocationList][google.cloud.security.privateca.v1.CertificateAuthorityService.GetCertificateRevocationList].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.CertificateRevocationList:
                        A
                    [CertificateRevocationList][google.cloud.security.privateca.v1.CertificateRevocationList]
                    corresponds to a signed X.509 certificate Revocation
                    List (CRL). A CRL contains the serial numbers of
                    certificates that should no longer be trusted.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificateAuthorities/*/certificateRevocationLists/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_certificate_revocation_list(
                request, metadata
            )
            pb_request = service.GetCertificateRevocationListRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.CertificateRevocationList()
            pb_resp = resources.CertificateRevocationList.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_certificate_revocation_list(resp)
            return resp

    class _GetCertificateTemplate(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("GetCertificateTemplate")

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
            request: service.GetCertificateTemplateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CertificateTemplate:
            r"""Call the get certificate template method over HTTP.

            Args:
                request (~.service.GetCertificateTemplateRequest):
                    The request object. Request message for
                [CertificateAuthorityService.GetCertificateTemplate][google.cloud.security.privateca.v1.CertificateAuthorityService.GetCertificateTemplate].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CertificateTemplate:
                    A
                [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate]
                refers to a managed template for certificate issuance.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/certificateTemplates/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_certificate_template(
                request, metadata
            )
            pb_request = service.GetCertificateTemplateRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.CertificateTemplate()
            pb_resp = resources.CertificateTemplate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_certificate_template(resp)
            return resp

    class _ListCaPools(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("ListCaPools")

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
            request: service.ListCaPoolsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCaPoolsResponse:
            r"""Call the list ca pools method over HTTP.

            Args:
                request (~.service.ListCaPoolsRequest):
                    The request object. Request message for
                [CertificateAuthorityService.ListCaPools][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCaPools].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListCaPoolsResponse:
                    Response message for
                [CertificateAuthorityService.ListCaPools][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCaPools].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/caPools",
                },
            ]
            request, metadata = self._interceptor.pre_list_ca_pools(request, metadata)
            pb_request = service.ListCaPoolsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.ListCaPoolsResponse()
            pb_resp = service.ListCaPoolsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_ca_pools(resp)
            return resp

    class _ListCertificateAuthorities(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("ListCertificateAuthorities")

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
            request: service.ListCertificateAuthoritiesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCertificateAuthoritiesResponse:
            r"""Call the list certificate
            authorities method over HTTP.

                Args:
                    request (~.service.ListCertificateAuthoritiesRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.ListCertificateAuthorities][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCertificateAuthorities].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.ListCertificateAuthoritiesResponse:
                        Response message for
                    [CertificateAuthorityService.ListCertificateAuthorities][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCertificateAuthorities].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/caPools/*}/certificateAuthorities",
                },
            ]
            request, metadata = self._interceptor.pre_list_certificate_authorities(
                request, metadata
            )
            pb_request = service.ListCertificateAuthoritiesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.ListCertificateAuthoritiesResponse()
            pb_resp = service.ListCertificateAuthoritiesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_certificate_authorities(resp)
            return resp

    class _ListCertificateRevocationLists(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("ListCertificateRevocationLists")

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
            request: service.ListCertificateRevocationListsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCertificateRevocationListsResponse:
            r"""Call the list certificate
            revocation lists method over HTTP.

                Args:
                    request (~.service.ListCertificateRevocationListsRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.ListCertificateRevocationLists][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCertificateRevocationLists].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.ListCertificateRevocationListsResponse:
                        Response message for
                    [CertificateAuthorityService.ListCertificateRevocationLists][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCertificateRevocationLists].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/caPools/*/certificateAuthorities/*}/certificateRevocationLists",
                },
            ]
            request, metadata = self._interceptor.pre_list_certificate_revocation_lists(
                request, metadata
            )
            pb_request = service.ListCertificateRevocationListsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.ListCertificateRevocationListsResponse()
            pb_resp = service.ListCertificateRevocationListsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_certificate_revocation_lists(resp)
            return resp

    class _ListCertificates(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("ListCertificates")

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
            request: service.ListCertificatesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCertificatesResponse:
            r"""Call the list certificates method over HTTP.

            Args:
                request (~.service.ListCertificatesRequest):
                    The request object. Request message for
                [CertificateAuthorityService.ListCertificates][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCertificates].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListCertificatesResponse:
                    Response message for
                [CertificateAuthorityService.ListCertificates][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCertificates].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/caPools/*}/certificates",
                },
            ]
            request, metadata = self._interceptor.pre_list_certificates(
                request, metadata
            )
            pb_request = service.ListCertificatesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.ListCertificatesResponse()
            pb_resp = service.ListCertificatesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_certificates(resp)
            return resp

    class _ListCertificateTemplates(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("ListCertificateTemplates")

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
            request: service.ListCertificateTemplatesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCertificateTemplatesResponse:
            r"""Call the list certificate
            templates method over HTTP.

                Args:
                    request (~.service.ListCertificateTemplatesRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.ListCertificateTemplates][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCertificateTemplates].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.service.ListCertificateTemplatesResponse:
                        Response message for
                    [CertificateAuthorityService.ListCertificateTemplates][google.cloud.security.privateca.v1.CertificateAuthorityService.ListCertificateTemplates].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/certificateTemplates",
                },
            ]
            request, metadata = self._interceptor.pre_list_certificate_templates(
                request, metadata
            )
            pb_request = service.ListCertificateTemplatesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = service.ListCertificateTemplatesResponse()
            pb_resp = service.ListCertificateTemplatesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_certificate_templates(resp)
            return resp

    class _RevokeCertificate(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("RevokeCertificate")

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
            request: service.RevokeCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Certificate:
            r"""Call the revoke certificate method over HTTP.

            Args:
                request (~.service.RevokeCertificateRequest):
                    The request object. Request message for
                [CertificateAuthorityService.RevokeCertificate][google.cloud.security.privateca.v1.CertificateAuthorityService.RevokeCertificate].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Certificate:
                    A
                [Certificate][google.cloud.security.privateca.v1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificates/*}:revoke",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_revoke_certificate(
                request, metadata
            )
            pb_request = service.RevokeCertificateRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.Certificate()
            pb_resp = resources.Certificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_revoke_certificate(resp)
            return resp

    class _UndeleteCertificateAuthority(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("UndeleteCertificateAuthority")

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
            request: service.UndeleteCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the undelete certificate
            authority method over HTTP.

                Args:
                    request (~.service.UndeleteCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.UndeleteCertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthorityService.UndeleteCertificateAuthority].
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
                    "uri": "/v1/{name=projects/*/locations/*/caPools/*/certificateAuthorities/*}:undelete",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_undelete_certificate_authority(
                request, metadata
            )
            pb_request = service.UndeleteCertificateAuthorityRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_undelete_certificate_authority(resp)
            return resp

    class _UpdateCaPool(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("UpdateCaPool")

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
            request: service.UpdateCaPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update ca pool method over HTTP.

            Args:
                request (~.service.UpdateCaPoolRequest):
                    The request object. Request message for
                [CertificateAuthorityService.UpdateCaPool][google.cloud.security.privateca.v1.CertificateAuthorityService.UpdateCaPool].
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
                    "uri": "/v1/{ca_pool.name=projects/*/locations/*/caPools/*}",
                    "body": "ca_pool",
                },
            ]
            request, metadata = self._interceptor.pre_update_ca_pool(request, metadata)
            pb_request = service.UpdateCaPoolRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_update_ca_pool(resp)
            return resp

    class _UpdateCertificate(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("UpdateCertificate")

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
            request: service.UpdateCertificateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Certificate:
            r"""Call the update certificate method over HTTP.

            Args:
                request (~.service.UpdateCertificateRequest):
                    The request object. Request message for
                [CertificateAuthorityService.UpdateCertificate][google.cloud.security.privateca.v1.CertificateAuthorityService.UpdateCertificate].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Certificate:
                    A
                [Certificate][google.cloud.security.privateca.v1.Certificate]
                corresponds to a signed X.509 certificate issued by a
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{certificate.name=projects/*/locations/*/caPools/*/certificates/*}",
                    "body": "certificate",
                },
            ]
            request, metadata = self._interceptor.pre_update_certificate(
                request, metadata
            )
            pb_request = service.UpdateCertificateRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = resources.Certificate()
            pb_resp = resources.Certificate.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_certificate(resp)
            return resp

    class _UpdateCertificateAuthority(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("UpdateCertificateAuthority")

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
            request: service.UpdateCertificateAuthorityRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update certificate
            authority method over HTTP.

                Args:
                    request (~.service.UpdateCertificateAuthorityRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.UpdateCertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthorityService.UpdateCertificateAuthority].
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
                    "uri": "/v1/{certificate_authority.name=projects/*/locations/*/caPools/*/certificateAuthorities/*}",
                    "body": "certificate_authority",
                },
            ]
            request, metadata = self._interceptor.pre_update_certificate_authority(
                request, metadata
            )
            pb_request = service.UpdateCertificateAuthorityRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_update_certificate_authority(resp)
            return resp

    class _UpdateCertificateRevocationList(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("UpdateCertificateRevocationList")

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
            request: service.UpdateCertificateRevocationListRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update certificate
            revocation list method over HTTP.

                Args:
                    request (~.service.UpdateCertificateRevocationListRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.UpdateCertificateRevocationList][google.cloud.security.privateca.v1.CertificateAuthorityService.UpdateCertificateRevocationList].
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
                    "uri": "/v1/{certificate_revocation_list.name=projects/*/locations/*/caPools/*/certificateAuthorities/*/certificateRevocationLists/*}",
                    "body": "certificate_revocation_list",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_update_certificate_revocation_list(
                request, metadata
            )
            pb_request = service.UpdateCertificateRevocationListRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_update_certificate_revocation_list(resp)
            return resp

    class _UpdateCertificateTemplate(CertificateAuthorityServiceRestStub):
        def __hash__(self):
            return hash("UpdateCertificateTemplate")

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
            request: service.UpdateCertificateTemplateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update certificate
            template method over HTTP.

                Args:
                    request (~.service.UpdateCertificateTemplateRequest):
                        The request object. Request message for
                    [CertificateAuthorityService.UpdateCertificateTemplate][google.cloud.security.privateca.v1.CertificateAuthorityService.UpdateCertificateTemplate].
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
                    "uri": "/v1/{certificate_template.name=projects/*/locations/*/certificateTemplates/*}",
                    "body": "certificate_template",
                },
            ]
            request, metadata = self._interceptor.pre_update_certificate_template(
                request, metadata
            )
            pb_request = service.UpdateCertificateTemplateRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=True,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
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
            resp = self._interceptor.post_update_certificate_template(resp)
            return resp

    @property
    def activate_certificate_authority(
        self,
    ) -> Callable[
        [service.ActivateCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ActivateCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_ca_pool(
        self,
    ) -> Callable[[service.CreateCaPoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCaPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_certificate(
        self,
    ) -> Callable[[service.CreateCertificateRequest], resources.Certificate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_certificate_authority(
        self,
    ) -> Callable[
        [service.CreateCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_certificate_template(
        self,
    ) -> Callable[[service.CreateCertificateTemplateRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCertificateTemplate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_ca_pool(
        self,
    ) -> Callable[[service.DeleteCaPoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCaPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_certificate_authority(
        self,
    ) -> Callable[
        [service.DeleteCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_certificate_template(
        self,
    ) -> Callable[[service.DeleteCertificateTemplateRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCertificateTemplate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def disable_certificate_authority(
        self,
    ) -> Callable[
        [service.DisableCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DisableCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enable_certificate_authority(
        self,
    ) -> Callable[
        [service.EnableCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnableCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_ca_certs(
        self,
    ) -> Callable[[service.FetchCaCertsRequest], service.FetchCaCertsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchCaCerts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def fetch_certificate_authority_csr(
        self,
    ) -> Callable[
        [service.FetchCertificateAuthorityCsrRequest],
        service.FetchCertificateAuthorityCsrResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._FetchCertificateAuthorityCsr(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_ca_pool(self) -> Callable[[service.GetCaPoolRequest], resources.CaPool]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCaPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_certificate(
        self,
    ) -> Callable[[service.GetCertificateRequest], resources.Certificate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_certificate_authority(
        self,
    ) -> Callable[
        [service.GetCertificateAuthorityRequest], resources.CertificateAuthority
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_certificate_revocation_list(
        self,
    ) -> Callable[
        [service.GetCertificateRevocationListRequest],
        resources.CertificateRevocationList,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCertificateRevocationList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_certificate_template(
        self,
    ) -> Callable[
        [service.GetCertificateTemplateRequest], resources.CertificateTemplate
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCertificateTemplate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_ca_pools(
        self,
    ) -> Callable[[service.ListCaPoolsRequest], service.ListCaPoolsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCaPools(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_certificate_authorities(
        self,
    ) -> Callable[
        [service.ListCertificateAuthoritiesRequest],
        service.ListCertificateAuthoritiesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCertificateAuthorities(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_certificate_revocation_lists(
        self,
    ) -> Callable[
        [service.ListCertificateRevocationListsRequest],
        service.ListCertificateRevocationListsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCertificateRevocationLists(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_certificates(
        self,
    ) -> Callable[[service.ListCertificatesRequest], service.ListCertificatesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCertificates(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_certificate_templates(
        self,
    ) -> Callable[
        [service.ListCertificateTemplatesRequest],
        service.ListCertificateTemplatesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCertificateTemplates(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def revoke_certificate(
        self,
    ) -> Callable[[service.RevokeCertificateRequest], resources.Certificate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RevokeCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def undelete_certificate_authority(
        self,
    ) -> Callable[
        [service.UndeleteCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UndeleteCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_ca_pool(
        self,
    ) -> Callable[[service.UpdateCaPoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCaPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_certificate(
        self,
    ) -> Callable[[service.UpdateCertificateRequest], resources.Certificate]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCertificate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_certificate_authority(
        self,
    ) -> Callable[
        [service.UpdateCertificateAuthorityRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCertificateAuthority(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_certificate_revocation_list(
        self,
    ) -> Callable[
        [service.UpdateCertificateRevocationListRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCertificateRevocationList(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_certificate_template(
        self,
    ) -> Callable[[service.UpdateCertificateTemplateRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCertificateTemplate(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(CertificateAuthorityServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*}",
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

    class _ListLocations(CertificateAuthorityServiceRestStub):
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
                    "uri": "/v1/{name=projects/*}/locations",
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
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(CertificateAuthorityServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:

            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/caPools/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/certificateTemplates/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/caPools/*/certificateAuthorities/*/certificateRevocationLists/*}:getIamPolicy",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
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

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(CertificateAuthorityServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:

            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/caPools/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/certificateTemplates/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/caPools/*/certificateAuthorities/*/certificateRevocationLists/*}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(CertificateAuthorityServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:

            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/caPools/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/certificateTemplates/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/caPools/*/certificateAuthorities/*/certificateRevocationLists/*}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(CertificateAuthorityServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
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
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(CertificateAuthorityServiceRestStub):
        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:

            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
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

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(CertificateAuthorityServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
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

    class _ListOperations(CertificateAuthorityServiceRestStub):
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
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
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


__all__ = ("CertificateAuthorityServiceRestTransport",)
