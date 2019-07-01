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

from google.cloud import irm_v1alpha2
from google.cloud.irm_v1alpha2.proto import incidents_pb2
from google.cloud.irm_v1alpha2.proto import incidents_service_pb2
from google.protobuf import empty_pb2


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


class TestIncidentServiceClient(object):
    def test_create_incident(self):
        # Setup Expected Response
        name = "name3373707"
        title = "title110371416"
        etag = "etag3123477"
        duplicate_incident = "duplicateIncident-316496506"
        expected_response = {
            "name": name,
            "title": title,
            "etag": etag,
            "duplicate_incident": duplicate_incident,
        }
        expected_response = incidents_pb2.Incident(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        incident = {}
        parent = client.project_path("[PROJECT]")

        response = client.create_incident(incident, parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.CreateIncidentRequest(
            incident=incident, parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_incident_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        incident = {}
        parent = client.project_path("[PROJECT]")

        with pytest.raises(CustomException):
            client.create_incident(incident, parent)

    def test_get_incident(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        title = "title110371416"
        etag = "etag3123477"
        duplicate_incident = "duplicateIncident-316496506"
        expected_response = {
            "name": name_2,
            "title": title,
            "etag": etag,
            "duplicate_incident": duplicate_incident,
        }
        expected_response = incidents_pb2.Incident(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.incident_path("[PROJECT]", "[INCIDENT]")

        response = client.get_incident(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.GetIncidentRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_incident_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.incident_path("[PROJECT]", "[INCIDENT]")

        with pytest.raises(CustomException):
            client.get_incident(name)

    def test_search_incidents(self):
        # Setup Expected Response
        next_page_token = ""
        incidents_element = {}
        incidents = [incidents_element]
        expected_response = {"next_page_token": next_page_token, "incidents": incidents}
        expected_response = incidents_service_pb2.SearchIncidentsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.search_incidents(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.incidents[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.SearchIncidentsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_incidents_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.search_incidents(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_incident(self):
        # Setup Expected Response
        name = "name3373707"
        title = "title110371416"
        etag = "etag3123477"
        duplicate_incident = "duplicateIncident-316496506"
        expected_response = {
            "name": name,
            "title": title,
            "etag": etag,
            "duplicate_incident": duplicate_incident,
        }
        expected_response = incidents_pb2.Incident(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        incident = {}

        response = client.update_incident(incident)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.UpdateIncidentRequest(
            incident=incident
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_incident_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        incident = {}

        with pytest.raises(CustomException):
            client.update_incident(incident)

    def test_search_similar_incidents(self):
        # Setup Expected Response
        next_page_token = ""
        results_element = {}
        results = [results_element]
        expected_response = {"next_page_token": next_page_token, "results": results}
        expected_response = incidents_service_pb2.SearchSimilarIncidentsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.search_similar_incidents(name)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.results[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.SearchSimilarIncidentsRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_similar_incidents_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.search_similar_incidents(name)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_annotation(self):
        # Setup Expected Response
        name = "name3373707"
        content = "content951530617"
        content_type = "contentType831846208"
        expected_response = {
            "name": name,
            "content": content,
            "content_type": content_type,
        }
        expected_response = incidents_pb2.Annotation(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        annotation = {}

        response = client.create_annotation(parent, annotation)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.CreateAnnotationRequest(
            parent=parent, annotation=annotation
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_annotation_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        annotation = {}

        with pytest.raises(CustomException):
            client.create_annotation(parent, annotation)

    def test_list_annotations(self):
        # Setup Expected Response
        next_page_token = ""
        annotations_element = {}
        annotations = [annotations_element]
        expected_response = {
            "next_page_token": next_page_token,
            "annotations": annotations,
        }
        expected_response = incidents_service_pb2.ListAnnotationsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_annotations(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.annotations[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.ListAnnotationsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_annotations_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_annotations(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_tag(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = incidents_pb2.Tag(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        tag = {}

        response = client.create_tag(parent, tag)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.CreateTagRequest(
            parent=parent, tag=tag
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        tag = {}

        with pytest.raises(CustomException):
            client.create_tag(parent, tag)

    def test_delete_tag(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.tag_path("[PROJECT]", "[INCIDENT]", "[TAG]")

        client.delete_tag(name)

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.DeleteTagRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.tag_path("[PROJECT]", "[INCIDENT]", "[TAG]")

        with pytest.raises(CustomException):
            client.delete_tag(name)

    def test_list_tags(self):
        # Setup Expected Response
        next_page_token = ""
        tags_element = {}
        tags = [tags_element]
        expected_response = {"next_page_token": next_page_token, "tags": tags}
        expected_response = incidents_service_pb2.ListTagsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_tags(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.tags[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.ListTagsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_tags_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_tags(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_create_signal(self):
        # Setup Expected Response
        name = "name3373707"
        etag = "etag3123477"
        incident = "incident86983890"
        title = "title110371416"
        content_type = "contentType831846208"
        content = "content951530617"
        expected_response = {
            "name": name,
            "etag": etag,
            "incident": incident,
            "title": title,
            "content_type": content_type,
            "content": content,
        }
        expected_response = incidents_pb2.Signal(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        signal = {}

        response = client.create_signal(parent, signal)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.CreateSignalRequest(
            parent=parent, signal=signal
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_signal_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        signal = {}

        with pytest.raises(CustomException):
            client.create_signal(parent, signal)

    def test_search_signals(self):
        # Setup Expected Response
        next_page_token = ""
        signals_element = {}
        signals = [signals_element]
        expected_response = {"next_page_token": next_page_token, "signals": signals}
        expected_response = incidents_service_pb2.SearchSignalsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.search_signals(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.signals[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.SearchSignalsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_signals_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")

        paged_list_response = client.search_signals(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_signal(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        etag = "etag3123477"
        incident = "incident86983890"
        title = "title110371416"
        content_type = "contentType831846208"
        content = "content951530617"
        expected_response = {
            "name": name_2,
            "etag": etag,
            "incident": incident,
            "title": title,
            "content_type": content_type,
            "content": content,
        }
        expected_response = incidents_pb2.Signal(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.signal_path("[PROJECT]", "[SIGNAL]")

        response = client.get_signal(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.GetSignalRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_signal_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.signal_path("[PROJECT]", "[SIGNAL]")

        with pytest.raises(CustomException):
            client.get_signal(name)

    def test_lookup_signal(self):
        # Setup Expected Response
        name = "name3373707"
        etag = "etag3123477"
        incident = "incident86983890"
        title = "title110371416"
        content_type = "contentType831846208"
        content = "content951530617"
        expected_response = {
            "name": name,
            "etag": etag,
            "incident": incident,
            "title": title,
            "content_type": content_type,
            "content": content,
        }
        expected_response = incidents_pb2.Signal(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        response = client.lookup_signal()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.LookupSignalRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_lookup_signal_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        with pytest.raises(CustomException):
            client.lookup_signal()

    def test_update_signal(self):
        # Setup Expected Response
        name = "name3373707"
        etag = "etag3123477"
        incident = "incident86983890"
        title = "title110371416"
        content_type = "contentType831846208"
        content = "content951530617"
        expected_response = {
            "name": name,
            "etag": etag,
            "incident": incident,
            "title": title,
            "content_type": content_type,
            "content": content,
        }
        expected_response = incidents_pb2.Signal(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        signal = {}

        response = client.update_signal(signal)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.UpdateSignalRequest(signal=signal)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_signal_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        signal = {}

        with pytest.raises(CustomException):
            client.update_signal(signal)

    def test_escalate_incident(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = incidents_service_pb2.EscalateIncidentResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        incident = {}

        response = client.escalate_incident(incident)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.EscalateIncidentRequest(
            incident=incident
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_escalate_incident_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        incident = {}

        with pytest.raises(CustomException):
            client.escalate_incident(incident)

    def test_create_artifact(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        etag = "etag3123477"
        url = "url116079"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "etag": etag,
            "url": url,
        }
        expected_response = incidents_pb2.Artifact(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        artifact = {}

        response = client.create_artifact(parent, artifact)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.CreateArtifactRequest(
            parent=parent, artifact=artifact
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_artifact_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        artifact = {}

        with pytest.raises(CustomException):
            client.create_artifact(parent, artifact)

    def test_list_artifacts(self):
        # Setup Expected Response
        next_page_token = ""
        artifacts_element = {}
        artifacts = [artifacts_element]
        expected_response = {"next_page_token": next_page_token, "artifacts": artifacts}
        expected_response = incidents_service_pb2.ListArtifactsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_artifacts(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.artifacts[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.ListArtifactsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_artifacts_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_artifacts(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_artifact(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        etag = "etag3123477"
        url = "url116079"
        expected_response = {
            "name": name,
            "display_name": display_name,
            "etag": etag,
            "url": url,
        }
        expected_response = incidents_pb2.Artifact(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        artifact = {}

        response = client.update_artifact(artifact)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.UpdateArtifactRequest(
            artifact=artifact
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_artifact_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        artifact = {}

        with pytest.raises(CustomException):
            client.update_artifact(artifact)

    def test_delete_artifact(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.artifact_path("[PROJECT]", "[INCIDENT]", "[ARTIFACT]")

        client.delete_artifact(name)

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.DeleteArtifactRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_artifact_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.artifact_path("[PROJECT]", "[INCIDENT]", "[ARTIFACT]")

        with pytest.raises(CustomException):
            client.delete_artifact(name)

    def test_send_shift_handoff(self):
        # Setup Expected Response
        content_type = "contentType831846208"
        content = "content951530617"
        expected_response = {"content_type": content_type, "content": content}
        expected_response = incidents_service_pb2.SendShiftHandoffResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.project_path("[PROJECT]")
        recipients = []
        subject = "subject-1867885268"

        response = client.send_shift_handoff(parent, recipients, subject)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.SendShiftHandoffRequest(
            parent=parent, recipients=recipients, subject=subject
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_send_shift_handoff_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.project_path("[PROJECT]")
        recipients = []
        subject = "subject-1867885268"

        with pytest.raises(CustomException):
            client.send_shift_handoff(parent, recipients, subject)

    def test_create_subscription(self):
        # Setup Expected Response
        name = "name3373707"
        etag = "etag3123477"
        expected_response = {"name": name, "etag": etag}
        expected_response = incidents_pb2.Subscription(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        subscription = {}

        response = client.create_subscription(parent, subscription)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.CreateSubscriptionRequest(
            parent=parent, subscription=subscription
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_subscription_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        subscription = {}

        with pytest.raises(CustomException):
            client.create_subscription(parent, subscription)

    def test_update_subscription(self):
        # Setup Expected Response
        name = "name3373707"
        etag = "etag3123477"
        expected_response = {"name": name, "etag": etag}
        expected_response = incidents_pb2.Subscription(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        subscription = {}

        response = client.update_subscription(subscription)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.UpdateSubscriptionRequest(
            subscription=subscription
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_subscription_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        subscription = {}

        with pytest.raises(CustomException):
            client.update_subscription(subscription)

    def test_list_subscriptions(self):
        # Setup Expected Response
        next_page_token = ""
        subscriptions_element = {}
        subscriptions = [subscriptions_element]
        expected_response = {
            "next_page_token": next_page_token,
            "subscriptions": subscriptions,
        }
        expected_response = incidents_service_pb2.ListSubscriptionsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_subscriptions(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.subscriptions[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.ListSubscriptionsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_subscriptions_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_subscriptions(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_delete_subscription(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.subscription_path("[PROJECT]", "[INCIDENT]", "[SUBSCRIPTION]")

        client.delete_subscription(name)

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.DeleteSubscriptionRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_subscription_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.subscription_path("[PROJECT]", "[INCIDENT]", "[SUBSCRIPTION]")

        with pytest.raises(CustomException):
            client.delete_subscription(name)

    def test_create_incident_role_assignment(self):
        # Setup Expected Response
        name = "name3373707"
        etag = "etag3123477"
        expected_response = {"name": name, "etag": etag}
        expected_response = incidents_pb2.IncidentRoleAssignment(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        incident_role_assignment = {}

        response = client.create_incident_role_assignment(
            parent, incident_role_assignment
        )
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.CreateIncidentRoleAssignmentRequest(
            parent=parent, incident_role_assignment=incident_role_assignment
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_incident_role_assignment_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")
        incident_role_assignment = {}

        with pytest.raises(CustomException):
            client.create_incident_role_assignment(parent, incident_role_assignment)

    def test_delete_incident_role_assignment(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )

        client.delete_incident_role_assignment(name)

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.DeleteIncidentRoleAssignmentRequest(
            name=name
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_incident_role_assignment_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )

        with pytest.raises(CustomException):
            client.delete_incident_role_assignment(name)

    def test_list_incident_role_assignments(self):
        # Setup Expected Response
        next_page_token = ""
        incident_role_assignments_element = {}
        incident_role_assignments = [incident_role_assignments_element]
        expected_response = {
            "next_page_token": next_page_token,
            "incident_role_assignments": incident_role_assignments,
        }
        expected_response = incidents_service_pb2.ListIncidentRoleAssignmentsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_incident_role_assignments(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.incident_role_assignments[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.ListIncidentRoleAssignmentsRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_incident_role_assignments_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        parent = client.incident_path("[PROJECT]", "[INCIDENT]")

        paged_list_response = client.list_incident_role_assignments(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_request_incident_role_handover(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        etag = "etag3123477"
        expected_response = {"name": name_2, "etag": etag}
        expected_response = incidents_pb2.IncidentRoleAssignment(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )
        new_assignee = {}

        response = client.request_incident_role_handover(name, new_assignee)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.RequestIncidentRoleHandoverRequest(
            name=name, new_assignee=new_assignee
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_request_incident_role_handover_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )
        new_assignee = {}

        with pytest.raises(CustomException):
            client.request_incident_role_handover(name, new_assignee)

    def test_confirm_incident_role_handover(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        etag = "etag3123477"
        expected_response = {"name": name_2, "etag": etag}
        expected_response = incidents_pb2.IncidentRoleAssignment(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )
        new_assignee = {}

        response = client.confirm_incident_role_handover(name, new_assignee)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.ConfirmIncidentRoleHandoverRequest(
            name=name, new_assignee=new_assignee
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_confirm_incident_role_handover_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )
        new_assignee = {}

        with pytest.raises(CustomException):
            client.confirm_incident_role_handover(name, new_assignee)

    def test_force_incident_role_handover(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        etag = "etag3123477"
        expected_response = {"name": name_2, "etag": etag}
        expected_response = incidents_pb2.IncidentRoleAssignment(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )
        new_assignee = {}

        response = client.force_incident_role_handover(name, new_assignee)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.ForceIncidentRoleHandoverRequest(
            name=name, new_assignee=new_assignee
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_force_incident_role_handover_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )
        new_assignee = {}

        with pytest.raises(CustomException):
            client.force_incident_role_handover(name, new_assignee)

    def test_cancel_incident_role_handover(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        etag = "etag3123477"
        expected_response = {"name": name_2, "etag": etag}
        expected_response = incidents_pb2.IncidentRoleAssignment(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup Request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )
        new_assignee = {}

        response = client.cancel_incident_role_handover(name, new_assignee)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = incidents_service_pb2.CancelIncidentRoleHandoverRequest(
            name=name, new_assignee=new_assignee
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_cancel_incident_role_handover_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = irm_v1alpha2.IncidentServiceClient()

        # Setup request
        name = client.role_assignment_path(
            "[PROJECT]", "[INCIDENT]", "[ROLE_ASSIGNMENT]"
        )
        new_assignee = {}

        with pytest.raises(CustomException):
            client.cancel_incident_role_handover(name, new_assignee)
