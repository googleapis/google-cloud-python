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
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.binaryauthorization_v1.types import resources
from google.cloud.binaryauthorization_v1.types import service
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import SystemPolicyV1Transport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import SystemPolicyV1GrpcAsyncIOTransport
from .client import SystemPolicyV1Client


class SystemPolicyV1AsyncClient:
    """API for working with the system policy."""

    _client: SystemPolicyV1Client

    DEFAULT_ENDPOINT = SystemPolicyV1Client.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = SystemPolicyV1Client.DEFAULT_MTLS_ENDPOINT

    policy_path = staticmethod(SystemPolicyV1Client.policy_path)
    parse_policy_path = staticmethod(SystemPolicyV1Client.parse_policy_path)
    common_billing_account_path = staticmethod(
        SystemPolicyV1Client.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        SystemPolicyV1Client.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(SystemPolicyV1Client.common_folder_path)
    parse_common_folder_path = staticmethod(
        SystemPolicyV1Client.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        SystemPolicyV1Client.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        SystemPolicyV1Client.parse_common_organization_path
    )
    common_project_path = staticmethod(SystemPolicyV1Client.common_project_path)
    parse_common_project_path = staticmethod(
        SystemPolicyV1Client.parse_common_project_path
    )
    common_location_path = staticmethod(SystemPolicyV1Client.common_location_path)
    parse_common_location_path = staticmethod(
        SystemPolicyV1Client.parse_common_location_path
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
            SystemPolicyV1AsyncClient: The constructed client.
        """
        return SystemPolicyV1Client.from_service_account_info.__func__(SystemPolicyV1AsyncClient, info, *args, **kwargs)  # type: ignore

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
            SystemPolicyV1AsyncClient: The constructed client.
        """
        return SystemPolicyV1Client.from_service_account_file.__func__(SystemPolicyV1AsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SystemPolicyV1Transport:
        """Returns the transport used by the client instance.

        Returns:
            SystemPolicyV1Transport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(SystemPolicyV1Client).get_transport_class, type(SystemPolicyV1Client)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, SystemPolicyV1Transport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the system policy v1 client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SystemPolicyV1Transport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
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

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = SystemPolicyV1Client(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_system_policy(
        self,
        request: service.GetSystemPolicyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Policy:
        r"""Gets the current system policy in the specified
        location.

        Args:
            request (:class:`google.cloud.binaryauthorization_v1.types.GetSystemPolicyRequest`):
                The request object. Request to read the current system
                policy.
            name (:class:`str`):
                Required. The resource name, in the format
                ``locations/*/policy``. Note that the system policy is
                not associated with a project.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.binaryauthorization_v1.types.Policy:
                A [policy][google.cloud.binaryauthorization.v1.Policy]
                for container image binary authorization.

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

        request = service.GetSystemPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_system_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-binary-authorization",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SystemPolicyV1AsyncClient",)
