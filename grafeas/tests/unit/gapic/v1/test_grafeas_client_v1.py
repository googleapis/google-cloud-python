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

from google.protobuf import empty_pb2
from grafeas import grafeas_v1
from grafeas.grafeas_v1.proto import grafeas_pb2
from grafeas.grafeas_v1.gapic.transports import grafeas_grpc_transport


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


class TestGrafeasClient(object):
    def test_get_occurrence(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        resource_uri = "resourceUri-384040517"
        note_name = "noteName1780787896"
        remediation = "remediation779381797"
        expected_response = {
            "name": name_2,
            "resource_uri": resource_uri,
            "note_name": note_name,
            "remediation": remediation,
        }
        expected_response = grafeas_pb2.Occurrence(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        name = client.occurrence_path("[PROJECT]", "[OCCURRENCE]")

        response = client.get_occurrence(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.GetOccurrenceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_occurrence_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        name = client.occurrence_path("[PROJECT]", "[OCCURRENCE]")

        with pytest.raises(CustomException):
            client.get_occurrence(name)

    def test_list_occurrences(self):
        # Setup Expected Response
        next_page_token = ""
        occurrences_element = {}
        occurrences = [occurrences_element]
        expected_response = {
            "next_page_token": next_page_token,
            "occurrences": occurrences,
        }
        expected_response = grafeas_pb2.ListOccurrencesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_occurrences(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.occurrences[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.ListOccurrencesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_occurrences_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_occurrences(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_occurrence(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        name = client.occurrence_path("[PROJECT]", "[OCCURRENCE]")

        client.delete_occurrence(name)

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.DeleteOccurrenceRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_occurrence_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        name = client.occurrence_path("[PROJECT]", "[OCCURRENCE]")

        with pytest.raises(CustomException):
            client.delete_occurrence(name)

    def test_create_occurrence(self):
        # Setup Expected Response
        name = "name3373707"
        resource_uri = "resourceUri-384040517"
        note_name = "noteName1780787896"
        remediation = "remediation779381797"
        expected_response = {
            "name": name,
            "resource_uri": resource_uri,
            "note_name": note_name,
            "remediation": remediation,
        }
        expected_response = grafeas_pb2.Occurrence(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        parent = client.project_path("[PROJECT]")
        occurrence = {}

        response = client.create_occurrence(parent, occurrence)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.CreateOccurrenceRequest(
            parent=parent, occurrence=occurrence
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_occurrence_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        parent = client.project_path("[PROJECT]")
        occurrence = {}

        with pytest.raises(CustomException):
            client.create_occurrence(parent, occurrence)

    def test_batch_create_occurrences(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = grafeas_pb2.BatchCreateOccurrencesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        parent = client.project_path("[PROJECT]")
        occurrences = []

        response = client.batch_create_occurrences(parent, occurrences)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.BatchCreateOccurrencesRequest(
            parent=parent, occurrences=occurrences
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_create_occurrences_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        parent = client.project_path("[PROJECT]")
        occurrences = []

        with pytest.raises(CustomException):
            client.batch_create_occurrences(parent, occurrences)

    def test_update_occurrence(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        resource_uri = "resourceUri-384040517"
        note_name = "noteName1780787896"
        remediation = "remediation779381797"
        expected_response = {
            "name": name_2,
            "resource_uri": resource_uri,
            "note_name": note_name,
            "remediation": remediation,
        }
        expected_response = grafeas_pb2.Occurrence(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        name = client.occurrence_path("[PROJECT]", "[OCCURRENCE]")
        occurrence = {}

        response = client.update_occurrence(name, occurrence)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.UpdateOccurrenceRequest(
            name=name, occurrence=occurrence
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_occurrence_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        name = client.occurrence_path("[PROJECT]", "[OCCURRENCE]")
        occurrence = {}

        with pytest.raises(CustomException):
            client.update_occurrence(name, occurrence)

    def test_get_occurrence_note(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        short_description = "shortDescription-235369287"
        long_description = "longDescription-1747792199"
        expected_response = {
            "name": name_2,
            "short_description": short_description,
            "long_description": long_description,
        }
        expected_response = grafeas_pb2.Note(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        name = client.occurrence_path("[PROJECT]", "[OCCURRENCE]")

        response = client.get_occurrence_note(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.GetOccurrenceNoteRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_occurrence_note_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        name = client.occurrence_path("[PROJECT]", "[OCCURRENCE]")

        with pytest.raises(CustomException):
            client.get_occurrence_note(name)

    def test_get_note(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        short_description = "shortDescription-235369287"
        long_description = "longDescription-1747792199"
        expected_response = {
            "name": name_2,
            "short_description": short_description,
            "long_description": long_description,
        }
        expected_response = grafeas_pb2.Note(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        name = client.note_path("[PROJECT]", "[NOTE]")

        response = client.get_note(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.GetNoteRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_note_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        name = client.note_path("[PROJECT]", "[NOTE]")

        with pytest.raises(CustomException):
            client.get_note(name)

    def test_list_notes(self):
        # Setup Expected Response
        next_page_token = ""
        notes_element = {}
        notes = [notes_element]
        expected_response = {"next_page_token": next_page_token, "notes": notes}
        expected_response = grafeas_pb2.ListNotesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_notes(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.notes[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.ListNotesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_notes_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.list_notes(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_note(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        name = client.note_path("[PROJECT]", "[NOTE]")

        client.delete_note(name)

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.DeleteNoteRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_note_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        name = client.note_path("[PROJECT]", "[NOTE]")

        with pytest.raises(CustomException):
            client.delete_note(name)

    def test_create_note(self):
        # Setup Expected Response
        name = "name3373707"
        short_description = "shortDescription-235369287"
        long_description = "longDescription-1747792199"
        expected_response = {
            "name": name,
            "short_description": short_description,
            "long_description": long_description,
        }
        expected_response = grafeas_pb2.Note(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        parent = client.project_path("[PROJECT]")
        note_id = "noteId2129224840"
        note = {}

        response = client.create_note(parent, note_id, note)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.CreateNoteRequest(
            parent=parent, note_id=note_id, note=note
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_note_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        parent = client.project_path("[PROJECT]")
        note_id = "noteId2129224840"
        note = {}

        with pytest.raises(CustomException):
            client.create_note(parent, note_id, note)

    def test_batch_create_notes(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = grafeas_pb2.BatchCreateNotesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        parent = client.project_path("[PROJECT]")
        notes = {}

        response = client.batch_create_notes(parent, notes)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.BatchCreateNotesRequest(
            parent=parent, notes=notes
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_create_notes_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        parent = client.project_path("[PROJECT]")
        notes = {}

        with pytest.raises(CustomException):
            client.batch_create_notes(parent, notes)

    def test_update_note(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        short_description = "shortDescription-235369287"
        long_description = "longDescription-1747792199"
        expected_response = {
            "name": name_2,
            "short_description": short_description,
            "long_description": long_description,
        }
        expected_response = grafeas_pb2.Note(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        name = client.note_path("[PROJECT]", "[NOTE]")
        note = {}

        response = client.update_note(name, note)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.UpdateNoteRequest(name=name, note=note)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_note_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        name = client.note_path("[PROJECT]", "[NOTE]")
        note = {}

        with pytest.raises(CustomException):
            client.update_note(name, note)

    def test_list_note_occurrences(self):
        # Setup Expected Response
        next_page_token = ""
        occurrences_element = {}
        occurrences = [occurrences_element]
        expected_response = {
            "next_page_token": next_page_token,
            "occurrences": occurrences,
        }
        expected_response = grafeas_pb2.ListNoteOccurrencesResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup Request
        name = client.note_path("[PROJECT]", "[NOTE]")

        paged_list_response = client.list_note_occurrences(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.occurrences[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = grafeas_pb2.ListNoteOccurrencesRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_note_occurrences_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            address = "[SERVICE_ADDRESS]"

            scopes = "SCOPE"

            transport = grafeas_grpc_transport.GrafeasGrpcTransport(address, scopes)

            client = grafeas_v1.GrafeasClient(transport)

        # Setup request
        name = client.note_path("[PROJECT]", "[NOTE]")

        paged_list_response = client.list_note_occurrences(name)
        with pytest.raises(CustomException):
            list(paged_list_response)
