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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.metastore_v1alpha.services.dataproc_metastore import pagers
from google.cloud.metastore_v1alpha.types import metastore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import DataprocMetastoreTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import DataprocMetastoreGrpcTransport
from .transports.grpc_asyncio import DataprocMetastoreGrpcAsyncIOTransport


class DataprocMetastoreClientMeta(type):
    """Metaclass for the DataprocMetastore client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[DataprocMetastoreTransport]]
    _transport_registry["grpc"] = DataprocMetastoreGrpcTransport
    _transport_registry["grpc_asyncio"] = DataprocMetastoreGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[DataprocMetastoreTransport]:
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


class DataprocMetastoreClient(metaclass=DataprocMetastoreClientMeta):
    """Configures and manages metastore services. Metastore services are
    fully managed, highly available, auto-scaled, auto-healing,
    OSS-native deployments of technical metadata management software.
    Each metastore service exposes a network endpoint through which
    metadata queries are served. Metadata queries can originate from a
    variety of sources, including Apache Hive, Apache Presto, and Apache
    Spark.

    The Dataproc Metastore API defines the following resource model:

    -  The service works with a collection of Google Cloud projects,
       named: ``/projects/*``

    -  Each project has a collection of available locations, named:
       ``/locations/*`` (a location must refer to a Google Cloud
       ``region``)

    -  Each location has a collection of services, named:
       ``/services/*``

    -  Dataproc Metastore services are resources with names of the form:

       ``/projects/{project_number}/locations/{location_id}/services/{service_id}``.
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

    DEFAULT_ENDPOINT = "metastore.googleapis.com"
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
            DataprocMetastoreClient: The constructed client.
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
            DataprocMetastoreClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DataprocMetastoreTransport:
        """Returns the transport used by the client instance.

        Returns:
            DataprocMetastoreTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def backup_path(project: str, location: str, service: str, backup: str,) -> str:
        """Returns a fully-qualified backup string."""
        return "projects/{project}/locations/{location}/services/{service}/backups/{backup}".format(
            project=project, location=location, service=service, backup=backup,
        )

    @staticmethod
    def parse_backup_path(path: str) -> Dict[str, str]:
        """Parses a backup path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/services/(?P<service>.+?)/backups/(?P<backup>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def metadata_import_path(
        project: str, location: str, service: str, metadata_import: str,
    ) -> str:
        """Returns a fully-qualified metadata_import string."""
        return "projects/{project}/locations/{location}/services/{service}/metadataImports/{metadata_import}".format(
            project=project,
            location=location,
            service=service,
            metadata_import=metadata_import,
        )

    @staticmethod
    def parse_metadata_import_path(path: str) -> Dict[str, str]:
        """Parses a metadata_import path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/services/(?P<service>.+?)/metadataImports/(?P<metadata_import>.+?)$",
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
    def service_path(project: str, location: str, service: str,) -> str:
        """Returns a fully-qualified service string."""
        return "projects/{project}/locations/{location}/services/{service}".format(
            project=project, location=location, service=service,
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
        transport: Union[str, DataprocMetastoreTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the dataproc metastore client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DataprocMetastoreTransport]): The
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
        if isinstance(transport, DataprocMetastoreTransport):
            # transport is a DataprocMetastoreTransport instance.
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

    def list_services(
        self,
        request: metastore.ListServicesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServicesPager:
        r"""Lists services in a project and location.

        Args:
            request (google.cloud.metastore_v1alpha.types.ListServicesRequest):
                The request object. Request message for
                [DataprocMetastore.ListServices][google.cloud.metastore.v1alpha.DataprocMetastore.ListServices].
            parent (str):
                Required. The relative resource name of the location of
                metastore services to list, in the following form:

                ``projects/{project_number}/locations/{location_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1alpha.services.dataproc_metastore.pagers.ListServicesPager:
                Response message for
                [DataprocMetastore.ListServices][google.cloud.metastore.v1alpha.DataprocMetastore.ListServices].

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
        # in a metastore.ListServicesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.ListServicesRequest):
            request = metastore.ListServicesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_services]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListServicesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_service(
        self,
        request: metastore.GetServiceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metastore.Service:
        r"""Gets the details of a single service.

        Args:
            request (google.cloud.metastore_v1alpha.types.GetServiceRequest):
                The request object. Request message for
                [DataprocMetastore.GetService][google.cloud.metastore.v1alpha.DataprocMetastore.GetService].
            name (str):
                Required. The relative resource name of the metastore
                service to retrieve, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1alpha.types.Service:
                A managed metastore service that
                serves metadata queries.

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
        # in a metastore.GetServiceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.GetServiceRequest):
            request = metastore.GetServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_service]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_service(
        self,
        request: metastore.CreateServiceRequest = None,
        *,
        parent: str = None,
        service: metastore.Service = None,
        service_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a metastore service in a project and
        location.

        Args:
            request (google.cloud.metastore_v1alpha.types.CreateServiceRequest):
                The request object. Request message for
                [DataprocMetastore.CreateService][google.cloud.metastore.v1alpha.DataprocMetastore.CreateService].
            parent (str):
                Required. The relative resource name of the location in
                which to create a metastore service, in the following
                form:

                ``projects/{project_number}/locations/{location_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service (google.cloud.metastore_v1alpha.types.Service):
                Required. The Metastore service to create. The ``name``
                field is ignored. The ID of the created metastore
                service must be provided in the request's ``service_id``
                field.

                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service_id (str):
                Required. The ID of the metastore
                service, which is used as the final
                component of the metastore service's
                name.
                This value must be between 2 and 63
                characters long inclusive, begin with a
                letter, end with a letter or number, and
                consist of alpha-numeric ASCII
                characters or hyphens.

                This corresponds to the ``service_id`` field
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
                :class:`google.cloud.metastore_v1alpha.types.Service` A
                managed metastore service that serves metadata queries.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, service, service_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metastore.CreateServiceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.CreateServiceRequest):
            request = metastore.CreateServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if service is not None:
                request.service = service
            if service_id is not None:
                request.service_id = service_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_service]

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
            metastore.Service,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_service(
        self,
        request: metastore.UpdateServiceRequest = None,
        *,
        service: metastore.Service = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the parameters of a single service.

        Args:
            request (google.cloud.metastore_v1alpha.types.UpdateServiceRequest):
                The request object. Request message for
                [DataprocMetastore.UpdateService][google.cloud.metastore.v1alpha.DataprocMetastore.UpdateService].
            service (google.cloud.metastore_v1alpha.types.Service):
                Required. The metastore service to update. The server
                only merges fields in the service if they are specified
                in ``update_mask``.

                The metastore service's ``name`` field is used to
                identify the metastore service to be updated.

                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. A field mask used to specify the fields to be
                overwritten in the metastore service resource by the
                update. Fields specified in the ``update_mask`` are
                relative to the resource (not to the full request). A
                field is overwritten if it is in the mask.

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
                :class:`google.cloud.metastore_v1alpha.types.Service` A
                managed metastore service that serves metadata queries.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metastore.UpdateServiceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.UpdateServiceRequest):
            request = metastore.UpdateServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service is not None:
                request.service = service
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_service]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("service.name", request.service.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            metastore.Service,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_service(
        self,
        request: metastore.DeleteServiceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single service.

        Args:
            request (google.cloud.metastore_v1alpha.types.DeleteServiceRequest):
                The request object. Request message for
                [DataprocMetastore.DeleteService][google.cloud.metastore.v1alpha.DataprocMetastore.DeleteService].
            name (str):
                Required. The relative resource name of the metastore
                service to delete, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}``.

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
        # in a metastore.DeleteServiceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.DeleteServiceRequest):
            request = metastore.DeleteServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_service]

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
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_metadata_imports(
        self,
        request: metastore.ListMetadataImportsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMetadataImportsPager:
        r"""Lists imports in a service.

        Args:
            request (google.cloud.metastore_v1alpha.types.ListMetadataImportsRequest):
                The request object. Request message for
                [DataprocMetastore.ListMetadataImports][google.cloud.metastore.v1alpha.DataprocMetastore.ListMetadataImports].
            parent (str):
                Required. The relative resource name of the service
                whose metadata imports to list, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}/metadataImports``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1alpha.services.dataproc_metastore.pagers.ListMetadataImportsPager:
                Response message for
                [DataprocMetastore.ListMetadataImports][google.cloud.metastore.v1alpha.DataprocMetastore.ListMetadataImports].

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
        # in a metastore.ListMetadataImportsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.ListMetadataImportsRequest):
            request = metastore.ListMetadataImportsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_metadata_imports]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListMetadataImportsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_metadata_import(
        self,
        request: metastore.GetMetadataImportRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metastore.MetadataImport:
        r"""Gets details of a single import.

        Args:
            request (google.cloud.metastore_v1alpha.types.GetMetadataImportRequest):
                The request object. Request message for
                [DataprocMetastore.GetMetadataImport][google.cloud.metastore.v1alpha.DataprocMetastore.GetMetadataImport].
            name (str):
                Required. The relative resource name of the metadata
                import to retrieve, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}/metadataImports/{import_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1alpha.types.MetadataImport:
                A metastore resource that imports
                metadata.

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
        # in a metastore.GetMetadataImportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.GetMetadataImportRequest):
            request = metastore.GetMetadataImportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_metadata_import]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_metadata_import(
        self,
        request: metastore.CreateMetadataImportRequest = None,
        *,
        parent: str = None,
        metadata_import: metastore.MetadataImport = None,
        metadata_import_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new MetadataImport in a given project and
        location.

        Args:
            request (google.cloud.metastore_v1alpha.types.CreateMetadataImportRequest):
                The request object. Request message for
                [DataprocMetastore.CreateMetadataImport][google.cloud.metastore.v1alpha.DataprocMetastore.CreateMetadataImport].
            parent (str):
                Required. The relative resource name of the service in
                which to create a metastore import, in the following
                form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_import (google.cloud.metastore_v1alpha.types.MetadataImport):
                Required. The metadata import to create. The ``name``
                field is ignored. The ID of the created metadata import
                must be provided in the request's ``metadata_import_id``
                field.

                This corresponds to the ``metadata_import`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_import_id (str):
                Required. The ID of the metadata
                import, which is used as the final
                component of the metadata import's name.
                This value must be between 1 and 64
                characters long, begin with a letter,
                end with a letter or number, and consist
                of alpha-numeric ASCII characters or
                hyphens.

                This corresponds to the ``metadata_import_id`` field
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
                :class:`google.cloud.metastore_v1alpha.types.MetadataImport`
                A metastore resource that imports metadata.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, metadata_import, metadata_import_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metastore.CreateMetadataImportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.CreateMetadataImportRequest):
            request = metastore.CreateMetadataImportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if metadata_import is not None:
                request.metadata_import = metadata_import
            if metadata_import_id is not None:
                request.metadata_import_id = metadata_import_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_metadata_import]

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
            metastore.MetadataImport,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_metadata_import(
        self,
        request: metastore.UpdateMetadataImportRequest = None,
        *,
        metadata_import: metastore.MetadataImport = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates a single import.
        Only the description field of MetadataImport is
        supported to be updated.

        Args:
            request (google.cloud.metastore_v1alpha.types.UpdateMetadataImportRequest):
                The request object. Request message for
                [DataprocMetastore.UpdateMetadataImport][google.cloud.metastore.v1alpha.DataprocMetastore.UpdateMetadataImport].
            metadata_import (google.cloud.metastore_v1alpha.types.MetadataImport):
                Required. The metadata import to update. The server only
                merges fields in the import if they are specified in
                ``update_mask``.

                The metadata import's ``name`` field is used to identify
                the metastore import to be updated.

                This corresponds to the ``metadata_import`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. A field mask used to specify the fields to be
                overwritten in the metadata import resource by the
                update. Fields specified in the ``update_mask`` are
                relative to the resource (not to the full request). A
                field is overwritten if it is in the mask.

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
                :class:`google.cloud.metastore_v1alpha.types.MetadataImport`
                A metastore resource that imports metadata.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([metadata_import, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metastore.UpdateMetadataImportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.UpdateMetadataImportRequest):
            request = metastore.UpdateMetadataImportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if metadata_import is not None:
                request.metadata_import = metadata_import
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_metadata_import]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("metadata_import.name", request.metadata_import.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            metastore.MetadataImport,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    def export_metadata(
        self,
        request: metastore.ExportMetadataRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Exports metadata from a service.

        Args:
            request (google.cloud.metastore_v1alpha.types.ExportMetadataRequest):
                The request object. Request message for
                [DataprocMetastore.ExportMetadata][google.cloud.metastore.v1alpha.DataprocMetastore.ExportMetadata].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.metastore_v1alpha.types.MetadataExport`
                The details of a metadata export operation.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a metastore.ExportMetadataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.ExportMetadataRequest):
            request = metastore.ExportMetadataRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.export_metadata]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("service", request.service),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            metastore.MetadataExport,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    def restore_service(
        self,
        request: metastore.RestoreServiceRequest = None,
        *,
        service: str = None,
        backup: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Restores a service from a backup.

        Args:
            request (google.cloud.metastore_v1alpha.types.RestoreServiceRequest):
                The request object. Request message for
                [DataprocMetastore.Restore][].
            service (str):
                Required. The relative resource name of the metastore
                service to run restore, in the following form:

                ``projects/{project_id}/locations/{location_id}/services/{service_id}``

                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup (str):
                Required. The relative resource name of the metastore
                service backup to restore from, in the following form:

                ``projects/{project_id}/locations/{location_id}/services/{service_id}/backups/{backup_id}``

                This corresponds to the ``backup`` field
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
                :class:`google.cloud.metastore_v1alpha.types.Restore`
                The details of a metadata restore operation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service, backup])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metastore.RestoreServiceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.RestoreServiceRequest):
            request = metastore.RestoreServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service is not None:
                request.service = service
            if backup is not None:
                request.backup = backup

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.restore_service]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("service", request.service),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            metastore.Restore,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_backups(
        self,
        request: metastore.ListBackupsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupsPager:
        r"""Lists backups in a service.

        Args:
            request (google.cloud.metastore_v1alpha.types.ListBackupsRequest):
                The request object. Request message for
                [DataprocMetastore.ListBackups][google.cloud.metastore.v1alpha.DataprocMetastore.ListBackups].
            parent (str):
                Required. The relative resource name of the service
                whose backups to list, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}/backups``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1alpha.services.dataproc_metastore.pagers.ListBackupsPager:
                Response message for
                [DataprocMetastore.ListBackups][google.cloud.metastore.v1alpha.DataprocMetastore.ListBackups].

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
        # in a metastore.ListBackupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.ListBackupsRequest):
            request = metastore.ListBackupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_backups]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBackupsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_backup(
        self,
        request: metastore.GetBackupRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metastore.Backup:
        r"""Gets details of a single backup.

        Args:
            request (google.cloud.metastore_v1alpha.types.GetBackupRequest):
                The request object. Request message for
                [DataprocMetastore.GetBackup][google.cloud.metastore.v1alpha.DataprocMetastore.GetBackup].
            name (str):
                Required. The relative resource name of the backup to
                retrieve, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}/backups/{backup_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1alpha.types.Backup:
                The details of a backup resource.
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
        # in a metastore.GetBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.GetBackupRequest):
            request = metastore.GetBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_backup(
        self,
        request: metastore.CreateBackupRequest = None,
        *,
        parent: str = None,
        backup: metastore.Backup = None,
        backup_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new Backup in a given project and location.

        Args:
            request (google.cloud.metastore_v1alpha.types.CreateBackupRequest):
                The request object. Request message for
                [DataprocMetastore.CreateBackup][google.cloud.metastore.v1alpha.DataprocMetastore.CreateBackup].
            parent (str):
                Required. The relative resource name of the service in
                which to create a backup of the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup (google.cloud.metastore_v1alpha.types.Backup):
                Required. The backup to create. The ``name`` field is
                ignored. The ID of the created backup must be provided
                in the request's ``backup_id`` field.

                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_id (str):
                Required. The ID of the backup, which
                is used as the final component of the
                backup's name.
                This value must be between 1 and 64
                characters long, begin with a letter,
                end with a letter or number, and consist
                of alpha-numeric ASCII characters or
                hyphens.

                This corresponds to the ``backup_id`` field
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
                :class:`google.cloud.metastore_v1alpha.types.Backup` The
                details of a backup resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, backup, backup_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a metastore.CreateBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.CreateBackupRequest):
            request = metastore.CreateBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if backup is not None:
                request.backup = backup
            if backup_id is not None:
                request.backup_id = backup_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_backup]

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
            metastore.Backup,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_backup(
        self,
        request: metastore.DeleteBackupRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single backup.

        Args:
            request (google.cloud.metastore_v1alpha.types.DeleteBackupRequest):
                The request object. Request message for
                [DataprocMetastore.DeleteBackup][google.cloud.metastore.v1alpha.DataprocMetastore.DeleteBackup].
            name (str):
                Required. The relative resource name of the backup to
                delete, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}/backups/{backup_id}``.

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
        # in a metastore.DeleteBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, metastore.DeleteBackupRequest):
            request = metastore.DeleteBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_backup]

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
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-metastore",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DataprocMetastoreClient",)
