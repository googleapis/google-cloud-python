# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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
from google.api_core import future
from google.api_core import operations_v1
from google.auth import credentials
from google.cloud.memcache_v1beta2.services.cloud_memcache import CloudMemcacheClient
from google.cloud.memcache_v1beta2.services.cloud_memcache import pagers
from google.cloud.memcache_v1beta2.services.cloud_memcache import transports
from google.cloud.memcache_v1beta2.types import cloud_memcache
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def test_cloud_memcache_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = CloudMemcacheClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = CloudMemcacheClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "memcache.googleapis.com:443"


def test_cloud_memcache_client_client_options():
    # Check the default options have their expected values.
    assert CloudMemcacheClient.DEFAULT_OPTIONS.api_endpoint == "memcache.googleapis.com"

    # Check that options can be customized.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.memcache_v1beta2.services.cloud_memcache.CloudMemcacheClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = CloudMemcacheClient(client_options=options)
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_cloud_memcache_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.memcache_v1beta2.services.cloud_memcache.CloudMemcacheClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = CloudMemcacheClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_list_instances(transport: str = "grpc"):
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_memcache.ListInstancesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_instances), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_memcache.ListInstancesResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"]
        )

        response = client.list_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListInstancesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_instances_field_headers():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_memcache.ListInstancesRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_instances), "__call__") as call:
        call.return_value = cloud_memcache.ListInstancesResponse()
        response = client.list_instances(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_instances_flattened():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_instances), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_memcache.ListInstancesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_instances(parent="parent_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_instances_flattened_error():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_instances(
            cloud_memcache.ListInstancesRequest(), parent="parent_value"
        )


def test_list_instances_pager():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_instances), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_memcache.ListInstancesResponse(
                resources=[
                    cloud_memcache.Instance(),
                    cloud_memcache.Instance(),
                    cloud_memcache.Instance(),
                ],
                next_page_token="abc",
            ),
            cloud_memcache.ListInstancesResponse(resources=[], next_page_token="def"),
            cloud_memcache.ListInstancesResponse(
                resources=[cloud_memcache.Instance()], next_page_token="ghi"
            ),
            cloud_memcache.ListInstancesResponse(
                resources=[cloud_memcache.Instance(), cloud_memcache.Instance()]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_instances(request={})]
        assert len(results) == 6
        assert all([isinstance(i, cloud_memcache.Instance) for i in results])


def test_list_instances_pages():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_instances), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_memcache.ListInstancesResponse(
                resources=[
                    cloud_memcache.Instance(),
                    cloud_memcache.Instance(),
                    cloud_memcache.Instance(),
                ],
                next_page_token="abc",
            ),
            cloud_memcache.ListInstancesResponse(resources=[], next_page_token="def"),
            cloud_memcache.ListInstancesResponse(
                resources=[cloud_memcache.Instance()], next_page_token="ghi"
            ),
            cloud_memcache.ListInstancesResponse(
                resources=[cloud_memcache.Instance(), cloud_memcache.Instance()]
            ),
            RuntimeError,
        )
        pages = list(client.list_instances(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_instance(transport: str = "grpc"):
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_memcache.GetInstanceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_memcache.Instance(
            name="name_value",
            display_name="display_name_value",
            authorized_network="authorized_network_value",
            zones=["zones_value"],
            node_count=1070,
            memcache_version=cloud_memcache.MemcacheVersion.MEMCACHE_1_5,
            state=cloud_memcache.Instance.State.CREATING,
            memcache_full_version="memcache_full_version_value",
            discovery_endpoint="discovery_endpoint_value",
        )

        response = client.get_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_memcache.Instance)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.authorized_network == "authorized_network_value"
    assert response.zones == ["zones_value"]
    assert response.node_count == 1070
    assert response.memcache_version == cloud_memcache.MemcacheVersion.MEMCACHE_1_5
    assert response.state == cloud_memcache.Instance.State.CREATING
    assert response.memcache_full_version == "memcache_full_version_value"
    assert response.discovery_endpoint == "discovery_endpoint_value"


def test_get_instance_field_headers():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_memcache.GetInstanceRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_instance), "__call__") as call:
        call.return_value = cloud_memcache.Instance()
        response = client.get_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_instance_flattened():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_memcache.Instance()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_instance(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_instance_flattened_error():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_instance(cloud_memcache.GetInstanceRequest(), name="name_value")


def test_create_instance(transport: str = "grpc"):
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_memcache.CreateInstanceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.create_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_instance_flattened():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_instance(
            parent="parent_value",
            instance_id="instance_id_value",
            resource=cloud_memcache.Instance(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].instance_id == "instance_id_value"
        assert args[0].resource == cloud_memcache.Instance(name="name_value")


def test_create_instance_flattened_error():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_instance(
            cloud_memcache.CreateInstanceRequest(),
            parent="parent_value",
            instance_id="instance_id_value",
            resource=cloud_memcache.Instance(name="name_value"),
        )


def test_update_instance(transport: str = "grpc"):
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_memcache.UpdateInstanceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.update_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_instance_flattened():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_instance(
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
            resource=cloud_memcache.Instance(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])
        assert args[0].resource == cloud_memcache.Instance(name="name_value")


def test_update_instance_flattened_error():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_instance(
            cloud_memcache.UpdateInstanceRequest(),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
            resource=cloud_memcache.Instance(name="name_value"),
        )


def test_update_parameters(transport: str = "grpc"):
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_memcache.UpdateParametersRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.update_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_parameters_flattened():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_parameters(
            name="name_value",
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
            parameters=cloud_memcache.MemcacheParameters(id="id_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])
        assert args[0].parameters == cloud_memcache.MemcacheParameters(id="id_value")


def test_update_parameters_flattened_error():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_parameters(
            cloud_memcache.UpdateParametersRequest(),
            name="name_value",
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
            parameters=cloud_memcache.MemcacheParameters(id="id_value"),
        )


def test_delete_instance(transport: str = "grpc"):
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_memcache.DeleteInstanceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.delete_instance(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_instance_flattened():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_instance), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_instance(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_instance_flattened_error():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_instance(
            cloud_memcache.DeleteInstanceRequest(), name="name_value"
        )


def test_apply_parameters(transport: str = "grpc"):
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_memcache.ApplyParametersRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.apply_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.apply_parameters(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_apply_parameters_flattened():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.apply_parameters), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.apply_parameters(
            name="name_value", node_ids=["node_ids_value"], apply_all=True
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].node_ids == ["node_ids_value"]
        assert args[0].apply_all == True


def test_apply_parameters_flattened_error():
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.apply_parameters(
            cloud_memcache.ApplyParametersRequest(),
            name="name_value",
            node_ids=["node_ids_value"],
            apply_all=True,
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudMemcacheGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = CloudMemcacheClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudMemcacheGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = CloudMemcacheClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudMemcacheClient(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.CloudMemcacheGrpcTransport)


def test_cloud_memcache_base_transport():
    # Instantiate the base transport.
    transport = transports.CloudMemcacheTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_instances",
        "get_instance",
        "create_instance",
        "update_instance",
        "update_parameters",
        "delete_instance",
        "apply_parameters",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_cloud_memcache_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        client = CloudMemcacheClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_cloud_memcache_host_no_port():
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="memcache.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "memcache.googleapis.com:443"


def test_cloud_memcache_host_with_port():
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="memcache.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "memcache.googleapis.com:8000"


def test_cloud_memcache_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.CloudMemcacheGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel


def test_cloud_memcache_grpc_lro_client():
    client = CloudMemcacheClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc"
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_instance_path():
    project = "squid"
    location = "clam"
    instance = "whelk"

    expected = "projects/{project}/locations/{location}/instances/{instance}".format(
        project=project, location=location, instance=instance
    )
    actual = CloudMemcacheClient.instance_path(project, location, instance)
    assert expected == actual
