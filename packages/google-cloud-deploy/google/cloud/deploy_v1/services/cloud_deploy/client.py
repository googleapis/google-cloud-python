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

from google.cloud.deploy_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.deploy_v1.services.cloud_deploy import pagers
from google.cloud.deploy_v1.types import cloud_deploy

from .transports.base import DEFAULT_CLIENT_INFO, CloudDeployTransport
from .transports.grpc import CloudDeployGrpcTransport
from .transports.grpc_asyncio import CloudDeployGrpcAsyncIOTransport
from .transports.rest import CloudDeployRestTransport


class CloudDeployClientMeta(type):
    """Metaclass for the CloudDeploy client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[CloudDeployTransport]]
    _transport_registry["grpc"] = CloudDeployGrpcTransport
    _transport_registry["grpc_asyncio"] = CloudDeployGrpcAsyncIOTransport
    _transport_registry["rest"] = CloudDeployRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[CloudDeployTransport]:
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


class CloudDeployClient(metaclass=CloudDeployClientMeta):
    """CloudDeploy service creates and manages Continuous Delivery
    operations on Google Cloud Platform via Skaffold
    (https://skaffold.dev).
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

    DEFAULT_ENDPOINT = "clouddeploy.googleapis.com"
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
            CloudDeployClient: The constructed client.
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
            CloudDeployClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudDeployTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudDeployTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def build_path(
        project: str,
        location: str,
        build: str,
    ) -> str:
        """Returns a fully-qualified build string."""
        return "projects/{project}/locations/{location}/builds/{build}".format(
            project=project,
            location=location,
            build=build,
        )

    @staticmethod
    def parse_build_path(path: str) -> Dict[str, str]:
        """Parses a build path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/builds/(?P<build>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def cluster_path(
        project: str,
        location: str,
        cluster: str,
    ) -> str:
        """Returns a fully-qualified cluster string."""
        return "projects/{project}/locations/{location}/clusters/{cluster}".format(
            project=project,
            location=location,
            cluster=cluster,
        )

    @staticmethod
    def parse_cluster_path(path: str) -> Dict[str, str]:
        """Parses a cluster path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/clusters/(?P<cluster>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def config_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified config string."""
        return "projects/{project}/locations/{location}/config".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_config_path(path: str) -> Dict[str, str]:
        """Parses a config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/config$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def delivery_pipeline_path(
        project: str,
        location: str,
        delivery_pipeline: str,
    ) -> str:
        """Returns a fully-qualified delivery_pipeline string."""
        return "projects/{project}/locations/{location}/deliveryPipelines/{delivery_pipeline}".format(
            project=project,
            location=location,
            delivery_pipeline=delivery_pipeline,
        )

    @staticmethod
    def parse_delivery_pipeline_path(path: str) -> Dict[str, str]:
        """Parses a delivery_pipeline path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/deliveryPipelines/(?P<delivery_pipeline>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def job_run_path(
        project: str,
        location: str,
        delivery_pipeline: str,
        release: str,
        rollout: str,
        job_run: str,
    ) -> str:
        """Returns a fully-qualified job_run string."""
        return "projects/{project}/locations/{location}/deliveryPipelines/{delivery_pipeline}/releases/{release}/rollouts/{rollout}/jobRuns/{job_run}".format(
            project=project,
            location=location,
            delivery_pipeline=delivery_pipeline,
            release=release,
            rollout=rollout,
            job_run=job_run,
        )

    @staticmethod
    def parse_job_run_path(path: str) -> Dict[str, str]:
        """Parses a job_run path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/deliveryPipelines/(?P<delivery_pipeline>.+?)/releases/(?P<release>.+?)/rollouts/(?P<rollout>.+?)/jobRuns/(?P<job_run>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def membership_path(
        project: str,
        location: str,
        membership: str,
    ) -> str:
        """Returns a fully-qualified membership string."""
        return (
            "projects/{project}/locations/{location}/memberships/{membership}".format(
                project=project,
                location=location,
                membership=membership,
            )
        )

    @staticmethod
    def parse_membership_path(path: str) -> Dict[str, str]:
        """Parses a membership path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/memberships/(?P<membership>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def release_path(
        project: str,
        location: str,
        delivery_pipeline: str,
        release: str,
    ) -> str:
        """Returns a fully-qualified release string."""
        return "projects/{project}/locations/{location}/deliveryPipelines/{delivery_pipeline}/releases/{release}".format(
            project=project,
            location=location,
            delivery_pipeline=delivery_pipeline,
            release=release,
        )

    @staticmethod
    def parse_release_path(path: str) -> Dict[str, str]:
        """Parses a release path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/deliveryPipelines/(?P<delivery_pipeline>.+?)/releases/(?P<release>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def rollout_path(
        project: str,
        location: str,
        delivery_pipeline: str,
        release: str,
        rollout: str,
    ) -> str:
        """Returns a fully-qualified rollout string."""
        return "projects/{project}/locations/{location}/deliveryPipelines/{delivery_pipeline}/releases/{release}/rollouts/{rollout}".format(
            project=project,
            location=location,
            delivery_pipeline=delivery_pipeline,
            release=release,
            rollout=rollout,
        )

    @staticmethod
    def parse_rollout_path(path: str) -> Dict[str, str]:
        """Parses a rollout path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/deliveryPipelines/(?P<delivery_pipeline>.+?)/releases/(?P<release>.+?)/rollouts/(?P<rollout>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def service_path(
        project: str,
        location: str,
        service: str,
    ) -> str:
        """Returns a fully-qualified service string."""
        return "projects/{project}/locations/{location}/services/{service}".format(
            project=project,
            location=location,
            service=service,
        )

    @staticmethod
    def parse_service_path(path: str) -> Dict[str, str]:
        """Parses a service path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/services/(?P<service>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def target_path(
        project: str,
        location: str,
        target: str,
    ) -> str:
        """Returns a fully-qualified target string."""
        return "projects/{project}/locations/{location}/targets/{target}".format(
            project=project,
            location=location,
            target=target,
        )

    @staticmethod
    def parse_target_path(path: str) -> Dict[str, str]:
        """Parses a target path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/targets/(?P<target>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def worker_pool_path(
        project: str,
        location: str,
        worker_pool: str,
    ) -> str:
        """Returns a fully-qualified worker_pool string."""
        return (
            "projects/{project}/locations/{location}/workerPools/{worker_pool}".format(
                project=project,
                location=location,
                worker_pool=worker_pool,
            )
        )

    @staticmethod
    def parse_worker_pool_path(path: str) -> Dict[str, str]:
        """Parses a worker_pool path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/workerPools/(?P<worker_pool>.+?)$",
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
        transport: Optional[Union[str, CloudDeployTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud deploy client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, CloudDeployTransport]): The
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
        if isinstance(transport, CloudDeployTransport):
            # transport is a CloudDeployTransport instance.
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

    def list_delivery_pipelines(
        self,
        request: Optional[
            Union[cloud_deploy.ListDeliveryPipelinesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDeliveryPipelinesPager:
        r"""Lists DeliveryPipelines in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_list_delivery_pipelines():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ListDeliveryPipelinesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_delivery_pipelines(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ListDeliveryPipelinesRequest, dict]):
                The request object. The request object for ``ListDeliveryPipelines``.
            parent (str):
                Required. The parent, which owns this collection of
                pipelines. Format must be
                projects/{project_id}/locations/{location_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.services.cloud_deploy.pagers.ListDeliveryPipelinesPager:
                The response object from ListDeliveryPipelines.

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
        # in a cloud_deploy.ListDeliveryPipelinesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.ListDeliveryPipelinesRequest):
            request = cloud_deploy.ListDeliveryPipelinesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_delivery_pipelines]

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
        response = pagers.ListDeliveryPipelinesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_delivery_pipeline(
        self,
        request: Optional[Union[cloud_deploy.GetDeliveryPipelineRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.DeliveryPipeline:
        r"""Gets details of a single DeliveryPipeline.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_get_delivery_pipeline():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetDeliveryPipelineRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_delivery_pipeline(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetDeliveryPipelineRequest, dict]):
                The request object. The request object for ``GetDeliveryPipeline``
            name (str):
                Required. Name of the ``DeliveryPipeline``. Format must
                be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.DeliveryPipeline:
                A DeliveryPipeline resource in the Google Cloud Deploy
                API.

                   A DeliveryPipeline defines a pipeline through which a
                   Skaffold configuration can progress.

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
        # in a cloud_deploy.GetDeliveryPipelineRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.GetDeliveryPipelineRequest):
            request = cloud_deploy.GetDeliveryPipelineRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_delivery_pipeline]

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

    def create_delivery_pipeline(
        self,
        request: Optional[
            Union[cloud_deploy.CreateDeliveryPipelineRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        delivery_pipeline: Optional[cloud_deploy.DeliveryPipeline] = None,
        delivery_pipeline_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new DeliveryPipeline in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_create_delivery_pipeline():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.CreateDeliveryPipelineRequest(
                    parent="parent_value",
                    delivery_pipeline_id="delivery_pipeline_id_value",
                )

                # Make the request
                operation = client.create_delivery_pipeline(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.CreateDeliveryPipelineRequest, dict]):
                The request object. The request object for ``CreateDeliveryPipeline``.
            parent (str):
                Required. The parent collection in which the
                ``DeliveryPipeline`` should be created. Format should be
                projects/{project_id}/locations/{location_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            delivery_pipeline (google.cloud.deploy_v1.types.DeliveryPipeline):
                Required. The ``DeliveryPipeline`` to create.
                This corresponds to the ``delivery_pipeline`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            delivery_pipeline_id (str):
                Required. ID of the ``DeliveryPipeline``.
                This corresponds to the ``delivery_pipeline_id`` field
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
                :class:`google.cloud.deploy_v1.types.DeliveryPipeline` A
                DeliveryPipeline resource in the Google Cloud Deploy
                API.

                   A DeliveryPipeline defines a pipeline through which a
                   Skaffold configuration can progress.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, delivery_pipeline, delivery_pipeline_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloud_deploy.CreateDeliveryPipelineRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.CreateDeliveryPipelineRequest):
            request = cloud_deploy.CreateDeliveryPipelineRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if delivery_pipeline is not None:
                request.delivery_pipeline = delivery_pipeline
            if delivery_pipeline_id is not None:
                request.delivery_pipeline_id = delivery_pipeline_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_delivery_pipeline]

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
            cloud_deploy.DeliveryPipeline,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_delivery_pipeline(
        self,
        request: Optional[
            Union[cloud_deploy.UpdateDeliveryPipelineRequest, dict]
        ] = None,
        *,
        delivery_pipeline: Optional[cloud_deploy.DeliveryPipeline] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the parameters of a single DeliveryPipeline.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_update_delivery_pipeline():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.UpdateDeliveryPipelineRequest(
                )

                # Make the request
                operation = client.update_delivery_pipeline(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.UpdateDeliveryPipelineRequest, dict]):
                The request object. The request object for ``UpdateDeliveryPipeline``.
            delivery_pipeline (google.cloud.deploy_v1.types.DeliveryPipeline):
                Required. The ``DeliveryPipeline`` to update.
                This corresponds to the ``delivery_pipeline`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to specify the fields to be
                overwritten in the ``DeliveryPipeline`` resource by the
                update. The fields specified in the update_mask are
                relative to the resource, not the full request. A field
                will be overwritten if it is in the mask. If the user
                does not provide a mask then all fields will be
                overwritten.

                This corresponds to the ``update_mask`` field
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
                :class:`google.cloud.deploy_v1.types.DeliveryPipeline` A
                DeliveryPipeline resource in the Google Cloud Deploy
                API.

                   A DeliveryPipeline defines a pipeline through which a
                   Skaffold configuration can progress.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([delivery_pipeline, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloud_deploy.UpdateDeliveryPipelineRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.UpdateDeliveryPipelineRequest):
            request = cloud_deploy.UpdateDeliveryPipelineRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if delivery_pipeline is not None:
                request.delivery_pipeline = delivery_pipeline
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_delivery_pipeline]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("delivery_pipeline.name", request.delivery_pipeline.name),)
            ),
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
            cloud_deploy.DeliveryPipeline,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_delivery_pipeline(
        self,
        request: Optional[
            Union[cloud_deploy.DeleteDeliveryPipelineRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single DeliveryPipeline.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_delete_delivery_pipeline():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.DeleteDeliveryPipelineRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_delivery_pipeline(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.DeleteDeliveryPipelineRequest, dict]):
                The request object. The request object for ``DeleteDeliveryPipeline``.
            name (str):
                Required. The name of the ``DeliveryPipeline`` to
                delete. Format should be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.

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
        # in a cloud_deploy.DeleteDeliveryPipelineRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.DeleteDeliveryPipelineRequest):
            request = cloud_deploy.DeleteDeliveryPipelineRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_delivery_pipeline]

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
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_targets(
        self,
        request: Optional[Union[cloud_deploy.ListTargetsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTargetsPager:
        r"""Lists Targets in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_list_targets():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ListTargetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_targets(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ListTargetsRequest, dict]):
                The request object. The request object for ``ListTargets``.
            parent (str):
                Required. The parent, which owns this collection of
                targets. Format must be
                projects/{project_id}/locations/{location_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.services.cloud_deploy.pagers.ListTargetsPager:
                The response object from ListTargets.

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
        # in a cloud_deploy.ListTargetsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.ListTargetsRequest):
            request = cloud_deploy.ListTargetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_targets]

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
        response = pagers.ListTargetsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_target(
        self,
        request: Optional[Union[cloud_deploy.GetTargetRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.Target:
        r"""Gets details of a single Target.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_get_target():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetTargetRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_target(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetTargetRequest, dict]):
                The request object. The request object for ``GetTarget``.
            name (str):
                Required. Name of the ``Target``. Format must be
                projects/{project_id}/locations/{location_name}/targets/{target_name}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.Target:
                A Target resource in the Google Cloud Deploy API.

                   A Target defines a location to which a Skaffold
                   configuration can be deployed.

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
        # in a cloud_deploy.GetTargetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.GetTargetRequest):
            request = cloud_deploy.GetTargetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_target]

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

    def create_target(
        self,
        request: Optional[Union[cloud_deploy.CreateTargetRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        target: Optional[cloud_deploy.Target] = None,
        target_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new Target in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_create_target():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.CreateTargetRequest(
                    parent="parent_value",
                    target_id="target_id_value",
                )

                # Make the request
                operation = client.create_target(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.CreateTargetRequest, dict]):
                The request object. The request object for ``CreateTarget``.
            parent (str):
                Required. The parent collection in which the ``Target``
                should be created. Format should be
                projects/{project_id}/locations/{location_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target (google.cloud.deploy_v1.types.Target):
                Required. The ``Target`` to create.
                This corresponds to the ``target`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target_id (str):
                Required. ID of the ``Target``.
                This corresponds to the ``target_id`` field
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
                :class:`google.cloud.deploy_v1.types.Target` A Target
                resource in the Google Cloud Deploy API.

                   A Target defines a location to which a Skaffold
                   configuration can be deployed.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, target, target_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloud_deploy.CreateTargetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.CreateTargetRequest):
            request = cloud_deploy.CreateTargetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if target is not None:
                request.target = target
            if target_id is not None:
                request.target_id = target_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_target]

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
            cloud_deploy.Target,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_target(
        self,
        request: Optional[Union[cloud_deploy.UpdateTargetRequest, dict]] = None,
        *,
        target: Optional[cloud_deploy.Target] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the parameters of a single Target.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_update_target():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.UpdateTargetRequest(
                )

                # Make the request
                operation = client.update_target(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.UpdateTargetRequest, dict]):
                The request object. The request object for ``UpdateTarget``.
            target (google.cloud.deploy_v1.types.Target):
                Required. The ``Target`` to update.
                This corresponds to the ``target`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. Field mask is used to specify the fields to be
                overwritten in the Target resource by the update. The
                fields specified in the update_mask are relative to the
                resource, not the full request. A field will be
                overwritten if it is in the mask. If the user does not
                provide a mask then all fields will be overwritten.

                This corresponds to the ``update_mask`` field
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
                :class:`google.cloud.deploy_v1.types.Target` A Target
                resource in the Google Cloud Deploy API.

                   A Target defines a location to which a Skaffold
                   configuration can be deployed.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([target, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloud_deploy.UpdateTargetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.UpdateTargetRequest):
            request = cloud_deploy.UpdateTargetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if target is not None:
                request.target = target
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_target]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("target.name", request.target.name),)
            ),
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
            cloud_deploy.Target,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_target(
        self,
        request: Optional[Union[cloud_deploy.DeleteTargetRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single Target.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_delete_target():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.DeleteTargetRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_target(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.DeleteTargetRequest, dict]):
                The request object. The request object for ``DeleteTarget``.
            name (str):
                Required. The name of the ``Target`` to delete. Format
                should be
                projects/{project_id}/locations/{location_name}/targets/{target_name}.

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
        # in a cloud_deploy.DeleteTargetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.DeleteTargetRequest):
            request = cloud_deploy.DeleteTargetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_target]

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
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_releases(
        self,
        request: Optional[Union[cloud_deploy.ListReleasesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListReleasesPager:
        r"""Lists Releases in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_list_releases():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ListReleasesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_releases(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ListReleasesRequest, dict]):
                The request object. The request object for ``ListReleases``.
            parent (str):
                Required. The ``DeliveryPipeline`` which owns this
                collection of ``Release`` objects.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.services.cloud_deploy.pagers.ListReleasesPager:
                The response object from ListReleases.

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
        # in a cloud_deploy.ListReleasesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.ListReleasesRequest):
            request = cloud_deploy.ListReleasesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_releases]

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
        response = pagers.ListReleasesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_release(
        self,
        request: Optional[Union[cloud_deploy.GetReleaseRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.Release:
        r"""Gets details of a single Release.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_get_release():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetReleaseRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_release(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetReleaseRequest, dict]):
                The request object. The request object for ``GetRelease``.
            name (str):
                Required. Name of the ``Release``. Format must be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.Release:
                A Release resource in the Google Cloud Deploy API.

                   A Release defines a specific Skaffold configuration
                   instance that can be deployed.

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
        # in a cloud_deploy.GetReleaseRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.GetReleaseRequest):
            request = cloud_deploy.GetReleaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_release]

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

    def create_release(
        self,
        request: Optional[Union[cloud_deploy.CreateReleaseRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        release: Optional[cloud_deploy.Release] = None,
        release_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new Release in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_create_release():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.CreateReleaseRequest(
                    parent="parent_value",
                    release_id="release_id_value",
                )

                # Make the request
                operation = client.create_release(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.CreateReleaseRequest, dict]):
                The request object. The request object for ``CreateRelease``,
            parent (str):
                Required. The parent collection in which the ``Release``
                should be created. Format should be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            release (google.cloud.deploy_v1.types.Release):
                Required. The ``Release`` to create.
                This corresponds to the ``release`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            release_id (str):
                Required. ID of the ``Release``.
                This corresponds to the ``release_id`` field
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
                :class:`google.cloud.deploy_v1.types.Release` A Release
                resource in the Google Cloud Deploy API.

                   A Release defines a specific Skaffold configuration
                   instance that can be deployed.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, release, release_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloud_deploy.CreateReleaseRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.CreateReleaseRequest):
            request = cloud_deploy.CreateReleaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if release is not None:
                request.release = release
            if release_id is not None:
                request.release_id = release_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_release]

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
            cloud_deploy.Release,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    def abandon_release(
        self,
        request: Optional[Union[cloud_deploy.AbandonReleaseRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.AbandonReleaseResponse:
        r"""Abandons a Release in the Delivery Pipeline.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_abandon_release():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.AbandonReleaseRequest(
                    name="name_value",
                )

                # Make the request
                response = client.abandon_release(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.AbandonReleaseRequest, dict]):
                The request object. The request object used by ``AbandonRelease``.
            name (str):
                Required. Name of the Release. Format
                is
                projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
                releases/{release}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.AbandonReleaseResponse:
                The response object for AbandonRelease.
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
        # in a cloud_deploy.AbandonReleaseRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.AbandonReleaseRequest):
            request = cloud_deploy.AbandonReleaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.abandon_release]

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

    def approve_rollout(
        self,
        request: Optional[Union[cloud_deploy.ApproveRolloutRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.ApproveRolloutResponse:
        r"""Approves a Rollout.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_approve_rollout():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ApproveRolloutRequest(
                    name="name_value",
                    approved=True,
                )

                # Make the request
                response = client.approve_rollout(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ApproveRolloutRequest, dict]):
                The request object. The request object used by ``ApproveRollout``.
            name (str):
                Required. Name of the Rollout. Format
                is
                projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
                releases/{release}/rollouts/{rollout}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.ApproveRolloutResponse:
                The response object from ApproveRollout.
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
        # in a cloud_deploy.ApproveRolloutRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.ApproveRolloutRequest):
            request = cloud_deploy.ApproveRolloutRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.approve_rollout]

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

    def advance_rollout(
        self,
        request: Optional[Union[cloud_deploy.AdvanceRolloutRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        phase_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.AdvanceRolloutResponse:
        r"""Advances a Rollout in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_advance_rollout():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.AdvanceRolloutRequest(
                    name="name_value",
                    phase_id="phase_id_value",
                )

                # Make the request
                response = client.advance_rollout(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.AdvanceRolloutRequest, dict]):
                The request object. The request object used by ``AdvanceRollout``.
            name (str):
                Required. Name of the Rollout. Format
                is
                projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
                releases/{release}/rollouts/{rollout}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            phase_id (str):
                Required. The phase ID to advance the ``Rollout`` to.
                This corresponds to the ``phase_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.AdvanceRolloutResponse:
                The response object from AdvanceRollout.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, phase_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloud_deploy.AdvanceRolloutRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.AdvanceRolloutRequest):
            request = cloud_deploy.AdvanceRolloutRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if phase_id is not None:
                request.phase_id = phase_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.advance_rollout]

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

    def cancel_rollout(
        self,
        request: Optional[Union[cloud_deploy.CancelRolloutRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.CancelRolloutResponse:
        r"""Cancels a Rollout in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_cancel_rollout():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.CancelRolloutRequest(
                    name="name_value",
                )

                # Make the request
                response = client.cancel_rollout(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.CancelRolloutRequest, dict]):
                The request object. The request object used by ``CancelRollout``.
            name (str):
                Required. Name of the Rollout. Format
                is
                projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
                releases/{release}/rollouts/{rollout}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.CancelRolloutResponse:
                The response object from CancelRollout.
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
        # in a cloud_deploy.CancelRolloutRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.CancelRolloutRequest):
            request = cloud_deploy.CancelRolloutRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_rollout]

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

    def list_rollouts(
        self,
        request: Optional[Union[cloud_deploy.ListRolloutsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRolloutsPager:
        r"""Lists Rollouts in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_list_rollouts():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ListRolloutsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_rollouts(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ListRolloutsRequest, dict]):
                The request object. ListRolloutsRequest is the request object used by
                ``ListRollouts``.
            parent (str):
                Required. The ``Release`` which owns this collection of
                ``Rollout`` objects.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.services.cloud_deploy.pagers.ListRolloutsPager:
                ListRolloutsResponse is the response object reutrned by
                ListRollouts.

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
        # in a cloud_deploy.ListRolloutsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.ListRolloutsRequest):
            request = cloud_deploy.ListRolloutsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_rollouts]

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
        response = pagers.ListRolloutsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_rollout(
        self,
        request: Optional[Union[cloud_deploy.GetRolloutRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.Rollout:
        r"""Gets details of a single Rollout.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_get_rollout():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetRolloutRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_rollout(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetRolloutRequest, dict]):
                The request object. GetRolloutRequest is the request object used by
                ``GetRollout``.
            name (str):
                Required. Name of the ``Rollout``. Format must be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}/rollouts/{rollout_name}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.Rollout:
                A Rollout resource in the Google Cloud Deploy API.

                   A Rollout contains information around a specific
                   deployment to a Target.

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
        # in a cloud_deploy.GetRolloutRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.GetRolloutRequest):
            request = cloud_deploy.GetRolloutRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_rollout]

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

    def create_rollout(
        self,
        request: Optional[Union[cloud_deploy.CreateRolloutRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        rollout: Optional[cloud_deploy.Rollout] = None,
        rollout_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new Rollout in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_create_rollout():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                rollout = deploy_v1.Rollout()
                rollout.target_id = "target_id_value"

                request = deploy_v1.CreateRolloutRequest(
                    parent="parent_value",
                    rollout_id="rollout_id_value",
                    rollout=rollout,
                )

                # Make the request
                operation = client.create_rollout(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.CreateRolloutRequest, dict]):
                The request object. CreateRolloutRequest is the request object used by
                ``CreateRollout``.
            parent (str):
                Required. The parent collection in which the ``Rollout``
                should be created. Format should be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rollout (google.cloud.deploy_v1.types.Rollout):
                Required. The ``Rollout`` to create.
                This corresponds to the ``rollout`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rollout_id (str):
                Required. ID of the ``Rollout``.
                This corresponds to the ``rollout_id`` field
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
                :class:`google.cloud.deploy_v1.types.Rollout` A Rollout
                resource in the Google Cloud Deploy API.

                   A Rollout contains information around a specific
                   deployment to a Target.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, rollout, rollout_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloud_deploy.CreateRolloutRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.CreateRolloutRequest):
            request = cloud_deploy.CreateRolloutRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if rollout is not None:
                request.rollout = rollout
            if rollout_id is not None:
                request.rollout_id = rollout_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_rollout]

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
            cloud_deploy.Rollout,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    def ignore_job(
        self,
        request: Optional[Union[cloud_deploy.IgnoreJobRequest, dict]] = None,
        *,
        rollout: Optional[str] = None,
        phase_id: Optional[str] = None,
        job_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.IgnoreJobResponse:
        r"""Ignores the specified Job in a Rollout.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_ignore_job():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.IgnoreJobRequest(
                    rollout="rollout_value",
                    phase_id="phase_id_value",
                    job_id="job_id_value",
                )

                # Make the request
                response = client.ignore_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.IgnoreJobRequest, dict]):
                The request object. The request object used by ``IgnoreJob``.
            rollout (str):
                Required. Name of the Rollout. Format
                is
                projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
                releases/{release}/rollouts/{rollout}.

                This corresponds to the ``rollout`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            phase_id (str):
                Required. The phase ID the Job to
                ignore belongs to.

                This corresponds to the ``phase_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_id (str):
                Required. The job ID for the Job to
                ignore.

                This corresponds to the ``job_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.IgnoreJobResponse:
                The response object from IgnoreJob.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([rollout, phase_id, job_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloud_deploy.IgnoreJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.IgnoreJobRequest):
            request = cloud_deploy.IgnoreJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if rollout is not None:
                request.rollout = rollout
            if phase_id is not None:
                request.phase_id = phase_id
            if job_id is not None:
                request.job_id = job_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.ignore_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("rollout", request.rollout),)),
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

    def retry_job(
        self,
        request: Optional[Union[cloud_deploy.RetryJobRequest, dict]] = None,
        *,
        rollout: Optional[str] = None,
        phase_id: Optional[str] = None,
        job_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.RetryJobResponse:
        r"""Retries the specified Job in a Rollout.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_retry_job():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.RetryJobRequest(
                    rollout="rollout_value",
                    phase_id="phase_id_value",
                    job_id="job_id_value",
                )

                # Make the request
                response = client.retry_job(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.RetryJobRequest, dict]):
                The request object. RetryJobRequest is the request object used by
                ``RetryJob``.
            rollout (str):
                Required. Name of the Rollout. Format
                is
                projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
                releases/{release}/rollouts/{rollout}.

                This corresponds to the ``rollout`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            phase_id (str):
                Required. The phase ID the Job to
                retry belongs to.

                This corresponds to the ``phase_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_id (str):
                Required. The job ID for the Job to
                retry.

                This corresponds to the ``job_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.RetryJobResponse:
                The response object from 'RetryJob'.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([rollout, phase_id, job_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloud_deploy.RetryJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.RetryJobRequest):
            request = cloud_deploy.RetryJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if rollout is not None:
                request.rollout = rollout
            if phase_id is not None:
                request.phase_id = phase_id
            if job_id is not None:
                request.job_id = job_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.retry_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("rollout", request.rollout),)),
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

    def list_job_runs(
        self,
        request: Optional[Union[cloud_deploy.ListJobRunsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobRunsPager:
        r"""Lists JobRuns in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_list_job_runs():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ListJobRunsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_job_runs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ListJobRunsRequest, dict]):
                The request object. ListJobRunsRequest is the request object used by
                ``ListJobRuns``.
            parent (str):
                Required. The ``Rollout`` which owns this collection of
                ``JobRun`` objects.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.services.cloud_deploy.pagers.ListJobRunsPager:
                ListJobRunsResponse is the response object returned by
                ListJobRuns.

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
        # in a cloud_deploy.ListJobRunsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.ListJobRunsRequest):
            request = cloud_deploy.ListJobRunsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_job_runs]

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
        response = pagers.ListJobRunsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_job_run(
        self,
        request: Optional[Union[cloud_deploy.GetJobRunRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.JobRun:
        r"""Gets details of a single JobRun.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_get_job_run():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetJobRunRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_job_run(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetJobRunRequest, dict]):
                The request object. GetJobRunRequest is the request object used by
                ``GetJobRun``.
            name (str):
                Required. Name of the ``JobRun``. Format must be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}/rollouts/{rollout_name}/jobRuns/{job_run_name}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.JobRun:
                A JobRun resource in the Google Cloud Deploy API.

                   A JobRun contains information of a single Rollout job
                   evaluation.

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
        # in a cloud_deploy.GetJobRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.GetJobRunRequest):
            request = cloud_deploy.GetJobRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_job_run]

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

    def terminate_job_run(
        self,
        request: Optional[Union[cloud_deploy.TerminateJobRunRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.TerminateJobRunResponse:
        r"""Terminates a Job Run in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_terminate_job_run():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.TerminateJobRunRequest(
                    name="name_value",
                )

                # Make the request
                response = client.terminate_job_run(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.TerminateJobRunRequest, dict]):
                The request object. The request object used by ``TerminateJobRun``.
            name (str):
                Required. Name of the ``JobRun``. Format must be
                projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
                releases/{release}/rollouts/{rollout}/jobRuns/{jobRun}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.TerminateJobRunResponse:
                The response object from TerminateJobRun.
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
        # in a cloud_deploy.TerminateJobRunRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.TerminateJobRunRequest):
            request = cloud_deploy.TerminateJobRunRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.terminate_job_run]

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

    def get_config(
        self,
        request: Optional[Union[cloud_deploy.GetConfigRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.Config:
        r"""Gets the configuration for a location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import deploy_v1

            def sample_get_config():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetConfigRequest, dict]):
                The request object. Request to get a configuration.
            name (str):
                Required. Name of requested
                configuration.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.Config:
                Service-wide configuration.
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
        # in a cloud_deploy.GetConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloud_deploy.GetConfigRequest):
            request = cloud_deploy.GetConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_config]

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

    def __enter__(self) -> "CloudDeployClient":
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

    def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
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
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_operation,
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

    def set_iam_policy(
        self,
        request: Optional[iam_policy_pb2.SetIamPolicyRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the IAM access control policy on the specified function.

        Replaces any existing policy.

        Args:
            request (:class:`~.iam_policy_pb2.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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

    def get_iam_policy(
        self,
        request: Optional[iam_policy_pb2.GetIamPolicyRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM access control policy for a function.

        Returns an empty policy if the function exists and does not have a
        policy set.

        Args:
            request (:class:`~.iam_policy_pb2.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if
                any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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

    def test_iam_permissions(
        self,
        request: Optional[iam_policy_pb2.TestIamPermissionsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Tests the specified IAM permissions against the IAM access control
            policy for a function.

        If the function does not exist, this will return an empty set
        of permissions, not a NOT_FOUND error.

        Args:
            request (:class:`~.iam_policy_pb2.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for ``TestIamPermissions`` method.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.test_iam_permissions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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

    def get_location(
        self,
        request: Optional[locations_pb2.GetLocationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.Location:
                Location object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.GetLocationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_location,
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

    def list_locations(
        self,
        request: Optional[locations_pb2.ListLocationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.ListLocationsResponse:
                Response message for ``ListLocations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.ListLocationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_locations,
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


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("CloudDeployClient",)
