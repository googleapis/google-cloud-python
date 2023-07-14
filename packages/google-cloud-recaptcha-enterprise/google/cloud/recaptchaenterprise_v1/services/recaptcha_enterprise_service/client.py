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

from google.cloud.recaptchaenterprise_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service import (
    pagers,
)
from google.cloud.recaptchaenterprise_v1.types import recaptchaenterprise

from .transports.base import DEFAULT_CLIENT_INFO, RecaptchaEnterpriseServiceTransport
from .transports.grpc import RecaptchaEnterpriseServiceGrpcTransport
from .transports.grpc_asyncio import RecaptchaEnterpriseServiceGrpcAsyncIOTransport


class RecaptchaEnterpriseServiceClientMeta(type):
    """Metaclass for the RecaptchaEnterpriseService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[RecaptchaEnterpriseServiceTransport]]
    _transport_registry["grpc"] = RecaptchaEnterpriseServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = RecaptchaEnterpriseServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[RecaptchaEnterpriseServiceTransport]:
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


class RecaptchaEnterpriseServiceClient(metaclass=RecaptchaEnterpriseServiceClientMeta):
    """Service to determine the likelihood an event is legitimate."""

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

    DEFAULT_ENDPOINT = "recaptchaenterprise.googleapis.com"
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
            RecaptchaEnterpriseServiceClient: The constructed client.
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
            RecaptchaEnterpriseServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> RecaptchaEnterpriseServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            RecaptchaEnterpriseServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def assessment_path(
        project: str,
        assessment: str,
    ) -> str:
        """Returns a fully-qualified assessment string."""
        return "projects/{project}/assessments/{assessment}".format(
            project=project,
            assessment=assessment,
        )

    @staticmethod
    def parse_assessment_path(path: str) -> Dict[str, str]:
        """Parses a assessment path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/assessments/(?P<assessment>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def key_path(
        project: str,
        key: str,
    ) -> str:
        """Returns a fully-qualified key string."""
        return "projects/{project}/keys/{key}".format(
            project=project,
            key=key,
        )

    @staticmethod
    def parse_key_path(path: str) -> Dict[str, str]:
        """Parses a key path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/keys/(?P<key>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def metrics_path(
        project: str,
        key: str,
    ) -> str:
        """Returns a fully-qualified metrics string."""
        return "projects/{project}/keys/{key}/metrics".format(
            project=project,
            key=key,
        )

    @staticmethod
    def parse_metrics_path(path: str) -> Dict[str, str]:
        """Parses a metrics path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/keys/(?P<key>.+?)/metrics$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def related_account_group_path(
        project: str,
        relatedaccountgroup: str,
    ) -> str:
        """Returns a fully-qualified related_account_group string."""
        return "projects/{project}/relatedaccountgroups/{relatedaccountgroup}".format(
            project=project,
            relatedaccountgroup=relatedaccountgroup,
        )

    @staticmethod
    def parse_related_account_group_path(path: str) -> Dict[str, str]:
        """Parses a related_account_group path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/relatedaccountgroups/(?P<relatedaccountgroup>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def related_account_group_membership_path(
        project: str,
        relatedaccountgroup: str,
        membership: str,
    ) -> str:
        """Returns a fully-qualified related_account_group_membership string."""
        return "projects/{project}/relatedaccountgroups/{relatedaccountgroup}/memberships/{membership}".format(
            project=project,
            relatedaccountgroup=relatedaccountgroup,
            membership=membership,
        )

    @staticmethod
    def parse_related_account_group_membership_path(path: str) -> Dict[str, str]:
        """Parses a related_account_group_membership path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/relatedaccountgroups/(?P<relatedaccountgroup>.+?)/memberships/(?P<membership>.+?)$",
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
        transport: Optional[Union[str, RecaptchaEnterpriseServiceTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the recaptcha enterprise service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, RecaptchaEnterpriseServiceTransport]): The
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
        if isinstance(transport, RecaptchaEnterpriseServiceTransport):
            # transport is a RecaptchaEnterpriseServiceTransport instance.
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

    def create_assessment(
        self,
        request: Optional[
            Union[recaptchaenterprise.CreateAssessmentRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        assessment: Optional[recaptchaenterprise.Assessment] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Assessment:
        r"""Creates an Assessment of the likelihood an event is
        legitimate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_create_assessment():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.CreateAssessmentRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_assessment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.CreateAssessmentRequest, dict]):
                The request object. The create assessment request
                message.
            parent (str):
                Required. The name of the project in
                which the assessment will be created, in
                the format "projects/{project}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            assessment (google.cloud.recaptchaenterprise_v1.types.Assessment):
                Required. The assessment details.
                This corresponds to the ``assessment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Assessment:
                A reCAPTCHA Enterprise assessment
                resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, assessment])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recaptchaenterprise.CreateAssessmentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.CreateAssessmentRequest):
            request = recaptchaenterprise.CreateAssessmentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if assessment is not None:
                request.assessment = assessment

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_assessment]

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

    def annotate_assessment(
        self,
        request: Optional[
            Union[recaptchaenterprise.AnnotateAssessmentRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        annotation: Optional[
            recaptchaenterprise.AnnotateAssessmentRequest.Annotation
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.AnnotateAssessmentResponse:
        r"""Annotates a previously created Assessment to provide
        additional information on whether the event turned out
        to be authentic or fraudulent.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_annotate_assessment():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.AnnotateAssessmentRequest(
                    name="name_value",
                )

                # Make the request
                response = client.annotate_assessment(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentRequest, dict]):
                The request object. The request message to annotate an
                Assessment.
            name (str):
                Required. The resource name of the
                Assessment, in the format
                "projects/{project}/assessments/{assessment}".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            annotation (google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentRequest.Annotation):
                Optional. The annotation that will be
                assigned to the Event. This field can be
                left empty to provide reasons that apply
                to an event without concluding whether
                the event is legitimate or fraudulent.

                This corresponds to the ``annotation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.AnnotateAssessmentResponse:
                Empty response for
                AnnotateAssessment.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, annotation])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recaptchaenterprise.AnnotateAssessmentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.AnnotateAssessmentRequest):
            request = recaptchaenterprise.AnnotateAssessmentRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if annotation is not None:
                request.annotation = annotation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.annotate_assessment]

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

    def create_key(
        self,
        request: Optional[Union[recaptchaenterprise.CreateKeyRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        key: Optional[recaptchaenterprise.Key] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Creates a new reCAPTCHA Enterprise key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_create_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                key = recaptchaenterprise_v1.Key()
                key.web_settings.integration_type = "INVISIBLE"

                request = recaptchaenterprise_v1.CreateKeyRequest(
                    parent="parent_value",
                    key=key,
                )

                # Make the request
                response = client.create_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.CreateKeyRequest, dict]):
                The request object. The create key request message.
            parent (str):
                Required. The name of the project in
                which the key will be created, in the
                format "projects/{project}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            key (google.cloud.recaptchaenterprise_v1.types.Key):
                Required. Information to create a
                reCAPTCHA Enterprise key.

                This corresponds to the ``key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, key])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recaptchaenterprise.CreateKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.CreateKeyRequest):
            request = recaptchaenterprise.CreateKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if key is not None:
                request.key = key

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_key]

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

    def list_keys(
        self,
        request: Optional[Union[recaptchaenterprise.ListKeysRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListKeysPager:
        r"""Returns the list of all keys that belong to a
        project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_list_keys():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.ListKeysRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_keys(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.ListKeysRequest, dict]):
                The request object. The list keys request message.
            parent (str):
                Required. The name of the project
                that contains the keys that will be
                listed, in the format
                "projects/{project}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.pagers.ListKeysPager:
                Response to request to list keys in a
                project.
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
        # in a recaptchaenterprise.ListKeysRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.ListKeysRequest):
            request = recaptchaenterprise.ListKeysRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_keys]

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
        response = pagers.ListKeysPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def retrieve_legacy_secret_key(
        self,
        request: Optional[
            Union[recaptchaenterprise.RetrieveLegacySecretKeyRequest, dict]
        ] = None,
        *,
        key: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.RetrieveLegacySecretKeyResponse:
        r"""Returns the secret key related to the specified
        public key. You must use the legacy secret key only in a
        3rd party integration with legacy reCAPTCHA.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_retrieve_legacy_secret_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.RetrieveLegacySecretKeyRequest(
                    key="key_value",
                )

                # Make the request
                response = client.retrieve_legacy_secret_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.RetrieveLegacySecretKeyRequest, dict]):
                The request object. The retrieve legacy secret key
                request message.
            key (str):
                Required. The public key name linked
                to the requested secret key in the
                format "projects/{project}/keys/{key}".

                This corresponds to the ``key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.RetrieveLegacySecretKeyResponse:
                Secret key is used only in legacy
                reCAPTCHA. It must be used in a 3rd
                party integration with legacy reCAPTCHA.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([key])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recaptchaenterprise.RetrieveLegacySecretKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.RetrieveLegacySecretKeyRequest):
            request = recaptchaenterprise.RetrieveLegacySecretKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if key is not None:
                request.key = key

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.retrieve_legacy_secret_key
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("key", request.key),)),
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

    def get_key(
        self,
        request: Optional[Union[recaptchaenterprise.GetKeyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Returns the specified key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_get_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.GetKeyRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.GetKeyRequest, dict]):
                The request object. The get key request message.
            name (str):
                Required. The name of the requested
                key, in the format
                "projects/{project}/keys/{key}".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

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
        # in a recaptchaenterprise.GetKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.GetKeyRequest):
            request = recaptchaenterprise.GetKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_key]

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

    def update_key(
        self,
        request: Optional[Union[recaptchaenterprise.UpdateKeyRequest, dict]] = None,
        *,
        key: Optional[recaptchaenterprise.Key] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Updates the specified key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_update_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                key = recaptchaenterprise_v1.Key()
                key.web_settings.integration_type = "INVISIBLE"

                request = recaptchaenterprise_v1.UpdateKeyRequest(
                    key=key,
                )

                # Make the request
                response = client.update_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.UpdateKeyRequest, dict]):
                The request object. The update key request message.
            key (google.cloud.recaptchaenterprise_v1.types.Key):
                Required. The key to update.
                This corresponds to the ``key`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. The mask to control which
                fields of the key get updated. If the
                mask is not present, all fields will be
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
            google.cloud.recaptchaenterprise_v1.types.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([key, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recaptchaenterprise.UpdateKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.UpdateKeyRequest):
            request = recaptchaenterprise.UpdateKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if key is not None:
                request.key = key
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_key]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("key.name", request.key.name),)),
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

    def delete_key(
        self,
        request: Optional[Union[recaptchaenterprise.DeleteKeyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified key.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_delete_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.DeleteKeyRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_key(request=request)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.DeleteKeyRequest, dict]):
                The request object. The delete key request message.
            name (str):
                Required. The name of the key to be
                deleted, in the format
                "projects/{project}/keys/{key}".

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
        # in a recaptchaenterprise.DeleteKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.DeleteKeyRequest):
            request = recaptchaenterprise.DeleteKeyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_key]

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

    def migrate_key(
        self,
        request: Optional[Union[recaptchaenterprise.MigrateKeyRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Key:
        r"""Migrates an existing key from reCAPTCHA to reCAPTCHA
        Enterprise. Once a key is migrated, it can be used from
        either product. SiteVerify requests are billed as
        CreateAssessment calls. You must be authenticated as one
        of the current owners of the reCAPTCHA Site Key, and
        your user must have the reCAPTCHA Enterprise Admin IAM
        role in the destination project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_migrate_key():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.MigrateKeyRequest(
                    name="name_value",
                )

                # Make the request
                response = client.migrate_key(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.MigrateKeyRequest, dict]):
                The request object. The migrate key request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Key:
                A key used to identify and configure
                applications (web and/or mobile) that
                use reCAPTCHA Enterprise.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a recaptchaenterprise.MigrateKeyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.MigrateKeyRequest):
            request = recaptchaenterprise.MigrateKeyRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.migrate_key]

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

    def get_metrics(
        self,
        request: Optional[Union[recaptchaenterprise.GetMetricsRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recaptchaenterprise.Metrics:
        r"""Get some aggregated metrics for a Key. This data can
        be used to build dashboards.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_get_metrics():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.GetMetricsRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_metrics(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.GetMetricsRequest, dict]):
                The request object. The get metrics request message.
            name (str):
                Required. The name of the requested
                metrics, in the format
                "projects/{project}/keys/{key}/metrics".

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.types.Metrics:
                Metrics for a single Key.
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
        # in a recaptchaenterprise.GetMetricsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.GetMetricsRequest):
            request = recaptchaenterprise.GetMetricsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_metrics]

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

    def list_related_account_groups(
        self,
        request: Optional[
            Union[recaptchaenterprise.ListRelatedAccountGroupsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRelatedAccountGroupsPager:
        r"""List groups of related accounts.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_list_related_account_groups():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.ListRelatedAccountGroupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_related_account_groups(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupsRequest, dict]):
                The request object. The request message to list related
                account groups.
            parent (str):
                Required. The name of the project to
                list related account groups from, in the
                format "projects/{project}".

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.pagers.ListRelatedAccountGroupsPager:
                The response to a ListRelatedAccountGroups call.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
        # in a recaptchaenterprise.ListRelatedAccountGroupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recaptchaenterprise.ListRelatedAccountGroupsRequest):
            request = recaptchaenterprise.ListRelatedAccountGroupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_related_account_groups
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListRelatedAccountGroupsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_related_account_group_memberships(
        self,
        request: Optional[
            Union[recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRelatedAccountGroupMembershipsPager:
        r"""Get memberships in a group of related accounts.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_list_related_account_group_memberships():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.ListRelatedAccountGroupMembershipsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_related_account_group_memberships(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.ListRelatedAccountGroupMembershipsRequest, dict]):
                The request object. The request message to list
                memberships in a related account group.
            parent (str):
                Required. The resource name for the related account
                group in the format
                ``projects/{project}/relatedaccountgroups/{relatedaccountgroup}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.pagers.ListRelatedAccountGroupMembershipsPager:
                The response to a ListRelatedAccountGroupMemberships
                call.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
        # in a recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest
        ):
            request = recaptchaenterprise.ListRelatedAccountGroupMembershipsRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_related_account_group_memberships
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListRelatedAccountGroupMembershipsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_related_account_group_memberships(
        self,
        request: Optional[
            Union[recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest, dict]
        ] = None,
        *,
        project: Optional[str] = None,
        hashed_account_id: Optional[bytes] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchRelatedAccountGroupMembershipsPager:
        r"""Search group memberships related to a given account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import recaptchaenterprise_v1

            def sample_search_related_account_group_memberships():
                # Create a client
                client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

                # Initialize request argument(s)
                request = recaptchaenterprise_v1.SearchRelatedAccountGroupMembershipsRequest(
                    project="project_value",
                )

                # Make the request
                page_result = client.search_related_account_group_memberships(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.recaptchaenterprise_v1.types.SearchRelatedAccountGroupMembershipsRequest, dict]):
                The request object. The request message to search related
                account group memberships.
            project (str):
                Required. The name of the project to
                search related account group memberships
                from. Specify the project name in the
                following format:

                "projects/{project}".

                This corresponds to the ``project`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            hashed_account_id (bytes):
                Optional. The unique stable hashed user identifier we
                should search connections to. The identifier should
                correspond to a ``hashed_account_id`` provided in a
                previous ``CreateAssessment`` or ``AnnotateAssessment``
                call.

                This corresponds to the ``hashed_account_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recaptchaenterprise_v1.services.recaptcha_enterprise_service.pagers.SearchRelatedAccountGroupMembershipsPager:
                The response to a SearchRelatedAccountGroupMemberships
                call.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project, hashed_account_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest
        ):
            request = recaptchaenterprise.SearchRelatedAccountGroupMembershipsRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project is not None:
                request.project = project
            if hashed_account_id is not None:
                request.hashed_account_id = hashed_account_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.search_related_account_group_memberships
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project", request.project),)),
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
        response = pagers.SearchRelatedAccountGroupMembershipsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "RecaptchaEnterpriseServiceClient":
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


__all__ = ("RecaptchaEnterpriseServiceClient",)
