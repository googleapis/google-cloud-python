# -*- coding: utf-8 -*-
from unittest import mock

import grpc

import pytest

from google import auth
from google.api_core import future
from google.api_core import operation
from google.api_core import operations_v1
from google.auth import credentials
from google.cloud.vision_v1.services.product_search import ProductSearch
from google.cloud.vision_v1.services.product_search import pagers
from google.cloud.vision_v1.services.product_search import transports
from google.cloud.vision_v1.types import product_search_service
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2 as empty  # type: ignore


def test_create_product_set(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.CreateProductSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ProductSet(
            name="name_value", display_name="display_name_value"
        )
        response = client.create_product_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, product_search_service.ProductSet)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_list_product_sets(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.ListProductSetsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_product_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ListProductSetsResponse(
            next_page_token="next_page_token_value"
        )
        response = client.list_product_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProductSetsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_product_sets_field_headers():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_search_service.ListProductSetsRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_product_sets), "__call__"
    ) as call:
        call.return_value = product_search_service.ListProductSetsResponse()
        response = client.list_product_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_product_sets_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_product_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ListProductSetsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_product_sets(parent="parent_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_product_sets_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_product_sets(
            product_search_service.ListProductSetsRequest(), parent="parent_value"
        )


def test_list_product_sets_pager():
    client = ProductSearch(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_product_sets), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            product_search_service.ListProductSetsResponse(
                product_sets=[
                    product_search_service.ProductSet(),
                    product_search_service.ProductSet(),
                    product_search_service.ProductSet(),
                ],
                next_page_token="abc",
            ),
            product_search_service.ListProductSetsResponse(
                product_sets=[], next_page_token="def"
            ),
            product_search_service.ListProductSetsResponse(
                product_sets=[product_search_service.ProductSet()],
                next_page_token="ghi",
            ),
            product_search_service.ListProductSetsResponse(
                product_sets=[
                    product_search_service.ProductSet(),
                    product_search_service.ProductSet(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_product_sets(request={})]
        assert len(results) == 6
        assert all([isinstance(i, product_search_service.ProductSet) for i in results])


def test_get_product_set(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.GetProductSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_product_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ProductSet(
            name="name_value", display_name="display_name_value"
        )
        response = client.get_product_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, product_search_service.ProductSet)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_get_product_set_field_headers():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_search_service.GetProductSetRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_product_set), "__call__") as call:
        call.return_value = product_search_service.ProductSet()
        response = client.get_product_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_product_set_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_product_set), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ProductSet()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_product_set(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_product_set_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_product_set(
            product_search_service.GetProductSetRequest(), name="name_value"
        )


def test_update_product_set(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.UpdateProductSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ProductSet(
            name="name_value", display_name="display_name_value"
        )
        response = client.update_product_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, product_search_service.ProductSet)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"


def test_delete_product_set(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.DeleteProductSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_product_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_product_set_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_product_set(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_product_set_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_product_set(
            product_search_service.DeleteProductSetRequest(), name="name_value"
        )


def test_create_product(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.CreateProductRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.Product(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            product_category="product_category_value",
        )
        response = client.create_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, product_search_service.Product)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.product_category == "product_category_value"


def test_list_products(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.ListProductsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ListProductsResponse(
            next_page_token="next_page_token_value"
        )
        response = client.list_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProductsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_products_field_headers():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_search_service.ListProductsRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_products), "__call__") as call:
        call.return_value = product_search_service.ListProductsResponse()
        response = client.list_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_products_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ListProductsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_products(parent="parent_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_products_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_products(
            product_search_service.ListProductsRequest(), parent="parent_value"
        )


def test_list_products_pager():
    client = ProductSearch(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_products), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            product_search_service.ListProductsResponse(
                products=[
                    product_search_service.Product(),
                    product_search_service.Product(),
                    product_search_service.Product(),
                ],
                next_page_token="abc",
            ),
            product_search_service.ListProductsResponse(
                products=[], next_page_token="def"
            ),
            product_search_service.ListProductsResponse(
                products=[product_search_service.Product()], next_page_token="ghi"
            ),
            product_search_service.ListProductsResponse(
                products=[
                    product_search_service.Product(),
                    product_search_service.Product(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_products(request={})]
        assert len(results) == 6
        assert all([isinstance(i, product_search_service.Product) for i in results])


def test_get_product(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.GetProductRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.Product(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            product_category="product_category_value",
        )
        response = client.get_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, product_search_service.Product)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.product_category == "product_category_value"


def test_get_product_field_headers():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_search_service.GetProductRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_product), "__call__") as call:
        call.return_value = product_search_service.Product()
        response = client.get_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_product_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.Product()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_product(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_product_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_product(
            product_search_service.GetProductRequest(), name="name_value"
        )


def test_update_product(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.UpdateProductRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.Product(
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            product_category="product_category_value",
        )
        response = client.update_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, product_search_service.Product)
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert response.product_category == "product_category_value"


def test_delete_product(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.DeleteProductRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_product(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_product_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_product), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_product(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_product_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_product(
            product_search_service.DeleteProductRequest(), name="name_value"
        )


def test_create_reference_image(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.CreateReferenceImageRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_reference_image), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ReferenceImage(
            name="name_value", uri="uri_value"
        )
        response = client.create_reference_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, product_search_service.ReferenceImage)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


def test_delete_reference_image(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.DeleteReferenceImageRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_reference_image), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_reference_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_reference_image_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_reference_image), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.delete_reference_image(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_reference_image_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_reference_image(
            product_search_service.DeleteReferenceImageRequest(), name="name_value"
        )


def test_list_reference_images(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.ListReferenceImagesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_reference_images), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ListReferenceImagesResponse(
            page_size=951, next_page_token="next_page_token_value"
        )
        response = client.list_reference_images(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListReferenceImagesPager)
    assert response.page_size == 951
    assert response.next_page_token == "next_page_token_value"


def test_list_reference_images_field_headers():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_search_service.ListReferenceImagesRequest(parent="parent/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_reference_images), "__call__"
    ) as call:
        call.return_value = product_search_service.ListReferenceImagesResponse()
        response = client.list_reference_images(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_reference_images_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_reference_images), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ListReferenceImagesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_reference_images(parent="parent_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_reference_images_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_reference_images(
            product_search_service.ListReferenceImagesRequest(), parent="parent_value"
        )


def test_list_reference_images_pager():
    client = ProductSearch(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_reference_images), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            product_search_service.ListReferenceImagesResponse(
                reference_images=[
                    product_search_service.ReferenceImage(),
                    product_search_service.ReferenceImage(),
                    product_search_service.ReferenceImage(),
                ],
                next_page_token="abc",
            ),
            product_search_service.ListReferenceImagesResponse(
                reference_images=[], next_page_token="def"
            ),
            product_search_service.ListReferenceImagesResponse(
                reference_images=[product_search_service.ReferenceImage()],
                next_page_token="ghi",
            ),
            product_search_service.ListReferenceImagesResponse(
                reference_images=[
                    product_search_service.ReferenceImage(),
                    product_search_service.ReferenceImage(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_reference_images(request={})]
        assert len(results) == 6
        assert all(
            [isinstance(i, product_search_service.ReferenceImage) for i in results]
        )


def test_get_reference_image(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.GetReferenceImageRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_reference_image), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ReferenceImage(
            name="name_value", uri="uri_value"
        )
        response = client.get_reference_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, product_search_service.ReferenceImage)
    assert response.name == "name_value"
    assert response.uri == "uri_value"


def test_get_reference_image_field_headers():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_search_service.GetReferenceImageRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_reference_image), "__call__"
    ) as call:
        call.return_value = product_search_service.ReferenceImage()
        response = client.get_reference_image(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_add_product_to_product_set(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.AddProductToProductSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.add_product_to_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.add_product_to_product_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_add_product_to_product_set_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.add_product_to_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.add_product_to_product_set(
            name="name_value", product="product_value"
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].product == "product_value"


def test_add_product_to_product_set_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.add_product_to_product_set(
            product_search_service.AddProductToProductSetRequest(),
            name="name_value",
            product="product_value",
        )


def test_remove_product_from_product_set(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.RemoveProductFromProductSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.remove_product_from_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.remove_product_from_product_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_remove_product_from_product_set_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.remove_product_from_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.remove_product_from_product_set(
            name="name_value", product="product_value"
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].product == "product_value"


def test_remove_product_from_product_set_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.remove_product_from_product_set(
            product_search_service.RemoveProductFromProductSetRequest(),
            name="name_value",
            product="product_value",
        )


def test_list_products_in_product_set(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.ListProductsInProductSetRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_products_in_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ListProductsInProductSetResponse(
            next_page_token="next_page_token_value"
        )
        response = client.list_products_in_product_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProductsInProductSetPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_products_in_product_set_field_headers():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = product_search_service.ListProductsInProductSetRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_products_in_product_set), "__call__"
    ) as call:
        call.return_value = product_search_service.ListProductsInProductSetResponse()
        response = client.list_products_in_product_set(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_list_products_in_product_set_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_products_in_product_set), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = product_search_service.ListProductsInProductSetResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_products_in_product_set(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_list_products_in_product_set_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_products_in_product_set(
            product_search_service.ListProductsInProductSetRequest(), name="name_value"
        )


def test_list_products_in_product_set_pager():
    client = ProductSearch(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_products_in_product_set), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            product_search_service.ListProductsInProductSetResponse(
                products=[
                    product_search_service.Product(),
                    product_search_service.Product(),
                    product_search_service.Product(),
                ],
                next_page_token="abc",
            ),
            product_search_service.ListProductsInProductSetResponse(
                products=[], next_page_token="def"
            ),
            product_search_service.ListProductsInProductSetResponse(
                products=[product_search_service.Product()], next_page_token="ghi"
            ),
            product_search_service.ListProductsInProductSetResponse(
                products=[
                    product_search_service.Product(),
                    product_search_service.Product(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_products_in_product_set(request={})]
        assert len(results) == 6
        assert all([isinstance(i, product_search_service.Product) for i in results])


def test_import_product_sets(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.ImportProductSetsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.import_product_sets), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.import_product_sets(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_purge_products(transport: str = "grpc"):
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = product_search_service.PurgeProductsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.purge_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.purge_products(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_purge_products_flattened():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.purge_products), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.purge_products(parent="parent_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_purge_products_flattened_error():
    client = ProductSearch(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.purge_products(
            product_search_service.PurgeProductsRequest(), parent="parent_value"
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ProductSearchGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = ProductSearch(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ProductSearchGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = ProductSearch(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ProductSearch(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.ProductSearchGrpcTransport)


def test_product_search_base_transport():
    # Instantiate the base transport.
    transport = transports.ProductSearchTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_product_set",
        "list_product_sets",
        "get_product_set",
        "update_product_set",
        "delete_product_set",
        "create_product",
        "list_products",
        "get_product",
        "update_product",
        "delete_product",
        "create_reference_image",
        "delete_reference_image",
        "list_reference_images",
        "get_reference_image",
        "add_product_to_product_set",
        "remove_product_from_product_set",
        "list_products_in_product_set",
        "import_product_sets",
        "purge_products",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_product_search_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        client = ProductSearch()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-vision",
            )
        )


def test_product_search_host_no_port():
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(),
        host="vision.googleapis.com",
        transport="grpc",
    )
    assert client._transport._host == "vision.googleapis.com:443"


def test_product_search_host_with_port():
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(),
        host="vision.googleapis.com:8000",
        transport="grpc",
    )
    assert client._transport._host == "vision.googleapis.com:8000"


def test_product_search_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.ProductSearchGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel


def test_product_search_grpc_lro_client():
    client = ProductSearch(
        credentials=credentials.AnonymousCredentials(), transport="grpc"
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client
