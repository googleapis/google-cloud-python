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

from requests import Response
from requests import Request
from requests.sessions import Session

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.compute_v1.services.instances import InstancesClient
from google.cloud.compute_v1.services.instances import pagers
from google.cloud.compute_v1.services.instances import transports
from google.cloud.compute_v1.types import compute
from google.oauth2 import service_account
import google.auth


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

    assert InstancesClient._get_default_mtls_endpoint(None) is None
    assert InstancesClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert (
        InstancesClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        InstancesClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        InstancesClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert InstancesClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [InstancesClient,])
def test_instances_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "compute.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name", [(transports.InstancesRestTransport, "rest"),]
)
def test_instances_client_service_account_always_use_jwt(
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


@pytest.mark.parametrize("client_class", [InstancesClient,])
def test_instances_client_from_service_account_file(client_class):
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

        assert client.transport._host == "compute.googleapis.com:443"


def test_instances_client_get_transport_class():
    transport = InstancesClient.get_transport_class()
    available_transports = [
        transports.InstancesRestTransport,
    ]
    assert transport in available_transports

    transport = InstancesClient.get_transport_class("rest")
    assert transport == transports.InstancesRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(InstancesClient, transports.InstancesRestTransport, "rest"),],
)
@mock.patch.object(
    InstancesClient, "DEFAULT_ENDPOINT", modify_default_endpoint(InstancesClient)
)
def test_instances_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(InstancesClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(InstancesClient, "get_transport_class") as gtc:
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
        client = client_class(transport=transport_name, client_options=options)
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
        (InstancesClient, transports.InstancesRestTransport, "rest", "true"),
        (InstancesClient, transports.InstancesRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    InstancesClient, "DEFAULT_ENDPOINT", modify_default_endpoint(InstancesClient)
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_instances_client_mtls_env_auto(
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
            client = client_class(transport=transport_name, client_options=options)

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
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(InstancesClient, transports.InstancesRestTransport, "rest"),],
)
def test_instances_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
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
    [(InstancesClient, transports.InstancesRestTransport, "rest"),],
)
def test_instances_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
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


def test_add_access_config_rest(
    transport: str = "rest", request_type=compute.AddAccessConfigInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["access_config_resource"] = compute.AccessConfig(
        external_ipv6="external_ipv6_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.add_access_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_add_access_config_rest_bad_request(
    transport: str = "rest", request_type=compute.AddAccessConfigInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["access_config_resource"] = compute.AccessConfig(
        external_ipv6="external_ipv6_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.add_access_config(request)


def test_add_access_config_rest_from_dict():
    test_add_access_config_rest(request_type=dict)


def test_add_access_config_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            network_interface="network_interface_value",
            access_config_resource=compute.AccessConfig(
                external_ipv6="external_ipv6_value"
            ),
        )
        mock_args.update(sample_request)
        client.add_access_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/addAccessConfig"
            % client.transport._host,
            args[1],
        )


def test_add_access_config_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_access_config(
            compute.AddAccessConfigInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            network_interface="network_interface_value",
            access_config_resource=compute.AccessConfig(
                external_ipv6="external_ipv6_value"
            ),
        )


def test_add_resource_policies_rest(
    transport: str = "rest", request_type=compute.AddResourcePoliciesInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_add_resource_policies_request_resource"
    ] = compute.InstancesAddResourcePoliciesRequest(
        resource_policies=["resource_policies_value"]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.add_resource_policies(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_add_resource_policies_rest_bad_request(
    transport: str = "rest", request_type=compute.AddResourcePoliciesInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_add_resource_policies_request_resource"
    ] = compute.InstancesAddResourcePoliciesRequest(
        resource_policies=["resource_policies_value"]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.add_resource_policies(request)


def test_add_resource_policies_rest_from_dict():
    test_add_resource_policies_rest(request_type=dict)


def test_add_resource_policies_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_add_resource_policies_request_resource=compute.InstancesAddResourcePoliciesRequest(
                resource_policies=["resource_policies_value"]
            ),
        )
        mock_args.update(sample_request)
        client.add_resource_policies(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/addResourcePolicies"
            % client.transport._host,
            args[1],
        )


def test_add_resource_policies_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_resource_policies(
            compute.AddResourcePoliciesInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_add_resource_policies_request_resource=compute.InstancesAddResourcePoliciesRequest(
                resource_policies=["resource_policies_value"]
            ),
        )


def test_aggregated_list_rest(
    transport: str = "rest", request_type=compute.AggregatedListInstancesRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceAggregatedList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            unreachables=["unreachables_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceAggregatedList.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.aggregated_list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AggregatedListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.unreachables == ["unreachables_value"]


def test_aggregated_list_rest_bad_request(
    transport: str = "rest", request_type=compute.AggregatedListInstancesRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.aggregated_list(request)


def test_aggregated_list_rest_from_dict():
    test_aggregated_list_rest(request_type=dict)


def test_aggregated_list_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceAggregatedList()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceAggregatedList.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1"}

        # get truthy value for each flattened field
        mock_args = dict(project="project_value",)
        mock_args.update(sample_request)
        client.aggregated_list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/aggregated/instances"
            % client.transport._host,
            args[1],
        )


def test_aggregated_list_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.aggregated_list(
            compute.AggregatedListInstancesRequest(), project="project_value",
        )


def test_aggregated_list_rest_pager():
    client = InstancesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.InstanceAggregatedList(
                items={
                    "a": compute.InstancesScopedList(),
                    "b": compute.InstancesScopedList(),
                    "c": compute.InstancesScopedList(),
                },
                next_page_token="abc",
            ),
            compute.InstanceAggregatedList(items={}, next_page_token="def",),
            compute.InstanceAggregatedList(
                items={"g": compute.InstancesScopedList(),}, next_page_token="ghi",
            ),
            compute.InstanceAggregatedList(
                items={
                    "h": compute.InstancesScopedList(),
                    "i": compute.InstancesScopedList(),
                },
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.InstanceAggregatedList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1"}

        pager = client.aggregated_list(request=sample_request)

        assert isinstance(pager.get("a"), compute.InstancesScopedList)
        assert pager.get("h") is None

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tuple) for i in results)
        for result in results:
            assert isinstance(result, tuple)
            assert tuple(type(t) for t in result) == (str, compute.InstancesScopedList)

        assert pager.get("a") is None
        assert isinstance(pager.get("h"), compute.InstancesScopedList)

        pages = list(client.aggregated_list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_attach_disk_rest(
    transport: str = "rest", request_type=compute.AttachDiskInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["attached_disk_resource"] = compute.AttachedDisk(auto_delete=True)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.attach_disk(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_attach_disk_rest_bad_request(
    transport: str = "rest", request_type=compute.AttachDiskInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["attached_disk_resource"] = compute.AttachedDisk(auto_delete=True)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.attach_disk(request)


def test_attach_disk_rest_from_dict():
    test_attach_disk_rest(request_type=dict)


def test_attach_disk_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            attached_disk_resource=compute.AttachedDisk(auto_delete=True),
        )
        mock_args.update(sample_request)
        client.attach_disk(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/attachDisk"
            % client.transport._host,
            args[1],
        )


def test_attach_disk_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.attach_disk(
            compute.AttachDiskInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            attached_disk_resource=compute.AttachedDisk(auto_delete=True),
        )


def test_bulk_insert_rest(
    transport: str = "rest", request_type=compute.BulkInsertInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init[
        "bulk_insert_instance_resource_resource"
    ] = compute.BulkInsertInstanceResource(count=553)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.bulk_insert(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_bulk_insert_rest_bad_request(
    transport: str = "rest", request_type=compute.BulkInsertInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init[
        "bulk_insert_instance_resource_resource"
    ] = compute.BulkInsertInstanceResource(count=553)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.bulk_insert(request)


def test_bulk_insert_rest_from_dict():
    test_bulk_insert_rest(request_type=dict)


def test_bulk_insert_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "zone": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            bulk_insert_instance_resource_resource=compute.BulkInsertInstanceResource(
                count=553
            ),
        )
        mock_args.update(sample_request)
        client.bulk_insert(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/bulkInsert"
            % client.transport._host,
            args[1],
        )


def test_bulk_insert_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.bulk_insert(
            compute.BulkInsertInstanceRequest(),
            project="project_value",
            zone="zone_value",
            bulk_insert_instance_resource_resource=compute.BulkInsertInstanceResource(
                count=553
            ),
        )


def test_delete_rest(
    transport: str = "rest", request_type=compute.DeleteInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_delete_rest_bad_request(
    transport: str = "rest", request_type=compute.DeleteInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete(request)


def test_delete_rest_from_dict():
    test_delete_rest(request_type=dict)


def test_delete_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.delete(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}"
            % client.transport._host,
            args[1],
        )


def test_delete_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete(
            compute.DeleteInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_delete_access_config_rest(
    transport: str = "rest", request_type=compute.DeleteAccessConfigInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete_access_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_delete_access_config_rest_bad_request(
    transport: str = "rest", request_type=compute.DeleteAccessConfigInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_access_config(request)


def test_delete_access_config_rest_from_dict():
    test_delete_access_config_rest(request_type=dict)


def test_delete_access_config_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            access_config="access_config_value",
            network_interface="network_interface_value",
        )
        mock_args.update(sample_request)
        client.delete_access_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/deleteAccessConfig"
            % client.transport._host,
            args[1],
        )


def test_delete_access_config_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_access_config(
            compute.DeleteAccessConfigInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            access_config="access_config_value",
            network_interface="network_interface_value",
        )


def test_detach_disk_rest(
    transport: str = "rest", request_type=compute.DetachDiskInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.detach_disk(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_detach_disk_rest_bad_request(
    transport: str = "rest", request_type=compute.DetachDiskInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.detach_disk(request)


def test_detach_disk_rest_from_dict():
    test_detach_disk_rest(request_type=dict)


def test_detach_disk_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            device_name="device_name_value",
        )
        mock_args.update(sample_request)
        client.detach_disk(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/detachDisk"
            % client.transport._host,
            args[1],
        )


def test_detach_disk_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.detach_disk(
            compute.DetachDiskInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            device_name="device_name_value",
        )


def test_get_rest(transport: str = "rest", request_type=compute.GetInstanceRequest):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Instance(
            can_ip_forward=True,
            cpu_platform="cpu_platform_value",
            creation_timestamp="creation_timestamp_value",
            deletion_protection=True,
            description="description_value",
            fingerprint="fingerprint_value",
            hostname="hostname_value",
            id=205,
            kind="kind_value",
            label_fingerprint="label_fingerprint_value",
            last_start_timestamp="last_start_timestamp_value",
            last_stop_timestamp="last_stop_timestamp_value",
            last_suspended_timestamp="last_suspended_timestamp_value",
            machine_type="machine_type_value",
            min_cpu_platform="min_cpu_platform_value",
            name="name_value",
            private_ipv6_google_access=compute.Instance.PrivateIpv6GoogleAccess.ENABLE_BIDIRECTIONAL_ACCESS_TO_GOOGLE,
            resource_policies=["resource_policies_value"],
            satisfies_pzs=True,
            self_link="self_link_value",
            start_restricted=True,
            status=compute.Instance.Status.DEPROVISIONING,
            status_message="status_message_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Instance.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Instance)
    assert response.can_ip_forward is True
    assert response.cpu_platform == "cpu_platform_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.deletion_protection is True
    assert response.description == "description_value"
    assert response.fingerprint == "fingerprint_value"
    assert response.hostname == "hostname_value"
    assert response.id == 205
    assert response.kind == "kind_value"
    assert response.label_fingerprint == "label_fingerprint_value"
    assert response.last_start_timestamp == "last_start_timestamp_value"
    assert response.last_stop_timestamp == "last_stop_timestamp_value"
    assert response.last_suspended_timestamp == "last_suspended_timestamp_value"
    assert response.machine_type == "machine_type_value"
    assert response.min_cpu_platform == "min_cpu_platform_value"
    assert response.name == "name_value"
    assert (
        response.private_ipv6_google_access
        == compute.Instance.PrivateIpv6GoogleAccess.ENABLE_BIDIRECTIONAL_ACCESS_TO_GOOGLE
    )
    assert response.resource_policies == ["resource_policies_value"]
    assert response.satisfies_pzs is True
    assert response.self_link == "self_link_value"
    assert response.start_restricted is True
    assert response.status == compute.Instance.Status.DEPROVISIONING
    assert response.status_message == "status_message_value"
    assert response.zone == "zone_value"


def test_get_rest_bad_request(
    transport: str = "rest", request_type=compute.GetInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get(request)


def test_get_rest_from_dict():
    test_get_rest(request_type=dict)


def test_get_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Instance()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Instance.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.get(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}"
            % client.transport._host,
            args[1],
        )


def test_get_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_get_effective_firewalls_rest(
    transport: str = "rest", request_type=compute.GetEffectiveFirewallsInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstancesGetEffectiveFirewallsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstancesGetEffectiveFirewallsResponse.to_json(
            return_value
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_effective_firewalls(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.InstancesGetEffectiveFirewallsResponse)


def test_get_effective_firewalls_rest_bad_request(
    transport: str = "rest", request_type=compute.GetEffectiveFirewallsInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_effective_firewalls(request)


def test_get_effective_firewalls_rest_from_dict():
    test_get_effective_firewalls_rest(request_type=dict)


def test_get_effective_firewalls_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstancesGetEffectiveFirewallsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstancesGetEffectiveFirewallsResponse.to_json(
            return_value
        )

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            network_interface="network_interface_value",
        )
        mock_args.update(sample_request)
        client.get_effective_firewalls(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/getEffectiveFirewalls"
            % client.transport._host,
            args[1],
        )


def test_get_effective_firewalls_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_effective_firewalls(
            compute.GetEffectiveFirewallsInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            network_interface="network_interface_value",
        )


def test_get_guest_attributes_rest(
    transport: str = "rest", request_type=compute.GetGuestAttributesInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.GuestAttributes(
            kind="kind_value",
            query_path="query_path_value",
            self_link="self_link_value",
            variable_key="variable_key_value",
            variable_value="variable_value_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.GuestAttributes.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_guest_attributes(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.GuestAttributes)
    assert response.kind == "kind_value"
    assert response.query_path == "query_path_value"
    assert response.self_link == "self_link_value"
    assert response.variable_key == "variable_key_value"
    assert response.variable_value == "variable_value_value"


def test_get_guest_attributes_rest_bad_request(
    transport: str = "rest", request_type=compute.GetGuestAttributesInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_guest_attributes(request)


def test_get_guest_attributes_rest_from_dict():
    test_get_guest_attributes_rest(request_type=dict)


def test_get_guest_attributes_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.GuestAttributes()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.GuestAttributes.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.get_guest_attributes(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/getGuestAttributes"
            % client.transport._host,
            args[1],
        )


def test_get_guest_attributes_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_guest_attributes(
            compute.GetGuestAttributesInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_get_iam_policy_rest(
    transport: str = "rest", request_type=compute.GetIamPolicyInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy(etag="etag_value", iam_owned=True, version=774,)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Policy.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Policy)
    assert response.etag == "etag_value"
    assert response.iam_owned is True
    assert response.version == 774


def test_get_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=compute.GetIamPolicyInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request = request_type(request_init)

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


def test_get_iam_policy_rest_from_dict():
    test_get_iam_policy_rest(request_type=dict)


def test_get_iam_policy_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Policy.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "resource": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", resource="resource_value",
        )
        mock_args.update(sample_request)
        client.get_iam_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{resource}/getIamPolicy"
            % client.transport._host,
            args[1],
        )


def test_get_iam_policy_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            compute.GetIamPolicyInstanceRequest(),
            project="project_value",
            zone="zone_value",
            resource="resource_value",
        )


def test_get_screenshot_rest(
    transport: str = "rest", request_type=compute.GetScreenshotInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Screenshot(contents="contents_value", kind="kind_value",)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Screenshot.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_screenshot(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Screenshot)
    assert response.contents == "contents_value"
    assert response.kind == "kind_value"


def test_get_screenshot_rest_bad_request(
    transport: str = "rest", request_type=compute.GetScreenshotInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_screenshot(request)


def test_get_screenshot_rest_from_dict():
    test_get_screenshot_rest(request_type=dict)


def test_get_screenshot_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Screenshot()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Screenshot.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.get_screenshot(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/screenshot"
            % client.transport._host,
            args[1],
        )


def test_get_screenshot_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_screenshot(
            compute.GetScreenshotInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_get_serial_port_output_rest(
    transport: str = "rest", request_type=compute.GetSerialPortOutputInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SerialPortOutput(
            contents="contents_value",
            kind="kind_value",
            next_=542,
            self_link="self_link_value",
            start=558,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.SerialPortOutput.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_serial_port_output(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.SerialPortOutput)
    assert response.contents == "contents_value"
    assert response.kind == "kind_value"
    assert response.next_ == 542
    assert response.self_link == "self_link_value"
    assert response.start == 558


def test_get_serial_port_output_rest_bad_request(
    transport: str = "rest", request_type=compute.GetSerialPortOutputInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_serial_port_output(request)


def test_get_serial_port_output_rest_from_dict():
    test_get_serial_port_output_rest(request_type=dict)


def test_get_serial_port_output_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SerialPortOutput()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.SerialPortOutput.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.get_serial_port_output(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/serialPort"
            % client.transport._host,
            args[1],
        )


def test_get_serial_port_output_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_serial_port_output(
            compute.GetSerialPortOutputInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_get_shielded_instance_identity_rest(
    transport: str = "rest",
    request_type=compute.GetShieldedInstanceIdentityInstanceRequest,
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.ShieldedInstanceIdentity(kind="kind_value",)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.ShieldedInstanceIdentity.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_shielded_instance_identity(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.ShieldedInstanceIdentity)
    assert response.kind == "kind_value"


def test_get_shielded_instance_identity_rest_bad_request(
    transport: str = "rest",
    request_type=compute.GetShieldedInstanceIdentityInstanceRequest,
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_shielded_instance_identity(request)


def test_get_shielded_instance_identity_rest_from_dict():
    test_get_shielded_instance_identity_rest(request_type=dict)


def test_get_shielded_instance_identity_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.ShieldedInstanceIdentity()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.ShieldedInstanceIdentity.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.get_shielded_instance_identity(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/getShieldedInstanceIdentity"
            % client.transport._host,
            args[1],
        )


def test_get_shielded_instance_identity_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_shielded_instance_identity(
            compute.GetShieldedInstanceIdentityInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_insert_rest(
    transport: str = "rest", request_type=compute.InsertInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init["instance_resource"] = compute.Instance(
        advanced_machine_features=compute.AdvancedMachineFeatures(
            enable_nested_virtualization=True
        )
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.insert(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_insert_rest_bad_request(
    transport: str = "rest", request_type=compute.InsertInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request_init["instance_resource"] = compute.Instance(
        advanced_machine_features=compute.AdvancedMachineFeatures(
            enable_nested_virtualization=True
        )
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.insert(request)


def test_insert_rest_from_dict():
    test_insert_rest(request_type=dict)


def test_insert_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "zone": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance_resource=compute.Instance(
                advanced_machine_features=compute.AdvancedMachineFeatures(
                    enable_nested_virtualization=True
                )
            ),
        )
        mock_args.update(sample_request)
        client.insert(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances"
            % client.transport._host,
            args[1],
        )


def test_insert_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert(
            compute.InsertInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance_resource=compute.Instance(
                advanced_machine_features=compute.AdvancedMachineFeatures(
                    enable_nested_virtualization=True
                )
            ),
        )


def test_list_rest(transport: str = "rest", request_type=compute.ListInstancesRequest):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceList(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceList.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"


def test_list_rest_bad_request(
    transport: str = "rest", request_type=compute.ListInstancesRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list(request)


def test_list_rest_from_dict():
    test_list_rest(request_type=dict)


def test_list_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceList()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceList.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {"project": "sample1", "zone": "sample2"}

        # get truthy value for each flattened field
        mock_args = dict(project="project_value", zone="zone_value",)
        mock_args.update(sample_request)
        client.list(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances"
            % client.transport._host,
            args[1],
        )


def test_list_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListInstancesRequest(), project="project_value", zone="zone_value",
        )


def test_list_rest_pager():
    client = InstancesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.InstanceList(
                items=[compute.Instance(), compute.Instance(), compute.Instance(),],
                next_page_token="abc",
            ),
            compute.InstanceList(items=[], next_page_token="def",),
            compute.InstanceList(items=[compute.Instance(),], next_page_token="ghi",),
            compute.InstanceList(items=[compute.Instance(), compute.Instance(),],),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.InstanceList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {"project": "sample1", "zone": "sample2"}

        pager = client.list(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.Instance) for i in results)

        pages = list(client.list(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_referrers_rest(
    transport: str = "rest", request_type=compute.ListReferrersInstancesRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceListReferrers(
            id="id_value",
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceListReferrers.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_referrers(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListReferrersPager)
    assert response.id == "id_value"
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"


def test_list_referrers_rest_bad_request(
    transport: str = "rest", request_type=compute.ListReferrersInstancesRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_referrers(request)


def test_list_referrers_rest_from_dict():
    test_list_referrers_rest(request_type=dict)


def test_list_referrers_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.InstanceListReferrers()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.InstanceListReferrers.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.list_referrers(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/referrers"
            % client.transport._host,
            args[1],
        )


def test_list_referrers_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_referrers(
            compute.ListReferrersInstancesRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_list_referrers_rest_pager():
    client = InstancesClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        # with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            compute.InstanceListReferrers(
                items=[compute.Reference(), compute.Reference(), compute.Reference(),],
                next_page_token="abc",
            ),
            compute.InstanceListReferrers(items=[], next_page_token="def",),
            compute.InstanceListReferrers(
                items=[compute.Reference(),], next_page_token="ghi",
            ),
            compute.InstanceListReferrers(
                items=[compute.Reference(), compute.Reference(),],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.InstanceListReferrers.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        pager = client.list_referrers(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.Reference) for i in results)

        pages = list(client.list_referrers(request=sample_request).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_remove_resource_policies_rest(
    transport: str = "rest", request_type=compute.RemoveResourcePoliciesInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_remove_resource_policies_request_resource"
    ] = compute.InstancesRemoveResourcePoliciesRequest(
        resource_policies=["resource_policies_value"]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.remove_resource_policies(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_remove_resource_policies_rest_bad_request(
    transport: str = "rest", request_type=compute.RemoveResourcePoliciesInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_remove_resource_policies_request_resource"
    ] = compute.InstancesRemoveResourcePoliciesRequest(
        resource_policies=["resource_policies_value"]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.remove_resource_policies(request)


def test_remove_resource_policies_rest_from_dict():
    test_remove_resource_policies_rest(request_type=dict)


def test_remove_resource_policies_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_remove_resource_policies_request_resource=compute.InstancesRemoveResourcePoliciesRequest(
                resource_policies=["resource_policies_value"]
            ),
        )
        mock_args.update(sample_request)
        client.remove_resource_policies(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/removeResourcePolicies"
            % client.transport._host,
            args[1],
        )


def test_remove_resource_policies_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_resource_policies(
            compute.RemoveResourcePoliciesInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_remove_resource_policies_request_resource=compute.InstancesRemoveResourcePoliciesRequest(
                resource_policies=["resource_policies_value"]
            ),
        )


def test_reset_rest(transport: str = "rest", request_type=compute.ResetInstanceRequest):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.reset(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_reset_rest_bad_request(
    transport: str = "rest", request_type=compute.ResetInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.reset(request)


def test_reset_rest_from_dict():
    test_reset_rest(request_type=dict)


def test_reset_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.reset(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/reset"
            % client.transport._host,
            args[1],
        )


def test_reset_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.reset(
            compute.ResetInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_send_diagnostic_interrupt_rest(
    transport: str = "rest", request_type=compute.SendDiagnosticInterruptInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SendDiagnosticInterruptInstanceResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.SendDiagnosticInterruptInstanceResponse.to_json(
            return_value
        )
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.send_diagnostic_interrupt(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.SendDiagnosticInterruptInstanceResponse)


def test_send_diagnostic_interrupt_rest_bad_request(
    transport: str = "rest", request_type=compute.SendDiagnosticInterruptInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.send_diagnostic_interrupt(request)


def test_send_diagnostic_interrupt_rest_from_dict():
    test_send_diagnostic_interrupt_rest(request_type=dict)


def test_send_diagnostic_interrupt_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SendDiagnosticInterruptInstanceResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.SendDiagnosticInterruptInstanceResponse.to_json(
            return_value
        )

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.send_diagnostic_interrupt(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/sendDiagnosticInterrupt"
            % client.transport._host,
            args[1],
        )


def test_send_diagnostic_interrupt_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.send_diagnostic_interrupt(
            compute.SendDiagnosticInterruptInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_set_deletion_protection_rest(
    transport: str = "rest", request_type=compute.SetDeletionProtectionInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_deletion_protection(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_deletion_protection_rest_bad_request(
    transport: str = "rest", request_type=compute.SetDeletionProtectionInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_deletion_protection(request)


def test_set_deletion_protection_rest_from_dict():
    test_set_deletion_protection_rest(request_type=dict)


def test_set_deletion_protection_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "resource": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", resource="resource_value",
        )
        mock_args.update(sample_request)
        client.set_deletion_protection(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{resource}/setDeletionProtection"
            % client.transport._host,
            args[1],
        )


def test_set_deletion_protection_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_deletion_protection(
            compute.SetDeletionProtectionInstanceRequest(),
            project="project_value",
            zone="zone_value",
            resource="resource_value",
        )


def test_set_disk_auto_delete_rest(
    transport: str = "rest", request_type=compute.SetDiskAutoDeleteInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_disk_auto_delete(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_disk_auto_delete_rest_bad_request(
    transport: str = "rest", request_type=compute.SetDiskAutoDeleteInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_disk_auto_delete(request)


def test_set_disk_auto_delete_rest_from_dict():
    test_set_disk_auto_delete_rest(request_type=dict)


def test_set_disk_auto_delete_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            auto_delete=True,
            device_name="device_name_value",
        )
        mock_args.update(sample_request)
        client.set_disk_auto_delete(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setDiskAutoDelete"
            % client.transport._host,
            args[1],
        )


def test_set_disk_auto_delete_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_disk_auto_delete(
            compute.SetDiskAutoDeleteInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            auto_delete=True,
            device_name="device_name_value",
        )


def test_set_iam_policy_rest(
    transport: str = "rest", request_type=compute.SetIamPolicyInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request_init["zone_set_policy_request_resource"] = compute.ZoneSetPolicyRequest(
        bindings=[compute.Binding(binding_id="binding_id_value")]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy(etag="etag_value", iam_owned=True, version=774,)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Policy.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Policy)
    assert response.etag == "etag_value"
    assert response.iam_owned is True
    assert response.version == 774


def test_set_iam_policy_rest_bad_request(
    transport: str = "rest", request_type=compute.SetIamPolicyInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request_init["zone_set_policy_request_resource"] = compute.ZoneSetPolicyRequest(
        bindings=[compute.Binding(binding_id="binding_id_value")]
    )
    request = request_type(request_init)

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


def test_set_iam_policy_rest_from_dict():
    test_set_iam_policy_rest(request_type=dict)


def test_set_iam_policy_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Policy.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "resource": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            resource="resource_value",
            zone_set_policy_request_resource=compute.ZoneSetPolicyRequest(
                bindings=[compute.Binding(binding_id="binding_id_value")]
            ),
        )
        mock_args.update(sample_request)
        client.set_iam_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{resource}/setIamPolicy"
            % client.transport._host,
            args[1],
        )


def test_set_iam_policy_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            compute.SetIamPolicyInstanceRequest(),
            project="project_value",
            zone="zone_value",
            resource="resource_value",
            zone_set_policy_request_resource=compute.ZoneSetPolicyRequest(
                bindings=[compute.Binding(binding_id="binding_id_value")]
            ),
        )


def test_set_labels_rest(
    transport: str = "rest", request_type=compute.SetLabelsInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_labels_request_resource"
    ] = compute.InstancesSetLabelsRequest(label_fingerprint="label_fingerprint_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_labels(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_labels_rest_bad_request(
    transport: str = "rest", request_type=compute.SetLabelsInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_labels_request_resource"
    ] = compute.InstancesSetLabelsRequest(label_fingerprint="label_fingerprint_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_labels(request)


def test_set_labels_rest_from_dict():
    test_set_labels_rest(request_type=dict)


def test_set_labels_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_labels_request_resource=compute.InstancesSetLabelsRequest(
                label_fingerprint="label_fingerprint_value"
            ),
        )
        mock_args.update(sample_request)
        client.set_labels(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setLabels"
            % client.transport._host,
            args[1],
        )


def test_set_labels_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_labels(
            compute.SetLabelsInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_labels_request_resource=compute.InstancesSetLabelsRequest(
                label_fingerprint="label_fingerprint_value"
            ),
        )


def test_set_machine_resources_rest(
    transport: str = "rest", request_type=compute.SetMachineResourcesInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_machine_resources_request_resource"
    ] = compute.InstancesSetMachineResourcesRequest(
        guest_accelerators=[compute.AcceleratorConfig(accelerator_count=1805)]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_machine_resources(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_machine_resources_rest_bad_request(
    transport: str = "rest", request_type=compute.SetMachineResourcesInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_machine_resources_request_resource"
    ] = compute.InstancesSetMachineResourcesRequest(
        guest_accelerators=[compute.AcceleratorConfig(accelerator_count=1805)]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_machine_resources(request)


def test_set_machine_resources_rest_from_dict():
    test_set_machine_resources_rest(request_type=dict)


def test_set_machine_resources_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_machine_resources_request_resource=compute.InstancesSetMachineResourcesRequest(
                guest_accelerators=[compute.AcceleratorConfig(accelerator_count=1805)]
            ),
        )
        mock_args.update(sample_request)
        client.set_machine_resources(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setMachineResources"
            % client.transport._host,
            args[1],
        )


def test_set_machine_resources_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_machine_resources(
            compute.SetMachineResourcesInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_machine_resources_request_resource=compute.InstancesSetMachineResourcesRequest(
                guest_accelerators=[compute.AcceleratorConfig(accelerator_count=1805)]
            ),
        )


def test_set_machine_type_rest(
    transport: str = "rest", request_type=compute.SetMachineTypeInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_machine_type_request_resource"
    ] = compute.InstancesSetMachineTypeRequest(machine_type="machine_type_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_machine_type(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_machine_type_rest_bad_request(
    transport: str = "rest", request_type=compute.SetMachineTypeInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_machine_type_request_resource"
    ] = compute.InstancesSetMachineTypeRequest(machine_type="machine_type_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_machine_type(request)


def test_set_machine_type_rest_from_dict():
    test_set_machine_type_rest(request_type=dict)


def test_set_machine_type_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_machine_type_request_resource=compute.InstancesSetMachineTypeRequest(
                machine_type="machine_type_value"
            ),
        )
        mock_args.update(sample_request)
        client.set_machine_type(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setMachineType"
            % client.transport._host,
            args[1],
        )


def test_set_machine_type_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_machine_type(
            compute.SetMachineTypeInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_machine_type_request_resource=compute.InstancesSetMachineTypeRequest(
                machine_type="machine_type_value"
            ),
        )


def test_set_metadata_rest(
    transport: str = "rest", request_type=compute.SetMetadataInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["metadata_resource"] = compute.Metadata(
        fingerprint="fingerprint_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_metadata(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_metadata_rest_bad_request(
    transport: str = "rest", request_type=compute.SetMetadataInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["metadata_resource"] = compute.Metadata(
        fingerprint="fingerprint_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_metadata(request)


def test_set_metadata_rest_from_dict():
    test_set_metadata_rest(request_type=dict)


def test_set_metadata_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            metadata_resource=compute.Metadata(fingerprint="fingerprint_value"),
        )
        mock_args.update(sample_request)
        client.set_metadata(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setMetadata"
            % client.transport._host,
            args[1],
        )


def test_set_metadata_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_metadata(
            compute.SetMetadataInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            metadata_resource=compute.Metadata(fingerprint="fingerprint_value"),
        )


def test_set_min_cpu_platform_rest(
    transport: str = "rest", request_type=compute.SetMinCpuPlatformInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_min_cpu_platform_request_resource"
    ] = compute.InstancesSetMinCpuPlatformRequest(
        min_cpu_platform="min_cpu_platform_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_min_cpu_platform(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_min_cpu_platform_rest_bad_request(
    transport: str = "rest", request_type=compute.SetMinCpuPlatformInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_min_cpu_platform_request_resource"
    ] = compute.InstancesSetMinCpuPlatformRequest(
        min_cpu_platform="min_cpu_platform_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_min_cpu_platform(request)


def test_set_min_cpu_platform_rest_from_dict():
    test_set_min_cpu_platform_rest(request_type=dict)


def test_set_min_cpu_platform_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_min_cpu_platform_request_resource=compute.InstancesSetMinCpuPlatformRequest(
                min_cpu_platform="min_cpu_platform_value"
            ),
        )
        mock_args.update(sample_request)
        client.set_min_cpu_platform(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setMinCpuPlatform"
            % client.transport._host,
            args[1],
        )


def test_set_min_cpu_platform_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_min_cpu_platform(
            compute.SetMinCpuPlatformInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_min_cpu_platform_request_resource=compute.InstancesSetMinCpuPlatformRequest(
                min_cpu_platform="min_cpu_platform_value"
            ),
        )


def test_set_scheduling_rest(
    transport: str = "rest", request_type=compute.SetSchedulingInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["scheduling_resource"] = compute.Scheduling(automatic_restart=True)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_scheduling(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_scheduling_rest_bad_request(
    transport: str = "rest", request_type=compute.SetSchedulingInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["scheduling_resource"] = compute.Scheduling(automatic_restart=True)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_scheduling(request)


def test_set_scheduling_rest_from_dict():
    test_set_scheduling_rest(request_type=dict)


def test_set_scheduling_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            scheduling_resource=compute.Scheduling(automatic_restart=True),
        )
        mock_args.update(sample_request)
        client.set_scheduling(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setScheduling"
            % client.transport._host,
            args[1],
        )


def test_set_scheduling_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_scheduling(
            compute.SetSchedulingInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            scheduling_resource=compute.Scheduling(automatic_restart=True),
        )


def test_set_service_account_rest(
    transport: str = "rest", request_type=compute.SetServiceAccountInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_service_account_request_resource"
    ] = compute.InstancesSetServiceAccountRequest(email="email_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_service_account(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_service_account_rest_bad_request(
    transport: str = "rest", request_type=compute.SetServiceAccountInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_set_service_account_request_resource"
    ] = compute.InstancesSetServiceAccountRequest(email="email_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_service_account(request)


def test_set_service_account_rest_from_dict():
    test_set_service_account_rest(request_type=dict)


def test_set_service_account_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_service_account_request_resource=compute.InstancesSetServiceAccountRequest(
                email="email_value"
            ),
        )
        mock_args.update(sample_request)
        client.set_service_account(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setServiceAccount"
            % client.transport._host,
            args[1],
        )


def test_set_service_account_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_service_account(
            compute.SetServiceAccountInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_set_service_account_request_resource=compute.InstancesSetServiceAccountRequest(
                email="email_value"
            ),
        )


def test_set_shielded_instance_integrity_policy_rest(
    transport: str = "rest",
    request_type=compute.SetShieldedInstanceIntegrityPolicyInstanceRequest,
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "shielded_instance_integrity_policy_resource"
    ] = compute.ShieldedInstanceIntegrityPolicy(update_auto_learn_policy=True)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_shielded_instance_integrity_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_shielded_instance_integrity_policy_rest_bad_request(
    transport: str = "rest",
    request_type=compute.SetShieldedInstanceIntegrityPolicyInstanceRequest,
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "shielded_instance_integrity_policy_resource"
    ] = compute.ShieldedInstanceIntegrityPolicy(update_auto_learn_policy=True)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_shielded_instance_integrity_policy(request)


def test_set_shielded_instance_integrity_policy_rest_from_dict():
    test_set_shielded_instance_integrity_policy_rest(request_type=dict)


def test_set_shielded_instance_integrity_policy_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            shielded_instance_integrity_policy_resource=compute.ShieldedInstanceIntegrityPolicy(
                update_auto_learn_policy=True
            ),
        )
        mock_args.update(sample_request)
        client.set_shielded_instance_integrity_policy(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setShieldedInstanceIntegrityPolicy"
            % client.transport._host,
            args[1],
        )


def test_set_shielded_instance_integrity_policy_rest_flattened_error(
    transport: str = "rest",
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_shielded_instance_integrity_policy(
            compute.SetShieldedInstanceIntegrityPolicyInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            shielded_instance_integrity_policy_resource=compute.ShieldedInstanceIntegrityPolicy(
                update_auto_learn_policy=True
            ),
        )


def test_set_tags_rest(
    transport: str = "rest", request_type=compute.SetTagsInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["tags_resource"] = compute.Tags(fingerprint="fingerprint_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_tags(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_set_tags_rest_bad_request(
    transport: str = "rest", request_type=compute.SetTagsInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["tags_resource"] = compute.Tags(fingerprint="fingerprint_value")
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.set_tags(request)


def test_set_tags_rest_from_dict():
    test_set_tags_rest(request_type=dict)


def test_set_tags_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            tags_resource=compute.Tags(fingerprint="fingerprint_value"),
        )
        mock_args.update(sample_request)
        client.set_tags(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/setTags"
            % client.transport._host,
            args[1],
        )


def test_set_tags_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_tags(
            compute.SetTagsInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            tags_resource=compute.Tags(fingerprint="fingerprint_value"),
        )


def test_simulate_maintenance_event_rest(
    transport: str = "rest",
    request_type=compute.SimulateMaintenanceEventInstanceRequest,
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.simulate_maintenance_event(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_simulate_maintenance_event_rest_bad_request(
    transport: str = "rest",
    request_type=compute.SimulateMaintenanceEventInstanceRequest,
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.simulate_maintenance_event(request)


def test_simulate_maintenance_event_rest_from_dict():
    test_simulate_maintenance_event_rest(request_type=dict)


def test_simulate_maintenance_event_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.simulate_maintenance_event(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/simulateMaintenanceEvent"
            % client.transport._host,
            args[1],
        )


def test_simulate_maintenance_event_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.simulate_maintenance_event(
            compute.SimulateMaintenanceEventInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_start_rest(transport: str = "rest", request_type=compute.StartInstanceRequest):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.start(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_start_rest_bad_request(
    transport: str = "rest", request_type=compute.StartInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.start(request)


def test_start_rest_from_dict():
    test_start_rest(request_type=dict)


def test_start_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.start(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/start"
            % client.transport._host,
            args[1],
        )


def test_start_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start(
            compute.StartInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_start_with_encryption_key_rest(
    transport: str = "rest", request_type=compute.StartWithEncryptionKeyInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_start_with_encryption_key_request_resource"
    ] = compute.InstancesStartWithEncryptionKeyRequest(
        disks=[
            compute.CustomerEncryptionKeyProtectedDisk(
                disk_encryption_key=compute.CustomerEncryptionKey(
                    kms_key_name="kms_key_name_value"
                )
            )
        ]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.start_with_encryption_key(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_start_with_encryption_key_rest_bad_request(
    transport: str = "rest", request_type=compute.StartWithEncryptionKeyInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init[
        "instances_start_with_encryption_key_request_resource"
    ] = compute.InstancesStartWithEncryptionKeyRequest(
        disks=[
            compute.CustomerEncryptionKeyProtectedDisk(
                disk_encryption_key=compute.CustomerEncryptionKey(
                    kms_key_name="kms_key_name_value"
                )
            )
        ]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.start_with_encryption_key(request)


def test_start_with_encryption_key_rest_from_dict():
    test_start_with_encryption_key_rest(request_type=dict)


def test_start_with_encryption_key_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_start_with_encryption_key_request_resource=compute.InstancesStartWithEncryptionKeyRequest(
                disks=[
                    compute.CustomerEncryptionKeyProtectedDisk(
                        disk_encryption_key=compute.CustomerEncryptionKey(
                            kms_key_name="kms_key_name_value"
                        )
                    )
                ]
            ),
        )
        mock_args.update(sample_request)
        client.start_with_encryption_key(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/startWithEncryptionKey"
            % client.transport._host,
            args[1],
        )


def test_start_with_encryption_key_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.start_with_encryption_key(
            compute.StartWithEncryptionKeyInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instances_start_with_encryption_key_request_resource=compute.InstancesStartWithEncryptionKeyRequest(
                disks=[
                    compute.CustomerEncryptionKeyProtectedDisk(
                        disk_encryption_key=compute.CustomerEncryptionKey(
                            kms_key_name="kms_key_name_value"
                        )
                    )
                ]
            ),
        )


def test_stop_rest(transport: str = "rest", request_type=compute.StopInstanceRequest):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.stop(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_stop_rest_bad_request(
    transport: str = "rest", request_type=compute.StopInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.stop(request)


def test_stop_rest_from_dict():
    test_stop_rest(request_type=dict)


def test_stop_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value", zone="zone_value", instance="instance_value",
        )
        mock_args.update(sample_request)
        client.stop(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/stop"
            % client.transport._host,
            args[1],
        )


def test_stop_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.stop(
            compute.StopInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
        )


def test_test_iam_permissions_rest(
    transport: str = "rest", request_type=compute.TestIamPermissionsInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request_init["test_permissions_request_resource"] = compute.TestPermissionsRequest(
        permissions=["permissions_value"]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.TestPermissionsResponse(
            permissions=["permissions_value"],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.TestPermissionsResponse.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.TestPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_rest_bad_request(
    transport: str = "rest", request_type=compute.TestIamPermissionsInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "resource": "sample3"}
    request_init["test_permissions_request_resource"] = compute.TestPermissionsRequest(
        permissions=["permissions_value"]
    )
    request = request_type(request_init)

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


def test_test_iam_permissions_rest_from_dict():
    test_test_iam_permissions_rest(request_type=dict)


def test_test_iam_permissions_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.TestPermissionsResponse()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.TestPermissionsResponse.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "resource": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            resource="resource_value",
            test_permissions_request_resource=compute.TestPermissionsRequest(
                permissions=["permissions_value"]
            ),
        )
        mock_args.update(sample_request)
        client.test_iam_permissions(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{resource}/testIamPermissions"
            % client.transport._host,
            args[1],
        )


def test_test_iam_permissions_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            compute.TestIamPermissionsInstanceRequest(),
            project="project_value",
            zone="zone_value",
            resource="resource_value",
            test_permissions_request_resource=compute.TestPermissionsRequest(
                permissions=["permissions_value"]
            ),
        )


def test_update_rest(
    transport: str = "rest", request_type=compute.UpdateInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["instance_resource"] = compute.Instance(
        advanced_machine_features=compute.AdvancedMachineFeatures(
            enable_nested_virtualization=True
        )
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_update_rest_bad_request(
    transport: str = "rest", request_type=compute.UpdateInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["instance_resource"] = compute.Instance(
        advanced_machine_features=compute.AdvancedMachineFeatures(
            enable_nested_virtualization=True
        )
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update(request)


def test_update_rest_from_dict():
    test_update_rest(request_type=dict)


def test_update_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instance_resource=compute.Instance(
                advanced_machine_features=compute.AdvancedMachineFeatures(
                    enable_nested_virtualization=True
                )
            ),
        )
        mock_args.update(sample_request)
        client.update(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}"
            % client.transport._host,
            args[1],
        )


def test_update_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update(
            compute.UpdateInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            instance_resource=compute.Instance(
                advanced_machine_features=compute.AdvancedMachineFeatures(
                    enable_nested_virtualization=True
                )
            ),
        )


def test_update_access_config_rest(
    transport: str = "rest", request_type=compute.UpdateAccessConfigInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["access_config_resource"] = compute.AccessConfig(
        external_ipv6="external_ipv6_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_access_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_update_access_config_rest_bad_request(
    transport: str = "rest", request_type=compute.UpdateAccessConfigInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["access_config_resource"] = compute.AccessConfig(
        external_ipv6="external_ipv6_value"
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_access_config(request)


def test_update_access_config_rest_from_dict():
    test_update_access_config_rest(request_type=dict)


def test_update_access_config_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            network_interface="network_interface_value",
            access_config_resource=compute.AccessConfig(
                external_ipv6="external_ipv6_value"
            ),
        )
        mock_args.update(sample_request)
        client.update_access_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/updateAccessConfig"
            % client.transport._host,
            args[1],
        )


def test_update_access_config_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_access_config(
            compute.UpdateAccessConfigInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            network_interface="network_interface_value",
            access_config_resource=compute.AccessConfig(
                external_ipv6="external_ipv6_value"
            ),
        )


def test_update_display_device_rest(
    transport: str = "rest", request_type=compute.UpdateDisplayDeviceInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["display_device_resource"] = compute.DisplayDevice(enable_display=True)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_display_device(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_update_display_device_rest_bad_request(
    transport: str = "rest", request_type=compute.UpdateDisplayDeviceInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["display_device_resource"] = compute.DisplayDevice(enable_display=True)
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_display_device(request)


def test_update_display_device_rest_from_dict():
    test_update_display_device_rest(request_type=dict)


def test_update_display_device_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            display_device_resource=compute.DisplayDevice(enable_display=True),
        )
        mock_args.update(sample_request)
        client.update_display_device(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/updateDisplayDevice"
            % client.transport._host,
            args[1],
        )


def test_update_display_device_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_display_device(
            compute.UpdateDisplayDeviceInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            display_device_resource=compute.DisplayDevice(enable_display=True),
        )


def test_update_network_interface_rest(
    transport: str = "rest", request_type=compute.UpdateNetworkInterfaceInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["network_interface_resource"] = compute.NetworkInterface(
        access_configs=[compute.AccessConfig(external_ipv6="external_ipv6_value")]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_network_interface(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_update_network_interface_rest_bad_request(
    transport: str = "rest", request_type=compute.UpdateNetworkInterfaceInstanceRequest
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["network_interface_resource"] = compute.NetworkInterface(
        access_configs=[compute.AccessConfig(external_ipv6="external_ipv6_value")]
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_network_interface(request)


def test_update_network_interface_rest_from_dict():
    test_update_network_interface_rest(request_type=dict)


def test_update_network_interface_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            network_interface="network_interface_value",
            network_interface_resource=compute.NetworkInterface(
                access_configs=[
                    compute.AccessConfig(external_ipv6="external_ipv6_value")
                ]
            ),
        )
        mock_args.update(sample_request)
        client.update_network_interface(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/updateNetworkInterface"
            % client.transport._host,
            args[1],
        )


def test_update_network_interface_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_network_interface(
            compute.UpdateNetworkInterfaceInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            network_interface="network_interface_value",
            network_interface_resource=compute.NetworkInterface(
                access_configs=[
                    compute.AccessConfig(external_ipv6="external_ipv6_value")
                ]
            ),
        )


def test_update_shielded_instance_config_rest(
    transport: str = "rest",
    request_type=compute.UpdateShieldedInstanceConfigInstanceRequest,
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["shielded_instance_config_resource"] = compute.ShieldedInstanceConfig(
        enable_integrity_monitoring=True
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id=205,
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_group_id="operation_group_id_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id=947,
            target_link="target_link_value",
            user="user_value",
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.update_shielded_instance_config(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == 205
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_group_id == "operation_group_id_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == 947
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.zone == "zone_value"


def test_update_shielded_instance_config_rest_bad_request(
    transport: str = "rest",
    request_type=compute.UpdateShieldedInstanceConfigInstanceRequest,
):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {"project": "sample1", "zone": "sample2", "instance": "sample3"}
    request_init["shielded_instance_config_resource"] = compute.ShieldedInstanceConfig(
        enable_integrity_monitoring=True
    )
    request = request_type(request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, "request") as req, pytest.raises(
        core_exceptions.BadRequest
    ):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_shielded_instance_config(request)


def test_update_shielded_instance_config_rest_from_dict():
    test_update_shielded_instance_config_rest(request_type=dict)


def test_update_shielded_instance_config_rest_flattened(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = compute.Operation.to_json(return_value)

        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # get arguments that satisfy an http rule for this method
        sample_request = {
            "project": "sample1",
            "zone": "sample2",
            "instance": "sample3",
        }

        # get truthy value for each flattened field
        mock_args = dict(
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            shielded_instance_config_resource=compute.ShieldedInstanceConfig(
                enable_integrity_monitoring=True
            ),
        )
        mock_args.update(sample_request)
        client.update_shielded_instance_config(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate(
            "https://%s/compute/v1/projects/{project}/zones/{zone}/instances/{instance}/updateShieldedInstanceConfig"
            % client.transport._host,
            args[1],
        )


def test_update_shielded_instance_config_rest_flattened_error(transport: str = "rest"):
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_shielded_instance_config(
            compute.UpdateShieldedInstanceConfigInstanceRequest(),
            project="project_value",
            zone="zone_value",
            instance="instance_value",
            shielded_instance_config_resource=compute.ShieldedInstanceConfig(
                enable_integrity_monitoring=True
            ),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.InstancesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InstancesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.InstancesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InstancesClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.InstancesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = InstancesClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.InstancesRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = InstancesClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize("transport_class", [transports.InstancesRestTransport,])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_instances_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.InstancesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_instances_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.instances.transports.InstancesTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.InstancesTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "add_access_config",
        "add_resource_policies",
        "aggregated_list",
        "attach_disk",
        "bulk_insert",
        "delete",
        "delete_access_config",
        "detach_disk",
        "get",
        "get_effective_firewalls",
        "get_guest_attributes",
        "get_iam_policy",
        "get_screenshot",
        "get_serial_port_output",
        "get_shielded_instance_identity",
        "insert",
        "list",
        "list_referrers",
        "remove_resource_policies",
        "reset",
        "send_diagnostic_interrupt",
        "set_deletion_protection",
        "set_disk_auto_delete",
        "set_iam_policy",
        "set_labels",
        "set_machine_resources",
        "set_machine_type",
        "set_metadata",
        "set_min_cpu_platform",
        "set_scheduling",
        "set_service_account",
        "set_shielded_instance_integrity_policy",
        "set_tags",
        "simulate_maintenance_event",
        "start",
        "start_with_encryption_key",
        "stop",
        "test_iam_permissions",
        "update",
        "update_access_config",
        "update_display_device",
        "update_network_interface",
        "update_shielded_instance_config",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()


def test_instances_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.instances.transports.InstancesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.InstancesTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_instances_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.compute_v1.services.instances.transports.InstancesTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.InstancesTransport()
        adc.assert_called_once()


def test_instances_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        InstancesClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_instances_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.InstancesRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_instances_host_no_port():
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:443"


def test_instances_host_with_port():
    client = InstancesClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:8000"


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = InstancesClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = InstancesClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = InstancesClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = InstancesClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = InstancesClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = InstancesClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = InstancesClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = InstancesClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = InstancesClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = InstancesClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = InstancesClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = InstancesClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = InstancesClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = InstancesClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = InstancesClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.InstancesTransport, "_prep_wrapped_messages"
    ) as prep:
        client = InstancesClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.InstancesTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = InstancesClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


def test_transport_close():
    transports = {
        "rest": "_session",
    }

    for transport, close_name in transports.items():
        client = InstancesClient(
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
    ]
    for transport in transports:
        client = InstancesClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()
