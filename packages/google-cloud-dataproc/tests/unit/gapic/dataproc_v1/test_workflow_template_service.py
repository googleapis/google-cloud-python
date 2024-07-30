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
import os

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

from collections.abc import Iterable
import json
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
from google.api_core import api_core_version, client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import operation_async  # type: ignore
from google.api_core import retry as retries
import google.auth
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import options_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from google.protobuf import timestamp_pb2  # type: ignore
import grpc
from grpc.experimental import aio
from proto.marshal.rules import wrappers
from proto.marshal.rules.dates import DurationRule, TimestampRule
import pytest
from requests import PreparedRequest, Request, Response
from requests.sessions import Session

from google.cloud.dataproc_v1.services.workflow_template_service import (
    WorkflowTemplateServiceAsyncClient,
    WorkflowTemplateServiceClient,
    pagers,
    transports,
)
from google.cloud.dataproc_v1.types import clusters, jobs, shared, workflow_templates


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


# If default endpoint template is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint template so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint_template(client):
    return (
        "test.{UNIVERSE_DOMAIN}"
        if ("localhost" in client._DEFAULT_ENDPOINT_TEMPLATE)
        else client._DEFAULT_ENDPOINT_TEMPLATE
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert WorkflowTemplateServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        WorkflowTemplateServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        WorkflowTemplateServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        WorkflowTemplateServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        WorkflowTemplateServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        WorkflowTemplateServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test__read_environment_variables():
    assert WorkflowTemplateServiceClient._read_environment_variables() == (
        False,
        "auto",
        None,
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        assert WorkflowTemplateServiceClient._read_environment_variables() == (
            True,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        assert WorkflowTemplateServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            WorkflowTemplateServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        assert WorkflowTemplateServiceClient._read_environment_variables() == (
            False,
            "never",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        assert WorkflowTemplateServiceClient._read_environment_variables() == (
            False,
            "always",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"}):
        assert WorkflowTemplateServiceClient._read_environment_variables() == (
            False,
            "auto",
            None,
        )

    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            WorkflowTemplateServiceClient._read_environment_variables()
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    with mock.patch.dict(os.environ, {"GOOGLE_CLOUD_UNIVERSE_DOMAIN": "foo.com"}):
        assert WorkflowTemplateServiceClient._read_environment_variables() == (
            False,
            "auto",
            "foo.com",
        )


def test__get_client_cert_source():
    mock_provided_cert_source = mock.Mock()
    mock_default_cert_source = mock.Mock()

    assert WorkflowTemplateServiceClient._get_client_cert_source(None, False) is None
    assert (
        WorkflowTemplateServiceClient._get_client_cert_source(
            mock_provided_cert_source, False
        )
        is None
    )
    assert (
        WorkflowTemplateServiceClient._get_client_cert_source(
            mock_provided_cert_source, True
        )
        == mock_provided_cert_source
    )

    with mock.patch(
        "google.auth.transport.mtls.has_default_client_cert_source", return_value=True
    ):
        with mock.patch(
            "google.auth.transport.mtls.default_client_cert_source",
            return_value=mock_default_cert_source,
        ):
            assert (
                WorkflowTemplateServiceClient._get_client_cert_source(None, True)
                is mock_default_cert_source
            )
            assert (
                WorkflowTemplateServiceClient._get_client_cert_source(
                    mock_provided_cert_source, "true"
                )
                is mock_provided_cert_source
            )


@mock.patch.object(
    WorkflowTemplateServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(WorkflowTemplateServiceClient),
)
@mock.patch.object(
    WorkflowTemplateServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(WorkflowTemplateServiceAsyncClient),
)
def test__get_api_endpoint():
    api_override = "foo.com"
    mock_client_cert_source = mock.Mock()
    default_universe = WorkflowTemplateServiceClient._DEFAULT_UNIVERSE
    default_endpoint = WorkflowTemplateServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = WorkflowTemplateServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    assert (
        WorkflowTemplateServiceClient._get_api_endpoint(
            api_override, mock_client_cert_source, default_universe, "always"
        )
        == api_override
    )
    assert (
        WorkflowTemplateServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "auto"
        )
        == WorkflowTemplateServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        WorkflowTemplateServiceClient._get_api_endpoint(
            None, None, default_universe, "auto"
        )
        == default_endpoint
    )
    assert (
        WorkflowTemplateServiceClient._get_api_endpoint(
            None, None, default_universe, "always"
        )
        == WorkflowTemplateServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        WorkflowTemplateServiceClient._get_api_endpoint(
            None, mock_client_cert_source, default_universe, "always"
        )
        == WorkflowTemplateServiceClient.DEFAULT_MTLS_ENDPOINT
    )
    assert (
        WorkflowTemplateServiceClient._get_api_endpoint(
            None, None, mock_universe, "never"
        )
        == mock_endpoint
    )
    assert (
        WorkflowTemplateServiceClient._get_api_endpoint(
            None, None, default_universe, "never"
        )
        == default_endpoint
    )

    with pytest.raises(MutualTLSChannelError) as excinfo:
        WorkflowTemplateServiceClient._get_api_endpoint(
            None, mock_client_cert_source, mock_universe, "auto"
        )
    assert (
        str(excinfo.value)
        == "mTLS is not supported in any universe other than googleapis.com."
    )


def test__get_universe_domain():
    client_universe_domain = "foo.com"
    universe_domain_env = "bar.com"

    assert (
        WorkflowTemplateServiceClient._get_universe_domain(
            client_universe_domain, universe_domain_env
        )
        == client_universe_domain
    )
    assert (
        WorkflowTemplateServiceClient._get_universe_domain(None, universe_domain_env)
        == universe_domain_env
    )
    assert (
        WorkflowTemplateServiceClient._get_universe_domain(None, None)
        == WorkflowTemplateServiceClient._DEFAULT_UNIVERSE
    )

    with pytest.raises(ValueError) as excinfo:
        WorkflowTemplateServiceClient._get_universe_domain("", None)
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceGrpcTransport,
            "grpc",
        ),
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceRestTransport,
            "rest",
        ),
    ],
)
def test__validate_universe_domain(client_class, transport_class, transport_name):
    client = client_class(
        transport=transport_class(credentials=ga_credentials.AnonymousCredentials())
    )
    assert client._validate_universe_domain() == True

    # Test the case when universe is already validated.
    assert client._validate_universe_domain() == True

    if transport_name == "grpc":
        # Test the case where credentials are provided by the
        # `local_channel_credentials`. The default universes in both match.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        client = client_class(transport=transport_class(channel=channel))
        assert client._validate_universe_domain() == True

        # Test the case where credentials do not exist: e.g. a transport is provided
        # with no credentials. Validation should still succeed because there is no
        # mismatch with non-existent credentials.
        channel = grpc.secure_channel(
            "http://localhost/", grpc.local_channel_credentials()
        )
        transport = transport_class(channel=channel)
        transport._credentials = None
        client = client_class(transport=transport)
        assert client._validate_universe_domain() == True

    # TODO: This is needed to cater for older versions of google-auth
    # Make this test unconditional once the minimum supported version of
    # google-auth becomes 2.23.0 or higher.
    google_auth_major, google_auth_minor = [
        int(part) for part in google.auth.__version__.split(".")[0:2]
    ]
    if google_auth_major > 2 or (google_auth_major == 2 and google_auth_minor >= 23):
        credentials = ga_credentials.AnonymousCredentials()
        credentials._universe_domain = "foo.com"
        # Test the case when there is a universe mismatch from the credentials.
        client = client_class(transport=transport_class(credentials=credentials))
        with pytest.raises(ValueError) as excinfo:
            client._validate_universe_domain()
        assert (
            str(excinfo.value)
            == "The configured universe domain (googleapis.com) does not match the universe domain found in the credentials (foo.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
        )

        # Test the case when there is a universe mismatch from the client.
        #
        # TODO: Make this test unconditional once the minimum supported version of
        # google-api-core becomes 2.15.0 or higher.
        api_core_major, api_core_minor = [
            int(part) for part in api_core_version.__version__.split(".")[0:2]
        ]
        if api_core_major > 2 or (api_core_major == 2 and api_core_minor >= 15):
            client = client_class(
                client_options={"universe_domain": "bar.com"},
                transport=transport_class(
                    credentials=ga_credentials.AnonymousCredentials(),
                ),
            )
            with pytest.raises(ValueError) as excinfo:
                client._validate_universe_domain()
            assert (
                str(excinfo.value)
                == "The configured universe domain (bar.com) does not match the universe domain found in the credentials (googleapis.com). If you haven't configured the universe domain explicitly, `googleapis.com` is the default."
            )

    # Test that ValueError is raised if universe_domain is provided via client options and credentials is None
    with pytest.raises(ValueError):
        client._compare_universes("foo.bar", None)


@pytest.mark.parametrize(
    "client_class,transport_name",
    [
        (WorkflowTemplateServiceClient, "grpc"),
        (WorkflowTemplateServiceAsyncClient, "grpc_asyncio"),
        (WorkflowTemplateServiceClient, "rest"),
    ],
)
def test_workflow_template_service_client_from_service_account_info(
    client_class, transport_name
):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            "dataproc.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dataproc.googleapis.com"
        )


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.WorkflowTemplateServiceGrpcTransport, "grpc"),
        (transports.WorkflowTemplateServiceGrpcAsyncIOTransport, "grpc_asyncio"),
        (transports.WorkflowTemplateServiceRestTransport, "rest"),
    ],
)
def test_workflow_template_service_client_service_account_always_use_jwt(
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
        (WorkflowTemplateServiceClient, "grpc"),
        (WorkflowTemplateServiceAsyncClient, "grpc_asyncio"),
        (WorkflowTemplateServiceClient, "rest"),
    ],
)
def test_workflow_template_service_client_from_service_account_file(
    client_class, transport_name
):
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

        assert client.transport._host == (
            "dataproc.googleapis.com:443"
            if transport_name in ["grpc", "grpc_asyncio"]
            else "https://dataproc.googleapis.com"
        )


def test_workflow_template_service_client_get_transport_class():
    transport = WorkflowTemplateServiceClient.get_transport_class()
    available_transports = [
        transports.WorkflowTemplateServiceGrpcTransport,
        transports.WorkflowTemplateServiceRestTransport,
    ]
    assert transport in available_transports

    transport = WorkflowTemplateServiceClient.get_transport_class("grpc")
    assert transport == transports.WorkflowTemplateServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceGrpcTransport,
            "grpc",
        ),
        (
            WorkflowTemplateServiceAsyncClient,
            transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceRestTransport,
            "rest",
        ),
    ],
)
@mock.patch.object(
    WorkflowTemplateServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(WorkflowTemplateServiceClient),
)
@mock.patch.object(
    WorkflowTemplateServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(WorkflowTemplateServiceAsyncClient),
)
def test_workflow_template_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(WorkflowTemplateServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(WorkflowTemplateServiceClient, "get_transport_class") as gtc:
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
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
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
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
    )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client = client_class(transport=transport_name)
    assert (
        str(excinfo.value)
        == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
    )

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
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
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
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
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            WorkflowTemplateServiceAsyncClient,
            transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            WorkflowTemplateServiceAsyncClient,
            transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceRestTransport,
            "rest",
            "true",
        ),
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceRestTransport,
            "rest",
            "false",
        ),
    ],
)
@mock.patch.object(
    WorkflowTemplateServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(WorkflowTemplateServiceClient),
)
@mock.patch.object(
    WorkflowTemplateServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(WorkflowTemplateServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_workflow_template_service_client_mtls_env_auto(
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
                expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                )
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
                        expected_host = client._DEFAULT_ENDPOINT_TEMPLATE.format(
                            UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                        )
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
                    host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                        UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                    ),
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize(
    "client_class", [WorkflowTemplateServiceClient, WorkflowTemplateServiceAsyncClient]
)
@mock.patch.object(
    WorkflowTemplateServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(WorkflowTemplateServiceClient),
)
@mock.patch.object(
    WorkflowTemplateServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(WorkflowTemplateServiceAsyncClient),
)
def test_workflow_template_service_client_get_mtls_endpoint_and_cert_source(
    client_class,
):
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

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
        )

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError) as excinfo:
            client_class.get_mtls_endpoint_and_cert_source()

        assert (
            str(excinfo.value)
            == "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
        )


@pytest.mark.parametrize(
    "client_class", [WorkflowTemplateServiceClient, WorkflowTemplateServiceAsyncClient]
)
@mock.patch.object(
    WorkflowTemplateServiceClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(WorkflowTemplateServiceClient),
)
@mock.patch.object(
    WorkflowTemplateServiceAsyncClient,
    "_DEFAULT_ENDPOINT_TEMPLATE",
    modify_default_endpoint_template(WorkflowTemplateServiceAsyncClient),
)
def test_workflow_template_service_client_client_api_endpoint(client_class):
    mock_client_cert_source = client_cert_source_callback
    api_override = "foo.com"
    default_universe = WorkflowTemplateServiceClient._DEFAULT_UNIVERSE
    default_endpoint = WorkflowTemplateServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=default_universe
    )
    mock_universe = "bar.com"
    mock_endpoint = WorkflowTemplateServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
        UNIVERSE_DOMAIN=mock_universe
    )

    # If ClientOptions.api_endpoint is set and GOOGLE_API_USE_CLIENT_CERTIFICATE="true",
    # use ClientOptions.api_endpoint as the api endpoint regardless.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
        ):
            options = client_options.ClientOptions(
                client_cert_source=mock_client_cert_source, api_endpoint=api_override
            )
            client = client_class(
                client_options=options,
                credentials=ga_credentials.AnonymousCredentials(),
            )
            assert client.api_endpoint == api_override

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == default_endpoint

    # If ClientOptions.api_endpoint is not set and GOOGLE_API_USE_MTLS_ENDPOINT="always",
    # use the DEFAULT_MTLS_ENDPOINT as the api endpoint.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        client = client_class(credentials=ga_credentials.AnonymousCredentials())
        assert client.api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT

    # If ClientOptions.api_endpoint is not set, GOOGLE_API_USE_MTLS_ENDPOINT="auto" (default),
    # GOOGLE_API_USE_CLIENT_CERTIFICATE="false" (default), default cert source doesn't exist,
    # and ClientOptions.universe_domain="bar.com",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with universe domain as the api endpoint.
    options = client_options.ClientOptions()
    universe_exists = hasattr(options, "universe_domain")
    if universe_exists:
        options = client_options.ClientOptions(universe_domain=mock_universe)
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    else:
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
    assert client.api_endpoint == (
        mock_endpoint if universe_exists else default_endpoint
    )
    assert client.universe_domain == (
        mock_universe if universe_exists else default_universe
    )

    # If ClientOptions does not have a universe domain attribute and GOOGLE_API_USE_MTLS_ENDPOINT="never",
    # use the _DEFAULT_ENDPOINT_TEMPLATE populated with GDU as the api endpoint.
    options = client_options.ClientOptions()
    if hasattr(options, "universe_domain"):
        delattr(options, "universe_domain")
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        client = client_class(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )
        assert client.api_endpoint == default_endpoint


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceGrpcTransport,
            "grpc",
        ),
        (
            WorkflowTemplateServiceAsyncClient,
            transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceRestTransport,
            "rest",
        ),
    ],
)
def test_workflow_template_service_client_client_options_scopes(
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
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
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
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            WorkflowTemplateServiceAsyncClient,
            transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceRestTransport,
            "rest",
            None,
        ),
    ],
)
def test_workflow_template_service_client_client_options_credentials_file(
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
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


def test_workflow_template_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.dataproc_v1.services.workflow_template_service.transports.WorkflowTemplateServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = WorkflowTemplateServiceClient(
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
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceGrpcTransport,
            "grpc",
            grpc_helpers,
        ),
        (
            WorkflowTemplateServiceAsyncClient,
            transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_workflow_template_service_client_create_channel_credentials_file(
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
            host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
            ),
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
            "dataproc.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="dataproc.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.CreateWorkflowTemplateRequest,
        dict,
    ],
)
def test_create_workflow_template(request_type, transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.WorkflowTemplate(
            id="id_value",
            name="name_value",
            version=774,
        )
        response = client.create_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.CreateWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflow_templates.WorkflowTemplate)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.version == 774


def test_create_workflow_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.CreateWorkflowTemplateRequest()


def test_create_workflow_template_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = workflow_templates.CreateWorkflowTemplateRequest(
        parent="parent_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.create_workflow_template(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.CreateWorkflowTemplateRequest(
            parent="parent_value",
        )


def test_create_workflow_template_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_workflow_template
        ] = mock_rpc
        request = {}
        client.create_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_create_workflow_template_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate(
                id="id_value",
                name="name_value",
                version=774,
            )
        )
        response = await client.create_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.CreateWorkflowTemplateRequest()


@pytest.mark.asyncio
async def test_create_workflow_template_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.create_workflow_template
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.create_workflow_template
        ] = mock_object

        request = {}
        await client.create_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.create_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_create_workflow_template_async(
    transport: str = "grpc_asyncio",
    request_type=workflow_templates.CreateWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate(
                id="id_value",
                name="name_value",
                version=774,
            )
        )
        response = await client.create_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.CreateWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflow_templates.WorkflowTemplate)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.version == 774


@pytest.mark.asyncio
async def test_create_workflow_template_async_from_dict():
    await test_create_workflow_template_async(request_type=dict)


def test_create_workflow_template_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.CreateWorkflowTemplateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_template), "__call__"
    ) as call:
        call.return_value = workflow_templates.WorkflowTemplate()
        client.create_workflow_template(request)

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
async def test_create_workflow_template_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.CreateWorkflowTemplateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate()
        )
        await client.create_workflow_template(request)

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


def test_create_workflow_template_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.WorkflowTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_workflow_template(
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].template
        mock_val = workflow_templates.WorkflowTemplate(id="id_value")
        assert arg == mock_val


def test_create_workflow_template_flattened_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_workflow_template(
            workflow_templates.CreateWorkflowTemplateRequest(),
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )


@pytest.mark.asyncio
async def test_create_workflow_template_flattened_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.WorkflowTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_workflow_template(
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].template
        mock_val = workflow_templates.WorkflowTemplate(id="id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_workflow_template_flattened_error_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_workflow_template(
            workflow_templates.CreateWorkflowTemplateRequest(),
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.GetWorkflowTemplateRequest,
        dict,
    ],
)
def test_get_workflow_template(request_type, transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.WorkflowTemplate(
            id="id_value",
            name="name_value",
            version=774,
        )
        response = client.get_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.GetWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflow_templates.WorkflowTemplate)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.version == 774


def test_get_workflow_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.GetWorkflowTemplateRequest()


def test_get_workflow_template_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = workflow_templates.GetWorkflowTemplateRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.get_workflow_template(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.GetWorkflowTemplateRequest(
            name="name_value",
        )


def test_get_workflow_template_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_workflow_template
        ] = mock_rpc
        request = {}
        client.get_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_get_workflow_template_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate(
                id="id_value",
                name="name_value",
                version=774,
            )
        )
        response = await client.get_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.GetWorkflowTemplateRequest()


@pytest.mark.asyncio
async def test_get_workflow_template_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.get_workflow_template
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.get_workflow_template
        ] = mock_object

        request = {}
        await client.get_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.get_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_get_workflow_template_async(
    transport: str = "grpc_asyncio",
    request_type=workflow_templates.GetWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate(
                id="id_value",
                name="name_value",
                version=774,
            )
        )
        response = await client.get_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.GetWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflow_templates.WorkflowTemplate)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.version == 774


@pytest.mark.asyncio
async def test_get_workflow_template_async_from_dict():
    await test_get_workflow_template_async(request_type=dict)


def test_get_workflow_template_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.GetWorkflowTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_template), "__call__"
    ) as call:
        call.return_value = workflow_templates.WorkflowTemplate()
        client.get_workflow_template(request)

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
async def test_get_workflow_template_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.GetWorkflowTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate()
        )
        await client.get_workflow_template(request)

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


def test_get_workflow_template_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.WorkflowTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_workflow_template(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_workflow_template_flattened_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_workflow_template(
            workflow_templates.GetWorkflowTemplateRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_workflow_template_flattened_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.WorkflowTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_workflow_template(
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
async def test_get_workflow_template_flattened_error_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_workflow_template(
            workflow_templates.GetWorkflowTemplateRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.InstantiateWorkflowTemplateRequest,
        dict,
    ],
)
def test_instantiate_workflow_template(request_type, transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.instantiate_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.InstantiateWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_instantiate_workflow_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.instantiate_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.InstantiateWorkflowTemplateRequest()


def test_instantiate_workflow_template_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = workflow_templates.InstantiateWorkflowTemplateRequest(
        name="name_value",
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.instantiate_workflow_template(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.InstantiateWorkflowTemplateRequest(
            name="name_value",
            request_id="request_id_value",
        )


def test_instantiate_workflow_template_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.instantiate_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.instantiate_workflow_template
        ] = mock_rpc
        request = {}
        client.instantiate_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.instantiate_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_instantiate_workflow_template_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.instantiate_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.InstantiateWorkflowTemplateRequest()


@pytest.mark.asyncio
async def test_instantiate_workflow_template_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.instantiate_workflow_template
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.instantiate_workflow_template
        ] = mock_object

        request = {}
        await client.instantiate_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.instantiate_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_instantiate_workflow_template_async(
    transport: str = "grpc_asyncio",
    request_type=workflow_templates.InstantiateWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.instantiate_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.InstantiateWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_instantiate_workflow_template_async_from_dict():
    await test_instantiate_workflow_template_async(request_type=dict)


def test_instantiate_workflow_template_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.InstantiateWorkflowTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_workflow_template), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.instantiate_workflow_template(request)

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
async def test_instantiate_workflow_template_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.InstantiateWorkflowTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_workflow_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.instantiate_workflow_template(request)

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


def test_instantiate_workflow_template_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.instantiate_workflow_template(
            name="name_value",
            parameters={"key_value": "value_value"},
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].parameters
        mock_val = {"key_value": "value_value"}
        assert arg == mock_val


def test_instantiate_workflow_template_flattened_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.instantiate_workflow_template(
            workflow_templates.InstantiateWorkflowTemplateRequest(),
            name="name_value",
            parameters={"key_value": "value_value"},
        )


@pytest.mark.asyncio
async def test_instantiate_workflow_template_flattened_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.instantiate_workflow_template(
            name="name_value",
            parameters={"key_value": "value_value"},
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].parameters
        mock_val = {"key_value": "value_value"}
        assert arg == mock_val


@pytest.mark.asyncio
async def test_instantiate_workflow_template_flattened_error_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.instantiate_workflow_template(
            workflow_templates.InstantiateWorkflowTemplateRequest(),
            name="name_value",
            parameters={"key_value": "value_value"},
        )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.InstantiateInlineWorkflowTemplateRequest,
        dict,
    ],
)
def test_instantiate_inline_workflow_template(request_type, transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_inline_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.instantiate_inline_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.InstantiateInlineWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_instantiate_inline_workflow_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_inline_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.instantiate_inline_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.InstantiateInlineWorkflowTemplateRequest()


def test_instantiate_inline_workflow_template_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = workflow_templates.InstantiateInlineWorkflowTemplateRequest(
        parent="parent_value",
        request_id="request_id_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_inline_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.instantiate_inline_workflow_template(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.InstantiateInlineWorkflowTemplateRequest(
            parent="parent_value",
            request_id="request_id_value",
        )


def test_instantiate_inline_workflow_template_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.instantiate_inline_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.instantiate_inline_workflow_template
        ] = mock_rpc
        request = {}
        client.instantiate_inline_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.instantiate_inline_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_instantiate_inline_workflow_template_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_inline_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.instantiate_inline_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.InstantiateInlineWorkflowTemplateRequest()


@pytest.mark.asyncio
async def test_instantiate_inline_workflow_template_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.instantiate_inline_workflow_template
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.instantiate_inline_workflow_template
        ] = mock_object

        request = {}
        await client.instantiate_inline_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        await client.instantiate_inline_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_instantiate_inline_workflow_template_async(
    transport: str = "grpc_asyncio",
    request_type=workflow_templates.InstantiateInlineWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_inline_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.instantiate_inline_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.InstantiateInlineWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_instantiate_inline_workflow_template_async_from_dict():
    await test_instantiate_inline_workflow_template_async(request_type=dict)


def test_instantiate_inline_workflow_template_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.InstantiateInlineWorkflowTemplateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_inline_workflow_template), "__call__"
    ) as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.instantiate_inline_workflow_template(request)

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
async def test_instantiate_inline_workflow_template_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.InstantiateInlineWorkflowTemplateRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_inline_workflow_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.instantiate_inline_workflow_template(request)

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


def test_instantiate_inline_workflow_template_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_inline_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.instantiate_inline_workflow_template(
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].template
        mock_val = workflow_templates.WorkflowTemplate(id="id_value")
        assert arg == mock_val


def test_instantiate_inline_workflow_template_flattened_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.instantiate_inline_workflow_template(
            workflow_templates.InstantiateInlineWorkflowTemplateRequest(),
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )


@pytest.mark.asyncio
async def test_instantiate_inline_workflow_template_flattened_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.instantiate_inline_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.instantiate_inline_workflow_template(
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].template
        mock_val = workflow_templates.WorkflowTemplate(id="id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_instantiate_inline_workflow_template_flattened_error_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.instantiate_inline_workflow_template(
            workflow_templates.InstantiateInlineWorkflowTemplateRequest(),
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.UpdateWorkflowTemplateRequest,
        dict,
    ],
)
def test_update_workflow_template(request_type, transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.WorkflowTemplate(
            id="id_value",
            name="name_value",
            version=774,
        )
        response = client.update_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.UpdateWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflow_templates.WorkflowTemplate)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.version == 774


def test_update_workflow_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.UpdateWorkflowTemplateRequest()


def test_update_workflow_template_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = workflow_templates.UpdateWorkflowTemplateRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.update_workflow_template(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.UpdateWorkflowTemplateRequest()


def test_update_workflow_template_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_workflow_template
        ] = mock_rpc
        request = {}
        client.update_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_update_workflow_template_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate(
                id="id_value",
                name="name_value",
                version=774,
            )
        )
        response = await client.update_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.UpdateWorkflowTemplateRequest()


@pytest.mark.asyncio
async def test_update_workflow_template_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.update_workflow_template
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.update_workflow_template
        ] = mock_object

        request = {}
        await client.update_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.update_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_update_workflow_template_async(
    transport: str = "grpc_asyncio",
    request_type=workflow_templates.UpdateWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate(
                id="id_value",
                name="name_value",
                version=774,
            )
        )
        response = await client.update_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.UpdateWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflow_templates.WorkflowTemplate)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.version == 774


@pytest.mark.asyncio
async def test_update_workflow_template_async_from_dict():
    await test_update_workflow_template_async(request_type=dict)


def test_update_workflow_template_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.UpdateWorkflowTemplateRequest()

    request.template.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_workflow_template), "__call__"
    ) as call:
        call.return_value = workflow_templates.WorkflowTemplate()
        client.update_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "template.name=name_value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_workflow_template_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.UpdateWorkflowTemplateRequest()

    request.template.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_workflow_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate()
        )
        await client.update_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "template.name=name_value",
    ) in kw["metadata"]


def test_update_workflow_template_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.WorkflowTemplate()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_workflow_template(
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].template
        mock_val = workflow_templates.WorkflowTemplate(id="id_value")
        assert arg == mock_val


def test_update_workflow_template_flattened_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_workflow_template(
            workflow_templates.UpdateWorkflowTemplateRequest(),
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )


@pytest.mark.asyncio
async def test_update_workflow_template_flattened_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.WorkflowTemplate()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.WorkflowTemplate()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_workflow_template(
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].template
        mock_val = workflow_templates.WorkflowTemplate(id="id_value")
        assert arg == mock_val


@pytest.mark.asyncio
async def test_update_workflow_template_flattened_error_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_workflow_template(
            workflow_templates.UpdateWorkflowTemplateRequest(),
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.ListWorkflowTemplatesRequest,
        dict,
    ],
)
def test_list_workflow_templates(request_type, transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.ListWorkflowTemplatesResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_workflow_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.ListWorkflowTemplatesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkflowTemplatesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_workflow_templates_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_workflow_templates()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.ListWorkflowTemplatesRequest()


def test_list_workflow_templates_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = workflow_templates.ListWorkflowTemplatesRequest(
        parent="parent_value",
        page_token="page_token_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.list_workflow_templates(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.ListWorkflowTemplatesRequest(
            parent="parent_value",
            page_token="page_token_value",
        )


def test_list_workflow_templates_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_workflow_templates
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_workflow_templates
        ] = mock_rpc
        request = {}
        client.list_workflow_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_workflow_templates(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_list_workflow_templates_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.ListWorkflowTemplatesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_workflow_templates()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.ListWorkflowTemplatesRequest()


@pytest.mark.asyncio
async def test_list_workflow_templates_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.list_workflow_templates
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.list_workflow_templates
        ] = mock_object

        request = {}
        await client.list_workflow_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.list_workflow_templates(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_list_workflow_templates_async(
    transport: str = "grpc_asyncio",
    request_type=workflow_templates.ListWorkflowTemplatesRequest,
):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.ListWorkflowTemplatesResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_workflow_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.ListWorkflowTemplatesRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkflowTemplatesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_workflow_templates_async_from_dict():
    await test_list_workflow_templates_async(request_type=dict)


def test_list_workflow_templates_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.ListWorkflowTemplatesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        call.return_value = workflow_templates.ListWorkflowTemplatesResponse()
        client.list_workflow_templates(request)

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
async def test_list_workflow_templates_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.ListWorkflowTemplatesRequest()

    request.parent = "parent_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.ListWorkflowTemplatesResponse()
        )
        await client.list_workflow_templates(request)

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


def test_list_workflow_templates_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.ListWorkflowTemplatesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_workflow_templates(
            parent="parent_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_workflow_templates_flattened_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_workflow_templates(
            workflow_templates.ListWorkflowTemplatesRequest(),
            parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_workflow_templates_flattened_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = workflow_templates.ListWorkflowTemplatesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            workflow_templates.ListWorkflowTemplatesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_workflow_templates(
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
async def test_list_workflow_templates_flattened_error_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_workflow_templates(
            workflow_templates.ListWorkflowTemplatesRequest(),
            parent="parent_value",
        )


def test_list_workflow_templates_pager(transport_name: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="abc",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[],
                next_page_token="def",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="ghi",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
            ),
            RuntimeError,
        )

        expected_metadata = ()
        retry = retries.Retry()
        timeout = 5
        expected_metadata = tuple(expected_metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_workflow_templates(request={}, retry=retry, timeout=timeout)

        assert pager._metadata == expected_metadata
        assert pager._retry == retry
        assert pager._timeout == timeout

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, workflow_templates.WorkflowTemplate) for i in results)


def test_list_workflow_templates_pages(transport_name: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="abc",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[],
                next_page_token="def",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="ghi",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_workflow_templates(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_workflow_templates_async_pager():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="abc",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[],
                next_page_token="def",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="ghi",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_workflow_templates(
            request={},
        )
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:  # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, workflow_templates.WorkflowTemplate) for i in responses
        )


@pytest.mark.asyncio
async def test_list_workflow_templates_async_pages():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_workflow_templates),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="abc",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[],
                next_page_token="def",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="ghi",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        # Workaround issue in python 3.9 related to code coverage by adding `# pragma: no branch`
        # See https://github.com/googleapis/gapic-generator-python/pull/1174#issuecomment-1025132372
        async for page_ in (  # pragma: no branch
            await client.list_workflow_templates(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.DeleteWorkflowTemplateRequest,
        dict,
    ],
)
def test_delete_workflow_template(request_type, transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.DeleteWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_workflow_template_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.DeleteWorkflowTemplateRequest()


def test_delete_workflow_template_non_empty_request_with_auto_populated_field():
    # This test is a coverage failsafe to make sure that UUID4 fields are
    # automatically populated, according to AIP-4235, with non-empty requests.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc",
    )

    # Populate all string fields in the request which are not UUID4
    # since we want to check that UUID4 are populated automatically
    # if they meet the requirements of AIP 4235.
    request = workflow_templates.DeleteWorkflowTemplateRequest(
        name="name_value",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_template), "__call__"
    ) as call:
        call.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client.delete_workflow_template(request=request)
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.DeleteWorkflowTemplateRequest(
            name="name_value",
        )


def test_delete_workflow_template_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="grpc",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_workflow_template
        ] = mock_rpc
        request = {}
        client.delete_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


@pytest.mark.asyncio
async def test_delete_workflow_template_empty_call_async():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_workflow_template()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == workflow_templates.DeleteWorkflowTemplateRequest()


@pytest.mark.asyncio
async def test_delete_workflow_template_async_use_cached_wrapped_rpc(
    transport: str = "grpc_asyncio",
):
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method_async.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceAsyncClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._client._transport.delete_workflow_template
            in client._client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_object = mock.AsyncMock()
        client._client._transport._wrapped_methods[
            client._client._transport.delete_workflow_template
        ] = mock_object

        request = {}
        await client.delete_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_object.call_count == 1

        await client.delete_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_object.call_count == 2


@pytest.mark.asyncio
async def test_delete_workflow_template_async(
    transport: str = "grpc_asyncio",
    request_type=workflow_templates.DeleteWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        request = workflow_templates.DeleteWorkflowTemplateRequest()
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_workflow_template_async_from_dict():
    await test_delete_workflow_template_async(request_type=dict)


def test_delete_workflow_template_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.DeleteWorkflowTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_template), "__call__"
    ) as call:
        call.return_value = None
        client.delete_workflow_template(request)

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
async def test_delete_workflow_template_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = workflow_templates.DeleteWorkflowTemplateRequest()

    request.name = "name_value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_template), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_workflow_template(request)

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


def test_delete_workflow_template_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_workflow_template(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_workflow_template_flattened_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_workflow_template(
            workflow_templates.DeleteWorkflowTemplateRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_workflow_template_flattened_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_workflow_template), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_workflow_template(
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
async def test_delete_workflow_template_flattened_error_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_workflow_template(
            workflow_templates.DeleteWorkflowTemplateRequest(),
            name="name_value",
        )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.CreateWorkflowTemplateRequest,
        dict,
    ],
)
def test_create_workflow_template_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["template"] = {
        "id": "id_value",
        "name": "name_value",
        "version": 774,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "placement": {
            "managed_cluster": {
                "cluster_name": "cluster_name_value",
                "config": {
                    "config_bucket": "config_bucket_value",
                    "temp_bucket": "temp_bucket_value",
                    "gce_cluster_config": {
                        "zone_uri": "zone_uri_value",
                        "network_uri": "network_uri_value",
                        "subnetwork_uri": "subnetwork_uri_value",
                        "internal_ip_only": True,
                        "private_ipv6_google_access": 1,
                        "service_account": "service_account_value",
                        "service_account_scopes": [
                            "service_account_scopes_value1",
                            "service_account_scopes_value2",
                        ],
                        "tags": ["tags_value1", "tags_value2"],
                        "metadata": {},
                        "reservation_affinity": {
                            "consume_reservation_type": 1,
                            "key": "key_value",
                            "values": ["values_value1", "values_value2"],
                        },
                        "node_group_affinity": {
                            "node_group_uri": "node_group_uri_value"
                        },
                        "shielded_instance_config": {
                            "enable_secure_boot": True,
                            "enable_vtpm": True,
                            "enable_integrity_monitoring": True,
                        },
                        "confidential_instance_config": {
                            "enable_confidential_compute": True
                        },
                    },
                    "master_config": {
                        "num_instances": 1399,
                        "instance_names": [
                            "instance_names_value1",
                            "instance_names_value2",
                        ],
                        "instance_references": [
                            {
                                "instance_name": "instance_name_value",
                                "instance_id": "instance_id_value",
                                "public_key": "public_key_value",
                                "public_ecies_key": "public_ecies_key_value",
                            }
                        ],
                        "image_uri": "image_uri_value",
                        "machine_type_uri": "machine_type_uri_value",
                        "disk_config": {
                            "boot_disk_type": "boot_disk_type_value",
                            "boot_disk_size_gb": 1792,
                            "num_local_ssds": 1494,
                            "local_ssd_interface": "local_ssd_interface_value",
                        },
                        "is_preemptible": True,
                        "preemptibility": 1,
                        "managed_group_config": {
                            "instance_template_name": "instance_template_name_value",
                            "instance_group_manager_name": "instance_group_manager_name_value",
                            "instance_group_manager_uri": "instance_group_manager_uri_value",
                        },
                        "accelerators": [
                            {
                                "accelerator_type_uri": "accelerator_type_uri_value",
                                "accelerator_count": 1805,
                            }
                        ],
                        "min_cpu_platform": "min_cpu_platform_value",
                        "min_num_instances": 1818,
                        "instance_flexibility_policy": {
                            "instance_selection_list": [
                                {
                                    "machine_types": [
                                        "machine_types_value1",
                                        "machine_types_value2",
                                    ],
                                    "rank": 428,
                                }
                            ],
                            "instance_selection_results": [
                                {"machine_type": "machine_type_value", "vm_count": 875}
                            ],
                        },
                        "startup_config": {"required_registration_fraction": 0.3216},
                    },
                    "worker_config": {},
                    "secondary_worker_config": {},
                    "software_config": {
                        "image_version": "image_version_value",
                        "properties": {},
                        "optional_components": [5],
                    },
                    "initialization_actions": [
                        {
                            "executable_file": "executable_file_value",
                            "execution_timeout": {"seconds": 751, "nanos": 543},
                        }
                    ],
                    "encryption_config": {
                        "gce_pd_kms_key_name": "gce_pd_kms_key_name_value"
                    },
                    "autoscaling_config": {"policy_uri": "policy_uri_value"},
                    "security_config": {
                        "kerberos_config": {
                            "enable_kerberos": True,
                            "root_principal_password_uri": "root_principal_password_uri_value",
                            "kms_key_uri": "kms_key_uri_value",
                            "keystore_uri": "keystore_uri_value",
                            "truststore_uri": "truststore_uri_value",
                            "keystore_password_uri": "keystore_password_uri_value",
                            "key_password_uri": "key_password_uri_value",
                            "truststore_password_uri": "truststore_password_uri_value",
                            "cross_realm_trust_realm": "cross_realm_trust_realm_value",
                            "cross_realm_trust_kdc": "cross_realm_trust_kdc_value",
                            "cross_realm_trust_admin_server": "cross_realm_trust_admin_server_value",
                            "cross_realm_trust_shared_password_uri": "cross_realm_trust_shared_password_uri_value",
                            "kdc_db_key_uri": "kdc_db_key_uri_value",
                            "tgt_lifetime_hours": 1933,
                            "realm": "realm_value",
                        },
                        "identity_config": {"user_service_account_mapping": {}},
                    },
                    "lifecycle_config": {
                        "idle_delete_ttl": {},
                        "auto_delete_time": {},
                        "auto_delete_ttl": {},
                        "idle_start_time": {},
                    },
                    "endpoint_config": {
                        "http_ports": {},
                        "enable_http_port_access": True,
                    },
                    "metastore_config": {
                        "dataproc_metastore_service": "dataproc_metastore_service_value"
                    },
                    "dataproc_metric_config": {
                        "metrics": [
                            {
                                "metric_source": 1,
                                "metric_overrides": [
                                    "metric_overrides_value1",
                                    "metric_overrides_value2",
                                ],
                            }
                        ]
                    },
                    "auxiliary_node_groups": [
                        {
                            "node_group": {
                                "name": "name_value",
                                "roles": [1],
                                "node_group_config": {},
                                "labels": {},
                            },
                            "node_group_id": "node_group_id_value",
                        }
                    ],
                },
                "labels": {},
            },
            "cluster_selector": {"zone": "zone_value", "cluster_labels": {}},
        },
        "jobs": [
            {
                "step_id": "step_id_value",
                "hadoop_job": {
                    "main_jar_file_uri": "main_jar_file_uri_value",
                    "main_class": "main_class_value",
                    "args": ["args_value1", "args_value2"],
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {"driver_log_levels": {}},
                },
                "spark_job": {
                    "main_jar_file_uri": "main_jar_file_uri_value",
                    "main_class": "main_class_value",
                    "args": ["args_value1", "args_value2"],
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "pyspark_job": {
                    "main_python_file_uri": "main_python_file_uri_value",
                    "args": ["args_value1", "args_value2"],
                    "python_file_uris": [
                        "python_file_uris_value1",
                        "python_file_uris_value2",
                    ],
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "hive_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {"queries": ["queries_value1", "queries_value2"]},
                    "continue_on_failure": True,
                    "script_variables": {},
                    "properties": {},
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                },
                "pig_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {},
                    "continue_on_failure": True,
                    "script_variables": {},
                    "properties": {},
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "logging_config": {},
                },
                "spark_r_job": {
                    "main_r_file_uri": "main_r_file_uri_value",
                    "args": ["args_value1", "args_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "spark_sql_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {},
                    "script_variables": {},
                    "properties": {},
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "logging_config": {},
                },
                "presto_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {},
                    "continue_on_failure": True,
                    "output_format": "output_format_value",
                    "client_tags": ["client_tags_value1", "client_tags_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "labels": {},
                "scheduling": {
                    "max_failures_per_hour": 2243,
                    "max_failures_total": 1923,
                },
                "prerequisite_step_ids": [
                    "prerequisite_step_ids_value1",
                    "prerequisite_step_ids_value2",
                ],
            }
        ],
        "parameters": [
            {
                "name": "name_value",
                "fields": ["fields_value1", "fields_value2"],
                "description": "description_value",
                "validation": {
                    "regex": {"regexes": ["regexes_value1", "regexes_value2"]},
                    "values": {"values": ["values_value1", "values_value2"]},
                },
            }
        ],
        "dag_timeout": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = workflow_templates.CreateWorkflowTemplateRequest.meta.fields[
        "template"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["template"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["template"][field])):
                    del request_init["template"][field][i][subfield]
            else:
                del request_init["template"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = workflow_templates.WorkflowTemplate(
            id="id_value",
            name="name_value",
            version=774,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = workflow_templates.WorkflowTemplate.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.create_workflow_template(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflow_templates.WorkflowTemplate)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.version == 774


def test_create_workflow_template_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.create_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.create_workflow_template
        ] = mock_rpc

        request = {}
        client.create_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.create_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_create_workflow_template_rest_required_fields(
    request_type=workflow_templates.CreateWorkflowTemplateRequest,
):
    transport_class = transports.WorkflowTemplateServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_workflow_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).create_workflow_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = workflow_templates.WorkflowTemplate()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = workflow_templates.WorkflowTemplate.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.create_workflow_template(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_create_workflow_template_rest_unset_required_fields():
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.create_workflow_template._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(())
        & set(
            (
                "parent",
                "template",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_workflow_template_rest_interceptors(null_interceptor):
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WorkflowTemplateServiceRestInterceptor(),
    )
    client = WorkflowTemplateServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "post_create_workflow_template",
    ) as post, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "pre_create_workflow_template",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = workflow_templates.CreateWorkflowTemplateRequest.pb(
            workflow_templates.CreateWorkflowTemplateRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = workflow_templates.WorkflowTemplate.to_json(
            workflow_templates.WorkflowTemplate()
        )

        request = workflow_templates.CreateWorkflowTemplateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = workflow_templates.WorkflowTemplate()

        client.create_workflow_template(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_create_workflow_template_rest_bad_request(
    transport: str = "rest",
    request_type=workflow_templates.CreateWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_workflow_template(request)


def test_create_workflow_template_rest_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = workflow_templates.WorkflowTemplate()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = workflow_templates.WorkflowTemplate.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.create_workflow_template(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/workflowTemplates"
            % client.transport._host,
            args[1],
        )


def test_create_workflow_template_rest_flattened_error(transport: str = "rest"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_workflow_template(
            workflow_templates.CreateWorkflowTemplateRequest(),
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )


def test_create_workflow_template_rest_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.GetWorkflowTemplateRequest,
        dict,
    ],
)
def test_get_workflow_template_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = workflow_templates.WorkflowTemplate(
            id="id_value",
            name="name_value",
            version=774,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = workflow_templates.WorkflowTemplate.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_workflow_template(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflow_templates.WorkflowTemplate)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.version == 774


def test_get_workflow_template_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.get_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.get_workflow_template
        ] = mock_rpc

        request = {}
        client.get_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.get_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_get_workflow_template_rest_required_fields(
    request_type=workflow_templates.GetWorkflowTemplateRequest,
):
    transport_class = transports.WorkflowTemplateServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_workflow_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).get_workflow_template._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("version",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = workflow_templates.WorkflowTemplate()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = workflow_templates.WorkflowTemplate.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.get_workflow_template(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_get_workflow_template_rest_unset_required_fields():
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.get_workflow_template._get_unset_required_fields({})
    assert set(unset_fields) == (set(("version",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_workflow_template_rest_interceptors(null_interceptor):
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WorkflowTemplateServiceRestInterceptor(),
    )
    client = WorkflowTemplateServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor, "post_get_workflow_template"
    ) as post, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor, "pre_get_workflow_template"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = workflow_templates.GetWorkflowTemplateRequest.pb(
            workflow_templates.GetWorkflowTemplateRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = workflow_templates.WorkflowTemplate.to_json(
            workflow_templates.WorkflowTemplate()
        )

        request = workflow_templates.GetWorkflowTemplateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = workflow_templates.WorkflowTemplate()

        client.get_workflow_template(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_get_workflow_template_rest_bad_request(
    transport: str = "rest", request_type=workflow_templates.GetWorkflowTemplateRequest
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_workflow_template(request)


def test_get_workflow_template_rest_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = workflow_templates.WorkflowTemplate()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = workflow_templates.WorkflowTemplate.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.get_workflow_template(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/workflowTemplates/*}"
            % client.transport._host,
            args[1],
        )


def test_get_workflow_template_rest_flattened_error(transport: str = "rest"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_workflow_template(
            workflow_templates.GetWorkflowTemplateRequest(),
            name="name_value",
        )


def test_get_workflow_template_rest_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.InstantiateWorkflowTemplateRequest,
        dict,
    ],
)
def test_instantiate_workflow_template_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.instantiate_workflow_template(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_instantiate_workflow_template_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.instantiate_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.instantiate_workflow_template
        ] = mock_rpc

        request = {}
        client.instantiate_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.instantiate_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_instantiate_workflow_template_rest_required_fields(
    request_type=workflow_templates.InstantiateWorkflowTemplateRequest,
):
    transport_class = transports.WorkflowTemplateServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).instantiate_workflow_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).instantiate_workflow_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.instantiate_workflow_template(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_instantiate_workflow_template_rest_unset_required_fields():
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.instantiate_workflow_template._get_unset_required_fields(
        {}
    )
    assert set(unset_fields) == (set(()) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_instantiate_workflow_template_rest_interceptors(null_interceptor):
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WorkflowTemplateServiceRestInterceptor(),
    )
    client = WorkflowTemplateServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "post_instantiate_workflow_template",
    ) as post, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "pre_instantiate_workflow_template",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = workflow_templates.InstantiateWorkflowTemplateRequest.pb(
            workflow_templates.InstantiateWorkflowTemplateRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = workflow_templates.InstantiateWorkflowTemplateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.instantiate_workflow_template(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_instantiate_workflow_template_rest_bad_request(
    transport: str = "rest",
    request_type=workflow_templates.InstantiateWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.instantiate_workflow_template(request)


def test_instantiate_workflow_template_rest_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
            parameters={"key_value": "value_value"},
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.instantiate_workflow_template(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/workflowTemplates/*}:instantiate"
            % client.transport._host,
            args[1],
        )


def test_instantiate_workflow_template_rest_flattened_error(transport: str = "rest"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.instantiate_workflow_template(
            workflow_templates.InstantiateWorkflowTemplateRequest(),
            name="name_value",
            parameters={"key_value": "value_value"},
        )


def test_instantiate_workflow_template_rest_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.InstantiateInlineWorkflowTemplateRequest,
        dict,
    ],
)
def test_instantiate_inline_workflow_template_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request_init["template"] = {
        "id": "id_value",
        "name": "name_value",
        "version": 774,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "placement": {
            "managed_cluster": {
                "cluster_name": "cluster_name_value",
                "config": {
                    "config_bucket": "config_bucket_value",
                    "temp_bucket": "temp_bucket_value",
                    "gce_cluster_config": {
                        "zone_uri": "zone_uri_value",
                        "network_uri": "network_uri_value",
                        "subnetwork_uri": "subnetwork_uri_value",
                        "internal_ip_only": True,
                        "private_ipv6_google_access": 1,
                        "service_account": "service_account_value",
                        "service_account_scopes": [
                            "service_account_scopes_value1",
                            "service_account_scopes_value2",
                        ],
                        "tags": ["tags_value1", "tags_value2"],
                        "metadata": {},
                        "reservation_affinity": {
                            "consume_reservation_type": 1,
                            "key": "key_value",
                            "values": ["values_value1", "values_value2"],
                        },
                        "node_group_affinity": {
                            "node_group_uri": "node_group_uri_value"
                        },
                        "shielded_instance_config": {
                            "enable_secure_boot": True,
                            "enable_vtpm": True,
                            "enable_integrity_monitoring": True,
                        },
                        "confidential_instance_config": {
                            "enable_confidential_compute": True
                        },
                    },
                    "master_config": {
                        "num_instances": 1399,
                        "instance_names": [
                            "instance_names_value1",
                            "instance_names_value2",
                        ],
                        "instance_references": [
                            {
                                "instance_name": "instance_name_value",
                                "instance_id": "instance_id_value",
                                "public_key": "public_key_value",
                                "public_ecies_key": "public_ecies_key_value",
                            }
                        ],
                        "image_uri": "image_uri_value",
                        "machine_type_uri": "machine_type_uri_value",
                        "disk_config": {
                            "boot_disk_type": "boot_disk_type_value",
                            "boot_disk_size_gb": 1792,
                            "num_local_ssds": 1494,
                            "local_ssd_interface": "local_ssd_interface_value",
                        },
                        "is_preemptible": True,
                        "preemptibility": 1,
                        "managed_group_config": {
                            "instance_template_name": "instance_template_name_value",
                            "instance_group_manager_name": "instance_group_manager_name_value",
                            "instance_group_manager_uri": "instance_group_manager_uri_value",
                        },
                        "accelerators": [
                            {
                                "accelerator_type_uri": "accelerator_type_uri_value",
                                "accelerator_count": 1805,
                            }
                        ],
                        "min_cpu_platform": "min_cpu_platform_value",
                        "min_num_instances": 1818,
                        "instance_flexibility_policy": {
                            "instance_selection_list": [
                                {
                                    "machine_types": [
                                        "machine_types_value1",
                                        "machine_types_value2",
                                    ],
                                    "rank": 428,
                                }
                            ],
                            "instance_selection_results": [
                                {"machine_type": "machine_type_value", "vm_count": 875}
                            ],
                        },
                        "startup_config": {"required_registration_fraction": 0.3216},
                    },
                    "worker_config": {},
                    "secondary_worker_config": {},
                    "software_config": {
                        "image_version": "image_version_value",
                        "properties": {},
                        "optional_components": [5],
                    },
                    "initialization_actions": [
                        {
                            "executable_file": "executable_file_value",
                            "execution_timeout": {"seconds": 751, "nanos": 543},
                        }
                    ],
                    "encryption_config": {
                        "gce_pd_kms_key_name": "gce_pd_kms_key_name_value"
                    },
                    "autoscaling_config": {"policy_uri": "policy_uri_value"},
                    "security_config": {
                        "kerberos_config": {
                            "enable_kerberos": True,
                            "root_principal_password_uri": "root_principal_password_uri_value",
                            "kms_key_uri": "kms_key_uri_value",
                            "keystore_uri": "keystore_uri_value",
                            "truststore_uri": "truststore_uri_value",
                            "keystore_password_uri": "keystore_password_uri_value",
                            "key_password_uri": "key_password_uri_value",
                            "truststore_password_uri": "truststore_password_uri_value",
                            "cross_realm_trust_realm": "cross_realm_trust_realm_value",
                            "cross_realm_trust_kdc": "cross_realm_trust_kdc_value",
                            "cross_realm_trust_admin_server": "cross_realm_trust_admin_server_value",
                            "cross_realm_trust_shared_password_uri": "cross_realm_trust_shared_password_uri_value",
                            "kdc_db_key_uri": "kdc_db_key_uri_value",
                            "tgt_lifetime_hours": 1933,
                            "realm": "realm_value",
                        },
                        "identity_config": {"user_service_account_mapping": {}},
                    },
                    "lifecycle_config": {
                        "idle_delete_ttl": {},
                        "auto_delete_time": {},
                        "auto_delete_ttl": {},
                        "idle_start_time": {},
                    },
                    "endpoint_config": {
                        "http_ports": {},
                        "enable_http_port_access": True,
                    },
                    "metastore_config": {
                        "dataproc_metastore_service": "dataproc_metastore_service_value"
                    },
                    "dataproc_metric_config": {
                        "metrics": [
                            {
                                "metric_source": 1,
                                "metric_overrides": [
                                    "metric_overrides_value1",
                                    "metric_overrides_value2",
                                ],
                            }
                        ]
                    },
                    "auxiliary_node_groups": [
                        {
                            "node_group": {
                                "name": "name_value",
                                "roles": [1],
                                "node_group_config": {},
                                "labels": {},
                            },
                            "node_group_id": "node_group_id_value",
                        }
                    ],
                },
                "labels": {},
            },
            "cluster_selector": {"zone": "zone_value", "cluster_labels": {}},
        },
        "jobs": [
            {
                "step_id": "step_id_value",
                "hadoop_job": {
                    "main_jar_file_uri": "main_jar_file_uri_value",
                    "main_class": "main_class_value",
                    "args": ["args_value1", "args_value2"],
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {"driver_log_levels": {}},
                },
                "spark_job": {
                    "main_jar_file_uri": "main_jar_file_uri_value",
                    "main_class": "main_class_value",
                    "args": ["args_value1", "args_value2"],
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "pyspark_job": {
                    "main_python_file_uri": "main_python_file_uri_value",
                    "args": ["args_value1", "args_value2"],
                    "python_file_uris": [
                        "python_file_uris_value1",
                        "python_file_uris_value2",
                    ],
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "hive_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {"queries": ["queries_value1", "queries_value2"]},
                    "continue_on_failure": True,
                    "script_variables": {},
                    "properties": {},
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                },
                "pig_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {},
                    "continue_on_failure": True,
                    "script_variables": {},
                    "properties": {},
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "logging_config": {},
                },
                "spark_r_job": {
                    "main_r_file_uri": "main_r_file_uri_value",
                    "args": ["args_value1", "args_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "spark_sql_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {},
                    "script_variables": {},
                    "properties": {},
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "logging_config": {},
                },
                "presto_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {},
                    "continue_on_failure": True,
                    "output_format": "output_format_value",
                    "client_tags": ["client_tags_value1", "client_tags_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "labels": {},
                "scheduling": {
                    "max_failures_per_hour": 2243,
                    "max_failures_total": 1923,
                },
                "prerequisite_step_ids": [
                    "prerequisite_step_ids_value1",
                    "prerequisite_step_ids_value2",
                ],
            }
        ],
        "parameters": [
            {
                "name": "name_value",
                "fields": ["fields_value1", "fields_value2"],
                "description": "description_value",
                "validation": {
                    "regex": {"regexes": ["regexes_value1", "regexes_value2"]},
                    "values": {"values": ["values_value1", "values_value2"]},
                },
            }
        ],
        "dag_timeout": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = (
        workflow_templates.InstantiateInlineWorkflowTemplateRequest.meta.fields[
            "template"
        ]
    )

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["template"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["template"][field])):
                    del request_init["template"][field][i][subfield]
            else:
                del request_init["template"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.instantiate_inline_workflow_template(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_instantiate_inline_workflow_template_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.instantiate_inline_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.instantiate_inline_workflow_template
        ] = mock_rpc

        request = {}
        client.instantiate_inline_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        # Operation methods build a cached wrapper on first rpc call
        # subsequent calls should use the cached wrapper
        wrapper_fn.reset_mock()

        client.instantiate_inline_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_instantiate_inline_workflow_template_rest_required_fields(
    request_type=workflow_templates.InstantiateInlineWorkflowTemplateRequest,
):
    transport_class = transports.WorkflowTemplateServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).instantiate_inline_workflow_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).instantiate_inline_workflow_template._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("request_id",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name="operations/spam")
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "post",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.instantiate_inline_workflow_template(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_instantiate_inline_workflow_template_rest_unset_required_fields():
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = (
        transport.instantiate_inline_workflow_template._get_unset_required_fields({})
    )
    assert set(unset_fields) == (
        set(("requestId",))
        & set(
            (
                "parent",
                "template",
            )
        )
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_instantiate_inline_workflow_template_rest_interceptors(null_interceptor):
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WorkflowTemplateServiceRestInterceptor(),
    )
    client = WorkflowTemplateServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        operation.Operation, "_set_result_from_operation"
    ), mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "post_instantiate_inline_workflow_template",
    ) as post, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "pre_instantiate_inline_workflow_template",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = workflow_templates.InstantiateInlineWorkflowTemplateRequest.pb(
            workflow_templates.InstantiateInlineWorkflowTemplateRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(
            operations_pb2.Operation()
        )

        request = workflow_templates.InstantiateInlineWorkflowTemplateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.instantiate_inline_workflow_template(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_instantiate_inline_workflow_template_rest_bad_request(
    transport: str = "rest",
    request_type=workflow_templates.InstantiateInlineWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.instantiate_inline_workflow_template(request)


def test_instantiate_inline_workflow_template_rest_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name="operations/spam")

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.instantiate_inline_workflow_template(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/workflowTemplates:instantiateInline"
            % client.transport._host,
            args[1],
        )


def test_instantiate_inline_workflow_template_rest_flattened_error(
    transport: str = "rest",
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.instantiate_inline_workflow_template(
            workflow_templates.InstantiateInlineWorkflowTemplateRequest(),
            parent="parent_value",
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )


def test_instantiate_inline_workflow_template_rest_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.UpdateWorkflowTemplateRequest,
        dict,
    ],
)
def test_update_workflow_template_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "template": {
            "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
        }
    }
    request_init["template"] = {
        "id": "id_value",
        "name": "projects/sample1/locations/sample2/workflowTemplates/sample3",
        "version": 774,
        "create_time": {"seconds": 751, "nanos": 543},
        "update_time": {},
        "labels": {},
        "placement": {
            "managed_cluster": {
                "cluster_name": "cluster_name_value",
                "config": {
                    "config_bucket": "config_bucket_value",
                    "temp_bucket": "temp_bucket_value",
                    "gce_cluster_config": {
                        "zone_uri": "zone_uri_value",
                        "network_uri": "network_uri_value",
                        "subnetwork_uri": "subnetwork_uri_value",
                        "internal_ip_only": True,
                        "private_ipv6_google_access": 1,
                        "service_account": "service_account_value",
                        "service_account_scopes": [
                            "service_account_scopes_value1",
                            "service_account_scopes_value2",
                        ],
                        "tags": ["tags_value1", "tags_value2"],
                        "metadata": {},
                        "reservation_affinity": {
                            "consume_reservation_type": 1,
                            "key": "key_value",
                            "values": ["values_value1", "values_value2"],
                        },
                        "node_group_affinity": {
                            "node_group_uri": "node_group_uri_value"
                        },
                        "shielded_instance_config": {
                            "enable_secure_boot": True,
                            "enable_vtpm": True,
                            "enable_integrity_monitoring": True,
                        },
                        "confidential_instance_config": {
                            "enable_confidential_compute": True
                        },
                    },
                    "master_config": {
                        "num_instances": 1399,
                        "instance_names": [
                            "instance_names_value1",
                            "instance_names_value2",
                        ],
                        "instance_references": [
                            {
                                "instance_name": "instance_name_value",
                                "instance_id": "instance_id_value",
                                "public_key": "public_key_value",
                                "public_ecies_key": "public_ecies_key_value",
                            }
                        ],
                        "image_uri": "image_uri_value",
                        "machine_type_uri": "machine_type_uri_value",
                        "disk_config": {
                            "boot_disk_type": "boot_disk_type_value",
                            "boot_disk_size_gb": 1792,
                            "num_local_ssds": 1494,
                            "local_ssd_interface": "local_ssd_interface_value",
                        },
                        "is_preemptible": True,
                        "preemptibility": 1,
                        "managed_group_config": {
                            "instance_template_name": "instance_template_name_value",
                            "instance_group_manager_name": "instance_group_manager_name_value",
                            "instance_group_manager_uri": "instance_group_manager_uri_value",
                        },
                        "accelerators": [
                            {
                                "accelerator_type_uri": "accelerator_type_uri_value",
                                "accelerator_count": 1805,
                            }
                        ],
                        "min_cpu_platform": "min_cpu_platform_value",
                        "min_num_instances": 1818,
                        "instance_flexibility_policy": {
                            "instance_selection_list": [
                                {
                                    "machine_types": [
                                        "machine_types_value1",
                                        "machine_types_value2",
                                    ],
                                    "rank": 428,
                                }
                            ],
                            "instance_selection_results": [
                                {"machine_type": "machine_type_value", "vm_count": 875}
                            ],
                        },
                        "startup_config": {"required_registration_fraction": 0.3216},
                    },
                    "worker_config": {},
                    "secondary_worker_config": {},
                    "software_config": {
                        "image_version": "image_version_value",
                        "properties": {},
                        "optional_components": [5],
                    },
                    "initialization_actions": [
                        {
                            "executable_file": "executable_file_value",
                            "execution_timeout": {"seconds": 751, "nanos": 543},
                        }
                    ],
                    "encryption_config": {
                        "gce_pd_kms_key_name": "gce_pd_kms_key_name_value"
                    },
                    "autoscaling_config": {"policy_uri": "policy_uri_value"},
                    "security_config": {
                        "kerberos_config": {
                            "enable_kerberos": True,
                            "root_principal_password_uri": "root_principal_password_uri_value",
                            "kms_key_uri": "kms_key_uri_value",
                            "keystore_uri": "keystore_uri_value",
                            "truststore_uri": "truststore_uri_value",
                            "keystore_password_uri": "keystore_password_uri_value",
                            "key_password_uri": "key_password_uri_value",
                            "truststore_password_uri": "truststore_password_uri_value",
                            "cross_realm_trust_realm": "cross_realm_trust_realm_value",
                            "cross_realm_trust_kdc": "cross_realm_trust_kdc_value",
                            "cross_realm_trust_admin_server": "cross_realm_trust_admin_server_value",
                            "cross_realm_trust_shared_password_uri": "cross_realm_trust_shared_password_uri_value",
                            "kdc_db_key_uri": "kdc_db_key_uri_value",
                            "tgt_lifetime_hours": 1933,
                            "realm": "realm_value",
                        },
                        "identity_config": {"user_service_account_mapping": {}},
                    },
                    "lifecycle_config": {
                        "idle_delete_ttl": {},
                        "auto_delete_time": {},
                        "auto_delete_ttl": {},
                        "idle_start_time": {},
                    },
                    "endpoint_config": {
                        "http_ports": {},
                        "enable_http_port_access": True,
                    },
                    "metastore_config": {
                        "dataproc_metastore_service": "dataproc_metastore_service_value"
                    },
                    "dataproc_metric_config": {
                        "metrics": [
                            {
                                "metric_source": 1,
                                "metric_overrides": [
                                    "metric_overrides_value1",
                                    "metric_overrides_value2",
                                ],
                            }
                        ]
                    },
                    "auxiliary_node_groups": [
                        {
                            "node_group": {
                                "name": "name_value",
                                "roles": [1],
                                "node_group_config": {},
                                "labels": {},
                            },
                            "node_group_id": "node_group_id_value",
                        }
                    ],
                },
                "labels": {},
            },
            "cluster_selector": {"zone": "zone_value", "cluster_labels": {}},
        },
        "jobs": [
            {
                "step_id": "step_id_value",
                "hadoop_job": {
                    "main_jar_file_uri": "main_jar_file_uri_value",
                    "main_class": "main_class_value",
                    "args": ["args_value1", "args_value2"],
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {"driver_log_levels": {}},
                },
                "spark_job": {
                    "main_jar_file_uri": "main_jar_file_uri_value",
                    "main_class": "main_class_value",
                    "args": ["args_value1", "args_value2"],
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "pyspark_job": {
                    "main_python_file_uri": "main_python_file_uri_value",
                    "args": ["args_value1", "args_value2"],
                    "python_file_uris": [
                        "python_file_uris_value1",
                        "python_file_uris_value2",
                    ],
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "hive_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {"queries": ["queries_value1", "queries_value2"]},
                    "continue_on_failure": True,
                    "script_variables": {},
                    "properties": {},
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                },
                "pig_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {},
                    "continue_on_failure": True,
                    "script_variables": {},
                    "properties": {},
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "logging_config": {},
                },
                "spark_r_job": {
                    "main_r_file_uri": "main_r_file_uri_value",
                    "args": ["args_value1", "args_value2"],
                    "file_uris": ["file_uris_value1", "file_uris_value2"],
                    "archive_uris": ["archive_uris_value1", "archive_uris_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "spark_sql_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {},
                    "script_variables": {},
                    "properties": {},
                    "jar_file_uris": ["jar_file_uris_value1", "jar_file_uris_value2"],
                    "logging_config": {},
                },
                "presto_job": {
                    "query_file_uri": "query_file_uri_value",
                    "query_list": {},
                    "continue_on_failure": True,
                    "output_format": "output_format_value",
                    "client_tags": ["client_tags_value1", "client_tags_value2"],
                    "properties": {},
                    "logging_config": {},
                },
                "labels": {},
                "scheduling": {
                    "max_failures_per_hour": 2243,
                    "max_failures_total": 1923,
                },
                "prerequisite_step_ids": [
                    "prerequisite_step_ids_value1",
                    "prerequisite_step_ids_value2",
                ],
            }
        ],
        "parameters": [
            {
                "name": "name_value",
                "fields": ["fields_value1", "fields_value2"],
                "description": "description_value",
                "validation": {
                    "regex": {"regexes": ["regexes_value1", "regexes_value2"]},
                    "values": {"values": ["values_value1", "values_value2"]},
                },
            }
        ],
        "dag_timeout": {},
    }
    # The version of a generated dependency at test runtime may differ from the version used during generation.
    # Delete any fields which are not present in the current runtime dependency
    # See https://github.com/googleapis/gapic-generator-python/issues/1748

    # Determine if the message type is proto-plus or protobuf
    test_field = workflow_templates.UpdateWorkflowTemplateRequest.meta.fields[
        "template"
    ]

    def get_message_fields(field):
        # Given a field which is a message (composite type), return a list with
        # all the fields of the message.
        # If the field is not a composite type, return an empty list.
        message_fields = []

        if hasattr(field, "message") and field.message:
            is_field_type_proto_plus_type = not hasattr(field.message, "DESCRIPTOR")

            if is_field_type_proto_plus_type:
                message_fields = field.message.meta.fields.values()
            # Add `# pragma: NO COVER` because there may not be any `*_pb2` field types
            else:  # pragma: NO COVER
                message_fields = field.message.DESCRIPTOR.fields
        return message_fields

    runtime_nested_fields = [
        (field.name, nested_field.name)
        for field in get_message_fields(test_field)
        for nested_field in get_message_fields(field)
    ]

    subfields_not_in_runtime = []

    # For each item in the sample request, create a list of sub fields which are not present at runtime
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for field, value in request_init["template"].items():  # pragma: NO COVER
        result = None
        is_repeated = False
        # For repeated fields
        if isinstance(value, list) and len(value):
            is_repeated = True
            result = value[0]
        # For fields where the type is another message
        if isinstance(value, dict):
            result = value

        if result and hasattr(result, "keys"):
            for subfield in result.keys():
                if (field, subfield) not in runtime_nested_fields:
                    subfields_not_in_runtime.append(
                        {
                            "field": field,
                            "subfield": subfield,
                            "is_repeated": is_repeated,
                        }
                    )

    # Remove fields from the sample request which are not present in the runtime version of the dependency
    # Add `# pragma: NO COVER` because this test code will not run if all subfields are present at runtime
    for subfield_to_delete in subfields_not_in_runtime:  # pragma: NO COVER
        field = subfield_to_delete.get("field")
        field_repeated = subfield_to_delete.get("is_repeated")
        subfield = subfield_to_delete.get("subfield")
        if subfield:
            if field_repeated:
                for i in range(0, len(request_init["template"][field])):
                    del request_init["template"][field][i][subfield]
            else:
                del request_init["template"][field][subfield]
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = workflow_templates.WorkflowTemplate(
            id="id_value",
            name="name_value",
            version=774,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = workflow_templates.WorkflowTemplate.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_workflow_template(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, workflow_templates.WorkflowTemplate)
    assert response.id == "id_value"
    assert response.name == "name_value"
    assert response.version == 774


def test_update_workflow_template_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.update_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.update_workflow_template
        ] = mock_rpc

        request = {}
        client.update_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.update_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_update_workflow_template_rest_required_fields(
    request_type=workflow_templates.UpdateWorkflowTemplateRequest,
):
    transport_class = transports.WorkflowTemplateServiceRestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_workflow_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).update_workflow_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = workflow_templates.WorkflowTemplate()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "put",
                "query_params": pb_request,
            }
            transcode_result["body"] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = workflow_templates.WorkflowTemplate.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.update_workflow_template(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_update_workflow_template_rest_unset_required_fields():
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.update_workflow_template._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("template",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_workflow_template_rest_interceptors(null_interceptor):
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WorkflowTemplateServiceRestInterceptor(),
    )
    client = WorkflowTemplateServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "post_update_workflow_template",
    ) as post, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "pre_update_workflow_template",
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = workflow_templates.UpdateWorkflowTemplateRequest.pb(
            workflow_templates.UpdateWorkflowTemplateRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = workflow_templates.WorkflowTemplate.to_json(
            workflow_templates.WorkflowTemplate()
        )

        request = workflow_templates.UpdateWorkflowTemplateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = workflow_templates.WorkflowTemplate()

        client.update_workflow_template(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_update_workflow_template_rest_bad_request(
    transport: str = "rest",
    request_type=workflow_templates.UpdateWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "template": {
            "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
        }
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_workflow_template(request)


def test_update_workflow_template_rest_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = workflow_templates.WorkflowTemplate()

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "template": {
                "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
            }
        }

        # get truthy value for each flattened field
        mock_args = dict(
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = workflow_templates.WorkflowTemplate.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.update_workflow_template(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{template.name=projects/*/locations/*/workflowTemplates/*}"
            % client.transport._host,
            args[1],
        )


def test_update_workflow_template_rest_flattened_error(transport: str = "rest"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_workflow_template(
            workflow_templates.UpdateWorkflowTemplateRequest(),
            template=workflow_templates.WorkflowTemplate(id="id_value"),
        )


def test_update_workflow_template_rest_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.ListWorkflowTemplatesRequest,
        dict,
    ],
)
def test_list_workflow_templates_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = workflow_templates.ListWorkflowTemplatesResponse(
            next_page_token="next_page_token_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = workflow_templates.ListWorkflowTemplatesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_workflow_templates(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListWorkflowTemplatesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_workflow_templates_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.list_workflow_templates
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.list_workflow_templates
        ] = mock_rpc

        request = {}
        client.list_workflow_templates(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.list_workflow_templates(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_list_workflow_templates_rest_required_fields(
    request_type=workflow_templates.ListWorkflowTemplatesRequest,
):
    transport_class = transports.WorkflowTemplateServiceRestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_workflow_templates._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = "parent_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).list_workflow_templates._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(
        (
            "page_size",
            "page_token",
        )
    )
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == "parent_value"

    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = workflow_templates.ListWorkflowTemplatesResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "get",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = workflow_templates.ListWorkflowTemplatesResponse.pb(
                return_value
            )
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.list_workflow_templates(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_list_workflow_templates_rest_unset_required_fields():
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.list_workflow_templates._get_unset_required_fields({})
    assert set(unset_fields) == (
        set(
            (
                "pageSize",
                "pageToken",
            )
        )
        & set(("parent",))
    )


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_workflow_templates_rest_interceptors(null_interceptor):
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WorkflowTemplateServiceRestInterceptor(),
    )
    client = WorkflowTemplateServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "post_list_workflow_templates",
    ) as post, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor, "pre_list_workflow_templates"
    ) as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = workflow_templates.ListWorkflowTemplatesRequest.pb(
            workflow_templates.ListWorkflowTemplatesRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = (
            workflow_templates.ListWorkflowTemplatesResponse.to_json(
                workflow_templates.ListWorkflowTemplatesResponse()
            )
        )

        request = workflow_templates.ListWorkflowTemplatesRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = workflow_templates.ListWorkflowTemplatesResponse()

        client.list_workflow_templates(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()
        post.assert_called_once()


def test_list_workflow_templates_rest_bad_request(
    transport: str = "rest",
    request_type=workflow_templates.ListWorkflowTemplatesRequest,
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"parent": "projects/sample1/locations/sample2"}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_workflow_templates(request)


def test_list_workflow_templates_rest_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = workflow_templates.ListWorkflowTemplatesResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {"parent": "projects/sample1/locations/sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            parent="parent_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = workflow_templates.ListWorkflowTemplatesResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.list_workflow_templates(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{parent=projects/*/locations/*}/workflowTemplates"
            % client.transport._host,
            args[1],
        )


def test_list_workflow_templates_rest_flattened_error(transport: str = "rest"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_workflow_templates(
            workflow_templates.ListWorkflowTemplatesRequest(),
            parent="parent_value",
        )


def test_list_workflow_templates_rest_pager(transport: str = "rest"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="abc",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[],
                next_page_token="def",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                ],
                next_page_token="ghi",
            ),
            workflow_templates.ListWorkflowTemplatesResponse(
                templates=[
                    workflow_templates.WorkflowTemplate(),
                    workflow_templates.WorkflowTemplate(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            workflow_templates.ListWorkflowTemplatesResponse.to_json(x)
            for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"parent": "projects/sample1/locations/sample2"}

        pager = client.list_workflow_templates(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, workflow_templates.WorkflowTemplate) for i in results)

        pages = list(client.list_workflow_templates(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize(
    "request_type",
    [
        workflow_templates.DeleteWorkflowTemplateRequest,
        dict,
    ],
)
def test_delete_workflow_template_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_workflow_template(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_workflow_template_rest_use_cached_wrapped_rpc():
    # Clients should use _prep_wrapped_messages to create cached wrapped rpcs,
    # instead of constructing them on each call
    with mock.patch("google.api_core.gapic_v1.method.wrap_method") as wrapper_fn:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport="rest",
        )

        # Should wrap all calls on client creation
        assert wrapper_fn.call_count > 0
        wrapper_fn.reset_mock()

        # Ensure method has been cached
        assert (
            client._transport.delete_workflow_template
            in client._transport._wrapped_methods
        )

        # Replace cached wrapped function with mock
        mock_rpc = mock.Mock()
        mock_rpc.return_value.name = (
            "foo"  # operation_request.operation in compute client(s) expect a string.
        )
        client._transport._wrapped_methods[
            client._transport.delete_workflow_template
        ] = mock_rpc

        request = {}
        client.delete_workflow_template(request)

        # Establish that the underlying gRPC stub method was called.
        assert mock_rpc.call_count == 1

        client.delete_workflow_template(request)

        # Establish that a new wrapper was not created for this call
        assert wrapper_fn.call_count == 0
        assert mock_rpc.call_count == 2


def test_delete_workflow_template_rest_required_fields(
    request_type=workflow_templates.DeleteWorkflowTemplateRequest,
):
    transport_class = transports.WorkflowTemplateServiceRestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(
        json_format.MessageToJson(pb_request, use_integers_for_enums=False)
    )

    # verify fields with default values are dropped

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_workflow_template._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = "name_value"

    unset_fields = transport_class(
        credentials=ga_credentials.AnonymousCredentials()
    ).delete_workflow_template._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("version",))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == "name_value"

    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = None
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, "transcode") as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                "uri": "v1/sample_method",
                "method": "delete",
                "query_params": pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = ""

            response_value._content = json_return_value.encode("UTF-8")
            req.return_value = response_value

            response = client.delete_workflow_template(request)

            expected_params = [("$alt", "json;enum-encoding=int")]
            actual_params = req.call_args.kwargs["params"]
            assert expected_params == actual_params


def test_delete_workflow_template_rest_unset_required_fields():
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials
    )

    unset_fields = transport.delete_workflow_template._get_unset_required_fields({})
    assert set(unset_fields) == (set(("version",)) & set(("name",)))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_workflow_template_rest_interceptors(null_interceptor):
    transport = transports.WorkflowTemplateServiceRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None
        if null_interceptor
        else transports.WorkflowTemplateServiceRestInterceptor(),
    )
    client = WorkflowTemplateServiceClient(transport=transport)
    with mock.patch.object(
        type(client.transport._session), "request"
    ) as req, mock.patch.object(
        path_template, "transcode"
    ) as transcode, mock.patch.object(
        transports.WorkflowTemplateServiceRestInterceptor,
        "pre_delete_workflow_template",
    ) as pre:
        pre.assert_not_called()
        pb_message = workflow_templates.DeleteWorkflowTemplateRequest.pb(
            workflow_templates.DeleteWorkflowTemplateRequest()
        )
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()

        request = workflow_templates.DeleteWorkflowTemplateRequest()
        metadata = [
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata

        client.delete_workflow_template(
            request,
            metadata=[
                ("key", "val"),
                ("cephalopod", "squid"),
            ],
        )

        pre.assert_called_once()


def test_delete_workflow_template_rest_bad_request(
    transport: str = "rest",
    request_type=workflow_templates.DeleteWorkflowTemplateRequest,
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {
        "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
    }
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_workflow_template(request)


def test_delete_workflow_template_rest_flattened():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "name": "projects/sample1/locations/sample2/workflowTemplates/sample3"
        }

        # get truthy value for each flattened field
        mock_args = dict(
            name="name_value",
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = ""
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        client.delete_workflow_template(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "%s/v1/{name=projects/*/locations/*/workflowTemplates/*}"
            % client.transport._host,
            args[1],
        )


def test_delete_workflow_template_rest_flattened_error(transport: str = "rest"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_workflow_template(
            workflow_templates.DeleteWorkflowTemplateRequest(),
            name="name_value",
        )


def test_delete_workflow_template_rest_error():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="rest"
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.WorkflowTemplateServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.WorkflowTemplateServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WorkflowTemplateServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.WorkflowTemplateServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = WorkflowTemplateServiceClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = WorkflowTemplateServiceClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.WorkflowTemplateServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = WorkflowTemplateServiceClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.WorkflowTemplateServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = WorkflowTemplateServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.WorkflowTemplateServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.WorkflowTemplateServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.WorkflowTemplateServiceGrpcTransport,
        transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
        transports.WorkflowTemplateServiceRestTransport,
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
        "rest",
    ],
)
def test_transport_kind(transport_name):
    transport = WorkflowTemplateServiceClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.WorkflowTemplateServiceGrpcTransport,
    )


def test_workflow_template_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.WorkflowTemplateServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_workflow_template_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.dataproc_v1.services.workflow_template_service.transports.WorkflowTemplateServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.WorkflowTemplateServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_workflow_template",
        "get_workflow_template",
        "instantiate_workflow_template",
        "instantiate_inline_workflow_template",
        "update_workflow_template",
        "list_workflow_templates",
        "delete_workflow_template",
        "set_iam_policy",
        "get_iam_policy",
        "test_iam_permissions",
        "get_operation",
        "cancel_operation",
        "delete_operation",
        "list_operations",
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


def test_workflow_template_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.dataproc_v1.services.workflow_template_service.transports.WorkflowTemplateServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.WorkflowTemplateServiceTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_workflow_template_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.dataproc_v1.services.workflow_template_service.transports.WorkflowTemplateServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.WorkflowTemplateServiceTransport()
        adc.assert_called_once()


def test_workflow_template_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        WorkflowTemplateServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.WorkflowTemplateServiceGrpcTransport,
        transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
    ],
)
def test_workflow_template_service_transport_auth_adc(transport_class):
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
        transports.WorkflowTemplateServiceGrpcTransport,
        transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
        transports.WorkflowTemplateServiceRestTransport,
    ],
)
def test_workflow_template_service_transport_auth_gdch_credentials(transport_class):
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
        (transports.WorkflowTemplateServiceGrpcTransport, grpc_helpers),
        (transports.WorkflowTemplateServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_workflow_template_service_transport_create_channel(
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
            "dataproc.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="dataproc.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.WorkflowTemplateServiceGrpcTransport,
        transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
    ],
)
def test_workflow_template_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
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


def test_workflow_template_service_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.WorkflowTemplateServiceRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_workflow_template_service_rest_lro_client():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_workflow_template_service_host_no_port(transport_name):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataproc.googleapis.com"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dataproc.googleapis.com:443"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dataproc.googleapis.com"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "grpc",
        "grpc_asyncio",
        "rest",
    ],
)
def test_workflow_template_service_host_with_port(transport_name):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="dataproc.googleapis.com:8000"
        ),
        transport=transport_name,
    )
    assert client.transport._host == (
        "dataproc.googleapis.com:8000"
        if transport_name in ["grpc", "grpc_asyncio"]
        else "https://dataproc.googleapis.com:8000"
    )


@pytest.mark.parametrize(
    "transport_name",
    [
        "rest",
    ],
)
def test_workflow_template_service_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = WorkflowTemplateServiceClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = WorkflowTemplateServiceClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_workflow_template._session
    session2 = client2.transport.create_workflow_template._session
    assert session1 != session2
    session1 = client1.transport.get_workflow_template._session
    session2 = client2.transport.get_workflow_template._session
    assert session1 != session2
    session1 = client1.transport.instantiate_workflow_template._session
    session2 = client2.transport.instantiate_workflow_template._session
    assert session1 != session2
    session1 = client1.transport.instantiate_inline_workflow_template._session
    session2 = client2.transport.instantiate_inline_workflow_template._session
    assert session1 != session2
    session1 = client1.transport.update_workflow_template._session
    session2 = client2.transport.update_workflow_template._session
    assert session1 != session2
    session1 = client1.transport.list_workflow_templates._session
    session2 = client2.transport.list_workflow_templates._session
    assert session1 != session2
    session1 = client1.transport.delete_workflow_template._session
    session2 = client2.transport.delete_workflow_template._session
    assert session1 != session2


def test_workflow_template_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.WorkflowTemplateServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_workflow_template_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.WorkflowTemplateServiceGrpcAsyncIOTransport(
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
        transports.WorkflowTemplateServiceGrpcTransport,
        transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
    ],
)
def test_workflow_template_service_transport_channel_mtls_with_client_cert_source(
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
        transports.WorkflowTemplateServiceGrpcTransport,
        transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
    ],
)
def test_workflow_template_service_transport_channel_mtls_with_adc(transport_class):
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


def test_workflow_template_service_grpc_lro_client():
    client = WorkflowTemplateServiceClient(
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


def test_workflow_template_service_grpc_lro_async_client():
    client = WorkflowTemplateServiceAsyncClient(
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


def test_node_group_path():
    project = "squid"
    region = "clam"
    cluster = "whelk"
    node_group = "octopus"
    expected = "projects/{project}/regions/{region}/clusters/{cluster}/nodeGroups/{node_group}".format(
        project=project,
        region=region,
        cluster=cluster,
        node_group=node_group,
    )
    actual = WorkflowTemplateServiceClient.node_group_path(
        project, region, cluster, node_group
    )
    assert expected == actual


def test_parse_node_group_path():
    expected = {
        "project": "oyster",
        "region": "nudibranch",
        "cluster": "cuttlefish",
        "node_group": "mussel",
    }
    path = WorkflowTemplateServiceClient.node_group_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowTemplateServiceClient.parse_node_group_path(path)
    assert expected == actual


def test_service_path():
    project = "winkle"
    location = "nautilus"
    service = "scallop"
    expected = "projects/{project}/locations/{location}/services/{service}".format(
        project=project,
        location=location,
        service=service,
    )
    actual = WorkflowTemplateServiceClient.service_path(project, location, service)
    assert expected == actual


def test_parse_service_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "service": "clam",
    }
    path = WorkflowTemplateServiceClient.service_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowTemplateServiceClient.parse_service_path(path)
    assert expected == actual


def test_workflow_template_path():
    project = "whelk"
    region = "octopus"
    workflow_template = "oyster"
    expected = "projects/{project}/regions/{region}/workflowTemplates/{workflow_template}".format(
        project=project,
        region=region,
        workflow_template=workflow_template,
    )
    actual = WorkflowTemplateServiceClient.workflow_template_path(
        project, region, workflow_template
    )
    assert expected == actual


def test_parse_workflow_template_path():
    expected = {
        "project": "nudibranch",
        "region": "cuttlefish",
        "workflow_template": "mussel",
    }
    path = WorkflowTemplateServiceClient.workflow_template_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowTemplateServiceClient.parse_workflow_template_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = WorkflowTemplateServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = WorkflowTemplateServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowTemplateServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(
        folder=folder,
    )
    actual = WorkflowTemplateServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = WorkflowTemplateServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowTemplateServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(
        organization=organization,
    )
    actual = WorkflowTemplateServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = WorkflowTemplateServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowTemplateServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(
        project=project,
    )
    actual = WorkflowTemplateServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = WorkflowTemplateServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowTemplateServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project,
        location=location,
    )
    actual = WorkflowTemplateServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = WorkflowTemplateServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = WorkflowTemplateServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.WorkflowTemplateServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = WorkflowTemplateServiceClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.WorkflowTemplateServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = WorkflowTemplateServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.GetIamPolicyRequest
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/regions/sample2/clusters/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.GetIamPolicyRequest,
        dict,
    ],
)
def test_get_iam_policy_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/regions/sample2/clusters/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_set_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.SetIamPolicyRequest
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/regions/sample2/clusters/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_iam_policy(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.SetIamPolicyRequest,
        dict,
    ],
)
def test_set_iam_policy_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/regions/sample2/clusters/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = policy_pb2.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)


def test_test_iam_permissions_rest_bad_request(
    transport: str = "rest", request_type=iam_policy_pb2.TestIamPermissionsRequest
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"resource": "projects/sample1/regions/sample2/clusters/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.test_iam_permissions(request)


@pytest.mark.parametrize(
    "request_type",
    [
        iam_policy_pb2.TestIamPermissionsRequest,
        dict,
    ],
)
def test_test_iam_permissions_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"resource": "projects/sample1/regions/sample2/clusters/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = iam_policy_pb2.TestIamPermissionsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)


def test_cancel_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.CancelOperationRequest
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/regions/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.cancel_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.CancelOperationRequest,
        dict,
    ],
)
def test_cancel_operation_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/regions/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.cancel_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.DeleteOperationRequest
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/regions/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.DeleteOperationRequest,
        dict,
    ],
)
def test_delete_operation_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/regions/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = None

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = "{}"

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.delete_operation(request)

    # Establish that the response is the type that we expect.
    assert response is None


def test_get_operation_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.GetOperationRequest
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/regions/sample2/operations/sample3"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_operation(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.GetOperationRequest,
        dict,
    ],
)
def test_get_operation_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/regions/sample2/operations/sample3"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.get_operation(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_list_operations_rest_bad_request(
    transport: str = "rest", request_type=operations_pb2.ListOperationsRequest
):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    request = request_type()
    request = json_format.ParseDict(
        {"name": "projects/sample1/regions/sample2/operations"}, request
    )

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_operations(request)


@pytest.mark.parametrize(
    "request_type",
    [
        operations_pb2.ListOperationsRequest,
        dict,
    ],
)
def test_list_operations_rest(request_type):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )
    request_init = {"name": "projects/sample1/regions/sample2/operations"}
    request = request_type(**request_init)
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.ListOperationsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        response = client.list_operations(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_delete_operation(transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_operation_async(transport: str = "grpc_asyncio"):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.DeleteOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_operation_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = None

        client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_operation_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.DeleteOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_delete_operation_from_dict():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_delete_operation_from_dict_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_cancel_operation(transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_cancel_operation_async(transport: str = "grpc_asyncio"):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.CancelOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_cancel_operation_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = None

        client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_cancel_operation_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.CancelOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.cancel_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_cancel_operation_from_dict():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_cancel_operation_from_dict_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.cancel_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.cancel_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_get_operation(transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()
        response = client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


@pytest.mark.asyncio
async def test_get_operation_async(transport: str = "grpc_asyncio"):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.GetOperationRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.Operation)


def test_get_operation_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = operations_pb2.Operation()

        client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_operation_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.GetOperationRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        await client.get_operation(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_get_operation_from_dict():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation()

        response = client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_operation_from_dict_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_operation), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation()
        )
        response = await client.get_operation(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_list_operations(transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()
        response = client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


@pytest.mark.asyncio
async def test_list_operations_async(transport: str = "grpc_asyncio"):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = operations_pb2.ListOperationsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, operations_pb2.ListOperationsResponse)


def test_list_operations_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = operations_pb2.ListOperationsResponse()

        client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_operations_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = operations_pb2.ListOperationsRequest()
    request.name = "locations"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        await client.list_operations(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "name=locations",
    ) in kw["metadata"]


def test_list_operations_from_dict():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.ListOperationsResponse()

        response = client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_list_operations_from_dict_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_operations), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.ListOperationsResponse()
        )
        response = await client.list_operations(
            request={
                "name": "locations",
            }
        )
        call.assert_called()


def test_set_iam_policy(transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )
        response = client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_set_iam_policy_async(transport: str = "grpc_asyncio"):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )
        response = await client.set_iam_policy(request)
        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_set_iam_policy_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_set_iam_policy_from_dict_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.set_iam_policy(
            request={
                "resource": "resource_value",
                "policy": policy_pb2.Policy(version=774),
            }
        )
        call.assert_called()


def test_get_iam_policy(transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy(
            version=774,
            etag=b"etag_blob",
        )

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


@pytest.mark.asyncio
async def test_get_iam_policy_async(transport: str = "grpc_asyncio"):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            policy_pb2.Policy(
                version=774,
                etag=b"etag_blob",
            )
        )

        response = await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy_pb2.Policy)

    assert response.version == 774

    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = policy_pb2.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_iam_policy_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        await client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy_pb2.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_get_iam_policy_from_dict_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(policy_pb2.Policy())

        response = await client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options_pb2.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_test_iam_permissions(transport: str = "grpc"):
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse(
            permissions=["permissions_value"],
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


@pytest.mark.asyncio
async def test_test_iam_permissions_async(transport: str = "grpc_asyncio"):
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy_pb2.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse(
                permissions=["permissions_value"],
            )
        )

        response = await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy_pb2.TestIamPermissionsResponse)

    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_test_iam_permissions_field_headers_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy_pb2.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        await client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "resource=resource/value",
    ) in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = WorkflowTemplateServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy_pb2.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


@pytest.mark.asyncio
async def test_test_iam_permissions_from_dict_async():
    client = WorkflowTemplateServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            iam_policy_pb2.TestIamPermissionsResponse()
        )

        response = await client.test_iam_permissions(
            request={
                "resource": "resource_value",
                "permissions": ["permissions_value"],
            }
        )
        call.assert_called()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = WorkflowTemplateServiceClient(
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
        "rest",
        "grpc",
    ]
    for transport in transports:
        client = WorkflowTemplateServiceClient(
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
        (
            WorkflowTemplateServiceClient,
            transports.WorkflowTemplateServiceGrpcTransport,
        ),
        (
            WorkflowTemplateServiceAsyncClient,
            transports.WorkflowTemplateServiceGrpcAsyncIOTransport,
        ),
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
                host=client._DEFAULT_ENDPOINT_TEMPLATE.format(
                    UNIVERSE_DOMAIN=client._DEFAULT_UNIVERSE
                ),
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
