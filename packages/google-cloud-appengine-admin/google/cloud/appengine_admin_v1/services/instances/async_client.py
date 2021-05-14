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

from google.api_core import operation as gac_operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.appengine_admin_v1.services.instances import pagers
from google.cloud.appengine_admin_v1.types import appengine
from google.cloud.appengine_admin_v1.types import instance
from google.cloud.appengine_admin_v1.types import operation as ga_operation
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import InstancesTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import InstancesGrpcAsyncIOTransport
from .client import InstancesClient


class InstancesAsyncClient:
    """Manages instances of a version."""

    _client: InstancesClient

    DEFAULT_ENDPOINT = InstancesClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = InstancesClient.DEFAULT_MTLS_ENDPOINT

    instance_path = staticmethod(InstancesClient.instance_path)
    parse_instance_path = staticmethod(InstancesClient.parse_instance_path)
    common_billing_account_path = staticmethod(
        InstancesClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        InstancesClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(InstancesClient.common_folder_path)
    parse_common_folder_path = staticmethod(InstancesClient.parse_common_folder_path)
    common_organization_path = staticmethod(InstancesClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        InstancesClient.parse_common_organization_path
    )
    common_project_path = staticmethod(InstancesClient.common_project_path)
    parse_common_project_path = staticmethod(InstancesClient.parse_common_project_path)
    common_location_path = staticmethod(InstancesClient.common_location_path)
    parse_common_location_path = staticmethod(
        InstancesClient.parse_common_location_path
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
            InstancesAsyncClient: The constructed client.
        """
        return InstancesClient.from_service_account_info.__func__(InstancesAsyncClient, info, *args, **kwargs)  # type: ignore

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
            InstancesAsyncClient: The constructed client.
        """
        return InstancesClient.from_service_account_file.__func__(InstancesAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> InstancesTransport:
        """Returns the transport used by the client instance.

        Returns:
            InstancesTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(InstancesClient).get_transport_class, type(InstancesClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, InstancesTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the instances client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.InstancesTransport]): The
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
        self._client = InstancesClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_instances(
        self,
        request: appengine.ListInstancesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstancesAsyncPager:
        r"""Lists the instances of a version.

        Tip: To aggregate details about instances over time, see the
        `Stackdriver Monitoring
        API <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list>`__.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.ListInstancesRequest`):
                The request object. Request message for
                `Instances.ListInstances`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.services.instances.pagers.ListInstancesAsyncPager:
                Response message for Instances.ListInstances.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = appengine.ListInstancesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_instances,
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
        response = pagers.ListInstancesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_instance(
        self,
        request: appengine.GetInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instance.Instance:
        r"""Gets instance information.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.GetInstanceRequest`):
                The request object. Request message for
                `Instances.GetInstance`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.appengine_admin_v1.types.Instance:
                An Instance resource is the computing
                unit that App Engine uses to
                automatically scale an application.

        """
        # Create or coerce a protobuf request object.
        request = appengine.GetInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_instance,
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

    async def delete_instance(
        self,
        request: appengine.DeleteInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Stops a running instance.

        The instance might be automatically recreated based on the
        scaling settings of the version. For more information, see "How
        Instances are Managed" (`standard
        environment <https://cloud.google.com/appengine/docs/standard/python/how-instances-are-managed>`__
        \| `flexible
        environment <https://cloud.google.com/appengine/docs/flexible/python/how-instances-are-managed>`__).

        To ensure that instances are not re-created and avoid getting
        billed, you can stop all instances within the target version by
        changing the serving status of the version to ``STOPPED`` with
        the
        ```apps.services.versions.patch`` <https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps.services.versions/patch>`__
        method.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.DeleteInstanceRequest`):
                The request object. Request message for
                `Instances.DeleteInstance`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        request = appengine.DeleteInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_instance,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=ga_operation.OperationMetadataV1,
        )

        # Done; return the response.
        return response

    async def debug_instance(
        self,
        request: appengine.DebugInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Enables debugging on a VM instance. This allows you
        to use the SSH command to connect to the virtual machine
        where the instance lives. While in "debug mode", the
        instance continues to serve live traffic. You should
        delete the instance when you are done debugging and then
        allow the system to take over and determine if another
        instance should be started.

        Only applicable for instances in App Engine flexible
        environment.

        Args:
            request (:class:`google.cloud.appengine_admin_v1.types.DebugInstanceRequest`):
                The request object. Request message for
                `Instances.DebugInstance`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.appengine_admin_v1.types.Instance` An Instance resource is the computing unit that App Engine uses to
                   automatically scale an application.

        """
        # Create or coerce a protobuf request object.
        request = appengine.DebugInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.debug_instance,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            instance.Instance,
            metadata_type=ga_operation.OperationMetadataV1,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-appengine-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("InstancesAsyncClient",)
