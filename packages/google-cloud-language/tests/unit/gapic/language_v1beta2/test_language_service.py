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
import packaging.version

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.language_v1beta2.services.language_service import (
    LanguageServiceAsyncClient,
)
from google.cloud.language_v1beta2.services.language_service import (
    LanguageServiceClient,
)
from google.cloud.language_v1beta2.services.language_service import transports
from google.cloud.language_v1beta2.services.language_service.transports.base import (
    _API_CORE_VERSION,
)
from google.cloud.language_v1beta2.services.language_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.language_v1beta2.types import language_service
from google.oauth2 import service_account
import google.auth


# TODO(busunkim): Once google-api-core >= 1.26.0 is required:
# - Delete all the api-core and auth "less than" test cases
# - Delete these pytest markers (Make the "greater than or equal to" tests the default).
requires_google_auth_lt_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) >= packaging.version.parse("1.25.0"),
    reason="This test requires google-auth < 1.25.0",
)
requires_google_auth_gte_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) < packaging.version.parse("1.25.0"),
    reason="This test requires google-auth >= 1.25.0",
)

requires_api_core_lt_1_26_0 = pytest.mark.skipif(
    packaging.version.parse(_API_CORE_VERSION) >= packaging.version.parse("1.26.0"),
    reason="This test requires google-api-core < 1.26.0",
)

requires_api_core_gte_1_26_0 = pytest.mark.skipif(
    packaging.version.parse(_API_CORE_VERSION) < packaging.version.parse("1.26.0"),
    reason="This test requires google-api-core >= 1.26.0",
)


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert LanguageServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        LanguageServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        LanguageServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        LanguageServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        LanguageServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        LanguageServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [LanguageServiceClient, LanguageServiceAsyncClient,]
)
def test_language_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "language.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [LanguageServiceClient, LanguageServiceAsyncClient,]
)
def test_language_service_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "language.googleapis.com:443"


def test_language_service_client_get_transport_class():
    transport = LanguageServiceClient.get_transport_class()
    available_transports = [
        transports.LanguageServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = LanguageServiceClient.get_transport_class("grpc")
    assert transport == transports.LanguageServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (LanguageServiceClient, transports.LanguageServiceGrpcTransport, "grpc"),
        (
            LanguageServiceAsyncClient,
            transports.LanguageServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    LanguageServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(LanguageServiceClient),
)
@mock.patch.object(
    LanguageServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(LanguageServiceAsyncClient),
)
def test_language_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(LanguageServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(LanguageServiceClient, "get_transport_class") as gtc:
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
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            LanguageServiceClient,
            transports.LanguageServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            LanguageServiceAsyncClient,
            transports.LanguageServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            LanguageServiceClient,
            transports.LanguageServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            LanguageServiceAsyncClient,
            transports.LanguageServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    LanguageServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(LanguageServiceClient),
)
@mock.patch.object(
    LanguageServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(LanguageServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_language_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
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
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (LanguageServiceClient, transports.LanguageServiceGrpcTransport, "grpc"),
        (
            LanguageServiceAsyncClient,
            transports.LanguageServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_language_service_client_client_options_scopes(
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
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (LanguageServiceClient, transports.LanguageServiceGrpcTransport, "grpc"),
        (
            LanguageServiceAsyncClient,
            transports.LanguageServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_language_service_client_client_options_credentials_file(
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
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_language_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.language_v1beta2.services.language_service.transports.LanguageServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = LanguageServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_analyze_sentiment(
    transport: str = "grpc", request_type=language_service.AnalyzeSentimentRequest
):
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeSentimentResponse(
            language="language_value",
        )
        response = client.analyze_sentiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeSentimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeSentimentResponse)
    assert response.language == "language_value"


def test_analyze_sentiment_from_dict():
    test_analyze_sentiment(request_type=dict)


def test_analyze_sentiment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_sentiment), "__call__"
    ) as call:
        client.analyze_sentiment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeSentimentRequest()


@pytest.mark.asyncio
async def test_analyze_sentiment_async(
    transport: str = "grpc_asyncio",
    request_type=language_service.AnalyzeSentimentRequest,
):
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnalyzeSentimentResponse(language="language_value",)
        )
        response = await client.analyze_sentiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeSentimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeSentimentResponse)
    assert response.language == "language_value"


@pytest.mark.asyncio
async def test_analyze_sentiment_async_from_dict():
    await test_analyze_sentiment_async(request_type=dict)


def test_analyze_sentiment_flattened():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeSentimentResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.analyze_sentiment(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


def test_analyze_sentiment_flattened_error():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.analyze_sentiment(
            language_service.AnalyzeSentimentRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )


@pytest.mark.asyncio
async def test_analyze_sentiment_flattened_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeSentimentResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnalyzeSentimentResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.analyze_sentiment(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


@pytest.mark.asyncio
async def test_analyze_sentiment_flattened_error_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.analyze_sentiment(
            language_service.AnalyzeSentimentRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )


def test_analyze_entities(
    transport: str = "grpc", request_type=language_service.AnalyzeEntitiesRequest
):
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_entities), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeEntitiesResponse(
            language="language_value",
        )
        response = client.analyze_entities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeEntitiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeEntitiesResponse)
    assert response.language == "language_value"


def test_analyze_entities_from_dict():
    test_analyze_entities(request_type=dict)


def test_analyze_entities_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_entities), "__call__") as call:
        client.analyze_entities()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeEntitiesRequest()


@pytest.mark.asyncio
async def test_analyze_entities_async(
    transport: str = "grpc_asyncio",
    request_type=language_service.AnalyzeEntitiesRequest,
):
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_entities), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnalyzeEntitiesResponse(language="language_value",)
        )
        response = await client.analyze_entities(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeEntitiesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeEntitiesResponse)
    assert response.language == "language_value"


@pytest.mark.asyncio
async def test_analyze_entities_async_from_dict():
    await test_analyze_entities_async(request_type=dict)


def test_analyze_entities_flattened():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_entities), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeEntitiesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.analyze_entities(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


def test_analyze_entities_flattened_error():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.analyze_entities(
            language_service.AnalyzeEntitiesRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )


@pytest.mark.asyncio
async def test_analyze_entities_flattened_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_entities), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeEntitiesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnalyzeEntitiesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.analyze_entities(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


@pytest.mark.asyncio
async def test_analyze_entities_flattened_error_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.analyze_entities(
            language_service.AnalyzeEntitiesRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )


def test_analyze_entity_sentiment(
    transport: str = "grpc", request_type=language_service.AnalyzeEntitySentimentRequest
):
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_entity_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeEntitySentimentResponse(
            language="language_value",
        )
        response = client.analyze_entity_sentiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeEntitySentimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeEntitySentimentResponse)
    assert response.language == "language_value"


def test_analyze_entity_sentiment_from_dict():
    test_analyze_entity_sentiment(request_type=dict)


def test_analyze_entity_sentiment_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_entity_sentiment), "__call__"
    ) as call:
        client.analyze_entity_sentiment()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeEntitySentimentRequest()


@pytest.mark.asyncio
async def test_analyze_entity_sentiment_async(
    transport: str = "grpc_asyncio",
    request_type=language_service.AnalyzeEntitySentimentRequest,
):
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_entity_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnalyzeEntitySentimentResponse(language="language_value",)
        )
        response = await client.analyze_entity_sentiment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeEntitySentimentRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeEntitySentimentResponse)
    assert response.language == "language_value"


@pytest.mark.asyncio
async def test_analyze_entity_sentiment_async_from_dict():
    await test_analyze_entity_sentiment_async(request_type=dict)


def test_analyze_entity_sentiment_flattened():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_entity_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeEntitySentimentResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.analyze_entity_sentiment(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


def test_analyze_entity_sentiment_flattened_error():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.analyze_entity_sentiment(
            language_service.AnalyzeEntitySentimentRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )


@pytest.mark.asyncio
async def test_analyze_entity_sentiment_flattened_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.analyze_entity_sentiment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeEntitySentimentResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnalyzeEntitySentimentResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.analyze_entity_sentiment(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


@pytest.mark.asyncio
async def test_analyze_entity_sentiment_flattened_error_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.analyze_entity_sentiment(
            language_service.AnalyzeEntitySentimentRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )


def test_analyze_syntax(
    transport: str = "grpc", request_type=language_service.AnalyzeSyntaxRequest
):
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_syntax), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeSyntaxResponse(
            language="language_value",
        )
        response = client.analyze_syntax(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeSyntaxRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeSyntaxResponse)
    assert response.language == "language_value"


def test_analyze_syntax_from_dict():
    test_analyze_syntax(request_type=dict)


def test_analyze_syntax_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_syntax), "__call__") as call:
        client.analyze_syntax()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeSyntaxRequest()


@pytest.mark.asyncio
async def test_analyze_syntax_async(
    transport: str = "grpc_asyncio", request_type=language_service.AnalyzeSyntaxRequest
):
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_syntax), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnalyzeSyntaxResponse(language="language_value",)
        )
        response = await client.analyze_syntax(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnalyzeSyntaxRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnalyzeSyntaxResponse)
    assert response.language == "language_value"


@pytest.mark.asyncio
async def test_analyze_syntax_async_from_dict():
    await test_analyze_syntax_async(request_type=dict)


def test_analyze_syntax_flattened():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_syntax), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeSyntaxResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.analyze_syntax(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


def test_analyze_syntax_flattened_error():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.analyze_syntax(
            language_service.AnalyzeSyntaxRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )


@pytest.mark.asyncio
async def test_analyze_syntax_flattened_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.analyze_syntax), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnalyzeSyntaxResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnalyzeSyntaxResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.analyze_syntax(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


@pytest.mark.asyncio
async def test_analyze_syntax_flattened_error_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.analyze_syntax(
            language_service.AnalyzeSyntaxRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            encoding_type=language_service.EncodingType.UTF8,
        )


def test_classify_text(
    transport: str = "grpc", request_type=language_service.ClassifyTextRequest
):
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.classify_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.ClassifyTextResponse()
        response = client.classify_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.ClassifyTextRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.ClassifyTextResponse)


def test_classify_text_from_dict():
    test_classify_text(request_type=dict)


def test_classify_text_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.classify_text), "__call__") as call:
        client.classify_text()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.ClassifyTextRequest()


@pytest.mark.asyncio
async def test_classify_text_async(
    transport: str = "grpc_asyncio", request_type=language_service.ClassifyTextRequest
):
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.classify_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.ClassifyTextResponse()
        )
        response = await client.classify_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.ClassifyTextRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.ClassifyTextResponse)


@pytest.mark.asyncio
async def test_classify_text_async_from_dict():
    await test_classify_text_async(request_type=dict)


def test_classify_text_flattened():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.classify_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.ClassifyTextResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.classify_text(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )


def test_classify_text_flattened_error():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.classify_text(
            language_service.ClassifyTextRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
        )


@pytest.mark.asyncio
async def test_classify_text_flattened_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.classify_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.ClassifyTextResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.ClassifyTextResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.classify_text(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )


@pytest.mark.asyncio
async def test_classify_text_flattened_error_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.classify_text(
            language_service.ClassifyTextRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
        )


def test_annotate_text(
    transport: str = "grpc", request_type=language_service.AnnotateTextRequest
):
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.annotate_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnnotateTextResponse(
            language="language_value",
        )
        response = client.annotate_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnnotateTextRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnnotateTextResponse)
    assert response.language == "language_value"


def test_annotate_text_from_dict():
    test_annotate_text(request_type=dict)


def test_annotate_text_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.annotate_text), "__call__") as call:
        client.annotate_text()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnnotateTextRequest()


@pytest.mark.asyncio
async def test_annotate_text_async(
    transport: str = "grpc_asyncio", request_type=language_service.AnnotateTextRequest
):
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.annotate_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnnotateTextResponse(language="language_value",)
        )
        response = await client.annotate_text(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == language_service.AnnotateTextRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, language_service.AnnotateTextResponse)
    assert response.language == "language_value"


@pytest.mark.asyncio
async def test_annotate_text_async_from_dict():
    await test_annotate_text_async(request_type=dict)


def test_annotate_text_flattened():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.annotate_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnnotateTextResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.annotate_text(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            features=language_service.AnnotateTextRequest.Features(extract_syntax=True),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].features == language_service.AnnotateTextRequest.Features(
            extract_syntax=True
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


def test_annotate_text_flattened_error():
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.annotate_text(
            language_service.AnnotateTextRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            features=language_service.AnnotateTextRequest.Features(extract_syntax=True),
            encoding_type=language_service.EncodingType.UTF8,
        )


@pytest.mark.asyncio
async def test_annotate_text_flattened_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.annotate_text), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = language_service.AnnotateTextResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            language_service.AnnotateTextResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.annotate_text(
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            features=language_service.AnnotateTextRequest.Features(extract_syntax=True),
            encoding_type=language_service.EncodingType.UTF8,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].document == language_service.Document(
            type_=language_service.Document.Type.PLAIN_TEXT
        )
        assert args[0].features == language_service.AnnotateTextRequest.Features(
            extract_syntax=True
        )
        assert args[0].encoding_type == language_service.EncodingType.UTF8


@pytest.mark.asyncio
async def test_annotate_text_flattened_error_async():
    client = LanguageServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.annotate_text(
            language_service.AnnotateTextRequest(),
            document=language_service.Document(
                type_=language_service.Document.Type.PLAIN_TEXT
            ),
            features=language_service.AnnotateTextRequest.Features(extract_syntax=True),
            encoding_type=language_service.EncodingType.UTF8,
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.LanguageServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = LanguageServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.LanguageServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = LanguageServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.LanguageServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = LanguageServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.LanguageServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = LanguageServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.LanguageServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.LanguageServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LanguageServiceGrpcTransport,
        transports.LanguageServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = LanguageServiceClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.LanguageServiceGrpcTransport,)


def test_language_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.LanguageServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_language_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.language_v1beta2.services.language_service.transports.LanguageServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.LanguageServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "analyze_sentiment",
        "analyze_entities",
        "analyze_entity_sentiment",
        "analyze_syntax",
        "classify_text",
        "annotate_text",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_language_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.language_v1beta2.services.language_service.transports.LanguageServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.LanguageServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_language_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.language_v1beta2.services.language_service.transports.LanguageServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.LanguageServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_language_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.language_v1beta2.services.language_service.transports.LanguageServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.LanguageServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_language_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        LanguageServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_language_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        LanguageServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LanguageServiceGrpcTransport,
        transports.LanguageServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_language_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LanguageServiceGrpcTransport,
        transports.LanguageServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_language_service_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.LanguageServiceGrpcTransport, grpc_helpers),
        (transports.LanguageServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
@requires_api_core_gte_1_26_0
def test_language_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "language.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            scopes=["1", "2"],
            default_host="language.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.LanguageServiceGrpcTransport, grpc_helpers),
        (transports.LanguageServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
@requires_api_core_lt_1_26_0
def test_language_service_transport_create_channel_old_api_core(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus")

        create_channel.assert_called_with(
            "language.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.LanguageServiceGrpcTransport, grpc_helpers),
        (transports.LanguageServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
@requires_api_core_lt_1_26_0
def test_language_service_transport_create_channel_user_scopes(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)

        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "language.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            scopes=["1", "2"],
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LanguageServiceGrpcTransport,
        transports.LanguageServiceGrpcAsyncIOTransport,
    ],
)
def test_language_service_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=(
                "https://www.googleapis.com/auth/cloud-language",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_language_service_host_no_port():
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="language.googleapis.com"
        ),
    )
    assert client.transport._host == "language.googleapis.com:443"


def test_language_service_host_with_port():
    client = LanguageServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="language.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "language.googleapis.com:8000"


def test_language_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.LanguageServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_language_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.LanguageServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LanguageServiceGrpcTransport,
        transports.LanguageServiceGrpcAsyncIOTransport,
    ],
)
def test_language_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-language",
                    "https://www.googleapis.com/auth/cloud-platform",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.LanguageServiceGrpcTransport,
        transports.LanguageServiceGrpcAsyncIOTransport,
    ],
)
def test_language_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-language",
                    "https://www.googleapis.com/auth/cloud-platform",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = LanguageServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = LanguageServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = LanguageServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = LanguageServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = LanguageServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = LanguageServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = LanguageServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = LanguageServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = LanguageServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = LanguageServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = LanguageServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = LanguageServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = LanguageServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = LanguageServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = LanguageServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.LanguageServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = LanguageServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.LanguageServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = LanguageServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
