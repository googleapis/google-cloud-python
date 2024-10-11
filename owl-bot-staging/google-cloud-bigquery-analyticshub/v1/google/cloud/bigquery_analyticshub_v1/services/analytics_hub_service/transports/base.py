# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

from google.cloud.bigquery_analyticshub_v1 import gapic_version as package_version

import google.auth  # type: ignore
import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account # type: ignore

from google.cloud.bigquery_analyticshub_v1.types import analyticshub
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2 # type: ignore
from google.protobuf import empty_pb2  # type: ignore

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


class AnalyticsHubServiceTransport(abc.ABC):
    """Abstract transport class for AnalyticsHubService."""

    AUTH_SCOPES = (
        'https://www.googleapis.com/auth/bigquery',
        'https://www.googleapis.com/auth/cloud-platform',
    )

    DEFAULT_HOST: str = 'analyticshub.googleapis.com'
    def __init__(
            self, *,
            host: str = DEFAULT_HOST,
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            api_audience: Optional[str] = None,
            **kwargs,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'analyticshub.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes
        if not hasattr(self, "_ignore_credentials"):
            self._ignore_credentials: bool = False

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs("'credentials_file' and 'credentials' are mutually exclusive")

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                                credentials_file,
                                **scopes_kwargs,
                                quota_project_id=quota_project_id
                            )
        elif credentials is None and not self._ignore_credentials:
            credentials, _ = google.auth.default(**scopes_kwargs, quota_project_id=quota_project_id)
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(api_audience if api_audience else host)

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if always_use_jwt_access and isinstance(credentials, service_account.Credentials) and hasattr(service_account.Credentials, "with_always_use_jwt_access"):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ':' not in host:
            host += ':443'
        self._host = host

    @property
    def host(self):
        return self._host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_data_exchanges: gapic_v1.method.wrap_method(
                self.list_data_exchanges,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_org_data_exchanges: gapic_v1.method.wrap_method(
                self.list_org_data_exchanges,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_data_exchange: gapic_v1.method.wrap_method(
                self.get_data_exchange,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_data_exchange: gapic_v1.method.wrap_method(
                self.create_data_exchange,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_data_exchange: gapic_v1.method.wrap_method(
                self.update_data_exchange,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_data_exchange: gapic_v1.method.wrap_method(
                self.delete_data_exchange,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_listings: gapic_v1.method.wrap_method(
                self.list_listings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_listing: gapic_v1.method.wrap_method(
                self.get_listing,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_listing: gapic_v1.method.wrap_method(
                self.create_listing,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_listing: gapic_v1.method.wrap_method(
                self.update_listing,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_listing: gapic_v1.method.wrap_method(
                self.delete_listing,
                default_timeout=None,
                client_info=client_info,
            ),
            self.subscribe_listing: gapic_v1.method.wrap_method(
                self.subscribe_listing,
                default_timeout=None,
                client_info=client_info,
            ),
            self.subscribe_data_exchange: gapic_v1.method.wrap_method(
                self.subscribe_data_exchange,
                default_timeout=None,
                client_info=client_info,
            ),
            self.refresh_subscription: gapic_v1.method.wrap_method(
                self.refresh_subscription,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_subscription: gapic_v1.method.wrap_method(
                self.get_subscription,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_subscriptions: gapic_v1.method.wrap_method(
                self.list_subscriptions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_shared_resource_subscriptions: gapic_v1.method.wrap_method(
                self.list_shared_resource_subscriptions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.revoke_subscription: gapic_v1.method.wrap_method(
                self.revoke_subscription,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_subscription: gapic_v1.method.wrap_method(
                self.delete_subscription,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
         }

    def close(self):
        """Closes resources associated with the transport.

       .. warning::
            Only call this method if the transport is NOT shared
            with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def operations_client(self):
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_data_exchanges(self) -> Callable[
            [analyticshub.ListDataExchangesRequest],
            Union[
                analyticshub.ListDataExchangesResponse,
                Awaitable[analyticshub.ListDataExchangesResponse]
            ]]:
        raise NotImplementedError()

    @property
    def list_org_data_exchanges(self) -> Callable[
            [analyticshub.ListOrgDataExchangesRequest],
            Union[
                analyticshub.ListOrgDataExchangesResponse,
                Awaitable[analyticshub.ListOrgDataExchangesResponse]
            ]]:
        raise NotImplementedError()

    @property
    def get_data_exchange(self) -> Callable[
            [analyticshub.GetDataExchangeRequest],
            Union[
                analyticshub.DataExchange,
                Awaitable[analyticshub.DataExchange]
            ]]:
        raise NotImplementedError()

    @property
    def create_data_exchange(self) -> Callable[
            [analyticshub.CreateDataExchangeRequest],
            Union[
                analyticshub.DataExchange,
                Awaitable[analyticshub.DataExchange]
            ]]:
        raise NotImplementedError()

    @property
    def update_data_exchange(self) -> Callable[
            [analyticshub.UpdateDataExchangeRequest],
            Union[
                analyticshub.DataExchange,
                Awaitable[analyticshub.DataExchange]
            ]]:
        raise NotImplementedError()

    @property
    def delete_data_exchange(self) -> Callable[
            [analyticshub.DeleteDataExchangeRequest],
            Union[
                empty_pb2.Empty,
                Awaitable[empty_pb2.Empty]
            ]]:
        raise NotImplementedError()

    @property
    def list_listings(self) -> Callable[
            [analyticshub.ListListingsRequest],
            Union[
                analyticshub.ListListingsResponse,
                Awaitable[analyticshub.ListListingsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def get_listing(self) -> Callable[
            [analyticshub.GetListingRequest],
            Union[
                analyticshub.Listing,
                Awaitable[analyticshub.Listing]
            ]]:
        raise NotImplementedError()

    @property
    def create_listing(self) -> Callable[
            [analyticshub.CreateListingRequest],
            Union[
                analyticshub.Listing,
                Awaitable[analyticshub.Listing]
            ]]:
        raise NotImplementedError()

    @property
    def update_listing(self) -> Callable[
            [analyticshub.UpdateListingRequest],
            Union[
                analyticshub.Listing,
                Awaitable[analyticshub.Listing]
            ]]:
        raise NotImplementedError()

    @property
    def delete_listing(self) -> Callable[
            [analyticshub.DeleteListingRequest],
            Union[
                empty_pb2.Empty,
                Awaitable[empty_pb2.Empty]
            ]]:
        raise NotImplementedError()

    @property
    def subscribe_listing(self) -> Callable[
            [analyticshub.SubscribeListingRequest],
            Union[
                analyticshub.SubscribeListingResponse,
                Awaitable[analyticshub.SubscribeListingResponse]
            ]]:
        raise NotImplementedError()

    @property
    def subscribe_data_exchange(self) -> Callable[
            [analyticshub.SubscribeDataExchangeRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def refresh_subscription(self) -> Callable[
            [analyticshub.RefreshSubscriptionRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def get_subscription(self) -> Callable[
            [analyticshub.GetSubscriptionRequest],
            Union[
                analyticshub.Subscription,
                Awaitable[analyticshub.Subscription]
            ]]:
        raise NotImplementedError()

    @property
    def list_subscriptions(self) -> Callable[
            [analyticshub.ListSubscriptionsRequest],
            Union[
                analyticshub.ListSubscriptionsResponse,
                Awaitable[analyticshub.ListSubscriptionsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def list_shared_resource_subscriptions(self) -> Callable[
            [analyticshub.ListSharedResourceSubscriptionsRequest],
            Union[
                analyticshub.ListSharedResourceSubscriptionsResponse,
                Awaitable[analyticshub.ListSharedResourceSubscriptionsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def revoke_subscription(self) -> Callable[
            [analyticshub.RevokeSubscriptionRequest],
            Union[
                analyticshub.RevokeSubscriptionResponse,
                Awaitable[analyticshub.RevokeSubscriptionResponse]
            ]]:
        raise NotImplementedError()

    @property
    def delete_subscription(self) -> Callable[
            [analyticshub.DeleteSubscriptionRequest],
            Union[
                operations_pb2.Operation,
                Awaitable[operations_pb2.Operation]
            ]]:
        raise NotImplementedError()

    @property
    def get_iam_policy(self) -> Callable[
            [iam_policy_pb2.GetIamPolicyRequest],
            Union[
                policy_pb2.Policy,
                Awaitable[policy_pb2.Policy]
            ]]:
        raise NotImplementedError()

    @property
    def set_iam_policy(self) -> Callable[
            [iam_policy_pb2.SetIamPolicyRequest],
            Union[
                policy_pb2.Policy,
                Awaitable[policy_pb2.Policy]
            ]]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(self) -> Callable[
            [iam_policy_pb2.TestIamPermissionsRequest],
            Union[
                iam_policy_pb2.TestIamPermissionsResponse,
                Awaitable[iam_policy_pb2.TestIamPermissionsResponse]
            ]]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = (
    'AnalyticsHubServiceTransport',
)
