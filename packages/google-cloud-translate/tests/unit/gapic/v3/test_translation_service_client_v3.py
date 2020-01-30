# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.cloud import translate_v3
from google.cloud.translate_v3.proto import translation_service_pb2
from google.longrunning import operations_pb2


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


class TestTranslationServiceClient(object):
    def test_translate_text(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = translation_service_pb2.TranslateTextResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        contents = []
        target_language_code = "targetLanguageCode1323228230"
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        response = client.translate_text(contents, target_language_code, parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = translation_service_pb2.TranslateTextRequest(
            contents=contents, target_language_code=target_language_code, parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_translate_text_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup request
        contents = []
        target_language_code = "targetLanguageCode1323228230"
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        with pytest.raises(CustomException):
            client.translate_text(contents, target_language_code, parent)

    def test_detect_language(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = translation_service_pb2.DetectLanguageResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        response = client.detect_language(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = translation_service_pb2.DetectLanguageRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_detect_language_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        with pytest.raises(CustomException):
            client.detect_language(parent)

    def test_get_supported_languages(self):
        # Setup Expected Response
        expected_response = {}
        expected_response = translation_service_pb2.SupportedLanguages(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        response = client.get_supported_languages(parent)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = translation_service_pb2.GetSupportedLanguagesRequest(
            parent=parent
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_supported_languages_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        with pytest.raises(CustomException):
            client.get_supported_languages(parent)

    def test_batch_translate_text(self):
        # Setup Expected Response
        total_characters = 1368640955
        translated_characters = 1337326221
        failed_characters = 1723028396
        expected_response = {
            "total_characters": total_characters,
            "translated_characters": translated_characters,
            "failed_characters": failed_characters,
        }
        expected_response = translation_service_pb2.BatchTranslateResponse(
            **expected_response
        )
        operation = operations_pb2.Operation(
            name="operations/test_batch_translate_text", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        source_language_code = "sourceLanguageCode1687263568"
        target_language_codes = []
        input_configs = []
        output_config = {}

        response = client.batch_translate_text(
            parent,
            source_language_code,
            target_language_codes,
            input_configs,
            output_config,
        )
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = translation_service_pb2.BatchTranslateTextRequest(
            parent=parent,
            source_language_code=source_language_code,
            target_language_codes=target_language_codes,
            input_configs=input_configs,
            output_config=output_config,
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_batch_translate_text_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_batch_translate_text_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        source_language_code = "sourceLanguageCode1687263568"
        target_language_codes = []
        input_configs = []
        output_config = {}

        response = client.batch_translate_text(
            parent,
            source_language_code,
            target_language_codes,
            input_configs,
            output_config,
        )
        exception = response.exception()
        assert exception.errors[0] == error

    def test_create_glossary(self):
        # Setup Expected Response
        name = "name3373707"
        entry_count = 811131134
        expected_response = {"name": name, "entry_count": entry_count}
        expected_response = translation_service_pb2.Glossary(**expected_response)
        operation = operations_pb2.Operation(
            name="operations/test_create_glossary", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        glossary = {}

        response = client.create_glossary(parent, glossary)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = translation_service_pb2.CreateGlossaryRequest(
            parent=parent, glossary=glossary
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_glossary_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_create_glossary_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")
        glossary = {}

        response = client.create_glossary(parent, glossary)
        exception = response.exception()
        assert exception.errors[0] == error

    def test_list_glossaries(self):
        # Setup Expected Response
        next_page_token = ""
        glossaries_element = {}
        glossaries = [glossaries_element]
        expected_response = {
            "next_page_token": next_page_token,
            "glossaries": glossaries,
        }
        expected_response = translation_service_pb2.ListGlossariesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_glossaries(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.glossaries[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = translation_service_pb2.ListGlossariesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_glossaries_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup request
        parent = client.location_path("[PROJECT]", "[LOCATION]")

        paged_list_response = client.list_glossaries(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)

    def test_get_glossary(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        entry_count = 811131134
        expected_response = {"name": name_2, "entry_count": entry_count}
        expected_response = translation_service_pb2.Glossary(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        name = client.glossary_path("[PROJECT]", "[LOCATION]", "[GLOSSARY]")

        response = client.get_glossary(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = translation_service_pb2.GetGlossaryRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_glossary_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup request
        name = client.glossary_path("[PROJECT]", "[LOCATION]", "[GLOSSARY]")

        with pytest.raises(CustomException):
            client.get_glossary(name)

    def test_delete_glossary(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        expected_response = {"name": name_2}
        expected_response = translation_service_pb2.DeleteGlossaryResponse(
            **expected_response
        )
        operation = operations_pb2.Operation(
            name="operations/test_delete_glossary", done=True
        )
        operation.response.Pack(expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        name = client.glossary_path("[PROJECT]", "[LOCATION]", "[GLOSSARY]")

        response = client.delete_glossary(name)
        result = response.result()
        assert expected_response == result

        assert len(channel.requests) == 1
        expected_request = translation_service_pb2.DeleteGlossaryRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_glossary_exception(self):
        # Setup Response
        error = status_pb2.Status()
        operation = operations_pb2.Operation(
            name="operations/test_delete_glossary_exception", done=True
        )
        operation.error.CopyFrom(error)

        # Mock the API response
        channel = ChannelStub(responses=[operation])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = translate_v3.TranslationServiceClient()

        # Setup Request
        name = client.glossary_path("[PROJECT]", "[LOCATION]", "[GLOSSARY]")

        response = client.delete_glossary(name)
        exception = response.exception()
        assert exception.errors[0] == error
