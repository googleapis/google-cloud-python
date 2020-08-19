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
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dialogflowcx_v3beta1.services.session_entity_types import pagers
from google.cloud.dialogflowcx_v3beta1.types import entity_type
from google.cloud.dialogflowcx_v3beta1.types import session_entity_type
from google.cloud.dialogflowcx_v3beta1.types import (
    session_entity_type as gcdc_session_entity_type,
)
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore

from .transports.base import SessionEntityTypesTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import SessionEntityTypesGrpcTransport
from .transports.grpc_asyncio import SessionEntityTypesGrpcAsyncIOTransport


class SessionEntityTypesClientMeta(type):
    """Metaclass for the SessionEntityTypes client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[SessionEntityTypesTransport]]
    _transport_registry["grpc"] = SessionEntityTypesGrpcTransport
    _transport_registry["grpc_asyncio"] = SessionEntityTypesGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[SessionEntityTypesTransport]:
        """Return an appropriate transport class.

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


class SessionEntityTypesClient(metaclass=SessionEntityTypesClientMeta):
    """Service for managing
    [SessionEntityTypes][google.cloud.dialogflow.cx.v3beta1.SessionEntityType].
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
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

    DEFAULT_ENDPOINT = "dialogflow.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

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
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def session_entity_type_path(
        project: str, location: str, agent: str, session: str, entity_type: str,
    ) -> str:
        """Return a fully-qualified session_entity_type string."""
        return "projects/{project}/locations/{location}/agents/{agent}/sessions/{session}/entityTypes/{entity_type}".format(
            project=project,
            location=location,
            agent=agent,
            session=session,
            entity_type=entity_type,
        )

    @staticmethod
    def parse_session_entity_type_path(path: str) -> Dict[str, str]:
        """Parse a session_entity_type path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/agents/(?P<agent>.+?)/sessions/(?P<session>.+?)/entityTypes/(?P<entity_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, SessionEntityTypesTransport] = None,
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the session entity types client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.SessionEntityTypesTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.
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
            client_options = ClientOptions.from_dict(client_options)
        if client_options is None:
            client_options = ClientOptions.ClientOptions()

        if client_options.api_endpoint is None:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS", "never")
            if use_mtls_env == "never":
                client_options.api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                client_options.api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                has_client_cert_source = (
                    client_options.client_cert_source is not None
                    or mtls.has_default_client_cert_source()
                )
                client_options.api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if has_client_cert_source
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, SessionEntityTypesTransport):
            # transport is a SessionEntityTypesTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=client_options.api_endpoint,
                scopes=client_options.scopes,
                api_mtls_endpoint=client_options.api_endpoint,
                client_cert_source=client_options.client_cert_source,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def list_session_entity_types(
        self,
        request: session_entity_type.ListSessionEntityTypesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSessionEntityTypesPager:
        r"""Returns the list of all session entity types in the
        specified session.

        Args:
            request (:class:`~.session_entity_type.ListSessionEntityTypesRequest`):
                The request object. The request message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.cx.v3beta1.SessionEntityTypes.ListSessionEntityTypes].
            parent (:class:`str`):
                Required. The session to list all session entity types
                from. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListSessionEntityTypesPager:
                The response message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.cx.v3beta1.SessionEntityTypes.ListSessionEntityTypes].

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

        # Minor optimization to avoid making a copy if the user passes
        # in a session_entity_type.ListSessionEntityTypesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, session_entity_type.ListSessionEntityTypesRequest):
            request = session_entity_type.ListSessionEntityTypesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_session_entity_types
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListSessionEntityTypesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_session_entity_type(
        self,
        request: session_entity_type.GetSessionEntityTypeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> session_entity_type.SessionEntityType:
        r"""Retrieves the specified session entity type.

        Args:
            request (:class:`~.session_entity_type.GetSessionEntityTypeRequest`):
                The request object. The request message for
                [SessionEntityTypes.GetSessionEntityType][google.cloud.dialogflow.cx.v3beta1.SessionEntityTypes.GetSessionEntityType].
            name (:class:`str`):
                Required. The name of the session entity type. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.session_entity_type.SessionEntityType:
                Session entity types are referred to as **User** entity
                types and are entities that are built for an individual
                user such as favorites, preferences, playlists, and so
                on.

                You can redefine a session entity type at the session
                level to extend or replace a [custom entity
                type][google.cloud.dialogflow.cx.v3beta1.EntityType] at
                the user session level (we refer to the entity types
                defined at the agent level as "custom entity types").

                Note: session entity types apply to all queries,
                regardless of the language.

                For more information about entity types, see the
                `Dialogflow
                documentation <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

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
        # in a session_entity_type.GetSessionEntityTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, session_entity_type.GetSessionEntityTypeRequest):
            request = session_entity_type.GetSessionEntityTypeRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_session_entity_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_session_entity_type(
        self,
        request: gcdc_session_entity_type.CreateSessionEntityTypeRequest = None,
        *,
        parent: str = None,
        session_entity_type: gcdc_session_entity_type.SessionEntityType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_session_entity_type.SessionEntityType:
        r"""Creates a session entity type.
        If the specified session entity type already exists,
        overrides the session entity type.

        Args:
            request (:class:`~.gcdc_session_entity_type.CreateSessionEntityTypeRequest`):
                The request object. The request message for
                [SessionEntityTypes.CreateSessionEntityType][google.cloud.dialogflow.cx.v3beta1.SessionEntityTypes.CreateSessionEntityType].
            parent (:class:`str`):
                Required. The session to create a session entity type
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            session_entity_type (:class:`~.gcdc_session_entity_type.SessionEntityType`):
                Required. The session entity type to
                create.
                This corresponds to the ``session_entity_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcdc_session_entity_type.SessionEntityType:
                Session entity types are referred to as **User** entity
                types and are entities that are built for an individual
                user such as favorites, preferences, playlists, and so
                on.

                You can redefine a session entity type at the session
                level to extend or replace a [custom entity
                type][google.cloud.dialogflow.cx.v3beta1.EntityType] at
                the user session level (we refer to the entity types
                defined at the agent level as "custom entity types").

                Note: session entity types apply to all queries,
                regardless of the language.

                For more information about entity types, see the
                `Dialogflow
                documentation <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, session_entity_type])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcdc_session_entity_type.CreateSessionEntityTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, gcdc_session_entity_type.CreateSessionEntityTypeRequest
        ):
            request = gcdc_session_entity_type.CreateSessionEntityTypeRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if session_entity_type is not None:
                request.session_entity_type = session_entity_type

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_session_entity_type
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_session_entity_type(
        self,
        request: gcdc_session_entity_type.UpdateSessionEntityTypeRequest = None,
        *,
        session_entity_type: gcdc_session_entity_type.SessionEntityType = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_session_entity_type.SessionEntityType:
        r"""Updates the specified session entity type.

        Args:
            request (:class:`~.gcdc_session_entity_type.UpdateSessionEntityTypeRequest`):
                The request object. The request message for
                [SessionEntityTypes.UpdateSessionEntityType][google.cloud.dialogflow.cx.v3beta1.SessionEntityTypes.UpdateSessionEntityType].
            session_entity_type (:class:`~.gcdc_session_entity_type.SessionEntityType`):
                Required. The session entity type to update. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.
                This corresponds to the ``session_entity_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                The mask to control which fields get
                updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcdc_session_entity_type.SessionEntityType:
                Session entity types are referred to as **User** entity
                types and are entities that are built for an individual
                user such as favorites, preferences, playlists, and so
                on.

                You can redefine a session entity type at the session
                level to extend or replace a [custom entity
                type][google.cloud.dialogflow.cx.v3beta1.EntityType] at
                the user session level (we refer to the entity types
                defined at the agent level as "custom entity types").

                Note: session entity types apply to all queries,
                regardless of the language.

                For more information about entity types, see the
                `Dialogflow
                documentation <https://cloud.google.com/dialogflow/docs/entities-overview>`__.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([session_entity_type, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcdc_session_entity_type.UpdateSessionEntityTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, gcdc_session_entity_type.UpdateSessionEntityTypeRequest
        ):
            request = gcdc_session_entity_type.UpdateSessionEntityTypeRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if session_entity_type is not None:
                request.session_entity_type = session_entity_type
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_session_entity_type
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("session_entity_type.name", request.session_entity_type.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_session_entity_type(
        self,
        request: session_entity_type.DeleteSessionEntityTypeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified session entity type.

        Args:
            request (:class:`~.session_entity_type.DeleteSessionEntityTypeRequest`):
                The request object. The request message for
                [SessionEntityTypes.DeleteSessionEntityType][google.cloud.dialogflow.cx.v3beta1.SessionEntityTypes.DeleteSessionEntityType].
            name (:class:`str`):
                Required. The name of the session entity type to delete.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>/entityTypes/<Entity Type ID>``.
                If ``Environment ID`` is not specified, we assume
                default 'draft' environment.
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
        # in a session_entity_type.DeleteSessionEntityTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, session_entity_type.DeleteSessionEntityTypeRequest):
            request = session_entity_type.DeleteSessionEntityTypeRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_session_entity_type
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SessionEntityTypesClient",)
