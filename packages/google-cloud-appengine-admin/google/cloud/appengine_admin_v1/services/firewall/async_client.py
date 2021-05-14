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

from google.cloud.appengine_admin_v1.services.firewall import pagers
from google.cloud.appengine_admin_v1.types import appengine
from google.cloud.appengine_admin_v1.types import firewall
from .transports.base import FirewallTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import FirewallGrpcAsyncIOTransport
from .client import FirewallClient


class FirewallAsyncClient:
    """Firewall resources are used to define a collection of access
    control rules for an Application. Each rule is defined with a
    position which specifies the rule's order in the sequence of
    rules, an IP range to be matched against requests, and an action
    to take upon matching requests.
    Every request is evaluated against the Firewall rules in
    priority order. Processesing stops at the first rule which
    matches the request's IP address. A final rule always specifies
    an action that applies to all remaining IP addresses. The
    default final rule for a newly-created application will be set
    to "allow" if not otherwise specified by the user.
    """

    _client: FirewallClient

    DEFAULT_ENDPOINT = FirewallClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = FirewallClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        FirewallClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        FirewallClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(FirewallClient.common_folder_path)
    parse_common_folder_path = staticmethod(FirewallClient.parse_common_folder_path)
    common_organization_path = staticmethod(FirewallClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        FirewallClient.parse_common_organization_path
    )
    common_project_path = staticmethod(FirewallClient.common_project_path)
    parse_common_project_path = staticmethod(FirewallClient.parse_common_project_path)
    common_location_path = staticmethod(FirewallClient.common_location_path)
    parse_common_location_path = staticmethod(FirewallClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            FirewallAsyncClient: The constructed client.
        """
        return FirewallClient.from_service_account_info.__func__(FirewallAsyncClient, info, *args, **kwargs)  # type: ignore

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
            FirewallAsyncClient: The constructed client.
        """
        return FirewallClient.from_service_account_file.__func__(FirewallAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> FirewallTransport:
        """Returns the transport used by the client instance.

        Returns:
            FirewallTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(FirewallClient).get_transport_class, type(FirewallClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, FirewallTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the firewall client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.FirewallTransport]): The
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
        self._client = FirewallClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_ingress_rules(
        self,
        request: appengine.ListIngressRulesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListIngressRulesAsyncPager:
        r"""Lists the firewall rules of an application.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.ListIngressRulesRequest`):
                The request object. Request message for
                `Firewall.ListIngressRules`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.services.firewall.pagers.ListIngressRulesAsyncPager:
                Response message for Firewall.ListIngressRules.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = appengine.ListIngressRulesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_ingress_rules,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListIngressRulesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def batch_update_ingress_rules(
        self,
        request: appengine.BatchUpdateIngressRulesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> appengine.BatchUpdateIngressRulesResponse:
        r"""Replaces the entire firewall ruleset in one bulk operation. This
        overrides and replaces the rules of an existing firewall with
        the new rules.

        If the final rule does not match traffic with the '*' wildcard
        IP range, then an "allow all" rule is explicitly added to the
        end of the list.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.BatchUpdateIngressRulesRequest`):
                The request object. Request message for
                `Firewall.BatchUpdateIngressRules`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.BatchUpdateIngressRulesResponse:
                Response message for Firewall.UpdateAllIngressRules.
        """
        # Create or coerce a protobuf request object.
        request = appengine.BatchUpdateIngressRulesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_update_ingress_rules,
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

    async def create_ingress_rule(
        self,
        request: appengine.CreateIngressRuleRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> firewall.FirewallRule:
        r"""Creates a firewall rule for the application.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.CreateIngressRuleRequest`):
                The request object. Request message for
                `Firewall.CreateIngressRule`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.FirewallRule:
                A single firewall rule that is
                evaluated against incoming traffic and
                provides an action to take on matched
                requests.

        """
        # Create or coerce a protobuf request object.
        request = appengine.CreateIngressRuleRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_ingress_rule,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_ingress_rule(
        self,
        request: appengine.GetIngressRuleRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> firewall.FirewallRule:
        r"""Gets the specified firewall rule.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.GetIngressRuleRequest`):
                The request object. Request message for
                `Firewall.GetIngressRule`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.FirewallRule:
                A single firewall rule that is
                evaluated against incoming traffic and
                provides an action to take on matched
                requests.

        """
        # Create or coerce a protobuf request object.
        request = appengine.GetIngressRuleRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_ingress_rule,
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

    async def update_ingress_rule(
        self,
        request: appengine.UpdateIngressRuleRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> firewall.FirewallRule:
        r"""Updates the specified firewall rule.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.UpdateIngressRuleRequest`):
                The request object. Request message for
                `Firewall.UpdateIngressRule`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.FirewallRule:
                A single firewall rule that is
                evaluated against incoming traffic and
                provides an action to take on matched
                requests.

        """
        # Create or coerce a protobuf request object.
        request = appengine.UpdateIngressRuleRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_ingress_rule,
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

    async def delete_ingress_rule(
        self,
        request: appengine.DeleteIngressRuleRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified firewall rule.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.DeleteIngressRuleRequest`):
                The request object. Request message for
                `Firewall.DeleteIngressRule`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = appengine.DeleteIngressRuleRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_ingress_rule,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-appengine-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("FirewallAsyncClient",)
