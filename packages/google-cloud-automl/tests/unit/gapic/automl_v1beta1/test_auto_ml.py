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
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.automl_v1beta1.services.auto_ml import AutoMlAsyncClient
from google.cloud.automl_v1beta1.services.auto_ml import AutoMlClient
from google.cloud.automl_v1beta1.services.auto_ml import pagers
from google.cloud.automl_v1beta1.services.auto_ml import transports
from google.cloud.automl_v1beta1.services.auto_ml.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.automl_v1beta1.types import annotation_spec
from google.cloud.automl_v1beta1.types import classification
from google.cloud.automl_v1beta1.types import column_spec
from google.cloud.automl_v1beta1.types import column_spec as gca_column_spec
from google.cloud.automl_v1beta1.types import data_stats
from google.cloud.automl_v1beta1.types import data_types
from google.cloud.automl_v1beta1.types import dataset
from google.cloud.automl_v1beta1.types import dataset as gca_dataset
from google.cloud.automl_v1beta1.types import detection
from google.cloud.automl_v1beta1.types import image
from google.cloud.automl_v1beta1.types import io
from google.cloud.automl_v1beta1.types import model
from google.cloud.automl_v1beta1.types import model as gca_model
from google.cloud.automl_v1beta1.types import model_evaluation
from google.cloud.automl_v1beta1.types import operations
from google.cloud.automl_v1beta1.types import regression
from google.cloud.automl_v1beta1.types import service
from google.cloud.automl_v1beta1.types import table_spec
from google.cloud.automl_v1beta1.types import table_spec as gca_table_spec
from google.cloud.automl_v1beta1.types import tables
from google.cloud.automl_v1beta1.types import text
from google.cloud.automl_v1beta1.types import text_extraction
from google.cloud.automl_v1beta1.types import text_sentiment
from google.cloud.automl_v1beta1.types import translation
from google.cloud.automl_v1beta1.types import video
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


# TODO(busunkim): Once google-auth >= 1.25.0 is required transitively
# through google-api-core:
# - Delete the auth "less than" test cases
# - Delete these pytest markers (Make the "greater than or equal to" tests the default).
requires_google_auth_lt_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) >= packaging.version.parse("1.25.0"),
    reason="This test requires google-auth < 1.25.0",
)
requires_google_auth_gte_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) < packaging.version.parse("1.25.0"),
    reason="This test requires google-auth >= 1.25.0",
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

    assert AutoMlClient._get_default_mtls_endpoint(None) is None
    assert AutoMlClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        AutoMlClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    )
    assert (
        AutoMlClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AutoMlClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert AutoMlClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [AutoMlClient, AutoMlAsyncClient,])
def test_auto_ml_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "automl.googleapis.com:443"


@pytest.mark.parametrize("client_class", [AutoMlClient, AutoMlAsyncClient,])
def test_auto_ml_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.AutoMlGrpcTransport, "grpc"),
        (transports.AutoMlGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_auto_ml_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize("client_class", [AutoMlClient, AutoMlAsyncClient,])
def test_auto_ml_client_from_service_account_file(client_class):
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

        assert client.transport._host == "automl.googleapis.com:443"


def test_auto_ml_client_get_transport_class():
    transport = AutoMlClient.get_transport_class()
    available_transports = [
        transports.AutoMlGrpcTransport,
    ]
    assert transport in available_transports

    transport = AutoMlClient.get_transport_class("grpc")
    assert transport == transports.AutoMlGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (AutoMlClient, transports.AutoMlGrpcTransport, "grpc"),
        (AutoMlAsyncClient, transports.AutoMlGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
@mock.patch.object(
    AutoMlClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AutoMlClient)
)
@mock.patch.object(
    AutoMlAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AutoMlAsyncClient)
)
def test_auto_ml_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AutoMlClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AutoMlClient, "get_transport_class") as gtc:
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
        (AutoMlClient, transports.AutoMlGrpcTransport, "grpc", "true"),
        (
            AutoMlAsyncClient,
            transports.AutoMlGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (AutoMlClient, transports.AutoMlGrpcTransport, "grpc", "false"),
        (
            AutoMlAsyncClient,
            transports.AutoMlGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    AutoMlClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AutoMlClient)
)
@mock.patch.object(
    AutoMlAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(AutoMlAsyncClient)
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_auto_ml_client_mtls_env_auto(
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
        (AutoMlClient, transports.AutoMlGrpcTransport, "grpc"),
        (AutoMlAsyncClient, transports.AutoMlGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_auto_ml_client_client_options_scopes(
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
        (AutoMlClient, transports.AutoMlGrpcTransport, "grpc"),
        (AutoMlAsyncClient, transports.AutoMlGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_auto_ml_client_client_options_credentials_file(
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


def test_auto_ml_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.automl_v1beta1.services.auto_ml.transports.AutoMlGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = AutoMlClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_dataset(
    transport: str = "grpc", request_type=service.CreateDatasetRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            example_count=1396,
            etag="etag_value",
            translation_dataset_metadata=translation.TranslationDatasetMetadata(
                source_language_code="source_language_code_value"
            ),
        )
        response = client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.example_count == 1396
    assert response.etag == "etag_value"


def test_create_dataset_from_dict():
    test_create_dataset(request_type=dict)


def test_create_dataset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        client.create_dataset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateDatasetRequest()


@pytest.mark.asyncio
async def test_create_dataset_async(
    transport: str = "grpc_asyncio", request_type=service.CreateDatasetRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_dataset.Dataset(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                example_count=1396,
                etag="etag_value",
            )
        )
        response = await client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.example_count == 1396
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_create_dataset_async_from_dict():
    await test_create_dataset_async(request_type=dict)


def test_create_dataset_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateDatasetRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        call.return_value = gca_dataset.Dataset()
        client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_dataset_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateDatasetRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gca_dataset.Dataset())
        await client.create_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_dataset_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_dataset.Dataset()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_dataset(
            parent="parent_value",
            dataset=gca_dataset.Dataset(
                translation_dataset_metadata=translation.TranslationDatasetMetadata(
                    source_language_code="source_language_code_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].dataset == gca_dataset.Dataset(
            translation_dataset_metadata=translation.TranslationDatasetMetadata(
                source_language_code="source_language_code_value"
            )
        )


def test_create_dataset_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_dataset(
            service.CreateDatasetRequest(),
            parent="parent_value",
            dataset=gca_dataset.Dataset(
                translation_dataset_metadata=translation.TranslationDatasetMetadata(
                    source_language_code="source_language_code_value"
                )
            ),
        )


@pytest.mark.asyncio
async def test_create_dataset_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_dataset.Dataset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gca_dataset.Dataset())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_dataset(
            parent="parent_value",
            dataset=gca_dataset.Dataset(
                translation_dataset_metadata=translation.TranslationDatasetMetadata(
                    source_language_code="source_language_code_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].dataset == gca_dataset.Dataset(
            translation_dataset_metadata=translation.TranslationDatasetMetadata(
                source_language_code="source_language_code_value"
            )
        )


@pytest.mark.asyncio
async def test_create_dataset_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_dataset(
            service.CreateDatasetRequest(),
            parent="parent_value",
            dataset=gca_dataset.Dataset(
                translation_dataset_metadata=translation.TranslationDatasetMetadata(
                    source_language_code="source_language_code_value"
                )
            ),
        )


def test_get_dataset(transport: str = "grpc", request_type=service.GetDatasetRequest):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            example_count=1396,
            etag="etag_value",
            translation_dataset_metadata=translation.TranslationDatasetMetadata(
                source_language_code="source_language_code_value"
            ),
        )
        response = client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.example_count == 1396
    assert response.etag == "etag_value"


def test_get_dataset_from_dict():
    test_get_dataset(request_type=dict)


def test_get_dataset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        client.get_dataset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetDatasetRequest()


@pytest.mark.asyncio
async def test_get_dataset_async(
    transport: str = "grpc_asyncio", request_type=service.GetDatasetRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            dataset.Dataset(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                example_count=1396,
                etag="etag_value",
            )
        )
        response = await client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.example_count == 1396
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_dataset_async_from_dict():
    await test_get_dataset_async(request_type=dict)


def test_get_dataset_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetDatasetRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        call.return_value = dataset.Dataset()
        client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_dataset_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetDatasetRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.Dataset())
        await client.get_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_dataset_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Dataset()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_dataset_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_dataset(
            service.GetDatasetRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_dataset_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = dataset.Dataset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(dataset.Dataset())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_dataset_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_dataset(
            service.GetDatasetRequest(), name="name_value",
        )


def test_list_datasets(
    transport: str = "grpc", request_type=service.ListDatasetsRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListDatasetsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListDatasetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_datasets_from_dict():
    test_list_datasets(request_type=dict)


def test_list_datasets_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        client.list_datasets()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListDatasetsRequest()


@pytest.mark.asyncio
async def test_list_datasets_async(
    transport: str = "grpc_asyncio", request_type=service.ListDatasetsRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListDatasetsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListDatasetsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListDatasetsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_datasets_async_from_dict():
    await test_list_datasets_async(request_type=dict)


def test_list_datasets_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListDatasetsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        call.return_value = service.ListDatasetsResponse()
        client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_datasets_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListDatasetsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListDatasetsResponse()
        )
        await client.list_datasets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_datasets_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListDatasetsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_datasets(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_datasets_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_datasets(
            service.ListDatasetsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_datasets_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListDatasetsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListDatasetsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_datasets(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_datasets_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_datasets(
            service.ListDatasetsRequest(), parent="parent_value",
        )


def test_list_datasets_pager():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(), dataset.Dataset(),],
                next_page_token="abc",
            ),
            service.ListDatasetsResponse(datasets=[], next_page_token="def",),
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(),], next_page_token="ghi",
            ),
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_datasets(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, dataset.Dataset) for i in results)


def test_list_datasets_pages():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_datasets), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(), dataset.Dataset(),],
                next_page_token="abc",
            ),
            service.ListDatasetsResponse(datasets=[], next_page_token="def",),
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(),], next_page_token="ghi",
            ),
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_datasets(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_datasets_async_pager():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datasets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(), dataset.Dataset(),],
                next_page_token="abc",
            ),
            service.ListDatasetsResponse(datasets=[], next_page_token="def",),
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(),], next_page_token="ghi",
            ),
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_datasets(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, dataset.Dataset) for i in responses)


@pytest.mark.asyncio
async def test_list_datasets_async_pages():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_datasets), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(), dataset.Dataset(),],
                next_page_token="abc",
            ),
            service.ListDatasetsResponse(datasets=[], next_page_token="def",),
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(),], next_page_token="ghi",
            ),
            service.ListDatasetsResponse(
                datasets=[dataset.Dataset(), dataset.Dataset(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_datasets(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_dataset(
    transport: str = "grpc", request_type=service.UpdateDatasetRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_dataset.Dataset(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            example_count=1396,
            etag="etag_value",
            translation_dataset_metadata=translation.TranslationDatasetMetadata(
                source_language_code="source_language_code_value"
            ),
        )
        response = client.update_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.example_count == 1396
    assert response.etag == "etag_value"


def test_update_dataset_from_dict():
    test_update_dataset(request_type=dict)


def test_update_dataset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_dataset), "__call__") as call:
        client.update_dataset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateDatasetRequest()


@pytest.mark.asyncio
async def test_update_dataset_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateDatasetRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_dataset.Dataset(
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                example_count=1396,
                etag="etag_value",
            )
        )
        response = await client.update_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_dataset.Dataset)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.example_count == 1396
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_update_dataset_async_from_dict():
    await test_update_dataset_async(request_type=dict)


def test_update_dataset_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateDatasetRequest()

    request.dataset.name = "dataset.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_dataset), "__call__") as call:
        call.return_value = gca_dataset.Dataset()
        client.update_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "dataset.name=dataset.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_dataset_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateDatasetRequest()

    request.dataset.name = "dataset.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_dataset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gca_dataset.Dataset())
        await client.update_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "dataset.name=dataset.name/value",) in kw[
        "metadata"
    ]


def test_update_dataset_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_dataset.Dataset()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_dataset(
            dataset=gca_dataset.Dataset(
                translation_dataset_metadata=translation.TranslationDatasetMetadata(
                    source_language_code="source_language_code_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].dataset == gca_dataset.Dataset(
            translation_dataset_metadata=translation.TranslationDatasetMetadata(
                source_language_code="source_language_code_value"
            )
        )


def test_update_dataset_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_dataset(
            service.UpdateDatasetRequest(),
            dataset=gca_dataset.Dataset(
                translation_dataset_metadata=translation.TranslationDatasetMetadata(
                    source_language_code="source_language_code_value"
                )
            ),
        )


@pytest.mark.asyncio
async def test_update_dataset_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_dataset.Dataset()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gca_dataset.Dataset())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_dataset(
            dataset=gca_dataset.Dataset(
                translation_dataset_metadata=translation.TranslationDatasetMetadata(
                    source_language_code="source_language_code_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].dataset == gca_dataset.Dataset(
            translation_dataset_metadata=translation.TranslationDatasetMetadata(
                source_language_code="source_language_code_value"
            )
        )


@pytest.mark.asyncio
async def test_update_dataset_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_dataset(
            service.UpdateDatasetRequest(),
            dataset=gca_dataset.Dataset(
                translation_dataset_metadata=translation.TranslationDatasetMetadata(
                    source_language_code="source_language_code_value"
                )
            ),
        )


def test_delete_dataset(
    transport: str = "grpc", request_type=service.DeleteDatasetRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_dataset_from_dict():
    test_delete_dataset(request_type=dict)


def test_delete_dataset_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        client.delete_dataset()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteDatasetRequest()


@pytest.mark.asyncio
async def test_delete_dataset_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteDatasetRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteDatasetRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_dataset_async_from_dict():
    await test_delete_dataset_async(request_type=dict)


def test_delete_dataset_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteDatasetRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_dataset_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteDatasetRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_dataset(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_dataset_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_dataset_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_dataset(
            service.DeleteDatasetRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_dataset_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_dataset), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_dataset(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_dataset_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_dataset(
            service.DeleteDatasetRequest(), name="name_value",
        )


def test_import_data(transport: str = "grpc", request_type=service.ImportDataRequest):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ImportDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_data_from_dict():
    test_import_data(request_type=dict)


def test_import_data_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_data), "__call__") as call:
        client.import_data()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ImportDataRequest()


@pytest.mark.asyncio
async def test_import_data_async(
    transport: str = "grpc_asyncio", request_type=service.ImportDataRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ImportDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_data_async_from_dict():
    await test_import_data_async(request_type=dict)


def test_import_data_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ImportDataRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_data), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_data_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ImportDataRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_data), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_import_data_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.import_data(
            name="name_value",
            input_config=io.InputConfig(
                gcs_source=io.GcsSource(input_uris=["input_uris_value"])
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].input_config == io.InputConfig(
            gcs_source=io.GcsSource(input_uris=["input_uris_value"])
        )


def test_import_data_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.import_data(
            service.ImportDataRequest(),
            name="name_value",
            input_config=io.InputConfig(
                gcs_source=io.GcsSource(input_uris=["input_uris_value"])
            ),
        )


@pytest.mark.asyncio
async def test_import_data_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.import_data(
            name="name_value",
            input_config=io.InputConfig(
                gcs_source=io.GcsSource(input_uris=["input_uris_value"])
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].input_config == io.InputConfig(
            gcs_source=io.GcsSource(input_uris=["input_uris_value"])
        )


@pytest.mark.asyncio
async def test_import_data_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.import_data(
            service.ImportDataRequest(),
            name="name_value",
            input_config=io.InputConfig(
                gcs_source=io.GcsSource(input_uris=["input_uris_value"])
            ),
        )


def test_export_data(transport: str = "grpc", request_type=service.ExportDataRequest):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.export_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ExportDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_data_from_dict():
    test_export_data(request_type=dict)


def test_export_data_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_data), "__call__") as call:
        client.export_data()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ExportDataRequest()


@pytest.mark.asyncio
async def test_export_data_async(
    transport: str = "grpc_asyncio", request_type=service.ExportDataRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.export_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ExportDataRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_data_async_from_dict():
    await test_export_data_async(request_type=dict)


def test_export_data_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ExportDataRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_data), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.export_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_data_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ExportDataRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_data), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.export_data(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_export_data_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_data(
            name="name_value",
            output_config=io.OutputConfig(
                gcs_destination=io.GcsDestination(
                    output_uri_prefix="output_uri_prefix_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].output_config == io.OutputConfig(
            gcs_destination=io.GcsDestination(
                output_uri_prefix="output_uri_prefix_value"
            )
        )


def test_export_data_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_data(
            service.ExportDataRequest(),
            name="name_value",
            output_config=io.OutputConfig(
                gcs_destination=io.GcsDestination(
                    output_uri_prefix="output_uri_prefix_value"
                )
            ),
        )


@pytest.mark.asyncio
async def test_export_data_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_data), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.export_data(
            name="name_value",
            output_config=io.OutputConfig(
                gcs_destination=io.GcsDestination(
                    output_uri_prefix="output_uri_prefix_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].output_config == io.OutputConfig(
            gcs_destination=io.GcsDestination(
                output_uri_prefix="output_uri_prefix_value"
            )
        )


@pytest.mark.asyncio
async def test_export_data_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_data(
            service.ExportDataRequest(),
            name="name_value",
            output_config=io.OutputConfig(
                gcs_destination=io.GcsDestination(
                    output_uri_prefix="output_uri_prefix_value"
                )
            ),
        )


def test_get_annotation_spec(
    transport: str = "grpc", request_type=service.GetAnnotationSpecRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_annotation_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = annotation_spec.AnnotationSpec(
            name="name_value", display_name="display_name_value", example_count=1396,
        )
        response = client.get_annotation_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetAnnotationSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, annotation_spec.AnnotationSpec)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.example_count == 1396


def test_get_annotation_spec_from_dict():
    test_get_annotation_spec(request_type=dict)


def test_get_annotation_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_annotation_spec), "__call__"
    ) as call:
        client.get_annotation_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetAnnotationSpecRequest()


@pytest.mark.asyncio
async def test_get_annotation_spec_async(
    transport: str = "grpc_asyncio", request_type=service.GetAnnotationSpecRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_annotation_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            annotation_spec.AnnotationSpec(
                name="name_value",
                display_name="display_name_value",
                example_count=1396,
            )
        )
        response = await client.get_annotation_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetAnnotationSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, annotation_spec.AnnotationSpec)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.example_count == 1396


@pytest.mark.asyncio
async def test_get_annotation_spec_async_from_dict():
    await test_get_annotation_spec_async(request_type=dict)


def test_get_annotation_spec_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetAnnotationSpecRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_annotation_spec), "__call__"
    ) as call:
        call.return_value = annotation_spec.AnnotationSpec()
        client.get_annotation_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_annotation_spec_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetAnnotationSpecRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_annotation_spec), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            annotation_spec.AnnotationSpec()
        )
        await client.get_annotation_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_annotation_spec_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_annotation_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = annotation_spec.AnnotationSpec()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_annotation_spec(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_annotation_spec_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_annotation_spec(
            service.GetAnnotationSpecRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_annotation_spec_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_annotation_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = annotation_spec.AnnotationSpec()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            annotation_spec.AnnotationSpec()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_annotation_spec(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_annotation_spec_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_annotation_spec(
            service.GetAnnotationSpecRequest(), name="name_value",
        )


def test_get_table_spec(
    transport: str = "grpc", request_type=service.GetTableSpecRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table_spec.TableSpec(
            name="name_value",
            time_column_spec_id="time_column_spec_id_value",
            row_count=992,
            valid_row_count=1615,
            column_count=1302,
            etag="etag_value",
        )
        response = client.get_table_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetTableSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table_spec.TableSpec)
    assert response.name == "name_value"
    assert response.time_column_spec_id == "time_column_spec_id_value"
    assert response.row_count == 992
    assert response.valid_row_count == 1615
    assert response.column_count == 1302
    assert response.etag == "etag_value"


def test_get_table_spec_from_dict():
    test_get_table_spec(request_type=dict)


def test_get_table_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table_spec), "__call__") as call:
        client.get_table_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetTableSpecRequest()


@pytest.mark.asyncio
async def test_get_table_spec_async(
    transport: str = "grpc_asyncio", request_type=service.GetTableSpecRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            table_spec.TableSpec(
                name="name_value",
                time_column_spec_id="time_column_spec_id_value",
                row_count=992,
                valid_row_count=1615,
                column_count=1302,
                etag="etag_value",
            )
        )
        response = await client.get_table_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetTableSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, table_spec.TableSpec)
    assert response.name == "name_value"
    assert response.time_column_spec_id == "time_column_spec_id_value"
    assert response.row_count == 992
    assert response.valid_row_count == 1615
    assert response.column_count == 1302
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_table_spec_async_from_dict():
    await test_get_table_spec_async(request_type=dict)


def test_get_table_spec_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetTableSpecRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table_spec), "__call__") as call:
        call.return_value = table_spec.TableSpec()
        client.get_table_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_table_spec_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetTableSpecRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table_spec), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            table_spec.TableSpec()
        )
        await client.get_table_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_table_spec_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table_spec.TableSpec()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_table_spec(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_table_spec_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_table_spec(
            service.GetTableSpecRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_table_spec_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_table_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = table_spec.TableSpec()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            table_spec.TableSpec()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_table_spec(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_table_spec_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_table_spec(
            service.GetTableSpecRequest(), name="name_value",
        )


def test_list_table_specs(
    transport: str = "grpc", request_type=service.ListTableSpecsRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_table_specs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListTableSpecsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_table_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTableSpecsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTableSpecsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_table_specs_from_dict():
    test_list_table_specs(request_type=dict)


def test_list_table_specs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_table_specs), "__call__") as call:
        client.list_table_specs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTableSpecsRequest()


@pytest.mark.asyncio
async def test_list_table_specs_async(
    transport: str = "grpc_asyncio", request_type=service.ListTableSpecsRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_table_specs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTableSpecsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_table_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListTableSpecsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTableSpecsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_table_specs_async_from_dict():
    await test_list_table_specs_async(request_type=dict)


def test_list_table_specs_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListTableSpecsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_table_specs), "__call__") as call:
        call.return_value = service.ListTableSpecsResponse()
        client.list_table_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_table_specs_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListTableSpecsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_table_specs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTableSpecsResponse()
        )
        await client.list_table_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_table_specs_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_table_specs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListTableSpecsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_table_specs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_table_specs_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_table_specs(
            service.ListTableSpecsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_table_specs_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_table_specs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListTableSpecsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListTableSpecsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_table_specs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_table_specs_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_table_specs(
            service.ListTableSpecsRequest(), parent="parent_value",
        )


def test_list_table_specs_pager():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_table_specs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTableSpecsResponse(
                table_specs=[
                    table_spec.TableSpec(),
                    table_spec.TableSpec(),
                    table_spec.TableSpec(),
                ],
                next_page_token="abc",
            ),
            service.ListTableSpecsResponse(table_specs=[], next_page_token="def",),
            service.ListTableSpecsResponse(
                table_specs=[table_spec.TableSpec(),], next_page_token="ghi",
            ),
            service.ListTableSpecsResponse(
                table_specs=[table_spec.TableSpec(), table_spec.TableSpec(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_table_specs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, table_spec.TableSpec) for i in results)


def test_list_table_specs_pages():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_table_specs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTableSpecsResponse(
                table_specs=[
                    table_spec.TableSpec(),
                    table_spec.TableSpec(),
                    table_spec.TableSpec(),
                ],
                next_page_token="abc",
            ),
            service.ListTableSpecsResponse(table_specs=[], next_page_token="def",),
            service.ListTableSpecsResponse(
                table_specs=[table_spec.TableSpec(),], next_page_token="ghi",
            ),
            service.ListTableSpecsResponse(
                table_specs=[table_spec.TableSpec(), table_spec.TableSpec(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_table_specs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_table_specs_async_pager():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_table_specs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTableSpecsResponse(
                table_specs=[
                    table_spec.TableSpec(),
                    table_spec.TableSpec(),
                    table_spec.TableSpec(),
                ],
                next_page_token="abc",
            ),
            service.ListTableSpecsResponse(table_specs=[], next_page_token="def",),
            service.ListTableSpecsResponse(
                table_specs=[table_spec.TableSpec(),], next_page_token="ghi",
            ),
            service.ListTableSpecsResponse(
                table_specs=[table_spec.TableSpec(), table_spec.TableSpec(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_table_specs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, table_spec.TableSpec) for i in responses)


@pytest.mark.asyncio
async def test_list_table_specs_async_pages():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_table_specs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListTableSpecsResponse(
                table_specs=[
                    table_spec.TableSpec(),
                    table_spec.TableSpec(),
                    table_spec.TableSpec(),
                ],
                next_page_token="abc",
            ),
            service.ListTableSpecsResponse(table_specs=[], next_page_token="def",),
            service.ListTableSpecsResponse(
                table_specs=[table_spec.TableSpec(),], next_page_token="ghi",
            ),
            service.ListTableSpecsResponse(
                table_specs=[table_spec.TableSpec(), table_spec.TableSpec(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_table_specs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_table_spec(
    transport: str = "grpc", request_type=service.UpdateTableSpecRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_table_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_table_spec.TableSpec(
            name="name_value",
            time_column_spec_id="time_column_spec_id_value",
            row_count=992,
            valid_row_count=1615,
            column_count=1302,
            etag="etag_value",
        )
        response = client.update_table_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateTableSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_table_spec.TableSpec)
    assert response.name == "name_value"
    assert response.time_column_spec_id == "time_column_spec_id_value"
    assert response.row_count == 992
    assert response.valid_row_count == 1615
    assert response.column_count == 1302
    assert response.etag == "etag_value"


def test_update_table_spec_from_dict():
    test_update_table_spec(request_type=dict)


def test_update_table_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_table_spec), "__call__"
    ) as call:
        client.update_table_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateTableSpecRequest()


@pytest.mark.asyncio
async def test_update_table_spec_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateTableSpecRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_table_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_table_spec.TableSpec(
                name="name_value",
                time_column_spec_id="time_column_spec_id_value",
                row_count=992,
                valid_row_count=1615,
                column_count=1302,
                etag="etag_value",
            )
        )
        response = await client.update_table_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateTableSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_table_spec.TableSpec)
    assert response.name == "name_value"
    assert response.time_column_spec_id == "time_column_spec_id_value"
    assert response.row_count == 992
    assert response.valid_row_count == 1615
    assert response.column_count == 1302
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_update_table_spec_async_from_dict():
    await test_update_table_spec_async(request_type=dict)


def test_update_table_spec_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateTableSpecRequest()

    request.table_spec.name = "table_spec.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_table_spec), "__call__"
    ) as call:
        call.return_value = gca_table_spec.TableSpec()
        client.update_table_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "table_spec.name=table_spec.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_table_spec_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateTableSpecRequest()

    request.table_spec.name = "table_spec.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_table_spec), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_table_spec.TableSpec()
        )
        await client.update_table_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "table_spec.name=table_spec.name/value",) in kw[
        "metadata"
    ]


def test_update_table_spec_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_table_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_table_spec.TableSpec()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_table_spec(
            table_spec=gca_table_spec.TableSpec(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].table_spec == gca_table_spec.TableSpec(name="name_value")


def test_update_table_spec_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_table_spec(
            service.UpdateTableSpecRequest(),
            table_spec=gca_table_spec.TableSpec(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_table_spec_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_table_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_table_spec.TableSpec()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_table_spec.TableSpec()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_table_spec(
            table_spec=gca_table_spec.TableSpec(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].table_spec == gca_table_spec.TableSpec(name="name_value")


@pytest.mark.asyncio
async def test_update_table_spec_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_table_spec(
            service.UpdateTableSpecRequest(),
            table_spec=gca_table_spec.TableSpec(name="name_value"),
        )


def test_get_column_spec(
    transport: str = "grpc", request_type=service.GetColumnSpecRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_column_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = column_spec.ColumnSpec(
            name="name_value", display_name="display_name_value", etag="etag_value",
        )
        response = client.get_column_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetColumnSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, column_spec.ColumnSpec)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.etag == "etag_value"


def test_get_column_spec_from_dict():
    test_get_column_spec(request_type=dict)


def test_get_column_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_column_spec), "__call__") as call:
        client.get_column_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetColumnSpecRequest()


@pytest.mark.asyncio
async def test_get_column_spec_async(
    transport: str = "grpc_asyncio", request_type=service.GetColumnSpecRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_column_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            column_spec.ColumnSpec(
                name="name_value", display_name="display_name_value", etag="etag_value",
            )
        )
        response = await client.get_column_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetColumnSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, column_spec.ColumnSpec)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_get_column_spec_async_from_dict():
    await test_get_column_spec_async(request_type=dict)


def test_get_column_spec_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetColumnSpecRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_column_spec), "__call__") as call:
        call.return_value = column_spec.ColumnSpec()
        client.get_column_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_column_spec_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetColumnSpecRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_column_spec), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            column_spec.ColumnSpec()
        )
        await client.get_column_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_column_spec_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_column_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = column_spec.ColumnSpec()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_column_spec(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_column_spec_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_column_spec(
            service.GetColumnSpecRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_column_spec_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_column_spec), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = column_spec.ColumnSpec()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            column_spec.ColumnSpec()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_column_spec(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_column_spec_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_column_spec(
            service.GetColumnSpecRequest(), name="name_value",
        )


def test_list_column_specs(
    transport: str = "grpc", request_type=service.ListColumnSpecsRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListColumnSpecsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_column_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListColumnSpecsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListColumnSpecsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_column_specs_from_dict():
    test_list_column_specs(request_type=dict)


def test_list_column_specs_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs), "__call__"
    ) as call:
        client.list_column_specs()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListColumnSpecsRequest()


@pytest.mark.asyncio
async def test_list_column_specs_async(
    transport: str = "grpc_asyncio", request_type=service.ListColumnSpecsRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListColumnSpecsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_column_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListColumnSpecsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListColumnSpecsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_column_specs_async_from_dict():
    await test_list_column_specs_async(request_type=dict)


def test_list_column_specs_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListColumnSpecsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs), "__call__"
    ) as call:
        call.return_value = service.ListColumnSpecsResponse()
        client.list_column_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_column_specs_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListColumnSpecsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListColumnSpecsResponse()
        )
        await client.list_column_specs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_column_specs_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListColumnSpecsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_column_specs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_column_specs_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_column_specs(
            service.ListColumnSpecsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_column_specs_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListColumnSpecsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListColumnSpecsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_column_specs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_column_specs_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_column_specs(
            service.ListColumnSpecsRequest(), parent="parent_value",
        )


def test_list_column_specs_pager():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListColumnSpecsResponse(
                column_specs=[
                    column_spec.ColumnSpec(),
                    column_spec.ColumnSpec(),
                    column_spec.ColumnSpec(),
                ],
                next_page_token="abc",
            ),
            service.ListColumnSpecsResponse(column_specs=[], next_page_token="def",),
            service.ListColumnSpecsResponse(
                column_specs=[column_spec.ColumnSpec(),], next_page_token="ghi",
            ),
            service.ListColumnSpecsResponse(
                column_specs=[column_spec.ColumnSpec(), column_spec.ColumnSpec(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_column_specs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, column_spec.ColumnSpec) for i in results)


def test_list_column_specs_pages():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListColumnSpecsResponse(
                column_specs=[
                    column_spec.ColumnSpec(),
                    column_spec.ColumnSpec(),
                    column_spec.ColumnSpec(),
                ],
                next_page_token="abc",
            ),
            service.ListColumnSpecsResponse(column_specs=[], next_page_token="def",),
            service.ListColumnSpecsResponse(
                column_specs=[column_spec.ColumnSpec(),], next_page_token="ghi",
            ),
            service.ListColumnSpecsResponse(
                column_specs=[column_spec.ColumnSpec(), column_spec.ColumnSpec(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_column_specs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_column_specs_async_pager():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListColumnSpecsResponse(
                column_specs=[
                    column_spec.ColumnSpec(),
                    column_spec.ColumnSpec(),
                    column_spec.ColumnSpec(),
                ],
                next_page_token="abc",
            ),
            service.ListColumnSpecsResponse(column_specs=[], next_page_token="def",),
            service.ListColumnSpecsResponse(
                column_specs=[column_spec.ColumnSpec(),], next_page_token="ghi",
            ),
            service.ListColumnSpecsResponse(
                column_specs=[column_spec.ColumnSpec(), column_spec.ColumnSpec(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_column_specs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, column_spec.ColumnSpec) for i in responses)


@pytest.mark.asyncio
async def test_list_column_specs_async_pages():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_column_specs),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListColumnSpecsResponse(
                column_specs=[
                    column_spec.ColumnSpec(),
                    column_spec.ColumnSpec(),
                    column_spec.ColumnSpec(),
                ],
                next_page_token="abc",
            ),
            service.ListColumnSpecsResponse(column_specs=[], next_page_token="def",),
            service.ListColumnSpecsResponse(
                column_specs=[column_spec.ColumnSpec(),], next_page_token="ghi",
            ),
            service.ListColumnSpecsResponse(
                column_specs=[column_spec.ColumnSpec(), column_spec.ColumnSpec(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_column_specs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_column_spec(
    transport: str = "grpc", request_type=service.UpdateColumnSpecRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_column_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_column_spec.ColumnSpec(
            name="name_value", display_name="display_name_value", etag="etag_value",
        )
        response = client.update_column_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateColumnSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_column_spec.ColumnSpec)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.etag == "etag_value"


def test_update_column_spec_from_dict():
    test_update_column_spec(request_type=dict)


def test_update_column_spec_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_column_spec), "__call__"
    ) as call:
        client.update_column_spec()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateColumnSpecRequest()


@pytest.mark.asyncio
async def test_update_column_spec_async(
    transport: str = "grpc_asyncio", request_type=service.UpdateColumnSpecRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_column_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_column_spec.ColumnSpec(
                name="name_value", display_name="display_name_value", etag="etag_value",
            )
        )
        response = await client.update_column_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UpdateColumnSpecRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gca_column_spec.ColumnSpec)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.etag == "etag_value"


@pytest.mark.asyncio
async def test_update_column_spec_async_from_dict():
    await test_update_column_spec_async(request_type=dict)


def test_update_column_spec_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateColumnSpecRequest()

    request.column_spec.name = "column_spec.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_column_spec), "__call__"
    ) as call:
        call.return_value = gca_column_spec.ColumnSpec()
        client.update_column_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "column_spec.name=column_spec.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_column_spec_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UpdateColumnSpecRequest()

    request.column_spec.name = "column_spec.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_column_spec), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_column_spec.ColumnSpec()
        )
        await client.update_column_spec(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "column_spec.name=column_spec.name/value",) in kw[
        "metadata"
    ]


def test_update_column_spec_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_column_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_column_spec.ColumnSpec()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_column_spec(
            column_spec=gca_column_spec.ColumnSpec(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].column_spec == gca_column_spec.ColumnSpec(name="name_value")


def test_update_column_spec_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_column_spec(
            service.UpdateColumnSpecRequest(),
            column_spec=gca_column_spec.ColumnSpec(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_column_spec_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_column_spec), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gca_column_spec.ColumnSpec()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gca_column_spec.ColumnSpec()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_column_spec(
            column_spec=gca_column_spec.ColumnSpec(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].column_spec == gca_column_spec.ColumnSpec(name="name_value")


@pytest.mark.asyncio
async def test_update_column_spec_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_column_spec(
            service.UpdateColumnSpecRequest(),
            column_spec=gca_column_spec.ColumnSpec(name="name_value"),
        )


def test_create_model(transport: str = "grpc", request_type=service.CreateModelRequest):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_model_from_dict():
    test_create_model(request_type=dict)


def test_create_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        client.create_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateModelRequest()


@pytest.mark.asyncio
async def test_create_model_async(
    transport: str = "grpc_asyncio", request_type=service.CreateModelRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.CreateModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_model_async_from_dict():
    await test_create_model_async(request_type=dict)


def test_create_model_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateModelRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_model_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.CreateModelRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_model_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_model(
            parent="parent_value",
            model=gca_model.Model(
                translation_model_metadata=translation.TranslationModelMetadata(
                    base_model="base_model_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].model == gca_model.Model(
            translation_model_metadata=translation.TranslationModelMetadata(
                base_model="base_model_value"
            )
        )


def test_create_model_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_model(
            service.CreateModelRequest(),
            parent="parent_value",
            model=gca_model.Model(
                translation_model_metadata=translation.TranslationModelMetadata(
                    base_model="base_model_value"
                )
            ),
        )


@pytest.mark.asyncio
async def test_create_model_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_model(
            parent="parent_value",
            model=gca_model.Model(
                translation_model_metadata=translation.TranslationModelMetadata(
                    base_model="base_model_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].model == gca_model.Model(
            translation_model_metadata=translation.TranslationModelMetadata(
                base_model="base_model_value"
            )
        )


@pytest.mark.asyncio
async def test_create_model_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_model(
            service.CreateModelRequest(),
            parent="parent_value",
            model=gca_model.Model(
                translation_model_metadata=translation.TranslationModelMetadata(
                    base_model="base_model_value"
                )
            ),
        )


def test_get_model(transport: str = "grpc", request_type=service.GetModelRequest):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model(
            name="name_value",
            display_name="display_name_value",
            dataset_id="dataset_id_value",
            deployment_state=model.Model.DeploymentState.DEPLOYED,
            translation_model_metadata=translation.TranslationModelMetadata(
                base_model="base_model_value"
            ),
        )
        response = client.get_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.Model)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.dataset_id == "dataset_id_value"
    assert response.deployment_state == model.Model.DeploymentState.DEPLOYED


def test_get_model_from_dict():
    test_get_model(request_type=dict)


def test_get_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_model), "__call__") as call:
        client.get_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetModelRequest()


@pytest.mark.asyncio
async def test_get_model_async(
    transport: str = "grpc_asyncio", request_type=service.GetModelRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model.Model(
                name="name_value",
                display_name="display_name_value",
                dataset_id="dataset_id_value",
                deployment_state=model.Model.DeploymentState.DEPLOYED,
            )
        )
        response = await client.get_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model.Model)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.dataset_id == "dataset_id_value"
    assert response.deployment_state == model.Model.DeploymentState.DEPLOYED


@pytest.mark.asyncio
async def test_get_model_async_from_dict():
    await test_get_model_async(request_type=dict)


def test_get_model_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_model), "__call__") as call:
        call.return_value = model.Model()
        client.get_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_model_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(model.Model())
        await client.get_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_model_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_model(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_model_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_model(
            service.GetModelRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_model_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = model.Model()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(model.Model())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_model(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_model_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_model(
            service.GetModelRequest(), name="name_value",
        )


def test_list_models(transport: str = "grpc", request_type=service.ListModelsRequest):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListModelsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListModelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListModelsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_models_from_dict():
    test_list_models(request_type=dict)


def test_list_models_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        client.list_models()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListModelsRequest()


@pytest.mark.asyncio
async def test_list_models_async(
    transport: str = "grpc_asyncio", request_type=service.ListModelsRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListModelsResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListModelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListModelsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_models_async_from_dict():
    await test_list_models_async(request_type=dict)


def test_list_models_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListModelsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        call.return_value = service.ListModelsResponse()
        client.list_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_models_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListModelsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListModelsResponse()
        )
        await client.list_models(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_models_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListModelsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_models(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_models_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_models(
            service.ListModelsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_models_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListModelsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListModelsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_models(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_models_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_models(
            service.ListModelsRequest(), parent="parent_value",
        )


def test_list_models_pager():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListModelsResponse(
                model=[model.Model(), model.Model(), model.Model(),],
                next_page_token="abc",
            ),
            service.ListModelsResponse(model=[], next_page_token="def",),
            service.ListModelsResponse(model=[model.Model(),], next_page_token="ghi",),
            service.ListModelsResponse(model=[model.Model(), model.Model(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_models(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, model.Model) for i in results)


def test_list_models_pages():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_models), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListModelsResponse(
                model=[model.Model(), model.Model(), model.Model(),],
                next_page_token="abc",
            ),
            service.ListModelsResponse(model=[], next_page_token="def",),
            service.ListModelsResponse(model=[model.Model(),], next_page_token="ghi",),
            service.ListModelsResponse(model=[model.Model(), model.Model(),],),
            RuntimeError,
        )
        pages = list(client.list_models(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_models_async_pager():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_models), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListModelsResponse(
                model=[model.Model(), model.Model(), model.Model(),],
                next_page_token="abc",
            ),
            service.ListModelsResponse(model=[], next_page_token="def",),
            service.ListModelsResponse(model=[model.Model(),], next_page_token="ghi",),
            service.ListModelsResponse(model=[model.Model(), model.Model(),],),
            RuntimeError,
        )
        async_pager = await client.list_models(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, model.Model) for i in responses)


@pytest.mark.asyncio
async def test_list_models_async_pages():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_models), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListModelsResponse(
                model=[model.Model(), model.Model(), model.Model(),],
                next_page_token="abc",
            ),
            service.ListModelsResponse(model=[], next_page_token="def",),
            service.ListModelsResponse(model=[model.Model(),], next_page_token="ghi",),
            service.ListModelsResponse(model=[model.Model(), model.Model(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_models(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_model(transport: str = "grpc", request_type=service.DeleteModelRequest):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_model_from_dict():
    test_delete_model(request_type=dict)


def test_delete_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        client.delete_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteModelRequest()


@pytest.mark.asyncio
async def test_delete_model_async(
    transport: str = "grpc_asyncio", request_type=service.DeleteModelRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeleteModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_model_async_from_dict():
    await test_delete_model_async(request_type=dict)


def test_delete_model_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_model_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeleteModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_model_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_model(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_model_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_model(
            service.DeleteModelRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_model_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_model(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_model_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_model(
            service.DeleteModelRequest(), name="name_value",
        )


def test_deploy_model(transport: str = "grpc", request_type=service.DeployModelRequest):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.deploy_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeployModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_deploy_model_from_dict():
    test_deploy_model(request_type=dict)


def test_deploy_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_model), "__call__") as call:
        client.deploy_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeployModelRequest()


@pytest.mark.asyncio
async def test_deploy_model_async(
    transport: str = "grpc_asyncio", request_type=service.DeployModelRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.deploy_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.DeployModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_deploy_model_async_from_dict():
    await test_deploy_model_async(request_type=dict)


def test_deploy_model_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeployModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_model), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.deploy_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_deploy_model_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.DeployModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.deploy_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_deploy_model_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.deploy_model(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_deploy_model_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.deploy_model(
            service.DeployModelRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_deploy_model_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.deploy_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.deploy_model(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_deploy_model_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.deploy_model(
            service.DeployModelRequest(), name="name_value",
        )


def test_undeploy_model(
    transport: str = "grpc", request_type=service.UndeployModelRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.undeploy_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UndeployModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_undeploy_model_from_dict():
    test_undeploy_model(request_type=dict)


def test_undeploy_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_model), "__call__") as call:
        client.undeploy_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UndeployModelRequest()


@pytest.mark.asyncio
async def test_undeploy_model_async(
    transport: str = "grpc_asyncio", request_type=service.UndeployModelRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.undeploy_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.UndeployModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_undeploy_model_async_from_dict():
    await test_undeploy_model_async(request_type=dict)


def test_undeploy_model_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UndeployModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_model), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.undeploy_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_undeploy_model_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.UndeployModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.undeploy_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_undeploy_model_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.undeploy_model(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_undeploy_model_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.undeploy_model(
            service.UndeployModelRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_undeploy_model_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.undeploy_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.undeploy_model(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_undeploy_model_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.undeploy_model(
            service.UndeployModelRequest(), name="name_value",
        )


def test_export_model(transport: str = "grpc", request_type=service.ExportModelRequest):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.export_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ExportModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_model_from_dict():
    test_export_model(request_type=dict)


def test_export_model_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_model), "__call__") as call:
        client.export_model()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ExportModelRequest()


@pytest.mark.asyncio
async def test_export_model_async(
    transport: str = "grpc_asyncio", request_type=service.ExportModelRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.export_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ExportModelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_model_async_from_dict():
    await test_export_model_async(request_type=dict)


def test_export_model_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ExportModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_model), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.export_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_model_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ExportModelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_model), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.export_model(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_export_model_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_model(
            name="name_value",
            output_config=io.ModelExportOutputConfig(
                gcs_destination=io.GcsDestination(
                    output_uri_prefix="output_uri_prefix_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].output_config == io.ModelExportOutputConfig(
            gcs_destination=io.GcsDestination(
                output_uri_prefix="output_uri_prefix_value"
            )
        )


def test_export_model_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_model(
            service.ExportModelRequest(),
            name="name_value",
            output_config=io.ModelExportOutputConfig(
                gcs_destination=io.GcsDestination(
                    output_uri_prefix="output_uri_prefix_value"
                )
            ),
        )


@pytest.mark.asyncio
async def test_export_model_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.export_model), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.export_model(
            name="name_value",
            output_config=io.ModelExportOutputConfig(
                gcs_destination=io.GcsDestination(
                    output_uri_prefix="output_uri_prefix_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].output_config == io.ModelExportOutputConfig(
            gcs_destination=io.GcsDestination(
                output_uri_prefix="output_uri_prefix_value"
            )
        )


@pytest.mark.asyncio
async def test_export_model_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_model(
            service.ExportModelRequest(),
            name="name_value",
            output_config=io.ModelExportOutputConfig(
                gcs_destination=io.GcsDestination(
                    output_uri_prefix="output_uri_prefix_value"
                )
            ),
        )


def test_export_evaluated_examples(
    transport: str = "grpc", request_type=service.ExportEvaluatedExamplesRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_evaluated_examples), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.export_evaluated_examples(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ExportEvaluatedExamplesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_export_evaluated_examples_from_dict():
    test_export_evaluated_examples(request_type=dict)


def test_export_evaluated_examples_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_evaluated_examples), "__call__"
    ) as call:
        client.export_evaluated_examples()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ExportEvaluatedExamplesRequest()


@pytest.mark.asyncio
async def test_export_evaluated_examples_async(
    transport: str = "grpc_asyncio", request_type=service.ExportEvaluatedExamplesRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_evaluated_examples), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.export_evaluated_examples(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ExportEvaluatedExamplesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_export_evaluated_examples_async_from_dict():
    await test_export_evaluated_examples_async(request_type=dict)


def test_export_evaluated_examples_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ExportEvaluatedExamplesRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_evaluated_examples), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.export_evaluated_examples(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_export_evaluated_examples_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ExportEvaluatedExamplesRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_evaluated_examples), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.export_evaluated_examples(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_export_evaluated_examples_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_evaluated_examples), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.export_evaluated_examples(
            name="name_value",
            output_config=io.ExportEvaluatedExamplesOutputConfig(
                bigquery_destination=io.BigQueryDestination(
                    output_uri="output_uri_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].output_config == io.ExportEvaluatedExamplesOutputConfig(
            bigquery_destination=io.BigQueryDestination(output_uri="output_uri_value")
        )


def test_export_evaluated_examples_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.export_evaluated_examples(
            service.ExportEvaluatedExamplesRequest(),
            name="name_value",
            output_config=io.ExportEvaluatedExamplesOutputConfig(
                bigquery_destination=io.BigQueryDestination(
                    output_uri="output_uri_value"
                )
            ),
        )


@pytest.mark.asyncio
async def test_export_evaluated_examples_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.export_evaluated_examples), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.export_evaluated_examples(
            name="name_value",
            output_config=io.ExportEvaluatedExamplesOutputConfig(
                bigquery_destination=io.BigQueryDestination(
                    output_uri="output_uri_value"
                )
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].output_config == io.ExportEvaluatedExamplesOutputConfig(
            bigquery_destination=io.BigQueryDestination(output_uri="output_uri_value")
        )


@pytest.mark.asyncio
async def test_export_evaluated_examples_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.export_evaluated_examples(
            service.ExportEvaluatedExamplesRequest(),
            name="name_value",
            output_config=io.ExportEvaluatedExamplesOutputConfig(
                bigquery_destination=io.BigQueryDestination(
                    output_uri="output_uri_value"
                )
            ),
        )


def test_get_model_evaluation(
    transport: str = "grpc", request_type=service.GetModelEvaluationRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_model_evaluation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = model_evaluation.ModelEvaluation(
            name="name_value",
            annotation_spec_id="annotation_spec_id_value",
            display_name="display_name_value",
            evaluated_example_count=2446,
            classification_evaluation_metrics=classification.ClassificationEvaluationMetrics(
                au_prc=0.634
            ),
        )
        response = client.get_model_evaluation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetModelEvaluationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model_evaluation.ModelEvaluation)
    assert response.name == "name_value"
    assert response.annotation_spec_id == "annotation_spec_id_value"
    assert response.display_name == "display_name_value"
    assert response.evaluated_example_count == 2446


def test_get_model_evaluation_from_dict():
    test_get_model_evaluation(request_type=dict)


def test_get_model_evaluation_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_model_evaluation), "__call__"
    ) as call:
        client.get_model_evaluation()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetModelEvaluationRequest()


@pytest.mark.asyncio
async def test_get_model_evaluation_async(
    transport: str = "grpc_asyncio", request_type=service.GetModelEvaluationRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_model_evaluation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model_evaluation.ModelEvaluation(
                name="name_value",
                annotation_spec_id="annotation_spec_id_value",
                display_name="display_name_value",
                evaluated_example_count=2446,
            )
        )
        response = await client.get_model_evaluation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.GetModelEvaluationRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, model_evaluation.ModelEvaluation)
    assert response.name == "name_value"
    assert response.annotation_spec_id == "annotation_spec_id_value"
    assert response.display_name == "display_name_value"
    assert response.evaluated_example_count == 2446


@pytest.mark.asyncio
async def test_get_model_evaluation_async_from_dict():
    await test_get_model_evaluation_async(request_type=dict)


def test_get_model_evaluation_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetModelEvaluationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_model_evaluation), "__call__"
    ) as call:
        call.return_value = model_evaluation.ModelEvaluation()
        client.get_model_evaluation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_model_evaluation_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetModelEvaluationRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_model_evaluation), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model_evaluation.ModelEvaluation()
        )
        await client.get_model_evaluation(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_model_evaluation_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_model_evaluation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = model_evaluation.ModelEvaluation()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_model_evaluation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_model_evaluation_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_model_evaluation(
            service.GetModelEvaluationRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_model_evaluation_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_model_evaluation), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = model_evaluation.ModelEvaluation()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            model_evaluation.ModelEvaluation()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_model_evaluation(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_model_evaluation_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_model_evaluation(
            service.GetModelEvaluationRequest(), name="name_value",
        )


def test_list_model_evaluations(
    transport: str = "grpc", request_type=service.ListModelEvaluationsRequest
):
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListModelEvaluationsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_model_evaluations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListModelEvaluationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListModelEvaluationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_model_evaluations_from_dict():
    test_list_model_evaluations(request_type=dict)


def test_list_model_evaluations_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations), "__call__"
    ) as call:
        client.list_model_evaluations()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListModelEvaluationsRequest()


@pytest.mark.asyncio
async def test_list_model_evaluations_async(
    transport: str = "grpc_asyncio", request_type=service.ListModelEvaluationsRequest
):
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListModelEvaluationsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_model_evaluations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == service.ListModelEvaluationsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListModelEvaluationsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_model_evaluations_async_from_dict():
    await test_list_model_evaluations_async(request_type=dict)


def test_list_model_evaluations_field_headers():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListModelEvaluationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations), "__call__"
    ) as call:
        call.return_value = service.ListModelEvaluationsResponse()
        client.list_model_evaluations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_model_evaluations_field_headers_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListModelEvaluationsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListModelEvaluationsResponse()
        )
        await client.list_model_evaluations(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_model_evaluations_flattened():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListModelEvaluationsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_model_evaluations(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_model_evaluations_flattened_error():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_model_evaluations(
            service.ListModelEvaluationsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_model_evaluations_flattened_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListModelEvaluationsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            service.ListModelEvaluationsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_model_evaluations(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_model_evaluations_flattened_error_async():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_model_evaluations(
            service.ListModelEvaluationsRequest(), parent="parent_value",
        )


def test_list_model_evaluations_pager():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListModelEvaluationsResponse(
                model_evaluation=[
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                ],
                next_page_token="abc",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[], next_page_token="def",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[model_evaluation.ModelEvaluation(),],
                next_page_token="ghi",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_model_evaluations(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, model_evaluation.ModelEvaluation) for i in results)


def test_list_model_evaluations_pages():
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListModelEvaluationsResponse(
                model_evaluation=[
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                ],
                next_page_token="abc",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[], next_page_token="def",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[model_evaluation.ModelEvaluation(),],
                next_page_token="ghi",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_model_evaluations(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_model_evaluations_async_pager():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListModelEvaluationsResponse(
                model_evaluation=[
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                ],
                next_page_token="abc",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[], next_page_token="def",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[model_evaluation.ModelEvaluation(),],
                next_page_token="ghi",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_model_evaluations(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, model_evaluation.ModelEvaluation) for i in responses)


@pytest.mark.asyncio
async def test_list_model_evaluations_async_pages():
    client = AutoMlAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_model_evaluations),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListModelEvaluationsResponse(
                model_evaluation=[
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                ],
                next_page_token="abc",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[], next_page_token="def",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[model_evaluation.ModelEvaluation(),],
                next_page_token="ghi",
            ),
            service.ListModelEvaluationsResponse(
                model_evaluation=[
                    model_evaluation.ModelEvaluation(),
                    model_evaluation.ModelEvaluation(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_model_evaluations(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.AutoMlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AutoMlClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.AutoMlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AutoMlClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.AutoMlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = AutoMlClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AutoMlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AutoMlClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.AutoMlGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.AutoMlGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.AutoMlGrpcTransport, transports.AutoMlGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = AutoMlClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.AutoMlGrpcTransport,)


def test_auto_ml_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.AutoMlTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_auto_ml_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.automl_v1beta1.services.auto_ml.transports.AutoMlTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.AutoMlTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_dataset",
        "get_dataset",
        "list_datasets",
        "update_dataset",
        "delete_dataset",
        "import_data",
        "export_data",
        "get_annotation_spec",
        "get_table_spec",
        "list_table_specs",
        "update_table_spec",
        "get_column_spec",
        "list_column_specs",
        "update_column_spec",
        "create_model",
        "get_model",
        "list_models",
        "delete_model",
        "deploy_model",
        "undeploy_model",
        "export_model",
        "export_evaluated_examples",
        "get_model_evaluation",
        "list_model_evaluations",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


@requires_google_auth_gte_1_25_0
def test_auto_ml_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.automl_v1beta1.services.auto_ml.transports.AutoMlTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AutoMlTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_auto_ml_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.automl_v1beta1.services.auto_ml.transports.AutoMlTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AutoMlTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_auto_ml_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.automl_v1beta1.services.auto_ml.transports.AutoMlTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.AutoMlTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_auto_ml_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AutoMlClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_auto_ml_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AutoMlClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.AutoMlGrpcTransport, transports.AutoMlGrpcAsyncIOTransport,],
)
@requires_google_auth_gte_1_25_0
def test_auto_ml_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.AutoMlGrpcTransport, transports.AutoMlGrpcAsyncIOTransport,],
)
@requires_google_auth_lt_1_25_0
def test_auto_ml_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.AutoMlGrpcTransport, grpc_helpers),
        (transports.AutoMlGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_auto_ml_transport_create_channel(transport_class, grpc_helpers):
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
            "automl.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="automl.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.AutoMlGrpcTransport, transports.AutoMlGrpcAsyncIOTransport],
)
def test_auto_ml_grpc_transport_client_cert_source_for_mtls(transport_class):
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
            scopes=None,
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


def test_auto_ml_host_no_port():
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="automl.googleapis.com"
        ),
    )
    assert client.transport._host == "automl.googleapis.com:443"


def test_auto_ml_host_with_port():
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="automl.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "automl.googleapis.com:8000"


def test_auto_ml_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AutoMlGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_auto_ml_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.AutoMlGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.AutoMlGrpcTransport, transports.AutoMlGrpcAsyncIOTransport],
)
def test_auto_ml_transport_channel_mtls_with_client_cert_source(transport_class):
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
                scopes=None,
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
    [transports.AutoMlGrpcTransport, transports.AutoMlGrpcAsyncIOTransport],
)
def test_auto_ml_transport_channel_mtls_with_adc(transport_class):
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
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_auto_ml_grpc_lro_client():
    client = AutoMlClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_auto_ml_grpc_lro_async_client():
    client = AutoMlAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_annotation_spec_path():
    project = "squid"
    location = "clam"
    dataset = "whelk"
    annotation_spec = "octopus"
    expected = "projects/{project}/locations/{location}/datasets/{dataset}/annotationSpecs/{annotation_spec}".format(
        project=project,
        location=location,
        dataset=dataset,
        annotation_spec=annotation_spec,
    )
    actual = AutoMlClient.annotation_spec_path(
        project, location, dataset, annotation_spec
    )
    assert expected == actual


def test_parse_annotation_spec_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "dataset": "cuttlefish",
        "annotation_spec": "mussel",
    }
    path = AutoMlClient.annotation_spec_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_annotation_spec_path(path)
    assert expected == actual


def test_column_spec_path():
    project = "winkle"
    location = "nautilus"
    dataset = "scallop"
    table_spec = "abalone"
    column_spec = "squid"
    expected = "projects/{project}/locations/{location}/datasets/{dataset}/tableSpecs/{table_spec}/columnSpecs/{column_spec}".format(
        project=project,
        location=location,
        dataset=dataset,
        table_spec=table_spec,
        column_spec=column_spec,
    )
    actual = AutoMlClient.column_spec_path(
        project, location, dataset, table_spec, column_spec
    )
    assert expected == actual


def test_parse_column_spec_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "dataset": "octopus",
        "table_spec": "oyster",
        "column_spec": "nudibranch",
    }
    path = AutoMlClient.column_spec_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_column_spec_path(path)
    assert expected == actual


def test_dataset_path():
    project = "cuttlefish"
    location = "mussel"
    dataset = "winkle"
    expected = "projects/{project}/locations/{location}/datasets/{dataset}".format(
        project=project, location=location, dataset=dataset,
    )
    actual = AutoMlClient.dataset_path(project, location, dataset)
    assert expected == actual


def test_parse_dataset_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "dataset": "abalone",
    }
    path = AutoMlClient.dataset_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_dataset_path(path)
    assert expected == actual


def test_model_path():
    project = "squid"
    location = "clam"
    model = "whelk"
    expected = "projects/{project}/locations/{location}/models/{model}".format(
        project=project, location=location, model=model,
    )
    actual = AutoMlClient.model_path(project, location, model)
    assert expected == actual


def test_parse_model_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "model": "nudibranch",
    }
    path = AutoMlClient.model_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_model_path(path)
    assert expected == actual


def test_model_evaluation_path():
    project = "cuttlefish"
    location = "mussel"
    model = "winkle"
    model_evaluation = "nautilus"
    expected = "projects/{project}/locations/{location}/models/{model}/modelEvaluations/{model_evaluation}".format(
        project=project,
        location=location,
        model=model,
        model_evaluation=model_evaluation,
    )
    actual = AutoMlClient.model_evaluation_path(
        project, location, model, model_evaluation
    )
    assert expected == actual


def test_parse_model_evaluation_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
        "model": "squid",
        "model_evaluation": "clam",
    }
    path = AutoMlClient.model_evaluation_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_model_evaluation_path(path)
    assert expected == actual


def test_table_spec_path():
    project = "whelk"
    location = "octopus"
    dataset = "oyster"
    table_spec = "nudibranch"
    expected = "projects/{project}/locations/{location}/datasets/{dataset}/tableSpecs/{table_spec}".format(
        project=project, location=location, dataset=dataset, table_spec=table_spec,
    )
    actual = AutoMlClient.table_spec_path(project, location, dataset, table_spec)
    assert expected == actual


def test_parse_table_spec_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
        "dataset": "winkle",
        "table_spec": "nautilus",
    }
    path = AutoMlClient.table_spec_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_table_spec_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AutoMlClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = AutoMlClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(folder=folder,)
    actual = AutoMlClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = AutoMlClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = AutoMlClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = AutoMlClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(project=project,)
    actual = AutoMlClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = AutoMlClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = AutoMlClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = AutoMlClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AutoMlClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.AutoMlTransport, "_prep_wrapped_messages"
    ) as prep:
        client = AutoMlClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.AutoMlTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AutoMlClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
