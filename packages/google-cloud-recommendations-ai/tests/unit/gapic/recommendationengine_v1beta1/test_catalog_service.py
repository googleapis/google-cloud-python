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
from google.cloud.recommendationengine_v1beta1.services.catalog_service import (
    CatalogServiceAsyncClient,
)
from google.cloud.recommendationengine_v1beta1.services.catalog_service import (
    CatalogServiceClient,
)
from google.cloud.recommendationengine_v1beta1.services.catalog_service import pagers
from google.cloud.recommendationengine_v1beta1.services.catalog_service import (
    transports,
)
from google.cloud.recommendationengine_v1beta1.services.catalog_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.recommendationengine_v1beta1.types import catalog
from google.cloud.recommendationengine_v1beta1.types import catalog_service
from google.cloud.recommendationengine_v1beta1.types import common
from google.cloud.recommendationengine_v1beta1.types import import_
from google.cloud.recommendationengine_v1beta1.types import user_event
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

    assert CatalogServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CatalogServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [CatalogServiceClient, CatalogServiceAsyncClient,]
)
def test_catalog_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "recommendationengine.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [CatalogServiceClient, CatalogServiceAsyncClient,]
)
def test_catalog_service_client_service_account_always_use_jwt(client_class):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        client = client_class(credentials=creds)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.CatalogServiceGrpcTransport, "grpc"),
        (transports.CatalogServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_catalog_service_client_service_account_always_use_jwt_true(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)


@pytest.mark.parametrize(
    "client_class", [CatalogServiceClient, CatalogServiceAsyncClient,]
)
def test_catalog_service_client_from_service_account_file(client_class):
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

        assert client.transport._host == "recommendationengine.googleapis.com:443"


def test_catalog_service_client_get_transport_class():
    transport = CatalogServiceClient.get_transport_class()
    available_transports = [
        transports.CatalogServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = CatalogServiceClient.get_transport_class("grpc")
    assert transport == transports.CatalogServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc"),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    CatalogServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CatalogServiceClient),
)
@mock.patch.object(
    CatalogServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CatalogServiceAsyncClient),
)
def test_catalog_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CatalogServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CatalogServiceClient, "get_transport_class") as gtc:
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
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc", "true"),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc", "false"),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    CatalogServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CatalogServiceClient),
)
@mock.patch.object(
    CatalogServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CatalogServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_catalog_service_client_mtls_env_auto(
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
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc"),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_catalog_service_client_client_options_scopes(
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
        (CatalogServiceClient, transports.CatalogServiceGrpcTransport, "grpc"),
        (
            CatalogServiceAsyncClient,
            transports.CatalogServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_catalog_service_client_client_options_credentials_file(
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


def test_catalog_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.catalog_service.transports.CatalogServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CatalogServiceClient(
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


def test_create_catalog_item(
    transport: str = "grpc", request_type=catalog_service.CreateCatalogItemRequest
):
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem(
            id="id_value",
            title="title_value",
            description="description_value",
            language_code="language_code_value",
            tags=["tags_value"],
            item_group_id="item_group_id_value",
            product_metadata=catalog.ProductCatalogItem(
                exact_price=catalog.ProductCatalogItem.ExactPrice(display_price=0.1384)
            ),
        )
        response = client.create_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.CreateCatalogItemRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CatalogItem)
    assert response.id == "id_value"
    assert response.title == "title_value"
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.item_group_id == "item_group_id_value"


def test_create_catalog_item_from_dict():
    test_create_catalog_item(request_type=dict)


def test_create_catalog_item_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_catalog_item), "__call__"
    ) as call:
        client.create_catalog_item()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.CreateCatalogItemRequest()


@pytest.mark.asyncio
async def test_create_catalog_item_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.CreateCatalogItemRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.CatalogItem(
                id="id_value",
                title="title_value",
                description="description_value",
                language_code="language_code_value",
                tags=["tags_value"],
                item_group_id="item_group_id_value",
            )
        )
        response = await client.create_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.CreateCatalogItemRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CatalogItem)
    assert response.id == "id_value"
    assert response.title == "title_value"
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.item_group_id == "item_group_id_value"


@pytest.mark.asyncio
async def test_create_catalog_item_async_from_dict():
    await test_create_catalog_item_async(request_type=dict)


def test_create_catalog_item_field_headers():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.CreateCatalogItemRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_catalog_item), "__call__"
    ) as call:
        call.return_value = catalog.CatalogItem()
        client.create_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_catalog_item_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.CreateCatalogItemRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_catalog_item), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(catalog.CatalogItem())
        await client.create_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_catalog_item_flattened():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_catalog_item(
            parent="parent_value", catalog_item=catalog.CatalogItem(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].catalog_item == catalog.CatalogItem(id="id_value")


def test_create_catalog_item_flattened_error():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_catalog_item(
            catalog_service.CreateCatalogItemRequest(),
            parent="parent_value",
            catalog_item=catalog.CatalogItem(id="id_value"),
        )


@pytest.mark.asyncio
async def test_create_catalog_item_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(catalog.CatalogItem())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_catalog_item(
            parent="parent_value", catalog_item=catalog.CatalogItem(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].catalog_item == catalog.CatalogItem(id="id_value")


@pytest.mark.asyncio
async def test_create_catalog_item_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_catalog_item(
            catalog_service.CreateCatalogItemRequest(),
            parent="parent_value",
            catalog_item=catalog.CatalogItem(id="id_value"),
        )


def test_get_catalog_item(
    transport: str = "grpc", request_type=catalog_service.GetCatalogItemRequest
):
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog_item), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem(
            id="id_value",
            title="title_value",
            description="description_value",
            language_code="language_code_value",
            tags=["tags_value"],
            item_group_id="item_group_id_value",
            product_metadata=catalog.ProductCatalogItem(
                exact_price=catalog.ProductCatalogItem.ExactPrice(display_price=0.1384)
            ),
        )
        response = client.get_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetCatalogItemRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CatalogItem)
    assert response.id == "id_value"
    assert response.title == "title_value"
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.item_group_id == "item_group_id_value"


def test_get_catalog_item_from_dict():
    test_get_catalog_item(request_type=dict)


def test_get_catalog_item_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog_item), "__call__") as call:
        client.get_catalog_item()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetCatalogItemRequest()


@pytest.mark.asyncio
async def test_get_catalog_item_async(
    transport: str = "grpc_asyncio", request_type=catalog_service.GetCatalogItemRequest
):
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog_item), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.CatalogItem(
                id="id_value",
                title="title_value",
                description="description_value",
                language_code="language_code_value",
                tags=["tags_value"],
                item_group_id="item_group_id_value",
            )
        )
        response = await client.get_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.GetCatalogItemRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CatalogItem)
    assert response.id == "id_value"
    assert response.title == "title_value"
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.item_group_id == "item_group_id_value"


@pytest.mark.asyncio
async def test_get_catalog_item_async_from_dict():
    await test_get_catalog_item_async(request_type=dict)


def test_get_catalog_item_field_headers():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.GetCatalogItemRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog_item), "__call__") as call:
        call.return_value = catalog.CatalogItem()
        client.get_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_catalog_item_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.GetCatalogItemRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog_item), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(catalog.CatalogItem())
        await client.get_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_catalog_item_flattened():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog_item), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_catalog_item(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_catalog_item_flattened_error():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_catalog_item(
            catalog_service.GetCatalogItemRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_catalog_item_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_catalog_item), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(catalog.CatalogItem())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_catalog_item(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_catalog_item_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_catalog_item(
            catalog_service.GetCatalogItemRequest(), name="name_value",
        )


def test_list_catalog_items(
    transport: str = "grpc", request_type=catalog_service.ListCatalogItemsRequest
):
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.ListCatalogItemsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.ListCatalogItemsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCatalogItemsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_catalog_items_from_dict():
    test_list_catalog_items(request_type=dict)


def test_list_catalog_items_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items), "__call__"
    ) as call:
        client.list_catalog_items()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.ListCatalogItemsRequest()


@pytest.mark.asyncio
async def test_list_catalog_items_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.ListCatalogItemsRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog_service.ListCatalogItemsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.ListCatalogItemsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCatalogItemsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_catalog_items_async_from_dict():
    await test_list_catalog_items_async(request_type=dict)


def test_list_catalog_items_field_headers():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.ListCatalogItemsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items), "__call__"
    ) as call:
        call.return_value = catalog_service.ListCatalogItemsResponse()
        client.list_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_catalog_items_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.ListCatalogItemsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog_service.ListCatalogItemsResponse()
        )
        await client.list_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_catalog_items_flattened():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.ListCatalogItemsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_catalog_items(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].filter == "filter_value"


def test_list_catalog_items_flattened_error():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_catalog_items(
            catalog_service.ListCatalogItemsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_catalog_items_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.ListCatalogItemsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog_service.ListCatalogItemsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_catalog_items(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_catalog_items_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_catalog_items(
            catalog_service.ListCatalogItemsRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_catalog_items_pager():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[
                    catalog.CatalogItem(),
                    catalog.CatalogItem(),
                    catalog.CatalogItem(),
                ],
                next_page_token="abc",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[], next_page_token="def",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(),], next_page_token="ghi",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(), catalog.CatalogItem(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_catalog_items(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, catalog.CatalogItem) for i in results)


def test_list_catalog_items_pages():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[
                    catalog.CatalogItem(),
                    catalog.CatalogItem(),
                    catalog.CatalogItem(),
                ],
                next_page_token="abc",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[], next_page_token="def",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(),], next_page_token="ghi",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(), catalog.CatalogItem(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_catalog_items(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_catalog_items_async_pager():
    client = CatalogServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[
                    catalog.CatalogItem(),
                    catalog.CatalogItem(),
                    catalog.CatalogItem(),
                ],
                next_page_token="abc",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[], next_page_token="def",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(),], next_page_token="ghi",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(), catalog.CatalogItem(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_catalog_items(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, catalog.CatalogItem) for i in responses)


@pytest.mark.asyncio
async def test_list_catalog_items_async_pages():
    client = CatalogServiceAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_catalog_items),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[
                    catalog.CatalogItem(),
                    catalog.CatalogItem(),
                    catalog.CatalogItem(),
                ],
                next_page_token="abc",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[], next_page_token="def",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(),], next_page_token="ghi",
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(), catalog.CatalogItem(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_catalog_items(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_update_catalog_item(
    transport: str = "grpc", request_type=catalog_service.UpdateCatalogItemRequest
):
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem(
            id="id_value",
            title="title_value",
            description="description_value",
            language_code="language_code_value",
            tags=["tags_value"],
            item_group_id="item_group_id_value",
            product_metadata=catalog.ProductCatalogItem(
                exact_price=catalog.ProductCatalogItem.ExactPrice(display_price=0.1384)
            ),
        )
        response = client.update_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateCatalogItemRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CatalogItem)
    assert response.id == "id_value"
    assert response.title == "title_value"
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.item_group_id == "item_group_id_value"


def test_update_catalog_item_from_dict():
    test_update_catalog_item(request_type=dict)


def test_update_catalog_item_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_catalog_item), "__call__"
    ) as call:
        client.update_catalog_item()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateCatalogItemRequest()


@pytest.mark.asyncio
async def test_update_catalog_item_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.UpdateCatalogItemRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            catalog.CatalogItem(
                id="id_value",
                title="title_value",
                description="description_value",
                language_code="language_code_value",
                tags=["tags_value"],
                item_group_id="item_group_id_value",
            )
        )
        response = await client.update_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.UpdateCatalogItemRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CatalogItem)
    assert response.id == "id_value"
    assert response.title == "title_value"
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.item_group_id == "item_group_id_value"


@pytest.mark.asyncio
async def test_update_catalog_item_async_from_dict():
    await test_update_catalog_item_async(request_type=dict)


def test_update_catalog_item_field_headers():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.UpdateCatalogItemRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_catalog_item), "__call__"
    ) as call:
        call.return_value = catalog.CatalogItem()
        client.update_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_catalog_item_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.UpdateCatalogItemRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_catalog_item), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(catalog.CatalogItem())
        await client.update_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_catalog_item_flattened():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_catalog_item(
            name="name_value",
            catalog_item=catalog.CatalogItem(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].catalog_item == catalog.CatalogItem(id="id_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_catalog_item_flattened_error():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_catalog_item(
            catalog_service.UpdateCatalogItemRequest(),
            name="name_value",
            catalog_item=catalog.CatalogItem(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_catalog_item_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(catalog.CatalogItem())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_catalog_item(
            name="name_value",
            catalog_item=catalog.CatalogItem(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].catalog_item == catalog.CatalogItem(id="id_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_catalog_item_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_catalog_item(
            catalog_service.UpdateCatalogItemRequest(),
            name="name_value",
            catalog_item=catalog.CatalogItem(id="id_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_delete_catalog_item(
    transport: str = "grpc", request_type=catalog_service.DeleteCatalogItemRequest
):
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.DeleteCatalogItemRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_catalog_item_from_dict():
    test_delete_catalog_item(request_type=dict)


def test_delete_catalog_item_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_catalog_item), "__call__"
    ) as call:
        client.delete_catalog_item()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.DeleteCatalogItemRequest()


@pytest.mark.asyncio
async def test_delete_catalog_item_async(
    transport: str = "grpc_asyncio",
    request_type=catalog_service.DeleteCatalogItemRequest,
):
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == catalog_service.DeleteCatalogItemRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_catalog_item_async_from_dict():
    await test_delete_catalog_item_async(request_type=dict)


def test_delete_catalog_item_field_headers():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.DeleteCatalogItemRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_catalog_item), "__call__"
    ) as call:
        call.return_value = None
        client.delete_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_catalog_item_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.DeleteCatalogItemRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_catalog_item), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_catalog_item_flattened():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_catalog_item(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_catalog_item_flattened_error():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_catalog_item(
            catalog_service.DeleteCatalogItemRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_catalog_item_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_catalog_item(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_catalog_item_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_catalog_item(
            catalog_service.DeleteCatalogItemRequest(), name="name_value",
        )


def test_import_catalog_items(
    transport: str = "grpc", request_type=import_.ImportCatalogItemsRequest
):
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == import_.ImportCatalogItemsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_catalog_items_from_dict():
    test_import_catalog_items(request_type=dict)


def test_import_catalog_items_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_catalog_items), "__call__"
    ) as call:
        client.import_catalog_items()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == import_.ImportCatalogItemsRequest()


@pytest.mark.asyncio
async def test_import_catalog_items_async(
    transport: str = "grpc_asyncio", request_type=import_.ImportCatalogItemsRequest
):
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == import_.ImportCatalogItemsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_catalog_items_async_from_dict():
    await test_import_catalog_items_async(request_type=dict)


def test_import_catalog_items_field_headers():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = import_.ImportCatalogItemsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_catalog_items), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_catalog_items_field_headers_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = import_.ImportCatalogItemsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_catalog_items), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_import_catalog_items_flattened():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.import_catalog_items(
            parent="parent_value",
            request_id="request_id_value",
            input_config=import_.InputConfig(
                catalog_inline_source=import_.CatalogInlineSource(
                    catalog_items=[catalog.CatalogItem(id="id_value")]
                )
            ),
            errors_config=import_.ImportErrorsConfig(gcs_prefix="gcs_prefix_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].request_id == "request_id_value"
        assert args[0].input_config == import_.InputConfig(
            catalog_inline_source=import_.CatalogInlineSource(
                catalog_items=[catalog.CatalogItem(id="id_value")]
            )
        )
        assert args[0].errors_config == import_.ImportErrorsConfig(
            gcs_prefix="gcs_prefix_value"
        )


def test_import_catalog_items_flattened_error():
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.import_catalog_items(
            import_.ImportCatalogItemsRequest(),
            parent="parent_value",
            request_id="request_id_value",
            input_config=import_.InputConfig(
                catalog_inline_source=import_.CatalogInlineSource(
                    catalog_items=[catalog.CatalogItem(id="id_value")]
                )
            ),
            errors_config=import_.ImportErrorsConfig(gcs_prefix="gcs_prefix_value"),
        )


@pytest.mark.asyncio
async def test_import_catalog_items_flattened_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.import_catalog_items(
            parent="parent_value",
            request_id="request_id_value",
            input_config=import_.InputConfig(
                catalog_inline_source=import_.CatalogInlineSource(
                    catalog_items=[catalog.CatalogItem(id="id_value")]
                )
            ),
            errors_config=import_.ImportErrorsConfig(gcs_prefix="gcs_prefix_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].request_id == "request_id_value"
        assert args[0].input_config == import_.InputConfig(
            catalog_inline_source=import_.CatalogInlineSource(
                catalog_items=[catalog.CatalogItem(id="id_value")]
            )
        )
        assert args[0].errors_config == import_.ImportErrorsConfig(
            gcs_prefix="gcs_prefix_value"
        )


@pytest.mark.asyncio
async def test_import_catalog_items_flattened_error_async():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.import_catalog_items(
            import_.ImportCatalogItemsRequest(),
            parent="parent_value",
            request_id="request_id_value",
            input_config=import_.InputConfig(
                catalog_inline_source=import_.CatalogInlineSource(
                    catalog_items=[catalog.CatalogItem(id="id_value")]
                )
            ),
            errors_config=import_.ImportErrorsConfig(gcs_prefix="gcs_prefix_value"),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CatalogServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CatalogServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CatalogServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = CatalogServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CatalogServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
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
    client = CatalogServiceClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.CatalogServiceGrpcTransport,)


def test_catalog_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.CatalogServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_catalog_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.catalog_service.transports.CatalogServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CatalogServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_catalog_item",
        "get_catalog_item",
        "list_catalog_items",
        "update_catalog_item",
        "delete_catalog_item",
        "import_catalog_items",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


@requires_google_auth_gte_1_25_0
def test_catalog_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.catalog_service.transports.CatalogServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CatalogServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_catalog_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.catalog_service.transports.CatalogServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CatalogServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_catalog_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.catalog_service.transports.CatalogServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.CatalogServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_catalog_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CatalogServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_catalog_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        CatalogServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_catalog_service_transport_auth_adc(transport_class):
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
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_catalog_service_transport_auth_adc_old_google_auth(transport_class):
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
        (transports.CatalogServiceGrpcTransport, grpc_helpers),
        (transports.CatalogServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_catalog_service_transport_create_channel(transport_class, grpc_helpers):
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
            "recommendationengine.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="recommendationengine.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
    ],
)
def test_catalog_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_catalog_service_host_no_port():
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommendationengine.googleapis.com"
        ),
    )
    assert client.transport._host == "recommendationengine.googleapis.com:443"


def test_catalog_service_host_with_port():
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommendationengine.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "recommendationengine.googleapis.com:8000"


def test_catalog_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CatalogServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_catalog_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.CatalogServiceGrpcAsyncIOTransport(
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
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
    ],
)
def test_catalog_service_transport_channel_mtls_with_client_cert_source(
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
    [
        transports.CatalogServiceGrpcTransport,
        transports.CatalogServiceGrpcAsyncIOTransport,
    ],
)
def test_catalog_service_transport_channel_mtls_with_adc(transport_class):
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


def test_catalog_service_grpc_lro_client():
    client = CatalogServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_catalog_service_grpc_lro_async_client():
    client = CatalogServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_catalog_path():
    project = "squid"
    location = "clam"
    catalog = "whelk"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}".format(
        project=project, location=location, catalog=catalog,
    )
    actual = CatalogServiceClient.catalog_path(project, location, catalog)
    assert expected == actual


def test_parse_catalog_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "catalog": "nudibranch",
    }
    path = CatalogServiceClient.catalog_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_catalog_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CatalogServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = CatalogServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = CatalogServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = CatalogServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = CatalogServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = CatalogServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = CatalogServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = CatalogServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = CatalogServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = CatalogServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CatalogServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CatalogServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CatalogServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CatalogServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CatalogServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
