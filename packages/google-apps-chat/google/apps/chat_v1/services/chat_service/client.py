# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from collections import OrderedDict
from http import HTTPStatus
import json
import logging as std_logging
import os
import re
from typing import (
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
import warnings

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
import google.protobuf

from google.apps.chat_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.apps.chat_v1.services.chat_service import pagers
from google.apps.chat_v1.types import (
    annotation,
    attachment,
    contextual_addon,
    deletion_metadata,
    event_payload,
    group,
    history_state,
    matched_url,
)
from google.apps.chat_v1.types import (
    space_notification_setting as gc_space_notification_setting,
)
from google.apps.chat_v1.types import membership
from google.apps.chat_v1.types import membership as gc_membership
from google.apps.chat_v1.types import message
from google.apps.chat_v1.types import message as gc_message
from google.apps.chat_v1.types import reaction
from google.apps.chat_v1.types import reaction as gc_reaction
from google.apps.chat_v1.types import slash_command
from google.apps.chat_v1.types import space
from google.apps.chat_v1.types import space as gc_space
from google.apps.chat_v1.types import space_event
from google.apps.chat_v1.types import space_notification_setting
from google.apps.chat_v1.types import space_read_state
from google.apps.chat_v1.types import space_read_state as gc_space_read_state
from google.apps.chat_v1.types import space_setup, thread_read_state, user

from .transports.base import DEFAULT_CLIENT_INFO, ChatServiceTransport
from .transports.grpc import ChatServiceGrpcTransport
from .transports.grpc_asyncio import ChatServiceGrpcAsyncIOTransport
from .transports.rest import ChatServiceRestTransport


class ChatServiceClientMeta(type):
    """Metaclass for the ChatService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[ChatServiceTransport]]
    _transport_registry["grpc"] = ChatServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = ChatServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = ChatServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[ChatServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class ChatServiceClient(metaclass=ChatServiceClientMeta):
    """Enables developers to build Chat apps and
    integrations on Google Chat Platform.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = "chat.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    _DEFAULT_ENDPOINT_TEMPLATE = "chat.{UNIVERSE_DOMAIN}"
    _DEFAULT_UNIVERSE = "googleapis.com"

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ChatServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ChatServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ChatServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ChatServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def attachment_path(
        space: str,
        message: str,
        attachment: str,
    ) -> str:
        """Returns a fully-qualified attachment string."""
        return "spaces/{space}/messages/{message}/attachments/{attachment}".format(
            space=space,
            message=message,
            attachment=attachment,
        )

    @staticmethod
    def parse_attachment_path(path: str) -> Dict[str, str]:
        """Parses a attachment path into its component segments."""
        m = re.match(
            r"^spaces/(?P<space>.+?)/messages/(?P<message>.+?)/attachments/(?P<attachment>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def custom_emoji_path(
        custom_emoji: str,
    ) -> str:
        """Returns a fully-qualified custom_emoji string."""
        return "customEmojis/{custom_emoji}".format(
            custom_emoji=custom_emoji,
        )

    @staticmethod
    def parse_custom_emoji_path(path: str) -> Dict[str, str]:
        """Parses a custom_emoji path into its component segments."""
        m = re.match(r"^customEmojis/(?P<custom_emoji>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def membership_path(
        space: str,
        member: str,
    ) -> str:
        """Returns a fully-qualified membership string."""
        return "spaces/{space}/members/{member}".format(
            space=space,
            member=member,
        )

    @staticmethod
    def parse_membership_path(path: str) -> Dict[str, str]:
        """Parses a membership path into its component segments."""
        m = re.match(r"^spaces/(?P<space>.+?)/members/(?P<member>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def message_path(
        space: str,
        message: str,
    ) -> str:
        """Returns a fully-qualified message string."""
        return "spaces/{space}/messages/{message}".format(
            space=space,
            message=message,
        )

    @staticmethod
    def parse_message_path(path: str) -> Dict[str, str]:
        """Parses a message path into its component segments."""
        m = re.match(r"^spaces/(?P<space>.+?)/messages/(?P<message>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def quoted_message_metadata_path(
        space: str,
        message: str,
        quoted_message_metadata: str,
    ) -> str:
        """Returns a fully-qualified quoted_message_metadata string."""
        return "spaces/{space}/messages/{message}/quotedMessageMetadata/{quoted_message_metadata}".format(
            space=space,
            message=message,
            quoted_message_metadata=quoted_message_metadata,
        )

    @staticmethod
    def parse_quoted_message_metadata_path(path: str) -> Dict[str, str]:
        """Parses a quoted_message_metadata path into its component segments."""
        m = re.match(
            r"^spaces/(?P<space>.+?)/messages/(?P<message>.+?)/quotedMessageMetadata/(?P<quoted_message_metadata>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def reaction_path(
        space: str,
        message: str,
        reaction: str,
    ) -> str:
        """Returns a fully-qualified reaction string."""
        return "spaces/{space}/messages/{message}/reactions/{reaction}".format(
            space=space,
            message=message,
            reaction=reaction,
        )

    @staticmethod
    def parse_reaction_path(path: str) -> Dict[str, str]:
        """Parses a reaction path into its component segments."""
        m = re.match(
            r"^spaces/(?P<space>.+?)/messages/(?P<message>.+?)/reactions/(?P<reaction>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def space_path(
        space: str,
    ) -> str:
        """Returns a fully-qualified space string."""
        return "spaces/{space}".format(
            space=space,
        )

    @staticmethod
    def parse_space_path(path: str) -> Dict[str, str]:
        """Parses a space path into its component segments."""
        m = re.match(r"^spaces/(?P<space>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def space_event_path(
        space: str,
        space_event: str,
    ) -> str:
        """Returns a fully-qualified space_event string."""
        return "spaces/{space}/spaceEvents/{space_event}".format(
            space=space,
            space_event=space_event,
        )

    @staticmethod
    def parse_space_event_path(path: str) -> Dict[str, str]:
        """Parses a space_event path into its component segments."""
        m = re.match(r"^spaces/(?P<space>.+?)/spaceEvents/(?P<space_event>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def space_notification_setting_path(
        user: str,
        space: str,
    ) -> str:
        """Returns a fully-qualified space_notification_setting string."""
        return "users/{user}/spaces/{space}/spaceNotificationSetting".format(
            user=user,
            space=space,
        )

    @staticmethod
    def parse_space_notification_setting_path(path: str) -> Dict[str, str]:
        """Parses a space_notification_setting path into its component segments."""
        m = re.match(
            r"^users/(?P<user>.+?)/spaces/(?P<space>.+?)/spaceNotificationSetting$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def space_read_state_path(
        user: str,
        space: str,
    ) -> str:
        """Returns a fully-qualified space_read_state string."""
        return "users/{user}/spaces/{space}/spaceReadState".format(
            user=user,
            space=space,
        )

    @staticmethod
    def parse_space_read_state_path(path: str) -> Dict[str, str]:
        """Parses a space_read_state path into its component segments."""
        m = re.match(
            r"^users/(?P<user>.+?)/spaces/(?P<space>.+?)/spaceReadState$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def thread_path(
        space: str,
        thread: str,
    ) -> str:
        """Returns a fully-qualified thread string."""
        return "spaces/{space}/threads/{thread}".format(
            space=space,
            thread=thread,
        )

    @staticmethod
    def parse_thread_path(path: str) -> Dict[str, str]:
        """Parses a thread path into its component segments."""
        m = re.match(r"^spaces/(?P<space>.+?)/threads/(?P<thread>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def thread_read_state_path(
        user: str,
        space: str,
        thread: str,
    ) -> str:
        """Returns a fully-qualified thread_read_state string."""
        return "users/{user}/spaces/{space}/threads/{thread}/threadReadState".format(
            user=user,
            space=space,
            thread=thread,
        )

    @staticmethod
    def parse_thread_read_state_path(path: str) -> Dict[str, str]:
        """Parses a thread_read_state path into its component segments."""
        m = re.match(
            r"^users/(?P<user>.+?)/spaces/(?P<space>.+?)/threads/(?P<thread>.+?)/threadReadState$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Deprecated. Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """

        warnings.warn(
            "get_mtls_endpoint_and_cert_source is deprecated. Use the api_endpoint property instead.",
            DeprecationWarning,
        )
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    @staticmethod
    def _read_environment_variables():
        """Returns the environment variables used by the client.

        Returns:
            Tuple[bool, str, str]: returns the GOOGLE_API_USE_CLIENT_CERTIFICATE,
            GOOGLE_API_USE_MTLS_ENDPOINT, and GOOGLE_CLOUD_UNIVERSE_DOMAIN environment variables.

        Raises:
            ValueError: If GOOGLE_API_USE_CLIENT_CERTIFICATE is not
                any of ["true", "false"].
            google.auth.exceptions.MutualTLSChannelError: If GOOGLE_API_USE_MTLS_ENDPOINT
                is not any of ["auto", "never", "always"].
        """
        use_client_cert = os.getenv(
            "GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"
        ).lower()
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto").lower()
        universe_domain_env = os.getenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )
        return use_client_cert == "true", use_mtls_endpoint, universe_domain_env

    @staticmethod
    def _get_client_cert_source(provided_cert_source, use_cert_flag):
        """Return the client cert source to be used by the client.

        Args:
            provided_cert_source (bytes): The client certificate source provided.
            use_cert_flag (bool): A flag indicating whether to use the client certificate.

        Returns:
            bytes or None: The client cert source to be used by the client.
        """
        client_cert_source = None
        if use_cert_flag:
            if provided_cert_source:
                client_cert_source = provided_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()
        return client_cert_source

    @staticmethod
    def _get_api_endpoint(
        api_override, client_cert_source, universe_domain, use_mtls_endpoint
    ):
        """Return the API endpoint used by the client.

        Args:
            api_override (str): The API endpoint override. If specified, this is always
                the return value of this function and the other arguments are not used.
            client_cert_source (bytes): The client certificate source used by the client.
            universe_domain (str): The universe domain used by the client.
            use_mtls_endpoint (str): How to use the mTLS endpoint, which depends also on the other parameters.
                Possible values are "always", "auto", or "never".

        Returns:
            str: The API endpoint to be used by the client.
        """
        if api_override is not None:
            api_endpoint = api_override
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            _default_universe = ChatServiceClient._DEFAULT_UNIVERSE
            if universe_domain != _default_universe:
                raise MutualTLSChannelError(
                    f"mTLS is not supported in any universe other than {_default_universe}."
                )
            api_endpoint = ChatServiceClient.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = ChatServiceClient._DEFAULT_ENDPOINT_TEMPLATE.format(
                UNIVERSE_DOMAIN=universe_domain
            )
        return api_endpoint

    @staticmethod
    def _get_universe_domain(
        client_universe_domain: Optional[str], universe_domain_env: Optional[str]
    ) -> str:
        """Return the universe domain used by the client.

        Args:
            client_universe_domain (Optional[str]): The universe domain configured via the client options.
            universe_domain_env (Optional[str]): The universe domain configured via the "GOOGLE_CLOUD_UNIVERSE_DOMAIN" environment variable.

        Returns:
            str: The universe domain to be used by the client.

        Raises:
            ValueError: If the universe domain is an empty string.
        """
        universe_domain = ChatServiceClient._DEFAULT_UNIVERSE
        if client_universe_domain is not None:
            universe_domain = client_universe_domain
        elif universe_domain_env is not None:
            universe_domain = universe_domain_env
        if len(universe_domain.strip()) == 0:
            raise ValueError("Universe Domain cannot be an empty string.")
        return universe_domain

    def _validate_universe_domain(self):
        """Validates client's and credentials' universe domains are consistent.

        Returns:
            bool: True iff the configured universe domain is valid.

        Raises:
            ValueError: If the configured universe domain is not valid.
        """

        # NOTE (b/349488459): universe validation is disabled until further notice.
        return True

    def _add_cred_info_for_auth_errors(
        self, error: core_exceptions.GoogleAPICallError
    ) -> None:
        """Adds credential info string to error details for 401/403/404 errors.

        Args:
            error (google.api_core.exceptions.GoogleAPICallError): The error to add the cred info.
        """
        if error.code not in [
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.NOT_FOUND,
        ]:
            return

        cred = self._transport._credentials

        # get_cred_info is only available in google-auth>=2.35.0
        if not hasattr(cred, "get_cred_info"):
            return

        # ignore the type check since pypy test fails when get_cred_info
        # is not available
        cred_info = cred.get_cred_info()  # type: ignore
        if cred_info and hasattr(error._details, "append"):
            error._details.append(json.dumps(cred_info))

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used by the client instance.
        """
        return self._universe_domain

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[str, ChatServiceTransport, Callable[..., ChatServiceTransport]]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the chat service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ChatServiceTransport,Callable[..., ChatServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ChatServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that the ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client_options = client_options
        if isinstance(self._client_options, dict):
            self._client_options = client_options_lib.from_dict(self._client_options)
        if self._client_options is None:
            self._client_options = client_options_lib.ClientOptions()
        self._client_options = cast(
            client_options_lib.ClientOptions, self._client_options
        )

        universe_domain_opt = getattr(self._client_options, "universe_domain", None)

        (
            self._use_client_cert,
            self._use_mtls_endpoint,
            self._universe_domain_env,
        ) = ChatServiceClient._read_environment_variables()
        self._client_cert_source = ChatServiceClient._get_client_cert_source(
            self._client_options.client_cert_source, self._use_client_cert
        )
        self._universe_domain = ChatServiceClient._get_universe_domain(
            universe_domain_opt, self._universe_domain_env
        )
        self._api_endpoint = None  # updated below, depending on `transport`

        # Initialize the universe domain validation.
        self._is_universe_domain_valid = False

        if CLIENT_LOGGING_SUPPORTED:  # pragma: NO COVER
            # Setup logging.
            client_logging.initialize_logging()

        api_key_value = getattr(self._client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        transport_provided = isinstance(transport, ChatServiceTransport)
        if transport_provided:
            # transport is a ChatServiceTransport instance.
            if credentials or self._client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if self._client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = cast(ChatServiceTransport, transport)
            self._api_endpoint = self._transport.host

        self._api_endpoint = self._api_endpoint or ChatServiceClient._get_api_endpoint(
            self._client_options.api_endpoint,
            self._client_cert_source,
            self._universe_domain,
            self._use_mtls_endpoint,
        )

        if not transport_provided:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            transport_init: Union[
                Type[ChatServiceTransport], Callable[..., ChatServiceTransport]
            ] = (
                ChatServiceClient.get_transport_class(transport)
                if isinstance(transport, str) or transport is None
                else cast(Callable[..., ChatServiceTransport], transport)
            )
            # initialize with the provided callable or the passed in class
            self._transport = transport_init(
                credentials=credentials,
                credentials_file=self._client_options.credentials_file,
                host=self._api_endpoint,
                scopes=self._client_options.scopes,
                client_cert_source_for_mtls=self._client_cert_source,
                quota_project_id=self._client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=self._client_options.api_audience,
            )

        if "async" not in str(self._transport):
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                std_logging.DEBUG
            ):  # pragma: NO COVER
                _LOGGER.debug(
                    "Created client `google.chat_v1.ChatServiceClient`.",
                    extra={
                        "serviceName": "google.chat.v1.ChatService",
                        "universeDomain": getattr(
                            self._transport._credentials, "universe_domain", ""
                        ),
                        "credentialsType": f"{type(self._transport._credentials).__module__}.{type(self._transport._credentials).__qualname__}",
                        "credentialsInfo": getattr(
                            self.transport._credentials, "get_cred_info", lambda: None
                        )(),
                    }
                    if hasattr(self._transport, "_credentials")
                    else {
                        "serviceName": "google.chat.v1.ChatService",
                        "credentialsType": None,
                    },
                )

    def create_message(
        self,
        request: Optional[Union[gc_message.CreateMessageRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        message: Optional[gc_message.Message] = None,
        message_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gc_message.Message:
        r"""Creates a message in a Google Chat space. For an example, see
        `Send a
        message <https://developers.google.com/workspace/chat/create-messages>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.bot``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.messages.create``
           -  ``https://www.googleapis.com/auth/chat.messages``
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)

        Chat attributes the message sender differently depending on the
        type of authentication that you use in your request.

        The following image shows how Chat attributes a message when you
        use app authentication. Chat displays the Chat app as the
        message sender. The content of the message can contain text
        (``text``), cards (``cardsV2``), and accessory widgets
        (``accessoryWidgets``).

        |Message sent with app authentication|

        The following image shows how Chat attributes a message when you
        use user authentication. Chat displays the user as the message
        sender and attributes the Chat app to the message by displaying
        its name. The content of message can only contain text
        (``text``).

        |Message sent with user authentication|

        The maximum message size, including the message contents, is
        32,000 bytes.

        For
        `webhook <https://developers.google.com/workspace/chat/quickstart/webhooks>`__
        requests, the response doesn't contain the full message. The
        response only populates the ``name`` and ``thread.name`` fields
        in addition to the information that was in the request.

        .. |Message sent with app authentication| image:: https://developers.google.com/workspace/chat/images/message-app-auth.svg
        .. |Message sent with user authentication| image:: https://developers.google.com/workspace/chat/images/message-user-auth.svg

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_create_message():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.CreateMessageRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_message(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.CreateMessageRequest, dict]):
                The request object. Creates a message.
            parent (str):
                Required. The resource name of the space in which to
                create a message.

                Format: ``spaces/{space}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            message (google.apps.chat_v1.types.Message):
                Required. Message body.
                This corresponds to the ``message`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            message_id (str):
                Optional. A custom ID for a message. Lets Chat apps get,
                update, or delete a message without needing to store the
                system-assigned ID in the message's resource name
                (represented in the message ``name`` field).

                The value for this field must meet the following
                requirements:

                -  Begins with ``client-``. For example,
                   ``client-custom-name`` is a valid custom ID, but
                   ``custom-name`` is not.
                -  Contains up to 63 characters and only lowercase
                   letters, numbers, and hyphens.
                -  Is unique within a space. A Chat app can't use the
                   same custom ID for different messages.

                For details, see `Name a
                message <https://developers.google.com/workspace/chat/create-messages#name_a_created_message>`__.

                This corresponds to the ``message_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Message:
                A message in a Google Chat space.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, message, message_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gc_message.CreateMessageRequest):
            request = gc_message.CreateMessageRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if message is not None:
                request.message = message
            if message_id is not None:
                request.message_id = message_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_message]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_messages(
        self,
        request: Optional[Union[message.ListMessagesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListMessagesPager:
        r"""Lists messages in a space that the caller is a member of,
        including messages from blocked members and spaces. If you list
        messages from a space with no messages, the response is an empty
        object. When using a REST/HTTP interface, the response contains
        an empty JSON object, ``{}``. For an example, see `List
        messages <https://developers.google.com/workspace/chat/api/guides/v1/messages/list>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.messages.readonly``
        -  ``https://www.googleapis.com/auth/chat.messages``
        -  ``https://www.googleapis.com/auth/chat.import`` (import mode
           spaces only)

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_list_messages():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.ListMessagesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_messages(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.chat_v1.types.ListMessagesRequest, dict]):
                The request object. Lists messages in the specified
                space, that the user is a member of.
            parent (str):
                Required. The resource name of the space to list
                messages from.

                Format: ``spaces/{space}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListMessagesPager:
                Response message for listing
                messages.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, message.ListMessagesRequest):
            request = message.ListMessagesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_messages]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMessagesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_memberships(
        self,
        request: Optional[Union[membership.ListMembershipsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListMembershipsPager:
        r"""Lists memberships in a space. For an example, see `List users
        and Google Chat apps in a
        space <https://developers.google.com/workspace/chat/list-members>`__.
        Listing memberships with `app
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
        lists memberships in spaces that the Chat app has access to, but
        excludes Chat app memberships, including its own. Listing
        memberships with `User
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        lists memberships in spaces that the authenticated user has
        access to.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.bot``
           -  ``https://www.googleapis.com/auth/chat.app.memberships``
              (requires `administrator
              approval <https://support.google.com/a?p=chat-app-auth>`__)

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.memberships.readonly``
           -  ``https://www.googleapis.com/auth/chat.memberships``
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)
           -  User authentication grants administrator privileges when
              an administrator account authenticates,
              ``use_admin_access`` is ``true``, and one of the following
              authorization scopes is used:

              -  ``https://www.googleapis.com/auth/chat.admin.memberships.readonly``
              -  ``https://www.googleapis.com/auth/chat.admin.memberships``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_list_memberships():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.ListMembershipsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_memberships(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.chat_v1.types.ListMembershipsRequest, dict]):
                The request object. Request message for listing
                memberships.
            parent (str):
                Required. The resource name of the
                space for which to fetch a membership
                list.

                Format: spaces/{space}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListMembershipsPager:
                Response to list memberships of the
                space.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, membership.ListMembershipsRequest):
            request = membership.ListMembershipsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_memberships]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMembershipsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_membership(
        self,
        request: Optional[Union[membership.GetMembershipRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> membership.Membership:
        r"""Returns details about a membership. For an example, see `Get
        details about a user's or Google Chat app's
        membership <https://developers.google.com/workspace/chat/get-members>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.bot``
           -  ``https://www.googleapis.com/auth/chat.app.memberships``
              (requires `administrator
              approval <https://support.google.com/a?p=chat-app-auth>`__)

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.memberships.readonly``
           -  ``https://www.googleapis.com/auth/chat.memberships``
           -  User authentication grants administrator privileges when
              an administrator account authenticates,
              ``use_admin_access`` is ``true``, and one of the following
              authorization scopes is used:

              -  ``https://www.googleapis.com/auth/chat.admin.memberships.readonly``
              -  ``https://www.googleapis.com/auth/chat.admin.memberships``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_get_membership():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.GetMembershipRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_membership(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.GetMembershipRequest, dict]):
                The request object. Request to get a membership of a
                space.
            name (str):
                Required. Resource name of the membership to retrieve.

                To get the app's own membership `by using user
                authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
                you can optionally use ``spaces/{space}/members/app``.

                Format: ``spaces/{space}/members/{member}`` or
                ``spaces/{space}/members/app``

                You can use the user's email as an alias for
                ``{member}``. For example,
                ``spaces/{space}/members/example@gmail.com`` where
                ``example@gmail.com`` is the email of the Google Chat
                user.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Membership:
                Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, membership.GetMembershipRequest):
            request = membership.GetMembershipRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_membership]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_message(
        self,
        request: Optional[Union[message.GetMessageRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> message.Message:
        r"""Returns details about a message. For an example, see `Get
        details about a
        message <https://developers.google.com/workspace/chat/get-messages>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.bot``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.messages.readonly``
           -  ``https://www.googleapis.com/auth/chat.messages``

        Note: Might return a message from a blocked member or space.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_get_message():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.GetMessageRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_message(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.GetMessageRequest, dict]):
                The request object. Request to get a message.
            name (str):
                Required. Resource name of the message.

                Format: ``spaces/{space}/messages/{message}``

                If you've set a custom ID for your message, you can use
                the value from the ``clientAssignedMessageId`` field for
                ``{message}``. For details, see [Name a message]
                (https://developers.google.com/workspace/chat/create-messages#name_a_created_message).

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Message:
                A message in a Google Chat space.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, message.GetMessageRequest):
            request = message.GetMessageRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_message]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_message(
        self,
        request: Optional[Union[gc_message.UpdateMessageRequest, dict]] = None,
        *,
        message: Optional[gc_message.Message] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gc_message.Message:
        r"""Updates a message. There's a difference between the ``patch``
        and ``update`` methods. The ``patch`` method uses a ``patch``
        request while the ``update`` method uses a ``put`` request. We
        recommend using the ``patch`` method. For an example, see
        `Update a
        message <https://developers.google.com/workspace/chat/update-messages>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.bot``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.messages``
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)

        When using app authentication, requests can only update messages
        created by the calling Chat app.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_update_message():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.UpdateMessageRequest(
                )

                # Make the request
                response = client.update_message(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.UpdateMessageRequest, dict]):
                The request object. Request to update a message.
            message (google.apps.chat_v1.types.Message):
                Required. Message with fields
                updated.

                This corresponds to the ``message`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The field paths to update. Separate multiple
                values with commas or use ``*`` to update all field
                paths.

                Currently supported field paths:

                -  ``text``

                -  ``attachment``

                -  ``cards`` (Requires `app
                   authentication </chat/api/guides/auth/service-accounts>`__.)

                -  ``cards_v2`` (Requires `app
                   authentication </chat/api/guides/auth/service-accounts>`__.)

                -  ``accessory_widgets`` (Requires `app
                   authentication </chat/api/guides/auth/service-accounts>`__.)

                -  ``quoted_message_metadata`` (Only allows removal of
                   the quoted message.)

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Message:
                A message in a Google Chat space.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [message, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gc_message.UpdateMessageRequest):
            request = gc_message.UpdateMessageRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if message is not None:
                request.message = message
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_message]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("message.name", request.message.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_message(
        self,
        request: Optional[Union[message.DeleteMessageRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes a message. For an example, see `Delete a
        message <https://developers.google.com/workspace/chat/delete-messages>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.bot``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.messages``
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)

        When using app authentication, requests can only delete messages
        created by the calling Chat app.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_delete_message():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.DeleteMessageRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_message(request=request)

        Args:
            request (Union[google.apps.chat_v1.types.DeleteMessageRequest, dict]):
                The request object. Request to delete a message.
            name (str):
                Required. Resource name of the message.

                Format: ``spaces/{space}/messages/{message}``

                If you've set a custom ID for your message, you can use
                the value from the ``clientAssignedMessageId`` field for
                ``{message}``. For details, see [Name a message]
                (https://developers.google.com/workspace/chat/create-messages#name_a_created_message).

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, message.DeleteMessageRequest):
            request = message.DeleteMessageRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_message]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_attachment(
        self,
        request: Optional[Union[attachment.GetAttachmentRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> attachment.Attachment:
        r"""Gets the metadata of a message attachment. The attachment data
        is fetched using the `media
        API <https://developers.google.com/workspace/chat/api/reference/rest/v1/media/download>`__.
        For an example, see `Get metadata about a message
        attachment <https://developers.google.com/workspace/chat/get-media-attachments>`__.

        Requires `app
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
        with the `authorization
        scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.bot``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_get_attachment():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.GetAttachmentRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_attachment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.GetAttachmentRequest, dict]):
                The request object. Request to get an attachment.
            name (str):
                Required. Resource name of the attachment, in the form
                ``spaces/{space}/messages/{message}/attachments/{attachment}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Attachment:
                An attachment in Google Chat.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, attachment.GetAttachmentRequest):
            request = attachment.GetAttachmentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_attachment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def upload_attachment(
        self,
        request: Optional[Union[attachment.UploadAttachmentRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> attachment.UploadAttachmentResponse:
        r"""Uploads an attachment. For an example, see `Upload media as a
        file
        attachment <https://developers.google.com/workspace/chat/upload-media-attachments>`__.

        Requires user
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.messages.create``
        -  ``https://www.googleapis.com/auth/chat.messages``
        -  ``https://www.googleapis.com/auth/chat.import`` (import mode
           spaces only)

        You can upload attachments up to 200 MB. Certain file types
        aren't supported. For details, see `File types blocked by Google
        Chat <https://support.google.com/chat/answer/7651457?&co=GENIE.Platform%3DDesktop#File%20types%20blocked%20in%20Google%20Chat>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_upload_attachment():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.UploadAttachmentRequest(
                    parent="parent_value",
                    filename="filename_value",
                )

                # Make the request
                response = client.upload_attachment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.UploadAttachmentRequest, dict]):
                The request object. Request to upload an attachment.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.UploadAttachmentResponse:
                Response of uploading an attachment.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, attachment.UploadAttachmentRequest):
            request = attachment.UploadAttachmentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.upload_attachment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_spaces(
        self,
        request: Optional[Union[space.ListSpacesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListSpacesPager:
        r"""Lists spaces the caller is a member of. Group chats and DMs
        aren't listed until the first message is sent. For an example,
        see `List
        spaces <https://developers.google.com/workspace/chat/list-spaces>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.bot``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.spaces.readonly``
           -  ``https://www.googleapis.com/auth/chat.spaces``

        To list all named spaces by Google Workspace organization, use
        the
        ```spaces.search()`` <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces/search>`__
        method using Workspace administrator privileges instead.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_list_spaces():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.ListSpacesRequest(
                )

                # Make the request
                page_result = client.list_spaces(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.chat_v1.types.ListSpacesRequest, dict]):
                The request object. A request to list the spaces the
                caller is a member of.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListSpacesPager:
                The response for a list spaces
                request.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space.ListSpacesRequest):
            request = space.ListSpacesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_spaces]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSpacesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_spaces(
        self,
        request: Optional[Union[space.SearchSpacesRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.SearchSpacesPager:
        r"""Returns a list of spaces in a Google Workspace organization
        based on an administrator's search.

        Requires `user authentication with administrator
        privileges <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user#admin-privileges>`__
        and one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.admin.spaces.readonly``
        -  ``https://www.googleapis.com/auth/chat.admin.spaces``

        In the request, set ``use_admin_access`` to ``true``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_search_spaces():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.SearchSpacesRequest(
                    query="query_value",
                )

                # Make the request
                page_result = client.search_spaces(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.chat_v1.types.SearchSpacesRequest, dict]):
                The request object. Request to search for a list of
                spaces based on a query.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.SearchSpacesPager:
                Response with a list of spaces
                corresponding to the search spaces
                request.  Iterating over this object
                will yield results and resolve
                additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space.SearchSpacesRequest):
            request = space.SearchSpacesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_spaces]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.SearchSpacesPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_space(
        self,
        request: Optional[Union[space.GetSpaceRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> space.Space:
        r"""Returns details about a space. For an example, see `Get details
        about a
        space <https://developers.google.com/workspace/chat/get-spaces>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.bot``
           -  ``https://www.googleapis.com/auth/chat.app.spaces`` with
              `administrator
              approval <https://support.google.com/a?p=chat-app-auth>`__

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.spaces.readonly``
           -  ``https://www.googleapis.com/auth/chat.spaces``
           -  User authentication grants administrator privileges when
              an administrator account authenticates,
              ``use_admin_access`` is ``true``, and one of the following
              authorization scopes is used:

              -  ``https://www.googleapis.com/auth/chat.admin.spaces.readonly``
              -  ``https://www.googleapis.com/auth/chat.admin.spaces``

        App authentication has the following limitations:

        -  ``space.access_settings`` is only populated when using the
           ``chat.app.spaces`` scope.
        -  ``space.predefind_permission_settings`` and
           ``space.permission_settings`` are only populated when using
           the ``chat.app.spaces`` scope, and only for spaces the app
           created.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_get_space():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.GetSpaceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.GetSpaceRequest, dict]):
                The request object. A request to return a single space.
            name (str):
                Required. Resource name of the space, in the form
                ``spaces/{space}``.

                Format: ``spaces/{space}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space.GetSpaceRequest):
            request = space.GetSpaceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_space]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_space(
        self,
        request: Optional[Union[gc_space.CreateSpaceRequest, dict]] = None,
        *,
        space: Optional[gc_space.Space] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gc_space.Space:
        r"""Creates a space. Can be used to create a named space, or a group
        chat in ``Import mode``. For an example, see `Create a
        space <https://developers.google.com/workspace/chat/create-spaces>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__
           and one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.app.spaces.create``
           -  ``https://www.googleapis.com/auth/chat.app.spaces``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.spaces.create``
           -  ``https://www.googleapis.com/auth/chat.spaces``
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)

        When authenticating as an app, the ``space.customer`` field must
        be set in the request.

        When authenticating as an app, the Chat app is added as a member
        of the space. However, unlike human authentication, the Chat app
        is not added as a space manager. By default, the Chat app can be
        removed from the space by all space members. To allow only space
        managers to remove the app from a space, set
        ``space.permission_settings.manage_apps`` to
        ``managers_allowed``.

        Space membership upon creation depends on whether the space is
        created in ``Import mode``:

        -  **Import mode:** No members are created.
        -  **All other modes:** The calling user is added as a member.
           This is:

           -  The app itself when using app authentication.
           -  The human user when using user authentication.

        If you receive the error message ``ALREADY_EXISTS`` when
        creating a space, try a different ``displayName``. An existing
        space within the Google Workspace organization might already use
        this display name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_create_space():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                space = chat_v1.Space()
                space.predefined_permission_settings = "ANNOUNCEMENT_SPACE"

                request = chat_v1.CreateSpaceRequest(
                    space=space,
                )

                # Make the request
                response = client.create_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.CreateSpaceRequest, dict]):
                The request object. A request to create a named space
                with no members.
            space (google.apps.chat_v1.types.Space):
                Required. The ``displayName`` and ``spaceType`` fields
                must be populated. Only ``SpaceType.SPACE`` and
                ``SpaceType.GROUP_CHAT`` are supported.
                ``SpaceType.GROUP_CHAT`` can only be used if
                ``importMode`` is set to true.

                If you receive the error message ``ALREADY_EXISTS``, try
                a different ``displayName``. An existing space within
                the Google Workspace organization might already use this
                display name.

                The space ``name`` is assigned on the server so anything
                specified in this field will be ignored.

                This corresponds to the ``space`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [space]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gc_space.CreateSpaceRequest):
            request = gc_space.CreateSpaceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if space is not None:
                request.space = space

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_space]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_up_space(
        self,
        request: Optional[Union[space_setup.SetUpSpaceRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> space.Space:
        r"""Creates a space and adds specified users to it. The calling user
        is automatically added to the space, and shouldn't be specified
        as a membership in the request. For an example, see `Set up a
        space with initial
        members <https://developers.google.com/workspace/chat/set-up-spaces>`__.

        To specify the human members to add, add memberships with the
        appropriate ``membership.member.name``. To add a human user, use
        ``users/{user}``, where ``{user}`` can be the email address for
        the user. For users in the same Workspace organization
        ``{user}`` can also be the ``id`` for the person from the People
        API, or the ``id`` for the user in the Directory API. For
        example, if the People API Person profile ID for
        ``user@example.com`` is ``123456789``, you can add the user to
        the space by setting the ``membership.member.name`` to
        ``users/user@example.com`` or ``users/123456789``.

        To specify the Google groups to add, add memberships with the
        appropriate ``membership.group_member.name``. To add or invite a
        Google group, use ``groups/{group}``, where ``{group}`` is the
        ``id`` for the group from the Cloud Identity Groups API. For
        example, you can use `Cloud Identity Groups lookup
        API <https://cloud.google.com/identity/docs/reference/rest/v1/groups/lookup>`__
        to retrieve the ID ``123456789`` for group email
        ``group@example.com``, then you can add the group to the space
        by setting the ``membership.group_member.name`` to
        ``groups/123456789``. Group email is not supported, and Google
        groups can only be added as members in named spaces.

        For a named space or group chat, if the caller blocks, or is
        blocked by some members, or doesn't have permission to add some
        members, then those members aren't added to the created space.

        To create a direct message (DM) between the calling user and
        another human user, specify exactly one membership to represent
        the human user. If one user blocks the other, the request fails
        and the DM isn't created.

        To create a DM between the calling user and the calling app, set
        ``Space.singleUserBotDm`` to ``true`` and don't specify any
        memberships. You can only use this method to set up a DM with
        the calling app. To add the calling app as a member of a space
        or an existing DM between two human users, see `Invite or add a
        user or app to a
        space <https://developers.google.com/workspace/chat/create-members>`__.

        If a DM already exists between two users, even when one user
        blocks the other at the time a request is made, then the
        existing DM is returned.

        Spaces with threaded replies aren't supported. If you receive
        the error message ``ALREADY_EXISTS`` when setting up a space,
        try a different ``displayName``. An existing space within the
        Google Workspace organization might already use this display
        name.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.spaces.create``
        -  ``https://www.googleapis.com/auth/chat.spaces``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_set_up_space():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                space = chat_v1.Space()
                space.predefined_permission_settings = "ANNOUNCEMENT_SPACE"

                request = chat_v1.SetUpSpaceRequest(
                    space=space,
                )

                # Make the request
                response = client.set_up_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.SetUpSpaceRequest, dict]):
                The request object. Request to create a space and add
                specified users to it.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space_setup.SetUpSpaceRequest):
            request = space_setup.SetUpSpaceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_up_space]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_space(
        self,
        request: Optional[Union[gc_space.UpdateSpaceRequest, dict]] = None,
        *,
        space: Optional[gc_space.Space] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gc_space.Space:
        r"""Updates a space. For an example, see `Update a
        space <https://developers.google.com/workspace/chat/update-spaces>`__.

        If you're updating the ``displayName`` field and receive the
        error message ``ALREADY_EXISTS``, try a different display name..
        An existing space within the Google Workspace organization might
        already use this display name.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__
           and one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.app.spaces``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.spaces``
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)
           -  User authentication grants administrator privileges when
              an administrator account authenticates,
              ``use_admin_access`` is ``true``, and the following
              authorization scopes is used:

              -  ``https://www.googleapis.com/auth/chat.admin.spaces``

        App authentication has the following limitations:

        -  To update either ``space.predefined_permission_settings`` or
           ``space.permission_settings``, the app must be the space
           creator.
        -  Updating the ``space.access_settings.audience`` is not
           supported for app authentication.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_update_space():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                space = chat_v1.Space()
                space.predefined_permission_settings = "ANNOUNCEMENT_SPACE"

                request = chat_v1.UpdateSpaceRequest(
                    space=space,
                )

                # Make the request
                response = client.update_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.UpdateSpaceRequest, dict]):
                The request object. A request to update a single space.
            space (google.apps.chat_v1.types.Space):
                Required. Space with fields to be updated.
                ``Space.name`` must be populated in the form of
                ``spaces/{space}``. Only fields specified by
                ``update_mask`` are updated.

                This corresponds to the ``space`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The updated field paths, comma separated if
                there are multiple.

                You can update the following fields for a space:

                ``space_details``: Updates the space's description.
                Supports up to 150 characters.

                ``display_name``: Only supports updating the display
                name for spaces where ``spaceType`` field is ``SPACE``.
                If you receive the error message ``ALREADY_EXISTS``, try
                a different value. An existing space within the Google
                Workspace organization might already use this display
                name.

                ``space_type``: Only supports changing a ``GROUP_CHAT``
                space type to ``SPACE``. Include ``display_name``
                together with ``space_type`` in the update mask and
                ensure that the specified space has a non-empty display
                name and the ``SPACE`` space type. Including the
                ``space_type`` mask and the ``SPACE`` type in the
                specified space when updating the display name is
                optional if the existing space already has the ``SPACE``
                type. Trying to update the space type in other ways
                results in an invalid argument error. ``space_type`` is
                not supported with ``useAdminAccess``.

                ``space_history_state``: Updates `space history
                settings <https://support.google.com/chat/answer/7664687>`__
                by turning history on or off for the space. Only
                supported if history settings are enabled for the Google
                Workspace organization. To update the space history
                state, you must omit all other field masks in your
                request. ``space_history_state`` is not supported with
                ``useAdminAccess``.

                ``access_settings.audience``: Updates the `access
                setting <https://support.google.com/chat/answer/11971020>`__
                of who can discover the space, join the space, and
                preview the messages in named space where ``spaceType``
                field is ``SPACE``. If the existing space has a target
                audience, you can remove the audience and restrict space
                access by omitting a value for this field mask. To
                update access settings for a space, the authenticating
                user must be a space manager and omit all other field
                masks in your request. You can't update this field if
                the space is in `import
                mode <https://developers.google.com/workspace/chat/import-data-overview>`__.
                To learn more, see `Make a space discoverable to
                specific
                users <https://developers.google.com/workspace/chat/space-target-audience>`__.
                ``access_settings.audience`` is not supported with
                ``useAdminAccess``.

                ``permission_settings``: Supports changing the
                `permission
                settings <https://support.google.com/chat/answer/13340792>`__
                of a space. When updating permission settings, you can
                only specify ``permissionSettings`` field masks; you
                cannot update other field masks at the same time.
                ``permissionSettings`` is not supported with
                ``useAdminAccess``. The supported field masks include:

                -  ``permission_settings.manageMembersAndGroups``
                -  ``permission_settings.modifySpaceDetails``
                -  ``permission_settings.toggleHistory``
                -  ``permission_settings.useAtMentionAll``
                -  ``permission_settings.manageApps``
                -  ``permission_settings.manageWebhooks``
                -  ``permission_settings.replyMessages``

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [space, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gc_space.UpdateSpaceRequest):
            request = gc_space.UpdateSpaceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if space is not None:
                request.space = space
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_space]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("space.name", request.space.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_space(
        self,
        request: Optional[Union[space.DeleteSpaceRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes a named space. Always performs a cascading delete, which
        means that the space's child resources—like messages posted in
        the space and memberships in the space—are also deleted. For an
        example, see `Delete a
        space <https://developers.google.com/workspace/chat/delete-spaces>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__
           and the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.app.delete`` (only
              in spaces the app created)

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.delete``
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)
           -  User authentication grants administrator privileges when
              an administrator account authenticates,
              ``use_admin_access`` is ``true``, and the following
              authorization scope is used:

              -  ``https://www.googleapis.com/auth/chat.admin.delete``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_delete_space():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.DeleteSpaceRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_space(request=request)

        Args:
            request (Union[google.apps.chat_v1.types.DeleteSpaceRequest, dict]):
                The request object. Request for deleting a space.
            name (str):
                Required. Resource name of the space to delete.

                Format: ``spaces/{space}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space.DeleteSpaceRequest):
            request = space.DeleteSpaceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_space]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def complete_import_space(
        self,
        request: Optional[Union[space.CompleteImportSpaceRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> space.CompleteImportSpaceResponse:
        r"""Completes the `import
        process <https://developers.google.com/workspace/chat/import-data>`__
        for the specified space and makes it visible to users.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        and domain-wide delegation with the `authorization
        scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.import``

        For more information, see `Authorize Google Chat apps to import
        data <https://developers.google.com/workspace/chat/authorize-import>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_complete_import_space():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.CompleteImportSpaceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.complete_import_space(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.CompleteImportSpaceRequest, dict]):
                The request object. Request message for completing the
                import process for a space.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.CompleteImportSpaceResponse:
                Response message for completing the
                import process for a space.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space.CompleteImportSpaceRequest):
            request = space.CompleteImportSpaceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.complete_import_space]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def find_direct_message(
        self,
        request: Optional[Union[space.FindDirectMessageRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> space.Space:
        r"""Returns the existing direct message with the specified user. If
        no direct message space is found, returns a ``404 NOT_FOUND``
        error. For an example, see `Find a direct
        message </chat/api/guides/v1/spaces/find-direct-message>`__.

        With `app
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__,
        returns the direct message space between the specified user and
        the calling Chat app.

        With `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
        returns the direct message space between the specified user and
        the authenticated user.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.bot``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.spaces.readonly``
           -  ``https://www.googleapis.com/auth/chat.spaces``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_find_direct_message():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.FindDirectMessageRequest(
                    name="name_value",
                )

                # Make the request
                response = client.find_direct_message(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.FindDirectMessageRequest, dict]):
                The request object. A request to get direct message space
                based on the user resource.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Space:
                A space in Google Chat. Spaces are
                conversations between two or more users
                or 1:1 messages between a user and a
                Chat app.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space.FindDirectMessageRequest):
            request = space.FindDirectMessageRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.find_direct_message]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_membership(
        self,
        request: Optional[Union[gc_membership.CreateMembershipRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        membership: Optional[gc_membership.Membership] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gc_membership.Membership:
        r"""Creates a membership for the calling Chat app, a user, or a
        Google Group. Creating memberships for other Chat apps isn't
        supported. When creating a membership, if the specified member
        has their auto-accept policy turned off, then they're invited,
        and must accept the space invitation before joining. Otherwise,
        creating a membership adds the member directly to the specified
        space.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__
           and the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.app.memberships``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.memberships``
           -  ``https://www.googleapis.com/auth/chat.memberships.app``
              (to add the calling app to the space)
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)
           -  User authentication grants administrator privileges when
              an administrator account authenticates,
              ``use_admin_access`` is ``true``, and the following
              authorization scope is used:

              -  ``https://www.googleapis.com/auth/chat.admin.memberships``

        App authentication is not supported for the following use cases:

        -  Inviting users external to the Workspace organization that
           owns the space.
        -  Adding a Google Group to a space.
        -  Adding a Chat app to a space.

        For example usage, see:

        -  `Invite or add a user to a
           space <https://developers.google.com/workspace/chat/create-members#create-user-membership>`__.
        -  `Invite or add a Google Group to a
           space <https://developers.google.com/workspace/chat/create-members#create-group-membership>`__.
        -  `Add the Chat app to a
           space <https://developers.google.com/workspace/chat/create-members#create-membership-calling-api>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_create_membership():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.CreateMembershipRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_membership(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.CreateMembershipRequest, dict]):
                The request object. Request message for creating a
                membership.
            parent (str):
                Required. The resource name of the
                space for which to create the
                membership.

                Format: spaces/{space}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            membership (google.apps.chat_v1.types.Membership):
                Required. The membership relation to create.

                The ``memberType`` field must contain a user with the
                ``user.name`` and ``user.type`` fields populated. The
                server will assign a resource name and overwrite
                anything specified.

                When a Chat app creates a membership relation for a
                human user, it must use certain authorization scopes and
                set specific values for certain fields:

                -  When `authenticating as a
                   user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
                   the ``chat.memberships`` authorization scope is
                   required.

                -  When `authenticating as an
                   app <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__,
                   the ``chat.app.memberships`` authorization scope is
                   required.

                -  Set ``user.type`` to ``HUMAN``, and set ``user.name``
                   with format ``users/{user}``, where ``{user}`` can be
                   the email address for the user. For users in the same
                   Workspace organization ``{user}`` can also be the
                   ``id`` of the
                   `person <https://developers.google.com/people/api/rest/v1/people>`__
                   from the People API, or the ``id`` for the user in
                   the Directory API. For example, if the People API
                   Person profile ID for ``user@example.com`` is
                   ``123456789``, you can add the user to the space by
                   setting the ``membership.member.name`` to
                   ``users/user@example.com`` or ``users/123456789``.

                Inviting users external to the Workspace organization
                that owns the space requires `user
                authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.

                When a Chat app creates a membership relation for
                itself, it must `authenticate as a
                user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
                and use the ``chat.memberships.app`` scope, set
                ``user.type`` to ``BOT``, and set ``user.name`` to
                ``users/app``.

                This corresponds to the ``membership`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Membership:
                Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, membership]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gc_membership.CreateMembershipRequest):
            request = gc_membership.CreateMembershipRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if membership is not None:
                request.membership = membership

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_membership]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_membership(
        self,
        request: Optional[Union[gc_membership.UpdateMembershipRequest, dict]] = None,
        *,
        membership: Optional[gc_membership.Membership] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gc_membership.Membership:
        r"""Updates a membership. For an example, see `Update a user's
        membership in a
        space <https://developers.google.com/workspace/chat/update-members>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__
           and the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.app.memberships``
              (only in spaces the app created)

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.memberships``
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)
           -  User authentication grants administrator privileges when
              an administrator account authenticates,
              ``use_admin_access`` is ``true``, and the following
              authorization scope is used:

              -  ``https://www.googleapis.com/auth/chat.admin.memberships``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_update_membership():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.UpdateMembershipRequest(
                )

                # Make the request
                response = client.update_membership(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.UpdateMembershipRequest, dict]):
                The request object. Request message for updating a
                membership.
            membership (google.apps.chat_v1.types.Membership):
                Required. The membership to update. Only fields
                specified by ``update_mask`` are updated.

                This corresponds to the ``membership`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The field paths to update. Separate multiple
                values with commas or use ``*`` to update all field
                paths.

                Currently supported field paths:

                -  ``role``

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Membership:
                Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [membership, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gc_membership.UpdateMembershipRequest):
            request = gc_membership.UpdateMembershipRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if membership is not None:
                request.membership = membership
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_membership]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("membership.name", request.membership.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_membership(
        self,
        request: Optional[Union[membership.DeleteMembershipRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> membership.Membership:
        r"""Deletes a membership. For an example, see `Remove a user or a
        Google Chat app from a
        space <https://developers.google.com/workspace/chat/delete-members>`__.

        Supports the following types of
        `authentication <https://developers.google.com/workspace/chat/authenticate-authorize>`__:

        -  `App
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
           with `administrator
           approval <https://support.google.com/a?p=chat-app-auth>`__
           and the authorization scope:

           -  ``https://www.googleapis.com/auth/chat.app.memberships``

        -  `User
           authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
           with one of the following authorization scopes:

           -  ``https://www.googleapis.com/auth/chat.memberships``
           -  ``https://www.googleapis.com/auth/chat.memberships.app``
              (to remove the calling app from the space)
           -  ``https://www.googleapis.com/auth/chat.import`` (import
              mode spaces only)
           -  User authentication grants administrator privileges when
              an administrator account authenticates,
              ``use_admin_access`` is ``true``, and the following
              authorization scope is used:

              -  ``https://www.googleapis.com/auth/chat.admin.memberships``

        App authentication is not supported for the following use cases:

        -  Removing a Google Group from a space.
        -  Removing a Chat app from a space.

        To delete memberships for space managers, the requester must be
        a space manager. If you're using `app
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
        the Chat app must be the space creator.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_delete_membership():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.DeleteMembershipRequest(
                    name="name_value",
                )

                # Make the request
                response = client.delete_membership(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.DeleteMembershipRequest, dict]):
                The request object. Request to delete a membership in a
                space.
            name (str):
                Required. Resource name of the membership to delete.
                Chat apps can delete human users' or their own
                memberships. Chat apps can't delete other apps'
                memberships.

                When deleting a human membership, requires the
                ``chat.memberships`` scope with `user
                authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
                or the ``chat.memberships.app`` scope with `app
                authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
                and the ``spaces/{space}/members/{member}`` format. You
                can use the email as an alias for ``{member}``. For
                example, ``spaces/{space}/members/example@gmail.com``
                where ``example@gmail.com`` is the email of the Google
                Chat user.

                When deleting an app membership, requires the
                ``chat.memberships.app`` scope and
                ``spaces/{space}/members/app`` format.

                Format: ``spaces/{space}/members/{member}`` or
                ``spaces/{space}/members/app``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Membership:
                Represents a membership relation in
                Google Chat, such as whether a user or
                Chat app is invited to, part of, or
                absent from a space.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, membership.DeleteMembershipRequest):
            request = membership.DeleteMembershipRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_membership]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_reaction(
        self,
        request: Optional[Union[gc_reaction.CreateReactionRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        reaction: Optional[gc_reaction.Reaction] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gc_reaction.Reaction:
        r"""Creates a reaction and adds it to a message. For an example, see
        `Add a reaction to a
        message <https://developers.google.com/workspace/chat/create-reactions>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.messages.reactions.create``
        -  ``https://www.googleapis.com/auth/chat.messages.reactions``
        -  ``https://www.googleapis.com/auth/chat.messages``
        -  ``https://www.googleapis.com/auth/chat.import`` (import mode
           spaces only)

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_create_reaction():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                reaction = chat_v1.Reaction()
                reaction.emoji.unicode = "unicode_value"

                request = chat_v1.CreateReactionRequest(
                    parent="parent_value",
                    reaction=reaction,
                )

                # Make the request
                response = client.create_reaction(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.CreateReactionRequest, dict]):
                The request object. Creates a reaction to a message.
            parent (str):
                Required. The message where the reaction is created.

                Format: ``spaces/{space}/messages/{message}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            reaction (google.apps.chat_v1.types.Reaction):
                Required. The reaction to create.
                This corresponds to the ``reaction`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.Reaction:
                A reaction to a message.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, reaction]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gc_reaction.CreateReactionRequest):
            request = gc_reaction.CreateReactionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if reaction is not None:
                request.reaction = reaction

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_reaction]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_reactions(
        self,
        request: Optional[Union[reaction.ListReactionsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListReactionsPager:
        r"""Lists reactions to a message. For an example, see `List
        reactions for a
        message <https://developers.google.com/workspace/chat/list-reactions>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.messages.reactions.readonly``
        -  ``https://www.googleapis.com/auth/chat.messages.reactions``
        -  ``https://www.googleapis.com/auth/chat.messages.readonly``
        -  ``https://www.googleapis.com/auth/chat.messages``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_list_reactions():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.ListReactionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_reactions(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.chat_v1.types.ListReactionsRequest, dict]):
                The request object. Lists reactions to a message.
            parent (str):
                Required. The message users reacted to.

                Format: ``spaces/{space}/messages/{message}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListReactionsPager:
                Response to a list reactions request.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, reaction.ListReactionsRequest):
            request = reaction.ListReactionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_reactions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListReactionsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_reaction(
        self,
        request: Optional[Union[reaction.DeleteReactionRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes a reaction to a message. For an example, see `Delete a
        reaction <https://developers.google.com/workspace/chat/delete-reactions>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.messages.reactions``
        -  ``https://www.googleapis.com/auth/chat.messages``
        -  ``https://www.googleapis.com/auth/chat.import`` (import mode
           spaces only)

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_delete_reaction():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.DeleteReactionRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_reaction(request=request)

        Args:
            request (Union[google.apps.chat_v1.types.DeleteReactionRequest, dict]):
                The request object. Deletes a reaction to a message.
            name (str):
                Required. Name of the reaction to delete.

                Format:
                ``spaces/{space}/messages/{message}/reactions/{reaction}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, reaction.DeleteReactionRequest):
            request = reaction.DeleteReactionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_reaction]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_custom_emoji(
        self,
        request: Optional[Union[reaction.CreateCustomEmojiRequest, dict]] = None,
        *,
        custom_emoji: Optional[reaction.CustomEmoji] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> reaction.CustomEmoji:
        r"""Creates a custom emoji.

        Custom emojis are only available for Google Workspace accounts,
        and the administrator must turn custom emojis on for the
        organization. For more information, see `Learn about custom
        emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__ and
        `Manage custom emoji
        permissions <https://support.google.com/a/answer/12850085>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with the `authorization
        scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.customemojis``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_create_custom_emoji():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.CreateCustomEmojiRequest(
                )

                # Make the request
                response = client.create_custom_emoji(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.CreateCustomEmojiRequest, dict]):
                The request object. A request to create a custom emoji.
            custom_emoji (google.apps.chat_v1.types.CustomEmoji):
                Required. The custom emoji to create.
                This corresponds to the ``custom_emoji`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.CustomEmoji:
                Represents a [custom
                emoji](\ https://support.google.com/chat/answer/12800149).

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [custom_emoji]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, reaction.CreateCustomEmojiRequest):
            request = reaction.CreateCustomEmojiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if custom_emoji is not None:
                request.custom_emoji = custom_emoji

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_custom_emoji]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_custom_emoji(
        self,
        request: Optional[Union[reaction.GetCustomEmojiRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> reaction.CustomEmoji:
        r"""Returns details about a custom emoji.

        Custom emojis are only available for Google Workspace accounts,
        and the administrator must turn custom emojis on for the
        organization. For more information, see `Learn about custom
        emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__ and
        `Manage custom emoji
        permissions <https://support.google.com/a/answer/12850085>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.customemojis.readonly``
        -  ``https://www.googleapis.com/auth/chat.customemojis``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_get_custom_emoji():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.GetCustomEmojiRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_custom_emoji(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.GetCustomEmojiRequest, dict]):
                The request object. A request to return a single custom
                emoji.
            name (str):
                Required. Resource name of the custom emoji.

                Format: ``customEmojis/{customEmoji}``

                You can use the emoji name as an alias for
                ``{customEmoji}``. For example,
                ``customEmojis/:example-emoji:`` where
                ``:example-emoji:`` is the emoji name for a custom
                emoji.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.CustomEmoji:
                Represents a [custom
                emoji](\ https://support.google.com/chat/answer/12800149).

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, reaction.GetCustomEmojiRequest):
            request = reaction.GetCustomEmojiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_custom_emoji]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_custom_emojis(
        self,
        request: Optional[Union[reaction.ListCustomEmojisRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListCustomEmojisPager:
        r"""Lists custom emojis visible to the authenticated user.

        Custom emojis are only available for Google Workspace accounts,
        and the administrator must turn custom emojis on for the
        organization. For more information, see `Learn about custom
        emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__ and
        `Manage custom emoji
        permissions <https://support.google.com/a/answer/12850085>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.customemojis.readonly``
        -  ``https://www.googleapis.com/auth/chat.customemojis``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_list_custom_emojis():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.ListCustomEmojisRequest(
                )

                # Make the request
                page_result = client.list_custom_emojis(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.chat_v1.types.ListCustomEmojisRequest, dict]):
                The request object. A request to return a list of custom
                emojis.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListCustomEmojisPager:
                A response to list custom emojis.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, reaction.ListCustomEmojisRequest):
            request = reaction.ListCustomEmojisRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_custom_emojis]

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCustomEmojisPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_custom_emoji(
        self,
        request: Optional[Union[reaction.DeleteCustomEmojiRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> None:
        r"""Deletes a custom emoji. By default, users can only delete custom
        emoji they created. `Emoji
        managers <https://support.google.com/a/answer/12850085>`__
        assigned by the administrator can delete any custom emoji in the
        organization. See `Learn about custom emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__.

        Custom emojis are only available for Google Workspace accounts,
        and the administrator must turn custom emojis on for the
        organization. For more information, see `Learn about custom
        emojis in Google
        Chat <https://support.google.com/chat/answer/12800149>`__ and
        `Manage custom emoji
        permissions <https://support.google.com/a/answer/12850085>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with the `authorization
        scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.customemojis``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_delete_custom_emoji():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.DeleteCustomEmojiRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_custom_emoji(request=request)

        Args:
            request (Union[google.apps.chat_v1.types.DeleteCustomEmojiRequest, dict]):
                The request object. Request for deleting a custom emoji.
            name (str):
                Required. Resource name of the custom emoji to delete.

                Format: ``customEmojis/{customEmoji}``

                You can use the emoji name as an alias for
                ``{customEmoji}``. For example,
                ``customEmojis/:example-emoji:`` where
                ``:example-emoji:`` is the emoji name for a custom
                emoji.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, reaction.DeleteCustomEmojiRequest):
            request = reaction.DeleteCustomEmojiRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_custom_emoji]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_space_read_state(
        self,
        request: Optional[
            Union[space_read_state.GetSpaceReadStateRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> space_read_state.SpaceReadState:
        r"""Returns details about a user's read state within a space, used
        to identify read and unread messages. For an example, see `Get
        details about a user's space read
        state <https://developers.google.com/workspace/chat/get-space-read-state>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.users.readstate.readonly``
        -  ``https://www.googleapis.com/auth/chat.users.readstate``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_get_space_read_state():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.GetSpaceReadStateRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_space_read_state(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.GetSpaceReadStateRequest, dict]):
                The request object. Request message for GetSpaceReadState
                API.
            name (str):
                Required. Resource name of the space read state to
                retrieve.

                Only supports getting read state for the calling user.

                To refer to the calling user, set one of the following:

                -  The ``me`` alias. For example,
                   ``users/me/spaces/{space}/spaceReadState``.

                -  Their Workspace email address. For example,
                   ``users/user@example.com/spaces/{space}/spaceReadState``.

                -  Their user id. For example,
                   ``users/123456789/spaces/{space}/spaceReadState``.

                Format: users/{user}/spaces/{space}/spaceReadState

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.SpaceReadState:
                A user's read state within a space,
                used to identify read and unread
                messages.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space_read_state.GetSpaceReadStateRequest):
            request = space_read_state.GetSpaceReadStateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_space_read_state]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_space_read_state(
        self,
        request: Optional[
            Union[gc_space_read_state.UpdateSpaceReadStateRequest, dict]
        ] = None,
        *,
        space_read_state: Optional[gc_space_read_state.SpaceReadState] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gc_space_read_state.SpaceReadState:
        r"""Updates a user's read state within a space, used to identify
        read and unread messages. For an example, see `Update a user's
        space read
        state <https://developers.google.com/workspace/chat/update-space-read-state>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with the `authorization
        scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.users.readstate``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_update_space_read_state():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.UpdateSpaceReadStateRequest(
                )

                # Make the request
                response = client.update_space_read_state(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.UpdateSpaceReadStateRequest, dict]):
                The request object. Request message for
                UpdateSpaceReadState API.
            space_read_state (google.apps.chat_v1.types.SpaceReadState):
                Required. The space read state and fields to update.

                Only supports updating read state for the calling user.

                To refer to the calling user, set one of the following:

                -  The ``me`` alias. For example,
                   ``users/me/spaces/{space}/spaceReadState``.

                -  Their Workspace email address. For example,
                   ``users/user@example.com/spaces/{space}/spaceReadState``.

                -  Their user id. For example,
                   ``users/123456789/spaces/{space}/spaceReadState``.

                Format: users/{user}/spaces/{space}/spaceReadState

                This corresponds to the ``space_read_state`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The field paths to update. Currently supported
                field paths:

                -  ``last_read_time``

                When the ``last_read_time`` is before the latest message
                create time, the space appears as unread in the UI.

                To mark the space as read, set ``last_read_time`` to any
                value later (larger) than the latest message create
                time. The ``last_read_time`` is coerced to match the
                latest message create time. Note that the space read
                state only affects the read state of messages that are
                visible in the space's top-level conversation. Replies
                in threads are unaffected by this timestamp, and instead
                rely on the thread read state.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.SpaceReadState:
                A user's read state within a space,
                used to identify read and unread
                messages.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [space_read_state, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, gc_space_read_state.UpdateSpaceReadStateRequest):
            request = gc_space_read_state.UpdateSpaceReadStateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if space_read_state is not None:
                request.space_read_state = space_read_state
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_space_read_state]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("space_read_state.name", request.space_read_state.name),)
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_thread_read_state(
        self,
        request: Optional[
            Union[thread_read_state.GetThreadReadStateRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> thread_read_state.ThreadReadState:
        r"""Returns details about a user's read state within a thread, used
        to identify read and unread messages. For an example, see `Get
        details about a user's thread read
        state <https://developers.google.com/workspace/chat/get-thread-read-state>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with one of the following `authorization
        scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.users.readstate.readonly``
        -  ``https://www.googleapis.com/auth/chat.users.readstate``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_get_thread_read_state():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.GetThreadReadStateRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_thread_read_state(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.GetThreadReadStateRequest, dict]):
                The request object. Request message for
                GetThreadReadStateRequest API.
            name (str):
                Required. Resource name of the thread read state to
                retrieve.

                Only supports getting read state for the calling user.

                To refer to the calling user, set one of the following:

                -  The ``me`` alias. For example,
                   ``users/me/spaces/{space}/threads/{thread}/threadReadState``.

                -  Their Workspace email address. For example,
                   ``users/user@example.com/spaces/{space}/threads/{thread}/threadReadState``.

                -  Their user id. For example,
                   ``users/123456789/spaces/{space}/threads/{thread}/threadReadState``.

                Format:
                users/{user}/spaces/{space}/threads/{thread}/threadReadState

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.ThreadReadState:
                A user's read state within a thread,
                used to identify read and unread
                messages.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, thread_read_state.GetThreadReadStateRequest):
            request = thread_read_state.GetThreadReadStateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_thread_read_state]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_space_event(
        self,
        request: Optional[Union[space_event.GetSpaceEventRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> space_event.SpaceEvent:
        r"""Returns an event from a Google Chat space. The `event
        payload <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.spaceEvents#SpaceEvent.FIELDS.oneof_payload>`__
        contains the most recent version of the resource that changed.
        For example, if you request an event about a new message but the
        message was later updated, the server returns the updated
        ``Message`` resource in the event payload.

        Note: The ``permissionSettings`` field is not returned in the
        Space object of the Space event data for this request.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with an `authorization
        scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__
        appropriate for reading the requested data:

        -  ``https://www.googleapis.com/auth/chat.spaces.readonly``
        -  ``https://www.googleapis.com/auth/chat.spaces``
        -  ``https://www.googleapis.com/auth/chat.messages.readonly``
        -  ``https://www.googleapis.com/auth/chat.messages``
        -  ``https://www.googleapis.com/auth/chat.messages.reactions.readonly``
        -  ``https://www.googleapis.com/auth/chat.messages.reactions``
        -  ``https://www.googleapis.com/auth/chat.memberships.readonly``
        -  ``https://www.googleapis.com/auth/chat.memberships``

        To get an event, the authenticated user must be a member of the
        space.

        For an example, see `Get details about an event from a Google
        Chat
        space <https://developers.google.com/workspace/chat/get-space-event>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_get_space_event():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.GetSpaceEventRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_space_event(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.GetSpaceEventRequest, dict]):
                The request object. Request message for getting a space
                event.
            name (str):
                Required. The resource name of the space event.

                Format: ``spaces/{space}/spaceEvents/{spaceEvent}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.SpaceEvent:
                An event that represents a change or activity in a Google Chat space. To
                   learn more, see [Work with events from Google
                   Chat](\ https://developers.google.com/workspace/chat/events-overview).

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space_event.GetSpaceEventRequest):
            request = space_event.GetSpaceEventRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_space_event]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_space_events(
        self,
        request: Optional[Union[space_event.ListSpaceEventsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        filter: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> pagers.ListSpaceEventsPager:
        r"""Lists events from a Google Chat space. For each event, the
        `payload <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.spaceEvents#SpaceEvent.FIELDS.oneof_payload>`__
        contains the most recent version of the Chat resource. For
        example, if you list events about new space members, the server
        returns ``Membership`` resources that contain the latest
        membership details. If new members were removed during the
        requested period, the event payload contains an empty
        ``Membership`` resource.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with an `authorization
        scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__
        appropriate for reading the requested data:

        -  ``https://www.googleapis.com/auth/chat.spaces.readonly``
        -  ``https://www.googleapis.com/auth/chat.spaces``
        -  ``https://www.googleapis.com/auth/chat.messages.readonly``
        -  ``https://www.googleapis.com/auth/chat.messages``
        -  ``https://www.googleapis.com/auth/chat.messages.reactions.readonly``
        -  ``https://www.googleapis.com/auth/chat.messages.reactions``
        -  ``https://www.googleapis.com/auth/chat.memberships.readonly``
        -  ``https://www.googleapis.com/auth/chat.memberships``

        To list events, the authenticated user must be a member of the
        space.

        For an example, see `List events from a Google Chat
        space <https://developers.google.com/workspace/chat/list-space-events>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_list_space_events():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.ListSpaceEventsRequest(
                    parent="parent_value",
                    filter="filter_value",
                )

                # Make the request
                page_result = client.list_space_events(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.apps.chat_v1.types.ListSpaceEventsRequest, dict]):
                The request object. Request message for listing space
                events.
            parent (str):
                Required. Resource name of the `Google Chat
                space <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces>`__
                where the events occurred.

                Format: ``spaces/{space}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Required. A query filter.

                You must specify at least one event type
                (``event_type``) using the has ``:`` operator. To filter
                by multiple event types, use the ``OR`` operator. Omit
                batch event types in your filter. The request
                automatically returns any related batch events. For
                example, if you filter by new reactions
                (``google.workspace.chat.reaction.v1.created``), the
                server also returns batch new reactions events
                (``google.workspace.chat.reaction.v1.batchCreated``).
                For a list of supported event types, see the
                ```SpaceEvents`` reference
                documentation <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.spaceEvents#SpaceEvent.FIELDS.event_type>`__.

                Optionally, you can also filter by start time
                (``start_time``) and end time (``end_time``):

                -  ``start_time``: Exclusive timestamp from which to
                   start listing space events. You can list events that
                   occurred up to 28 days ago. If unspecified, lists
                   space events from the past 28 days.
                -  ``end_time``: Inclusive timestamp until which space
                   events are listed. If unspecified, lists events up to
                   the time of the request.

                To specify a start or end time, use the equals ``=``
                operator and format in
                `RFC-3339 <https://www.rfc-editor.org/rfc/rfc3339>`__.
                To filter by both ``start_time`` and ``end_time``, use
                the ``AND`` operator.

                For example, the following queries are valid:

                ::

                   start_time="2023-08-23T19:20:33+00:00" AND
                   end_time="2023-08-23T19:21:54+00:00"

                ::

                   start_time="2023-08-23T19:20:33+00:00" AND
                   (event_types:"google.workspace.chat.space.v1.updated" OR
                   event_types:"google.workspace.chat.message.v1.created")

                The following queries are invalid:

                ::

                   start_time="2023-08-23T19:20:33+00:00" OR
                   end_time="2023-08-23T19:21:54+00:00"

                ::

                   event_types:"google.workspace.chat.space.v1.updated" AND
                   event_types:"google.workspace.chat.message.v1.created"

                Invalid queries are rejected by the server with an
                ``INVALID_ARGUMENT`` error.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.services.chat_service.pagers.ListSpaceEventsPager:
                Response message for listing space
                events.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [parent, filter]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, space_event.ListSpaceEventsRequest):
            request = space_event.ListSpaceEventsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_space_events]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSpaceEventsPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_space_notification_setting(
        self,
        request: Optional[
            Union[space_notification_setting.GetSpaceNotificationSettingRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> space_notification_setting.SpaceNotificationSetting:
        r"""Gets the space notification setting. For an example, see `Get
        the caller's space notification
        setting <https://developers.google.com/workspace/chat/get-space-notification-setting>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with the `authorization
        scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.users.spacesettings``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_get_space_notification_setting():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.GetSpaceNotificationSettingRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_space_notification_setting(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.GetSpaceNotificationSettingRequest, dict]):
                The request object. Request message to get space
                notification setting. Only supports
                getting notification setting for the
                calling user.
            name (str):
                Required. Format:
                users/{user}/spaces/{space}/spaceNotificationSetting

                -  ``users/me/spaces/{space}/spaceNotificationSetting``,
                   OR
                -  ``users/user@example.com/spaces/{space}/spaceNotificationSetting``,
                   OR
                -  ``users/123456789/spaces/{space}/spaceNotificationSetting``.
                   Note: Only the caller's user id or email is allowed
                   in the path.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.SpaceNotificationSetting:
                The notification setting of a user in
                a space.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [name]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, space_notification_setting.GetSpaceNotificationSettingRequest
        ):
            request = space_notification_setting.GetSpaceNotificationSettingRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_space_notification_setting
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_space_notification_setting(
        self,
        request: Optional[
            Union[
                gc_space_notification_setting.UpdateSpaceNotificationSettingRequest,
                dict,
            ]
        ] = None,
        *,
        space_notification_setting: Optional[
            gc_space_notification_setting.SpaceNotificationSetting
        ] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> gc_space_notification_setting.SpaceNotificationSetting:
        r"""Updates the space notification setting. For an example, see
        `Update the caller's space notification
        setting <https://developers.google.com/workspace/chat/update-space-notification-setting>`__.

        Requires `user
        authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
        with the `authorization
        scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__:

        -  ``https://www.googleapis.com/auth/chat.users.spacesettings``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.apps import chat_v1

            def sample_update_space_notification_setting():
                # Create a client
                client = chat_v1.ChatServiceClient()

                # Initialize request argument(s)
                request = chat_v1.UpdateSpaceNotificationSettingRequest(
                )

                # Make the request
                response = client.update_space_notification_setting(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.apps.chat_v1.types.UpdateSpaceNotificationSettingRequest, dict]):
                The request object. Request to update the space
                notification settings. Only supports
                updating notification setting for the
                calling user.
            space_notification_setting (google.apps.chat_v1.types.SpaceNotificationSetting):
                Required. The resource name for the space notification
                settings must be populated in the form of
                ``users/{user}/spaces/{space}/spaceNotificationSetting``.
                Only fields specified by ``update_mask`` are updated.

                This corresponds to the ``space_notification_setting`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Supported field paths:

                -  ``notification_setting``

                -  ``mute_setting``

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.apps.chat_v1.types.SpaceNotificationSetting:
                The notification setting of a user in
                a space.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [space_notification_setting, update_mask]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, gc_space_notification_setting.UpdateSpaceNotificationSettingRequest
        ):
            request = (
                gc_space_notification_setting.UpdateSpaceNotificationSettingRequest(
                    request
                )
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if space_notification_setting is not None:
                request.space_notification_setting = space_notification_setting
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_space_notification_setting
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "space_notification_setting.name",
                        request.space_notification_setting.name,
                    ),
                )
            ),
        )

        # Validate the universe domain.
        self._validate_universe_domain()

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "ChatServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__

__all__ = ("ChatServiceClient",)
