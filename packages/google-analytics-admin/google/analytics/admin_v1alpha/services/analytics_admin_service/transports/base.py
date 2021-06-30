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
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.analytics.admin_v1alpha.types import analytics_admin
from google.analytics.admin_v1alpha.types import resources
from google.protobuf import empty_pb2  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-analytics-admin",).version,
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


class AnalyticsAdminServiceTransport(abc.ABC):
    """Abstract transport class for AnalyticsAdminService."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/analytics.edit",
        "https://www.googleapis.com/auth/analytics.manage.users",
        "https://www.googleapis.com/auth/analytics.manage.users.readonly",
        "https://www.googleapis.com/auth/analytics.readonly",
    )

    DEFAULT_HOST: str = "analyticsadmin.googleapis.com"

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
            self.get_account: gapic_v1.method.wrap_method(
                self.get_account, default_timeout=60.0, client_info=client_info,
            ),
            self.list_accounts: gapic_v1.method.wrap_method(
                self.list_accounts, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_account: gapic_v1.method.wrap_method(
                self.delete_account, default_timeout=60.0, client_info=client_info,
            ),
            self.update_account: gapic_v1.method.wrap_method(
                self.update_account, default_timeout=60.0, client_info=client_info,
            ),
            self.provision_account_ticket: gapic_v1.method.wrap_method(
                self.provision_account_ticket,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_account_summaries: gapic_v1.method.wrap_method(
                self.list_account_summaries,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_property: gapic_v1.method.wrap_method(
                self.get_property, default_timeout=60.0, client_info=client_info,
            ),
            self.list_properties: gapic_v1.method.wrap_method(
                self.list_properties, default_timeout=60.0, client_info=client_info,
            ),
            self.create_property: gapic_v1.method.wrap_method(
                self.create_property, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_property: gapic_v1.method.wrap_method(
                self.delete_property, default_timeout=60.0, client_info=client_info,
            ),
            self.update_property: gapic_v1.method.wrap_method(
                self.update_property, default_timeout=60.0, client_info=client_info,
            ),
            self.get_user_link: gapic_v1.method.wrap_method(
                self.get_user_link, default_timeout=60.0, client_info=client_info,
            ),
            self.batch_get_user_links: gapic_v1.method.wrap_method(
                self.batch_get_user_links,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_user_links: gapic_v1.method.wrap_method(
                self.list_user_links, default_timeout=60.0, client_info=client_info,
            ),
            self.audit_user_links: gapic_v1.method.wrap_method(
                self.audit_user_links, default_timeout=60.0, client_info=client_info,
            ),
            self.create_user_link: gapic_v1.method.wrap_method(
                self.create_user_link, default_timeout=60.0, client_info=client_info,
            ),
            self.batch_create_user_links: gapic_v1.method.wrap_method(
                self.batch_create_user_links,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_user_link: gapic_v1.method.wrap_method(
                self.update_user_link, default_timeout=60.0, client_info=client_info,
            ),
            self.batch_update_user_links: gapic_v1.method.wrap_method(
                self.batch_update_user_links,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_user_link: gapic_v1.method.wrap_method(
                self.delete_user_link, default_timeout=60.0, client_info=client_info,
            ),
            self.batch_delete_user_links: gapic_v1.method.wrap_method(
                self.batch_delete_user_links,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_web_data_stream: gapic_v1.method.wrap_method(
                self.get_web_data_stream, default_timeout=60.0, client_info=client_info,
            ),
            self.delete_web_data_stream: gapic_v1.method.wrap_method(
                self.delete_web_data_stream,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_web_data_stream: gapic_v1.method.wrap_method(
                self.update_web_data_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_web_data_stream: gapic_v1.method.wrap_method(
                self.create_web_data_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_web_data_streams: gapic_v1.method.wrap_method(
                self.list_web_data_streams,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_ios_app_data_stream: gapic_v1.method.wrap_method(
                self.get_ios_app_data_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_ios_app_data_stream: gapic_v1.method.wrap_method(
                self.delete_ios_app_data_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_ios_app_data_stream: gapic_v1.method.wrap_method(
                self.update_ios_app_data_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_ios_app_data_streams: gapic_v1.method.wrap_method(
                self.list_ios_app_data_streams,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_android_app_data_stream: gapic_v1.method.wrap_method(
                self.get_android_app_data_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_android_app_data_stream: gapic_v1.method.wrap_method(
                self.delete_android_app_data_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_android_app_data_stream: gapic_v1.method.wrap_method(
                self.update_android_app_data_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_android_app_data_streams: gapic_v1.method.wrap_method(
                self.list_android_app_data_streams,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_enhanced_measurement_settings: gapic_v1.method.wrap_method(
                self.get_enhanced_measurement_settings,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_enhanced_measurement_settings: gapic_v1.method.wrap_method(
                self.update_enhanced_measurement_settings,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_firebase_link: gapic_v1.method.wrap_method(
                self.create_firebase_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_firebase_link: gapic_v1.method.wrap_method(
                self.update_firebase_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_firebase_link: gapic_v1.method.wrap_method(
                self.delete_firebase_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_firebase_links: gapic_v1.method.wrap_method(
                self.list_firebase_links, default_timeout=60.0, client_info=client_info,
            ),
            self.get_global_site_tag: gapic_v1.method.wrap_method(
                self.get_global_site_tag, default_timeout=60.0, client_info=client_info,
            ),
            self.create_google_ads_link: gapic_v1.method.wrap_method(
                self.create_google_ads_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_google_ads_link: gapic_v1.method.wrap_method(
                self.update_google_ads_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_google_ads_link: gapic_v1.method.wrap_method(
                self.delete_google_ads_link,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_google_ads_links: gapic_v1.method.wrap_method(
                self.list_google_ads_links,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_data_sharing_settings: gapic_v1.method.wrap_method(
                self.get_data_sharing_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_measurement_protocol_secret: gapic_v1.method.wrap_method(
                self.get_measurement_protocol_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_measurement_protocol_secrets: gapic_v1.method.wrap_method(
                self.list_measurement_protocol_secrets,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_measurement_protocol_secret: gapic_v1.method.wrap_method(
                self.create_measurement_protocol_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_measurement_protocol_secret: gapic_v1.method.wrap_method(
                self.delete_measurement_protocol_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_measurement_protocol_secret: gapic_v1.method.wrap_method(
                self.update_measurement_protocol_secret,
                default_timeout=None,
                client_info=client_info,
            ),
            self.search_change_history_events: gapic_v1.method.wrap_method(
                self.search_change_history_events,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_google_signals_settings: gapic_v1.method.wrap_method(
                self.get_google_signals_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_google_signals_settings: gapic_v1.method.wrap_method(
                self.update_google_signals_settings,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_conversion_event: gapic_v1.method.wrap_method(
                self.create_conversion_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_conversion_event: gapic_v1.method.wrap_method(
                self.get_conversion_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_conversion_event: gapic_v1.method.wrap_method(
                self.delete_conversion_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_conversion_events: gapic_v1.method.wrap_method(
                self.list_conversion_events,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_custom_dimension: gapic_v1.method.wrap_method(
                self.create_custom_dimension,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_custom_dimension: gapic_v1.method.wrap_method(
                self.update_custom_dimension,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_custom_dimensions: gapic_v1.method.wrap_method(
                self.list_custom_dimensions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.archive_custom_dimension: gapic_v1.method.wrap_method(
                self.archive_custom_dimension,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_custom_dimension: gapic_v1.method.wrap_method(
                self.get_custom_dimension,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_custom_metric: gapic_v1.method.wrap_method(
                self.create_custom_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_custom_metric: gapic_v1.method.wrap_method(
                self.update_custom_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_custom_metrics: gapic_v1.method.wrap_method(
                self.list_custom_metrics, default_timeout=None, client_info=client_info,
            ),
            self.archive_custom_metric: gapic_v1.method.wrap_method(
                self.archive_custom_metric,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_custom_metric: gapic_v1.method.wrap_method(
                self.get_custom_metric, default_timeout=None, client_info=client_info,
            ),
        }

    @property
    def get_account(
        self,
    ) -> Callable[
        [analytics_admin.GetAccountRequest],
        Union[resources.Account, Awaitable[resources.Account]],
    ]:
        raise NotImplementedError()

    @property
    def list_accounts(
        self,
    ) -> Callable[
        [analytics_admin.ListAccountsRequest],
        Union[
            analytics_admin.ListAccountsResponse,
            Awaitable[analytics_admin.ListAccountsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_account(
        self,
    ) -> Callable[
        [analytics_admin.DeleteAccountRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_account(
        self,
    ) -> Callable[
        [analytics_admin.UpdateAccountRequest],
        Union[resources.Account, Awaitable[resources.Account]],
    ]:
        raise NotImplementedError()

    @property
    def provision_account_ticket(
        self,
    ) -> Callable[
        [analytics_admin.ProvisionAccountTicketRequest],
        Union[
            analytics_admin.ProvisionAccountTicketResponse,
            Awaitable[analytics_admin.ProvisionAccountTicketResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_account_summaries(
        self,
    ) -> Callable[
        [analytics_admin.ListAccountSummariesRequest],
        Union[
            analytics_admin.ListAccountSummariesResponse,
            Awaitable[analytics_admin.ListAccountSummariesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_property(
        self,
    ) -> Callable[
        [analytics_admin.GetPropertyRequest],
        Union[resources.Property, Awaitable[resources.Property]],
    ]:
        raise NotImplementedError()

    @property
    def list_properties(
        self,
    ) -> Callable[
        [analytics_admin.ListPropertiesRequest],
        Union[
            analytics_admin.ListPropertiesResponse,
            Awaitable[analytics_admin.ListPropertiesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_property(
        self,
    ) -> Callable[
        [analytics_admin.CreatePropertyRequest],
        Union[resources.Property, Awaitable[resources.Property]],
    ]:
        raise NotImplementedError()

    @property
    def delete_property(
        self,
    ) -> Callable[
        [analytics_admin.DeletePropertyRequest],
        Union[resources.Property, Awaitable[resources.Property]],
    ]:
        raise NotImplementedError()

    @property
    def update_property(
        self,
    ) -> Callable[
        [analytics_admin.UpdatePropertyRequest],
        Union[resources.Property, Awaitable[resources.Property]],
    ]:
        raise NotImplementedError()

    @property
    def get_user_link(
        self,
    ) -> Callable[
        [analytics_admin.GetUserLinkRequest],
        Union[resources.UserLink, Awaitable[resources.UserLink]],
    ]:
        raise NotImplementedError()

    @property
    def batch_get_user_links(
        self,
    ) -> Callable[
        [analytics_admin.BatchGetUserLinksRequest],
        Union[
            analytics_admin.BatchGetUserLinksResponse,
            Awaitable[analytics_admin.BatchGetUserLinksResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_user_links(
        self,
    ) -> Callable[
        [analytics_admin.ListUserLinksRequest],
        Union[
            analytics_admin.ListUserLinksResponse,
            Awaitable[analytics_admin.ListUserLinksResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def audit_user_links(
        self,
    ) -> Callable[
        [analytics_admin.AuditUserLinksRequest],
        Union[
            analytics_admin.AuditUserLinksResponse,
            Awaitable[analytics_admin.AuditUserLinksResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_user_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateUserLinkRequest],
        Union[resources.UserLink, Awaitable[resources.UserLink]],
    ]:
        raise NotImplementedError()

    @property
    def batch_create_user_links(
        self,
    ) -> Callable[
        [analytics_admin.BatchCreateUserLinksRequest],
        Union[
            analytics_admin.BatchCreateUserLinksResponse,
            Awaitable[analytics_admin.BatchCreateUserLinksResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_user_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateUserLinkRequest],
        Union[resources.UserLink, Awaitable[resources.UserLink]],
    ]:
        raise NotImplementedError()

    @property
    def batch_update_user_links(
        self,
    ) -> Callable[
        [analytics_admin.BatchUpdateUserLinksRequest],
        Union[
            analytics_admin.BatchUpdateUserLinksResponse,
            Awaitable[analytics_admin.BatchUpdateUserLinksResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_user_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteUserLinkRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def batch_delete_user_links(
        self,
    ) -> Callable[
        [analytics_admin.BatchDeleteUserLinksRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_web_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.GetWebDataStreamRequest],
        Union[resources.WebDataStream, Awaitable[resources.WebDataStream]],
    ]:
        raise NotImplementedError()

    @property
    def delete_web_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.DeleteWebDataStreamRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_web_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.UpdateWebDataStreamRequest],
        Union[resources.WebDataStream, Awaitable[resources.WebDataStream]],
    ]:
        raise NotImplementedError()

    @property
    def create_web_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.CreateWebDataStreamRequest],
        Union[resources.WebDataStream, Awaitable[resources.WebDataStream]],
    ]:
        raise NotImplementedError()

    @property
    def list_web_data_streams(
        self,
    ) -> Callable[
        [analytics_admin.ListWebDataStreamsRequest],
        Union[
            analytics_admin.ListWebDataStreamsResponse,
            Awaitable[analytics_admin.ListWebDataStreamsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_ios_app_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.GetIosAppDataStreamRequest],
        Union[resources.IosAppDataStream, Awaitable[resources.IosAppDataStream]],
    ]:
        raise NotImplementedError()

    @property
    def delete_ios_app_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.DeleteIosAppDataStreamRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_ios_app_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.UpdateIosAppDataStreamRequest],
        Union[resources.IosAppDataStream, Awaitable[resources.IosAppDataStream]],
    ]:
        raise NotImplementedError()

    @property
    def list_ios_app_data_streams(
        self,
    ) -> Callable[
        [analytics_admin.ListIosAppDataStreamsRequest],
        Union[
            analytics_admin.ListIosAppDataStreamsResponse,
            Awaitable[analytics_admin.ListIosAppDataStreamsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_android_app_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.GetAndroidAppDataStreamRequest],
        Union[
            resources.AndroidAppDataStream, Awaitable[resources.AndroidAppDataStream]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_android_app_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.DeleteAndroidAppDataStreamRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_android_app_data_stream(
        self,
    ) -> Callable[
        [analytics_admin.UpdateAndroidAppDataStreamRequest],
        Union[
            resources.AndroidAppDataStream, Awaitable[resources.AndroidAppDataStream]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_android_app_data_streams(
        self,
    ) -> Callable[
        [analytics_admin.ListAndroidAppDataStreamsRequest],
        Union[
            analytics_admin.ListAndroidAppDataStreamsResponse,
            Awaitable[analytics_admin.ListAndroidAppDataStreamsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_enhanced_measurement_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetEnhancedMeasurementSettingsRequest],
        Union[
            resources.EnhancedMeasurementSettings,
            Awaitable[resources.EnhancedMeasurementSettings],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_enhanced_measurement_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateEnhancedMeasurementSettingsRequest],
        Union[
            resources.EnhancedMeasurementSettings,
            Awaitable[resources.EnhancedMeasurementSettings],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_firebase_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateFirebaseLinkRequest],
        Union[resources.FirebaseLink, Awaitable[resources.FirebaseLink]],
    ]:
        raise NotImplementedError()

    @property
    def update_firebase_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateFirebaseLinkRequest],
        Union[resources.FirebaseLink, Awaitable[resources.FirebaseLink]],
    ]:
        raise NotImplementedError()

    @property
    def delete_firebase_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteFirebaseLinkRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_firebase_links(
        self,
    ) -> Callable[
        [analytics_admin.ListFirebaseLinksRequest],
        Union[
            analytics_admin.ListFirebaseLinksResponse,
            Awaitable[analytics_admin.ListFirebaseLinksResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_global_site_tag(
        self,
    ) -> Callable[
        [analytics_admin.GetGlobalSiteTagRequest],
        Union[resources.GlobalSiteTag, Awaitable[resources.GlobalSiteTag]],
    ]:
        raise NotImplementedError()

    @property
    def create_google_ads_link(
        self,
    ) -> Callable[
        [analytics_admin.CreateGoogleAdsLinkRequest],
        Union[resources.GoogleAdsLink, Awaitable[resources.GoogleAdsLink]],
    ]:
        raise NotImplementedError()

    @property
    def update_google_ads_link(
        self,
    ) -> Callable[
        [analytics_admin.UpdateGoogleAdsLinkRequest],
        Union[resources.GoogleAdsLink, Awaitable[resources.GoogleAdsLink]],
    ]:
        raise NotImplementedError()

    @property
    def delete_google_ads_link(
        self,
    ) -> Callable[
        [analytics_admin.DeleteGoogleAdsLinkRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_google_ads_links(
        self,
    ) -> Callable[
        [analytics_admin.ListGoogleAdsLinksRequest],
        Union[
            analytics_admin.ListGoogleAdsLinksResponse,
            Awaitable[analytics_admin.ListGoogleAdsLinksResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_data_sharing_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetDataSharingSettingsRequest],
        Union[resources.DataSharingSettings, Awaitable[resources.DataSharingSettings]],
    ]:
        raise NotImplementedError()

    @property
    def get_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.GetMeasurementProtocolSecretRequest],
        Union[
            resources.MeasurementProtocolSecret,
            Awaitable[resources.MeasurementProtocolSecret],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_measurement_protocol_secrets(
        self,
    ) -> Callable[
        [analytics_admin.ListMeasurementProtocolSecretsRequest],
        Union[
            analytics_admin.ListMeasurementProtocolSecretsResponse,
            Awaitable[analytics_admin.ListMeasurementProtocolSecretsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.CreateMeasurementProtocolSecretRequest],
        Union[
            resources.MeasurementProtocolSecret,
            Awaitable[resources.MeasurementProtocolSecret],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.DeleteMeasurementProtocolSecretRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_measurement_protocol_secret(
        self,
    ) -> Callable[
        [analytics_admin.UpdateMeasurementProtocolSecretRequest],
        Union[
            resources.MeasurementProtocolSecret,
            Awaitable[resources.MeasurementProtocolSecret],
        ],
    ]:
        raise NotImplementedError()

    @property
    def search_change_history_events(
        self,
    ) -> Callable[
        [analytics_admin.SearchChangeHistoryEventsRequest],
        Union[
            analytics_admin.SearchChangeHistoryEventsResponse,
            Awaitable[analytics_admin.SearchChangeHistoryEventsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_google_signals_settings(
        self,
    ) -> Callable[
        [analytics_admin.GetGoogleSignalsSettingsRequest],
        Union[
            resources.GoogleSignalsSettings, Awaitable[resources.GoogleSignalsSettings]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_google_signals_settings(
        self,
    ) -> Callable[
        [analytics_admin.UpdateGoogleSignalsSettingsRequest],
        Union[
            resources.GoogleSignalsSettings, Awaitable[resources.GoogleSignalsSettings]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.CreateConversionEventRequest],
        Union[resources.ConversionEvent, Awaitable[resources.ConversionEvent]],
    ]:
        raise NotImplementedError()

    @property
    def get_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.GetConversionEventRequest],
        Union[resources.ConversionEvent, Awaitable[resources.ConversionEvent]],
    ]:
        raise NotImplementedError()

    @property
    def delete_conversion_event(
        self,
    ) -> Callable[
        [analytics_admin.DeleteConversionEventRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_conversion_events(
        self,
    ) -> Callable[
        [analytics_admin.ListConversionEventsRequest],
        Union[
            analytics_admin.ListConversionEventsResponse,
            Awaitable[analytics_admin.ListConversionEventsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.CreateCustomDimensionRequest],
        Union[resources.CustomDimension, Awaitable[resources.CustomDimension]],
    ]:
        raise NotImplementedError()

    @property
    def update_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.UpdateCustomDimensionRequest],
        Union[resources.CustomDimension, Awaitable[resources.CustomDimension]],
    ]:
        raise NotImplementedError()

    @property
    def list_custom_dimensions(
        self,
    ) -> Callable[
        [analytics_admin.ListCustomDimensionsRequest],
        Union[
            analytics_admin.ListCustomDimensionsResponse,
            Awaitable[analytics_admin.ListCustomDimensionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def archive_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.ArchiveCustomDimensionRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_custom_dimension(
        self,
    ) -> Callable[
        [analytics_admin.GetCustomDimensionRequest],
        Union[resources.CustomDimension, Awaitable[resources.CustomDimension]],
    ]:
        raise NotImplementedError()

    @property
    def create_custom_metric(
        self,
    ) -> Callable[
        [analytics_admin.CreateCustomMetricRequest],
        Union[resources.CustomMetric, Awaitable[resources.CustomMetric]],
    ]:
        raise NotImplementedError()

    @property
    def update_custom_metric(
        self,
    ) -> Callable[
        [analytics_admin.UpdateCustomMetricRequest],
        Union[resources.CustomMetric, Awaitable[resources.CustomMetric]],
    ]:
        raise NotImplementedError()

    @property
    def list_custom_metrics(
        self,
    ) -> Callable[
        [analytics_admin.ListCustomMetricsRequest],
        Union[
            analytics_admin.ListCustomMetricsResponse,
            Awaitable[analytics_admin.ListCustomMetricsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def archive_custom_metric(
        self,
    ) -> Callable[
        [analytics_admin.ArchiveCustomMetricRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_custom_metric(
        self,
    ) -> Callable[
        [analytics_admin.GetCustomMetricRequest],
        Union[resources.CustomMetric, Awaitable[resources.CustomMetric]],
    ]:
        raise NotImplementedError()


__all__ = ("AnalyticsAdminServiceTransport",)
