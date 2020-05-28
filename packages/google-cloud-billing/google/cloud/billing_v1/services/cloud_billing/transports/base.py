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

import abc
import typing

from google import auth
from google.auth import credentials  # type: ignore

from google.cloud.billing_v1.types import cloud_billing
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore


class CloudBillingTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for CloudBilling."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "cloudbilling.googleapis.com",
        credentials: credentials.Credentials = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def get_billing_account(
        self
    ) -> typing.Callable[
        [cloud_billing.GetBillingAccountRequest], cloud_billing.BillingAccount
    ]:
        raise NotImplementedError

    @property
    def list_billing_accounts(
        self
    ) -> typing.Callable[
        [cloud_billing.ListBillingAccountsRequest],
        cloud_billing.ListBillingAccountsResponse,
    ]:
        raise NotImplementedError

    @property
    def update_billing_account(
        self
    ) -> typing.Callable[
        [cloud_billing.UpdateBillingAccountRequest], cloud_billing.BillingAccount
    ]:
        raise NotImplementedError

    @property
    def create_billing_account(
        self
    ) -> typing.Callable[
        [cloud_billing.CreateBillingAccountRequest], cloud_billing.BillingAccount
    ]:
        raise NotImplementedError

    @property
    def list_project_billing_info(
        self
    ) -> typing.Callable[
        [cloud_billing.ListProjectBillingInfoRequest],
        cloud_billing.ListProjectBillingInfoResponse,
    ]:
        raise NotImplementedError

    @property
    def get_project_billing_info(
        self
    ) -> typing.Callable[
        [cloud_billing.GetProjectBillingInfoRequest], cloud_billing.ProjectBillingInfo
    ]:
        raise NotImplementedError

    @property
    def update_project_billing_info(
        self
    ) -> typing.Callable[
        [cloud_billing.UpdateProjectBillingInfoRequest],
        cloud_billing.ProjectBillingInfo,
    ]:
        raise NotImplementedError

    @property
    def get_iam_policy(
        self
    ) -> typing.Callable[[iam_policy.GetIamPolicyRequest], policy.Policy]:
        raise NotImplementedError

    @property
    def set_iam_policy(
        self
    ) -> typing.Callable[[iam_policy.SetIamPolicyRequest], policy.Policy]:
        raise NotImplementedError

    @property
    def test_iam_permissions(
        self
    ) -> typing.Callable[
        [iam_policy.TestIamPermissionsRequest], iam_policy.TestIamPermissionsResponse
    ]:
        raise NotImplementedError


__all__ = ("CloudBillingTransport",)
