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
from google.oauth2 import service_account
from google.protobuf import any_pb2 as any  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore
from grafeas.grafeas_v1.services.grafeas import GrafeasAsyncClient
from grafeas.grafeas_v1.services.grafeas import GrafeasClient
from grafeas.grafeas_v1.services.grafeas import pagers
from grafeas.grafeas_v1.services.grafeas import transports
from grafeas.grafeas_v1.types import attestation
from grafeas.grafeas_v1.types import build
from grafeas.grafeas_v1.types import common
from grafeas.grafeas_v1.types import cvss
from grafeas.grafeas_v1.types import deployment
from grafeas.grafeas_v1.types import discovery
from grafeas.grafeas_v1.types import grafeas
from grafeas.grafeas_v1.types import image
from grafeas.grafeas_v1.types import package
from grafeas.grafeas_v1.types import package as g_package
from grafeas.grafeas_v1.types import provenance
from grafeas.grafeas_v1.types import provenance as g_provenance
from grafeas.grafeas_v1.types import upgrade
from grafeas.grafeas_v1.types import vulnerability


def test_get_occurrence(
    transport: str = "grpc", request_type=grafeas.GetOccurrenceRequest
):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_occurrence), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence(
            name="name_value",
            resource_uri="resource_uri_value",
            note_name="note_name_value",
            kind=common.NoteKind.VULNERABILITY,
            remediation="remediation_value",
            vulnerability=vulnerability.VulnerabilityOccurrence(type="type_value"),
        )

        response = client.get_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.GetOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)

    assert response.name == "name_value"

    assert response.resource_uri == "resource_uri_value"

    assert response.note_name == "note_name_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.remediation == "remediation_value"


def test_get_occurrence_from_dict():
    test_get_occurrence(request_type=dict)


@pytest.mark.asyncio
async def test_get_occurrence_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.GetOccurrenceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.Occurrence(
                name="name_value",
                resource_uri="resource_uri_value",
                note_name="note_name_value",
                kind=common.NoteKind.VULNERABILITY,
                remediation="remediation_value",
            )
        )

        response = await client.get_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)

    assert response.name == "name_value"

    assert response.resource_uri == "resource_uri_value"

    assert response.note_name == "note_name_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.remediation == "remediation_value"


def test_get_occurrence_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_occurrence), "__call__") as call:
        call.return_value = grafeas.Occurrence()

        client.get_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_occurrence_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_occurrence), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())

        await client.get_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_occurrence_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_occurrence), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_occurrence(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_occurrence_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_occurrence(
            grafeas.GetOccurrenceRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_occurrence_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_occurrence(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_occurrence_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_occurrence(
            grafeas.GetOccurrenceRequest(), name="name_value",
        )


def test_list_occurrences(
    transport: str = "grpc", request_type=grafeas.ListOccurrencesRequest
):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListOccurrencesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.ListOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOccurrencesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_occurrences_from_dict():
    test_list_occurrences(request_type=dict)


@pytest.mark.asyncio
async def test_list_occurrences_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.ListOccurrencesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListOccurrencesResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOccurrencesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_occurrences_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListOccurrencesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_occurrences), "__call__"
    ) as call:
        call.return_value = grafeas.ListOccurrencesResponse()

        client.list_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_occurrences_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListOccurrencesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_occurrences), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListOccurrencesResponse()
        )

        await client.list_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_occurrences_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListOccurrencesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_occurrences(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_list_occurrences_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_occurrences(
            grafeas.ListOccurrencesRequest(),
            parent="parent_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_occurrences_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListOccurrencesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListOccurrencesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_occurrences(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_occurrences_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_occurrences(
            grafeas.ListOccurrencesRequest(),
            parent="parent_value",
            filter="filter_value",
        )


def test_list_occurrences_pager():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_occurrences), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token="abc",
            ),
            grafeas.ListOccurrencesResponse(occurrences=[], next_page_token="def",),
            grafeas.ListOccurrencesResponse(
                occurrences=[grafeas.Occurrence(),], next_page_token="ghi",
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[grafeas.Occurrence(), grafeas.Occurrence(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_occurrences(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, grafeas.Occurrence) for i in results)


def test_list_occurrences_pages():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_occurrences), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token="abc",
            ),
            grafeas.ListOccurrencesResponse(occurrences=[], next_page_token="def",),
            grafeas.ListOccurrencesResponse(
                occurrences=[grafeas.Occurrence(),], next_page_token="ghi",
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[grafeas.Occurrence(), grafeas.Occurrence(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_occurrences(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_occurrences_async_pager():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_occurrences),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token="abc",
            ),
            grafeas.ListOccurrencesResponse(occurrences=[], next_page_token="def",),
            grafeas.ListOccurrencesResponse(
                occurrences=[grafeas.Occurrence(),], next_page_token="ghi",
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[grafeas.Occurrence(), grafeas.Occurrence(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_occurrences(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, grafeas.Occurrence) for i in responses)


@pytest.mark.asyncio
async def test_list_occurrences_async_pages():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_occurrences),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token="abc",
            ),
            grafeas.ListOccurrencesResponse(occurrences=[], next_page_token="def",),
            grafeas.ListOccurrencesResponse(
                occurrences=[grafeas.Occurrence(),], next_page_token="ghi",
            ),
            grafeas.ListOccurrencesResponse(
                occurrences=[grafeas.Occurrence(), grafeas.Occurrence(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_occurrences(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_delete_occurrence(
    transport: str = "grpc", request_type=grafeas.DeleteOccurrenceRequest
):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.DeleteOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_occurrence_from_dict():
    test_delete_occurrence(request_type=dict)


@pytest.mark.asyncio
async def test_delete_occurrence_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.DeleteOccurrenceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_occurrence_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteOccurrenceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_occurrence), "__call__"
    ) as call:
        call.return_value = None

        client.delete_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_occurrence_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteOccurrenceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_occurrence), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_occurrence_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_occurrence(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_occurrence_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_occurrence(
            grafeas.DeleteOccurrenceRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_occurrence_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_occurrence(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_occurrence_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_occurrence(
            grafeas.DeleteOccurrenceRequest(), name="name_value",
        )


def test_create_occurrence(
    transport: str = "grpc", request_type=grafeas.CreateOccurrenceRequest
):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence(
            name="name_value",
            resource_uri="resource_uri_value",
            note_name="note_name_value",
            kind=common.NoteKind.VULNERABILITY,
            remediation="remediation_value",
            vulnerability=vulnerability.VulnerabilityOccurrence(type="type_value"),
        )

        response = client.create_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.CreateOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)

    assert response.name == "name_value"

    assert response.resource_uri == "resource_uri_value"

    assert response.note_name == "note_name_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.remediation == "remediation_value"


def test_create_occurrence_from_dict():
    test_create_occurrence(request_type=dict)


@pytest.mark.asyncio
async def test_create_occurrence_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.CreateOccurrenceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.Occurrence(
                name="name_value",
                resource_uri="resource_uri_value",
                note_name="note_name_value",
                kind=common.NoteKind.VULNERABILITY,
                remediation="remediation_value",
            )
        )

        response = await client.create_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)

    assert response.name == "name_value"

    assert response.resource_uri == "resource_uri_value"

    assert response.note_name == "note_name_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.remediation == "remediation_value"


def test_create_occurrence_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateOccurrenceRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_occurrence), "__call__"
    ) as call:
        call.return_value = grafeas.Occurrence()

        client.create_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_occurrence_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateOccurrenceRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_occurrence), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())

        await client.create_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_occurrence_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_occurrence(
            parent="parent_value", occurrence=grafeas.Occurrence(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].occurrence == grafeas.Occurrence(name="name_value")


def test_create_occurrence_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_occurrence(
            grafeas.CreateOccurrenceRequest(),
            parent="parent_value",
            occurrence=grafeas.Occurrence(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_occurrence_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_occurrence(
            parent="parent_value", occurrence=grafeas.Occurrence(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].occurrence == grafeas.Occurrence(name="name_value")


@pytest.mark.asyncio
async def test_create_occurrence_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_occurrence(
            grafeas.CreateOccurrenceRequest(),
            parent="parent_value",
            occurrence=grafeas.Occurrence(name="name_value"),
        )


def test_batch_create_occurrences(
    transport: str = "grpc", request_type=grafeas.BatchCreateOccurrencesRequest
):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateOccurrencesResponse()

        response = client.batch_create_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.BatchCreateOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateOccurrencesResponse)


def test_batch_create_occurrences_from_dict():
    test_batch_create_occurrences(request_type=dict)


@pytest.mark.asyncio
async def test_batch_create_occurrences_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.BatchCreateOccurrencesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.BatchCreateOccurrencesResponse()
        )

        response = await client.batch_create_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateOccurrencesResponse)


def test_batch_create_occurrences_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateOccurrencesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_occurrences), "__call__"
    ) as call:
        call.return_value = grafeas.BatchCreateOccurrencesResponse()

        client.batch_create_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_create_occurrences_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateOccurrencesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_occurrences), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.BatchCreateOccurrencesResponse()
        )

        await client.batch_create_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_batch_create_occurrences_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateOccurrencesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_create_occurrences(
            parent="parent_value", occurrences=[grafeas.Occurrence(name="name_value")],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].occurrences == [grafeas.Occurrence(name="name_value")]


def test_batch_create_occurrences_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_occurrences(
            grafeas.BatchCreateOccurrencesRequest(),
            parent="parent_value",
            occurrences=[grafeas.Occurrence(name="name_value")],
        )


@pytest.mark.asyncio
async def test_batch_create_occurrences_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateOccurrencesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.BatchCreateOccurrencesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_create_occurrences(
            parent="parent_value", occurrences=[grafeas.Occurrence(name="name_value")],
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].occurrences == [grafeas.Occurrence(name="name_value")]


@pytest.mark.asyncio
async def test_batch_create_occurrences_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_create_occurrences(
            grafeas.BatchCreateOccurrencesRequest(),
            parent="parent_value",
            occurrences=[grafeas.Occurrence(name="name_value")],
        )


def test_update_occurrence(
    transport: str = "grpc", request_type=grafeas.UpdateOccurrenceRequest
):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence(
            name="name_value",
            resource_uri="resource_uri_value",
            note_name="note_name_value",
            kind=common.NoteKind.VULNERABILITY,
            remediation="remediation_value",
            vulnerability=vulnerability.VulnerabilityOccurrence(type="type_value"),
        )

        response = client.update_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.UpdateOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)

    assert response.name == "name_value"

    assert response.resource_uri == "resource_uri_value"

    assert response.note_name == "note_name_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.remediation == "remediation_value"


def test_update_occurrence_from_dict():
    test_update_occurrence(request_type=dict)


@pytest.mark.asyncio
async def test_update_occurrence_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.UpdateOccurrenceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.Occurrence(
                name="name_value",
                resource_uri="resource_uri_value",
                note_name="note_name_value",
                kind=common.NoteKind.VULNERABILITY,
                remediation="remediation_value",
            )
        )

        response = await client.update_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)

    assert response.name == "name_value"

    assert response.resource_uri == "resource_uri_value"

    assert response.note_name == "note_name_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.remediation == "remediation_value"


def test_update_occurrence_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateOccurrenceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_occurrence), "__call__"
    ) as call:
        call.return_value = grafeas.Occurrence()

        client.update_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_occurrence_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateOccurrenceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_occurrence), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())

        await client.update_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_occurrence_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_occurrence(
            name="name_value",
            occurrence=grafeas.Occurrence(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].occurrence == grafeas.Occurrence(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_occurrence_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_occurrence(
            grafeas.UpdateOccurrenceRequest(),
            name="name_value",
            occurrence=grafeas.Occurrence(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_occurrence_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_occurrence(
            name="name_value",
            occurrence=grafeas.Occurrence(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].occurrence == grafeas.Occurrence(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_occurrence_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_occurrence(
            grafeas.UpdateOccurrenceRequest(),
            name="name_value",
            occurrence=grafeas.Occurrence(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_get_occurrence_note(
    transport: str = "grpc", request_type=grafeas.GetOccurrenceNoteRequest
):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_occurrence_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note(
            name="name_value",
            short_description="short_description_value",
            long_description="long_description_value",
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=["related_note_names_value"],
            vulnerability=vulnerability.VulnerabilityNote(cvss_score=0.1082),
        )

        response = client.get_occurrence_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.GetOccurrenceNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)

    assert response.name == "name_value"

    assert response.short_description == "short_description_value"

    assert response.long_description == "long_description_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.related_note_names == ["related_note_names_value"]


def test_get_occurrence_note_from_dict():
    test_get_occurrence_note(request_type=dict)


@pytest.mark.asyncio
async def test_get_occurrence_note_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.GetOccurrenceNoteRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_occurrence_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.Note(
                name="name_value",
                short_description="short_description_value",
                long_description="long_description_value",
                kind=common.NoteKind.VULNERABILITY,
                related_note_names=["related_note_names_value"],
            )
        )

        response = await client.get_occurrence_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)

    assert response.name == "name_value"

    assert response.short_description == "short_description_value"

    assert response.long_description == "long_description_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.related_note_names == ["related_note_names_value"]


def test_get_occurrence_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceNoteRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_occurrence_note), "__call__"
    ) as call:
        call.return_value = grafeas.Note()

        client.get_occurrence_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_occurrence_note_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceNoteRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_occurrence_note), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())

        await client.get_occurrence_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_occurrence_note_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_occurrence_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_occurrence_note(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_occurrence_note_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_occurrence_note(
            grafeas.GetOccurrenceNoteRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_occurrence_note_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_occurrence_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_occurrence_note(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_occurrence_note_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_occurrence_note(
            grafeas.GetOccurrenceNoteRequest(), name="name_value",
        )


def test_get_note(transport: str = "grpc", request_type=grafeas.GetNoteRequest):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note(
            name="name_value",
            short_description="short_description_value",
            long_description="long_description_value",
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=["related_note_names_value"],
            vulnerability=vulnerability.VulnerabilityNote(cvss_score=0.1082),
        )

        response = client.get_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.GetNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)

    assert response.name == "name_value"

    assert response.short_description == "short_description_value"

    assert response.long_description == "long_description_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.related_note_names == ["related_note_names_value"]


def test_get_note_from_dict():
    test_get_note(request_type=dict)


@pytest.mark.asyncio
async def test_get_note_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.GetNoteRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.Note(
                name="name_value",
                short_description="short_description_value",
                long_description="long_description_value",
                kind=common.NoteKind.VULNERABILITY,
                related_note_names=["related_note_names_value"],
            )
        )

        response = await client.get_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)

    assert response.name == "name_value"

    assert response.short_description == "short_description_value"

    assert response.long_description == "long_description_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.related_note_names == ["related_note_names_value"]


def test_get_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetNoteRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_note), "__call__") as call:
        call.return_value = grafeas.Note()

        client.get_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_note_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetNoteRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_note), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())

        await client.get_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_note_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_note(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_note_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_note(
            grafeas.GetNoteRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_note_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.get_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_note(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_note_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_note(
            grafeas.GetNoteRequest(), name="name_value",
        )


def test_list_notes(transport: str = "grpc", request_type=grafeas.ListNotesRequest):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_notes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNotesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.ListNotesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_notes_from_dict():
    test_list_notes(request_type=dict)


@pytest.mark.asyncio
async def test_list_notes_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.ListNotesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_notes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListNotesResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_notes_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNotesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_notes), "__call__") as call:
        call.return_value = grafeas.ListNotesResponse()

        client.list_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_notes_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNotesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_notes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListNotesResponse()
        )

        await client.list_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_notes_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_notes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNotesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_notes(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


def test_list_notes_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_notes(
            grafeas.ListNotesRequest(), parent="parent_value", filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_notes_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_notes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNotesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListNotesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_notes(
            parent="parent_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_notes_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_notes(
            grafeas.ListNotesRequest(), parent="parent_value", filter="filter_value",
        )


def test_list_notes_pager():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_notes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNotesResponse(
                notes=[grafeas.Note(), grafeas.Note(), grafeas.Note(),],
                next_page_token="abc",
            ),
            grafeas.ListNotesResponse(notes=[], next_page_token="def",),
            grafeas.ListNotesResponse(notes=[grafeas.Note(),], next_page_token="ghi",),
            grafeas.ListNotesResponse(notes=[grafeas.Note(), grafeas.Note(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_notes(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, grafeas.Note) for i in results)


def test_list_notes_pages():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_notes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNotesResponse(
                notes=[grafeas.Note(), grafeas.Note(), grafeas.Note(),],
                next_page_token="abc",
            ),
            grafeas.ListNotesResponse(notes=[], next_page_token="def",),
            grafeas.ListNotesResponse(notes=[grafeas.Note(),], next_page_token="ghi",),
            grafeas.ListNotesResponse(notes=[grafeas.Note(), grafeas.Note(),],),
            RuntimeError,
        )
        pages = list(client.list_notes(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_notes_async_pager():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_notes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNotesResponse(
                notes=[grafeas.Note(), grafeas.Note(), grafeas.Note(),],
                next_page_token="abc",
            ),
            grafeas.ListNotesResponse(notes=[], next_page_token="def",),
            grafeas.ListNotesResponse(notes=[grafeas.Note(),], next_page_token="ghi",),
            grafeas.ListNotesResponse(notes=[grafeas.Note(), grafeas.Note(),],),
            RuntimeError,
        )
        async_pager = await client.list_notes(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, grafeas.Note) for i in responses)


@pytest.mark.asyncio
async def test_list_notes_async_pages():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_notes),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNotesResponse(
                notes=[grafeas.Note(), grafeas.Note(), grafeas.Note(),],
                next_page_token="abc",
            ),
            grafeas.ListNotesResponse(notes=[], next_page_token="def",),
            grafeas.ListNotesResponse(notes=[grafeas.Note(),], next_page_token="ghi",),
            grafeas.ListNotesResponse(notes=[grafeas.Note(), grafeas.Note(),],),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_notes(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_delete_note(transport: str = "grpc", request_type=grafeas.DeleteNoteRequest):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.DeleteNoteRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_note_from_dict():
    test_delete_note(request_type=dict)


@pytest.mark.asyncio
async def test_delete_note_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.DeleteNoteRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteNoteRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_note), "__call__") as call:
        call.return_value = None

        client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_note_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteNoteRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_note), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_note_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_note(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_note_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_note(
            grafeas.DeleteNoteRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_note_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_note(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_note_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_note(
            grafeas.DeleteNoteRequest(), name="name_value",
        )


def test_create_note(transport: str = "grpc", request_type=grafeas.CreateNoteRequest):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note(
            name="name_value",
            short_description="short_description_value",
            long_description="long_description_value",
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=["related_note_names_value"],
            vulnerability=vulnerability.VulnerabilityNote(cvss_score=0.1082),
        )

        response = client.create_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.CreateNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)

    assert response.name == "name_value"

    assert response.short_description == "short_description_value"

    assert response.long_description == "long_description_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.related_note_names == ["related_note_names_value"]


def test_create_note_from_dict():
    test_create_note(request_type=dict)


@pytest.mark.asyncio
async def test_create_note_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.CreateNoteRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.Note(
                name="name_value",
                short_description="short_description_value",
                long_description="long_description_value",
                kind=common.NoteKind.VULNERABILITY,
                related_note_names=["related_note_names_value"],
            )
        )

        response = await client.create_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)

    assert response.name == "name_value"

    assert response.short_description == "short_description_value"

    assert response.long_description == "long_description_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.related_note_names == ["related_note_names_value"]


def test_create_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateNoteRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_note), "__call__") as call:
        call.return_value = grafeas.Note()

        client.create_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_note_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateNoteRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_note), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())

        await client.create_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_note_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_note(
            parent="parent_value",
            note_id="note_id_value",
            note=grafeas.Note(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].note_id == "note_id_value"

        assert args[0].note == grafeas.Note(name="name_value")


def test_create_note_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_note(
            grafeas.CreateNoteRequest(),
            parent="parent_value",
            note_id="note_id_value",
            note=grafeas.Note(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_note_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.create_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_note(
            parent="parent_value",
            note_id="note_id_value",
            note=grafeas.Note(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].note_id == "note_id_value"

        assert args[0].note == grafeas.Note(name="name_value")


@pytest.mark.asyncio
async def test_create_note_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_note(
            grafeas.CreateNoteRequest(),
            parent="parent_value",
            note_id="note_id_value",
            note=grafeas.Note(name="name_value"),
        )


def test_batch_create_notes(
    transport: str = "grpc", request_type=grafeas.BatchCreateNotesRequest
):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_notes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateNotesResponse()

        response = client.batch_create_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.BatchCreateNotesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateNotesResponse)


def test_batch_create_notes_from_dict():
    test_batch_create_notes(request_type=dict)


@pytest.mark.asyncio
async def test_batch_create_notes_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.BatchCreateNotesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_notes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.BatchCreateNotesResponse()
        )

        response = await client.batch_create_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateNotesResponse)


def test_batch_create_notes_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateNotesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_notes), "__call__"
    ) as call:
        call.return_value = grafeas.BatchCreateNotesResponse()

        client.batch_create_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_batch_create_notes_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateNotesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_notes), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.BatchCreateNotesResponse()
        )

        await client.batch_create_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_batch_create_notes_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.batch_create_notes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateNotesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.batch_create_notes(
            parent="parent_value", notes={"key_value": grafeas.Note(name="name_value")},
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].notes == {"key_value": grafeas.Note(name="name_value")}


def test_batch_create_notes_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.batch_create_notes(
            grafeas.BatchCreateNotesRequest(),
            parent="parent_value",
            notes={"key_value": grafeas.Note(name="name_value")},
        )


@pytest.mark.asyncio
async def test_batch_create_notes_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.batch_create_notes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.BatchCreateNotesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.BatchCreateNotesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.batch_create_notes(
            parent="parent_value", notes={"key_value": grafeas.Note(name="name_value")},
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].notes == {"key_value": grafeas.Note(name="name_value")}


@pytest.mark.asyncio
async def test_batch_create_notes_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.batch_create_notes(
            grafeas.BatchCreateNotesRequest(),
            parent="parent_value",
            notes={"key_value": grafeas.Note(name="name_value")},
        )


def test_update_note(transport: str = "grpc", request_type=grafeas.UpdateNoteRequest):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note(
            name="name_value",
            short_description="short_description_value",
            long_description="long_description_value",
            kind=common.NoteKind.VULNERABILITY,
            related_note_names=["related_note_names_value"],
            vulnerability=vulnerability.VulnerabilityNote(cvss_score=0.1082),
        )

        response = client.update_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.UpdateNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)

    assert response.name == "name_value"

    assert response.short_description == "short_description_value"

    assert response.long_description == "long_description_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.related_note_names == ["related_note_names_value"]


def test_update_note_from_dict():
    test_update_note(request_type=dict)


@pytest.mark.asyncio
async def test_update_note_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.UpdateNoteRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.Note(
                name="name_value",
                short_description="short_description_value",
                long_description="long_description_value",
                kind=common.NoteKind.VULNERABILITY,
                related_note_names=["related_note_names_value"],
            )
        )

        response = await client.update_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)

    assert response.name == "name_value"

    assert response.short_description == "short_description_value"

    assert response.long_description == "long_description_value"

    assert response.kind == common.NoteKind.VULNERABILITY

    assert response.related_note_names == ["related_note_names_value"]


def test_update_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateNoteRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_note), "__call__") as call:
        call.return_value = grafeas.Note()

        client.update_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_note_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateNoteRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_note), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())

        await client.update_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_note_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_note(
            name="name_value",
            note=grafeas.Note(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].note == grafeas.Note(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_note_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_note(
            grafeas.UpdateNoteRequest(),
            name="name_value",
            note=grafeas.Note(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_note_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.update_note), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_note(
            name="name_value",
            note=grafeas.Note(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].note == grafeas.Note(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_note_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_note(
            grafeas.UpdateNoteRequest(),
            name="name_value",
            note=grafeas.Note(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_list_note_occurrences(
    transport: str = "grpc", request_type=grafeas.ListNoteOccurrencesRequest
):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_note_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNoteOccurrencesResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_note_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == grafeas.ListNoteOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNoteOccurrencesPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_note_occurrences_from_dict():
    test_list_note_occurrences(request_type=dict)


@pytest.mark.asyncio
async def test_list_note_occurrences_async(transport: str = "grpc_asyncio"):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = grafeas.ListNoteOccurrencesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_note_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListNoteOccurrencesResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_note_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNoteOccurrencesAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_note_occurrences_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNoteOccurrencesRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_note_occurrences), "__call__"
    ) as call:
        call.return_value = grafeas.ListNoteOccurrencesResponse()

        client.list_note_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_note_occurrences_field_headers_async():
    client = GrafeasAsyncClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNoteOccurrencesRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_note_occurrences), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListNoteOccurrencesResponse()
        )

        await client.list_note_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_list_note_occurrences_flattened():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_note_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNoteOccurrencesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_note_occurrences(
            name="name_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].filter == "filter_value"


def test_list_note_occurrences_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_note_occurrences(
            grafeas.ListNoteOccurrencesRequest(),
            name="name_value",
            filter="filter_value",
        )


@pytest.mark.asyncio
async def test_list_note_occurrences_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_note_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.ListNoteOccurrencesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListNoteOccurrencesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_note_occurrences(
            name="name_value", filter="filter_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"

        assert args[0].filter == "filter_value"


@pytest.mark.asyncio
async def test_list_note_occurrences_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_note_occurrences(
            grafeas.ListNoteOccurrencesRequest(),
            name="name_value",
            filter="filter_value",
        )


def test_list_note_occurrences_pager():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_note_occurrences), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token="abc",
            ),
            grafeas.ListNoteOccurrencesResponse(occurrences=[], next_page_token="def",),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[grafeas.Occurrence(),], next_page_token="ghi",
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[grafeas.Occurrence(), grafeas.Occurrence(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_note_occurrences(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, grafeas.Occurrence) for i in results)


def test_list_note_occurrences_pages():
    client = GrafeasClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_note_occurrences), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token="abc",
            ),
            grafeas.ListNoteOccurrencesResponse(occurrences=[], next_page_token="def",),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[grafeas.Occurrence(),], next_page_token="ghi",
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[grafeas.Occurrence(), grafeas.Occurrence(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_note_occurrences(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_note_occurrences_async_pager():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_note_occurrences),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token="abc",
            ),
            grafeas.ListNoteOccurrencesResponse(occurrences=[], next_page_token="def",),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[grafeas.Occurrence(),], next_page_token="ghi",
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[grafeas.Occurrence(), grafeas.Occurrence(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_note_occurrences(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, grafeas.Occurrence) for i in responses)


@pytest.mark.asyncio
async def test_list_note_occurrences_async_pages():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_note_occurrences),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                    grafeas.Occurrence(),
                ],
                next_page_token="abc",
            ),
            grafeas.ListNoteOccurrencesResponse(occurrences=[], next_page_token="def",),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[grafeas.Occurrence(),], next_page_token="ghi",
            ),
            grafeas.ListNoteOccurrencesResponse(
                occurrences=[grafeas.Occurrence(), grafeas.Occurrence(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page in (await client.list_note_occurrences(request={})).pages:
            pages.append(page)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.GrafeasGrpcTransport()
    client = GrafeasClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.GrafeasGrpcTransport()
    channel = transport.grpc_channel
    assert channel

    transport = transports.GrafeasGrpcAsyncIOTransport()
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = GrafeasClient()
    assert isinstance(client._transport, transports.GrafeasGrpcTransport,)


def test_grafeas_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "grafeas.grafeas_v1.services.grafeas.transports.GrafeasTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.GrafeasTransport()

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_occurrence",
        "list_occurrences",
        "delete_occurrence",
        "create_occurrence",
        "batch_create_occurrences",
        "update_occurrence",
        "get_occurrence_note",
        "get_note",
        "list_notes",
        "delete_note",
        "create_note",
        "batch_create_notes",
        "update_note",
        "list_note_occurrences",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_grafeas_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "grafeas.grafeas_v1.services.grafeas.transports.GrafeasTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.GrafeasTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json", scopes=(), quota_project_id="octopus",
        )


def test_grafeas_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        GrafeasClient()
        adc.assert_called_once_with(
            scopes=(), quota_project_id=None,
        )


def test_grafeas_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.GrafeasGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(), quota_project_id="octopus",
        )


def test_grafeas_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.GrafeasGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_grafeas_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.GrafeasGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_occurrence_path():
    project = "squid"
    occurrence = "clam"

    expected = "projects/{project}/occurrences/{occurrence}".format(
        project=project, occurrence=occurrence,
    )
    actual = GrafeasClient.occurrence_path(project, occurrence)
    assert expected == actual


def test_parse_occurrence_path():
    expected = {
        "project": "whelk",
        "occurrence": "octopus",
    }
    path = GrafeasClient.occurrence_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_occurrence_path(path)
    assert expected == actual


def test_note_path():
    project = "squid"
    note = "clam"

    expected = "projects/{project}/notes/{note}".format(project=project, note=note,)
    actual = GrafeasClient.note_path(project, note)
    assert expected == actual


def test_parse_note_path():
    expected = {
        "project": "whelk",
        "note": "octopus",
    }
    path = GrafeasClient.note_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_note_path(path)
    assert expected == actual
