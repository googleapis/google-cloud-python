# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from typing import (
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

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.contact_center_insights_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.contact_center_insights_v1.services.contact_center_insights import (
    pagers,
)
from google.cloud.contact_center_insights_v1.types import (
    contact_center_insights,
    resources,
)

from .transports.base import DEFAULT_CLIENT_INFO, ContactCenterInsightsTransport
from .transports.grpc import ContactCenterInsightsGrpcTransport
from .transports.grpc_asyncio import ContactCenterInsightsGrpcAsyncIOTransport
from .transports.rest import ContactCenterInsightsRestTransport


class ContactCenterInsightsClientMeta(type):
    """Metaclass for the ContactCenterInsights client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ContactCenterInsightsTransport]]
    _transport_registry["grpc"] = ContactCenterInsightsGrpcTransport
    _transport_registry["grpc_asyncio"] = ContactCenterInsightsGrpcAsyncIOTransport
    _transport_registry["rest"] = ContactCenterInsightsRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[ContactCenterInsightsTransport]:
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


class ContactCenterInsightsClient(metaclass=ContactCenterInsightsClientMeta):
    """An API that lets users analyze and explore their business
    conversation data.
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

    DEFAULT_ENDPOINT = "contactcenterinsights.googleapis.com"
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
            ContactCenterInsightsClient: The constructed client.
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
            ContactCenterInsightsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ContactCenterInsightsTransport:
        """Returns the transport used by the client instance.

        Returns:
            ContactCenterInsightsTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def analysis_path(
        project: str,
        location: str,
        conversation: str,
        analysis: str,
    ) -> str:
        """Returns a fully-qualified analysis string."""
        return "projects/{project}/locations/{location}/conversations/{conversation}/analyses/{analysis}".format(
            project=project,
            location=location,
            conversation=conversation,
            analysis=analysis,
        )

    @staticmethod
    def parse_analysis_path(path: str) -> Dict[str, str]:
        """Parses a analysis path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/conversations/(?P<conversation>.+?)/analyses/(?P<analysis>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def conversation_path(
        project: str,
        location: str,
        conversation: str,
    ) -> str:
        """Returns a fully-qualified conversation string."""
        return "projects/{project}/locations/{location}/conversations/{conversation}".format(
            project=project,
            location=location,
            conversation=conversation,
        )

    @staticmethod
    def parse_conversation_path(path: str) -> Dict[str, str]:
        """Parses a conversation path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/conversations/(?P<conversation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def conversation_profile_path(
        project: str,
        location: str,
        conversation_profile: str,
    ) -> str:
        """Returns a fully-qualified conversation_profile string."""
        return "projects/{project}/locations/{location}/conversationProfiles/{conversation_profile}".format(
            project=project,
            location=location,
            conversation_profile=conversation_profile,
        )

    @staticmethod
    def parse_conversation_profile_path(path: str) -> Dict[str, str]:
        """Parses a conversation_profile path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/conversationProfiles/(?P<conversation_profile>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def issue_path(
        project: str,
        location: str,
        issue_model: str,
        issue: str,
    ) -> str:
        """Returns a fully-qualified issue string."""
        return "projects/{project}/locations/{location}/issueModels/{issue_model}/issues/{issue}".format(
            project=project,
            location=location,
            issue_model=issue_model,
            issue=issue,
        )

    @staticmethod
    def parse_issue_path(path: str) -> Dict[str, str]:
        """Parses a issue path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/issueModels/(?P<issue_model>.+?)/issues/(?P<issue>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def issue_model_path(
        project: str,
        location: str,
        issue_model: str,
    ) -> str:
        """Returns a fully-qualified issue_model string."""
        return (
            "projects/{project}/locations/{location}/issueModels/{issue_model}".format(
                project=project,
                location=location,
                issue_model=issue_model,
            )
        )

    @staticmethod
    def parse_issue_model_path(path: str) -> Dict[str, str]:
        """Parses a issue_model path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/issueModels/(?P<issue_model>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def participant_path(
        project: str,
        conversation: str,
        participant: str,
    ) -> str:
        """Returns a fully-qualified participant string."""
        return "projects/{project}/conversations/{conversation}/participants/{participant}".format(
            project=project,
            conversation=conversation,
            participant=participant,
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
    def phrase_matcher_path(
        project: str,
        location: str,
        phrase_matcher: str,
    ) -> str:
        """Returns a fully-qualified phrase_matcher string."""
        return "projects/{project}/locations/{location}/phraseMatchers/{phrase_matcher}".format(
            project=project,
            location=location,
            phrase_matcher=phrase_matcher,
        )

    @staticmethod
    def parse_phrase_matcher_path(path: str) -> Dict[str, str]:
        """Parses a phrase_matcher path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/phraseMatchers/(?P<phrase_matcher>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def settings_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified settings string."""
        return "projects/{project}/locations/{location}/settings".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_settings_path(path: str) -> Dict[str, str]:
        """Parses a settings path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/settings$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def view_path(
        project: str,
        location: str,
        view: str,
    ) -> str:
        """Returns a fully-qualified view string."""
        return "projects/{project}/locations/{location}/views/{view}".format(
            project=project,
            location=location,
            view=view,
        )

    @staticmethod
    def parse_view_path(path: str) -> Dict[str, str]:
        """Parses a view path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/views/(?P<view>.+?)$",
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
        """Return the API endpoint and client cert source for mutual TLS.

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

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[Union[str, ContactCenterInsightsTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the contact center insights client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ContactCenterInsightsTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
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
        client_options = cast(client_options_lib.ClientOptions, client_options)

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ContactCenterInsightsTransport):
            # transport is a ContactCenterInsightsTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
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
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

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
                api_audience=client_options.api_audience,
            )

    def create_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.CreateConversationRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        conversation: Optional[resources.Conversation] = None,
        conversation_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Conversation:
        r"""Creates a conversation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_create_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CreateConversationRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_conversation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.CreateConversationRequest, dict]):
                The request object. Request to create a conversation.
            parent (str):
                Required. The parent resource of the
                conversation.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            conversation (google.cloud.contact_center_insights_v1.types.Conversation):
                Required. The conversation resource
                to create.

                This corresponds to the ``conversation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            conversation_id (str):
                A unique ID for the new conversation. This ID will
                become the final component of the conversation's
                resource name. If no ID is specified, a server-generated
                ID will be used.

                This value should be 4-64 characters and must match the
                regular expression ``^[a-z0-9-]{4,64}$``. Valid
                characters are ``[a-z][0-9]-``

                This corresponds to the ``conversation_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Conversation:
                The conversation resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, conversation, conversation_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.CreateConversationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.CreateConversationRequest):
            request = contact_center_insights.CreateConversationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if conversation is not None:
                request.conversation = conversation
            if conversation_id is not None:
                request.conversation_id = conversation_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_conversation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def upload_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.UploadConversationRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Create a longrunning conversation upload operation.
        This method differs from CreateConversation by allowing
        audio transcription and optional DLP redaction.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_upload_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UploadConversationRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.upload_conversation(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.UploadConversationRequest, dict]):
                The request object. Request to upload a conversation.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.contact_center_insights_v1.types.Conversation`
                The conversation resource.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.UploadConversationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.UploadConversationRequest):
            request = contact_center_insights.UploadConversationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.upload_conversation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resources.Conversation,
            metadata_type=contact_center_insights.UploadConversationMetadata,
        )

        # Done; return the response.
        return response

    def update_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateConversationRequest, dict]
        ] = None,
        *,
        conversation: Optional[resources.Conversation] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Conversation:
        r"""Updates a conversation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_update_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateConversationRequest(
                )

                # Make the request
                response = client.update_conversation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.UpdateConversationRequest, dict]):
                The request object. The request to update a conversation.
            conversation (google.cloud.contact_center_insights_v1.types.Conversation):
                Required. The new values for the
                conversation.

                This corresponds to the ``conversation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Conversation:
                The conversation resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([conversation, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.UpdateConversationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.UpdateConversationRequest):
            request = contact_center_insights.UpdateConversationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if conversation is not None:
                request.conversation = conversation
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_conversation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("conversation.name", request.conversation.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.GetConversationRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Conversation:
        r"""Gets a conversation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_get_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetConversationRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_conversation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.GetConversationRequest, dict]):
                The request object. The request to get a conversation.
            name (str):
                Required. The name of the
                conversation to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Conversation:
                The conversation resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.GetConversationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.GetConversationRequest):
            request = contact_center_insights.GetConversationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_conversation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_conversations(
        self,
        request: Optional[
            Union[contact_center_insights.ListConversationsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListConversationsPager:
        r"""Lists conversations.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_list_conversations():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListConversationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_conversations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.ListConversationsRequest, dict]):
                The request object. Request to list conversations.
            parent (str):
                Required. The parent resource of the
                conversation.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.services.contact_center_insights.pagers.ListConversationsPager:
                The response of listing
                conversations.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.ListConversationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.ListConversationsRequest):
            request = contact_center_insights.ListConversationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_conversations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListConversationsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_conversation(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteConversationRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a conversation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_delete_conversation():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteConversationRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_conversation(request=request)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.DeleteConversationRequest, dict]):
                The request object. The request to delete a conversation.
            name (str):
                Required. The name of the
                conversation to delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.DeleteConversationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.DeleteConversationRequest):
            request = contact_center_insights.DeleteConversationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_conversation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def create_analysis(
        self,
        request: Optional[
            Union[contact_center_insights.CreateAnalysisRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        analysis: Optional[resources.Analysis] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates an analysis. The long running operation is
        done when the analysis has completed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_create_analysis():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CreateAnalysisRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_analysis(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.CreateAnalysisRequest, dict]):
                The request object. The request to create an analysis.
            parent (str):
                Required. The parent resource of the
                analysis.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            analysis (google.cloud.contact_center_insights_v1.types.Analysis):
                Required. The analysis to create.
                This corresponds to the ``analysis`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.contact_center_insights_v1.types.Analysis`
                The analysis resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, analysis])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.CreateAnalysisRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.CreateAnalysisRequest):
            request = contact_center_insights.CreateAnalysisRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if analysis is not None:
                request.analysis = analysis

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_analysis]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resources.Analysis,
            metadata_type=contact_center_insights.CreateAnalysisOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_analysis(
        self,
        request: Optional[
            Union[contact_center_insights.GetAnalysisRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Analysis:
        r"""Gets an analysis.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_get_analysis():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetAnalysisRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_analysis(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.GetAnalysisRequest, dict]):
                The request object. The request to get an analysis.
            name (str):
                Required. The name of the analysis to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Analysis:
                The analysis resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.GetAnalysisRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.GetAnalysisRequest):
            request = contact_center_insights.GetAnalysisRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_analysis]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_analyses(
        self,
        request: Optional[
            Union[contact_center_insights.ListAnalysesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAnalysesPager:
        r"""Lists analyses.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_list_analyses():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListAnalysesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_analyses(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.ListAnalysesRequest, dict]):
                The request object. The request to list analyses.
            parent (str):
                Required. The parent resource of the
                analyses.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.services.contact_center_insights.pagers.ListAnalysesPager:
                The response to list analyses.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.ListAnalysesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.ListAnalysesRequest):
            request = contact_center_insights.ListAnalysesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_analyses]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAnalysesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_analysis(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteAnalysisRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an analysis.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_delete_analysis():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteAnalysisRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_analysis(request=request)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.DeleteAnalysisRequest, dict]):
                The request object. The request to delete an analysis.
            name (str):
                Required. The name of the analysis to
                delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.DeleteAnalysisRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.DeleteAnalysisRequest):
            request = contact_center_insights.DeleteAnalysisRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_analysis]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def bulk_analyze_conversations(
        self,
        request: Optional[
            Union[contact_center_insights.BulkAnalyzeConversationsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        filter: Optional[str] = None,
        analysis_percentage: Optional[float] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Analyzes multiple conversations in a single request.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_bulk_analyze_conversations():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.BulkAnalyzeConversationsRequest(
                    parent="parent_value",
                    filter="filter_value",
                    analysis_percentage=0.20170000000000002,
                )

                # Make the request
                operation = client.bulk_analyze_conversations(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.BulkAnalyzeConversationsRequest, dict]):
                The request object. The request to analyze conversations
                in bulk.
            parent (str):
                Required. The parent resource to
                create analyses in.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Required. Filter used to select the
                subset of conversations to analyze.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            analysis_percentage (float):
                Required. Percentage of selected conversation to
                analyze, between [0, 100].

                This corresponds to the ``analysis_percentage`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.contact_center_insights_v1.types.BulkAnalyzeConversationsResponse`
                The response for a bulk analyze conversations operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter, analysis_percentage])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.BulkAnalyzeConversationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, contact_center_insights.BulkAnalyzeConversationsRequest
        ):
            request = contact_center_insights.BulkAnalyzeConversationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter
            if analysis_percentage is not None:
                request.analysis_percentage = analysis_percentage

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.bulk_analyze_conversations
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            contact_center_insights.BulkAnalyzeConversationsResponse,
            metadata_type=contact_center_insights.BulkAnalyzeConversationsMetadata,
        )

        # Done; return the response.
        return response

    def ingest_conversations(
        self,
        request: Optional[
            Union[contact_center_insights.IngestConversationsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Imports conversations and processes them according to
        the user's configuration.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_ingest_conversations():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                gcs_source = contact_center_insights_v1.GcsSource()
                gcs_source.bucket_uri = "bucket_uri_value"

                transcript_object_config = contact_center_insights_v1.TranscriptObjectConfig()
                transcript_object_config.medium = "CHAT"

                request = contact_center_insights_v1.IngestConversationsRequest(
                    gcs_source=gcs_source,
                    transcript_object_config=transcript_object_config,
                    parent="parent_value",
                )

                # Make the request
                operation = client.ingest_conversations(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.IngestConversationsRequest, dict]):
                The request object. The request to ingest conversations.
            parent (str):
                Required. The parent resource for new
                conversations.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.contact_center_insights_v1.types.IngestConversationsResponse`
                The response to an IngestConversations operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.IngestConversationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.IngestConversationsRequest):
            request = contact_center_insights.IngestConversationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.ingest_conversations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            contact_center_insights.IngestConversationsResponse,
            metadata_type=contact_center_insights.IngestConversationsMetadata,
        )

        # Done; return the response.
        return response

    def export_insights_data(
        self,
        request: Optional[
            Union[contact_center_insights.ExportInsightsDataRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Export insights data to a destination defined in the
        request body.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_export_insights_data():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                big_query_destination = contact_center_insights_v1.BigQueryDestination()
                big_query_destination.dataset = "dataset_value"

                request = contact_center_insights_v1.ExportInsightsDataRequest(
                    big_query_destination=big_query_destination,
                    parent="parent_value",
                )

                # Make the request
                operation = client.export_insights_data(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.ExportInsightsDataRequest, dict]):
                The request object. The request to export insights.
            parent (str):
                Required. The parent resource to
                export data from.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.contact_center_insights_v1.types.ExportInsightsDataResponse`
                Response for an export insights operation.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.ExportInsightsDataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.ExportInsightsDataRequest):
            request = contact_center_insights.ExportInsightsDataRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.export_insights_data]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            contact_center_insights.ExportInsightsDataResponse,
            metadata_type=contact_center_insights.ExportInsightsDataMetadata,
        )

        # Done; return the response.
        return response

    def create_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.CreateIssueModelRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        issue_model: Optional[resources.IssueModel] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates an issue model.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_create_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CreateIssueModelRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_issue_model(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.CreateIssueModelRequest, dict]):
                The request object. The request to create an issue model.
            parent (str):
                Required. The parent resource of the
                issue model.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            issue_model (google.cloud.contact_center_insights_v1.types.IssueModel):
                Required. The issue model to create.
                This corresponds to the ``issue_model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.contact_center_insights_v1.types.IssueModel`
                The issue model resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, issue_model])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.CreateIssueModelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.CreateIssueModelRequest):
            request = contact_center_insights.CreateIssueModelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if issue_model is not None:
                request.issue_model = issue_model

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_issue_model]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resources.IssueModel,
            metadata_type=contact_center_insights.CreateIssueModelMetadata,
        )

        # Done; return the response.
        return response

    def update_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateIssueModelRequest, dict]
        ] = None,
        *,
        issue_model: Optional[resources.IssueModel] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.IssueModel:
        r"""Updates an issue model.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_update_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateIssueModelRequest(
                )

                # Make the request
                response = client.update_issue_model(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.UpdateIssueModelRequest, dict]):
                The request object. The request to update an issue model.
            issue_model (google.cloud.contact_center_insights_v1.types.IssueModel):
                Required. The new values for the
                issue model.

                This corresponds to the ``issue_model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.IssueModel:
                The issue model resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([issue_model, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.UpdateIssueModelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.UpdateIssueModelRequest):
            request = contact_center_insights.UpdateIssueModelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if issue_model is not None:
                request.issue_model = issue_model
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_issue_model]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("issue_model.name", request.issue_model.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.GetIssueModelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.IssueModel:
        r"""Gets an issue model.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_get_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetIssueModelRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_issue_model(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.GetIssueModelRequest, dict]):
                The request object. The request to get an issue model.
            name (str):
                Required. The name of the issue model
                to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.IssueModel:
                The issue model resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.GetIssueModelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.GetIssueModelRequest):
            request = contact_center_insights.GetIssueModelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_issue_model]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_issue_models(
        self,
        request: Optional[
            Union[contact_center_insights.ListIssueModelsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> contact_center_insights.ListIssueModelsResponse:
        r"""Lists issue models.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_list_issue_models():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListIssueModelsRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.list_issue_models(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.ListIssueModelsRequest, dict]):
                The request object. Request to list issue models.
            parent (str):
                Required. The parent resource of the
                issue model.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.ListIssueModelsResponse:
                The response of listing issue models.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.ListIssueModelsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.ListIssueModelsRequest):
            request = contact_center_insights.ListIssueModelsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_issue_models]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteIssueModelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes an issue model.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_delete_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteIssueModelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_issue_model(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.DeleteIssueModelRequest, dict]):
                The request object. The request to delete an issue model.
            name (str):
                Required. The name of the issue model
                to delete.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.DeleteIssueModelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.DeleteIssueModelRequest):
            request = contact_center_insights.DeleteIssueModelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_issue_model]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=contact_center_insights.DeleteIssueModelMetadata,
        )

        # Done; return the response.
        return response

    def deploy_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.DeployIssueModelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deploys an issue model. Returns an error if a model
        is already deployed. An issue model can only be used in
        analysis after it has been deployed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_deploy_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeployIssueModelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.deploy_issue_model(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.DeployIssueModelRequest, dict]):
                The request object. The request to deploy an issue model.
            name (str):
                Required. The issue model to deploy.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.contact_center_insights_v1.types.DeployIssueModelResponse`
                The response to deploy an issue model.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.DeployIssueModelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.DeployIssueModelRequest):
            request = contact_center_insights.DeployIssueModelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.deploy_issue_model]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            contact_center_insights.DeployIssueModelResponse,
            metadata_type=contact_center_insights.DeployIssueModelMetadata,
        )

        # Done; return the response.
        return response

    def undeploy_issue_model(
        self,
        request: Optional[
            Union[contact_center_insights.UndeployIssueModelRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Undeploys an issue model.
        An issue model can not be used in analysis after it has
        been undeployed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_undeploy_issue_model():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UndeployIssueModelRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undeploy_issue_model(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.UndeployIssueModelRequest, dict]):
                The request object. The request to undeploy an issue
                model.
            name (str):
                Required. The issue model to
                undeploy.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.contact_center_insights_v1.types.UndeployIssueModelResponse`
                The response to undeploy an issue model.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.UndeployIssueModelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.UndeployIssueModelRequest):
            request = contact_center_insights.UndeployIssueModelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.undeploy_issue_model]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            contact_center_insights.UndeployIssueModelResponse,
            metadata_type=contact_center_insights.UndeployIssueModelMetadata,
        )

        # Done; return the response.
        return response

    def get_issue(
        self,
        request: Optional[Union[contact_center_insights.GetIssueRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Issue:
        r"""Gets an issue.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_get_issue():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetIssueRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_issue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.GetIssueRequest, dict]):
                The request object. The request to get an issue.
            name (str):
                Required. The name of the issue to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Issue:
                The issue resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.GetIssueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.GetIssueRequest):
            request = contact_center_insights.GetIssueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_issue]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_issues(
        self,
        request: Optional[
            Union[contact_center_insights.ListIssuesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> contact_center_insights.ListIssuesResponse:
        r"""Lists issues.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_list_issues():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListIssuesRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.list_issues(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.ListIssuesRequest, dict]):
                The request object. Request to list issues.
            parent (str):
                Required. The parent resource of the
                issue.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.ListIssuesResponse:
                The response of listing issues.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.ListIssuesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.ListIssuesRequest):
            request = contact_center_insights.ListIssuesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_issues]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_issue(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateIssueRequest, dict]
        ] = None,
        *,
        issue: Optional[resources.Issue] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Issue:
        r"""Updates an issue.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_update_issue():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateIssueRequest(
                )

                # Make the request
                response = client.update_issue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.UpdateIssueRequest, dict]):
                The request object. The request to update an issue.
            issue (google.cloud.contact_center_insights_v1.types.Issue):
                Required. The new values for the
                issue.

                This corresponds to the ``issue`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Issue:
                The issue resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([issue, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.UpdateIssueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.UpdateIssueRequest):
            request = contact_center_insights.UpdateIssueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if issue is not None:
                request.issue = issue
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_issue]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("issue.name", request.issue.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_issue(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteIssueRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an issue.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_delete_issue():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteIssueRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_issue(request=request)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.DeleteIssueRequest, dict]):
                The request object. The request to delete an issue.
            name (str):
                Required. The name of the issue to
                delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.DeleteIssueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.DeleteIssueRequest):
            request = contact_center_insights.DeleteIssueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_issue]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def calculate_issue_model_stats(
        self,
        request: Optional[
            Union[contact_center_insights.CalculateIssueModelStatsRequest, dict]
        ] = None,
        *,
        issue_model: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> contact_center_insights.CalculateIssueModelStatsResponse:
        r"""Gets an issue model's statistics.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_calculate_issue_model_stats():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CalculateIssueModelStatsRequest(
                    issue_model="issue_model_value",
                )

                # Make the request
                response = client.calculate_issue_model_stats(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.CalculateIssueModelStatsRequest, dict]):
                The request object. Request to get statistics of an issue
                model.
            issue_model (str):
                Required. The resource name of the
                issue model to query against.

                This corresponds to the ``issue_model`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.CalculateIssueModelStatsResponse:
                Response of querying an issue model's
                statistics.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([issue_model])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.CalculateIssueModelStatsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, contact_center_insights.CalculateIssueModelStatsRequest
        ):
            request = contact_center_insights.CalculateIssueModelStatsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if issue_model is not None:
                request.issue_model = issue_model

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.calculate_issue_model_stats
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("issue_model", request.issue_model),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_phrase_matcher(
        self,
        request: Optional[
            Union[contact_center_insights.CreatePhraseMatcherRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        phrase_matcher: Optional[resources.PhraseMatcher] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.PhraseMatcher:
        r"""Creates a phrase matcher.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_create_phrase_matcher():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                phrase_matcher = contact_center_insights_v1.PhraseMatcher()
                phrase_matcher.type_ = "ANY_OF"

                request = contact_center_insights_v1.CreatePhraseMatcherRequest(
                    parent="parent_value",
                    phrase_matcher=phrase_matcher,
                )

                # Make the request
                response = client.create_phrase_matcher(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.CreatePhraseMatcherRequest, dict]):
                The request object. Request to create a phrase matcher.
            parent (str):
                Required. The parent resource of the phrase matcher.
                Required. The location to create a phrase matcher for.
                Format:
                ``projects/<Project ID>/locations/<Location ID>`` or
                ``projects/<Project Number>/locations/<Location ID>``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            phrase_matcher (google.cloud.contact_center_insights_v1.types.PhraseMatcher):
                Required. The phrase matcher resource
                to create.

                This corresponds to the ``phrase_matcher`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.PhraseMatcher:
                The phrase matcher resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, phrase_matcher])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.CreatePhraseMatcherRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.CreatePhraseMatcherRequest):
            request = contact_center_insights.CreatePhraseMatcherRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if phrase_matcher is not None:
                request.phrase_matcher = phrase_matcher

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_phrase_matcher]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_phrase_matcher(
        self,
        request: Optional[
            Union[contact_center_insights.GetPhraseMatcherRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.PhraseMatcher:
        r"""Gets a phrase matcher.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_get_phrase_matcher():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetPhraseMatcherRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_phrase_matcher(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.GetPhraseMatcherRequest, dict]):
                The request object. The request to get a a phrase
                matcher.
            name (str):
                Required. The name of the phrase
                matcher to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.PhraseMatcher:
                The phrase matcher resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.GetPhraseMatcherRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.GetPhraseMatcherRequest):
            request = contact_center_insights.GetPhraseMatcherRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_phrase_matcher]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_phrase_matchers(
        self,
        request: Optional[
            Union[contact_center_insights.ListPhraseMatchersRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListPhraseMatchersPager:
        r"""Lists phrase matchers.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_list_phrase_matchers():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListPhraseMatchersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_phrase_matchers(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.ListPhraseMatchersRequest, dict]):
                The request object. Request to list phrase matchers.
            parent (str):
                Required. The parent resource of the
                phrase matcher.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.services.contact_center_insights.pagers.ListPhraseMatchersPager:
                The response of listing phrase
                matchers.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.ListPhraseMatchersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.ListPhraseMatchersRequest):
            request = contact_center_insights.ListPhraseMatchersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_phrase_matchers]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListPhraseMatchersPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_phrase_matcher(
        self,
        request: Optional[
            Union[contact_center_insights.DeletePhraseMatcherRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a phrase matcher.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_delete_phrase_matcher():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeletePhraseMatcherRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_phrase_matcher(request=request)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.DeletePhraseMatcherRequest, dict]):
                The request object. The request to delete a phrase
                matcher.
            name (str):
                Required. The name of the phrase
                matcher to delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.DeletePhraseMatcherRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.DeletePhraseMatcherRequest):
            request = contact_center_insights.DeletePhraseMatcherRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_phrase_matcher]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def update_phrase_matcher(
        self,
        request: Optional[
            Union[contact_center_insights.UpdatePhraseMatcherRequest, dict]
        ] = None,
        *,
        phrase_matcher: Optional[resources.PhraseMatcher] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.PhraseMatcher:
        r"""Updates a phrase matcher.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_update_phrase_matcher():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                phrase_matcher = contact_center_insights_v1.PhraseMatcher()
                phrase_matcher.type_ = "ANY_OF"

                request = contact_center_insights_v1.UpdatePhraseMatcherRequest(
                    phrase_matcher=phrase_matcher,
                )

                # Make the request
                response = client.update_phrase_matcher(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.UpdatePhraseMatcherRequest, dict]):
                The request object. The request to update a phrase
                matcher.
            phrase_matcher (google.cloud.contact_center_insights_v1.types.PhraseMatcher):
                Required. The new values for the
                phrase matcher.

                This corresponds to the ``phrase_matcher`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.PhraseMatcher:
                The phrase matcher resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([phrase_matcher, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.UpdatePhraseMatcherRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.UpdatePhraseMatcherRequest):
            request = contact_center_insights.UpdatePhraseMatcherRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if phrase_matcher is not None:
                request.phrase_matcher = phrase_matcher
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_phrase_matcher]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("phrase_matcher.name", request.phrase_matcher.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def calculate_stats(
        self,
        request: Optional[
            Union[contact_center_insights.CalculateStatsRequest, dict]
        ] = None,
        *,
        location: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> contact_center_insights.CalculateStatsResponse:
        r"""Gets conversation statistics.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_calculate_stats():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CalculateStatsRequest(
                    location="location_value",
                )

                # Make the request
                response = client.calculate_stats(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.CalculateStatsRequest, dict]):
                The request object. The request for calculating
                conversation statistics.
            location (str):
                Required. The location of the
                conversations.

                This corresponds to the ``location`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.CalculateStatsResponse:
                The response for calculating
                conversation statistics.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([location])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.CalculateStatsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.CalculateStatsRequest):
            request = contact_center_insights.CalculateStatsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if location is not None:
                request.location = location

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.calculate_stats]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("location", request.location),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_settings(
        self,
        request: Optional[
            Union[contact_center_insights.GetSettingsRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Settings:
        r"""Gets project-level settings.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_get_settings():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetSettingsRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.GetSettingsRequest, dict]):
                The request object. The request to get project-level
                settings.
            name (str):
                Required. The name of the settings
                resource to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.Settings:
                The settings resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.GetSettingsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.GetSettingsRequest):
            request = contact_center_insights.GetSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_settings]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_settings(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateSettingsRequest, dict]
        ] = None,
        *,
        settings: Optional[resources.Settings] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Settings:
        r"""Updates project-level settings.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_update_settings():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateSettingsRequest(
                )

                # Make the request
                response = client.update_settings(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.UpdateSettingsRequest, dict]):
                The request object. The request to update project-level
                settings.
            settings (google.cloud.contact_center_insights_v1.types.Settings):
                Required. The new settings values.
                This corresponds to the ``settings`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The list of fields to be
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
            google.cloud.contact_center_insights_v1.types.Settings:
                The settings resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([settings, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.UpdateSettingsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.UpdateSettingsRequest):
            request = contact_center_insights.UpdateSettingsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if settings is not None:
                request.settings = settings
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_settings]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("settings.name", request.settings.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_view(
        self,
        request: Optional[
            Union[contact_center_insights.CreateViewRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        view: Optional[resources.View] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.View:
        r"""Creates a view.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_create_view():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.CreateViewRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_view(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.CreateViewRequest, dict]):
                The request object. The request to create a view.
            parent (str):
                Required. The parent resource of the view. Required. The
                location to create a view for. Format:
                ``projects/<Project ID>/locations/<Location ID>`` or
                ``projects/<Project Number>/locations/<Location ID>``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            view (google.cloud.contact_center_insights_v1.types.View):
                Required. The view resource to
                create.

                This corresponds to the ``view`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.View:
                The View resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, view])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.CreateViewRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.CreateViewRequest):
            request = contact_center_insights.CreateViewRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if view is not None:
                request.view = view

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_view]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_view(
        self,
        request: Optional[Union[contact_center_insights.GetViewRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.View:
        r"""Gets a view.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_get_view():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.GetViewRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_view(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.GetViewRequest, dict]):
                The request object. The request to get a view.
            name (str):
                Required. The name of the view to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.View:
                The View resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.GetViewRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.GetViewRequest):
            request = contact_center_insights.GetViewRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_view]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_views(
        self,
        request: Optional[Union[contact_center_insights.ListViewsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListViewsPager:
        r"""Lists views.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_list_views():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.ListViewsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_views(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.ListViewsRequest, dict]):
                The request object. The request to list views.
            parent (str):
                Required. The parent resource of the
                views.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.services.contact_center_insights.pagers.ListViewsPager:
                The response of listing views.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.ListViewsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.ListViewsRequest):
            request = contact_center_insights.ListViewsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_views]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListViewsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_view(
        self,
        request: Optional[
            Union[contact_center_insights.UpdateViewRequest, dict]
        ] = None,
        *,
        view: Optional[resources.View] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.View:
        r"""Updates a view.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_update_view():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.UpdateViewRequest(
                )

                # Make the request
                response = client.update_view(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.UpdateViewRequest, dict]):
                The request object. The request to update a view.
            view (google.cloud.contact_center_insights_v1.types.View):
                Required. The new view.
                This corresponds to the ``view`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.contact_center_insights_v1.types.View:
                The View resource.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([view, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.UpdateViewRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.UpdateViewRequest):
            request = contact_center_insights.UpdateViewRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if view is not None:
                request.view = view
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_view]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("view.name", request.view.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_view(
        self,
        request: Optional[
            Union[contact_center_insights.DeleteViewRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a view.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import contact_center_insights_v1

            def sample_delete_view():
                # Create a client
                client = contact_center_insights_v1.ContactCenterInsightsClient()

                # Initialize request argument(s)
                request = contact_center_insights_v1.DeleteViewRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_view(request=request)

        Args:
            request (Union[google.cloud.contact_center_insights_v1.types.DeleteViewRequest, dict]):
                The request object. The request to delete a view.
            name (str):
                Required. The name of the view to
                delete.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a contact_center_insights.DeleteViewRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, contact_center_insights.DeleteViewRequest):
            request = contact_center_insights.DeleteViewRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_view]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def __enter__(self) -> "ContactCenterInsightsClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_operations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.cancel_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ContactCenterInsightsClient",)
