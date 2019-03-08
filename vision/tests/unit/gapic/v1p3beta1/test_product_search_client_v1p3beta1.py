# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests."""

import mock
import pytest

from google.rpc import status_pb2

from google.cloud import vision_v1p3beta1
from google.cloud.vision_v1p3beta1.proto import product_search_service_pb2
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


class MultiCallableStub(object):
    """Stub for the grpc.UnaryUnaryMultiCallable interface."""

    def __init__(self, method, channel_stub):
        self.method = method
        self.channel_stub = channel_stub

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        self.channel_stub.requests.append((self.method, request))

        response = None
        if self.channel_stub.responses:
            response = self.channel_stub.responses.pop()

        if isinstance(response, Exception):
            raise response

        if response:
            return response


class ChannelStub(object):
    """Stub for the grpc.Channel interface."""

    def __init__(self, responses=[]):
        self.responses = responses
        self.requests = []

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        return MultiCallableStub(method, self)


class CustomException(Exception):
    pass


class TestProductSearchClient(object):
    def test_create_product_set(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = product_search_service_pb2.ProductSet(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        product_set = {}
        product_set_id = "productSetId4216680"

        response = client.create_product_set(parent, product_set, product_set_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.CreateProductSetRequest(
            parent=parent, product_set=product_set, product_set_id=product_set_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_product_set_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        product_set = {}
        product_set_id = "productSetId4216680"

        with pytest.raises(CustomException):
            client.create_product_set(parent, product_set, product_set_id)

    def test_list_product_sets(self):
        # Setup Expected Response
        next_page_token = ""
        product_sets_element = {}
        product_sets = [product_sets_element]
        expected_response = {
            "next_page_token": next_page_token,
            "product_sets": product_sets,
        }
        expected_response = product_search_service_pb2.ListProductSetsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_product_sets(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.product_sets[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.ListProductSetsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_product_sets_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_product_sets(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_product_set(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        expected_response = {"name": name_2, "display_name": display_name}
        expected_response = product_search_service_pb2.ProductSet(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")

        response = client.get_product_set(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.GetProductSetRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_product_set_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")

        with pytest.raises(CustomException):
            client.get_product_set(name)

    def test_update_product_set(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = product_search_service_pb2.ProductSet(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        product_set = {}
        update_mask = {}

        response = client.update_product_set(product_set, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.UpdateProductSetRequest(
            product_set=product_set, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_product_set_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        product_set = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_product_set(product_set, update_mask)

    def test_delete_product_set(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")

        client.delete_product_set(name)

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.DeleteProductSetRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_product_set_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")

        with pytest.raises(CustomException):
            client.delete_product_set(name)

    def test_create_product(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        product_category = "productCategory-1607451058"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "product_category": product_category,
        }
        expected_response = product_search_service_pb2.Product(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        product = {}
        product_id = "productId1753008747"

        response = client.create_product(parent, product, product_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.CreateProductRequest(
            parent=parent, product=product, product_id=product_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_product_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        product = {}
        product_id = "productId1753008747"

        with pytest.raises(CustomException):
            client.create_product(parent, product, product_id)

    def test_list_products(self):
        # Setup Expected Response
        next_page_token = ""
        products_element = {}
        products = [products_element]
        expected_response = {"next_page_token": next_page_token, "products": products}
        expected_response = product_search_service_pb2.ListProductsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_products(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.products[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.ListProductsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_products_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_products(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_product(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        product_category = "productCategory-1607451058"
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "description": description,
            "product_category": product_category,
        }
        expected_response = product_search_service_pb2.Product(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        name = client.product_path("[PROJECT]", "[LOCATION]", "[PRODUCT]")

        response = client.get_product(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.GetProductRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_product_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        name = client.product_path("[PROJECT]", "[LOCATION]", "[PRODUCT]")

        with pytest.raises(CustomException):
            client.get_product(name)

    def test_update_product(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        product_category = "productCategory-1607451058"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "description": description,
            "product_category": product_category,
        }
        expected_response = product_search_service_pb2.Product(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        product = {}
        update_mask = {}

        response = client.update_product(product, update_mask)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.UpdateProductRequest(
            product=product, update_mask=update_mask
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_product_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        product = {}
        update_mask = {}

        with pytest.raises(CustomException):
            client.update_product(product, update_mask)

    def test_delete_product(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        name = client.product_path("[PROJECT]", "[LOCATION]", "[PRODUCT]")

        client.delete_product(name)

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.DeleteProductRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_product_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        name = client.product_path("[PROJECT]", "[LOCATION]", "[PRODUCT]")

        with pytest.raises(CustomException):
            client.delete_product(name)

    def test_create_reference_image(self):
        # Setup Expected Response
        name = "name3373707"
        uri = "uri116076"
        expected_response = {"name": name, "uri": uri}
        expected_response = product_search_service_pb2.ReferenceImage(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        parent = client.product_path("[PROJECT]", "[LOCATION]", "[PRODUCT]")
        reference_image = {}
        reference_image_id = "referenceImageId1946713331"

        response = client.create_reference_image(
            parent, reference_image, reference_image_id
        )
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.CreateReferenceImageRequest(
            parent=parent,
            reference_image=reference_image,
            reference_image_id=reference_image_id,
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_reference_image_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        parent = client.product_path("[PROJECT]", "[LOCATION]", "[PRODUCT]")
        reference_image = {}
        reference_image_id = "referenceImageId1946713331"

        with pytest.raises(CustomException):
            client.create_reference_image(parent, reference_image, reference_image_id)

    def test_delete_reference_image(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        name = client.reference_image_path(
            "[PROJECT]", "[LOCATION]", "[PRODUCT]", "[REFERENCE_IMAGE]"
        )

        client.delete_reference_image(name)

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.DeleteReferenceImageRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_reference_image_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        name = client.reference_image_path(
            "[PROJECT]", "[LOCATION]", "[PRODUCT]", "[REFERENCE_IMAGE]"
        )

        with pytest.raises(CustomException):
            client.delete_reference_image(name)

    def test_list_reference_images(self):
        # Setup Expected Response
        page_size = 883849137
        next_page_token = ""
        reference_images_element = {}
        reference_images = [reference_images_element]
        expected_response = {
            "page_size": page_size,
            "next_page_token": next_page_token,
            "reference_images": reference_images,
        }
        expected_response = product_search_service_pb2.ListReferenceImagesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        parent = client.product_path("[PROJECT]", "[LOCATION]", "[PRODUCT]")

        paged_list_response = client.list_reference_images(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.reference_images[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.ListReferenceImagesRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_reference_images_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        parent = client.product_path("[PROJECT]", "[LOCATION]", "[PRODUCT]")

        paged_list_response = client.list_reference_images(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_reference_image(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        uri = "uri116076"
        expected_response = {"name": name_2, "uri": uri}
        expected_response = product_search_service_pb2.ReferenceImage(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        name = client.reference_image_path(
            "[PROJECT]", "[LOCATION]", "[PRODUCT]", "[REFERENCE_IMAGE]"
        )

        response = client.get_reference_image(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.GetReferenceImageRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_reference_image_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        name = client.reference_image_path(
            "[PROJECT]", "[LOCATION]", "[PRODUCT]", "[REFERENCE_IMAGE]"
        )

        with pytest.raises(CustomException):
            client.get_reference_image(name)

    def test_add_product_to_product_set(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")
        product = "product-309474065"

        client.add_product_to_product_set(name, product)

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.AddProductToProductSetRequest(
            name=name, product=product
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_add_product_to_product_set_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")
        product = "product-309474065"

        with pytest.raises(CustomException):
            client.add_product_to_product_set(name, product)

    def test_remove_product_from_product_set(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")
        product = "product-309474065"

        client.remove_product_from_product_set(name, product)

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.RemoveProductFromProductSetRequest(
            name=name, product=product
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_remove_product_from_product_set_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")
        product = "product-309474065"

        with pytest.raises(CustomException):
            client.remove_product_from_product_set(name, product)

    def test_list_products_in_product_set(self):
        # Setup Expected Response
        next_page_token = ""
        products_element = {}
        products = [products_element]
        expected_response = {"next_page_token": next_page_token, "products": products}
        expected_response = product_search_service_pb2.ListProductsInProductSetResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")

        paged_list_response = client.list_products_in_product_set(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.products[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.ListProductsInProductSetRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_products_in_product_set_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup request
        name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")

        paged_list_response = client.list_products_in_product_set(name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_import_product_sets(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = product_search_service_pb2.ImportProductSetsResponse(
            **expected_response
        )
        operation = operations_pb2.Operation(
            name="operations/test_import_product_sets", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        input_config = {}

        response = client.import_product_sets(parent, input_config)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = product_search_service_pb2.ImportProductSetsRequest(
            parent=parent, input_config=input_config
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_import_product_sets_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_import_product_sets_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = vision_v1p3beta1.ProductSearchClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        input_config = {}

        response = client.import_product_sets(parent, input_config)
        exception = response.exception()
        assert exception.errors[0] == error
