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
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore

from google.cloud.kms_v1.types import resources, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import KeyManagementServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class KeyManagementServiceRestInterceptor:
    """Interceptor for KeyManagementService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the KeyManagementServiceRestTransport.

    .. code-block:: python
        class MyCustomKeyManagementServiceInterceptor(KeyManagementServiceRestInterceptor):
            def pre_asymmetric_decrypt(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_asymmetric_decrypt(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_asymmetric_sign(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_asymmetric_sign(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_crypto_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_crypto_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_crypto_key_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_crypto_key_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_import_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_import_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_key_ring(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_key_ring(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_decrypt(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_decrypt(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_destroy_crypto_key_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_destroy_crypto_key_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_encrypt(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_encrypt(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_random_bytes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_random_bytes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_crypto_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_crypto_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_crypto_key_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_crypto_key_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_import_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_import_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_key_ring(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_key_ring(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_public_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_public_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_import_crypto_key_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_import_crypto_key_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_crypto_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_crypto_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_crypto_key_versions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_crypto_key_versions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_import_jobs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_import_jobs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_key_rings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_key_rings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_mac_sign(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_mac_sign(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_mac_verify(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_mac_verify(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_raw_decrypt(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_raw_decrypt(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_raw_encrypt(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_raw_encrypt(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restore_crypto_key_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restore_crypto_key_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_crypto_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_crypto_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_crypto_key_primary_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_crypto_key_primary_version(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_crypto_key_version(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_crypto_key_version(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = KeyManagementServiceRestTransport(interceptor=MyCustomKeyManagementServiceInterceptor())
        client = KeyManagementServiceClient(transport=transport)


    """

    def pre_asymmetric_decrypt(
        self,
        request: service.AsymmetricDecryptRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.AsymmetricDecryptRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for asymmetric_decrypt

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_asymmetric_decrypt(
        self, response: service.AsymmetricDecryptResponse
    ) -> service.AsymmetricDecryptResponse:
        """Post-rpc interceptor for asymmetric_decrypt

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_asymmetric_sign(
        self,
        request: service.AsymmetricSignRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.AsymmetricSignRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for asymmetric_sign

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_asymmetric_sign(
        self, response: service.AsymmetricSignResponse
    ) -> service.AsymmetricSignResponse:
        """Post-rpc interceptor for asymmetric_sign

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_create_crypto_key(
        self,
        request: service.CreateCryptoKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateCryptoKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_crypto_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_create_crypto_key(
        self, response: resources.CryptoKey
    ) -> resources.CryptoKey:
        """Post-rpc interceptor for create_crypto_key

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_create_crypto_key_version(
        self,
        request: service.CreateCryptoKeyVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateCryptoKeyVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_crypto_key_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_create_crypto_key_version(
        self, response: resources.CryptoKeyVersion
    ) -> resources.CryptoKeyVersion:
        """Post-rpc interceptor for create_crypto_key_version

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_create_import_job(
        self,
        request: service.CreateImportJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.CreateImportJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_import_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_create_import_job(
        self, response: resources.ImportJob
    ) -> resources.ImportJob:
        """Post-rpc interceptor for create_import_job

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_create_key_ring(
        self, request: service.CreateKeyRingRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateKeyRingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_key_ring

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_create_key_ring(self, response: resources.KeyRing) -> resources.KeyRing:
        """Post-rpc interceptor for create_key_ring

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_decrypt(
        self, request: service.DecryptRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DecryptRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for decrypt

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_decrypt(
        self, response: service.DecryptResponse
    ) -> service.DecryptResponse:
        """Post-rpc interceptor for decrypt

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_destroy_crypto_key_version(
        self,
        request: service.DestroyCryptoKeyVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.DestroyCryptoKeyVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for destroy_crypto_key_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_destroy_crypto_key_version(
        self, response: resources.CryptoKeyVersion
    ) -> resources.CryptoKeyVersion:
        """Post-rpc interceptor for destroy_crypto_key_version

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_encrypt(
        self, request: service.EncryptRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.EncryptRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for encrypt

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_encrypt(
        self, response: service.EncryptResponse
    ) -> service.EncryptResponse:
        """Post-rpc interceptor for encrypt

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_generate_random_bytes(
        self,
        request: service.GenerateRandomBytesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GenerateRandomBytesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for generate_random_bytes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_generate_random_bytes(
        self, response: service.GenerateRandomBytesResponse
    ) -> service.GenerateRandomBytesResponse:
        """Post-rpc interceptor for generate_random_bytes

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_get_crypto_key(
        self, request: service.GetCryptoKeyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetCryptoKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_crypto_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_get_crypto_key(self, response: resources.CryptoKey) -> resources.CryptoKey:
        """Post-rpc interceptor for get_crypto_key

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_get_crypto_key_version(
        self,
        request: service.GetCryptoKeyVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetCryptoKeyVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_crypto_key_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_get_crypto_key_version(
        self, response: resources.CryptoKeyVersion
    ) -> resources.CryptoKeyVersion:
        """Post-rpc interceptor for get_crypto_key_version

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_get_import_job(
        self, request: service.GetImportJobRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetImportJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_import_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_get_import_job(self, response: resources.ImportJob) -> resources.ImportJob:
        """Post-rpc interceptor for get_import_job

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_get_key_ring(
        self, request: service.GetKeyRingRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetKeyRingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_key_ring

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_get_key_ring(self, response: resources.KeyRing) -> resources.KeyRing:
        """Post-rpc interceptor for get_key_ring

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_get_public_key(
        self, request: service.GetPublicKeyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetPublicKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_public_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_get_public_key(self, response: resources.PublicKey) -> resources.PublicKey:
        """Post-rpc interceptor for get_public_key

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_import_crypto_key_version(
        self,
        request: service.ImportCryptoKeyVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ImportCryptoKeyVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for import_crypto_key_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_import_crypto_key_version(
        self, response: resources.CryptoKeyVersion
    ) -> resources.CryptoKeyVersion:
        """Post-rpc interceptor for import_crypto_key_version

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_list_crypto_keys(
        self,
        request: service.ListCryptoKeysRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListCryptoKeysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_crypto_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_list_crypto_keys(
        self, response: service.ListCryptoKeysResponse
    ) -> service.ListCryptoKeysResponse:
        """Post-rpc interceptor for list_crypto_keys

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_list_crypto_key_versions(
        self,
        request: service.ListCryptoKeyVersionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListCryptoKeyVersionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_crypto_key_versions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_list_crypto_key_versions(
        self, response: service.ListCryptoKeyVersionsResponse
    ) -> service.ListCryptoKeyVersionsResponse:
        """Post-rpc interceptor for list_crypto_key_versions

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_list_import_jobs(
        self,
        request: service.ListImportJobsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListImportJobsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_import_jobs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_list_import_jobs(
        self, response: service.ListImportJobsResponse
    ) -> service.ListImportJobsResponse:
        """Post-rpc interceptor for list_import_jobs

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_list_key_rings(
        self, request: service.ListKeyRingsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListKeyRingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_key_rings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_list_key_rings(
        self, response: service.ListKeyRingsResponse
    ) -> service.ListKeyRingsResponse:
        """Post-rpc interceptor for list_key_rings

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_mac_sign(
        self, request: service.MacSignRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.MacSignRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for mac_sign

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_mac_sign(
        self, response: service.MacSignResponse
    ) -> service.MacSignResponse:
        """Post-rpc interceptor for mac_sign

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_mac_verify(
        self, request: service.MacVerifyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.MacVerifyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for mac_verify

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_mac_verify(
        self, response: service.MacVerifyResponse
    ) -> service.MacVerifyResponse:
        """Post-rpc interceptor for mac_verify

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_raw_decrypt(
        self, request: service.RawDecryptRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.RawDecryptRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for raw_decrypt

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_raw_decrypt(
        self, response: service.RawDecryptResponse
    ) -> service.RawDecryptResponse:
        """Post-rpc interceptor for raw_decrypt

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_raw_encrypt(
        self, request: service.RawEncryptRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.RawEncryptRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for raw_encrypt

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_raw_encrypt(
        self, response: service.RawEncryptResponse
    ) -> service.RawEncryptResponse:
        """Post-rpc interceptor for raw_encrypt

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_restore_crypto_key_version(
        self,
        request: service.RestoreCryptoKeyVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.RestoreCryptoKeyVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for restore_crypto_key_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_restore_crypto_key_version(
        self, response: resources.CryptoKeyVersion
    ) -> resources.CryptoKeyVersion:
        """Post-rpc interceptor for restore_crypto_key_version

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_update_crypto_key(
        self,
        request: service.UpdateCryptoKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateCryptoKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_crypto_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_update_crypto_key(
        self, response: resources.CryptoKey
    ) -> resources.CryptoKey:
        """Post-rpc interceptor for update_crypto_key

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_update_crypto_key_primary_version(
        self,
        request: service.UpdateCryptoKeyPrimaryVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateCryptoKeyPrimaryVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_crypto_key_primary_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_update_crypto_key_primary_version(
        self, response: resources.CryptoKey
    ) -> resources.CryptoKey:
        """Post-rpc interceptor for update_crypto_key_primary_version

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response

    def pre_update_crypto_key_version(
        self,
        request: service.UpdateCryptoKeyVersionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.UpdateCryptoKeyVersionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_crypto_key_version

        Override in a subclass to manipulate the request or metadata
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_update_crypto_key_version(
        self, response: resources.CryptoKeyVersion
    ) -> resources.CryptoKeyVersion:
        """Post-rpc interceptor for update_crypto_key_version

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
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
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
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
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
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
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
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
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
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
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
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
        before they are sent to the KeyManagementService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the KeyManagementService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class KeyManagementServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: KeyManagementServiceRestInterceptor


class KeyManagementServiceRestTransport(KeyManagementServiceTransport):
    """REST backend transport for KeyManagementService.

    Google Cloud Key Management Service

    Manages cryptographic keys and operations using those keys.
    Implements a REST model with the following objects:

    -  [KeyRing][google.cloud.kms.v1.KeyRing]
    -  [CryptoKey][google.cloud.kms.v1.CryptoKey]
    -  [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
    -  [ImportJob][google.cloud.kms.v1.ImportJob]

    If you are using manual gRPC libraries, see `Using gRPC with Cloud
    KMS <https://cloud.google.com/kms/docs/grpc>`__.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "cloudkms.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[KeyManagementServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'cloudkms.googleapis.com').
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
        self._interceptor = interceptor or KeyManagementServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _AsymmetricDecrypt(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("AsymmetricDecrypt")

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
            request: service.AsymmetricDecryptRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.AsymmetricDecryptResponse:
            r"""Call the asymmetric decrypt method over HTTP.

            Args:
                request (~.service.AsymmetricDecryptRequest):
                    The request object. Request message for
                [KeyManagementService.AsymmetricDecrypt][google.cloud.kms.v1.KeyManagementService.AsymmetricDecrypt].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.AsymmetricDecryptResponse:
                    Response message for
                [KeyManagementService.AsymmetricDecrypt][google.cloud.kms.v1.KeyManagementService.AsymmetricDecrypt].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:asymmetricDecrypt",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_asymmetric_decrypt(
                request, metadata
            )
            pb_request = service.AsymmetricDecryptRequest.pb(request)
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
            resp = service.AsymmetricDecryptResponse()
            pb_resp = service.AsymmetricDecryptResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_asymmetric_decrypt(resp)
            return resp

    class _AsymmetricSign(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("AsymmetricSign")

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
            request: service.AsymmetricSignRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.AsymmetricSignResponse:
            r"""Call the asymmetric sign method over HTTP.

            Args:
                request (~.service.AsymmetricSignRequest):
                    The request object. Request message for
                [KeyManagementService.AsymmetricSign][google.cloud.kms.v1.KeyManagementService.AsymmetricSign].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.AsymmetricSignResponse:
                    Response message for
                [KeyManagementService.AsymmetricSign][google.cloud.kms.v1.KeyManagementService.AsymmetricSign].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:asymmetricSign",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_asymmetric_sign(request, metadata)
            pb_request = service.AsymmetricSignRequest.pb(request)
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
            resp = service.AsymmetricSignResponse()
            pb_resp = service.AsymmetricSignResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_asymmetric_sign(resp)
            return resp

    class _CreateCryptoKey(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("CreateCryptoKey")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "cryptoKeyId": "",
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
            request: service.CreateCryptoKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKey:
            r"""Call the create crypto key method over HTTP.

            Args:
                request (~.service.CreateCryptoKeyRequest):
                    The request object. Request message for
                [KeyManagementService.CreateCryptoKey][google.cloud.kms.v1.KeyManagementService.CreateCryptoKey].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CryptoKey:
                    A [CryptoKey][google.cloud.kms.v1.CryptoKey] represents
                a logical key that can be used for cryptographic
                operations.

                A [CryptoKey][google.cloud.kms.v1.CryptoKey] is made up
                of zero or more
                [versions][google.cloud.kms.v1.CryptoKeyVersion], which
                represent the actual key material used in cryptographic
                operations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/keyRings/*}/cryptoKeys",
                    "body": "crypto_key",
                },
            ]
            request, metadata = self._interceptor.pre_create_crypto_key(
                request, metadata
            )
            pb_request = service.CreateCryptoKeyRequest.pb(request)
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
            resp = resources.CryptoKey()
            pb_resp = resources.CryptoKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_crypto_key(resp)
            return resp

    class _CreateCryptoKeyVersion(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("CreateCryptoKeyVersion")

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
            request: service.CreateCryptoKeyVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKeyVersion:
            r"""Call the create crypto key version method over HTTP.

            Args:
                request (~.service.CreateCryptoKeyVersionRequest):
                    The request object. Request message for
                [KeyManagementService.CreateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.CreateCryptoKeyVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CryptoKeyVersion:
                    A
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                represents an individual cryptographic key, and the
                associated key material.

                An
                [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                version can be used for cryptographic operations.

                For security reasons, the raw cryptographic key material
                represented by a
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                can never be viewed or exported. It can only be used to
                encrypt, decrypt, or sign data when an authorized user
                or application invokes Cloud KMS.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/keyRings/*/cryptoKeys/*}/cryptoKeyVersions",
                    "body": "crypto_key_version",
                },
            ]
            request, metadata = self._interceptor.pre_create_crypto_key_version(
                request, metadata
            )
            pb_request = service.CreateCryptoKeyVersionRequest.pb(request)
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
            resp = resources.CryptoKeyVersion()
            pb_resp = resources.CryptoKeyVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_crypto_key_version(resp)
            return resp

    class _CreateImportJob(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("CreateImportJob")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "importJobId": "",
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
            request: service.CreateImportJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ImportJob:
            r"""Call the create import job method over HTTP.

            Args:
                request (~.service.CreateImportJobRequest):
                    The request object. Request message for
                [KeyManagementService.CreateImportJob][google.cloud.kms.v1.KeyManagementService.CreateImportJob].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.ImportJob:
                    An [ImportJob][google.cloud.kms.v1.ImportJob] can be
                used to create
                [CryptoKeys][google.cloud.kms.v1.CryptoKey] and
                [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                using pre-existing key material, generated outside of
                Cloud KMS.

                When an [ImportJob][google.cloud.kms.v1.ImportJob] is
                created, Cloud KMS will generate a "wrapping key", which
                is a public/private key pair. You use the wrapping key
                to encrypt (also known as wrap) the pre-existing key
                material to protect it during the import process. The
                nature of the wrapping key depends on the choice of
                [import_method][google.cloud.kms.v1.ImportJob.import_method].
                When the wrapping key generation is complete, the
                [state][google.cloud.kms.v1.ImportJob.state] will be set
                to
                [ACTIVE][google.cloud.kms.v1.ImportJob.ImportJobState.ACTIVE]
                and the
                [public_key][google.cloud.kms.v1.ImportJob.public_key]
                can be fetched. The fetched public key can then be used
                to wrap your pre-existing key material.

                Once the key material is wrapped, it can be imported
                into a new
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                in an existing
                [CryptoKey][google.cloud.kms.v1.CryptoKey] by calling
                [ImportCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.ImportCryptoKeyVersion].
                Multiple
                [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                can be imported with a single
                [ImportJob][google.cloud.kms.v1.ImportJob]. Cloud KMS
                uses the private key portion of the wrapping key to
                unwrap the key material. Only Cloud KMS has access to
                the private key.

                An [ImportJob][google.cloud.kms.v1.ImportJob] expires 3
                days after it is created. Once expired, Cloud KMS will
                no longer be able to import or unwrap any key material
                that was wrapped with the
                [ImportJob][google.cloud.kms.v1.ImportJob]'s public key.

                For more information, see `Importing a
                key <https://cloud.google.com/kms/docs/importing-a-key>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/keyRings/*}/importJobs",
                    "body": "import_job",
                },
            ]
            request, metadata = self._interceptor.pre_create_import_job(
                request, metadata
            )
            pb_request = service.CreateImportJobRequest.pb(request)
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
            resp = resources.ImportJob()
            pb_resp = resources.ImportJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_import_job(resp)
            return resp

    class _CreateKeyRing(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("CreateKeyRing")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "keyRingId": "",
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
            request: service.CreateKeyRingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.KeyRing:
            r"""Call the create key ring method over HTTP.

            Args:
                request (~.service.CreateKeyRingRequest):
                    The request object. Request message for
                [KeyManagementService.CreateKeyRing][google.cloud.kms.v1.KeyManagementService.CreateKeyRing].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.KeyRing:
                    A [KeyRing][google.cloud.kms.v1.KeyRing] is a toplevel
                logical grouping of
                [CryptoKeys][google.cloud.kms.v1.CryptoKey].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/keyRings",
                    "body": "key_ring",
                },
            ]
            request, metadata = self._interceptor.pre_create_key_ring(request, metadata)
            pb_request = service.CreateKeyRingRequest.pb(request)
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
            resp = resources.KeyRing()
            pb_resp = resources.KeyRing.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_key_ring(resp)
            return resp

    class _Decrypt(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("Decrypt")

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
            request: service.DecryptRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.DecryptResponse:
            r"""Call the decrypt method over HTTP.

            Args:
                request (~.service.DecryptRequest):
                    The request object. Request message for
                [KeyManagementService.Decrypt][google.cloud.kms.v1.KeyManagementService.Decrypt].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.DecryptResponse:
                    Response message for
                [KeyManagementService.Decrypt][google.cloud.kms.v1.KeyManagementService.Decrypt].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*}:decrypt",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_decrypt(request, metadata)
            pb_request = service.DecryptRequest.pb(request)
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
            resp = service.DecryptResponse()
            pb_resp = service.DecryptResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_decrypt(resp)
            return resp

    class _DestroyCryptoKeyVersion(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("DestroyCryptoKeyVersion")

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
            request: service.DestroyCryptoKeyVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKeyVersion:
            r"""Call the destroy crypto key
            version method over HTTP.

                Args:
                    request (~.service.DestroyCryptoKeyVersionRequest):
                        The request object. Request message for
                    [KeyManagementService.DestroyCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.DestroyCryptoKeyVersion].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.CryptoKeyVersion:
                        A
                    [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                    represents an individual cryptographic key, and the
                    associated key material.

                    An
                    [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                    version can be used for cryptographic operations.

                    For security reasons, the raw cryptographic key material
                    represented by a
                    [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                    can never be viewed or exported. It can only be used to
                    encrypt, decrypt, or sign data when an authorized user
                    or application invokes Cloud KMS.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:destroy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_destroy_crypto_key_version(
                request, metadata
            )
            pb_request = service.DestroyCryptoKeyVersionRequest.pb(request)
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
            resp = resources.CryptoKeyVersion()
            pb_resp = resources.CryptoKeyVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_destroy_crypto_key_version(resp)
            return resp

    class _Encrypt(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("Encrypt")

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
            request: service.EncryptRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.EncryptResponse:
            r"""Call the encrypt method over HTTP.

            Args:
                request (~.service.EncryptRequest):
                    The request object. Request message for
                [KeyManagementService.Encrypt][google.cloud.kms.v1.KeyManagementService.Encrypt].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.EncryptResponse:
                    Response message for
                [KeyManagementService.Encrypt][google.cloud.kms.v1.KeyManagementService.Encrypt].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/**}:encrypt",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_encrypt(request, metadata)
            pb_request = service.EncryptRequest.pb(request)
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
            resp = service.EncryptResponse()
            pb_resp = service.EncryptResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_encrypt(resp)
            return resp

    class _GenerateRandomBytes(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("GenerateRandomBytes")

        def __call__(
            self,
            request: service.GenerateRandomBytesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.GenerateRandomBytesResponse:
            r"""Call the generate random bytes method over HTTP.

            Args:
                request (~.service.GenerateRandomBytesRequest):
                    The request object. Request message for
                [KeyManagementService.GenerateRandomBytes][google.cloud.kms.v1.KeyManagementService.GenerateRandomBytes].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.GenerateRandomBytesResponse:
                    Response message for
                [KeyManagementService.GenerateRandomBytes][google.cloud.kms.v1.KeyManagementService.GenerateRandomBytes].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{location=projects/*/locations/*}:generateRandomBytes",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_generate_random_bytes(
                request, metadata
            )
            pb_request = service.GenerateRandomBytesRequest.pb(request)
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
            resp = service.GenerateRandomBytesResponse()
            pb_resp = service.GenerateRandomBytesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_random_bytes(resp)
            return resp

    class _GetCryptoKey(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("GetCryptoKey")

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
            request: service.GetCryptoKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKey:
            r"""Call the get crypto key method over HTTP.

            Args:
                request (~.service.GetCryptoKeyRequest):
                    The request object. Request message for
                [KeyManagementService.GetCryptoKey][google.cloud.kms.v1.KeyManagementService.GetCryptoKey].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CryptoKey:
                    A [CryptoKey][google.cloud.kms.v1.CryptoKey] represents
                a logical key that can be used for cryptographic
                operations.

                A [CryptoKey][google.cloud.kms.v1.CryptoKey] is made up
                of zero or more
                [versions][google.cloud.kms.v1.CryptoKeyVersion], which
                represent the actual key material used in cryptographic
                operations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_crypto_key(request, metadata)
            pb_request = service.GetCryptoKeyRequest.pb(request)
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
            resp = resources.CryptoKey()
            pb_resp = resources.CryptoKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_crypto_key(resp)
            return resp

    class _GetCryptoKeyVersion(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("GetCryptoKeyVersion")

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
            request: service.GetCryptoKeyVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKeyVersion:
            r"""Call the get crypto key version method over HTTP.

            Args:
                request (~.service.GetCryptoKeyVersionRequest):
                    The request object. Request message for
                [KeyManagementService.GetCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.GetCryptoKeyVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CryptoKeyVersion:
                    A
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                represents an individual cryptographic key, and the
                associated key material.

                An
                [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                version can be used for cryptographic operations.

                For security reasons, the raw cryptographic key material
                represented by a
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                can never be viewed or exported. It can only be used to
                encrypt, decrypt, or sign data when an authorized user
                or application invokes Cloud KMS.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_crypto_key_version(
                request, metadata
            )
            pb_request = service.GetCryptoKeyVersionRequest.pb(request)
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
            resp = resources.CryptoKeyVersion()
            pb_resp = resources.CryptoKeyVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_crypto_key_version(resp)
            return resp

    class _GetImportJob(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("GetImportJob")

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
            request: service.GetImportJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.ImportJob:
            r"""Call the get import job method over HTTP.

            Args:
                request (~.service.GetImportJobRequest):
                    The request object. Request message for
                [KeyManagementService.GetImportJob][google.cloud.kms.v1.KeyManagementService.GetImportJob].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.ImportJob:
                    An [ImportJob][google.cloud.kms.v1.ImportJob] can be
                used to create
                [CryptoKeys][google.cloud.kms.v1.CryptoKey] and
                [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                using pre-existing key material, generated outside of
                Cloud KMS.

                When an [ImportJob][google.cloud.kms.v1.ImportJob] is
                created, Cloud KMS will generate a "wrapping key", which
                is a public/private key pair. You use the wrapping key
                to encrypt (also known as wrap) the pre-existing key
                material to protect it during the import process. The
                nature of the wrapping key depends on the choice of
                [import_method][google.cloud.kms.v1.ImportJob.import_method].
                When the wrapping key generation is complete, the
                [state][google.cloud.kms.v1.ImportJob.state] will be set
                to
                [ACTIVE][google.cloud.kms.v1.ImportJob.ImportJobState.ACTIVE]
                and the
                [public_key][google.cloud.kms.v1.ImportJob.public_key]
                can be fetched. The fetched public key can then be used
                to wrap your pre-existing key material.

                Once the key material is wrapped, it can be imported
                into a new
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                in an existing
                [CryptoKey][google.cloud.kms.v1.CryptoKey] by calling
                [ImportCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.ImportCryptoKeyVersion].
                Multiple
                [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                can be imported with a single
                [ImportJob][google.cloud.kms.v1.ImportJob]. Cloud KMS
                uses the private key portion of the wrapping key to
                unwrap the key material. Only Cloud KMS has access to
                the private key.

                An [ImportJob][google.cloud.kms.v1.ImportJob] expires 3
                days after it is created. Once expired, Cloud KMS will
                no longer be able to import or unwrap any key material
                that was wrapped with the
                [ImportJob][google.cloud.kms.v1.ImportJob]'s public key.

                For more information, see `Importing a
                key <https://cloud.google.com/kms/docs/importing-a-key>`__.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/importJobs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_import_job(request, metadata)
            pb_request = service.GetImportJobRequest.pb(request)
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
            resp = resources.ImportJob()
            pb_resp = resources.ImportJob.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_import_job(resp)
            return resp

    class _GetKeyRing(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("GetKeyRing")

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
            request: service.GetKeyRingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.KeyRing:
            r"""Call the get key ring method over HTTP.

            Args:
                request (~.service.GetKeyRingRequest):
                    The request object. Request message for
                [KeyManagementService.GetKeyRing][google.cloud.kms.v1.KeyManagementService.GetKeyRing].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.KeyRing:
                    A [KeyRing][google.cloud.kms.v1.KeyRing] is a toplevel
                logical grouping of
                [CryptoKeys][google.cloud.kms.v1.CryptoKey].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_key_ring(request, metadata)
            pb_request = service.GetKeyRingRequest.pb(request)
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
            resp = resources.KeyRing()
            pb_resp = resources.KeyRing.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_key_ring(resp)
            return resp

    class _GetPublicKey(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("GetPublicKey")

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
            request: service.GetPublicKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.PublicKey:
            r"""Call the get public key method over HTTP.

            Args:
                request (~.service.GetPublicKeyRequest):
                    The request object. Request message for
                [KeyManagementService.GetPublicKey][google.cloud.kms.v1.KeyManagementService.GetPublicKey].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.PublicKey:
                    The public keys for a given
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion].
                Obtained via
                [GetPublicKey][google.cloud.kms.v1.KeyManagementService.GetPublicKey].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}/publicKey",
                },
            ]
            request, metadata = self._interceptor.pre_get_public_key(request, metadata)
            pb_request = service.GetPublicKeyRequest.pb(request)
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
            resp = resources.PublicKey()
            pb_resp = resources.PublicKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_public_key(resp)
            return resp

    class _ImportCryptoKeyVersion(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("ImportCryptoKeyVersion")

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
            request: service.ImportCryptoKeyVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKeyVersion:
            r"""Call the import crypto key version method over HTTP.

            Args:
                request (~.service.ImportCryptoKeyVersionRequest):
                    The request object. Request message for
                [KeyManagementService.ImportCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.ImportCryptoKeyVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CryptoKeyVersion:
                    A
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                represents an individual cryptographic key, and the
                associated key material.

                An
                [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                version can be used for cryptographic operations.

                For security reasons, the raw cryptographic key material
                represented by a
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                can never be viewed or exported. It can only be used to
                encrypt, decrypt, or sign data when an authorized user
                or application invokes Cloud KMS.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/keyRings/*/cryptoKeys/*}/cryptoKeyVersions:import",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_import_crypto_key_version(
                request, metadata
            )
            pb_request = service.ImportCryptoKeyVersionRequest.pb(request)
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
            resp = resources.CryptoKeyVersion()
            pb_resp = resources.CryptoKeyVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_import_crypto_key_version(resp)
            return resp

    class _ListCryptoKeys(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("ListCryptoKeys")

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
            request: service.ListCryptoKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCryptoKeysResponse:
            r"""Call the list crypto keys method over HTTP.

            Args:
                request (~.service.ListCryptoKeysRequest):
                    The request object. Request message for
                [KeyManagementService.ListCryptoKeys][google.cloud.kms.v1.KeyManagementService.ListCryptoKeys].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListCryptoKeysResponse:
                    Response message for
                [KeyManagementService.ListCryptoKeys][google.cloud.kms.v1.KeyManagementService.ListCryptoKeys].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/keyRings/*}/cryptoKeys",
                },
            ]
            request, metadata = self._interceptor.pre_list_crypto_keys(
                request, metadata
            )
            pb_request = service.ListCryptoKeysRequest.pb(request)
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
            resp = service.ListCryptoKeysResponse()
            pb_resp = service.ListCryptoKeysResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_crypto_keys(resp)
            return resp

    class _ListCryptoKeyVersions(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("ListCryptoKeyVersions")

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
            request: service.ListCryptoKeyVersionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListCryptoKeyVersionsResponse:
            r"""Call the list crypto key versions method over HTTP.

            Args:
                request (~.service.ListCryptoKeyVersionsRequest):
                    The request object. Request message for
                [KeyManagementService.ListCryptoKeyVersions][google.cloud.kms.v1.KeyManagementService.ListCryptoKeyVersions].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListCryptoKeyVersionsResponse:
                    Response message for
                [KeyManagementService.ListCryptoKeyVersions][google.cloud.kms.v1.KeyManagementService.ListCryptoKeyVersions].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/keyRings/*/cryptoKeys/*}/cryptoKeyVersions",
                },
            ]
            request, metadata = self._interceptor.pre_list_crypto_key_versions(
                request, metadata
            )
            pb_request = service.ListCryptoKeyVersionsRequest.pb(request)
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
            resp = service.ListCryptoKeyVersionsResponse()
            pb_resp = service.ListCryptoKeyVersionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_crypto_key_versions(resp)
            return resp

    class _ListImportJobs(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("ListImportJobs")

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
            request: service.ListImportJobsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListImportJobsResponse:
            r"""Call the list import jobs method over HTTP.

            Args:
                request (~.service.ListImportJobsRequest):
                    The request object. Request message for
                [KeyManagementService.ListImportJobs][google.cloud.kms.v1.KeyManagementService.ListImportJobs].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListImportJobsResponse:
                    Response message for
                [KeyManagementService.ListImportJobs][google.cloud.kms.v1.KeyManagementService.ListImportJobs].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/keyRings/*}/importJobs",
                },
            ]
            request, metadata = self._interceptor.pre_list_import_jobs(
                request, metadata
            )
            pb_request = service.ListImportJobsRequest.pb(request)
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
            resp = service.ListImportJobsResponse()
            pb_resp = service.ListImportJobsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_import_jobs(resp)
            return resp

    class _ListKeyRings(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("ListKeyRings")

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
            request: service.ListKeyRingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListKeyRingsResponse:
            r"""Call the list key rings method over HTTP.

            Args:
                request (~.service.ListKeyRingsRequest):
                    The request object. Request message for
                [KeyManagementService.ListKeyRings][google.cloud.kms.v1.KeyManagementService.ListKeyRings].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListKeyRingsResponse:
                    Response message for
                [KeyManagementService.ListKeyRings][google.cloud.kms.v1.KeyManagementService.ListKeyRings].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/keyRings",
                },
            ]
            request, metadata = self._interceptor.pre_list_key_rings(request, metadata)
            pb_request = service.ListKeyRingsRequest.pb(request)
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
            resp = service.ListKeyRingsResponse()
            pb_resp = service.ListKeyRingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_key_rings(resp)
            return resp

    class _MacSign(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("MacSign")

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
            request: service.MacSignRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.MacSignResponse:
            r"""Call the mac sign method over HTTP.

            Args:
                request (~.service.MacSignRequest):
                    The request object. Request message for
                [KeyManagementService.MacSign][google.cloud.kms.v1.KeyManagementService.MacSign].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.MacSignResponse:
                    Response message for
                [KeyManagementService.MacSign][google.cloud.kms.v1.KeyManagementService.MacSign].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:macSign",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_mac_sign(request, metadata)
            pb_request = service.MacSignRequest.pb(request)
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
            resp = service.MacSignResponse()
            pb_resp = service.MacSignResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_mac_sign(resp)
            return resp

    class _MacVerify(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("MacVerify")

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
            request: service.MacVerifyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.MacVerifyResponse:
            r"""Call the mac verify method over HTTP.

            Args:
                request (~.service.MacVerifyRequest):
                    The request object. Request message for
                [KeyManagementService.MacVerify][google.cloud.kms.v1.KeyManagementService.MacVerify].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.MacVerifyResponse:
                    Response message for
                [KeyManagementService.MacVerify][google.cloud.kms.v1.KeyManagementService.MacVerify].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:macVerify",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_mac_verify(request, metadata)
            pb_request = service.MacVerifyRequest.pb(request)
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
            resp = service.MacVerifyResponse()
            pb_resp = service.MacVerifyResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_mac_verify(resp)
            return resp

    class _RawDecrypt(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("RawDecrypt")

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
            request: service.RawDecryptRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.RawDecryptResponse:
            r"""Call the raw decrypt method over HTTP.

            Args:
                request (~.service.RawDecryptRequest):
                    The request object. Request message for
                [KeyManagementService.RawDecrypt][google.cloud.kms.v1.KeyManagementService.RawDecrypt].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.RawDecryptResponse:
                    Response message for
                [KeyManagementService.RawDecrypt][google.cloud.kms.v1.KeyManagementService.RawDecrypt].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:rawDecrypt",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_raw_decrypt(request, metadata)
            pb_request = service.RawDecryptRequest.pb(request)
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
            resp = service.RawDecryptResponse()
            pb_resp = service.RawDecryptResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_raw_decrypt(resp)
            return resp

    class _RawEncrypt(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("RawEncrypt")

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
            request: service.RawEncryptRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.RawEncryptResponse:
            r"""Call the raw encrypt method over HTTP.

            Args:
                request (~.service.RawEncryptRequest):
                    The request object. Request message for
                [KeyManagementService.RawEncrypt][google.cloud.kms.v1.KeyManagementService.RawEncrypt].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.RawEncryptResponse:
                    Response message for
                [KeyManagementService.RawEncrypt][google.cloud.kms.v1.KeyManagementService.RawEncrypt].

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:rawEncrypt",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_raw_encrypt(request, metadata)
            pb_request = service.RawEncryptRequest.pb(request)
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
            resp = service.RawEncryptResponse()
            pb_resp = service.RawEncryptResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_raw_encrypt(resp)
            return resp

    class _RestoreCryptoKeyVersion(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("RestoreCryptoKeyVersion")

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
            request: service.RestoreCryptoKeyVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKeyVersion:
            r"""Call the restore crypto key
            version method over HTTP.

                Args:
                    request (~.service.RestoreCryptoKeyVersionRequest):
                        The request object. Request message for
                    [KeyManagementService.RestoreCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.RestoreCryptoKeyVersion].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.CryptoKeyVersion:
                        A
                    [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                    represents an individual cryptographic key, and the
                    associated key material.

                    An
                    [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                    version can be used for cryptographic operations.

                    For security reasons, the raw cryptographic key material
                    represented by a
                    [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                    can never be viewed or exported. It can only be used to
                    encrypt, decrypt, or sign data when an authorized user
                    or application invokes Cloud KMS.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}:restore",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_restore_crypto_key_version(
                request, metadata
            )
            pb_request = service.RestoreCryptoKeyVersionRequest.pb(request)
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
            resp = resources.CryptoKeyVersion()
            pb_resp = resources.CryptoKeyVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_restore_crypto_key_version(resp)
            return resp

    class _UpdateCryptoKey(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("UpdateCryptoKey")

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
            request: service.UpdateCryptoKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKey:
            r"""Call the update crypto key method over HTTP.

            Args:
                request (~.service.UpdateCryptoKeyRequest):
                    The request object. Request message for
                [KeyManagementService.UpdateCryptoKey][google.cloud.kms.v1.KeyManagementService.UpdateCryptoKey].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CryptoKey:
                    A [CryptoKey][google.cloud.kms.v1.CryptoKey] represents
                a logical key that can be used for cryptographic
                operations.

                A [CryptoKey][google.cloud.kms.v1.CryptoKey] is made up
                of zero or more
                [versions][google.cloud.kms.v1.CryptoKeyVersion], which
                represent the actual key material used in cryptographic
                operations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{crypto_key.name=projects/*/locations/*/keyRings/*/cryptoKeys/*}",
                    "body": "crypto_key",
                },
            ]
            request, metadata = self._interceptor.pre_update_crypto_key(
                request, metadata
            )
            pb_request = service.UpdateCryptoKeyRequest.pb(request)
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
            resp = resources.CryptoKey()
            pb_resp = resources.CryptoKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_crypto_key(resp)
            return resp

    class _UpdateCryptoKeyPrimaryVersion(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("UpdateCryptoKeyPrimaryVersion")

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
            request: service.UpdateCryptoKeyPrimaryVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKey:
            r"""Call the update crypto key primary
            version method over HTTP.

                Args:
                    request (~.service.UpdateCryptoKeyPrimaryVersionRequest):
                        The request object. Request message for
                    [KeyManagementService.UpdateCryptoKeyPrimaryVersion][google.cloud.kms.v1.KeyManagementService.UpdateCryptoKeyPrimaryVersion].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.resources.CryptoKey:
                        A [CryptoKey][google.cloud.kms.v1.CryptoKey] represents
                    a logical key that can be used for cryptographic
                    operations.

                    A [CryptoKey][google.cloud.kms.v1.CryptoKey] is made up
                    of zero or more
                    [versions][google.cloud.kms.v1.CryptoKeyVersion], which
                    represent the actual key material used in cryptographic
                    operations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/keyRings/*/cryptoKeys/*}:updatePrimaryVersion",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_update_crypto_key_primary_version(
                request, metadata
            )
            pb_request = service.UpdateCryptoKeyPrimaryVersionRequest.pb(request)
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
            resp = resources.CryptoKey()
            pb_resp = resources.CryptoKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_crypto_key_primary_version(resp)
            return resp

    class _UpdateCryptoKeyVersion(KeyManagementServiceRestStub):
        def __hash__(self):
            return hash("UpdateCryptoKeyVersion")

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
            request: service.UpdateCryptoKeyVersionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.CryptoKeyVersion:
            r"""Call the update crypto key version method over HTTP.

            Args:
                request (~.service.UpdateCryptoKeyVersionRequest):
                    The request object. Request message for
                [KeyManagementService.UpdateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.UpdateCryptoKeyVersion].
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.CryptoKeyVersion:
                    A
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                represents an individual cryptographic key, and the
                associated key material.

                An
                [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                version can be used for cryptographic operations.

                For security reasons, the raw cryptographic key material
                represented by a
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
                can never be viewed or exported. It can only be used to
                encrypt, decrypt, or sign data when an authorized user
                or application invokes Cloud KMS.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{crypto_key_version.name=projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*}",
                    "body": "crypto_key_version",
                },
            ]
            request, metadata = self._interceptor.pre_update_crypto_key_version(
                request, metadata
            )
            pb_request = service.UpdateCryptoKeyVersionRequest.pb(request)
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
            resp = resources.CryptoKeyVersion()
            pb_resp = resources.CryptoKeyVersion.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_crypto_key_version(resp)
            return resp

    @property
    def asymmetric_decrypt(
        self,
    ) -> Callable[
        [service.AsymmetricDecryptRequest], service.AsymmetricDecryptResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AsymmetricDecrypt(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def asymmetric_sign(
        self,
    ) -> Callable[[service.AsymmetricSignRequest], service.AsymmetricSignResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AsymmetricSign(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_crypto_key(
        self,
    ) -> Callable[[service.CreateCryptoKeyRequest], resources.CryptoKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCryptoKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_crypto_key_version(
        self,
    ) -> Callable[[service.CreateCryptoKeyVersionRequest], resources.CryptoKeyVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCryptoKeyVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_import_job(
        self,
    ) -> Callable[[service.CreateImportJobRequest], resources.ImportJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateImportJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_key_ring(
        self,
    ) -> Callable[[service.CreateKeyRingRequest], resources.KeyRing]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateKeyRing(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def decrypt(self) -> Callable[[service.DecryptRequest], service.DecryptResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Decrypt(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def destroy_crypto_key_version(
        self,
    ) -> Callable[[service.DestroyCryptoKeyVersionRequest], resources.CryptoKeyVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DestroyCryptoKeyVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def encrypt(self) -> Callable[[service.EncryptRequest], service.EncryptResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._Encrypt(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_random_bytes(
        self,
    ) -> Callable[
        [service.GenerateRandomBytesRequest], service.GenerateRandomBytesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateRandomBytes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_crypto_key(
        self,
    ) -> Callable[[service.GetCryptoKeyRequest], resources.CryptoKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCryptoKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_crypto_key_version(
        self,
    ) -> Callable[[service.GetCryptoKeyVersionRequest], resources.CryptoKeyVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCryptoKeyVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_import_job(
        self,
    ) -> Callable[[service.GetImportJobRequest], resources.ImportJob]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetImportJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_key_ring(self) -> Callable[[service.GetKeyRingRequest], resources.KeyRing]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetKeyRing(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_public_key(
        self,
    ) -> Callable[[service.GetPublicKeyRequest], resources.PublicKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPublicKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def import_crypto_key_version(
        self,
    ) -> Callable[[service.ImportCryptoKeyVersionRequest], resources.CryptoKeyVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ImportCryptoKeyVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_crypto_keys(
        self,
    ) -> Callable[[service.ListCryptoKeysRequest], service.ListCryptoKeysResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCryptoKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_crypto_key_versions(
        self,
    ) -> Callable[
        [service.ListCryptoKeyVersionsRequest], service.ListCryptoKeyVersionsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCryptoKeyVersions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_import_jobs(
        self,
    ) -> Callable[[service.ListImportJobsRequest], service.ListImportJobsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListImportJobs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_key_rings(
        self,
    ) -> Callable[[service.ListKeyRingsRequest], service.ListKeyRingsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListKeyRings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def mac_sign(self) -> Callable[[service.MacSignRequest], service.MacSignResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MacSign(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def mac_verify(
        self,
    ) -> Callable[[service.MacVerifyRequest], service.MacVerifyResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MacVerify(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def raw_decrypt(
        self,
    ) -> Callable[[service.RawDecryptRequest], service.RawDecryptResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RawDecrypt(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def raw_encrypt(
        self,
    ) -> Callable[[service.RawEncryptRequest], service.RawEncryptResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RawEncrypt(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def restore_crypto_key_version(
        self,
    ) -> Callable[[service.RestoreCryptoKeyVersionRequest], resources.CryptoKeyVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestoreCryptoKeyVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_crypto_key(
        self,
    ) -> Callable[[service.UpdateCryptoKeyRequest], resources.CryptoKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCryptoKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_crypto_key_primary_version(
        self,
    ) -> Callable[[service.UpdateCryptoKeyPrimaryVersionRequest], resources.CryptoKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCryptoKeyPrimaryVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_crypto_key_version(
        self,
    ) -> Callable[[service.UpdateCryptoKeyVersionRequest], resources.CryptoKeyVersion]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCryptoKeyVersion(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(KeyManagementServiceRestStub):
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

    class _ListLocations(KeyManagementServiceRestStub):
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

    class _GetIamPolicy(KeyManagementServiceRestStub):
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
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/cryptoKeys/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/importJobs/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConfig}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConnections/*}:getIamPolicy",
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

    class _SetIamPolicy(KeyManagementServiceRestStub):
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
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/cryptoKeys/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/importJobs/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConfig}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConnections/*}:setIamPolicy",
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

    class _TestIamPermissions(KeyManagementServiceRestStub):
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
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/cryptoKeys/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/keyRings/*/importJobs/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConfig}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/ekmConnections/*}:testIamPermissions",
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
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(KeyManagementServiceRestStub):
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
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("KeyManagementServiceRestTransport",)
