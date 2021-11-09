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
from collections import OrderedDict
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api import label_pb2  # type: ignore
from google.api import launch_stage_pb2  # type: ignore
from google.cloud.monitoring_v3.services.notification_channel_service import pagers
from google.cloud.monitoring_v3.types import common
from google.cloud.monitoring_v3.types import mutation_record
from google.cloud.monitoring_v3.types import notification
from google.cloud.monitoring_v3.types import notification_service
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from .transports.base import NotificationChannelServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import NotificationChannelServiceGrpcTransport
from .transports.grpc_asyncio import NotificationChannelServiceGrpcAsyncIOTransport


class NotificationChannelServiceClientMeta(type):
    """Metaclass for the NotificationChannelService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[NotificationChannelServiceTransport]]
    _transport_registry["grpc"] = NotificationChannelServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = NotificationChannelServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[NotificationChannelServiceTransport]:
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


class NotificationChannelServiceClient(metaclass=NotificationChannelServiceClientMeta):
    """The Notification Channel API provides access to configuration
    that controls how messages related to incidents are sent.
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

    DEFAULT_ENDPOINT = "monitoring.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            NotificationChannelServiceClient: The constructed client.
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
            NotificationChannelServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> NotificationChannelServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            NotificationChannelServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def notification_channel_path(project: str, notification_channel: str,) -> str:
        """Returns a fully-qualified notification_channel string."""
        return "projects/{project}/notificationChannels/{notification_channel}".format(
            project=project, notification_channel=notification_channel,
        )

    @staticmethod
    def parse_notification_channel_path(path: str) -> Dict[str, str]:
        """Parses a notification_channel path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/notificationChannels/(?P<notification_channel>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def notification_channel_descriptor_path(
        project: str, channel_descriptor: str,
    ) -> str:
        """Returns a fully-qualified notification_channel_descriptor string."""
        return "projects/{project}/notificationChannelDescriptors/{channel_descriptor}".format(
            project=project, channel_descriptor=channel_descriptor,
        )

    @staticmethod
    def parse_notification_channel_descriptor_path(path: str) -> Dict[str, str]:
        """Parses a notification_channel_descriptor path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/notificationChannelDescriptors/(?P<channel_descriptor>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
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
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, NotificationChannelServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the notification channel service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, NotificationChannelServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        if os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") not in (
            "true",
            "false",
        ):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        use_client_cert = (
            os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") == "true"
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                if is_mtls:
                    api_endpoint = self.DEFAULT_MTLS_ENDPOINT
                else:
                    api_endpoint = self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, NotificationChannelServiceTransport):
            # transport is a NotificationChannelServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
            )

    def list_notification_channel_descriptors(
        self,
        request: Union[
            notification_service.ListNotificationChannelDescriptorsRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNotificationChannelDescriptorsPager:
        r"""Lists the descriptors for supported channel types.
        The use of descriptors makes it possible for new channel
        types to be dynamically added.

        Args:
            request (Union[google.cloud.monitoring_v3.types.ListNotificationChannelDescriptorsRequest, dict]):
                The request object. The
                `ListNotificationChannelDescriptors` request.
            name (str):
                Required. The REST resource name of the parent from
                which to retrieve the notification channel descriptors.
                The expected syntax is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                Note that this
                `names <https://cloud.google.com/monitoring/api/v3#project_name>`__
                the parent container in which to look for the
                descriptors; to retrieve a single descriptor by name,
                use the
                [GetNotificationChannelDescriptor][google.monitoring.v3.NotificationChannelService.GetNotificationChannelDescriptor]
                operation, instead.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.notification_channel_service.pagers.ListNotificationChannelDescriptorsPager:
                The ListNotificationChannelDescriptors response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.ListNotificationChannelDescriptorsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, notification_service.ListNotificationChannelDescriptorsRequest
        ):
            request = notification_service.ListNotificationChannelDescriptorsRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_notification_channel_descriptors
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListNotificationChannelDescriptorsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_notification_channel_descriptor(
        self,
        request: Union[
            notification_service.GetNotificationChannelDescriptorRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannelDescriptor:
        r"""Gets a single channel descriptor. The descriptor
        indicates which fields are expected / permitted for a
        notification channel of the given type.

        Args:
            request (Union[google.cloud.monitoring_v3.types.GetNotificationChannelDescriptorRequest, dict]):
                The request object. The
                `GetNotificationChannelDescriptor` response.
            name (str):
                Required. The channel type for which to execute the
                request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/notificationChannelDescriptors/[CHANNEL_TYPE]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannelDescriptor:
                A description of a notification
                channel. The descriptor includes the
                properties of the channel and the set of
                labels or fields that must be specified
                to configure channels of a given type.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.GetNotificationChannelDescriptorRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, notification_service.GetNotificationChannelDescriptorRequest
        ):
            request = notification_service.GetNotificationChannelDescriptorRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_notification_channel_descriptor
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_notification_channels(
        self,
        request: Union[
            notification_service.ListNotificationChannelsRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNotificationChannelsPager:
        r"""Lists the notification channels that have been
        created for the project.

        Args:
            request (Union[google.cloud.monitoring_v3.types.ListNotificationChannelsRequest, dict]):
                The request object. The `ListNotificationChannels`
                request.
            name (str):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                on which to execute the request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This names the container in which to look for the
                notification channels; it does not name a specific
                channel. To query a specific channel by REST resource
                name, use the
                [``GetNotificationChannel``][google.monitoring.v3.NotificationChannelService.GetNotificationChannel]
                operation.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.notification_channel_service.pagers.ListNotificationChannelsPager:
                The ListNotificationChannels response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.ListNotificationChannelsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, notification_service.ListNotificationChannelsRequest
        ):
            request = notification_service.ListNotificationChannelsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_notification_channels
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListNotificationChannelsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_notification_channel(
        self,
        request: Union[notification_service.GetNotificationChannelRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannel:
        r"""Gets a single notification channel. The channel
        includes the relevant configuration details with which
        the channel was created. However, the response may
        truncate or omit passwords, API keys, or other private
        key matter and thus the response may not be 100%
        identical to the information that was supplied in the
        call to the create method.

        Args:
            request (Union[google.cloud.monitoring_v3.types.GetNotificationChannelRequest, dict]):
                The request object. The `GetNotificationChannel`
                request.
            name (str):
                Required. The channel for which to execute the request.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/notificationChannels/[CHANNEL_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannel:
                A NotificationChannel is a medium through which an alert is
                   delivered when a policy violation is detected.
                   Examples of channels include email, SMS, and
                   third-party messaging applications. Fields containing
                   sensitive information like authentication tokens or
                   contact info are only partially populated on
                   retrieval.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.GetNotificationChannelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, notification_service.GetNotificationChannelRequest):
            request = notification_service.GetNotificationChannelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_notification_channel]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_notification_channel(
        self,
        request: Union[
            notification_service.CreateNotificationChannelRequest, dict
        ] = None,
        *,
        name: str = None,
        notification_channel: notification.NotificationChannel = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannel:
        r"""Creates a new notification channel, representing a
        single notification endpoint such as an email address,
        SMS number, or PagerDuty service.

        Args:
            request (Union[google.cloud.monitoring_v3.types.CreateNotificationChannelRequest, dict]):
                The request object. The `CreateNotificationChannel`
                request.
            name (str):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                on which to execute the request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This names the container into which the channel will be
                written, this does not name the newly created channel.
                The resulting channel's name will have a normalized
                version of this field as a prefix, but will add
                ``/notificationChannels/[CHANNEL_ID]`` to identify the
                channel.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            notification_channel (google.cloud.monitoring_v3.types.NotificationChannel):
                Required. The definition of the ``NotificationChannel``
                to create.

                This corresponds to the ``notification_channel`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannel:
                A NotificationChannel is a medium through which an alert is
                   delivered when a policy violation is detected.
                   Examples of channels include email, SMS, and
                   third-party messaging applications. Fields containing
                   sensitive information like authentication tokens or
                   contact info are only partially populated on
                   retrieval.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, notification_channel])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.CreateNotificationChannelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, notification_service.CreateNotificationChannelRequest
        ):
            request = notification_service.CreateNotificationChannelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if notification_channel is not None:
                request.notification_channel = notification_channel

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_notification_channel
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_notification_channel(
        self,
        request: Union[
            notification_service.UpdateNotificationChannelRequest, dict
        ] = None,
        *,
        update_mask: field_mask_pb2.FieldMask = None,
        notification_channel: notification.NotificationChannel = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannel:
        r"""Updates a notification channel. Fields not specified
        in the field mask remain unchanged.

        Args:
            request (Union[google.cloud.monitoring_v3.types.UpdateNotificationChannelRequest, dict]):
                The request object. The `UpdateNotificationChannel`
                request.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            notification_channel (google.cloud.monitoring_v3.types.NotificationChannel):
                Required. A description of the changes to be applied to
                the specified notification channel. The description must
                provide a definition for fields to be updated; the names
                of these fields should also be included in the
                ``update_mask``.

                This corresponds to the ``notification_channel`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannel:
                A NotificationChannel is a medium through which an alert is
                   delivered when a policy violation is detected.
                   Examples of channels include email, SMS, and
                   third-party messaging applications. Fields containing
                   sensitive information like authentication tokens or
                   contact info are only partially populated on
                   retrieval.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([update_mask, notification_channel])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.UpdateNotificationChannelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, notification_service.UpdateNotificationChannelRequest
        ):
            request = notification_service.UpdateNotificationChannelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if update_mask is not None:
                request.update_mask = update_mask
            if notification_channel is not None:
                request.notification_channel = notification_channel

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_notification_channel
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("notification_channel.name", request.notification_channel.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_notification_channel(
        self,
        request: Union[
            notification_service.DeleteNotificationChannelRequest, dict
        ] = None,
        *,
        name: str = None,
        force: bool = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a notification channel.

        Args:
            request (Union[google.cloud.monitoring_v3.types.DeleteNotificationChannelRequest, dict]):
                The request object. The `DeleteNotificationChannel`
                request.
            name (str):
                Required. The channel for which to execute the request.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/notificationChannels/[CHANNEL_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            force (bool):
                If true, the notification channel
                will be deleted regardless of its use in
                alert policies (the policies will be
                updated to remove the channel). If
                false, channels that are still
                referenced by an existing alerting
                policy will fail to be deleted in a
                delete operation.

                This corresponds to the ``force`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, force])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.DeleteNotificationChannelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, notification_service.DeleteNotificationChannelRequest
        ):
            request = notification_service.DeleteNotificationChannelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if force is not None:
                request.force = force

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_notification_channel
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def send_notification_channel_verification_code(
        self,
        request: Union[
            notification_service.SendNotificationChannelVerificationCodeRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Causes a verification code to be delivered to the channel. The
        code can then be supplied in ``VerifyNotificationChannel`` to
        verify the channel.

        Args:
            request (Union[google.cloud.monitoring_v3.types.SendNotificationChannelVerificationCodeRequest, dict]):
                The request object. The
                `SendNotificationChannelVerificationCode` request.
            name (str):
                Required. The notification channel to
                which to send a verification code.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.SendNotificationChannelVerificationCodeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, notification_service.SendNotificationChannelVerificationCodeRequest
        ):
            request = notification_service.SendNotificationChannelVerificationCodeRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.send_notification_channel_verification_code
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def get_notification_channel_verification_code(
        self,
        request: Union[
            notification_service.GetNotificationChannelVerificationCodeRequest, dict
        ] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification_service.GetNotificationChannelVerificationCodeResponse:
        r"""Requests a verification code for an already verified
        channel that can then be used in a call to
        VerifyNotificationChannel() on a different channel with
        an equivalent identity in the same or in a different
        project. This makes it possible to copy a channel
        between projects without requiring manual reverification
        of the channel. If the channel is not in the verified
        state, this method will fail (in other words, this may
        only be used if the
        SendNotificationChannelVerificationCode and
        VerifyNotificationChannel paths have already been used
        to put the given channel into the verified state).

        There is no guarantee that the verification codes
        returned by this method will be of a similar structure
        or form as the ones that are delivered to the channel
        via SendNotificationChannelVerificationCode; while
        VerifyNotificationChannel() will recognize both the
        codes delivered via
        SendNotificationChannelVerificationCode() and returned
        from GetNotificationChannelVerificationCode(), it is
        typically the case that the verification codes delivered
        via
        SendNotificationChannelVerificationCode() will be
        shorter and also have a shorter expiration (e.g. codes
        such as "G-123456") whereas GetVerificationCode() will
        typically return a much longer, websafe base 64 encoded
        string that has a longer expiration time.

        Args:
            request (Union[google.cloud.monitoring_v3.types.GetNotificationChannelVerificationCodeRequest, dict]):
                The request object. The
                `GetNotificationChannelVerificationCode` request.
            name (str):
                Required. The notification channel
                for which a verification code is to be
                generated and retrieved. This must name
                a channel that is already verified; if
                the specified channel is not verified,
                the request will fail.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.GetNotificationChannelVerificationCodeResponse:
                The GetNotificationChannelVerificationCode request.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.GetNotificationChannelVerificationCodeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, notification_service.GetNotificationChannelVerificationCodeRequest
        ):
            request = notification_service.GetNotificationChannelVerificationCodeRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_notification_channel_verification_code
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def verify_notification_channel(
        self,
        request: Union[
            notification_service.VerifyNotificationChannelRequest, dict
        ] = None,
        *,
        name: str = None,
        code: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannel:
        r"""Verifies a ``NotificationChannel`` by proving receipt of the
        code delivered to the channel as a result of calling
        ``SendNotificationChannelVerificationCode``.

        Args:
            request (Union[google.cloud.monitoring_v3.types.VerifyNotificationChannelRequest, dict]):
                The request object. The `VerifyNotificationChannel`
                request.
            name (str):
                Required. The notification channel to
                verify.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            code (str):
                Required. The verification code that was delivered to
                the channel as a result of invoking the
                ``SendNotificationChannelVerificationCode`` API method
                or that was retrieved from a verified channel via
                ``GetNotificationChannelVerificationCode``. For example,
                one might have "G-123456" or "TKNZGhhd2EyN3I1MnRnMjRv"
                (in general, one is only guaranteed that the code is
                valid UTF-8; one should not make any assumptions
                regarding the structure or format of the code).

                This corresponds to the ``code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannel:
                A NotificationChannel is a medium through which an alert is
                   delivered when a policy violation is detected.
                   Examples of channels include email, SMS, and
                   third-party messaging applications. Fields containing
                   sensitive information like authentication tokens or
                   contact info are only partially populated on
                   retrieval.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, code])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a notification_service.VerifyNotificationChannelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, notification_service.VerifyNotificationChannelRequest
        ):
            request = notification_service.VerifyNotificationChannelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if code is not None:
                request.code = code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.verify_notification_channel
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-monitoring",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("NotificationChannelServiceClient",)
