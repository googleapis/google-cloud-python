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
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import packaging.version
import pkg_resources

import google.auth  # type: ignore
import google.api_core  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.channel_v1.types import channel_partner_links
from google.cloud.channel_v1.types import customers
from google.cloud.channel_v1.types import entitlements
from google.cloud.channel_v1.types import offers
from google.cloud.channel_v1.types import service
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-channel",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()

try:
    # google.auth.__version__ was added in 1.26.0
    _GOOGLE_AUTH_VERSION = google.auth.__version__
except AttributeError:
    try:  # try pkg_resources if it is available
        _GOOGLE_AUTH_VERSION = pkg_resources.get_distribution("google-auth").version
    except pkg_resources.DistributionNotFound:  # pragma: NO COVER
        _GOOGLE_AUTH_VERSION = None


class CloudChannelServiceTransport(abc.ABC):
    """Abstract transport class for CloudChannelService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/apps.order",)

    DEFAULT_HOST: str = "cloudchannel.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
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
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        scopes_kwargs = self._get_scopes_kwargs(self._host, scopes)

        # Save the scopes.
        self._scopes = scopes

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )

        # If the credentials is service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

    # TODO(busunkim): This method is in the base transport
    # to avoid duplicating code across the transport classes. These functions
    # should be deleted once the minimum required versions of google-auth is increased.

    # TODO: Remove this function once google-auth >= 1.25.0 is required
    @classmethod
    def _get_scopes_kwargs(
        cls, host: str, scopes: Optional[Sequence[str]]
    ) -> Dict[str, Optional[Sequence[str]]]:
        """Returns scopes kwargs to pass to google-auth methods depending on the google-auth version"""

        scopes_kwargs = {}

        if _GOOGLE_AUTH_VERSION and (
            packaging.version.parse(_GOOGLE_AUTH_VERSION)
            >= packaging.version.parse("1.25.0")
        ):
            scopes_kwargs = {"scopes": scopes, "default_scopes": cls.AUTH_SCOPES}
        else:
            scopes_kwargs = {"scopes": scopes or cls.AUTH_SCOPES}

        return scopes_kwargs

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_customers: gapic_v1.method.wrap_method(
                self.list_customers, default_timeout=None, client_info=client_info,
            ),
            self.get_customer: gapic_v1.method.wrap_method(
                self.get_customer, default_timeout=None, client_info=client_info,
            ),
            self.check_cloud_identity_accounts_exist: gapic_v1.method.wrap_method(
                self.check_cloud_identity_accounts_exist,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_customer: gapic_v1.method.wrap_method(
                self.create_customer, default_timeout=None, client_info=client_info,
            ),
            self.update_customer: gapic_v1.method.wrap_method(
                self.update_customer, default_timeout=None, client_info=client_info,
            ),
            self.delete_customer: gapic_v1.method.wrap_method(
                self.delete_customer, default_timeout=None, client_info=client_info,
            ),
            self.provision_cloud_identity: gapic_v1.method.wrap_method(
                self.provision_cloud_identity,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_entitlements: gapic_v1.method.wrap_method(
                self.list_entitlements, default_timeout=None, client_info=client_info,
            ),
            self.list_transferable_skus: gapic_v1.method.wrap_method(
                self.list_transferable_skus,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_transferable_offers: gapic_v1.method.wrap_method(
                self.list_transferable_offers,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_entitlement: gapic_v1.method.wrap_method(
                self.get_entitlement, default_timeout=None, client_info=client_info,
            ),
            self.create_entitlement: gapic_v1.method.wrap_method(
                self.create_entitlement, default_timeout=60.0, client_info=client_info,
            ),
            self.change_parameters: gapic_v1.method.wrap_method(
                self.change_parameters, default_timeout=60.0, client_info=client_info,
            ),
            self.change_renewal_settings: gapic_v1.method.wrap_method(
                self.change_renewal_settings,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.change_offer: gapic_v1.method.wrap_method(
                self.change_offer, default_timeout=60.0, client_info=client_info,
            ),
            self.start_paid_service: gapic_v1.method.wrap_method(
                self.start_paid_service, default_timeout=60.0, client_info=client_info,
            ),
            self.suspend_entitlement: gapic_v1.method.wrap_method(
                self.suspend_entitlement, default_timeout=60.0, client_info=client_info,
            ),
            self.cancel_entitlement: gapic_v1.method.wrap_method(
                self.cancel_entitlement, default_timeout=60.0, client_info=client_info,
            ),
            self.activate_entitlement: gapic_v1.method.wrap_method(
                self.activate_entitlement,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.transfer_entitlements: gapic_v1.method.wrap_method(
                self.transfer_entitlements,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.transfer_entitlements_to_google: gapic_v1.method.wrap_method(
                self.transfer_entitlements_to_google,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_channel_partner_links: gapic_v1.method.wrap_method(
                self.list_channel_partner_links,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_channel_partner_link: gapic_v1.method.wrap_method(
                self.get_channel_partner_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_channel_partner_link: gapic_v1.method.wrap_method(
                self.create_channel_partner_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_channel_partner_link: gapic_v1.method.wrap_method(
                self.update_channel_partner_link,
                default_timeout=None,
                client_info=client_info,
            ),
            self.lookup_offer: gapic_v1.method.wrap_method(
                self.lookup_offer, default_timeout=None, client_info=client_info,
            ),
            self.list_products: gapic_v1.method.wrap_method(
                self.list_products, default_timeout=None, client_info=client_info,
            ),
            self.list_skus: gapic_v1.method.wrap_method(
                self.list_skus, default_timeout=None, client_info=client_info,
            ),
            self.list_offers: gapic_v1.method.wrap_method(
                self.list_offers, default_timeout=None, client_info=client_info,
            ),
            self.list_purchasable_skus: gapic_v1.method.wrap_method(
                self.list_purchasable_skus,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_purchasable_offers: gapic_v1.method.wrap_method(
                self.list_purchasable_offers,
                default_timeout=None,
                client_info=client_info,
            ),
            self.register_subscriber: gapic_v1.method.wrap_method(
                self.register_subscriber, default_timeout=None, client_info=client_info,
            ),
            self.unregister_subscriber: gapic_v1.method.wrap_method(
                self.unregister_subscriber,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_subscribers: gapic_v1.method.wrap_method(
                self.list_subscribers, default_timeout=None, client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_customers(
        self,
    ) -> Callable[
        [service.ListCustomersRequest],
        Union[service.ListCustomersResponse, Awaitable[service.ListCustomersResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_customer(
        self,
    ) -> Callable[
        [service.GetCustomerRequest],
        Union[customers.Customer, Awaitable[customers.Customer]],
    ]:
        raise NotImplementedError()

    @property
    def check_cloud_identity_accounts_exist(
        self,
    ) -> Callable[
        [service.CheckCloudIdentityAccountsExistRequest],
        Union[
            service.CheckCloudIdentityAccountsExistResponse,
            Awaitable[service.CheckCloudIdentityAccountsExistResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_customer(
        self,
    ) -> Callable[
        [service.CreateCustomerRequest],
        Union[customers.Customer, Awaitable[customers.Customer]],
    ]:
        raise NotImplementedError()

    @property
    def update_customer(
        self,
    ) -> Callable[
        [service.UpdateCustomerRequest],
        Union[customers.Customer, Awaitable[customers.Customer]],
    ]:
        raise NotImplementedError()

    @property
    def delete_customer(
        self,
    ) -> Callable[
        [service.DeleteCustomerRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def provision_cloud_identity(
        self,
    ) -> Callable[
        [service.ProvisionCloudIdentityRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_entitlements(
        self,
    ) -> Callable[
        [service.ListEntitlementsRequest],
        Union[
            service.ListEntitlementsResponse,
            Awaitable[service.ListEntitlementsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_transferable_skus(
        self,
    ) -> Callable[
        [service.ListTransferableSkusRequest],
        Union[
            service.ListTransferableSkusResponse,
            Awaitable[service.ListTransferableSkusResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_transferable_offers(
        self,
    ) -> Callable[
        [service.ListTransferableOffersRequest],
        Union[
            service.ListTransferableOffersResponse,
            Awaitable[service.ListTransferableOffersResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_entitlement(
        self,
    ) -> Callable[
        [service.GetEntitlementRequest],
        Union[entitlements.Entitlement, Awaitable[entitlements.Entitlement]],
    ]:
        raise NotImplementedError()

    @property
    def create_entitlement(
        self,
    ) -> Callable[
        [service.CreateEntitlementRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def change_parameters(
        self,
    ) -> Callable[
        [service.ChangeParametersRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def change_renewal_settings(
        self,
    ) -> Callable[
        [service.ChangeRenewalSettingsRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def change_offer(
        self,
    ) -> Callable[
        [service.ChangeOfferRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start_paid_service(
        self,
    ) -> Callable[
        [service.StartPaidServiceRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def suspend_entitlement(
        self,
    ) -> Callable[
        [service.SuspendEntitlementRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_entitlement(
        self,
    ) -> Callable[
        [service.CancelEntitlementRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def activate_entitlement(
        self,
    ) -> Callable[
        [service.ActivateEntitlementRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def transfer_entitlements(
        self,
    ) -> Callable[
        [service.TransferEntitlementsRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def transfer_entitlements_to_google(
        self,
    ) -> Callable[
        [service.TransferEntitlementsToGoogleRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_channel_partner_links(
        self,
    ) -> Callable[
        [service.ListChannelPartnerLinksRequest],
        Union[
            service.ListChannelPartnerLinksResponse,
            Awaitable[service.ListChannelPartnerLinksResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_channel_partner_link(
        self,
    ) -> Callable[
        [service.GetChannelPartnerLinkRequest],
        Union[
            channel_partner_links.ChannelPartnerLink,
            Awaitable[channel_partner_links.ChannelPartnerLink],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_channel_partner_link(
        self,
    ) -> Callable[
        [service.CreateChannelPartnerLinkRequest],
        Union[
            channel_partner_links.ChannelPartnerLink,
            Awaitable[channel_partner_links.ChannelPartnerLink],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_channel_partner_link(
        self,
    ) -> Callable[
        [service.UpdateChannelPartnerLinkRequest],
        Union[
            channel_partner_links.ChannelPartnerLink,
            Awaitable[channel_partner_links.ChannelPartnerLink],
        ],
    ]:
        raise NotImplementedError()

    @property
    def lookup_offer(
        self,
    ) -> Callable[
        [service.LookupOfferRequest], Union[offers.Offer, Awaitable[offers.Offer]]
    ]:
        raise NotImplementedError()

    @property
    def list_products(
        self,
    ) -> Callable[
        [service.ListProductsRequest],
        Union[service.ListProductsResponse, Awaitable[service.ListProductsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def list_skus(
        self,
    ) -> Callable[
        [service.ListSkusRequest],
        Union[service.ListSkusResponse, Awaitable[service.ListSkusResponse]],
    ]:
        raise NotImplementedError()

    @property
    def list_offers(
        self,
    ) -> Callable[
        [service.ListOffersRequest],
        Union[service.ListOffersResponse, Awaitable[service.ListOffersResponse]],
    ]:
        raise NotImplementedError()

    @property
    def list_purchasable_skus(
        self,
    ) -> Callable[
        [service.ListPurchasableSkusRequest],
        Union[
            service.ListPurchasableSkusResponse,
            Awaitable[service.ListPurchasableSkusResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_purchasable_offers(
        self,
    ) -> Callable[
        [service.ListPurchasableOffersRequest],
        Union[
            service.ListPurchasableOffersResponse,
            Awaitable[service.ListPurchasableOffersResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def register_subscriber(
        self,
    ) -> Callable[
        [service.RegisterSubscriberRequest],
        Union[
            service.RegisterSubscriberResponse,
            Awaitable[service.RegisterSubscriberResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def unregister_subscriber(
        self,
    ) -> Callable[
        [service.UnregisterSubscriberRequest],
        Union[
            service.UnregisterSubscriberResponse,
            Awaitable[service.UnregisterSubscriberResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_subscribers(
        self,
    ) -> Callable[
        [service.ListSubscribersRequest],
        Union[
            service.ListSubscribersResponse, Awaitable[service.ListSubscribersResponse]
        ],
    ]:
        raise NotImplementedError()


__all__ = ("CloudChannelServiceTransport",)
