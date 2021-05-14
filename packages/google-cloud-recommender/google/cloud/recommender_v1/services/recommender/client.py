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

from google.cloud.recommender_v1.services.recommender import pagers
from google.cloud.recommender_v1.types import insight
from google.cloud.recommender_v1.types import recommendation
from google.cloud.recommender_v1.types import recommender_service
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import RecommenderTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import RecommenderGrpcTransport
from .transports.grpc_asyncio import RecommenderGrpcAsyncIOTransport


class RecommenderClientMeta(type):
    """Metaclass for the Recommender client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[RecommenderTransport]]
    _transport_registry["grpc"] = RecommenderGrpcTransport
    _transport_registry["grpc_asyncio"] = RecommenderGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[RecommenderTransport]:
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


class RecommenderClient(metaclass=RecommenderClientMeta):
    """Provides insights and recommendations for cloud customers for
    various categories like performance optimization, cost savings,
    reliability, feature discovery, etc. Insights and
    recommendations are generated automatically based on analysis of
    user resources, configuration and monitoring metrics.
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

    DEFAULT_ENDPOINT = "recommender.googleapis.com"
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
            RecommenderClient: The constructed client.
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
            RecommenderClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> RecommenderTransport:
        """Returns the transport used by the client instance.

        Returns:
            RecommenderTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def insight_path(
        project: str, location: str, insight_type: str, insight: str,
    ) -> str:
        """Returns a fully-qualified insight string."""
        return "projects/{project}/locations/{location}/insightTypes/{insight_type}/insights/{insight}".format(
            project=project,
            location=location,
            insight_type=insight_type,
            insight=insight,
        )

    @staticmethod
    def parse_insight_path(path: str) -> Dict[str, str]:
        """Parses a insight path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/insightTypes/(?P<insight_type>.+?)/insights/(?P<insight>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def insight_type_path(project: str, location: str, insight_type: str,) -> str:
        """Returns a fully-qualified insight_type string."""
        return "projects/{project}/locations/{location}/insightTypes/{insight_type}".format(
            project=project, location=location, insight_type=insight_type,
        )

    @staticmethod
    def parse_insight_type_path(path: str) -> Dict[str, str]:
        """Parses a insight_type path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/insightTypes/(?P<insight_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def recommendation_path(
        project: str, location: str, recommender: str, recommendation: str,
    ) -> str:
        """Returns a fully-qualified recommendation string."""
        return "projects/{project}/locations/{location}/recommenders/{recommender}/recommendations/{recommendation}".format(
            project=project,
            location=location,
            recommender=recommender,
            recommendation=recommendation,
        )

    @staticmethod
    def parse_recommendation_path(path: str) -> Dict[str, str]:
        """Parses a recommendation path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/recommenders/(?P<recommender>.+?)/recommendations/(?P<recommendation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def recommender_path(project: str, location: str, recommender: str,) -> str:
        """Returns a fully-qualified recommender string."""
        return "projects/{project}/locations/{location}/recommenders/{recommender}".format(
            project=project, location=location, recommender=recommender,
        )

    @staticmethod
    def parse_recommender_path(path: str) -> Dict[str, str]:
        """Parses a recommender path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/recommenders/(?P<recommender>.+?)$",
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
        transport: Union[str, RecommenderTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the recommender client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, RecommenderTransport]): The
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
        if isinstance(transport, RecommenderTransport):
            # transport is a RecommenderTransport instance.
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

    def list_insights(
        self,
        request: recommender_service.ListInsightsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInsightsPager:
        r"""Lists insights for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified insight
        type.

        Args:
            request (google.cloud.recommender_v1.types.ListInsightsRequest):
                The request object. Request for the `ListInsights`
                method.
            parent (str):
                Required. The container resource on which to execute the
                request. Acceptable formats:

                1.

                "projects/[PROJECT_NUMBER]/locations/[LOCATION]/insightTypes/[INSIGHT_TYPE_ID]",

                LOCATION here refers to GCP Locations:
                https://cloud.google.com/about/locations/
                INSIGHT_TYPE_ID refers to supported insight types:
                https://cloud.google.com/recommender/docs/insights/insight-types.)

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.services.recommender.pagers.ListInsightsPager:
                Response to the ListInsights method.

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
        # in a recommender_service.ListInsightsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recommender_service.ListInsightsRequest):
            request = recommender_service.ListInsightsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_insights]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListInsightsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_insight(
        self,
        request: recommender_service.GetInsightRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> insight.Insight:
        r"""Gets the requested insight. Requires the recommender.*.get IAM
        permission for the specified insight type.

        Args:
            request (google.cloud.recommender_v1.types.GetInsightRequest):
                The request object. Request to the `GetInsight` method.
            name (str):
                Required. Name of the insight.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Insight:
                An insight along with the information
                used to derive the insight. The insight
                may have associated recomendations as
                well.

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
        # in a recommender_service.GetInsightRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recommender_service.GetInsightRequest):
            request = recommender_service.GetInsightRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_insight]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def mark_insight_accepted(
        self,
        request: recommender_service.MarkInsightAcceptedRequest = None,
        *,
        name: str = None,
        state_metadata: Sequence[
            recommender_service.MarkInsightAcceptedRequest.StateMetadataEntry
        ] = None,
        etag: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> insight.Insight:
        r"""Marks the Insight State as Accepted. Users can use this method
        to indicate to the Recommender API that they have applied some
        action based on the insight. This stops the insight content from
        being updated.

        MarkInsightAccepted can be applied to insights in ACTIVE state.
        Requires the recommender.*.update IAM permission for the
        specified insight.

        Args:
            request (google.cloud.recommender_v1.types.MarkInsightAcceptedRequest):
                The request object. Request for the
                `MarkInsightAccepted` method.
            name (str):
                Required. Name of the insight.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            state_metadata (Sequence[google.cloud.recommender_v1.types.MarkInsightAcceptedRequest.StateMetadataEntry]):
                Optional. State properties user wish to include with
                this state. Full replace of the current state_metadata.

                This corresponds to the ``state_metadata`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            etag (str):
                Required. Fingerprint of the Insight.
                Provides optimistic locking.

                This corresponds to the ``etag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Insight:
                An insight along with the information
                used to derive the insight. The insight
                may have associated recomendations as
                well.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, state_metadata, etag])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recommender_service.MarkInsightAcceptedRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recommender_service.MarkInsightAcceptedRequest):
            request = recommender_service.MarkInsightAcceptedRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if state_metadata is not None:
                request.state_metadata = state_metadata
            if etag is not None:
                request.etag = etag

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.mark_insight_accepted]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_recommendations(
        self,
        request: recommender_service.ListRecommendationsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRecommendationsPager:
        r"""Lists recommendations for a Cloud project. Requires the
        recommender.*.list IAM permission for the specified recommender.

        Args:
            request (google.cloud.recommender_v1.types.ListRecommendationsRequest):
                The request object. Request for the
                `ListRecommendations` method.
            parent (str):
                Required. The container resource on which to execute the
                request. Acceptable formats:

                1.

                "projects/[PROJECT_NUMBER]/locations/[LOCATION]/recommenders/[RECOMMENDER_ID]",

                LOCATION here refers to GCP Locations:
                https://cloud.google.com/about/locations/ RECOMMENDER_ID
                refers to supported recommenders:
                https://cloud.google.com/recommender/docs/recommenders.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Filter expression to restrict the recommendations
                returned. Supported filter fields: state_info.state Eg:
                \`state_info.state:"DISMISSED" or
                state_info.state:"FAILED"

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.services.recommender.pagers.ListRecommendationsPager:
                Response to the ListRecommendations method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recommender_service.ListRecommendationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recommender_service.ListRecommendationsRequest):
            request = recommender_service.ListRecommendationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_recommendations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListRecommendationsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_recommendation(
        self,
        request: recommender_service.GetRecommendationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation.Recommendation:
        r"""Gets the requested recommendation. Requires the
        recommender.*.get IAM permission for the specified recommender.

        Args:
            request (google.cloud.recommender_v1.types.GetRecommendationRequest):
                The request object. Request to the `GetRecommendation`
                method.
            name (str):
                Required. Name of the recommendation.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

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
        # in a recommender_service.GetRecommendationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recommender_service.GetRecommendationRequest):
            request = recommender_service.GetRecommendationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_recommendation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def mark_recommendation_claimed(
        self,
        request: recommender_service.MarkRecommendationClaimedRequest = None,
        *,
        name: str = None,
        state_metadata: Sequence[
            recommender_service.MarkRecommendationClaimedRequest.StateMetadataEntry
        ] = None,
        etag: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation.Recommendation:
        r"""Marks the Recommendation State as Claimed. Users can use this
        method to indicate to the Recommender API that they are starting
        to apply the recommendation themselves. This stops the
        recommendation content from being updated. Associated insights
        are frozen and placed in the ACCEPTED state.

        MarkRecommendationClaimed can be applied to recommendations in
        CLAIMED, SUCCEEDED, FAILED, or ACTIVE state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Args:
            request (google.cloud.recommender_v1.types.MarkRecommendationClaimedRequest):
                The request object. Request for the
                `MarkRecommendationClaimed` Method.
            name (str):
                Required. Name of the recommendation.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            state_metadata (Sequence[google.cloud.recommender_v1.types.MarkRecommendationClaimedRequest.StateMetadataEntry]):
                State properties to include with this state. Overwrites
                any existing ``state_metadata``. Keys must match the
                regex ``/^[a-z0-9][a-z0-9_.-]{0,62}$/``. Values must match
                the regex ``/^[a-zA-Z0-9_./-]{0,255}$/``.

                This corresponds to the ``state_metadata`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            etag (str):
                Required. Fingerprint of the
                Recommendation. Provides optimistic
                locking.

                This corresponds to the ``etag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, state_metadata, etag])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recommender_service.MarkRecommendationClaimedRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, recommender_service.MarkRecommendationClaimedRequest
        ):
            request = recommender_service.MarkRecommendationClaimedRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if state_metadata is not None:
                request.state_metadata = state_metadata
            if etag is not None:
                request.etag = etag

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.mark_recommendation_claimed
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

    def mark_recommendation_succeeded(
        self,
        request: recommender_service.MarkRecommendationSucceededRequest = None,
        *,
        name: str = None,
        state_metadata: Sequence[
            recommender_service.MarkRecommendationSucceededRequest.StateMetadataEntry
        ] = None,
        etag: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation.Recommendation:
        r"""Marks the Recommendation State as Succeeded. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation was successful.
        This stops the recommendation content from being updated.
        Associated insights are frozen and placed in the ACCEPTED state.

        MarkRecommendationSucceeded can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Args:
            request (google.cloud.recommender_v1.types.MarkRecommendationSucceededRequest):
                The request object. Request for the
                `MarkRecommendationSucceeded` Method.
            name (str):
                Required. Name of the recommendation.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            state_metadata (Sequence[google.cloud.recommender_v1.types.MarkRecommendationSucceededRequest.StateMetadataEntry]):
                State properties to include with this state. Overwrites
                any existing ``state_metadata``. Keys must match the
                regex ``/^[a-z0-9][a-z0-9_.-]{0,62}$/``. Values must match
                the regex ``/^[a-zA-Z0-9_./-]{0,255}$/``.

                This corresponds to the ``state_metadata`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            etag (str):
                Required. Fingerprint of the
                Recommendation. Provides optimistic
                locking.

                This corresponds to the ``etag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, state_metadata, etag])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recommender_service.MarkRecommendationSucceededRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, recommender_service.MarkRecommendationSucceededRequest
        ):
            request = recommender_service.MarkRecommendationSucceededRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if state_metadata is not None:
                request.state_metadata = state_metadata
            if etag is not None:
                request.etag = etag

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.mark_recommendation_succeeded
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

    def mark_recommendation_failed(
        self,
        request: recommender_service.MarkRecommendationFailedRequest = None,
        *,
        name: str = None,
        state_metadata: Sequence[
            recommender_service.MarkRecommendationFailedRequest.StateMetadataEntry
        ] = None,
        etag: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation.Recommendation:
        r"""Marks the Recommendation State as Failed. Users can use this
        method to indicate to the Recommender API that they have applied
        the recommendation themselves, and the operation failed. This
        stops the recommendation content from being updated. Associated
        insights are frozen and placed in the ACCEPTED state.

        MarkRecommendationFailed can be applied to recommendations in
        ACTIVE, CLAIMED, SUCCEEDED, or FAILED state.

        Requires the recommender.*.update IAM permission for the
        specified recommender.

        Args:
            request (google.cloud.recommender_v1.types.MarkRecommendationFailedRequest):
                The request object. Request for the
                `MarkRecommendationFailed` Method.
            name (str):
                Required. Name of the recommendation.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            state_metadata (Sequence[google.cloud.recommender_v1.types.MarkRecommendationFailedRequest.StateMetadataEntry]):
                State properties to include with this state. Overwrites
                any existing ``state_metadata``. Keys must match the
                regex ``/^[a-z0-9][a-z0-9_.-]{0,62}$/``. Values must match
                the regex ``/^[a-zA-Z0-9_./-]{0,255}$/``.

                This corresponds to the ``state_metadata`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            etag (str):
                Required. Fingerprint of the
                Recommendation. Provides optimistic
                locking.

                This corresponds to the ``etag`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.recommender_v1.types.Recommendation:
                A recommendation along with a
                suggested action. E.g., a rightsizing
                recommendation for an underutilized VM,
                IAM role recommendations, etc

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, state_metadata, etag])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recommender_service.MarkRecommendationFailedRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, recommender_service.MarkRecommendationFailedRequest):
            request = recommender_service.MarkRecommendationFailedRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if state_metadata is not None:
                request.state_metadata = state_metadata
            if etag is not None:
                request.etag = etag

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.mark_recommendation_failed
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-recommender",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("RecommenderClient",)
