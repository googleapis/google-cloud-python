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
from typing import Dict, Optional, Sequence, Tuple, Type, Union
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

OptionalRetry = Union[retries.Retry, object]

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.devtools.cloudbuild_v1.services.cloud_build import pagers
from google.cloud.devtools.cloudbuild_v1.types import cloudbuild
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import CloudBuildTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import CloudBuildGrpcTransport
from .transports.grpc_asyncio import CloudBuildGrpcAsyncIOTransport


class CloudBuildClientMeta(type):
    """Metaclass for the CloudBuild client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[CloudBuildTransport]]
    _transport_registry["grpc"] = CloudBuildGrpcTransport
    _transport_registry["grpc_asyncio"] = CloudBuildGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[CloudBuildTransport]:
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


class CloudBuildClient(metaclass=CloudBuildClientMeta):
    """Creates and manages builds on Google Cloud Platform.

    The main concept used by this API is a ``Build``, which describes
    the location of the source to build, how to build the source, and
    where to store the built artifacts, if any.

    A user can list previously-requested builds or get builds by their
    ID to determine the status of the build.
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

    DEFAULT_ENDPOINT = "cloudbuild.googleapis.com"
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
            CloudBuildClient: The constructed client.
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
            CloudBuildClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudBuildTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudBuildTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def build_path(project: str, build: str,) -> str:
        """Returns a fully-qualified build string."""
        return "projects/{project}/builds/{build}".format(project=project, build=build,)

    @staticmethod
    def parse_build_path(path: str) -> Dict[str, str]:
        """Parses a build path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/builds/(?P<build>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def build_trigger_path(project: str, trigger: str,) -> str:
        """Returns a fully-qualified build_trigger string."""
        return "projects/{project}/triggers/{trigger}".format(
            project=project, trigger=trigger,
        )

    @staticmethod
    def parse_build_trigger_path(path: str) -> Dict[str, str]:
        """Parses a build_trigger path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/triggers/(?P<trigger>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def crypto_key_path(project: str, location: str, keyring: str, key: str,) -> str:
        """Returns a fully-qualified crypto_key string."""
        return "projects/{project}/locations/{location}/keyRings/{keyring}/cryptoKeys/{key}".format(
            project=project, location=location, keyring=keyring, key=key,
        )

    @staticmethod
    def parse_crypto_key_path(path: str) -> Dict[str, str]:
        """Parses a crypto_key path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/keyRings/(?P<keyring>.+?)/cryptoKeys/(?P<key>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def network_path(project: str, network: str,) -> str:
        """Returns a fully-qualified network string."""
        return "projects/{project}/global/networks/{network}".format(
            project=project, network=network,
        )

    @staticmethod
    def parse_network_path(path: str) -> Dict[str, str]:
        """Parses a network path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/global/networks/(?P<network>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def secret_version_path(project: str, secret: str, version: str,) -> str:
        """Returns a fully-qualified secret_version string."""
        return "projects/{project}/secrets/{secret}/versions/{version}".format(
            project=project, secret=secret, version=version,
        )

    @staticmethod
    def parse_secret_version_path(path: str) -> Dict[str, str]:
        """Parses a secret_version path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/secrets/(?P<secret>.+?)/versions/(?P<version>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def service_account_path(project: str, service_account: str,) -> str:
        """Returns a fully-qualified service_account string."""
        return "projects/{project}/serviceAccounts/{service_account}".format(
            project=project, service_account=service_account,
        )

    @staticmethod
    def parse_service_account_path(path: str) -> Dict[str, str]:
        """Parses a service_account path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/serviceAccounts/(?P<service_account>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def subscription_path(project: str, subscription: str,) -> str:
        """Returns a fully-qualified subscription string."""
        return "projects/{project}/subscriptions/{subscription}".format(
            project=project, subscription=subscription,
        )

    @staticmethod
    def parse_subscription_path(path: str) -> Dict[str, str]:
        """Parses a subscription path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/subscriptions/(?P<subscription>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def topic_path(project: str, topic: str,) -> str:
        """Returns a fully-qualified topic string."""
        return "projects/{project}/topics/{topic}".format(project=project, topic=topic,)

    @staticmethod
    def parse_topic_path(path: str) -> Dict[str, str]:
        """Parses a topic path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/topics/(?P<topic>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def worker_pool_path(project: str, location: str, worker_pool: str,) -> str:
        """Returns a fully-qualified worker_pool string."""
        return "projects/{project}/locations/{location}/workerPools/{worker_pool}".format(
            project=project, location=location, worker_pool=worker_pool,
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
        transport: Union[str, CloudBuildTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud build client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, CloudBuildTransport]): The
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
        if isinstance(transport, CloudBuildTransport):
            # transport is a CloudBuildTransport instance.
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
                always_use_jwt_access=True,
            )

    def create_build(
        self,
        request: Union[cloudbuild.CreateBuildRequest, dict] = None,
        *,
        project_id: str = None,
        build: cloudbuild.Build = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Starts a build with the specified configuration.

        This method returns a long-running ``Operation``, which includes
        the build ID. Pass the build ID to ``GetBuild`` to determine the
        build status (such as ``SUCCESS`` or ``FAILURE``).

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.CreateBuildRequest, dict]):
                The request object. Request to create a new build.
            project_id (str):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            build (google.cloud.devtools.cloudbuild_v1.types.Build):
                Required. Build resource to create.
                This corresponds to the ``build`` field
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
                :class:`google.cloud.devtools.cloudbuild_v1.types.Build`
                A build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, build])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.CreateBuildRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.CreateBuildRequest):
            request = cloudbuild.CreateBuildRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if build is not None:
                request.build = build

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_build]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_build(
        self,
        request: Union[cloudbuild.GetBuildRequest, dict] = None,
        *,
        project_id: str = None,
        id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.Build:
        r"""Returns information about a previously requested build.

        The ``Build`` that is returned includes its status (such as
        ``SUCCESS``, ``FAILURE``, or ``WORKING``), and timing
        information.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.GetBuildRequest, dict]):
                The request object. Request to get a build.
            project_id (str):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            id (str):
                Required. ID of the build.
                This corresponds to the ``id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.Build:
                A build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.GetBuildRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.GetBuildRequest):
            request = cloudbuild.GetBuildRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if id is not None:
                request.id = id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_build]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_builds(
        self,
        request: Union[cloudbuild.ListBuildsRequest, dict] = None,
        *,
        project_id: str = None,
        filter: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBuildsPager:
        r"""Lists previously requested builds.
        Previously requested builds may still be in-progress, or
        may have finished successfully or unsuccessfully.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.ListBuildsRequest, dict]):
                The request object. Request to list builds.
            project_id (str):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                The raw filter text to constrain the
                results.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.services.cloud_build.pagers.ListBuildsPager:
                Response including listed builds.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.ListBuildsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.ListBuildsRequest):
            request = cloudbuild.ListBuildsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_builds]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBuildsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def cancel_build(
        self,
        request: Union[cloudbuild.CancelBuildRequest, dict] = None,
        *,
        project_id: str = None,
        id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.Build:
        r"""Cancels a build in progress.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.CancelBuildRequest, dict]):
                The request object. Request to cancel an ongoing build.
            project_id (str):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            id (str):
                Required. ID of the build.
                This corresponds to the ``id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.Build:
                A build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.CancelBuildRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.CancelBuildRequest):
            request = cloudbuild.CancelBuildRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if id is not None:
                request.id = id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_build]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def retry_build(
        self,
        request: Union[cloudbuild.RetryBuildRequest, dict] = None,
        *,
        project_id: str = None,
        id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new build based on the specified build.

        This method creates a new build using the original build
        request, which may or may not result in an identical build.

        For triggered builds:

        -  Triggered builds resolve to a precise revision; therefore a
           retry of a triggered build will result in a build that uses
           the same revision.

        For non-triggered builds that specify ``RepoSource``:

        -  If the original build built from the tip of a branch, the
           retried build will build from the tip of that branch, which
           may not be the same revision as the original build.
        -  If the original build specified a commit sha or revision ID,
           the retried build will use the identical source.

        For builds that specify ``StorageSource``:

        -  If the original build pulled source from Google Cloud Storage
           without specifying the generation of the object, the new
           build will use the current object, which may be different
           from the original build source.
        -  If the original build pulled source from Cloud Storage and
           specified the generation of the object, the new build will
           attempt to use the same object, which may or may not be
           available depending on the bucket's lifecycle management
           settings.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.RetryBuildRequest, dict]):
                The request object. Specifies a build to retry.
            project_id (str):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            id (str):
                Required. Build ID of the original
                build.

                This corresponds to the ``id`` field
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
                :class:`google.cloud.devtools.cloudbuild_v1.types.Build`
                A build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.RetryBuildRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.RetryBuildRequest):
            request = cloudbuild.RetryBuildRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if id is not None:
                request.id = id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.retry_build]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    def approve_build(
        self,
        request: Union[cloudbuild.ApproveBuildRequest, dict] = None,
        *,
        name: str = None,
        approval_result: cloudbuild.ApprovalResult = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Approves or rejects a pending build.
        If approved, the returned LRO will be analogous to the
        LRO returned from a CreateBuild call.

        If rejected, the returned LRO will be immediately done.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.ApproveBuildRequest, dict]):
                The request object. Request to approve or reject a
                pending build.
            name (str):
                Required. Name of the target build. For example:
                "projects/{$project_id}/builds/{$build_id}"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            approval_result (google.cloud.devtools.cloudbuild_v1.types.ApprovalResult):
                Approval decision and metadata.
                This corresponds to the ``approval_result`` field
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
                :class:`google.cloud.devtools.cloudbuild_v1.types.Build`
                A build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, approval_result])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.ApproveBuildRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.ApproveBuildRequest):
            request = cloudbuild.ApproveBuildRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if approval_result is not None:
                request.approval_result = approval_result

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.approve_build]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    def create_build_trigger(
        self,
        request: Union[cloudbuild.CreateBuildTriggerRequest, dict] = None,
        *,
        project_id: str = None,
        trigger: cloudbuild.BuildTrigger = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.BuildTrigger:
        r"""Creates a new ``BuildTrigger``.

        This API is experimental.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.CreateBuildTriggerRequest, dict]):
                The request object. Request to create a new
                `BuildTrigger`.
            project_id (str):
                Required. ID of the project for which
                to configure automatic builds.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger (google.cloud.devtools.cloudbuild_v1.types.BuildTrigger):
                Required. ``BuildTrigger`` to create.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.BuildTrigger:
                Configuration for an automated build
                in response to source repository
                changes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trigger])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.CreateBuildTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.CreateBuildTriggerRequest):
            request = cloudbuild.CreateBuildTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if trigger is not None:
                request.trigger = trigger

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_build_trigger]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_build_trigger(
        self,
        request: Union[cloudbuild.GetBuildTriggerRequest, dict] = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.BuildTrigger:
        r"""Returns information about a ``BuildTrigger``.

        This API is experimental.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.GetBuildTriggerRequest, dict]):
                The request object. Returns the `BuildTrigger` with the
                specified ID.
            project_id (str):
                Required. ID of the project that owns
                the trigger.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (str):
                Required. Identifier (``id`` or ``name``) of the
                ``BuildTrigger`` to get.

                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.BuildTrigger:
                Configuration for an automated build
                in response to source repository
                changes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trigger_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.GetBuildTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.GetBuildTriggerRequest):
            request = cloudbuild.GetBuildTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if trigger_id is not None:
                request.trigger_id = trigger_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_build_trigger]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_build_triggers(
        self,
        request: Union[cloudbuild.ListBuildTriggersRequest, dict] = None,
        *,
        project_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBuildTriggersPager:
        r"""Lists existing ``BuildTrigger``\ s.

        This API is experimental.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.ListBuildTriggersRequest, dict]):
                The request object. Request to list existing
                `BuildTriggers`.
            project_id (str):
                Required. ID of the project for which
                to list BuildTriggers.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.services.cloud_build.pagers.ListBuildTriggersPager:
                Response containing existing BuildTriggers.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.ListBuildTriggersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.ListBuildTriggersRequest):
            request = cloudbuild.ListBuildTriggersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_build_triggers]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBuildTriggersPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_build_trigger(
        self,
        request: Union[cloudbuild.DeleteBuildTriggerRequest, dict] = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.DeleteBuildTriggerRequest, dict]):
                The request object. Request to delete a `BuildTrigger`.
            project_id (str):
                Required. ID of the project that owns
                the trigger.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (str):
                Required. ID of the ``BuildTrigger`` to delete.
                This corresponds to the ``trigger_id`` field
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
        has_flattened_params = any([project_id, trigger_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.DeleteBuildTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.DeleteBuildTriggerRequest):
            request = cloudbuild.DeleteBuildTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if trigger_id is not None:
                request.trigger_id = trigger_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_build_trigger]

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def update_build_trigger(
        self,
        request: Union[cloudbuild.UpdateBuildTriggerRequest, dict] = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        trigger: cloudbuild.BuildTrigger = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.BuildTrigger:
        r"""Updates a ``BuildTrigger`` by its project ID and trigger ID.

        This API is experimental.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.UpdateBuildTriggerRequest, dict]):
                The request object. Request to update an existing
                `BuildTrigger`.
            project_id (str):
                Required. ID of the project that owns
                the trigger.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (str):
                Required. ID of the ``BuildTrigger`` to update.
                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger (google.cloud.devtools.cloudbuild_v1.types.BuildTrigger):
                Required. ``BuildTrigger`` to update.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.BuildTrigger:
                Configuration for an automated build
                in response to source repository
                changes.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trigger_id, trigger])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.UpdateBuildTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.UpdateBuildTriggerRequest):
            request = cloudbuild.UpdateBuildTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if trigger_id is not None:
                request.trigger_id = trigger_id
            if trigger is not None:
                request.trigger = trigger

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_build_trigger]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def run_build_trigger(
        self,
        request: Union[cloudbuild.RunBuildTriggerRequest, dict] = None,
        *,
        project_id: str = None,
        trigger_id: str = None,
        source: cloudbuild.RepoSource = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Runs a ``BuildTrigger`` at a particular source revision.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.RunBuildTriggerRequest, dict]):
                The request object. Specifies a build trigger to run and
                the source to use.
            project_id (str):
                Required. ID of the project.
                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (str):
                Required. ID of the trigger.
                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source (google.cloud.devtools.cloudbuild_v1.types.RepoSource):
                Source to build against this trigger.
                This corresponds to the ``source`` field
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
                :class:`google.cloud.devtools.cloudbuild_v1.types.Build`
                A build resource in the Cloud Build API.

                   At a high level, a Build describes where to find
                   source code, how to build it (for example, the
                   builder image to run on the source), and where to
                   store the built artifacts.

                   Fields can include the following variables, which
                   will be expanded when the build is created:

                   -  $PROJECT_ID: the project ID of the build.
                   -  $PROJECT_NUMBER: the project number of the build.
                   -  $BUILD_ID: the autogenerated ID of the build.
                   -  $REPO_NAME: the source repository name specified
                      by RepoSource.
                   -  $BRANCH_NAME: the branch name specified by
                      RepoSource.
                   -  $TAG_NAME: the tag name specified by RepoSource.
                   -  $REVISION_ID or $COMMIT_SHA: the commit SHA
                      specified by RepoSource or resolved from the
                      specified branch or tag.
                   -  $SHORT_SHA: first 7 characters of $REVISION_ID or
                      $COMMIT_SHA.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, trigger_id, source])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.RunBuildTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.RunBuildTriggerRequest):
            request = cloudbuild.RunBuildTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if trigger_id is not None:
                request.trigger_id = trigger_id
            if source is not None:
                request.source = source

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_build_trigger]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloudbuild.Build,
            metadata_type=cloudbuild.BuildOperationMetadata,
        )

        # Done; return the response.
        return response

    def receive_trigger_webhook(
        self,
        request: Union[cloudbuild.ReceiveTriggerWebhookRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.ReceiveTriggerWebhookResponse:
        r"""ReceiveTriggerWebhook [Experimental] is called when the API
        receives a webhook request targeted at a specific trigger.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.ReceiveTriggerWebhookRequest, dict]):
                The request object. ReceiveTriggerWebhookRequest
                [Experimental] is the request object accepted by the
                ReceiveTriggerWebhook method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.ReceiveTriggerWebhookResponse:
                ReceiveTriggerWebhookResponse [Experimental] is the response object for the
                   ReceiveTriggerWebhook method.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.ReceiveTriggerWebhookRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.ReceiveTriggerWebhookRequest):
            request = cloudbuild.ReceiveTriggerWebhookRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.receive_trigger_webhook]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_worker_pool(
        self,
        request: Union[cloudbuild.CreateWorkerPoolRequest, dict] = None,
        *,
        parent: str = None,
        worker_pool: cloudbuild.WorkerPool = None,
        worker_pool_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a ``WorkerPool``.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.CreateWorkerPoolRequest, dict]):
                The request object. Request to create a new
                `WorkerPool`.
            parent (str):
                Required. The parent resource where this worker pool
                will be created. Format:
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            worker_pool (google.cloud.devtools.cloudbuild_v1.types.WorkerPool):
                Required. ``WorkerPool`` resource to create.
                This corresponds to the ``worker_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            worker_pool_id (str):
                Required. Immutable. The ID to use for the
                ``WorkerPool``, which will become the final component of
                the resource name.

                This value should be 1-63 characters, and valid
                characters are /[a-z][0-9]-/.

                This corresponds to the ``worker_pool_id`` field
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
                :class:`google.cloud.devtools.cloudbuild_v1.types.WorkerPool`
                Configuration for a WorkerPool.

                   Cloud Build owns and maintains a pool of workers for
                   general use and have no access to a project's private
                   network. By default, builds submitted to Cloud Build
                   will use a worker from this pool.

                   If your build needs access to resources on a private
                   network, create and use a WorkerPool to run your
                   builds. Private WorkerPools give your builds access
                   to any single VPC network that you administer,
                   including any on-prem resources connected to that VPC
                   network. For an overview of private pools, see
                   [Private pools
                   overview](\ https://cloud.google.com/build/docs/private-pools/private-pools-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, worker_pool, worker_pool_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.CreateWorkerPoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.CreateWorkerPoolRequest):
            request = cloudbuild.CreateWorkerPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if worker_pool is not None:
                request.worker_pool = worker_pool
            if worker_pool_id is not None:
                request.worker_pool_id = worker_pool_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_worker_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloudbuild.WorkerPool,
            metadata_type=cloudbuild.CreateWorkerPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_worker_pool(
        self,
        request: Union[cloudbuild.GetWorkerPoolRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloudbuild.WorkerPool:
        r"""Returns details of a ``WorkerPool``.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.GetWorkerPoolRequest, dict]):
                The request object. Request to get a `WorkerPool` with
                the specified name.
            name (str):
                Required. The name of the ``WorkerPool`` to retrieve.
                Format:
                ``projects/{project}/locations/{location}/workerPools/{workerPool}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.types.WorkerPool:
                Configuration for a WorkerPool.

                   Cloud Build owns and maintains a pool of workers for
                   general use and have no access to a project's private
                   network. By default, builds submitted to Cloud Build
                   will use a worker from this pool.

                   If your build needs access to resources on a private
                   network, create and use a WorkerPool to run your
                   builds. Private WorkerPools give your builds access
                   to any single VPC network that you administer,
                   including any on-prem resources connected to that VPC
                   network. For an overview of private pools, see
                   [Private pools
                   overview](\ https://cloud.google.com/build/docs/private-pools/private-pools-overview).

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
        # in a cloudbuild.GetWorkerPoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.GetWorkerPoolRequest):
            request = cloudbuild.GetWorkerPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_worker_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_worker_pool(
        self,
        request: Union[cloudbuild.DeleteWorkerPoolRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a ``WorkerPool``.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.DeleteWorkerPoolRequest, dict]):
                The request object. Request to delete a `WorkerPool`.
            name (str):
                Required. The name of the ``WorkerPool`` to delete.
                Format:
                ``projects/{project}/locations/{workerPool}/workerPools/{workerPool}``.

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

                   The JSON representation for Empty is empty JSON
                   object {}.

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
        # in a cloudbuild.DeleteWorkerPoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.DeleteWorkerPoolRequest):
            request = cloudbuild.DeleteWorkerPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_worker_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=cloudbuild.DeleteWorkerPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    def update_worker_pool(
        self,
        request: Union[cloudbuild.UpdateWorkerPoolRequest, dict] = None,
        *,
        worker_pool: cloudbuild.WorkerPool = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates a ``WorkerPool``.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.UpdateWorkerPoolRequest, dict]):
                The request object. Request to update a `WorkerPool`.
            worker_pool (google.cloud.devtools.cloudbuild_v1.types.WorkerPool):
                Required. The ``WorkerPool`` to update.

                The ``name`` field is used to identify the
                ``WorkerPool`` to update. Format:
                ``projects/{project}/locations/{location}/workerPools/{workerPool}``.

                This corresponds to the ``worker_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                A mask specifying which fields in ``worker_pool`` to
                update.

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
                :class:`google.cloud.devtools.cloudbuild_v1.types.WorkerPool`
                Configuration for a WorkerPool.

                   Cloud Build owns and maintains a pool of workers for
                   general use and have no access to a project's private
                   network. By default, builds submitted to Cloud Build
                   will use a worker from this pool.

                   If your build needs access to resources on a private
                   network, create and use a WorkerPool to run your
                   builds. Private WorkerPools give your builds access
                   to any single VPC network that you administer,
                   including any on-prem resources connected to that VPC
                   network. For an overview of private pools, see
                   [Private pools
                   overview](\ https://cloud.google.com/build/docs/private-pools/private-pools-overview).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([worker_pool, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudbuild.UpdateWorkerPoolRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.UpdateWorkerPoolRequest):
            request = cloudbuild.UpdateWorkerPoolRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if worker_pool is not None:
                request.worker_pool = worker_pool
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_worker_pool]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("worker_pool.name", request.worker_pool.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            cloudbuild.WorkerPool,
            metadata_type=cloudbuild.UpdateWorkerPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    def list_worker_pools(
        self,
        request: Union[cloudbuild.ListWorkerPoolsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWorkerPoolsPager:
        r"""Lists ``WorkerPool``\ s.

        Args:
            request (Union[google.cloud.devtools.cloudbuild_v1.types.ListWorkerPoolsRequest, dict]):
                The request object. Request to list `WorkerPool`\s.
            parent (str):
                Required. The parent of the collection of
                ``WorkerPools``. Format:
                ``projects/{project}/locations/{location}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.devtools.cloudbuild_v1.services.cloud_build.pagers.ListWorkerPoolsPager:
                Response containing existing WorkerPools.

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
        # in a cloudbuild.ListWorkerPoolsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudbuild.ListWorkerPoolsRequest):
            request = cloudbuild.ListWorkerPoolsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_worker_pools]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListWorkerPoolsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-build",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudBuildClient",)
