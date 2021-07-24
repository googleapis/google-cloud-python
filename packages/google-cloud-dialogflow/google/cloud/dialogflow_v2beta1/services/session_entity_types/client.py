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
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dialogflow_v2beta1.services.session_entity_types import pagers
from google.cloud.dialogflow_v2beta1.types import entity_type
from google.cloud.dialogflow_v2beta1.types import session_entity_type
from google.cloud.dialogflow_v2beta1.types import (
    session_entity_type as gcd_session_entity_type,
)
from google.protobuf import field_mask_pb2  # type: ignore
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


class SessionEntityTypesClient(metaclass=SessionEntityTypesClientMeta):
    """Service for managing
    [SessionEntityTypes][google.cloud.dialogflow.v2beta1.SessionEntityType].
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

    DEFAULT_ENDPOINT = "dialogflow.googleapis.com"
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
            SessionEntityTypesClient: The constructed client.
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
            SessionEntityTypesClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> SessionEntityTypesTransport:
        """Returns the transport used by the client instance.

        Returns:
            SessionEntityTypesTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def session_entity_type_path(project: str, session: str, entity_type: str,) -> str:
        """Returns a fully-qualified session_entity_type string."""
        return "projects/{project}/agent/sessions/{session}/entityTypes/{entity_type}".format(
            project=project, session=session, entity_type=entity_type,
        )

    @staticmethod
    def parse_session_entity_type_path(path: str) -> Dict[str, str]:
        """Parses a session_entity_type path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/agent/sessions/(?P<session>.+?)/entityTypes/(?P<entity_type>.+?)$",
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
        transport: Union[str, SessionEntityTypesTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the session entity types client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, SessionEntityTypesTransport]): The
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
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
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
        if isinstance(transport, SessionEntityTypesTransport):
            # transport is a SessionEntityTypesTransport instance.
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
                always_use_jwt_access=(
                    Transport == type(self).get_transport_class("grpc")
                    or Transport == type(self).get_transport_class("grpc_asyncio")
                ),
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
        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (google.cloud.dialogflow_v2beta1.types.ListSessionEntityTypesRequest):
                The request object. The request message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.v2beta1.SessionEntityTypes.ListSessionEntityTypes].
            parent (str):
                Required. The session to list all session entity types
                from. Supported formats:

                -  \`projects//agent/sessions/,
                -  ``projects/<Project ID>/locations/<Location ID>/agent/sessions/<Session ID>``,
                -  ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``,
                -  ``projects/<Project ID>/locations/<Location ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``,

                If ``Location ID`` is not specified we assume default
                'us' location. If ``Environment ID`` is not specified,
                we assume default 'draft' environment. If ``User ID`` is
                not specified, we assume default '-' user.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.services.session_entity_types.pagers.ListSessionEntityTypesPager:
                The response message for
                [SessionEntityTypes.ListSessionEntityTypes][google.cloud.dialogflow.v2beta1.SessionEntityTypes.ListSessionEntityTypes].

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
        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (google.cloud.dialogflow_v2beta1.types.GetSessionEntityTypeRequest):
                The request object. The request message for
                [SessionEntityTypes.GetSessionEntityType][google.cloud.dialogflow.v2beta1.SessionEntityTypes.GetSessionEntityType].
            name (str):
                Required. The name of the session entity type. Supported
                formats:

                -  ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                -  ``projects/<Project ID>/locations/<Location ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                -  ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                -  ``projects/<Project ID>/locations/<Location ID>/agent/environments/ <Environment ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``

                If ``Location ID`` is not specified we assume default
                'us' location. If ``Environment ID`` is not specified,
                we assume default 'draft' environment. If ``User ID`` is
                not specified, we assume default '-' user.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.SessionEntityType:
                A session represents a conversation between a Dialogflow agent and an
                   end-user. You can create special entities, called
                   session entities, during a session. Session entities
                   can extend or replace custom entity types and only
                   exist during the session that they were created for.
                   All session data, including session entities, is
                   stored by Dialogflow for 20 minutes.

                   For more information, see the [session entity
                   guide](\ https://cloud.google.com/dialogflow/docs/entities-session).

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
        request: gcd_session_entity_type.CreateSessionEntityTypeRequest = None,
        *,
        parent: str = None,
        session_entity_type: gcd_session_entity_type.SessionEntityType = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_session_entity_type.SessionEntityType:
        r"""Creates a session entity type.
        If the specified session entity type already exists,
        overrides the session entity type.

        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (google.cloud.dialogflow_v2beta1.types.CreateSessionEntityTypeRequest):
                The request object. The request message for
                [SessionEntityTypes.CreateSessionEntityType][google.cloud.dialogflow.v2beta1.SessionEntityTypes.CreateSessionEntityType].
            parent (str):
                Required. The session to create a session entity type
                for. Supported formats:

                -  \`projects//agent/sessions/,
                -  ``projects/<Project ID>/locations/<Location ID>/agent/sessions/<Session ID>``,
                -  ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``,
                -  ``projects/<Project ID>/locations/<Location ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``,

                If ``Location ID`` is not specified we assume default
                'us' location. If ``Environment ID`` is not specified,
                we assume default 'draft' environment. If ``User ID`` is
                not specified, we assume default '-' user.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            session_entity_type (google.cloud.dialogflow_v2beta1.types.SessionEntityType):
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
            google.cloud.dialogflow_v2beta1.types.SessionEntityType:
                A session represents a conversation between a Dialogflow agent and an
                   end-user. You can create special entities, called
                   session entities, during a session. Session entities
                   can extend or replace custom entity types and only
                   exist during the session that they were created for.
                   All session data, including session entities, is
                   stored by Dialogflow for 20 minutes.

                   For more information, see the [session entity
                   guide](\ https://cloud.google.com/dialogflow/docs/entities-session).

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
        # in a gcd_session_entity_type.CreateSessionEntityTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, gcd_session_entity_type.CreateSessionEntityTypeRequest
        ):
            request = gcd_session_entity_type.CreateSessionEntityTypeRequest(request)
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
        request: gcd_session_entity_type.UpdateSessionEntityTypeRequest = None,
        *,
        session_entity_type: gcd_session_entity_type.SessionEntityType = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_session_entity_type.SessionEntityType:
        r"""Updates the specified session entity type.
        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (google.cloud.dialogflow_v2beta1.types.UpdateSessionEntityTypeRequest):
                The request object. The request message for
                [SessionEntityTypes.UpdateSessionEntityType][google.cloud.dialogflow.v2beta1.SessionEntityTypes.UpdateSessionEntityType].
            session_entity_type (google.cloud.dialogflow_v2beta1.types.SessionEntityType):
                Required. The session entity type to
                update.

                This corresponds to the ``session_entity_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. The mask to control which
                fields get updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2beta1.types.SessionEntityType:
                A session represents a conversation between a Dialogflow agent and an
                   end-user. You can create special entities, called
                   session entities, during a session. Session entities
                   can extend or replace custom entity types and only
                   exist during the session that they were created for.
                   All session data, including session entities, is
                   stored by Dialogflow for 20 minutes.

                   For more information, see the [session entity
                   guide](\ https://cloud.google.com/dialogflow/docs/entities-session).

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
        # in a gcd_session_entity_type.UpdateSessionEntityTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, gcd_session_entity_type.UpdateSessionEntityTypeRequest
        ):
            request = gcd_session_entity_type.UpdateSessionEntityTypeRequest(request)
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
        This method doesn't work with Google Assistant
        integration. Contact Dialogflow support if you need to
        use session entities with Google Assistant integration.

        Args:
            request (google.cloud.dialogflow_v2beta1.types.DeleteSessionEntityTypeRequest):
                The request object. The request message for
                [SessionEntityTypes.DeleteSessionEntityType][google.cloud.dialogflow.v2beta1.SessionEntityTypes.DeleteSessionEntityType].
            name (str):
                Required. The name of the entity type to delete.
                Supported formats:

                -  ``projects/<Project ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                -  ``projects/<Project ID>/locations/<Location ID>/agent/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                -  ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``
                -  ``projects/<Project ID>/locations/<Location ID>/agent/environments/ <Environment ID>/users/<User ID>/sessions/<Session ID>/entityTypes/<Entity Type Display Name>``

                If ``Location ID`` is not specified we assume default
                'us' location. If ``Environment ID`` is not specified,
                we assume default 'draft' environment. If ``User ID`` is
                not specified, we assume default '-' user.

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
            "google-cloud-dialogflow",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("SessionEntityTypesClient",)
