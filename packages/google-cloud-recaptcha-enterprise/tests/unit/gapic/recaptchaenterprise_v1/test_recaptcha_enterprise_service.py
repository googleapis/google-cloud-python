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

from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import grpc_helpers
from google.auth import credentials
from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    RecaptchaEnterpriseServiceClient,
)
from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    pagers,
)
from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    transports,
)
from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        RecaptchaEnterpriseServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test_recaptcha_enterprise_service_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = RecaptchaEnterpriseServiceClient.from_service_account_file(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        client = RecaptchaEnterpriseServiceClient.from_service_account_json(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        assert client._transport._host == "recaptchaenterprise.googleapis.com:443"


def test_recaptcha_enterprise_service_client_client_options():
    # Check that if channel is provided we won't create a new one.
    with mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.RecaptchaEnterpriseServiceClient.get_transport_class"
    ) as gtc:
        transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
            credentials=credentials.AnonymousCredentials()
        )
        client = RecaptchaEnterpriseServiceClient(transport=transport)
        gtc.assert_not_called()

    # Check mTLS is not triggered with empty client options.
    options = client_options.ClientOptions()
    with mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.RecaptchaEnterpriseServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = RecaptchaEnterpriseServiceClient(client_options=options)
        transport.assert_called_once_with(
            credentials=None, host=client.DEFAULT_ENDPOINT
        )

    # Check mTLS is not triggered if api_endpoint is provided but
    # client_cert_source is None.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.transports.RecaptchaEnterpriseServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RecaptchaEnterpriseServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )

    # Check mTLS is triggered if client_cert_source is provided.
    options = client_options.ClientOptions(
        client_cert_source=client_cert_source_callback
    )
    with mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.transports.RecaptchaEnterpriseServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RecaptchaEnterpriseServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is triggered if api_endpoint and client_cert_source are provided.
    options = client_options.ClientOptions(
        api_endpoint="squid.clam.whelk", client_cert_source=client_cert_source_callback
    )
    with mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.transports.RecaptchaEnterpriseServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RecaptchaEnterpriseServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_recaptcha_enterprise_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.transports.RecaptchaEnterpriseServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RecaptchaEnterpriseServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_create_assessment(transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recaptchaenterprise.CreateAssessmentRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Assessment(name="name_value")

        response = client.create_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Assessment)
    assert response.name == "name_value"


def test_create_assessment_flattened():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials()
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Assessment()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_assessment(
            parent="parent_value",
            assessment=recaptchaenterprise.Assessment(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].assessment == recaptchaenterprise.Assessment(name="name_value")


def test_create_assessment_flattened_error():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials()
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_assessment(
            recaptchaenterprise.CreateAssessmentRequest(),
            parent="parent_value",
            assessment=recaptchaenterprise.Assessment(name="name_value"),
        )


def test_annotate_assessment(transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recaptchaenterprise.AnnotateAssessmentRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.annotate_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.AnnotateAssessmentResponse()

        response = client.annotate_assessment(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.AnnotateAssessmentResponse)


def test_annotate_assessment_flattened():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials()
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.annotate_assessment), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.AnnotateAssessmentResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.annotate_assessment(
            name="name_value",
            annotation=recaptchaenterprise.AnnotateAssessmentRequest.Annotation.LEGITIMATE,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert (
            args[0].annotation
            == recaptchaenterprise.AnnotateAssessmentRequest.Annotation.LEGITIMATE
        )


def test_annotate_assessment_flattened_error():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials()
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.annotate_assessment(
            recaptchaenterprise.AnnotateAssessmentRequest(),
            name="name_value",
            annotation=recaptchaenterprise.AnnotateAssessmentRequest.Annotation.LEGITIMATE,
        )


def test_create_key(transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recaptchaenterprise.CreateKeyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Key(
            name="name_value", display_name="display_name_value"
        )

        response = client.create_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_list_keys(transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recaptchaenterprise.ListKeysRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_keys), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.ListKeysResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListKeysPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_keys_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.ListKeysRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_keys), "__call__") as call:
        call.return_value = recaptchaenterprise.ListKeysResponse()
        client.list_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_keys_pager():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListKeysResponse(
                keys=[
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListKeysResponse(keys=[], next_page_token="def"),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key()], next_page_token="ghi"
            ),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(), recaptchaenterprise.Key()]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_keys(request={})]
        assert len(results) == 6
        assert all(isinstance(i, recaptchaenterprise.Key) for i in results)


def test_list_keys_pages():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_keys), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            recaptchaenterprise.ListKeysResponse(
                keys=[
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                    recaptchaenterprise.Key(),
                ],
                next_page_token="abc",
            ),
            recaptchaenterprise.ListKeysResponse(keys=[], next_page_token="def"),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key()], next_page_token="ghi"
            ),
            recaptchaenterprise.ListKeysResponse(
                keys=[recaptchaenterprise.Key(), recaptchaenterprise.Key()]
            ),
            RuntimeError,
        )
        pages = list(client.list_keys(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_key(transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recaptchaenterprise.GetKeyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Key(
            name="name_value", display_name="display_name_value"
        )

        response = client.get_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_get_key_field_headers():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials()
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = recaptchaenterprise.GetKeyRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_key), "__call__") as call:
        call.return_value = recaptchaenterprise.Key()
        client.get_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_update_key(transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recaptchaenterprise.UpdateKeyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = recaptchaenterprise.Key(
            name="name_value", display_name="display_name_value"
        )

        response = client.update_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, recaptchaenterprise.Key)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_delete_key(transport: str = "grpc"):
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = recaptchaenterprise.DeleteKeyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_key), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = RecaptchaEnterpriseServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = RecaptchaEnterpriseServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials()
    )
    assert isinstance(
        client._transport, transports.RecaptchaEnterpriseServiceGrpcTransport
    )


def test_recaptcha_enterprise_service_base_transport():
    # Instantiate the base transport.
    transport = transports.RecaptchaEnterpriseServiceTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_assessment",
        "annotate_assessment",
        "create_key",
        "list_keys",
        "get_key",
        "update_key",
        "delete_key",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_recaptcha_enterprise_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        RecaptchaEnterpriseServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_recaptcha_enterprise_service_host_no_port():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recaptchaenterprise.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "recaptchaenterprise.googleapis.com:443"


def test_recaptcha_enterprise_service_host_with_port():
    client = RecaptchaEnterpriseServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recaptchaenterprise.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "recaptchaenterprise.googleapis.com:8000"


def test_recaptcha_enterprise_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
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
def test_recaptcha_enterprise_service_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
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
        ssl_credentials=mock_ssl_cred,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_recaptcha_enterprise_service_grpc_transport_channel_mtls_with_adc(
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
        transport = transports.RecaptchaEnterpriseServiceGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            ssl_credentials=mock_ssl_cred,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_assessment_path():
    project = "squid"
    assessment = "clam"

    expected = "projects/{project}/assessments/{assessment}".format(
        project=project, assessment=assessment
    )
    actual = RecaptchaEnterpriseServiceClient.assessment_path(project, assessment)
    assert expected == actual


def test_parse_assessment_path():
    expected = {"project": "whelk", "assessment": "octopus"}
    path = RecaptchaEnterpriseServiceClient.assessment_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_assessment_path(path)
    assert expected == actual


def test_key_path():
    project = "squid"
    key = "clam"

    expected = "projects/{project}/keys/{key}".format(project=project, key=key)
    actual = RecaptchaEnterpriseServiceClient.key_path(project, key)
    assert expected == actual


def test_parse_key_path():
    expected = {"project": "whelk", "key": "octopus"}
    path = RecaptchaEnterpriseServiceClient.key_path(**expected)

    # Check that the path construction is reversible.
    actual = RecaptchaEnterpriseServiceClient.parse_key_path(path)
    assert expected == actual
