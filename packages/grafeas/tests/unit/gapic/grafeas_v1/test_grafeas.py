# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.oauth2 import service_account
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from grafeas.grafeas_v1.services.grafeas import GrafeasAsyncClient
from grafeas.grafeas_v1.services.grafeas import GrafeasClient
from grafeas.grafeas_v1.services.grafeas import pagers
from grafeas.grafeas_v1.services.grafeas import transports
from grafeas.grafeas_v1.types import attestation
from grafeas.grafeas_v1.types import build
from grafeas.grafeas_v1.types import common
from grafeas.grafeas_v1.types import compliance
from grafeas.grafeas_v1.types import cvss
from grafeas.grafeas_v1.types import deployment
from grafeas.grafeas_v1.types import discovery
from grafeas.grafeas_v1.types import dsse_attestation
from grafeas.grafeas_v1.types import grafeas
from grafeas.grafeas_v1.types import image
from grafeas.grafeas_v1.types import intoto_provenance
from grafeas.grafeas_v1.types import intoto_statement
from grafeas.grafeas_v1.types import package
from grafeas.grafeas_v1.types import provenance
from grafeas.grafeas_v1.types import severity
from grafeas.grafeas_v1.types import slsa_provenance
from grafeas.grafeas_v1.types import upgrade
from grafeas.grafeas_v1.types import vulnerability
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


@pytest.mark.parametrize("request_type", [grafeas.GetOccurrenceRequest, dict,])
def test_get_occurrence(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_occurrence), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence(
            name="name_value",
            resource_uri="resource_uri_value",
            note_name="note_name_value",
            kind=common.NoteKind.VULNERABILITY,
            remediation="remediation_value",
            vulnerability=vulnerability.VulnerabilityOccurrence(type_="type__value"),
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


def test_get_occurrence_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_occurrence), "__call__") as call:
        client.get_occurrence()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetOccurrenceRequest()


@pytest.mark.asyncio
async def test_get_occurrence_async(
    transport: str = "grpc_asyncio", request_type=grafeas.GetOccurrenceRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_occurrence), "__call__") as call:
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
        assert args[0] == grafeas.GetOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == "name_value"
    assert response.resource_uri == "resource_uri_value"
    assert response.note_name == "note_name_value"
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == "remediation_value"


@pytest.mark.asyncio
async def test_get_occurrence_async_from_dict():
    await test_get_occurrence_async(request_type=dict)


def test_get_occurrence_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_occurrence), "__call__") as call:
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
    with mock.patch.object(type(client.transport.get_occurrence), "__call__") as call:
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
    with mock.patch.object(type(client.transport.get_occurrence), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_occurrence(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


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
    with mock.patch.object(type(client.transport.get_occurrence), "__call__") as call:
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_occurrence_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_occurrence(
            grafeas.GetOccurrenceRequest(), name="name_value",
        )


@pytest.mark.parametrize("request_type", [grafeas.ListOccurrencesRequest, dict,])
def test_list_occurrences(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_occurrences), "__call__") as call:
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


def test_list_occurrences_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_occurrences), "__call__") as call:
        client.list_occurrences()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListOccurrencesRequest()


@pytest.mark.asyncio
async def test_list_occurrences_async(
    transport: str = "grpc_asyncio", request_type=grafeas.ListOccurrencesRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_occurrences), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListOccurrencesResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListOccurrencesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_occurrences_async_from_dict():
    await test_list_occurrences_async(request_type=dict)


def test_list_occurrences_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListOccurrencesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_occurrences), "__call__") as call:
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
    with mock.patch.object(type(client.transport.list_occurrences), "__call__") as call:
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
    with mock.patch.object(type(client.transport.list_occurrences), "__call__") as call:
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


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
    with mock.patch.object(type(client.transport.list_occurrences), "__call__") as call:
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


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


def test_list_occurrences_pager(transport_name: str = "grpc"):
    client = GrafeasClient(transport=transport_name,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_occurrences), "__call__") as call:
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


def test_list_occurrences_pages(transport_name: str = "grpc"):
    client = GrafeasClient(transport=transport_name,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_occurrences), "__call__") as call:
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
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_occurrences_async_pager():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_occurrences), "__call__", new_callable=mock.AsyncMock
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
        type(client.transport.list_occurrences), "__call__", new_callable=mock.AsyncMock
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
        async for page_ in (await client.list_occurrences(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [grafeas.DeleteOccurrenceRequest, dict,])
def test_delete_occurrence(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_occurrence), "__call__"
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


def test_delete_occurrence_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_occurrence), "__call__"
    ) as call:
        client.delete_occurrence()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteOccurrenceRequest()


@pytest.mark.asyncio
async def test_delete_occurrence_async(
    transport: str = "grpc_asyncio", request_type=grafeas.DeleteOccurrenceRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_occurrence(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_occurrence_async_from_dict():
    await test_delete_occurrence_async(request_type=dict)


def test_delete_occurrence_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteOccurrenceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_occurrence), "__call__"
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
        type(client.transport.delete_occurrence), "__call__"
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
        type(client.transport.delete_occurrence), "__call__"
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


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
        type(client.transport.delete_occurrence), "__call__"
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_occurrence_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_occurrence(
            grafeas.DeleteOccurrenceRequest(), name="name_value",
        )


@pytest.mark.parametrize("request_type", [grafeas.CreateOccurrenceRequest, dict,])
def test_create_occurrence(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence(
            name="name_value",
            resource_uri="resource_uri_value",
            note_name="note_name_value",
            kind=common.NoteKind.VULNERABILITY,
            remediation="remediation_value",
            vulnerability=vulnerability.VulnerabilityOccurrence(type_="type__value"),
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


def test_create_occurrence_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_occurrence), "__call__"
    ) as call:
        client.create_occurrence()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.CreateOccurrenceRequest()


@pytest.mark.asyncio
async def test_create_occurrence_async(
    transport: str = "grpc_asyncio", request_type=grafeas.CreateOccurrenceRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_occurrence), "__call__"
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
        assert args[0] == grafeas.CreateOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == "name_value"
    assert response.resource_uri == "resource_uri_value"
    assert response.note_name == "note_name_value"
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == "remediation_value"


@pytest.mark.asyncio
async def test_create_occurrence_async_from_dict():
    await test_create_occurrence_async(request_type=dict)


def test_create_occurrence_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateOccurrenceRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_occurrence), "__call__"
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
        type(client.transport.create_occurrence), "__call__"
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
        type(client.transport.create_occurrence), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].occurrence
        mock_val = grafeas.Occurrence(name="name_value")
        assert arg == mock_val


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
        type(client.transport.create_occurrence), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].occurrence
        mock_val = grafeas.Occurrence(name="name_value")
        assert arg == mock_val


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


@pytest.mark.parametrize("request_type", [grafeas.BatchCreateOccurrencesRequest, dict,])
def test_batch_create_occurrences(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_occurrences), "__call__"
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


def test_batch_create_occurrences_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_occurrences), "__call__"
    ) as call:
        client.batch_create_occurrences()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateOccurrencesRequest()


@pytest.mark.asyncio
async def test_batch_create_occurrences_async(
    transport: str = "grpc_asyncio", request_type=grafeas.BatchCreateOccurrencesRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_occurrences), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.BatchCreateOccurrencesResponse()
        )
        response = await client.batch_create_occurrences(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateOccurrencesResponse)


@pytest.mark.asyncio
async def test_batch_create_occurrences_async_from_dict():
    await test_batch_create_occurrences_async(request_type=dict)


def test_batch_create_occurrences_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateOccurrencesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_occurrences), "__call__"
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
        type(client.transport.batch_create_occurrences), "__call__"
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
        type(client.transport.batch_create_occurrences), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].occurrences
        mock_val = [grafeas.Occurrence(name="name_value")]
        assert arg == mock_val


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
        type(client.transport.batch_create_occurrences), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].occurrences
        mock_val = [grafeas.Occurrence(name="name_value")]
        assert arg == mock_val


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


@pytest.mark.parametrize("request_type", [grafeas.UpdateOccurrenceRequest, dict,])
def test_update_occurrence(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence(
            name="name_value",
            resource_uri="resource_uri_value",
            note_name="note_name_value",
            kind=common.NoteKind.VULNERABILITY,
            remediation="remediation_value",
            vulnerability=vulnerability.VulnerabilityOccurrence(type_="type__value"),
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


def test_update_occurrence_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_occurrence), "__call__"
    ) as call:
        client.update_occurrence()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.UpdateOccurrenceRequest()


@pytest.mark.asyncio
async def test_update_occurrence_async(
    transport: str = "grpc_asyncio", request_type=grafeas.UpdateOccurrenceRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_occurrence), "__call__"
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
        assert args[0] == grafeas.UpdateOccurrenceRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Occurrence)
    assert response.name == "name_value"
    assert response.resource_uri == "resource_uri_value"
    assert response.note_name == "note_name_value"
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.remediation == "remediation_value"


@pytest.mark.asyncio
async def test_update_occurrence_async_from_dict():
    await test_update_occurrence_async(request_type=dict)


def test_update_occurrence_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateOccurrenceRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_occurrence), "__call__"
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
        type(client.transport.update_occurrence), "__call__"
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
        type(client.transport.update_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_occurrence(
            name="name_value",
            occurrence=grafeas.Occurrence(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].occurrence
        mock_val = grafeas.Occurrence(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_occurrence_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_occurrence(
            grafeas.UpdateOccurrenceRequest(),
            name="name_value",
            occurrence=grafeas.Occurrence(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_occurrence_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_occurrence), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Occurrence()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Occurrence())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_occurrence(
            name="name_value",
            occurrence=grafeas.Occurrence(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].occurrence
        mock_val = grafeas.Occurrence(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


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
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize("request_type", [grafeas.GetOccurrenceNoteRequest, dict,])
def test_get_occurrence_note(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_occurrence_note), "__call__"
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


def test_get_occurrence_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_occurrence_note), "__call__"
    ) as call:
        client.get_occurrence_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetOccurrenceNoteRequest()


@pytest.mark.asyncio
async def test_get_occurrence_note_async(
    transport: str = "grpc_asyncio", request_type=grafeas.GetOccurrenceNoteRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_occurrence_note), "__call__"
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
        assert args[0] == grafeas.GetOccurrenceNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == "name_value"
    assert response.short_description == "short_description_value"
    assert response.long_description == "long_description_value"
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ["related_note_names_value"]


@pytest.mark.asyncio
async def test_get_occurrence_note_async_from_dict():
    await test_get_occurrence_note_async(request_type=dict)


def test_get_occurrence_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetOccurrenceNoteRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_occurrence_note), "__call__"
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
        type(client.transport.get_occurrence_note), "__call__"
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
        type(client.transport.get_occurrence_note), "__call__"
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


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
        type(client.transport.get_occurrence_note), "__call__"
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_occurrence_note_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_occurrence_note(
            grafeas.GetOccurrenceNoteRequest(), name="name_value",
        )


@pytest.mark.parametrize("request_type", [grafeas.GetNoteRequest, dict,])
def test_get_note(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_note), "__call__") as call:
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


def test_get_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_note), "__call__") as call:
        client.get_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.GetNoteRequest()


@pytest.mark.asyncio
async def test_get_note_async(
    transport: str = "grpc_asyncio", request_type=grafeas.GetNoteRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_note), "__call__") as call:
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
        assert args[0] == grafeas.GetNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == "name_value"
    assert response.short_description == "short_description_value"
    assert response.long_description == "long_description_value"
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ["related_note_names_value"]


@pytest.mark.asyncio
async def test_get_note_async_from_dict():
    await test_get_note_async(request_type=dict)


def test_get_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.GetNoteRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_note), "__call__") as call:
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
    with mock.patch.object(type(client.transport.get_note), "__call__") as call:
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
    with mock.patch.object(type(client.transport.get_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_note(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


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
    with mock.patch.object(type(client.transport.get_note), "__call__") as call:
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_note_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_note(
            grafeas.GetNoteRequest(), name="name_value",
        )


@pytest.mark.parametrize("request_type", [grafeas.ListNotesRequest, dict,])
def test_list_notes(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_notes), "__call__") as call:
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


def test_list_notes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_notes), "__call__") as call:
        client.list_notes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListNotesRequest()


@pytest.mark.asyncio
async def test_list_notes_async(
    transport: str = "grpc_asyncio", request_type=grafeas.ListNotesRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_notes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.ListNotesResponse(next_page_token="next_page_token_value",)
        )
        response = await client.list_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListNotesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_notes_async_from_dict():
    await test_list_notes_async(request_type=dict)


def test_list_notes_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNotesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_notes), "__call__") as call:
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
    with mock.patch.object(type(client.transport.list_notes), "__call__") as call:
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
    with mock.patch.object(type(client.transport.list_notes), "__call__") as call:
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


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
    with mock.patch.object(type(client.transport.list_notes), "__call__") as call:
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_notes_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_notes(
            grafeas.ListNotesRequest(), parent="parent_value", filter="filter_value",
        )


def test_list_notes_pager(transport_name: str = "grpc"):
    client = GrafeasClient(transport=transport_name,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_notes), "__call__") as call:
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


def test_list_notes_pages(transport_name: str = "grpc"):
    client = GrafeasClient(transport=transport_name,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_notes), "__call__") as call:
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
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_notes_async_pager():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notes), "__call__", new_callable=mock.AsyncMock
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
        type(client.transport.list_notes), "__call__", new_callable=mock.AsyncMock
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
        async for page_ in (await client.list_notes(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [grafeas.DeleteNoteRequest, dict,])
def test_delete_note(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteNoteRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_note), "__call__") as call:
        client.delete_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteNoteRequest()


@pytest.mark.asyncio
async def test_delete_note_async(
    transport: str = "grpc_asyncio", request_type=grafeas.DeleteNoteRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_note(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.DeleteNoteRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_note_async_from_dict():
    await test_delete_note_async(request_type=dict)


def test_delete_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.DeleteNoteRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_note), "__call__") as call:
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
    with mock.patch.object(type(client.transport.delete_note), "__call__") as call:
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
    with mock.patch.object(type(client.transport.delete_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_note(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


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
    with mock.patch.object(type(client.transport.delete_note), "__call__") as call:
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_note_flattened_error_async():
    client = GrafeasAsyncClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_note(
            grafeas.DeleteNoteRequest(), name="name_value",
        )


@pytest.mark.parametrize("request_type", [grafeas.CreateNoteRequest, dict,])
def test_create_note(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_note), "__call__") as call:
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


def test_create_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_note), "__call__") as call:
        client.create_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.CreateNoteRequest()


@pytest.mark.asyncio
async def test_create_note_async(
    transport: str = "grpc_asyncio", request_type=grafeas.CreateNoteRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_note), "__call__") as call:
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
        assert args[0] == grafeas.CreateNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == "name_value"
    assert response.short_description == "short_description_value"
    assert response.long_description == "long_description_value"
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ["related_note_names_value"]


@pytest.mark.asyncio
async def test_create_note_async_from_dict():
    await test_create_note_async(request_type=dict)


def test_create_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.CreateNoteRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_note), "__call__") as call:
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
    with mock.patch.object(type(client.transport.create_note), "__call__") as call:
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
    with mock.patch.object(type(client.transport.create_note), "__call__") as call:
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].note_id
        mock_val = "note_id_value"
        assert arg == mock_val
        arg = args[0].note
        mock_val = grafeas.Note(name="name_value")
        assert arg == mock_val


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
    with mock.patch.object(type(client.transport.create_note), "__call__") as call:
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].note_id
        mock_val = "note_id_value"
        assert arg == mock_val
        arg = args[0].note
        mock_val = grafeas.Note(name="name_value")
        assert arg == mock_val


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


@pytest.mark.parametrize("request_type", [grafeas.BatchCreateNotesRequest, dict,])
def test_batch_create_notes(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_notes), "__call__"
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


def test_batch_create_notes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_notes), "__call__"
    ) as call:
        client.batch_create_notes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateNotesRequest()


@pytest.mark.asyncio
async def test_batch_create_notes_async(
    transport: str = "grpc_asyncio", request_type=grafeas.BatchCreateNotesRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_notes), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            grafeas.BatchCreateNotesResponse()
        )
        response = await client.batch_create_notes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.BatchCreateNotesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.BatchCreateNotesResponse)


@pytest.mark.asyncio
async def test_batch_create_notes_async_from_dict():
    await test_batch_create_notes_async(request_type=dict)


def test_batch_create_notes_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.BatchCreateNotesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.batch_create_notes), "__call__"
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
        type(client.transport.batch_create_notes), "__call__"
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
        type(client.transport.batch_create_notes), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].notes
        mock_val = {"key_value": grafeas.Note(name="name_value")}
        assert arg == mock_val


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
        type(client.transport.batch_create_notes), "__call__"
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
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].notes
        mock_val = {"key_value": grafeas.Note(name="name_value")}
        assert arg == mock_val


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


@pytest.mark.parametrize("request_type", [grafeas.UpdateNoteRequest, dict,])
def test_update_note(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_note), "__call__") as call:
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


def test_update_note_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_note), "__call__") as call:
        client.update_note()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.UpdateNoteRequest()


@pytest.mark.asyncio
async def test_update_note_async(
    transport: str = "grpc_asyncio", request_type=grafeas.UpdateNoteRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_note), "__call__") as call:
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
        assert args[0] == grafeas.UpdateNoteRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, grafeas.Note)
    assert response.name == "name_value"
    assert response.short_description == "short_description_value"
    assert response.long_description == "long_description_value"
    assert response.kind == common.NoteKind.VULNERABILITY
    assert response.related_note_names == ["related_note_names_value"]


@pytest.mark.asyncio
async def test_update_note_async_from_dict():
    await test_update_note_async(request_type=dict)


def test_update_note_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.UpdateNoteRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_note), "__call__") as call:
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
    with mock.patch.object(type(client.transport.update_note), "__call__") as call:
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
    with mock.patch.object(type(client.transport.update_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_note(
            name="name_value",
            note=grafeas.Note(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].note
        mock_val = grafeas.Note(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


def test_update_note_flattened_error():
    client = GrafeasClient()

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_note(
            grafeas.UpdateNoteRequest(),
            name="name_value",
            note=grafeas.Note(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_note_flattened_async():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_note), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grafeas.Note()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(grafeas.Note())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_note(
            name="name_value",
            note=grafeas.Note(name="name_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].note
        mock_val = grafeas.Note(name="name_value")
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=["paths_value"])
        assert arg == mock_val


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
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.parametrize("request_type", [grafeas.ListNoteOccurrencesRequest, dict,])
def test_list_note_occurrences(request_type, transport: str = "grpc"):
    client = GrafeasClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_note_occurrences), "__call__"
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


def test_list_note_occurrences_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = GrafeasClient(transport="grpc",)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_note_occurrences), "__call__"
    ) as call:
        client.list_note_occurrences()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == grafeas.ListNoteOccurrencesRequest()


@pytest.mark.asyncio
async def test_list_note_occurrences_async(
    transport: str = "grpc_asyncio", request_type=grafeas.ListNoteOccurrencesRequest
):
    client = GrafeasAsyncClient(transport=transport,)

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_note_occurrences), "__call__"
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
        assert args[0] == grafeas.ListNoteOccurrencesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNoteOccurrencesAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_note_occurrences_async_from_dict():
    await test_list_note_occurrences_async(request_type=dict)


def test_list_note_occurrences_field_headers():
    client = GrafeasClient()

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = grafeas.ListNoteOccurrencesRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_note_occurrences), "__call__"
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
        type(client.transport.list_note_occurrences), "__call__"
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
        type(client.transport.list_note_occurrences), "__call__"
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


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
        type(client.transport.list_note_occurrences), "__call__"
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
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val
        arg = args[0].filter
        mock_val = "filter_value"
        assert arg == mock_val


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


def test_list_note_occurrences_pager(transport_name: str = "grpc"):
    client = GrafeasClient(transport=transport_name,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_note_occurrences), "__call__"
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


def test_list_note_occurrences_pages(transport_name: str = "grpc"):
    client = GrafeasClient(transport=transport_name,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_note_occurrences), "__call__"
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
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_note_occurrences_async_pager():
    client = GrafeasAsyncClient()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_note_occurrences),
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
        type(client.transport.list_note_occurrences),
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
        async for page_ in (await client.list_note_occurrences(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.GrafeasGrpcTransport()
    client = GrafeasClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.GrafeasGrpcTransport()
    channel = transport.grpc_channel
    assert channel

    transport = transports.GrafeasGrpcAsyncIOTransport()
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.GrafeasGrpcTransport, transports.GrafeasGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = GrafeasClient()
    assert isinstance(client.transport, transports.GrafeasGrpcTransport,)


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

    with pytest.raises(NotImplementedError):
        transport.close()


def test_grafeas_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "grafeas.grafeas_v1.services.grafeas.transports.GrafeasTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.GrafeasTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(),
            quota_project_id="octopus",
        )


def test_grafeas_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "grafeas.grafeas_v1.services.grafeas.transports.GrafeasTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.GrafeasTransport()
        adc.assert_called_once()


def test_grafeas_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        GrafeasClient()
        adc.assert_called_once_with(
            scopes=None, default_scopes=(), quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.GrafeasGrpcTransport, transports.GrafeasGrpcAsyncIOTransport,],
)
def test_grafeas_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"], default_scopes=(), quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.GrafeasGrpcTransport, grpc_helpers),
        (transports.GrafeasGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_grafeas_transport_create_channel(transport_class, grpc_helpers):
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
            ":443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(),
            scopes=["1", "2"],
            default_host="",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.GrafeasGrpcTransport, transports.GrafeasGrpcAsyncIOTransport],
)
def test_grafeas_grpc_transport_client_cert_source_for_mtls(transport_class):
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


def test_grafeas_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.GrafeasGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_grafeas_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.GrafeasGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [transports.GrafeasGrpcTransport, transports.GrafeasGrpcAsyncIOTransport],
)
def test_grafeas_transport_channel_mtls_with_client_cert_source(transport_class):
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
    [transports.GrafeasGrpcTransport, transports.GrafeasGrpcAsyncIOTransport],
)
def test_grafeas_transport_channel_mtls_with_adc(transport_class):
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


def test_occurrence_path():
    project = "oyster"
    occurrence = "nudibranch"
    expected = "projects/{project}/occurrences/{occurrence}".format(
        project=project, occurrence=occurrence,
    )
    actual = GrafeasClient.occurrence_path(project, occurrence)
    assert expected == actual


def test_parse_occurrence_path():
    expected = {
        "project": "cuttlefish",
        "occurrence": "mussel",
    }
    path = GrafeasClient.occurrence_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_occurrence_path(path)
    assert expected == actual


def test_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project,)
    actual = GrafeasClient.project_path(project)
    assert expected == actual


def test_parse_project_path():
    expected = {
        "project": "nautilus",
    }
    path = GrafeasClient.project_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_project_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = GrafeasClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = GrafeasClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"
    expected = "folders/{folder}".format(folder=folder,)
    actual = GrafeasClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = GrafeasClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = GrafeasClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = GrafeasClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"
    expected = "projects/{project}".format(project=project,)
    actual = GrafeasClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = GrafeasClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = GrafeasClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = GrafeasClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = GrafeasClient.parse_common_location_path(path)
    assert expected == actual


@pytest.mark.asyncio
async def test_transport_close_async():
    client = GrafeasAsyncClient(transport="grpc_asyncio",)
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = GrafeasClient(transport=transport)
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = GrafeasClient(transport=transport)
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()
