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
from google.cloud.recommendationengine_v1beta1.services.catalog_service import (
    CatalogServiceClient,
)
from google.cloud.recommendationengine_v1beta1.services.catalog_service import pagers
from google.cloud.recommendationengine_v1beta1.services.catalog_service import (
    transports,
)
from google.cloud.recommendationengine_v1beta1.types import catalog
from google.cloud.recommendationengine_v1beta1.types import catalog_service
from google.cloud.recommendationengine_v1beta1.types import common
from google.cloud.recommendationengine_v1beta1.types import import_
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


def test_catalog_service_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = CatalogServiceClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = CatalogServiceClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "recommendationengine.googleapis.com:443"


def test_catalog_service_client_client_options():
    # Check the default options have their expected values.
    assert (
        CatalogServiceClient.DEFAULT_OPTIONS.api_endpoint
        == "recommendationengine.googleapis.com"
    )

    # Check that options can be customized.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.catalog_service.CatalogServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = CatalogServiceClient(client_options=options)
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_catalog_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.recommendationengine_v1beta1.services.catalog_service.CatalogServiceClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = CatalogServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_create_catalog_item(transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = catalog_service.CreateCatalogItemRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem(
            id="id_value",
            title="title_value",
            description="description_value",
            language_code="language_code_value",
            tags=["tags_value"],
            item_group_id="item_group_id_value",
        )

        response = client.create_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CatalogItem)
    assert response.id == "id_value"
    assert response.title == "title_value"
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.item_group_id == "item_group_id_value"


def test_get_catalog_item(transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = catalog_service.GetCatalogItemRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem(
            id="id_value",
            title="title_value",
            description="description_value",
            language_code="language_code_value",
            tags=["tags_value"],
            item_group_id="item_group_id_value",
        )

        response = client.get_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CatalogItem)
    assert response.id == "id_value"
    assert response.title == "title_value"
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.item_group_id == "item_group_id_value"


def test_get_catalog_item_field_headers():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.GetCatalogItemRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_catalog_item), "__call__"
    ) as call:
        call.return_value = catalog.CatalogItem()
        client.get_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_catalog_item_flattened():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_catalog_item(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_catalog_item_flattened_error():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_catalog_item(
            catalog_service.GetCatalogItemRequest(), name="name_value"
        )


def test_list_catalog_items(transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = catalog_service.ListCatalogItemsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog_service.ListCatalogItemsResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCatalogItemsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_catalog_items_field_headers():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = catalog_service.ListCatalogItemsRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_catalog_items), "__call__"
    ) as call:
        call.return_value = catalog_service.ListCatalogItemsResponse()
        client.list_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_catalog_items_pager():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_catalog_items), "__call__"
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
                catalog_items=[], next_page_token="def"
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem()], next_page_token="ghi"
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(), catalog.CatalogItem()]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_catalog_items(request={})]
        assert len(results) == 6
        assert all(isinstance(i, catalog.CatalogItem) for i in results)


def test_list_catalog_items_pages():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_catalog_items), "__call__"
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
                catalog_items=[], next_page_token="def"
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem()], next_page_token="ghi"
            ),
            catalog_service.ListCatalogItemsResponse(
                catalog_items=[catalog.CatalogItem(), catalog.CatalogItem()]
            ),
            RuntimeError,
        )
        pages = list(client.list_catalog_items(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_update_catalog_item(transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = catalog_service.UpdateCatalogItemRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem(
            id="id_value",
            title="title_value",
            description="description_value",
            language_code="language_code_value",
            tags=["tags_value"],
            item_group_id="item_group_id_value",
        )

        response = client.update_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, catalog.CatalogItem)
    assert response.id == "id_value"
    assert response.title == "title_value"
    assert response.description == "description_value"
    assert response.language_code == "language_code_value"
    assert response.tags == ["tags_value"]
    assert response.item_group_id == "item_group_id_value"


def test_update_catalog_item_flattened():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = catalog.CatalogItem()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_catalog_item(
            catalog_item=catalog.CatalogItem(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].catalog_item == catalog.CatalogItem(id="id_value")
        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_catalog_item_flattened_error():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_catalog_item(
            catalog_service.UpdateCatalogItemRequest(),
            catalog_item=catalog.CatalogItem(id="id_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_catalog_item(transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = catalog_service.DeleteCatalogItemRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_catalog_item(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_catalog_item_flattened():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_catalog_item), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_catalog_item(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_catalog_item_flattened_error():
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_catalog_item(
            catalog_service.DeleteCatalogItemRequest(), name="name_value"
        )


def test_import_catalog_items(transport: str = "grpc"):
    client = CatalogServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = import_.ImportCatalogItemsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.import_catalog_items), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")

        response = client.import_catalog_items(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = CatalogServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CatalogServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = CatalogServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CatalogServiceClient(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.CatalogServiceGrpcTransport)


def test_catalog_service_base_transport():
    # Instantiate the base transport.
    transport = transports.CatalogServiceTransport(
        credentials=credentials.AnonymousCredentials()
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


def test_catalog_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        CatalogServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_catalog_service_host_no_port():
    client = CatalogServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommendationengine.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "recommendationengine.googleapis.com:443"


def test_catalog_service_host_with_port():
    client = CatalogServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="recommendationengine.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "recommendationengine.googleapis.com:8000"


def test_catalog_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.CatalogServiceGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel


def test_catalog_service_grpc_lro_client():
    client = CatalogServiceClient(
        credentials=credentials.AnonymousCredentials(), transport="grpc"
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client
