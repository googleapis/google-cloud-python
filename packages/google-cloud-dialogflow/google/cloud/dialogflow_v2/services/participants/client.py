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

from google.cloud.dialogflow_v2.services.participants import pagers
from google.cloud.dialogflow_v2.types import participant
from google.cloud.dialogflow_v2.types import participant as gcd_participant
from google.cloud.dialogflow_v2.types import session
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import ParticipantsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import ParticipantsGrpcTransport
from .transports.grpc_asyncio import ParticipantsGrpcAsyncIOTransport


class ParticipantsClientMeta(type):
    """Metaclass for the Participants client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[ParticipantsTransport]]
    _transport_registry["grpc"] = ParticipantsGrpcTransport
    _transport_registry["grpc_asyncio"] = ParticipantsGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[ParticipantsTransport]:
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


class ParticipantsClient(metaclass=ParticipantsClientMeta):
    """Service for managing
    [Participants][google.cloud.dialogflow.v2.Participant].
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
            ParticipantsClient: The constructed client.
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
            ParticipantsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ParticipantsTransport:
        """Returns the transport used by the client instance.

        Returns:
            ParticipantsTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def context_path(project: str, session: str, context: str,) -> str:
        """Returns a fully-qualified context string."""
        return "projects/{project}/agent/sessions/{session}/contexts/{context}".format(
            project=project, session=session, context=context,
        )

    @staticmethod
    def parse_context_path(path: str) -> Dict[str, str]:
        """Parses a context path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/agent/sessions/(?P<session>.+?)/contexts/(?P<context>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def intent_path(project: str, intent: str,) -> str:
        """Returns a fully-qualified intent string."""
        return "projects/{project}/agent/intents/{intent}".format(
            project=project, intent=intent,
        )

    @staticmethod
    def parse_intent_path(path: str) -> Dict[str, str]:
        """Parses a intent path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/agent/intents/(?P<intent>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def message_path(project: str, conversation: str, message: str,) -> str:
        """Returns a fully-qualified message string."""
        return "projects/{project}/conversations/{conversation}/messages/{message}".format(
            project=project, conversation=conversation, message=message,
        )

    @staticmethod
    def parse_message_path(path: str) -> Dict[str, str]:
        """Parses a message path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/conversations/(?P<conversation>.+?)/messages/(?P<message>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def participant_path(project: str, conversation: str, participant: str,) -> str:
        """Returns a fully-qualified participant string."""
        return "projects/{project}/conversations/{conversation}/participants/{participant}".format(
            project=project, conversation=conversation, participant=participant,
        )

    @staticmethod
    def parse_participant_path(path: str) -> Dict[str, str]:
        """Parses a participant path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/conversations/(?P<conversation>.+?)/participants/(?P<participant>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

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
        transport: Union[str, ParticipantsTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the participants client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ParticipantsTransport]): The
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
        if isinstance(transport, ParticipantsTransport):
            # transport is a ParticipantsTransport instance.
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
            )

    def create_participant(
        self,
        request: gcd_participant.CreateParticipantRequest = None,
        *,
        parent: str = None,
        participant: gcd_participant.Participant = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_participant.Participant:
        r"""Creates a new participant in a conversation.

        Args:
            request (google.cloud.dialogflow_v2.types.CreateParticipantRequest):
                The request object. The request message for
                [Participants.CreateParticipant][google.cloud.dialogflow.v2.Participants.CreateParticipant].
            parent (str):
                Required. Resource identifier of the conversation adding
                the participant. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            participant (google.cloud.dialogflow_v2.types.Participant):
                Required. The participant to create.
                This corresponds to the ``participant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Participant:
                Represents a conversation participant
                (human agent, virtual agent, end-user).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, participant])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcd_participant.CreateParticipantRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gcd_participant.CreateParticipantRequest):
            request = gcd_participant.CreateParticipantRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if participant is not None:
                request.participant = participant

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_participant]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_participant(
        self,
        request: participant.GetParticipantRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> participant.Participant:
        r"""Retrieves a conversation participant.

        Args:
            request (google.cloud.dialogflow_v2.types.GetParticipantRequest):
                The request object. The request message for
                [Participants.GetParticipant][google.cloud.dialogflow.v2.Participants.GetParticipant].
            name (str):
                Required. The name of the participant. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Participant:
                Represents a conversation participant
                (human agent, virtual agent, end-user).

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
        # in a participant.GetParticipantRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, participant.GetParticipantRequest):
            request = participant.GetParticipantRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_participant]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_participants(
        self,
        request: participant.ListParticipantsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListParticipantsPager:
        r"""Returns the list of all participants in the specified
        conversation.

        Args:
            request (google.cloud.dialogflow_v2.types.ListParticipantsRequest):
                The request object. The request message for
                [Participants.ListParticipants][google.cloud.dialogflow.v2.Participants.ListParticipants].
            parent (str):
                Required. The conversation to list all participants
                from. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.services.participants.pagers.ListParticipantsPager:
                The response message for
                [Participants.ListParticipants][google.cloud.dialogflow.v2.Participants.ListParticipants].

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
        # in a participant.ListParticipantsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, participant.ListParticipantsRequest):
            request = participant.ListParticipantsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_participants]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListParticipantsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_participant(
        self,
        request: gcd_participant.UpdateParticipantRequest = None,
        *,
        participant: gcd_participant.Participant = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_participant.Participant:
        r"""Updates the specified participant.

        Args:
            request (google.cloud.dialogflow_v2.types.UpdateParticipantRequest):
                The request object. The request message for
                [Participants.UpdateParticipant][google.cloud.dialogflow.v2.Participants.UpdateParticipant].
            participant (google.cloud.dialogflow_v2.types.Participant):
                Required. The participant to update.
                This corresponds to the ``participant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The mask to specify which
                fields to update.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.Participant:
                Represents a conversation participant
                (human agent, virtual agent, end-user).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([participant, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcd_participant.UpdateParticipantRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gcd_participant.UpdateParticipantRequest):
            request = gcd_participant.UpdateParticipantRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if participant is not None:
                request.participant = participant
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_participant]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("participant.name", request.participant.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def analyze_content(
        self,
        request: gcd_participant.AnalyzeContentRequest = None,
        *,
        participant: str = None,
        text_input: session.TextInput = None,
        event_input: session.EventInput = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_participant.AnalyzeContentResponse:
        r"""Adds a text (chat, for example), or audio (phone recording, for
        example) message from a participant into the conversation.

        Note: Always use agent versions for production traffic sent to
        virtual agents. See `Versions and
        environments <https://cloud.google.com/dialogflow/es/docs/agents-versions>`__.

        Args:
            request (google.cloud.dialogflow_v2.types.AnalyzeContentRequest):
                The request object. The request message for
                [Participants.AnalyzeContent][google.cloud.dialogflow.v2.Participants.AnalyzeContent].
            participant (str):
                Required. The name of the participant this text comes
                from. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.

                This corresponds to the ``participant`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            text_input (google.cloud.dialogflow_v2.types.TextInput):
                The natural language text to be
                processed.

                This corresponds to the ``text_input`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            event_input (google.cloud.dialogflow_v2.types.EventInput):
                An input event to send to Dialogflow.
                This corresponds to the ``event_input`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.AnalyzeContentResponse:
                The response message for
                [Participants.AnalyzeContent][google.cloud.dialogflow.v2.Participants.AnalyzeContent].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([participant, text_input, event_input])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcd_participant.AnalyzeContentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gcd_participant.AnalyzeContentRequest):
            request = gcd_participant.AnalyzeContentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if participant is not None:
                request.participant = participant
            if text_input is not None:
                request.text_input = text_input
            if event_input is not None:
                request.event_input = event_input

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.analyze_content]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("participant", request.participant),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def suggest_articles(
        self,
        request: participant.SuggestArticlesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> participant.SuggestArticlesResponse:
        r"""Gets suggested articles for a participant based on
        specific historical messages.

        Args:
            request (google.cloud.dialogflow_v2.types.SuggestArticlesRequest):
                The request object. The request message for
                [Participants.SuggestArticles][google.cloud.dialogflow.v2.Participants.SuggestArticles].
            parent (str):
                Required. The name of the participant to fetch
                suggestion for. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.SuggestArticlesResponse:
                The response message for
                [Participants.SuggestArticles][google.cloud.dialogflow.v2.Participants.SuggestArticles].

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
        # in a participant.SuggestArticlesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, participant.SuggestArticlesRequest):
            request = participant.SuggestArticlesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.suggest_articles]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def suggest_faq_answers(
        self,
        request: participant.SuggestFaqAnswersRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> participant.SuggestFaqAnswersResponse:
        r"""Gets suggested faq answers for a participant based on
        specific historical messages.

        Args:
            request (google.cloud.dialogflow_v2.types.SuggestFaqAnswersRequest):
                The request object. The request message for
                [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2.Participants.SuggestFaqAnswers].
            parent (str):
                Required. The name of the participant to fetch
                suggestion for. Format:
                ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflow_v2.types.SuggestFaqAnswersResponse:
                The request message for
                [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2.Participants.SuggestFaqAnswers].

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
        # in a participant.SuggestFaqAnswersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, participant.SuggestFaqAnswersRequest):
            request = participant.SuggestFaqAnswersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.suggest_faq_answers]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

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


__all__ = ("ParticipantsClient",)
