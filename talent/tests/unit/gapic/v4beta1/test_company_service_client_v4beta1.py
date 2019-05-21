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

from google.cloud import talent_v4beta1
from google.cloud.talent_v4beta1.proto import company_pb2
from google.cloud.talent_v4beta1.proto import company_service_pb2
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


class TestCompanyServiceClient(object):
    def test_create_company(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        external_id = "externalId-1153075697"
        headquarters_address = "headquartersAddress-1879520036"
        hiring_agency = False
        eeo_text = "eeoText-1652097123"
        website_uri = "websiteUri-2118185016"
        career_site_uri = "careerSiteUri1223331861"
        image_uri = "imageUri-877823864"
        suspended = False
        expected_response = {
            "name": name,
            "display_name": display_name,
            "external_id": external_id,
            "headquarters_address": headquarters_address,
            "hiring_agency": hiring_agency,
            "eeo_text": eeo_text,
            "website_uri": website_uri,
            "career_site_uri": career_site_uri,
            "image_uri": image_uri,
            "suspended": suspended,
        }
        expected_response = company_pb2.Company(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        company = {}

        response = client.create_company(parent, company)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = company_service_pb2.CreateCompanyRequest(
            parent=parent, company=company
        )
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_create_company_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")
        company = {}

        with pytest.raises(CustomException):
            client.create_company(parent, company)

    def test_get_company(self):
        # Setup Expected Response
        name_2 = "name2-1052831874"
        display_name = "displayName1615086568"
        external_id = "externalId-1153075697"
        headquarters_address = "headquartersAddress-1879520036"
        hiring_agency = False
        eeo_text = "eeoText-1652097123"
        website_uri = "websiteUri-2118185016"
        career_site_uri = "careerSiteUri1223331861"
        image_uri = "imageUri-877823864"
        suspended = False
        expected_response = {
            "name": name_2,
            "display_name": display_name,
            "external_id": external_id,
            "headquarters_address": headquarters_address,
            "hiring_agency": hiring_agency,
            "eeo_text": eeo_text,
            "website_uri": website_uri,
            "career_site_uri": career_site_uri,
            "image_uri": image_uri,
            "suspended": suspended,
        }
        expected_response = company_pb2.Company(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup Request
        name = client.company_path("[PROJECT]", "[TENANT]", "[COMPANY]")

        response = client.get_company(name)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = company_service_pb2.GetCompanyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_get_company_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup request
        name = client.company_path("[PROJECT]", "[TENANT]", "[COMPANY]")

        with pytest.raises(CustomException):
            client.get_company(name)

    def test_update_company(self):
        # Setup Expected Response
        name = "name3373707"
        display_name = "displayName1615086568"
        external_id = "externalId-1153075697"
        headquarters_address = "headquartersAddress-1879520036"
        hiring_agency = False
        eeo_text = "eeoText-1652097123"
        website_uri = "websiteUri-2118185016"
        career_site_uri = "careerSiteUri1223331861"
        image_uri = "imageUri-877823864"
        suspended = False
        expected_response = {
            "name": name,
            "display_name": display_name,
            "external_id": external_id,
            "headquarters_address": headquarters_address,
            "hiring_agency": hiring_agency,
            "eeo_text": eeo_text,
            "website_uri": website_uri,
            "career_site_uri": career_site_uri,
            "image_uri": image_uri,
            "suspended": suspended,
        }
        expected_response = company_pb2.Company(**expected_response)

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup Request
        company = {}

        response = client.update_company(company)
        assert expected_response == response

        assert len(channel.requests) == 1
        expected_request = company_service_pb2.UpdateCompanyRequest(company=company)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_update_company_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup request
        company = {}

        with pytest.raises(CustomException):
            client.update_company(company)

    def test_delete_company(self):
        channel = ChannelStub()
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup Request
        name = client.company_path("[PROJECT]", "[TENANT]", "[COMPANY]")

        client.delete_company(name)

        assert len(channel.requests) == 1
        expected_request = company_service_pb2.DeleteCompanyRequest(name=name)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_delete_company_exception(self):
        # Mock the API response
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup request
        name = client.company_path("[PROJECT]", "[TENANT]", "[COMPANY]")

        with pytest.raises(CustomException):
            client.delete_company(name)

    def test_list_companies(self):
        # Setup Expected Response
        next_page_token = ""
        companies_element = {}
        companies = [companies_element]
        expected_response = {"next_page_token": next_page_token, "companies": companies}
        expected_response = company_service_pb2.ListCompaniesResponse(
            **expected_response
        )

        # Mock the API response
        channel = ChannelStub(responses=[expected_response])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup Request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")

        paged_list_response = client.list_companies(parent)
        resources = list(paged_list_response)
        assert len(resources) == 1

        assert expected_response.companies[0] == resources[0]

        assert len(channel.requests) == 1
        expected_request = company_service_pb2.ListCompaniesRequest(parent=parent)
        actual_request = channel.requests[0][1]
        assert expected_request == actual_request

    def test_list_companies_exception(self):
        channel = ChannelStub(responses=[CustomException()])
        patch = mock.patch("google.api_core.grpc_helpers.create_channel")
        with patch as create_channel:
            create_channel.return_value = channel
            client = talent_v4beta1.CompanyServiceClient()

        # Setup request
        parent = client.tenant_path("[PROJECT]", "[TENANT]")

        paged_list_response = client.list_companies(parent)
        with pytest.raises(CustomException):
            list(paged_list_response)
