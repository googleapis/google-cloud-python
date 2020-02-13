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
from google.auth import credentials
from google.cloud.billing_v1.services.cloud_billing import CloudBillingClient
from google.cloud.billing_v1.services.cloud_billing import pagers
from google.cloud.billing_v1.services.cloud_billing import transports
from google.cloud.billing_v1.types import cloud_billing
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.oauth2 import service_account


def test_cloud_billing_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = CloudBillingClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = CloudBillingClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "cloudbilling.googleapis.com:443"


def test_cloud_billing_client_client_options():
    # Check the default options have their expected values.
    assert (
        CloudBillingClient.DEFAULT_OPTIONS.api_endpoint == "cloudbilling.googleapis.com"
    )

    # Check that options can be customized.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.CloudBillingClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = CloudBillingClient(client_options=options)
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_cloud_billing_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.billing_v1.services.cloud_billing.CloudBillingClient.get_transport_class"
    ) as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = CloudBillingClient(client_options={"api_endpoint": "squid.clam.whelk"})
        transport.assert_called_once_with(credentials=None, host="squid.clam.whelk")


def test_get_billing_account(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.GetBillingAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount(
            name="name_value",
            open=True,
            display_name="display_name_value",
            master_billing_account="master_billing_account_value",
        )

        response = client.get_billing_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.BillingAccount)
    assert response.name == "name_value"
    assert response.open == True
    assert response.display_name == "display_name_value"
    assert response.master_billing_account == "master_billing_account_value"


def test_get_billing_account_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_billing.GetBillingAccountRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_billing_account), "__call__"
    ) as call:
        call.return_value = cloud_billing.BillingAccount()
        response = client.get_billing_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_billing_account_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_billing_account(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_billing_account_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_billing_account(
            cloud_billing.GetBillingAccountRequest(), name="name_value"
        )


def test_list_billing_accounts(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.ListBillingAccountsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_billing_accounts), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ListBillingAccountsResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_billing_accounts(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBillingAccountsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_billing_accounts_pager():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_billing_accounts), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                ],
                next_page_token="abc",
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[], next_page_token="def"
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[cloud_billing.BillingAccount()], next_page_token="ghi"
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_billing_accounts(request={})]
        assert len(results) == 6
        assert all([isinstance(i, cloud_billing.BillingAccount) for i in results])


def test_list_billing_accounts_pages():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_billing_accounts), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                ],
                next_page_token="abc",
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[], next_page_token="def"
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[cloud_billing.BillingAccount()], next_page_token="ghi"
            ),
            cloud_billing.ListBillingAccountsResponse(
                billing_accounts=[
                    cloud_billing.BillingAccount(),
                    cloud_billing.BillingAccount(),
                ]
            ),
            RuntimeError,
        )
        pages = list(client.list_billing_accounts(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_update_billing_account(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.UpdateBillingAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount(
            name="name_value",
            open=True,
            display_name="display_name_value",
            master_billing_account="master_billing_account_value",
        )

        response = client.update_billing_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.BillingAccount)
    assert response.name == "name_value"
    assert response.open == True
    assert response.display_name == "display_name_value"
    assert response.master_billing_account == "master_billing_account_value"


def test_update_billing_account_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_billing_account(
            name="name_value", account=cloud_billing.BillingAccount(name="name_value")
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].account == cloud_billing.BillingAccount(name="name_value")


def test_update_billing_account_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_billing_account(
            cloud_billing.UpdateBillingAccountRequest(),
            name="name_value",
            account=cloud_billing.BillingAccount(name="name_value"),
        )


def test_create_billing_account(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.CreateBillingAccountRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount(
            name="name_value",
            open=True,
            display_name="display_name_value",
            master_billing_account="master_billing_account_value",
        )

        response = client.create_billing_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.BillingAccount)
    assert response.name == "name_value"
    assert response.open == True
    assert response.display_name == "display_name_value"
    assert response.master_billing_account == "master_billing_account_value"


def test_create_billing_account_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_billing_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.BillingAccount()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_billing_account(
            billing_account=cloud_billing.BillingAccount(name="name_value")
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].billing_account == cloud_billing.BillingAccount(
            name="name_value"
        )


def test_create_billing_account_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_billing_account(
            cloud_billing.CreateBillingAccountRequest(),
            billing_account=cloud_billing.BillingAccount(name="name_value"),
        )


def test_list_project_billing_info(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.ListProjectBillingInfoRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ListProjectBillingInfoResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListProjectBillingInfoPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_project_billing_info_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_billing.ListProjectBillingInfoRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        call.return_value = cloud_billing.ListProjectBillingInfoResponse()
        response = client.list_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_list_project_billing_info_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ListProjectBillingInfoResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_project_billing_info(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_list_project_billing_info_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_project_billing_info(
            cloud_billing.ListProjectBillingInfoRequest(), name="name_value"
        )


def test_list_project_billing_info_pager():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                ],
                next_page_token="abc",
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[], next_page_token="def"
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[cloud_billing.ProjectBillingInfo()],
                next_page_token="ghi",
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                ]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_project_billing_info(request={})]
        assert len(results) == 6
        assert all([isinstance(i, cloud_billing.ProjectBillingInfo) for i in results])


def test_list_project_billing_info_pages():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_project_billing_info), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                ],
                next_page_token="abc",
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[], next_page_token="def"
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[cloud_billing.ProjectBillingInfo()],
                next_page_token="ghi",
            ),
            cloud_billing.ListProjectBillingInfoResponse(
                project_billing_info=[
                    cloud_billing.ProjectBillingInfo(),
                    cloud_billing.ProjectBillingInfo(),
                ]
            ),
            RuntimeError,
        )
        pages = list(client.list_project_billing_info(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_project_billing_info(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.GetProjectBillingInfoRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ProjectBillingInfo(
            name="name_value",
            project_id="project_id_value",
            billing_account_name="billing_account_name_value",
            billing_enabled=True,
        )

        response = client.get_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.ProjectBillingInfo)
    assert response.name == "name_value"
    assert response.project_id == "project_id_value"
    assert response.billing_account_name == "billing_account_name_value"
    assert response.billing_enabled == True


def test_get_project_billing_info_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_billing.GetProjectBillingInfoRequest(name="name/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_project_billing_info), "__call__"
    ) as call:
        call.return_value = cloud_billing.ProjectBillingInfo()
        response = client.get_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_project_billing_info_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.get_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ProjectBillingInfo()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_project_billing_info(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_project_billing_info_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_project_billing_info(
            cloud_billing.GetProjectBillingInfoRequest(), name="name_value"
        )


def test_update_project_billing_info(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = cloud_billing.UpdateProjectBillingInfoRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ProjectBillingInfo(
            name="name_value",
            project_id="project_id_value",
            billing_account_name="billing_account_name_value",
            billing_enabled=True,
        )

        response = client.update_project_billing_info(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_billing.ProjectBillingInfo)
    assert response.name == "name_value"
    assert response.project_id == "project_id_value"
    assert response.billing_account_name == "billing_account_name_value"
    assert response.billing_enabled == True


def test_update_project_billing_info_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_project_billing_info), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_billing.ProjectBillingInfo()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_project_billing_info(
            name="name_value",
            project_billing_info=cloud_billing.ProjectBillingInfo(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].project_billing_info == cloud_billing.ProjectBillingInfo(
            name="name_value"
        )


def test_update_project_billing_info_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_project_billing_info(
            cloud_billing.UpdateProjectBillingInfoRequest(),
            name="name_value",
            project_billing_info=cloud_billing.ProjectBillingInfo(name="name_value"),
        )


def test_get_iam_policy(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob")

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest(resource="resource/value")

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()
        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value") in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.get_iam_policy(request={"resource": "resource_value"})
        call.assert_called()


def test_get_iam_policy_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_iam_policy(resource="resource_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].resource == "resource_value"


def test_get_iam_policy_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            iam_policy.GetIamPolicyRequest(), resource="resource_value"
        )


def test_set_iam_policy(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob")

        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_from_dict():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.set_iam_policy(
            request={"resource": "resource_value", "policy": policy.Policy(version=774)}
        )
        call.assert_called()


def test_set_iam_policy_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.set_iam_policy(resource="resource_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].resource == "resource_value"


def test_set_iam_policy_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            iam_policy.SetIamPolicyRequest(), resource="resource_value"
        )


def test_test_iam_permissions(transport: str = "grpc"):
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse(
            permissions=["permissions_value"]
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_from_dict():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={"resource": "resource_value", "permissions": ["permissions_value"]}
        )
        call.assert_called()


def test_test_iam_permissions_flattened():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.test_iam_permissions(
            resource="resource_value", permissions=["permissions_value"]
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].resource == "resource_value"
        assert args[0].permissions == ["permissions_value"]


def test_test_iam_permissions_flattened_error():
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            iam_policy.TestIamPermissionsRequest(),
            resource="resource_value",
            permissions=["permissions_value"],
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudBillingGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = CloudBillingClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudBillingGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = CloudBillingClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudBillingClient(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.CloudBillingGrpcTransport)


def test_cloud_billing_base_transport():
    # Instantiate the base transport.
    transport = transports.CloudBillingTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "get_billing_account",
        "list_billing_accounts",
        "update_billing_account",
        "create_billing_account",
        "list_project_billing_info",
        "get_project_billing_info",
        "update_project_billing_info",
        "get_iam_policy",
        "set_iam_policy",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_cloud_billing_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        client = CloudBillingClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_cloud_billing_host_no_port():
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbilling.googleapis.com"
        ),
        transport="grpc",
    )
    assert client._transport._host == "cloudbilling.googleapis.com:443"


def test_cloud_billing_host_with_port():
    client = CloudBillingClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudbilling.googleapis.com:8000"
        ),
        transport="grpc",
    )
    assert client._transport._host == "cloudbilling.googleapis.com:8000"


def test_cloud_billing_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")
    transport = transports.CloudBillingGrpcTransport(channel=channel)
    assert transport.grpc_channel is channel
