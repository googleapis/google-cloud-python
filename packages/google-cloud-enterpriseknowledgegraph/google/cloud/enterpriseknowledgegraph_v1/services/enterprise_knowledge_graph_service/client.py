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

from google.cloud.enterpriseknowledgegraph_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.longrunning import operations_pb2
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore

from google.cloud.enterpriseknowledgegraph_v1.services.enterprise_knowledge_graph_service import (
    pagers,
)
from google.cloud.enterpriseknowledgegraph_v1.types import job_state, service

from .transports.base import (
    DEFAULT_CLIENT_INFO,
    EnterpriseKnowledgeGraphServiceTransport,
)
from .transports.grpc import EnterpriseKnowledgeGraphServiceGrpcTransport
from .transports.grpc_asyncio import EnterpriseKnowledgeGraphServiceGrpcAsyncIOTransport
from .transports.rest import EnterpriseKnowledgeGraphServiceRestTransport


class EnterpriseKnowledgeGraphServiceClientMeta(type):
    """Metaclass for the EnterpriseKnowledgeGraphService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[EnterpriseKnowledgeGraphServiceTransport]]
    _transport_registry["grpc"] = EnterpriseKnowledgeGraphServiceGrpcTransport
    _transport_registry[
        "grpc_asyncio"
    ] = EnterpriseKnowledgeGraphServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = EnterpriseKnowledgeGraphServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[EnterpriseKnowledgeGraphServiceTransport]:
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


class EnterpriseKnowledgeGraphServiceClient(
    metaclass=EnterpriseKnowledgeGraphServiceClientMeta
):
    """APIs for enterprise knowledge graph product."""

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

    DEFAULT_ENDPOINT = "enterpriseknowledgegraph.googleapis.com"
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
            EnterpriseKnowledgeGraphServiceClient: The constructed client.
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
            EnterpriseKnowledgeGraphServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> EnterpriseKnowledgeGraphServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            EnterpriseKnowledgeGraphServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def cloud_knowledge_graph_entity_path(
        project: str,
        location: str,
        cloud_knowledge_graph_entity: str,
    ) -> str:
        """Returns a fully-qualified cloud_knowledge_graph_entity string."""
        return "projects/{project}/locations/{location}/cloudKnowledgeGraphEntities/{cloud_knowledge_graph_entity}".format(
            project=project,
            location=location,
            cloud_knowledge_graph_entity=cloud_knowledge_graph_entity,
        )

    @staticmethod
    def parse_cloud_knowledge_graph_entity_path(path: str) -> Dict[str, str]:
        """Parses a cloud_knowledge_graph_entity path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/cloudKnowledgeGraphEntities/(?P<cloud_knowledge_graph_entity>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def dataset_path(
        project: str,
        dataset: str,
    ) -> str:
        """Returns a fully-qualified dataset string."""
        return "projects/{project}/datasets/{dataset}".format(
            project=project,
            dataset=dataset,
        )

    @staticmethod
    def parse_dataset_path(path: str) -> Dict[str, str]:
        """Parses a dataset path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/datasets/(?P<dataset>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def entity_reconciliation_job_path(
        project: str,
        location: str,
        entity_reconciliation_job: str,
    ) -> str:
        """Returns a fully-qualified entity_reconciliation_job string."""
        return "projects/{project}/locations/{location}/entityReconciliationJobs/{entity_reconciliation_job}".format(
            project=project,
            location=location,
            entity_reconciliation_job=entity_reconciliation_job,
        )

    @staticmethod
    def parse_entity_reconciliation_job_path(path: str) -> Dict[str, str]:
        """Parses a entity_reconciliation_job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/entityReconciliationJobs/(?P<entity_reconciliation_job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def public_knowledge_graph_entity_path(
        project: str,
        location: str,
        public_knowledge_graph_entity: str,
    ) -> str:
        """Returns a fully-qualified public_knowledge_graph_entity string."""
        return "projects/{project}/locations/{location}/publicKnowledgeGraphEntities/{public_knowledge_graph_entity}".format(
            project=project,
            location=location,
            public_knowledge_graph_entity=public_knowledge_graph_entity,
        )

    @staticmethod
    def parse_public_knowledge_graph_entity_path(path: str) -> Dict[str, str]:
        """Parses a public_knowledge_graph_entity path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/publicKnowledgeGraphEntities/(?P<public_knowledge_graph_entity>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def table_path(
        project: str,
        dataset: str,
        table: str,
    ) -> str:
        """Returns a fully-qualified table string."""
        return "projects/{project}/datasets/{dataset}/tables/{table}".format(
            project=project,
            dataset=dataset,
            table=table,
        )

    @staticmethod
    def parse_table_path(path: str) -> Dict[str, str]:
        """Parses a table path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/datasets/(?P<dataset>.+?)/tables/(?P<table>.+?)$",
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
        transport: Optional[
            Union[str, EnterpriseKnowledgeGraphServiceTransport]
        ] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the enterprise knowledge graph service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, EnterpriseKnowledgeGraphServiceTransport]): The
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
        if isinstance(transport, EnterpriseKnowledgeGraphServiceTransport):
            # transport is a EnterpriseKnowledgeGraphServiceTransport instance.
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

    def create_entity_reconciliation_job(
        self,
        request: Optional[
            Union[service.CreateEntityReconciliationJobRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        entity_reconciliation_job: Optional[service.EntityReconciliationJob] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.EntityReconciliationJob:
        r"""Creates a EntityReconciliationJob. A
        EntityReconciliationJob once created will right away be
        attempted to start.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import enterpriseknowledgegraph_v1

            def sample_create_entity_reconciliation_job():
                # Create a client
                client = enterpriseknowledgegraph_v1.EnterpriseKnowledgeGraphServiceClient()

                # Initialize request argument(s)
                request = enterpriseknowledgegraph_v1.CreateEntityReconciliationJobRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_entity_reconciliation_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.enterpriseknowledgegraph_v1.types.CreateEntityReconciliationJobRequest, dict]):
                The request object. Request message for
                CreateEntityReconciliationJob.
            parent (str):
                Required. The resource name of the Location to create
                the EntityReconciliationJob in. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entity_reconciliation_job (google.cloud.enterpriseknowledgegraph_v1.types.EntityReconciliationJob):
                Required. The EntityReconciliationJob
                to create.

                This corresponds to the ``entity_reconciliation_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.enterpriseknowledgegraph_v1.types.EntityReconciliationJob:
                Entity reconciliation job message.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, entity_reconciliation_job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.CreateEntityReconciliationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.CreateEntityReconciliationJobRequest):
            request = service.CreateEntityReconciliationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if entity_reconciliation_job is not None:
                request.entity_reconciliation_job = entity_reconciliation_job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_entity_reconciliation_job
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

        # Done; return the response.
        return response

    def get_entity_reconciliation_job(
        self,
        request: Optional[
            Union[service.GetEntityReconciliationJobRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.EntityReconciliationJob:
        r"""Gets a EntityReconciliationJob.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import enterpriseknowledgegraph_v1

            def sample_get_entity_reconciliation_job():
                # Create a client
                client = enterpriseknowledgegraph_v1.EnterpriseKnowledgeGraphServiceClient()

                # Initialize request argument(s)
                request = enterpriseknowledgegraph_v1.GetEntityReconciliationJobRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_entity_reconciliation_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.enterpriseknowledgegraph_v1.types.GetEntityReconciliationJobRequest, dict]):
                The request object. Request message for
                GetEntityReconciliationJob.
            name (str):
                Required. The name of the EntityReconciliationJob
                resource. Format:
                ``projects/{project}/locations/{location}/entityReconciliationJobs/{entity_reconciliation_job}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.enterpriseknowledgegraph_v1.types.EntityReconciliationJob:
                Entity reconciliation job message.
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
        # in a service.GetEntityReconciliationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetEntityReconciliationJobRequest):
            request = service.GetEntityReconciliationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_entity_reconciliation_job
        ]

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

    def list_entity_reconciliation_jobs(
        self,
        request: Optional[
            Union[service.ListEntityReconciliationJobsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEntityReconciliationJobsPager:
        r"""Lists Entity Reconciliation Jobs.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import enterpriseknowledgegraph_v1

            def sample_list_entity_reconciliation_jobs():
                # Create a client
                client = enterpriseknowledgegraph_v1.EnterpriseKnowledgeGraphServiceClient()

                # Initialize request argument(s)
                request = enterpriseknowledgegraph_v1.ListEntityReconciliationJobsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_entity_reconciliation_jobs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.enterpriseknowledgegraph_v1.types.ListEntityReconciliationJobsRequest, dict]):
                The request object. Request message for
                [EnterpriseKnowledgeGraphService.ListEntityReconciliationJobs][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.ListEntityReconciliationJobs].
            parent (str):
                Required. The name of the EntityReconciliationJob's
                parent resource. Format:
                ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.enterpriseknowledgegraph_v1.services.enterprise_knowledge_graph_service.pagers.ListEntityReconciliationJobsPager:
                Response message for
                   [EnterpriseKnowledgeGraphService.ListEntityReconciliationJobs][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.ListEntityReconciliationJobs].

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
        # in a service.ListEntityReconciliationJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListEntityReconciliationJobsRequest):
            request = service.ListEntityReconciliationJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_entity_reconciliation_jobs
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
        response = pagers.ListEntityReconciliationJobsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def cancel_entity_reconciliation_job(
        self,
        request: Optional[
            Union[service.CancelEntityReconciliationJobRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Cancels a EntityReconciliationJob. Success of
        cancellation is not guaranteed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import enterpriseknowledgegraph_v1

            def sample_cancel_entity_reconciliation_job():
                # Create a client
                client = enterpriseknowledgegraph_v1.EnterpriseKnowledgeGraphServiceClient()

                # Initialize request argument(s)
                request = enterpriseknowledgegraph_v1.CancelEntityReconciliationJobRequest(
                    name="name_value",
                )

                # Make the request
                client.cancel_entity_reconciliation_job(request=request)

        Args:
            request (Union[google.cloud.enterpriseknowledgegraph_v1.types.CancelEntityReconciliationJobRequest, dict]):
                The request object. Request message for
                CancelEntityReconciliationJob.
            name (str):
                Required. The name of the EntityReconciliationJob
                resource. Format:
                ``projects/{project}/locations/{location}/entityReconciliationJobs/{entity_reconciliation_job}``

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
        # in a service.CancelEntityReconciliationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.CancelEntityReconciliationJobRequest):
            request = service.CancelEntityReconciliationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.cancel_entity_reconciliation_job
        ]

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

    def delete_entity_reconciliation_job(
        self,
        request: Optional[
            Union[service.DeleteEntityReconciliationJobRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a EntityReconciliationJob.
        It only deletes the job when the job state is in FAILED,
        SUCCEEDED, and CANCELLED.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import enterpriseknowledgegraph_v1

            def sample_delete_entity_reconciliation_job():
                # Create a client
                client = enterpriseknowledgegraph_v1.EnterpriseKnowledgeGraphServiceClient()

                # Initialize request argument(s)
                request = enterpriseknowledgegraph_v1.DeleteEntityReconciliationJobRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_entity_reconciliation_job(request=request)

        Args:
            request (Union[google.cloud.enterpriseknowledgegraph_v1.types.DeleteEntityReconciliationJobRequest, dict]):
                The request object. Request message for
                DeleteEntityReconciliationJob.
            name (str):
                Required. The name of the EntityReconciliationJob
                resource. Format:
                ``projects/{project}/locations/{location}/entityReconciliationJobs/{entity_reconciliation_job}``

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
        # in a service.DeleteEntityReconciliationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.DeleteEntityReconciliationJobRequest):
            request = service.DeleteEntityReconciliationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_entity_reconciliation_job
        ]

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

    def lookup(
        self,
        request: Optional[Union[service.LookupRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        ids: Optional[MutableSequence[str]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.LookupResponse:
        r"""Finds the Cloud KG entities with CKG ID(s).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import enterpriseknowledgegraph_v1

            def sample_lookup():
                # Create a client
                client = enterpriseknowledgegraph_v1.EnterpriseKnowledgeGraphServiceClient()

                # Initialize request argument(s)
                request = enterpriseknowledgegraph_v1.LookupRequest(
                    parent="parent_value",
                    ids=['ids_value1', 'ids_value2'],
                )

                # Make the request
                response = client.lookup(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.enterpriseknowledgegraph_v1.types.LookupRequest, dict]):
                The request object. Request message for
                [EnterpriseKnowledgeGraphService.Lookup][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.Lookup].
            parent (str):
                Required. The name of the Entity's parent resource.
                Format: ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ids (MutableSequence[str]):
                Required. The list of entity ids to
                be used for lookup.

                This corresponds to the ``ids`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.enterpriseknowledgegraph_v1.types.LookupResponse:
                Response message for
                   [EnterpriseKnowledgeGraphService.Lookup][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.Lookup].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, ids])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.LookupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.LookupRequest):
            request = service.LookupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if ids is not None:
                request.ids = ids

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.lookup]

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

    def search(
        self,
        request: Optional[Union[service.SearchRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        query: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.SearchResponse:
        r"""Searches the Cloud KG entities with entity name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import enterpriseknowledgegraph_v1

            def sample_search():
                # Create a client
                client = enterpriseknowledgegraph_v1.EnterpriseKnowledgeGraphServiceClient()

                # Initialize request argument(s)
                request = enterpriseknowledgegraph_v1.SearchRequest(
                    parent="parent_value",
                    query="query_value",
                )

                # Make the request
                response = client.search(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.enterpriseknowledgegraph_v1.types.SearchRequest, dict]):
                The request object. Request message for
                [EnterpriseKnowledgeGraphService.Search][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.Search].
            parent (str):
                Required. The name of the Entity's parent resource.
                Format: ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (str):
                Required. The literal query string
                for search.

                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.enterpriseknowledgegraph_v1.types.SearchResponse:
                Response message for
                   [EnterpriseKnowledgeGraphService.Search][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.Search].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, query])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.SearchRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.SearchRequest):
            request = service.SearchRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if query is not None:
                request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search]

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

    def lookup_public_kg(
        self,
        request: Optional[Union[service.LookupPublicKgRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        ids: Optional[MutableSequence[str]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.LookupPublicKgResponse:
        r"""Finds the public KG entities with public KG ID(s).

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import enterpriseknowledgegraph_v1

            def sample_lookup_public_kg():
                # Create a client
                client = enterpriseknowledgegraph_v1.EnterpriseKnowledgeGraphServiceClient()

                # Initialize request argument(s)
                request = enterpriseknowledgegraph_v1.LookupPublicKgRequest(
                    parent="parent_value",
                    ids=['ids_value1', 'ids_value2'],
                )

                # Make the request
                response = client.lookup_public_kg(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.enterpriseknowledgegraph_v1.types.LookupPublicKgRequest, dict]):
                The request object. Request message for
                [EnterpriseKnowledgeGraphService.LookupPublicKg][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.LookupPublicKg].
            parent (str):
                Required. The name of the Entity's parent resource.
                Format: ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ids (MutableSequence[str]):
                Required. The list of entity ids to
                be used for lookup.

                This corresponds to the ``ids`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.enterpriseknowledgegraph_v1.types.LookupPublicKgResponse:
                Response message for
                   [EnterpriseKnowledgeGraphService.LookupPublicKg][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.LookupPublicKg].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, ids])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.LookupPublicKgRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.LookupPublicKgRequest):
            request = service.LookupPublicKgRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if ids is not None:
                request.ids = ids

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.lookup_public_kg]

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

    def search_public_kg(
        self,
        request: Optional[Union[service.SearchPublicKgRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        query: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.SearchPublicKgResponse:
        r"""Searches the public KG entities with entity name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import enterpriseknowledgegraph_v1

            def sample_search_public_kg():
                # Create a client
                client = enterpriseknowledgegraph_v1.EnterpriseKnowledgeGraphServiceClient()

                # Initialize request argument(s)
                request = enterpriseknowledgegraph_v1.SearchPublicKgRequest(
                    parent="parent_value",
                    query="query_value",
                )

                # Make the request
                response = client.search_public_kg(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.enterpriseknowledgegraph_v1.types.SearchPublicKgRequest, dict]):
                The request object. Request message for
                [EnterpriseKnowledgeGraphService.Search][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.Search].
            parent (str):
                Required. The name of the Entity's parent resource.
                Format: ``projects/{project}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (str):
                Required. The literal query string
                for search.

                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.enterpriseknowledgegraph_v1.types.SearchPublicKgResponse:
                Response message for
                   [EnterpriseKnowledgeGraphService.Search][google.cloud.enterpriseknowledgegraph.v1.EnterpriseKnowledgeGraphService.Search].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, query])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a service.SearchPublicKgRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.SearchPublicKgRequest):
            request = service.SearchPublicKgRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if query is not None:
                request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_public_kg]

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

    def __enter__(self) -> "EnterpriseKnowledgeGraphServiceClient":
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


__all__ = ("EnterpriseKnowledgeGraphServiceClient",)
