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

from google.cloud import datacatalog_v1beta1
from google.cloud.datacatalog_v1beta1.proto import datacatalog_pb2
from google.cloud.datacatalog_v1beta1.proto import search_pb2
from google.cloud.datacatalog_v1beta1.proto import tags_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
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


class TestDataCatalogClient(object):
    def test_search_catalog(self):
        # Setup Expected Response
        next_page_token = ""
        results_element = {}
        results = [results_element]
        expected_response = {"next_page_token": next_page_token, "results": results}
        expected_response = datacatalog_pb2.SearchCatalogResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        scope = {}
        query = "query107944136"

        paged_list_response = client.search_catalog(scope, query)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.results[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.SearchCatalogRequest(
            scope=scope, query=query
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_search_catalog_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        scope = {}
        query = "query107944136"

        paged_list_response = client.search_catalog(scope, query)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_update_entry(self):
        # Setup Expected Response
        name = "name3373707"
        linked_resource = "linkedResource1544625012"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name,
            "linked_resource": linked_resource,
            "display_name": display_name,
            "description": description,
        }
        expected_response = datacatalog_pb2.Entry(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        entry = {}

        response = client.update_entry(entry)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.UpdateEntryRequest(entry=entry)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_entry_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        entry = {}

        with pytest.raises(CustomException):
            client.update_entry(entry)

    def test_get_entry(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        linked_resource = "linkedResource1544625012"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name_2,
            "linked_resource": linked_resource,
            "display_name": display_name,
            "description": description,
        }
        expected_response = datacatalog_pb2.Entry(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        name = client.entry_path("[PROJECT]", "[LOCATION]", "[ENTRY_GROUP]", "[ENTRY]")

        response = client.get_entry(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.GetEntryRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_entry_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        name = client.entry_path("[PROJECT]", "[LOCATION]", "[ENTRY_GROUP]", "[ENTRY]")

        with pytest.raises(CustomException):
            client.get_entry(name)

    def test_lookup_entry(self):
        # Setup Expected Response
        name = "name3373707"
        linked_resource = "linkedResource1544625012"
        display_name = "displayName1615086568"
        description = "description-1724546052"
        expected_response = {
            "name": name,
            "linked_resource": linked_resource,
            "display_name": display_name,
            "description": description,
        }
        expected_response = datacatalog_pb2.Entry(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        response = client.lookup_entry()
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.LookupEntryRequest()
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_lookup_entry_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        with pytest.raises(CustomException):
            client.lookup_entry()

    def test_create_tag_template(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = tags_pb2.TagTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        tag_template_id = "tagTemplateId-2020335141"
        tag_template = {}

        response = client.create_tag_template(parent, tag_template_id, tag_template)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.CreateTagTemplateRequest(
            parent=parent, tag_template_id=tag_template_id, tag_template=tag_template
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_tag_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        tag_template_id = "tagTemplateId-2020335141"
        tag_template = {}

        with pytest.raises(CustomException):
            client.create_tag_template(parent, tag_template_id, tag_template)

    def test_get_tag_template(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        expected_response = {"name": name_2, "display_name": display_name}
        expected_response = tags_pb2.TagTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        name = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")

        response = client.get_tag_template(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.GetTagTemplateRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_tag_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        name = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")

        with pytest.raises(CustomException):
            client.get_tag_template(name)

    def test_update_tag_template(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        expected_response = {"name": name, "display_name": display_name}
        expected_response = tags_pb2.TagTemplate(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        tag_template = {}

        response = client.update_tag_template(tag_template)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.UpdateTagTemplateRequest(
            tag_template=tag_template
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_tag_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        tag_template = {}

        with pytest.raises(CustomException):
            client.update_tag_template(tag_template)

    def test_delete_tag_template(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        name = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")
        force = False

        client.delete_tag_template(name, force)

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.DeleteTagTemplateRequest(
            name=name, force=force
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_tag_template_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        name = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")
        force = False

        with pytest.raises(CustomException):
            client.delete_tag_template(name, force)

    def test_create_tag_template_field(self):
        # Setup Expected Response
        display_name = "displayName1615086568"
        expected_response = {"display_name": display_name}
        expected_response = tags_pb2.TagTemplateField(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        parent = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")
        tag_template_field_id = "tagTemplateFieldId-92144832"
        tag_template_field = {}

        response = client.create_tag_template_field(
            parent, tag_template_field_id, tag_template_field
        )
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.CreateTagTemplateFieldRequest(
            parent=parent,
            tag_template_field_id=tag_template_field_id,
            tag_template_field=tag_template_field,
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_tag_template_field_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        parent = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")
        tag_template_field_id = "tagTemplateFieldId-92144832"
        tag_template_field = {}

        with pytest.raises(CustomException):
            client.create_tag_template_field(
                parent, tag_template_field_id, tag_template_field
            )

    def test_update_tag_template_field(self):
        # Setup Expected Response
        display_name = "displayName1615086568"
        expected_response = {"display_name": display_name}
        expected_response = tags_pb2.TagTemplateField(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        name = client.field_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]", "[FIELD]")
        tag_template_field = {}

        response = client.update_tag_template_field(name, tag_template_field)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.UpdateTagTemplateFieldRequest(
            name=name, tag_template_field=tag_template_field
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_tag_template_field_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        name = client.field_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]", "[FIELD]")
        tag_template_field = {}

        with pytest.raises(CustomException):
            client.update_tag_template_field(name, tag_template_field)

    def test_rename_tag_template_field(self):
        # Setup Expected Response
        display_name = "displayName1615086568"
        expected_response = {"display_name": display_name}
        expected_response = tags_pb2.TagTemplateField(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        name = client.field_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]", "[FIELD]")
        new_tag_template_field_id = "newTagTemplateFieldId-1668354591"

        response = client.rename_tag_template_field(name, new_tag_template_field_id)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.RenameTagTemplateFieldRequest(
            name=name, new_tag_template_field_id=new_tag_template_field_id
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_rename_tag_template_field_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        name = client.field_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]", "[FIELD]")
        new_tag_template_field_id = "newTagTemplateFieldId-1668354591"

        with pytest.raises(CustomException):
            client.rename_tag_template_field(name, new_tag_template_field_id)

    def test_delete_tag_template_field(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        name = client.field_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]", "[FIELD]")
        force = False

        client.delete_tag_template_field(name, force)

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.DeleteTagTemplateFieldRequest(
            name=name, force=force
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_tag_template_field_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        name = client.field_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]", "[FIELD]")
        force = False

        with pytest.raises(CustomException):
            client.delete_tag_template_field(name, force)

    def test_create_tag(self):
        # Setup Expected Response
        name = "name3373707"
        template = "template-1321546630"
        template_display_name = "templateDisplayName-532252787"
        column = "column-1354837162"
        expected_response = {
            "name": name,
            "template": template,
            "template_display_name": template_display_name,
            "column": column,
        }
        expected_response = tags_pb2.Tag(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        parent = client.entry_path(
            "[PROJECT]", "[LOCATION]", "[ENTRY_GROUP]", "[ENTRY]"
        )
        tag = {}

        response = client.create_tag(parent, tag)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.CreateTagRequest(parent=parent, tag=tag)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        parent = client.entry_path(
            "[PROJECT]", "[LOCATION]", "[ENTRY_GROUP]", "[ENTRY]"
        )
        tag = {}

        with pytest.raises(CustomException):
            client.create_tag(parent, tag)

    def test_update_tag(self):
        # Setup Expected Response
        name = "name3373707"
        template = "template-1321546630"
        template_display_name = "templateDisplayName-532252787"
        column = "column-1354837162"
        expected_response = {
            "name": name,
            "template": template,
            "template_display_name": template_display_name,
            "column": column,
        }
        expected_response = tags_pb2.Tag(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        tag = {}

        response = client.update_tag(tag)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.UpdateTagRequest(tag=tag)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        tag = {}

        with pytest.raises(CustomException):
            client.update_tag(tag)

    def test_delete_tag(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        name = client.tag_path(
            "[PROJECT]", "[LOCATION]", "[ENTRY_GROUP]", "[ENTRY]", "[TAG]"
        )

        client.delete_tag(name)

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.DeleteTagRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_tag_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        name = client.tag_path(
            "[PROJECT]", "[LOCATION]", "[ENTRY_GROUP]", "[ENTRY]", "[TAG]"
        )

        with pytest.raises(CustomException):
            client.delete_tag(name)

    def test_list_tags(self):
        # Setup Expected Response
        next_page_token = ""
        tags_element = {}
        tags = [tags_element]
        expected_response = {"next_page_token": next_page_token, "tags": tags}
        expected_response = datacatalog_pb2.ListTagsResponse(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        parent = client.entry_path(
            "[PROJECT]", "[LOCATION]", "[ENTRY_GROUP]", "[ENTRY]"
        )

        paged_list_response = client.list_tags(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.tags[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = datacatalog_pb2.ListTagsRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_tags_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        parent = client.entry_path(
            "[PROJECT]", "[LOCATION]", "[ENTRY_GROUP]", "[ENTRY]"
        )

        paged_list_response = client.list_tags(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_set_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"21"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        resource = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")
        policy = {}

        response = client.set_iam_policy(resource, policy)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_set_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        resource = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")
        policy = {}

        with pytest.raises(CustomException):
            client.set_iam_policy(resource, policy)

    def test_get_iam_policy(self):
        # Setup Expected Response
        version = 351608024
        etag = b"21"
        expected_response = {"version": version, "etag": etag}
        expected_response = policy_pb2.Policy(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        resource = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")

        response = client.get_iam_policy(resource)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_iam_policy_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        resource = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")

        with pytest.raises(CustomException):
            client.get_iam_policy(resource)

    def test_test_iam_permissions(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = iam_policy_pb2.TestIamPermissionsResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup Request
        resource = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")
        permissions = []

        response = client.test_iam_permissions(resource, permissions)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_test_iam_permissions_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = datacatalog_v1beta1.DataCatalogClient()

        # Setup request
        resource = client.tag_template_path("[PROJECT]", "[LOCATION]", "[TAG_TEMPLATE]")
        permissions = []

        with pytest.raises(CustomException):
            client.test_iam_permissions(resource, permissions)
