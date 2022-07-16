# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock
except ImportError:
    import mock

import math

from google.api_core import (
    future,
    gapic_v1,
    grpc_helpers,
    grpc_helpers_async,
    operation,
    operations_v1,
    path_template,
)
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest

from google.cloud.retail_v2.services.product_service import (
    ProductServiceAsyncClient,
    ProductServiceClient,
    pagers,
    transports,
)
from google.cloud.retail_v2.types import common, import_config
from google.cloud.retail_v2.types import product
from google.cloud.retail_v2.types import product as gcr_product
from google.cloud.retail_v2.types import product_service, promotion


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

    assert ProductServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ProductServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ProductServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ProductServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ProductServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ProductServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ProductServiceClient, "grpc"),
        (ProductServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_product_service_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("retail.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.ProductServiceGrpcTransport, "grpc"),
        (transports.ProductServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_product_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (ProductServiceClient, "grpc"),
        (ProductServiceAsyncClient, "grpc_asyncio"),
    ],
)
def test_product_service_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json(
            "dummy/file/path.json", transport=transport_name
        )
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == ("retail.googleapis.com:443")


def test_product_service_client_get_transport_class():
    transport = ProductServiceClient.get_transport_class()
    available_transports = [
        transports.ProductServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = ProductServiceClient.get_transport_class("grpc")
    assert transport == transports.ProductServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ProductServiceClient, transports.ProductServiceGrpcTransport, "grpc"),
        (
            ProductServiceAsyncClient,
            transports.ProductServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ProductServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ProductServiceClient),
)
@mock.patch.object(
    ProductServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ProductServiceAsyncClient),
)
def test_product_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ProductServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ProductServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(
        api_audience="https://language.googleapis.com"
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com",
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (ProductServiceClient, transports.ProductServiceGrpcTransport, "grpc", "true"),
        (
            ProductServiceAsyncClient,
            transports.ProductServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (ProductServiceClient, transports.ProductServiceGrpcTransport, "grpc", "false"),
        (
            ProductServiceAsyncClient,
            transports.ProductServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    ProductServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ProductServiceClient),
)
@mock.patch.object(
    ProductServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ProductServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_product_service_client_mtls_env_auto(
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
            client = client_class(client_options=options, transport=transport_name)

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
                always_use_jwt_access=True,
                api_audience=None,
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
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
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
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [ProductServiceClient, ProductServiceAsyncClient]
)
@mock.patch.object(
    ProductServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ProductServiceClient),
)
@mock.patch.object(
    ProductServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ProductServiceAsyncClient),
)
def test_product_service_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ProductServiceClient, transports.ProductServiceGrpcTransport, "grpc"),
        (
            ProductServiceAsyncClient,
            transports.ProductServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_product_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            ProductServiceClient,
            transports.ProductServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ProductServiceAsyncClient,
            transports.ProductServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_product_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_product_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.retail_v2.services.product_service.transports.ProductServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ProductServiceClient(
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
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (
            ProductServiceClient,
            transports.ProductServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            ProductServiceAsyncClient,
            transports.ProductServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_product_service_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "retail.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="retail.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.CreateProductRequest,
        dict,
    ],
)
def test_create_product(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_product.Product(
            name="name_value",
            id="id_value",
            type_=gcr_product.Product.Type.PRIMARY,
            primary_product_id="primary_product_id_value",
            collection_member_ids=["collection_member_ids_value"],
            gtin="gtin_value",
            categories=["categories_value"],
            title="title_value",
            brands=["brands_value"],
            description="description_value",
            language_code="language_code_value",
            tags=["tags_value"],
            availability=gcr_product.Product.Availability.IN_STOCK,
            uri="uri_value",
            sizes=["sizes_value"],
            materials=["materials_value"],
            patterns=["patterns_value"],
            conditions=["conditions_value"],
            expire_time=timestamp_pb2.Timestamp(seconds=751),
        )
        response = client.create_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.CreateProductRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcr_product.Product)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.type_ == gcr_product.Product.Type.PRIMARY
    assert response.primary_product_id == "primary_product_id_value"
    assert response.collection_member_ids == ["collection_member_ids_value"]
    assert response.gtin == "gtin_value"
    assert response.categories == ["categories_value"]
    assert response.title == "title_value"
    assert response.brands == ["brands_value"]
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.availability == gcr_product.Product.Availability.IN_STOCK
    assert response.uri == "uri_value"
    assert response.sizes == ["sizes_value"]
    assert response.materials == ["materials_value"]
    assert response.patterns == ["patterns_value"]
    assert response.conditions == ["conditions_value"]


def test_create_product_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_product), "__call__") as call:
        client.create_product()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.CreateProductRequest()


@pytest.mark.asyncio
async def test_create_product_async(
    transport: str = "grpc_asyncio", request_type=product_service.CreateProductRequest
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcr_product.Product(
                name="name_value",
                id="id_value",
                type_=gcr_product.Product.Type.PRIMARY,
                primary_product_id="primary_product_id_value",
                collection_member_ids=["collection_member_ids_value"],
                gtin="gtin_value",
                categories=["categories_value"],
                title="title_value",
                brands=["brands_value"],
                description="description_value",
                language_code="language_code_value",
                tags=["tags_value"],
                availability=gcr_product.Product.Availability.IN_STOCK,
                uri="uri_value",
                sizes=["sizes_value"],
                materials=["materials_value"],
                patterns=["patterns_value"],
                conditions=["conditions_value"],
            )
        )
        response = await client.create_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.CreateProductRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcr_product.Product)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.type_ == gcr_product.Product.Type.PRIMARY
    assert response.primary_product_id == "primary_product_id_value"
    assert response.collection_member_ids == ["collection_member_ids_value"]
    assert response.gtin == "gtin_value"
    assert response.categories == ["categories_value"]
    assert response.title == "title_value"
    assert response.brands == ["brands_value"]
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.availability == gcr_product.Product.Availability.IN_STOCK
    assert response.uri == "uri_value"
    assert response.sizes == ["sizes_value"]
    assert response.materials == ["materials_value"]
    assert response.patterns == ["patterns_value"]
    assert response.conditions == ["conditions_value"]


@pytest.mark.asyncio
async def test_create_product_async_from_dict():
    await test_create_product_async(request_type=dict)


def test_create_product_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.CreateProductRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_product), "__call__") as call:
        call.return_value = gcr_product.Product()
        client.create_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_product_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.CreateProductRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_product), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcr_product.Product())
        await client.create_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_create_product_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_product.Product()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_product(
            parent="parent_value",
            product=gcr_product.Product(
                expire_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            product_id="product_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].product
        mock_val = gcr_product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751))
        assert arg == mock_val
        arg = args[0].product_id
        mock_val = "product_id_value"
        assert arg == mock_val


def test_create_product_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_product(
            product_service.CreateProductRequest(),
            parent="parent_value",
            product=gcr_product.Product(
                expire_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            product_id="product_id_value",
        )


@pytest.mark.asyncio
async def test_create_product_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_product.Product()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcr_product.Product())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_product(
            parent="parent_value",
            product=gcr_product.Product(
                expire_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            product_id="product_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].product
        mock_val = gcr_product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751))
        assert arg == mock_val
        arg = args[0].product_id
        mock_val = "product_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_product_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_product(
            product_service.CreateProductRequest(),
            parent="parent_value",
            product=gcr_product.Product(
                expire_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            product_id="product_id_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.GetProductRequest,
        dict,
    ],
)
def test_get_product(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product.Product(
            name="name_value",
            id="id_value",
            type_=product.Product.Type.PRIMARY,
            primary_product_id="primary_product_id_value",
            collection_member_ids=["collection_member_ids_value"],
            gtin="gtin_value",
            categories=["categories_value"],
            title="title_value",
            brands=["brands_value"],
            description="description_value",
            language_code="language_code_value",
            tags=["tags_value"],
            availability=product.Product.Availability.IN_STOCK,
            uri="uri_value",
            sizes=["sizes_value"],
            materials=["materials_value"],
            patterns=["patterns_value"],
            conditions=["conditions_value"],
            expire_time=timestamp_pb2.Timestamp(seconds=751),
        )
        response = client.get_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.GetProductRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, product.Product)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.type_ == product.Product.Type.PRIMARY
    assert response.primary_product_id == "primary_product_id_value"
    assert response.collection_member_ids == ["collection_member_ids_value"]
    assert response.gtin == "gtin_value"
    assert response.categories == ["categories_value"]
    assert response.title == "title_value"
    assert response.brands == ["brands_value"]
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.availability == product.Product.Availability.IN_STOCK
    assert response.uri == "uri_value"
    assert response.sizes == ["sizes_value"]
    assert response.materials == ["materials_value"]
    assert response.patterns == ["patterns_value"]
    assert response.conditions == ["conditions_value"]


def test_get_product_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_product), "__call__") as call:
        client.get_product()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.GetProductRequest()


@pytest.mark.asyncio
async def test_get_product_async(
    transport: str = "grpc_asyncio", request_type=product_service.GetProductRequest
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            product.Product(
                name="name_value",
                id="id_value",
                type_=product.Product.Type.PRIMARY,
                primary_product_id="primary_product_id_value",
                collection_member_ids=["collection_member_ids_value"],
                gtin="gtin_value",
                categories=["categories_value"],
                title="title_value",
                brands=["brands_value"],
                description="description_value",
                language_code="language_code_value",
                tags=["tags_value"],
                availability=product.Product.Availability.IN_STOCK,
                uri="uri_value",
                sizes=["sizes_value"],
                materials=["materials_value"],
                patterns=["patterns_value"],
                conditions=["conditions_value"],
            )
        )
        response = await client.get_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.GetProductRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, product.Product)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.type_ == product.Product.Type.PRIMARY
    assert response.primary_product_id == "primary_product_id_value"
    assert response.collection_member_ids == ["collection_member_ids_value"]
    assert response.gtin == "gtin_value"
    assert response.categories == ["categories_value"]
    assert response.title == "title_value"
    assert response.brands == ["brands_value"]
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.availability == product.Product.Availability.IN_STOCK
    assert response.uri == "uri_value"
    assert response.sizes == ["sizes_value"]
    assert response.materials == ["materials_value"]
    assert response.patterns == ["patterns_value"]
    assert response.conditions == ["conditions_value"]


@pytest.mark.asyncio
async def test_get_product_async_from_dict():
    await test_get_product_async(request_type=dict)


def test_get_product_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.GetProductRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_product), "__call__") as call:
        call.return_value = product.Product()
        client.get_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_product_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.GetProductRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_product), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(product.Product())
        await client.get_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_get_product_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product.Product()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_product(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_product_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_product(
            product_service.GetProductRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_product_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product.Product()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(product.Product())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_product(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_product_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_product(
            product_service.GetProductRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.ListProductsRequest,
        dict,
    ],
)
def test_list_products(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_service.ListProductsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.ListProductsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProductsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_products_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        client.list_products()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.ListProductsRequest()


@pytest.mark.asyncio
async def test_list_products_async(
    transport: str = "grpc_asyncio", request_type=product_service.ListProductsRequest
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            product_service.ListProductsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.ListProductsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProductsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_products_async_from_dict():
    await test_list_products_async(request_type=dict)


def test_list_products_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.ListProductsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        call.return_value = product_service.ListProductsResponse()
        client.list_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_products_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.ListProductsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            product_service.ListProductsResponse()
        )
        await client.list_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


def test_list_products_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_service.ListProductsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_products(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_products_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_products(
            product_service.ListProductsRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_products_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_service.ListProductsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            product_service.ListProductsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_products(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_products_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_products(
            product_service.ListProductsRequest(),
            parent="parent_value",
        )


def test_list_products_pager(transport_name: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                    product.Product(),
                    product.Product(),
                ],
                next_page_token="abc",
            ),
            product_service.ListProductsResponse(
                products=[],
                next_page_token="def",
            ),
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                ],
                next_page_token="ghi",
            ),
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                    product.Product(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_products(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, product.Product) for i in results)


def test_list_products_pages(transport_name: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_products), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                    product.Product(),
                    product.Product(),
                ],
                next_page_token="abc",
            ),
            product_service.ListProductsResponse(
                products=[],
                next_page_token="def",
            ),
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                ],
                next_page_token="ghi",
            ),
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                    product.Product(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_products(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_products_async_pager():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_products), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                    product.Product(),
                    product.Product(),
                ],
                next_page_token="abc",
            ),
            product_service.ListProductsResponse(
                products=[],
                next_page_token="def",
            ),
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                ],
                next_page_token="ghi",
            ),
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                    product.Product(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_products(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, product.Product) for i in responses)


@pytest.mark.asyncio
async def test_list_products_async_pages():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_products), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                    product.Product(),
                    product.Product(),
                ],
                next_page_token="abc",
            ),
            product_service.ListProductsResponse(
                products=[],
                next_page_token="def",
            ),
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                ],
                next_page_token="ghi",
            ),
            product_service.ListProductsResponse(
                products=[
                    product.Product(),
                    product.Product(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_products(request={})
        ).pages:  # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.UpdateProductRequest,
        dict,
    ],
)
def test_update_product(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_product.Product(
            name="name_value",
            id="id_value",
            type_=gcr_product.Product.Type.PRIMARY,
            primary_product_id="primary_product_id_value",
            collection_member_ids=["collection_member_ids_value"],
            gtin="gtin_value",
            categories=["categories_value"],
            title="title_value",
            brands=["brands_value"],
            description="description_value",
            language_code="language_code_value",
            tags=["tags_value"],
            availability=gcr_product.Product.Availability.IN_STOCK,
            uri="uri_value",
            sizes=["sizes_value"],
            materials=["materials_value"],
            patterns=["patterns_value"],
            conditions=["conditions_value"],
            expire_time=timestamp_pb2.Timestamp(seconds=751),
        )
        response = client.update_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.UpdateProductRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcr_product.Product)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.type_ == gcr_product.Product.Type.PRIMARY
    assert response.primary_product_id == "primary_product_id_value"
    assert response.collection_member_ids == ["collection_member_ids_value"]
    assert response.gtin == "gtin_value"
    assert response.categories == ["categories_value"]
    assert response.title == "title_value"
    assert response.brands == ["brands_value"]
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.availability == gcr_product.Product.Availability.IN_STOCK
    assert response.uri == "uri_value"
    assert response.sizes == ["sizes_value"]
    assert response.materials == ["materials_value"]
    assert response.patterns == ["patterns_value"]
    assert response.conditions == ["conditions_value"]


def test_update_product_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_product), "__call__") as call:
        client.update_product()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.UpdateProductRequest()


@pytest.mark.asyncio
async def test_update_product_async(
    transport: str = "grpc_asyncio", request_type=product_service.UpdateProductRequest
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcr_product.Product(
                name="name_value",
                id="id_value",
                type_=gcr_product.Product.Type.PRIMARY,
                primary_product_id="primary_product_id_value",
                collection_member_ids=["collection_member_ids_value"],
                gtin="gtin_value",
                categories=["categories_value"],
                title="title_value",
                brands=["brands_value"],
                description="description_value",
                language_code="language_code_value",
                tags=["tags_value"],
                availability=gcr_product.Product.Availability.IN_STOCK,
                uri="uri_value",
                sizes=["sizes_value"],
                materials=["materials_value"],
                patterns=["patterns_value"],
                conditions=["conditions_value"],
            )
        )
        response = await client.update_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.UpdateProductRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcr_product.Product)
    assert response.name == "name_value"
    assert response.id == "id_value"
    assert response.type_ == gcr_product.Product.Type.PRIMARY
    assert response.primary_product_id == "primary_product_id_value"
    assert response.collection_member_ids == ["collection_member_ids_value"]
    assert response.gtin == "gtin_value"
    assert response.categories == ["categories_value"]
    assert response.title == "title_value"
    assert response.brands == ["brands_value"]
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.availability == gcr_product.Product.Availability.IN_STOCK
    assert response.uri == "uri_value"
    assert response.sizes == ["sizes_value"]
    assert response.materials == ["materials_value"]
    assert response.patterns == ["patterns_value"]
    assert response.conditions == ["conditions_value"]


@pytest.mark.asyncio
async def test_update_product_async_from_dict():
    await test_update_product_async(request_type=dict)


def test_update_product_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.UpdateProductRequest()

    request.product.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_product), "__call__") as call:
        call.return_value = gcr_product.Product()
        client.update_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_product_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.UpdateProductRequest()

    request.product.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_product), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcr_product.Product())
        await client.update_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product.name=name_value",
    ) in kw["metadata"]


def test_update_product_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_product.Product()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_product(
            product=gcr_product.Product(
                expire_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = gcr_product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751))
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_product_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_product(
            product_service.UpdateProductRequest(),
            product=gcr_product.Product(
                expire_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_product_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcr_product.Product()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcr_product.Product())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_product(
            product=gcr_product.Product(
                expire_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = gcr_product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751))
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_product_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_product(
            product_service.UpdateProductRequest(),
            product=gcr_product.Product(
                expire_time=timestamp_pb2.Timestamp(seconds=751)
            ),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.DeleteProductRequest,
        dict,
    ],
)
def test_delete_product(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.DeleteProductRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_product_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_product), "__call__") as call:
        client.delete_product()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.DeleteProductRequest()


@pytest.mark.asyncio
async def test_delete_product_async(
    transport: str = "grpc_asyncio", request_type=product_service.DeleteProductRequest
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.DeleteProductRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_product_async_from_dict():
    await test_delete_product_async(request_type=dict)


def test_delete_product_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.DeleteProductRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_product), "__call__") as call:
        call.return_value = None
        client.delete_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_product_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.DeleteProductRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_product), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=name_value",
    ) in kw["metadata"]


def test_delete_product_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_product(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_product_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_product(
            product_service.DeleteProductRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_product_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_product(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_product_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_product(
            product_service.DeleteProductRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        import_config.ImportProductsRequest,
        dict,
    ],
)
def test_import_products(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == import_config.ImportProductsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_import_products_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_products), "__call__") as call:
        client.import_products()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == import_config.ImportProductsRequest()


@pytest.mark.asyncio
async def test_import_products_async(
    transport: str = "grpc_asyncio", request_type=import_config.ImportProductsRequest
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.import_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == import_config.ImportProductsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_import_products_async_from_dict():
    await test_import_products_async(request_type=dict)


def test_import_products_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = import_config.ImportProductsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_products), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.import_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_products_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = import_config.ImportProductsRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.import_products), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.import_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "parent=parent_value",
    ) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.SetInventoryRequest,
        dict,
    ],
)
def test_set_inventory(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.set_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.SetInventoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_set_inventory_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_inventory), "__call__") as call:
        client.set_inventory()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.SetInventoryRequest()


@pytest.mark.asyncio
async def test_set_inventory_async(
    transport: str = "grpc_asyncio", request_type=product_service.SetInventoryRequest
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.set_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.SetInventoryRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_set_inventory_async_from_dict():
    await test_set_inventory_async(request_type=dict)


def test_set_inventory_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.SetInventoryRequest()

    request.inventory.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_inventory), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.set_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "inventory.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_inventory_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.SetInventoryRequest()

    request.inventory.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_inventory), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.set_inventory(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "inventory.name=name_value",
    ) in kw["metadata"]


def test_set_inventory_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.set_inventory(
            inventory=product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751)),
            set_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].inventory
        mock_val = product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751))
        assert arg == mock_val
        arg = args[0].set_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_set_inventory_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_inventory(
            product_service.SetInventoryRequest(),
            inventory=product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751)),
            set_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_set_inventory_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_inventory), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.set_inventory(
            inventory=product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751)),
            set_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].inventory
        mock_val = product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751))
        assert arg == mock_val
        arg = args[0].set_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


@pytest.mark.asyncio
async def test_set_inventory_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.set_inventory(
            product_service.SetInventoryRequest(),
            inventory=product.Product(expire_time=timestamp_pb2.Timestamp(seconds=751)),
            set_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.AddFulfillmentPlacesRequest,
        dict,
    ],
)
def test_add_fulfillment_places(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_fulfillment_places), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.add_fulfillment_places(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.AddFulfillmentPlacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_add_fulfillment_places_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_fulfillment_places), "__call__"
    ) as call:
        client.add_fulfillment_places()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.AddFulfillmentPlacesRequest()


@pytest.mark.asyncio
async def test_add_fulfillment_places_async(
    transport: str = "grpc_asyncio",
    request_type=product_service.AddFulfillmentPlacesRequest,
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_fulfillment_places), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.add_fulfillment_places(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.AddFulfillmentPlacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_add_fulfillment_places_async_from_dict():
    await test_add_fulfillment_places_async(request_type=dict)


def test_add_fulfillment_places_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.AddFulfillmentPlacesRequest()

    request.product = "product_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_fulfillment_places), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.add_fulfillment_places(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product=product_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_add_fulfillment_places_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.AddFulfillmentPlacesRequest()

    request.product = "product_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_fulfillment_places), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.add_fulfillment_places(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product=product_value",
    ) in kw["metadata"]


def test_add_fulfillment_places_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_fulfillment_places), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.add_fulfillment_places(
            product="product_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = "product_value"
        assert arg == mock_val


def test_add_fulfillment_places_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_fulfillment_places(
            product_service.AddFulfillmentPlacesRequest(),
            product="product_value",
        )


@pytest.mark.asyncio
async def test_add_fulfillment_places_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_fulfillment_places), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.add_fulfillment_places(
            product="product_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = "product_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_add_fulfillment_places_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.add_fulfillment_places(
            product_service.AddFulfillmentPlacesRequest(),
            product="product_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.RemoveFulfillmentPlacesRequest,
        dict,
    ],
)
def test_remove_fulfillment_places(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_fulfillment_places), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.remove_fulfillment_places(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.RemoveFulfillmentPlacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_remove_fulfillment_places_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_fulfillment_places), "__call__"
    ) as call:
        client.remove_fulfillment_places()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.RemoveFulfillmentPlacesRequest()


@pytest.mark.asyncio
async def test_remove_fulfillment_places_async(
    transport: str = "grpc_asyncio",
    request_type=product_service.RemoveFulfillmentPlacesRequest,
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_fulfillment_places), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.remove_fulfillment_places(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.RemoveFulfillmentPlacesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_remove_fulfillment_places_async_from_dict():
    await test_remove_fulfillment_places_async(request_type=dict)


def test_remove_fulfillment_places_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.RemoveFulfillmentPlacesRequest()

    request.product = "product_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_fulfillment_places), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.remove_fulfillment_places(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product=product_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_remove_fulfillment_places_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.RemoveFulfillmentPlacesRequest()

    request.product = "product_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_fulfillment_places), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.remove_fulfillment_places(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product=product_value",
    ) in kw["metadata"]


def test_remove_fulfillment_places_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_fulfillment_places), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.remove_fulfillment_places(
            product="product_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = "product_value"
        assert arg == mock_val


def test_remove_fulfillment_places_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_fulfillment_places(
            product_service.RemoveFulfillmentPlacesRequest(),
            product="product_value",
        )


@pytest.mark.asyncio
async def test_remove_fulfillment_places_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_fulfillment_places), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.remove_fulfillment_places(
            product="product_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = "product_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_remove_fulfillment_places_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.remove_fulfillment_places(
            product_service.RemoveFulfillmentPlacesRequest(),
            product="product_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.AddLocalInventoriesRequest,
        dict,
    ],
)
def test_add_local_inventories(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_local_inventories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.add_local_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.AddLocalInventoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_add_local_inventories_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_local_inventories), "__call__"
    ) as call:
        client.add_local_inventories()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.AddLocalInventoriesRequest()


@pytest.mark.asyncio
async def test_add_local_inventories_async(
    transport: str = "grpc_asyncio",
    request_type=product_service.AddLocalInventoriesRequest,
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_local_inventories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.add_local_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.AddLocalInventoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_add_local_inventories_async_from_dict():
    await test_add_local_inventories_async(request_type=dict)


def test_add_local_inventories_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.AddLocalInventoriesRequest()

    request.product = "product_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_local_inventories), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.add_local_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product=product_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_add_local_inventories_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.AddLocalInventoriesRequest()

    request.product = "product_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_local_inventories), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.add_local_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product=product_value",
    ) in kw["metadata"]


def test_add_local_inventories_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_local_inventories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.add_local_inventories(
            product="product_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = "product_value"
        assert arg == mock_val


def test_add_local_inventories_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_local_inventories(
            product_service.AddLocalInventoriesRequest(),
            product="product_value",
        )


@pytest.mark.asyncio
async def test_add_local_inventories_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.add_local_inventories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.add_local_inventories(
            product="product_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = "product_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_add_local_inventories_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.add_local_inventories(
            product_service.AddLocalInventoriesRequest(),
            product="product_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        product_service.RemoveLocalInventoriesRequest,
        dict,
    ],
)
def test_remove_local_inventories(request_type, transport: str = "grpc"):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_local_inventories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.remove_local_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.RemoveLocalInventoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_remove_local_inventories_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_local_inventories), "__call__"
    ) as call:
        client.remove_local_inventories()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.RemoveLocalInventoriesRequest()


@pytest.mark.asyncio
async def test_remove_local_inventories_async(
    transport: str = "grpc_asyncio",
    request_type=product_service.RemoveLocalInventoriesRequest,
):
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_local_inventories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.remove_local_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == product_service.RemoveLocalInventoriesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_remove_local_inventories_async_from_dict():
    await test_remove_local_inventories_async(request_type=dict)


def test_remove_local_inventories_field_headers():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.RemoveLocalInventoriesRequest()

    request.product = "product_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_local_inventories), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.remove_local_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product=product_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_remove_local_inventories_field_headers_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_service.RemoveLocalInventoriesRequest()

    request.product = "product_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_local_inventories), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.remove_local_inventories(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "product=product_value",
    ) in kw["metadata"]


def test_remove_local_inventories_flattened():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_local_inventories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.remove_local_inventories(
            product="product_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = "product_value"
        assert arg == mock_val


def test_remove_local_inventories_flattened_error():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_local_inventories(
            product_service.RemoveLocalInventoriesRequest(),
            product="product_value",
        )


@pytest.mark.asyncio
async def test_remove_local_inventories_flattened_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.remove_local_inventories), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.remove_local_inventories(
            product="product_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].product
        mock_val = "product_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_remove_local_inventories_flattened_error_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.remove_local_inventories(
            product_service.RemoveLocalInventoriesRequest(),
            product="product_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ProductServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ProductServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ProductServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ProductServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.ProductServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ProductServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = ProductServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ProductServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ProductServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ProductServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = ProductServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ProductServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ProductServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ProductServiceGrpcTransport,
        transports.ProductServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
    ],
)
def test_transport_kind(transport_name):
    transport = ProductServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.ProductServiceGrpcTransport,
    )


def test_product_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.ProductServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_product_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.retail_v2.services.product_service.transports.ProductServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ProductServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_product",
        "get_product",
        "list_products",
        "update_product",
        "delete_product",
        "import_products",
        "set_inventory",
        "add_fulfillment_places",
        "remove_fulfillment_places",
        "add_local_inventories",
        "remove_local_inventories",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        "kind",
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_product_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.retail_v2.services.product_service.transports.ProductServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ProductServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_product_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.retail_v2.services.product_service.transports.ProductServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.ProductServiceTransport()
        adc.assert_called_once()


def test_product_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        ProductServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ProductServiceGrpcTransport,
        transports.ProductServiceGrpcAsyncIOTransport,
    ],
)
def test_product_service_transport_auth_adc(transport_class):
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
        transports.ProductServiceGrpcTransport,
        transports.ProductServiceGrpcAsyncIOTransport,
    ],
)
def test_product_service_transport_auth_gdch_credentials(transport_class):
    host = "https://language.com"
    api_audience_tests = [None, "https://language2.com"]
    api_audience_expect = [host, "https://language2.com"]
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, "default", autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(
                return_value=gdch_mock
            )
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(e)


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.ProductServiceGrpcTransport, grpc_helpers),
        (transports.ProductServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_product_service_transport_create_channel(transport_class, grpc_helpers):
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
            "retail.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="retail.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ProductServiceGrpcTransport,
        transports.ProductServiceGrpcAsyncIOTransport,
    ],
)
def test_product_service_grpc_transport_client_cert_source_for_mtls(transport_class):
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


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_product_service_host_no_port(transport_name):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="retail.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("retail.googleapis.com:443")


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
    ],
)
def test_product_service_host_with_port(transport_name):
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="retail.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == ("retail.googleapis.com:8000")


def test_product_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ProductServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_product_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.ProductServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.ProductServiceGrpcTransport,
        transports.ProductServiceGrpcAsyncIOTransport,
    ],
)
def test_product_service_transport_channel_mtls_with_client_cert_source(
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
        transports.ProductServiceGrpcTransport,
        transports.ProductServiceGrpcAsyncIOTransport,
    ],
)
def test_product_service_transport_channel_mtls_with_adc(transport_class):
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


def test_product_service_grpc_lro_client():
    client = ProductServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_product_service_grpc_lro_async_client():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_branch_path():
    project = "squid"
    location = "clam"
    catalog = "whelk"
    branch = "octopus"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}/branches/{branch}".format(
        project=project,
        location=location,
        catalog=catalog,
        branch=branch,
    )
    actual = ProductServiceClient.branch_path(project, location, catalog, branch)
    assert expected == actual


def test_parse_branch_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "catalog": "cuttlefish",
        "branch": "mussel",
    }
    path = ProductServiceClient.branch_path(**expected)

    # Check that the path construction is reversible.
    actual = ProductServiceClient.parse_branch_path(path)
    assert expected == actual


def test_product_path():
    project = "winkle"
    location = "nautilus"
    catalog = "scallop"
    branch = "abalone"
    product = "squid"
    expected = "projects/{project}/locations/{location}/catalogs/{catalog}/branches/{branch}/products/{product}".format(
        project=project,
        location=location,
        catalog=catalog,
        branch=branch,
        product=product,
    )
    actual = ProductServiceClient.product_path(
        project, location, catalog, branch, product
    )
    assert expected == actual


def test_parse_product_path():
    expected = {
        "project": "clam",
        "location": "whelk",
        "catalog": "octopus",
        "branch": "oyster",
        "product": "nudibranch",
    }
    path = ProductServiceClient.product_path(**expected)

    # Check that the path construction is reversible.
    actual = ProductServiceClient.parse_product_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = ProductServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = ProductServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = ProductServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = ProductServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = ProductServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = ProductServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = ProductServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = ProductServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = ProductServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = ProductServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = ProductServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = ProductServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = ProductServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = ProductServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = ProductServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ProductServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ProductServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ProductServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ProductServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = ProductServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = ProductServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = ProductServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (ProductServiceClient, transports.ProductServiceGrpcTransport),
        (ProductServiceAsyncClient, transports.ProductServiceGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
