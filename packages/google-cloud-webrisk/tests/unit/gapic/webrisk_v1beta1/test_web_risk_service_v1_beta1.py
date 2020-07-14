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

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.webrisk_v1beta1.services.web_risk_service_v1_beta1 import (
    WebRiskServiceV1Beta1AsyncClient,
)
from google.cloud.webrisk_v1beta1.services.web_risk_service_v1_beta1 import (
    WebRiskServiceV1Beta1Client,
)
from google.cloud.webrisk_v1beta1.services.web_risk_service_v1_beta1 import transports
from google.cloud.webrisk_v1beta1.types import webrisk
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert WebRiskServiceV1Beta1Client._get_default_mtls_endpoint(None) is None
    assert (
        WebRiskServiceV1Beta1Client._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        WebRiskServiceV1Beta1Client._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        WebRiskServiceV1Beta1Client._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        WebRiskServiceV1Beta1Client._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        WebRiskServiceV1Beta1Client._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [WebRiskServiceV1Beta1Client, WebRiskServiceV1Beta1AsyncClient]
)
def test_web_risk_service_v1_beta1_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "webrisk.googleapis.com:443"


def test_web_risk_service_v1_beta1_client_get_transport_class():
    transport = WebRiskServiceV1Beta1Client.get_transport_class()
    assert transport == transports.WebRiskServiceV1Beta1GrpcTransport

    transport = WebRiskServiceV1Beta1Client.get_transport_class("grpc")
    assert transport == transports.WebRiskServiceV1Beta1GrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            WebRiskServiceV1Beta1Client,
            transports.WebRiskServiceV1Beta1GrpcTransport,
            "grpc",
        ),
        (
            WebRiskServiceV1Beta1AsyncClient,
            transports.WebRiskServiceV1Beta1GrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_web_risk_service_v1_beta1_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(WebRiskServiceV1Beta1Client, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(WebRiskServiceV1Beta1Client, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    os.environ["GOOGLE_API_USE_MTLS"] = "never"
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class()
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    os.environ["GOOGLE_API_USE_MTLS"] = "always"
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class()
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_MTLS_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=None,
        )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
    options = client_options.ClientOptions(
        client_cert_source=client_cert_source_callback
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_MTLS_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=client_cert_source_callback,
        )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
    with mock.patch.object(transport_class, "__init__") as patched:
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
    with mock.patch.object(transport_class, "__init__") as patched:
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    os.environ["GOOGLE_API_USE_MTLS"] = "Unsupported"
    with pytest.raises(MutualTLSChannelError):
        client = client_class()

    del os.environ["GOOGLE_API_USE_MTLS"]


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            WebRiskServiceV1Beta1Client,
            transports.WebRiskServiceV1Beta1GrpcTransport,
            "grpc",
        ),
        (
            WebRiskServiceV1Beta1AsyncClient,
            transports.WebRiskServiceV1Beta1GrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_web_risk_service_v1_beta1_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            WebRiskServiceV1Beta1Client,
            transports.WebRiskServiceV1Beta1GrpcTransport,
            "grpc",
        ),
        (
            WebRiskServiceV1Beta1AsyncClient,
            transports.WebRiskServiceV1Beta1GrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_web_risk_service_v1_beta1_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
        )


def test_web_risk_service_v1_beta1_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.webrisk_v1beta1.services.web_risk_service_v1_beta1.transports.WebRiskServiceV1Beta1GrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = WebRiskServiceV1Beta1Client(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
        )


def test_compute_threat_list_diff(transport: str = "grpc"):
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = webrisk.ComputeThreatListDiffRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.compute_threat_list_diff), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = webrisk.ComputeThreatListDiffResponse(
            response_type=webrisk.ComputeThreatListDiffResponse.ResponseType.DIFF,
            new_version_token=b"new_version_token_blob",
        )

        response = client.compute_threat_list_diff(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, webrisk.ComputeThreatListDiffResponse)

    assert (
        response.response_type
        == webrisk.ComputeThreatListDiffResponse.ResponseType.DIFF
    )

    assert response.new_version_token == b"new_version_token_blob"


@pytest.mark.asyncio
async def test_compute_threat_list_diff_async(transport: str = "grpc_asyncio"):
    client = WebRiskServiceV1Beta1AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = webrisk.ComputeThreatListDiffRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.compute_threat_list_diff), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            webrisk.ComputeThreatListDiffResponse(
                response_type=webrisk.ComputeThreatListDiffResponse.ResponseType.DIFF,
                new_version_token=b"new_version_token_blob",
            )
        )

        response = await client.compute_threat_list_diff(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, webrisk.ComputeThreatListDiffResponse)

    assert (
        response.response_type
        == webrisk.ComputeThreatListDiffResponse.ResponseType.DIFF
    )

    assert response.new_version_token == b"new_version_token_blob"


def test_compute_threat_list_diff_flattened():
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.compute_threat_list_diff), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = webrisk.ComputeThreatListDiffResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.compute_threat_list_diff(
            threat_type=webrisk.ThreatType.MALWARE,
            version_token=b"version_token_blob",
            constraints=webrisk.ComputeThreatListDiffRequest.Constraints(
                max_diff_entries=1687
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].threat_type == webrisk.ThreatType.MALWARE
        assert args[0].version_token == b"version_token_blob"
        assert args[0].constraints == webrisk.ComputeThreatListDiffRequest.Constraints(
            max_diff_entries=1687
        )


def test_compute_threat_list_diff_flattened_error():
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.compute_threat_list_diff(
            webrisk.ComputeThreatListDiffRequest(),
            threat_type=webrisk.ThreatType.MALWARE,
            version_token=b"version_token_blob",
            constraints=webrisk.ComputeThreatListDiffRequest.Constraints(
                max_diff_entries=1687
            ),
        )


@pytest.mark.asyncio
async def test_compute_threat_list_diff_flattened_async():
    client = WebRiskServiceV1Beta1AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.compute_threat_list_diff), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = webrisk.ComputeThreatListDiffResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            webrisk.ComputeThreatListDiffResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.compute_threat_list_diff(
            threat_type=webrisk.ThreatType.MALWARE,
            version_token=b"version_token_blob",
            constraints=webrisk.ComputeThreatListDiffRequest.Constraints(
                max_diff_entries=1687
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].threat_type == webrisk.ThreatType.MALWARE
        assert args[0].version_token == b"version_token_blob"
        assert args[0].constraints == webrisk.ComputeThreatListDiffRequest.Constraints(
            max_diff_entries=1687
        )


@pytest.mark.asyncio
async def test_compute_threat_list_diff_flattened_error_async():
    client = WebRiskServiceV1Beta1AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.compute_threat_list_diff(
            webrisk.ComputeThreatListDiffRequest(),
            threat_type=webrisk.ThreatType.MALWARE,
            version_token=b"version_token_blob",
            constraints=webrisk.ComputeThreatListDiffRequest.Constraints(
                max_diff_entries=1687
            ),
        )


def test_search_uris(transport: str = "grpc"):
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = webrisk.SearchUrisRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.search_uris), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = webrisk.SearchUrisResponse()

        response = client.search_uris(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, webrisk.SearchUrisResponse)


@pytest.mark.asyncio
async def test_search_uris_async(transport: str = "grpc_asyncio"):
    client = WebRiskServiceV1Beta1AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = webrisk.SearchUrisRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_uris), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            webrisk.SearchUrisResponse()
        )

        response = await client.search_uris(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, webrisk.SearchUrisResponse)


def test_search_uris_flattened():
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.search_uris), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = webrisk.SearchUrisResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_uris(
            uri="uri_value", threat_types=[webrisk.ThreatType.MALWARE],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].uri == "uri_value"
        assert args[0].threat_types == [webrisk.ThreatType.MALWARE]


def test_search_uris_flattened_error():
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_uris(
            webrisk.SearchUrisRequest(),
            uri="uri_value",
            threat_types=[webrisk.ThreatType.MALWARE],
        )


@pytest.mark.asyncio
async def test_search_uris_flattened_async():
    client = WebRiskServiceV1Beta1AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_uris), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = webrisk.SearchUrisResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            webrisk.SearchUrisResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_uris(
            uri="uri_value", threat_types=[webrisk.ThreatType.MALWARE],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].uri == "uri_value"
        assert args[0].threat_types == [webrisk.ThreatType.MALWARE]


@pytest.mark.asyncio
async def test_search_uris_flattened_error_async():
    client = WebRiskServiceV1Beta1AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_uris(
            webrisk.SearchUrisRequest(),
            uri="uri_value",
            threat_types=[webrisk.ThreatType.MALWARE],
        )


def test_search_hashes(transport: str = "grpc"):
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = webrisk.SearchHashesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.search_hashes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = webrisk.SearchHashesResponse()

        response = client.search_hashes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, webrisk.SearchHashesResponse)


@pytest.mark.asyncio
async def test_search_hashes_async(transport: str = "grpc_asyncio"):
    client = WebRiskServiceV1Beta1AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = webrisk.SearchHashesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_hashes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            webrisk.SearchHashesResponse()
        )

        response = await client.search_hashes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, webrisk.SearchHashesResponse)


def test_search_hashes_flattened():
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.search_hashes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = webrisk.SearchHashesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.search_hashes(
            hash_prefix=b"hash_prefix_blob", threat_types=[webrisk.ThreatType.MALWARE],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].hash_prefix == b"hash_prefix_blob"
        assert args[0].threat_types == [webrisk.ThreatType.MALWARE]


def test_search_hashes_flattened_error():
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.search_hashes(
            webrisk.SearchHashesRequest(),
            hash_prefix=b"hash_prefix_blob",
            threat_types=[webrisk.ThreatType.MALWARE],
        )


@pytest.mark.asyncio
async def test_search_hashes_flattened_async():
    client = WebRiskServiceV1Beta1AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.search_hashes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = webrisk.SearchHashesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            webrisk.SearchHashesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.search_hashes(
            hash_prefix=b"hash_prefix_blob", threat_types=[webrisk.ThreatType.MALWARE],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].hash_prefix == b"hash_prefix_blob"
        assert args[0].threat_types == [webrisk.ThreatType.MALWARE]


@pytest.mark.asyncio
async def test_search_hashes_flattened_error_async():
    client = WebRiskServiceV1Beta1AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.search_hashes(
            webrisk.SearchHashesRequest(),
            hash_prefix=b"hash_prefix_blob",
            threat_types=[webrisk.ThreatType.MALWARE],
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.WebRiskServiceV1Beta1GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WebRiskServiceV1Beta1Client(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.WebRiskServiceV1Beta1GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WebRiskServiceV1Beta1Client(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.WebRiskServiceV1Beta1GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WebRiskServiceV1Beta1Client(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.WebRiskServiceV1Beta1GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = WebRiskServiceV1Beta1Client(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.WebRiskServiceV1Beta1GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.WebRiskServiceV1Beta1GrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(),
    )
    assert isinstance(client._transport, transports.WebRiskServiceV1Beta1GrpcTransport,)


def test_web_risk_service_v1_beta1_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.WebRiskServiceV1Beta1Transport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_web_risk_service_v1_beta1_base_transport():
    # Instantiate the base transport.
    transport = transports.WebRiskServiceV1Beta1Transport(
        credentials=credentials.AnonymousCredentials(),
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "compute_threat_list_diff",
        "search_uris",
        "search_hashes",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_web_risk_service_v1_beta1_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(auth, "load_credentials_from_file") as load_creds:
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.WebRiskServiceV1Beta1Transport(
            credentials_file="credentials.json",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
        )


def test_web_risk_service_v1_beta1_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        WebRiskServiceV1Beta1Client()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_web_risk_service_v1_beta1_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.WebRiskServiceV1Beta1GrpcTransport(host="squid.clam.whelk")
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_web_risk_service_v1_beta1_host_no_port():
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="webrisk.googleapis.com"
        ),
    )
    assert client._transport._host == "webrisk.googleapis.com:443"


def test_web_risk_service_v1_beta1_host_with_port():
    client = WebRiskServiceV1Beta1Client(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="webrisk.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "webrisk.googleapis.com:8000"


def test_web_risk_service_v1_beta1_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.WebRiskServiceV1Beta1GrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_web_risk_service_v1_beta1_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.WebRiskServiceV1Beta1GrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_web_risk_service_v1_beta1_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.WebRiskServiceV1Beta1GrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_web_risk_service_v1_beta1_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.WebRiskServiceV1Beta1GrpcAsyncIOTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_web_risk_service_v1_beta1_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.WebRiskServiceV1Beta1GrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_web_risk_service_v1_beta1_grpc_asyncio_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.WebRiskServiceV1Beta1GrpcAsyncIOTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
        )
        assert transport.grpc_channel == mock_grpc_channel
