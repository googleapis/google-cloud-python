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

from google.cloud.bigquery_datapolicies_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore

from google.cloud.bigquery_datapolicies_v1.services.data_policy_service import pagers
from google.cloud.bigquery_datapolicies_v1.types import datapolicy

from .transports.base import DEFAULT_CLIENT_INFO, DataPolicyServiceTransport
from .transports.grpc import DataPolicyServiceGrpcTransport
from .transports.grpc_asyncio import DataPolicyServiceGrpcAsyncIOTransport
from .transports.rest import DataPolicyServiceRestTransport


class DataPolicyServiceClientMeta(type):
    """Metaclass for the DataPolicyService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[DataPolicyServiceTransport]]
    _transport_registry["grpc"] = DataPolicyServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = DataPolicyServiceGrpcAsyncIOTransport
    _transport_registry["rest"] = DataPolicyServiceRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[DataPolicyServiceTransport]:
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


class DataPolicyServiceClient(metaclass=DataPolicyServiceClientMeta):
    """Data Policy Service provides APIs for managing the
    label-policy bindings.
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

    DEFAULT_ENDPOINT = "bigquerydatapolicy.googleapis.com"
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
            DataPolicyServiceClient: The constructed client.
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
            DataPolicyServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DataPolicyServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            DataPolicyServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def data_policy_path(
        project: str,
        location: str,
        data_policy: str,
    ) -> str:
        """Returns a fully-qualified data_policy string."""
        return (
            "projects/{project}/locations/{location}/dataPolicies/{data_policy}".format(
                project=project,
                location=location,
                data_policy=data_policy,
            )
        )

    @staticmethod
    def parse_data_policy_path(path: str) -> Dict[str, str]:
        """Parses a data_policy path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/dataPolicies/(?P<data_policy>.+?)$",
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
        transport: Optional[Union[str, DataPolicyServiceTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the data policy service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DataPolicyServiceTransport]): The
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
        if isinstance(transport, DataPolicyServiceTransport):
            # transport is a DataPolicyServiceTransport instance.
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

    def create_data_policy(
        self,
        request: Optional[Union[datapolicy.CreateDataPolicyRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        data_policy: Optional[datapolicy.DataPolicy] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datapolicy.DataPolicy:
        r"""Creates a new data policy under a project with the given
        ``dataPolicyId`` (used as the display name), policy tag, and
        data policy type.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import bigquery_datapolicies_v1

            def sample_create_data_policy():
                # Create a client
                client = bigquery_datapolicies_v1.DataPolicyServiceClient()

                # Initialize request argument(s)
                data_policy = bigquery_datapolicies_v1.DataPolicy()
                data_policy.policy_tag = "policy_tag_value"
                data_policy.data_masking_policy.predefined_expression = "DEFAULT_MASKING_VALUE"

                request = bigquery_datapolicies_v1.CreateDataPolicyRequest(
                    parent="parent_value",
                    data_policy=data_policy,
                )

                # Make the request
                response = client.create_data_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_datapolicies_v1.types.CreateDataPolicyRequest, dict]):
                The request object. Request message for the
                CreateDataPolicy method.
            parent (str):
                Required. Resource name of the project that the data
                policy will belong to. The format is
                ``projects/{project_number}/locations/{location_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            data_policy (google.cloud.bigquery_datapolicies_v1.types.DataPolicy):
                Required. The data policy to create. The ``name`` field
                does not need to be provided for the data policy
                creation.

                This corresponds to the ``data_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datapolicies_v1.types.DataPolicy:
                Represents the label-policy binding.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, data_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datapolicy.CreateDataPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datapolicy.CreateDataPolicyRequest):
            request = datapolicy.CreateDataPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if data_policy is not None:
                request.data_policy = data_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_data_policy]

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

    def update_data_policy(
        self,
        request: Optional[Union[datapolicy.UpdateDataPolicyRequest, dict]] = None,
        *,
        data_policy: Optional[datapolicy.DataPolicy] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datapolicy.DataPolicy:
        r"""Updates the metadata for an existing data policy. The
        target data policy can be specified by the resource
        name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import bigquery_datapolicies_v1

            def sample_update_data_policy():
                # Create a client
                client = bigquery_datapolicies_v1.DataPolicyServiceClient()

                # Initialize request argument(s)
                data_policy = bigquery_datapolicies_v1.DataPolicy()
                data_policy.policy_tag = "policy_tag_value"
                data_policy.data_masking_policy.predefined_expression = "DEFAULT_MASKING_VALUE"

                request = bigquery_datapolicies_v1.UpdateDataPolicyRequest(
                    data_policy=data_policy,
                )

                # Make the request
                response = client.update_data_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_datapolicies_v1.types.UpdateDataPolicyRequest, dict]):
                The request object. Response message for the
                UpdateDataPolicy method.
            data_policy (google.cloud.bigquery_datapolicies_v1.types.DataPolicy):
                Required. Update the data policy's metadata.

                The target data policy is determined by the ``name``
                field. Other fields are updated to the specified values
                based on the field masks.

                This corresponds to the ``data_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The update mask applies to the resource. For the
                ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
                If not set, defaults to all of the fields that are
                allowed to update.

                Updates to the ``name`` and ``dataPolicyId`` fields are
                not allowed.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datapolicies_v1.types.DataPolicy:
                Represents the label-policy binding.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([data_policy, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datapolicy.UpdateDataPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datapolicy.UpdateDataPolicyRequest):
            request = datapolicy.UpdateDataPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if data_policy is not None:
                request.data_policy = data_policy
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_data_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("data_policy.name", request.data_policy.name),)
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

    def rename_data_policy(
        self,
        request: Optional[Union[datapolicy.RenameDataPolicyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        new_data_policy_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datapolicy.DataPolicy:
        r"""Renames the id (display name) of the specified data
        policy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import bigquery_datapolicies_v1

            def sample_rename_data_policy():
                # Create a client
                client = bigquery_datapolicies_v1.DataPolicyServiceClient()

                # Initialize request argument(s)
                request = bigquery_datapolicies_v1.RenameDataPolicyRequest(
                    name="name_value",
                    new_data_policy_id="new_data_policy_id_value",
                )

                # Make the request
                response = client.rename_data_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_datapolicies_v1.types.RenameDataPolicyRequest, dict]):
                The request object. Request message for the
                RenameDataPolicy method.
            name (str):
                Required. Resource name of the data policy to rename.
                The format is
                ``projects/{project_number}/locations/{location_id}/dataPolicies/{data_policy_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            new_data_policy_id (str):
                Required. The new data policy id.
                This corresponds to the ``new_data_policy_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datapolicies_v1.types.DataPolicy:
                Represents the label-policy binding.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, new_data_policy_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a datapolicy.RenameDataPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datapolicy.RenameDataPolicyRequest):
            request = datapolicy.RenameDataPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if new_data_policy_id is not None:
                request.new_data_policy_id = new_data_policy_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.rename_data_policy]

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

    def delete_data_policy(
        self,
        request: Optional[Union[datapolicy.DeleteDataPolicyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the data policy specified by its resource
        name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import bigquery_datapolicies_v1

            def sample_delete_data_policy():
                # Create a client
                client = bigquery_datapolicies_v1.DataPolicyServiceClient()

                # Initialize request argument(s)
                request = bigquery_datapolicies_v1.DeleteDataPolicyRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_data_policy(request=request)

        Args:
            request (Union[google.cloud.bigquery_datapolicies_v1.types.DeleteDataPolicyRequest, dict]):
                The request object. Request message for the
                DeleteDataPolicy method.
            name (str):
                Required. Resource name of the data policy to delete.
                Format is
                ``projects/{project_number}/locations/{location_id}/dataPolicies/{data_policy_id}``.

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
        # in a datapolicy.DeleteDataPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datapolicy.DeleteDataPolicyRequest):
            request = datapolicy.DeleteDataPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_data_policy]

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

    def get_data_policy(
        self,
        request: Optional[Union[datapolicy.GetDataPolicyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datapolicy.DataPolicy:
        r"""Gets the data policy specified by its resource name.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import bigquery_datapolicies_v1

            def sample_get_data_policy():
                # Create a client
                client = bigquery_datapolicies_v1.DataPolicyServiceClient()

                # Initialize request argument(s)
                request = bigquery_datapolicies_v1.GetDataPolicyRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_data_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.bigquery_datapolicies_v1.types.GetDataPolicyRequest, dict]):
                The request object. Request message for the GetDataPolicy
                method.
            name (str):
                Required. Resource name of the requested data policy.
                Format is
                ``projects/{project_number}/locations/{location_id}/dataPolicies/{data_policy_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_datapolicies_v1.types.DataPolicy:
                Represents the label-policy binding.
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
        # in a datapolicy.GetDataPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datapolicy.GetDataPolicyRequest):
            request = datapolicy.GetDataPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_data_policy]

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

    def list_data_policies(
        self,
        request: Optional[Union[datapolicy.ListDataPoliciesRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDataPoliciesPager:
        r"""List all of the data policies in the specified parent
        project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import bigquery_datapolicies_v1

            def sample_list_data_policies():
                # Create a client
                client = bigquery_datapolicies_v1.DataPolicyServiceClient()

                # Initialize request argument(s)
                request = bigquery_datapolicies_v1.ListDataPoliciesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_data_policies(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.bigquery_datapolicies_v1.types.ListDataPoliciesRequest, dict]):
                The request object. Request message for the
                ListDataPolicies method.
            parent (str):
                Required. Resource name of the project for which to list
                data policies. Format is
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
            google.cloud.bigquery_datapolicies_v1.services.data_policy_service.pagers.ListDataPoliciesPager:
                Response message for the
                ListDataPolicies method.
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
        # in a datapolicy.ListDataPoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datapolicy.ListDataPoliciesRequest):
            request = datapolicy.ListDataPoliciesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_data_policies]

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
        response = pagers.ListDataPoliciesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.GetIamPolicyRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM policy for the specified data policy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import bigquery_datapolicies_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_get_iam_policy():
                # Create a client
                client = bigquery_datapolicies_v1.DataPolicyServiceClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.GetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for ``GetIamPolicy`` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": [ "user:eve@example.com" ],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ], "etag": "BwWWja0YfJA=", "version": 3

                      }

                   **YAML example:**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z') etag:
                      BwWWja0YfJA= version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.GetIamPolicyRequest()

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

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

    def set_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.SetIamPolicyRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the IAM policy for the specified data policy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import bigquery_datapolicies_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_set_iam_policy():
                # Create a client
                client = bigquery_datapolicies_v1.DataPolicyServiceClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.SetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for ``SetIamPolicy`` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": [ "user:eve@example.com" ],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ], "etag": "BwWWja0YfJA=", "version": 3

                      }

                   **YAML example:**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z') etag:
                      BwWWja0YfJA= version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.SetIamPolicyRequest()

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

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
        request: Optional[Union[iam_policy_pb2.TestIamPermissionsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns the caller's permission on the specified data
        policy resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import bigquery_datapolicies_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_test_iam_permissions():
                # Create a client
                client = bigquery_datapolicies_v1.DataPolicyServiceClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value1', 'permissions_value2'],
                )

                # Make the request
                response = client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for ``TestIamPermissions`` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.TestIamPermissionsRequest()

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

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

    def __enter__(self) -> "DataPolicyServiceClient":
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


__all__ = ("DataPolicyServiceClient",)
