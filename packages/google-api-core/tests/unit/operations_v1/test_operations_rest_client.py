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
import pytest

try:
    import grpc  # noqa: F401
except ImportError:
    pytest.skip("No GRPC", allow_module_level=True)
from requests import Response  # noqa I201
from requests.sessions import Session

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core.operations_v1 import AbstractOperationsClient
from google.api_core.operations_v1 import pagers
from google.api_core.operations_v1 import transports
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import json_format  # type: ignore
from google.rpc import status_pb2  # type: ignore


HTTP_OPTIONS = {
    "google.longrunning.Operations.CancelOperation": [
        {"method": "post", "uri": "/v3/{name=operations/*}:cancel", "body": "*"},
    ],
    "google.longrunning.Operations.DeleteOperation": [
        {"method": "delete", "uri": "/v3/{name=operations/*}"},
    ],
    "google.longrunning.Operations.GetOperation": [
        {"method": "get", "uri": "/v3/{name=operations/*}"},
    ],
    "google.longrunning.Operations.ListOperations": [
        {"method": "get", "uri": "/v3/{name=operations}"},
    ],
}


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def _get_operations_client(http_options=HTTP_OPTIONS):
    transport = transports.rest.OperationsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(), http_options=http_options
    )

    return AbstractOperationsClient(transport=transport)


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

    assert AbstractOperationsClient._get_default_mtls_endpoint(None) is None
    assert (
        AbstractOperationsClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AbstractOperationsClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        AbstractOperationsClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AbstractOperationsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        AbstractOperationsClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize("client_class", [AbstractOperationsClient])
def test_operations_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "longrunning.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name", [(transports.OperationsRestTransport, "rest")]
)
def test_operations_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class", [AbstractOperationsClient])
def test_operations_client_from_service_account_file(client_class):
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

        assert client.transport._host == "longrunning.googleapis.com:443"


def test_operations_client_get_transport_class():
    transport = AbstractOperationsClient.get_transport_class()
    available_transports = [
        transports.OperationsRestTransport,
    ]
    assert transport in available_transports

    transport = AbstractOperationsClient.get_transport_class("rest")
    assert transport == transports.OperationsRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(AbstractOperationsClient, transports.OperationsRestTransport, "rest")],
)
@mock.patch.object(
    AbstractOperationsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AbstractOperationsClient),
)
def test_operations_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(AbstractOperationsClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(AbstractOperationsClient, "get_transport_class") as gtc:
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
            always_use_jwt_access=True,
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
                always_use_jwt_access=True,
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
                always_use_jwt_access=True,
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
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (AbstractOperationsClient, transports.OperationsRestTransport, "rest", "true"),
        (AbstractOperationsClient, transports.OperationsRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    AbstractOperationsClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(AbstractOperationsClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_operations_client_mtls_env_auto(
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

        def fake_init(client_cert_source_for_mtls=None, **kwargs):
            """Invoke client_cert source if provided."""

            if client_cert_source_for_mtls:
                client_cert_source_for_mtls()
                return None

        with mock.patch.object(transport_class, "__init__") as patched:
            patched.side_effect = fake_init
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
                always_use_jwt_access=True,
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
                        always_use_jwt_access=True,
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
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(AbstractOperationsClient, transports.OperationsRestTransport, "rest")],
)
def test_operations_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
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
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(AbstractOperationsClient, transports.OperationsRestTransport, "rest")],
)
def test_operations_client_client_options_credentials_file(
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
            always_use_jwt_access=True,
        )


def test_list_operations_rest(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = _get_operations_client()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_operations(
            name="operations", filter_="my_filter", page_size=10, page_token="abc"
        )

        actual_args = req.call_args
        assert actual_args.args[0] == "GET"
        assert (
            actual_args.args[1]
            == "https://longrunning.googleapis.com:443/v3/operations"
        )
        assert actual_args.kwargs["params"] == [
            ("filter", "my_filter"),
            ("pageSize", 10),
            ("pageToken", "abc"),
        ]

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOperationsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_operations_rest_failure():
    client = _get_operations_client(http_options=None)

    with mock.patch.object(Session, "request") as req:
        response_value = Response()
        response_value.status_code = 400
        mock_request = mock.MagicMock()
        mock_request.method = "GET"
        mock_request.url = "https://longrunning.googleapis.com:443/v1/operations"
        response_value.request = mock_request
        req.return_value = response_value
        with pytest.raises(core_exceptions.GoogleAPIError):
            client.list_operations(name="operations")


def test_list_operations_rest_pager():
    client = AbstractOperationsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            operations_pb2.ListOperationsResponse(
                operations=[
                    operations_pb2.Operation(),
                    operations_pb2.Operation(),
                    operations_pb2.Operation(),
                ],
                next_page_token="abc",
            ),
            operations_pb2.ListOperationsResponse(
                operations=[],
                next_page_token="def",
            ),
            operations_pb2.ListOperationsResponse(
                operations=[operations_pb2.Operation()],
                next_page_token="ghi",
            ),
            operations_pb2.ListOperationsResponse(
                operations=[operations_pb2.Operation(), operations_pb2.Operation()],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(json_format.MessageToJson(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        pager = client.list_operations(name="operations")

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, operations_pb2.Operation) for i in results)

        pages = list(client.list_operations(name="operations").pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.next_page_token == token


def test_get_operation_rest(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = _get_operations_client()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(
            name="operations/sample1",
            done=True,
            error=status_pb2.Status(code=411),
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_operation("operations/sample1")

    actual_args = req.call_args
    assert actual_args.args[0] == "GET"
    assert (
        actual_args.args[1]
        == "https://longrunning.googleapis.com:443/v3/operations/sample1"
    )

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)
    assert response.name == "operations/sample1"
    assert response.done is True


def test_get_operation_rest_failure():
    client = _get_operations_client(http_options=None)

    with mock.patch.object(Session, "request") as req:
        response_value = Response()
        response_value.status_code = 400
        mock_request = mock.MagicMock()
        mock_request.method = "GET"
        mock_request.url = (
            "https://longrunning.googleapis.com:443/v1/operations/sample1"
        )
        response_value.request = mock_request
        req.return_value = response_value
        with pytest.raises(core_exceptions.GoogleAPIError):
            client.get_operation("operations/sample1")


def test_delete_operation_rest(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = _get_operations_client()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        client.delete_operation(name="operations/sample1")
        assert req.call_count == 1
        actual_args = req.call_args
        assert actual_args.args[0] == "DELETE"
        assert (
            actual_args.args[1]
            == "https://longrunning.googleapis.com:443/v3/operations/sample1"
        )


def test_delete_operation_rest_failure():
    client = _get_operations_client(http_options=None)

    with mock.patch.object(Session, "request") as req:
        response_value = Response()
        response_value.status_code = 400
        mock_request = mock.MagicMock()
        mock_request.method = "DELETE"
        mock_request.url = (
            "https://longrunning.googleapis.com:443/v1/operations/sample1"
        )
        response_value.request = mock_request
        req.return_value = response_value
        with pytest.raises(core_exceptions.GoogleAPIError):
            client.delete_operation(name="operations/sample1")


def test_cancel_operation_rest(transport: str = "rest"):
    client = _get_operations_client()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        client.cancel_operation(name="operations/sample1")
        assert req.call_count == 1
        actual_args = req.call_args
        assert actual_args.args[0] == "POST"
        assert (
            actual_args.args[1]
            == "https://longrunning.googleapis.com:443/v3/operations/sample1:cancel"
        )


def test_cancel_operation_rest_failure():
    client = _get_operations_client(http_options=None)

    with mock.patch.object(Session, "request") as req:
        response_value = Response()
        response_value.status_code = 400
        mock_request = mock.MagicMock()
        mock_request.method = "POST"
        mock_request.url = (
            "https://longrunning.googleapis.com:443/v1/operations/sample1:cancel"
        )
        response_value.request = mock_request
        req.return_value = response_value
        with pytest.raises(core_exceptions.GoogleAPIError):
            client.cancel_operation(name="operations/sample1")


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.OperationsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        AbstractOperationsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.OperationsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        AbstractOperationsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.OperationsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        AbstractOperationsClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OperationsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = AbstractOperationsClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize("transport_class", [transports.OperationsRestTransport])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_operations_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transports.OperationsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_operations_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.api_core.operations_v1.transports.OperationsTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.OperationsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_operations",
        "get_operation",
        "delete_operation",
        "cancel_operation",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_operations_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.api_core.operations_v1.transports.OperationsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transports.OperationsTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(),
            quota_project_id="octopus",
        )


def test_operations_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.api_core.operations_v1.transports.OperationsTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transports.OperationsTransport()
        adc.assert_called_once()


def test_operations_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        AbstractOperationsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(),
            quota_project_id=None,
        )


def test_operations_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.OperationsRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_operations_host_no_port():
    client = AbstractOperationsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="longrunning.googleapis.com"
        ),
    )
    assert client.transport._host == "longrunning.googleapis.com:443"


def test_operations_host_with_port():
    client = AbstractOperationsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="longrunning.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "longrunning.googleapis.com:8000"


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = AbstractOperationsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = AbstractOperationsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = AbstractOperationsClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = AbstractOperationsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = AbstractOperationsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = AbstractOperationsClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = AbstractOperationsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = AbstractOperationsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = AbstractOperationsClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = AbstractOperationsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = AbstractOperationsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = AbstractOperationsClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = AbstractOperationsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = AbstractOperationsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = AbstractOperationsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.OperationsTransport, "_prep_wrapped_messages"
    ) as prep:
        AbstractOperationsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.OperationsTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = AbstractOperationsClient.get_transport_class()
        transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
