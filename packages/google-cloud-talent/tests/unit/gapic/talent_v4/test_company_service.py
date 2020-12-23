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
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.talent_v4.services.company_service import CompanyServiceAsyncClient
from google.cloud.talent_v4.services.company_service import CompanyServiceClient
from google.cloud.talent_v4.services.company_service import pagers
from google.cloud.talent_v4.services.company_service import transports
from google.cloud.talent_v4.types import common
from google.cloud.talent_v4.types import company
from google.cloud.talent_v4.types import company as gct_company
from google.cloud.talent_v4.types import company_service
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.type import latlng_pb2 as latlng  # type: ignore
from google.type import postal_address_pb2 as postal_address  # type: ignore


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

    assert CompanyServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        CompanyServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CompanyServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CompanyServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CompanyServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CompanyServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [CompanyServiceClient, CompanyServiceAsyncClient]
)
def test_company_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "jobs.googleapis.com:443"


def test_company_service_client_get_transport_class():
    transport = CompanyServiceClient.get_transport_class()
    assert transport == transports.CompanyServiceGrpcTransport

    transport = CompanyServiceClient.get_transport_class("grpc")
    assert transport == transports.CompanyServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CompanyServiceClient, transports.CompanyServiceGrpcTransport, "grpc"),
        (
            CompanyServiceAsyncClient,
            transports.CompanyServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    CompanyServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CompanyServiceClient),
)
@mock.patch.object(
    CompanyServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CompanyServiceAsyncClient),
)
def test_company_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CompanyServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CompanyServiceClient, "get_transport_class") as gtc:
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
            ssl_channel_credentials=None,
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
                ssl_channel_credentials=None,
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
                ssl_channel_credentials=None,
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
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (CompanyServiceClient, transports.CompanyServiceGrpcTransport, "grpc", "true"),
        (
            CompanyServiceAsyncClient,
            transports.CompanyServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CompanyServiceClient, transports.CompanyServiceGrpcTransport, "grpc", "false"),
        (
            CompanyServiceAsyncClient,
            transports.CompanyServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    CompanyServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CompanyServiceClient),
)
@mock.patch.object(
    CompanyServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CompanyServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_company_service_client_mtls_env_auto(
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
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
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
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CompanyServiceClient, transports.CompanyServiceGrpcTransport, "grpc"),
        (
            CompanyServiceAsyncClient,
            transports.CompanyServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_company_service_client_client_options_scopes(
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
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CompanyServiceClient, transports.CompanyServiceGrpcTransport, "grpc"),
        (
            CompanyServiceAsyncClient,
            transports.CompanyServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_company_service_client_client_options_credentials_file(
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
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_company_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.talent_v4.services.company_service.transports.CompanyServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CompanyServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_create_company(
    transport: str = "grpc", request_type=company_service.CreateCompanyRequest
):
    client = CompanyServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_company.Company(
            name="name_value",
            display_name="display_name_value",
            external_id="external_id_value",
            size=common.CompanySize.MINI,
            headquarters_address="headquarters_address_value",
            hiring_agency=True,
            eeo_text="eeo_text_value",
            website_uri="website_uri_value",
            career_site_uri="career_site_uri_value",
            image_uri="image_uri_value",
            keyword_searchable_job_custom_attributes=[
                "keyword_searchable_job_custom_attributes_value"
            ],
            suspended=True,
        )

        response = client.create_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.CreateCompanyRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, gct_company.Company)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.external_id == "external_id_value"

    assert response.size == common.CompanySize.MINI

    assert response.headquarters_address == "headquarters_address_value"

    assert response.hiring_agency is True

    assert response.eeo_text == "eeo_text_value"

    assert response.website_uri == "website_uri_value"

    assert response.career_site_uri == "career_site_uri_value"

    assert response.image_uri == "image_uri_value"

    assert response.keyword_searchable_job_custom_attributes == [
        "keyword_searchable_job_custom_attributes_value"
    ]

    assert response.suspended is True


def test_create_company_from_dict():
    test_create_company(request_type=dict)


@pytest.mark.asyncio
async def test_create_company_async(
    transport: str = "grpc_asyncio", request_type=company_service.CreateCompanyRequest
):
    client = CompanyServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gct_company.Company(
                name="name_value",
                display_name="display_name_value",
                external_id="external_id_value",
                size=common.CompanySize.MINI,
                headquarters_address="headquarters_address_value",
                hiring_agency=True,
                eeo_text="eeo_text_value",
                website_uri="website_uri_value",
                career_site_uri="career_site_uri_value",
                image_uri="image_uri_value",
                keyword_searchable_job_custom_attributes=[
                    "keyword_searchable_job_custom_attributes_value"
                ],
                suspended=True,
            )
        )

        response = await client.create_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.CreateCompanyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gct_company.Company)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.external_id == "external_id_value"

    assert response.size == common.CompanySize.MINI

    assert response.headquarters_address == "headquarters_address_value"

    assert response.hiring_agency is True

    assert response.eeo_text == "eeo_text_value"

    assert response.website_uri == "website_uri_value"

    assert response.career_site_uri == "career_site_uri_value"

    assert response.image_uri == "image_uri_value"

    assert response.keyword_searchable_job_custom_attributes == [
        "keyword_searchable_job_custom_attributes_value"
    ]

    assert response.suspended is True


@pytest.mark.asyncio
async def test_create_company_async_from_dict():
    await test_create_company_async(request_type=dict)


def test_create_company_field_headers():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.CreateCompanyRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_company), "__call__") as call:
        call.return_value = gct_company.Company()

        client.create_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_company_field_headers_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.CreateCompanyRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_company), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gct_company.Company())

        await client.create_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_company_flattened():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_company.Company()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_company(
            parent="parent_value", company=gct_company.Company(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].company == gct_company.Company(name="name_value")


def test_create_company_flattened_error():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_company(
            company_service.CreateCompanyRequest(),
            parent="parent_value",
            company=gct_company.Company(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_company_flattened_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_company.Company()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gct_company.Company())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_company(
            parent="parent_value", company=gct_company.Company(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].company == gct_company.Company(name="name_value")


@pytest.mark.asyncio
async def test_create_company_flattened_error_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_company(
            company_service.CreateCompanyRequest(),
            parent="parent_value",
            company=gct_company.Company(name="name_value"),
        )


def test_get_company(
    transport: str = "grpc", request_type=company_service.GetCompanyRequest
):
    client = CompanyServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = company.Company(
            name="name_value",
            display_name="display_name_value",
            external_id="external_id_value",
            size=common.CompanySize.MINI,
            headquarters_address="headquarters_address_value",
            hiring_agency=True,
            eeo_text="eeo_text_value",
            website_uri="website_uri_value",
            career_site_uri="career_site_uri_value",
            image_uri="image_uri_value",
            keyword_searchable_job_custom_attributes=[
                "keyword_searchable_job_custom_attributes_value"
            ],
            suspended=True,
        )

        response = client.get_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.GetCompanyRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, company.Company)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.external_id == "external_id_value"

    assert response.size == common.CompanySize.MINI

    assert response.headquarters_address == "headquarters_address_value"

    assert response.hiring_agency is True

    assert response.eeo_text == "eeo_text_value"

    assert response.website_uri == "website_uri_value"

    assert response.career_site_uri == "career_site_uri_value"

    assert response.image_uri == "image_uri_value"

    assert response.keyword_searchable_job_custom_attributes == [
        "keyword_searchable_job_custom_attributes_value"
    ]

    assert response.suspended is True


def test_get_company_from_dict():
    test_get_company(request_type=dict)


@pytest.mark.asyncio
async def test_get_company_async(
    transport: str = "grpc_asyncio", request_type=company_service.GetCompanyRequest
):
    client = CompanyServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            company.Company(
                name="name_value",
                display_name="display_name_value",
                external_id="external_id_value",
                size=common.CompanySize.MINI,
                headquarters_address="headquarters_address_value",
                hiring_agency=True,
                eeo_text="eeo_text_value",
                website_uri="website_uri_value",
                career_site_uri="career_site_uri_value",
                image_uri="image_uri_value",
                keyword_searchable_job_custom_attributes=[
                    "keyword_searchable_job_custom_attributes_value"
                ],
                suspended=True,
            )
        )

        response = await client.get_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.GetCompanyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, company.Company)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.external_id == "external_id_value"

    assert response.size == common.CompanySize.MINI

    assert response.headquarters_address == "headquarters_address_value"

    assert response.hiring_agency is True

    assert response.eeo_text == "eeo_text_value"

    assert response.website_uri == "website_uri_value"

    assert response.career_site_uri == "career_site_uri_value"

    assert response.image_uri == "image_uri_value"

    assert response.keyword_searchable_job_custom_attributes == [
        "keyword_searchable_job_custom_attributes_value"
    ]

    assert response.suspended is True


@pytest.mark.asyncio
async def test_get_company_async_from_dict():
    await test_get_company_async(request_type=dict)


def test_get_company_field_headers():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.GetCompanyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_company), "__call__") as call:
        call.return_value = company.Company()

        client.get_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_company_field_headers_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.GetCompanyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_company), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(company.Company())

        await client.get_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_company_flattened():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = company.Company()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_company(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_company_flattened_error():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_company(
            company_service.GetCompanyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_company_flattened_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = company.Company()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(company.Company())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_company(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_company_flattened_error_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_company(
            company_service.GetCompanyRequest(), name="name_value",
        )


def test_update_company(
    transport: str = "grpc", request_type=company_service.UpdateCompanyRequest
):
    client = CompanyServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_company.Company(
            name="name_value",
            display_name="display_name_value",
            external_id="external_id_value",
            size=common.CompanySize.MINI,
            headquarters_address="headquarters_address_value",
            hiring_agency=True,
            eeo_text="eeo_text_value",
            website_uri="website_uri_value",
            career_site_uri="career_site_uri_value",
            image_uri="image_uri_value",
            keyword_searchable_job_custom_attributes=[
                "keyword_searchable_job_custom_attributes_value"
            ],
            suspended=True,
        )

        response = client.update_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.UpdateCompanyRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, gct_company.Company)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.external_id == "external_id_value"

    assert response.size == common.CompanySize.MINI

    assert response.headquarters_address == "headquarters_address_value"

    assert response.hiring_agency is True

    assert response.eeo_text == "eeo_text_value"

    assert response.website_uri == "website_uri_value"

    assert response.career_site_uri == "career_site_uri_value"

    assert response.image_uri == "image_uri_value"

    assert response.keyword_searchable_job_custom_attributes == [
        "keyword_searchable_job_custom_attributes_value"
    ]

    assert response.suspended is True


def test_update_company_from_dict():
    test_update_company(request_type=dict)


@pytest.mark.asyncio
async def test_update_company_async(
    transport: str = "grpc_asyncio", request_type=company_service.UpdateCompanyRequest
):
    client = CompanyServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gct_company.Company(
                name="name_value",
                display_name="display_name_value",
                external_id="external_id_value",
                size=common.CompanySize.MINI,
                headquarters_address="headquarters_address_value",
                hiring_agency=True,
                eeo_text="eeo_text_value",
                website_uri="website_uri_value",
                career_site_uri="career_site_uri_value",
                image_uri="image_uri_value",
                keyword_searchable_job_custom_attributes=[
                    "keyword_searchable_job_custom_attributes_value"
                ],
                suspended=True,
            )
        )

        response = await client.update_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.UpdateCompanyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gct_company.Company)

    assert response.name == "name_value"

    assert response.display_name == "display_name_value"

    assert response.external_id == "external_id_value"

    assert response.size == common.CompanySize.MINI

    assert response.headquarters_address == "headquarters_address_value"

    assert response.hiring_agency is True

    assert response.eeo_text == "eeo_text_value"

    assert response.website_uri == "website_uri_value"

    assert response.career_site_uri == "career_site_uri_value"

    assert response.image_uri == "image_uri_value"

    assert response.keyword_searchable_job_custom_attributes == [
        "keyword_searchable_job_custom_attributes_value"
    ]

    assert response.suspended is True


@pytest.mark.asyncio
async def test_update_company_async_from_dict():
    await test_update_company_async(request_type=dict)


def test_update_company_field_headers():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.UpdateCompanyRequest()
    request.company.name = "company.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_company), "__call__") as call:
        call.return_value = gct_company.Company()

        client.update_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "company.name=company.name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_update_company_field_headers_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.UpdateCompanyRequest()
    request.company.name = "company.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_company), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gct_company.Company())

        await client.update_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "company.name=company.name/value",) in kw[
        "metadata"
    ]


def test_update_company_flattened():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_company.Company()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_company(
            company=gct_company.Company(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].company == gct_company.Company(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_company_flattened_error():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_company(
            company_service.UpdateCompanyRequest(),
            company=gct_company.Company(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_company_flattened_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gct_company.Company()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gct_company.Company())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_company(
            company=gct_company.Company(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].company == gct_company.Company(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_company_flattened_error_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_company(
            company_service.UpdateCompanyRequest(),
            company=gct_company.Company(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_company(
    transport: str = "grpc", request_type=company_service.DeleteCompanyRequest
):
    client = CompanyServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.DeleteCompanyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_company_from_dict():
    test_delete_company(request_type=dict)


@pytest.mark.asyncio
async def test_delete_company_async(
    transport: str = "grpc_asyncio", request_type=company_service.DeleteCompanyRequest
):
    client = CompanyServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.DeleteCompanyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_company_async_from_dict():
    await test_delete_company_async(request_type=dict)


def test_delete_company_field_headers():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.DeleteCompanyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_company), "__call__") as call:
        call.return_value = None

        client.delete_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_company_field_headers_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.DeleteCompanyRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_company), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_company(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_company_flattened():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_company(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_company_flattened_error():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_company(
            company_service.DeleteCompanyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_company_flattened_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_company), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_company(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_company_flattened_error_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_company(
            company_service.DeleteCompanyRequest(), name="name_value",
        )


def test_list_companies(
    transport: str = "grpc", request_type=company_service.ListCompaniesRequest
):
    client = CompanyServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_companies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = company_service.ListCompaniesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_companies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.ListCompaniesRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListCompaniesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_companies_from_dict():
    test_list_companies(request_type=dict)


@pytest.mark.asyncio
async def test_list_companies_async(
    transport: str = "grpc_asyncio", request_type=company_service.ListCompaniesRequest
):
    client = CompanyServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_companies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            company_service.ListCompaniesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_companies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == company_service.ListCompaniesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCompaniesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_companies_async_from_dict():
    await test_list_companies_async(request_type=dict)


def test_list_companies_field_headers():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.ListCompaniesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_companies), "__call__") as call:
        call.return_value = company_service.ListCompaniesResponse()

        client.list_companies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_companies_field_headers_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = company_service.ListCompaniesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_companies), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            company_service.ListCompaniesResponse()
        )

        await client.list_companies(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_companies_flattened():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_companies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = company_service.ListCompaniesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_companies(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_companies_flattened_error():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_companies(
            company_service.ListCompaniesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_companies_flattened_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_companies), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = company_service.ListCompaniesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            company_service.ListCompaniesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_companies(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_companies_flattened_error_async():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_companies(
            company_service.ListCompaniesRequest(), parent="parent_value",
        )


def test_list_companies_pager():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_companies), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            company_service.ListCompaniesResponse(
                companies=[company.Company(), company.Company(), company.Company(),],
                next_page_token="abc",
            ),
            company_service.ListCompaniesResponse(companies=[], next_page_token="def",),
            company_service.ListCompaniesResponse(
                companies=[company.Company(),], next_page_token="ghi",
            ),
            company_service.ListCompaniesResponse(
                companies=[company.Company(), company.Company(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_companies(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, company.Company) for i in results)


def test_list_companies_pages():
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_companies), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            company_service.ListCompaniesResponse(
                companies=[company.Company(), company.Company(), company.Company(),],
                next_page_token="abc",
            ),
            company_service.ListCompaniesResponse(companies=[], next_page_token="def",),
            company_service.ListCompaniesResponse(
                companies=[company.Company(),], next_page_token="ghi",
            ),
            company_service.ListCompaniesResponse(
                companies=[company.Company(), company.Company(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_companies(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_companies_async_pager():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_companies), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            company_service.ListCompaniesResponse(
                companies=[company.Company(), company.Company(), company.Company(),],
                next_page_token="abc",
            ),
            company_service.ListCompaniesResponse(companies=[], next_page_token="def",),
            company_service.ListCompaniesResponse(
                companies=[company.Company(),], next_page_token="ghi",
            ),
            company_service.ListCompaniesResponse(
                companies=[company.Company(), company.Company(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_companies(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, company.Company) for i in responses)


@pytest.mark.asyncio
async def test_list_companies_async_pages():
    client = CompanyServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_companies), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            company_service.ListCompaniesResponse(
                companies=[company.Company(), company.Company(), company.Company(),],
                next_page_token="abc",
            ),
            company_service.ListCompaniesResponse(companies=[], next_page_token="def",),
            company_service.ListCompaniesResponse(
                companies=[company.Company(),], next_page_token="ghi",
            ),
            company_service.ListCompaniesResponse(
                companies=[company.Company(), company.Company(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_companies(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CompanyServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CompanyServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CompanyServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CompanyServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CompanyServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CompanyServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CompanyServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = CompanyServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CompanyServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CompanyServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CompanyServiceGrpcTransport,
        transports.CompanyServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CompanyServiceClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.CompanyServiceGrpcTransport,)


def test_company_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.CompanyServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_company_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.talent_v4.services.company_service.transports.CompanyServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CompanyServiceTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_company",
        "get_company",
        "update_company",
        "delete_company",
        "list_companies",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_company_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.talent_v4.services.company_service.transports.CompanyServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.CompanyServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            quota_project_id="octopus",
        )


def test_company_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.talent_v4.services.company_service.transports.CompanyServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.CompanyServiceTransport()
        adc.assert_called_once()


def test_company_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        CompanyServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            quota_project_id=None,
        )


def test_company_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.CompanyServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/jobs",
            ),
            quota_project_id="octopus",
        )


def test_company_service_host_no_port():
    client = CompanyServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint="jobs.googleapis.com"),
    )
    assert client.transport._host == "jobs.googleapis.com:443"


def test_company_service_host_with_port():
    client = CompanyServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="jobs.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "jobs.googleapis.com:8000"


def test_company_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.CompanyServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_company_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.CompanyServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CompanyServiceGrpcTransport,
        transports.CompanyServiceGrpcAsyncIOTransport,
    ],
)
def test_company_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
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
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/jobs",
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


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CompanyServiceGrpcTransport,
        transports.CompanyServiceGrpcAsyncIOTransport,
    ],
)
def test_company_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
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
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/jobs",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_company_path():
    project = "squid"
    tenant = "clam"
    company = "whelk"

    expected = "projects/{project}/tenants/{tenant}/companies/{company}".format(
        project=project, tenant=tenant, company=company,
    )
    actual = CompanyServiceClient.company_path(project, tenant, company)
    assert expected == actual


def test_parse_company_path():
    expected = {
        "project": "octopus",
        "tenant": "oyster",
        "company": "nudibranch",
    }
    path = CompanyServiceClient.company_path(**expected)

    # Check that the path construction is reversible.
    actual = CompanyServiceClient.parse_company_path(path)
    assert expected == actual


def test_tenant_path():
    project = "cuttlefish"
    tenant = "mussel"

    expected = "projects/{project}/tenants/{tenant}".format(
        project=project, tenant=tenant,
    )
    actual = CompanyServiceClient.tenant_path(project, tenant)
    assert expected == actual


def test_parse_tenant_path():
    expected = {
        "project": "winkle",
        "tenant": "nautilus",
    }
    path = CompanyServiceClient.tenant_path(**expected)

    # Check that the path construction is reversible.
    actual = CompanyServiceClient.parse_tenant_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CompanyServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = CompanyServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CompanyServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"

    expected = "folders/{folder}".format(folder=folder,)
    actual = CompanyServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = CompanyServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CompanyServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = CompanyServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = CompanyServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CompanyServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"

    expected = "projects/{project}".format(project=project,)
    actual = CompanyServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = CompanyServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CompanyServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = CompanyServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = CompanyServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CompanyServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CompanyServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CompanyServiceClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CompanyServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CompanyServiceClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
