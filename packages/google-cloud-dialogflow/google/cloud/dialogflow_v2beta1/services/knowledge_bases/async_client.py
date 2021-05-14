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

from google.cloud.dialogflow_v2beta1.services.knowledge_bases import pagers
from google.cloud.dialogflow_v2beta1.types import knowledge_base
from google.cloud.dialogflow_v2beta1.types import knowledge_base as gcd_knowledge_base
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import KnowledgeBasesTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import KnowledgeBasesGrpcAsyncIOTransport
from .client import KnowledgeBasesClient


class KnowledgeBasesAsyncClient:
    """Service for managing
    [KnowledgeBases][google.cloud.dialogflow.v2beta1.KnowledgeBase].
    """

    _client: KnowledgeBasesClient

    DEFAULT_ENDPOINT = KnowledgeBasesClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = KnowledgeBasesClient.DEFAULT_MTLS_ENDPOINT

    knowledge_base_path = staticmethod(KnowledgeBasesClient.knowledge_base_path)
    parse_knowledge_base_path = staticmethod(
        KnowledgeBasesClient.parse_knowledge_base_path
    )
    common_billing_account_path = staticmethod(
        KnowledgeBasesClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        KnowledgeBasesClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(KnowledgeBasesClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        KnowledgeBasesClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        KnowledgeBasesClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        KnowledgeBasesClient.parse_common_organization_path
    )
    common_project_path = staticmethod(KnowledgeBasesClient.common_project_path)
    parse_common_project_path = staticmethod(
        KnowledgeBasesClient.parse_common_project_path
    )
    common_location_path = staticmethod(KnowledgeBasesClient.common_location_path)
    parse_common_location_path = staticmethod(
        KnowledgeBasesClient.parse_common_location_path
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
            KnowledgeBasesAsyncClient: The constructed client.
        """
        return KnowledgeBasesClient.from_service_account_info.__func__(KnowledgeBasesAsyncClient, info, *args, **kwargs)  # type: ignore

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
            KnowledgeBasesAsyncClient: The constructed client.
        """
        return KnowledgeBasesClient.from_service_account_file.__func__(KnowledgeBasesAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> KnowledgeBasesTransport:
        """Returns the transport used by the client instance.

        Returns:
            KnowledgeBasesTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(KnowledgeBasesClient).get_transport_class, type(KnowledgeBasesClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, KnowledgeBasesTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the knowledge bases client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.KnowledgeBasesTransport]): The
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
        self._client = KnowledgeBasesClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_knowledge_bases(
        self,
        request: knowledge_base.ListKnowledgeBasesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListKnowledgeBasesAsyncPager:
        r"""Returns the list of all knowledge bases of the specified agent.

        Note: The ``projects.agent.knowledgeBases`` resource is
        deprecated; only use ``projects.knowledgeBases``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.ListKnowledgeBasesRequest`):
                The request object. Request message for
                [KnowledgeBases.ListKnowledgeBases][google.cloud.dialogflow.v2beta1.KnowledgeBases.ListKnowledgeBases].
            parent (:class:`str`):
                Required. The project to list of knowledge bases for.
                Format:
                ``projects/<Project ID>/locations/<Location ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.services.knowledge_bases.pagers.ListKnowledgeBasesAsyncPager:
                Response message for
                [KnowledgeBases.ListKnowledgeBases][google.cloud.dialogflow.v2beta1.KnowledgeBases.ListKnowledgeBases].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = knowledge_base.ListKnowledgeBasesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_knowledge_bases,
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
        response = pagers.ListKnowledgeBasesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_knowledge_base(
        self,
        request: knowledge_base.GetKnowledgeBaseRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> knowledge_base.KnowledgeBase:
        r"""Retrieves the specified knowledge base.

        Note: The ``projects.agent.knowledgeBases`` resource is
        deprecated; only use ``projects.knowledgeBases``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.GetKnowledgeBaseRequest`):
                The request object. Request message for
                [KnowledgeBases.GetKnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBases.GetKnowledgeBase].
            name (:class:`str`):
                Required. The name of the knowledge base to retrieve.
                Format
                ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.KnowledgeBase:
                A knowledge base represents a collection of knowledge documents that you
                   provide to Dialogflow. Your knowledge documents
                   contain information that may be useful during
                   conversations with end-users. Some Dialogflow
                   features use knowledge bases when looking for a
                   response to an end-user input.

                   For more information, see the [knowledge base
                   guide](\ https://cloud.google.com/dialogflow/docs/how/knowledge-bases).

                   Note: The projects.agent.knowledgeBases resource is
                   deprecated; only use projects.knowledgeBases.

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

        request = knowledge_base.GetKnowledgeBaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_knowledge_base,
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

    async def create_knowledge_base(
        self,
        request: gcd_knowledge_base.CreateKnowledgeBaseRequest = None,
        *,
        parent: str = None,
        knowledge_base: gcd_knowledge_base.KnowledgeBase = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_knowledge_base.KnowledgeBase:
        r"""Creates a knowledge base.

        Note: The ``projects.agent.knowledgeBases`` resource is
        deprecated; only use ``projects.knowledgeBases``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.CreateKnowledgeBaseRequest`):
                The request object. Request message for
                [KnowledgeBases.CreateKnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBases.CreateKnowledgeBase].
            parent (:class:`str`):
                Required. The project to create a knowledge base for.
                Format:
                ``projects/<Project ID>/locations/<Location ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            knowledge_base (:class:`google.cloud.dialogflow_v2beta1.types.KnowledgeBase`):
                Required. The knowledge base to
                create.

                This corresponds to the ``knowledge_base`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.KnowledgeBase:
                A knowledge base represents a collection of knowledge documents that you
                   provide to Dialogflow. Your knowledge documents
                   contain information that may be useful during
                   conversations with end-users. Some Dialogflow
                   features use knowledge bases when looking for a
                   response to an end-user input.

                   For more information, see the [knowledge base
                   guide](\ https://cloud.google.com/dialogflow/docs/how/knowledge-bases).

                   Note: The projects.agent.knowledgeBases resource is
                   deprecated; only use projects.knowledgeBases.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, knowledge_base])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_knowledge_base.CreateKnowledgeBaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if knowledge_base is not None:
            request.knowledge_base = knowledge_base

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_knowledge_base,
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

    async def delete_knowledge_base(
        self,
        request: knowledge_base.DeleteKnowledgeBaseRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified knowledge base.

        Note: The ``projects.agent.knowledgeBases`` resource is
        deprecated; only use ``projects.knowledgeBases``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.DeleteKnowledgeBaseRequest`):
                The request object. Request message for
                [KnowledgeBases.DeleteKnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBases.DeleteKnowledgeBase].
            name (:class:`str`):
                Required. The name of the knowledge base to delete.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>``.

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

        request = knowledge_base.DeleteKnowledgeBaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_knowledge_base,
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

    async def update_knowledge_base(
        self,
        request: gcd_knowledge_base.UpdateKnowledgeBaseRequest = None,
        *,
        knowledge_base: gcd_knowledge_base.KnowledgeBase = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_knowledge_base.KnowledgeBase:
        r"""Updates the specified knowledge base.

        Note: The ``projects.agent.knowledgeBases`` resource is
        deprecated; only use ``projects.knowledgeBases``.

        Args:
            request (:class:`google.cloud.dialogflow_v2beta1.types.UpdateKnowledgeBaseRequest`):
                The request object. Request message for
                [KnowledgeBases.UpdateKnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBases.UpdateKnowledgeBase].
            knowledge_base (:class:`google.cloud.dialogflow_v2beta1.types.KnowledgeBase`):
                Required. The knowledge base to
                update.

                This corresponds to the ``knowledge_base`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. Not specified means ``update all``. Currently,
                only ``display_name`` can be updated, an InvalidArgument
                will be returned for attempting to update other fields.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.KnowledgeBase:
                A knowledge base represents a collection of knowledge documents that you
                   provide to Dialogflow. Your knowledge documents
                   contain information that may be useful during
                   conversations with end-users. Some Dialogflow
                   features use knowledge bases when looking for a
                   response to an end-user input.

                   For more information, see the [knowledge base
                   guide](\ https://cloud.google.com/dialogflow/docs/how/knowledge-bases).

                   Note: The projects.agent.knowledgeBases resource is
                   deprecated; only use projects.knowledgeBases.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([knowledge_base, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcd_knowledge_base.UpdateKnowledgeBaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if knowledge_base is not None:
            request.knowledge_base = knowledge_base
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_knowledge_base,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("knowledge_base.name", request.knowledge_base.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("KnowledgeBasesAsyncClient",)
