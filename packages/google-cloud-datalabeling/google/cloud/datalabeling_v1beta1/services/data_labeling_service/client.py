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
from google.cloud.datalabeling_v1beta1.services.data_labeling_service import pagers
from google.cloud.datalabeling_v1beta1.types import annotation
from google.cloud.datalabeling_v1beta1.types import annotation_spec_set
from google.cloud.datalabeling_v1beta1.types import (
    annotation_spec_set as gcd_annotation_spec_set,
)
from google.cloud.datalabeling_v1beta1.types import data_labeling_service
from google.cloud.datalabeling_v1beta1.types import data_payloads
from google.cloud.datalabeling_v1beta1.types import dataset
from google.cloud.datalabeling_v1beta1.types import dataset as gcd_dataset
from google.cloud.datalabeling_v1beta1.types import evaluation
from google.cloud.datalabeling_v1beta1.types import evaluation_job
from google.cloud.datalabeling_v1beta1.types import evaluation_job as gcd_evaluation_job
from google.cloud.datalabeling_v1beta1.types import human_annotation_config
from google.cloud.datalabeling_v1beta1.types import instruction
from google.cloud.datalabeling_v1beta1.types import instruction as gcd_instruction
from google.cloud.datalabeling_v1beta1.types import operations
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import DataLabelingServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import DataLabelingServiceGrpcTransport
from .transports.grpc_asyncio import DataLabelingServiceGrpcAsyncIOTransport


class DataLabelingServiceClientMeta(type):
    """Metaclass for the DataLabelingService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[DataLabelingServiceTransport]]
    _transport_registry["grpc"] = DataLabelingServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = DataLabelingServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[DataLabelingServiceTransport]:
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


class DataLabelingServiceClient(metaclass=DataLabelingServiceClientMeta):
    """Service for the AI Platform Data Labeling API."""

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

    DEFAULT_ENDPOINT = "datalabeling.googleapis.com"
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
            DataLabelingServiceClient: The constructed client.
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
            DataLabelingServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DataLabelingServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            DataLabelingServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def annotated_dataset_path(
        project: str, dataset: str, annotated_dataset: str,
    ) -> str:
        """Returns a fully-qualified annotated_dataset string."""
        return "projects/{project}/datasets/{dataset}/annotatedDatasets/{annotated_dataset}".format(
            project=project, dataset=dataset, annotated_dataset=annotated_dataset,
        )

    @staticmethod
    def parse_annotated_dataset_path(path: str) -> Dict[str, str]:
        """Parses a annotated_dataset path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/datasets/(?P<dataset>.+?)/annotatedDatasets/(?P<annotated_dataset>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def annotation_spec_set_path(project: str, annotation_spec_set: str,) -> str:
        """Returns a fully-qualified annotation_spec_set string."""
        return "projects/{project}/annotationSpecSets/{annotation_spec_set}".format(
            project=project, annotation_spec_set=annotation_spec_set,
        )

    @staticmethod
    def parse_annotation_spec_set_path(path: str) -> Dict[str, str]:
        """Parses a annotation_spec_set path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/annotationSpecSets/(?P<annotation_spec_set>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def data_item_path(project: str, dataset: str, data_item: str,) -> str:
        """Returns a fully-qualified data_item string."""
        return "projects/{project}/datasets/{dataset}/dataItems/{data_item}".format(
            project=project, dataset=dataset, data_item=data_item,
        )

    @staticmethod
    def parse_data_item_path(path: str) -> Dict[str, str]:
        """Parses a data_item path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/datasets/(?P<dataset>.+?)/dataItems/(?P<data_item>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def dataset_path(project: str, dataset: str,) -> str:
        """Returns a fully-qualified dataset string."""
        return "projects/{project}/datasets/{dataset}".format(
            project=project, dataset=dataset,
        )

    @staticmethod
    def parse_dataset_path(path: str) -> Dict[str, str]:
        """Parses a dataset path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/datasets/(?P<dataset>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def evaluation_path(project: str, dataset: str, evaluation: str,) -> str:
        """Returns a fully-qualified evaluation string."""
        return "projects/{project}/datasets/{dataset}/evaluations/{evaluation}".format(
            project=project, dataset=dataset, evaluation=evaluation,
        )

    @staticmethod
    def parse_evaluation_path(path: str) -> Dict[str, str]:
        """Parses a evaluation path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/datasets/(?P<dataset>.+?)/evaluations/(?P<evaluation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def evaluation_job_path(project: str, evaluation_job: str,) -> str:
        """Returns a fully-qualified evaluation_job string."""
        return "projects/{project}/evaluationJobs/{evaluation_job}".format(
            project=project, evaluation_job=evaluation_job,
        )

    @staticmethod
    def parse_evaluation_job_path(path: str) -> Dict[str, str]:
        """Parses a evaluation_job path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/evaluationJobs/(?P<evaluation_job>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def example_path(
        project: str, dataset: str, annotated_dataset: str, example: str,
    ) -> str:
        """Returns a fully-qualified example string."""
        return "projects/{project}/datasets/{dataset}/annotatedDatasets/{annotated_dataset}/examples/{example}".format(
            project=project,
            dataset=dataset,
            annotated_dataset=annotated_dataset,
            example=example,
        )

    @staticmethod
    def parse_example_path(path: str) -> Dict[str, str]:
        """Parses a example path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/datasets/(?P<dataset>.+?)/annotatedDatasets/(?P<annotated_dataset>.+?)/examples/(?P<example>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def instruction_path(project: str, instruction: str,) -> str:
        """Returns a fully-qualified instruction string."""
        return "projects/{project}/instructions/{instruction}".format(
            project=project, instruction=instruction,
        )

    @staticmethod
    def parse_instruction_path(path: str) -> Dict[str, str]:
        """Parses a instruction path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/instructions/(?P<instruction>.+?)$", path
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
        transport: Union[str, DataLabelingServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the data labeling service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DataLabelingServiceTransport]): The
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
        if isinstance(transport, DataLabelingServiceTransport):
            # transport is a DataLabelingServiceTransport instance.
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

    def create_dataset(
        self,
        request: data_labeling_service.CreateDatasetRequest = None,
        *,
        parent: str = None,
        dataset: gcd_dataset.Dataset = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_dataset.Dataset:
        r"""Creates dataset. If success return a Dataset
        resource.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.CreateDatasetRequest):
                The request object. Request message for CreateDataset.
            parent (str):
                Required. Dataset resource parent, format:
                projects/{project_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            dataset (google.cloud.datalabeling_v1beta1.types.Dataset):
                Required. The dataset to be created.
                This corresponds to the ``dataset`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.Dataset:
                Dataset is the resource to hold your
                data. You can request multiple labeling
                tasks for a dataset while each one will
                generate an AnnotatedDataset.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, dataset])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.CreateDatasetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.CreateDatasetRequest):
            request = data_labeling_service.CreateDatasetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if dataset is not None:
                request.dataset = dataset

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_dataset]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_dataset(
        self,
        request: data_labeling_service.GetDatasetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataset.Dataset:
        r"""Gets dataset by resource name.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.GetDatasetRequest):
                The request object. Request message for GetDataSet.
            name (str):
                Required. Dataset resource name, format:
                projects/{project_id}/datasets/{dataset_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.Dataset:
                Dataset is the resource to hold your
                data. You can request multiple labeling
                tasks for a dataset while each one will
                generate an AnnotatedDataset.

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
        # in a data_labeling_service.GetDatasetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.GetDatasetRequest):
            request = data_labeling_service.GetDatasetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_dataset]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_datasets(
        self,
        request: data_labeling_service.ListDatasetsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDatasetsPager:
        r"""Lists datasets under a project. Pagination is
        supported.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ListDatasetsRequest):
                The request object. Request message for ListDataset.
            parent (str):
                Required. Dataset resource parent, format:
                projects/{project_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. Filter on dataset is not
                supported at this moment.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.services.data_labeling_service.pagers.ListDatasetsPager:
                Results of listing datasets within a
                project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a data_labeling_service.ListDatasetsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ListDatasetsRequest):
            request = data_labeling_service.ListDatasetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_datasets]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDatasetsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_dataset(
        self,
        request: data_labeling_service.DeleteDatasetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a dataset by resource name.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.DeleteDatasetRequest):
                The request object. Request message for DeleteDataset.
            name (str):
                Required. Dataset resource name, format:
                projects/{project_id}/datasets/{dataset_id}

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
        # in a data_labeling_service.DeleteDatasetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.DeleteDatasetRequest):
            request = data_labeling_service.DeleteDatasetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_dataset]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def import_data(
        self,
        request: data_labeling_service.ImportDataRequest = None,
        *,
        name: str = None,
        input_config: dataset.InputConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Imports data into dataset based on source locations
        defined in request. It can be called multiple times for
        the same dataset. Each dataset can only have one long
        running operation running on it. For example, no
        labeling task (also long running operation) can be
        started while importing is still ongoing. Vice versa.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ImportDataRequest):
                The request object. Request message for ImportData API.
            name (str):
                Required. Dataset resource name, format:
                projects/{project_id}/datasets/{dataset_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            input_config (google.cloud.datalabeling_v1beta1.types.InputConfig):
                Required. Specify the input source of
                the data.

                This corresponds to the ``input_config`` field
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
                :class:`google.cloud.datalabeling_v1beta1.types.ImportDataOperationResponse`
                Response used for ImportData longrunning operation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, input_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.ImportDataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ImportDataRequest):
            request = data_labeling_service.ImportDataRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if input_config is not None:
                request.input_config = input_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.import_data]

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
            operations.ImportDataOperationResponse,
            metadata_type=operations.ImportDataOperationMetadata,
        )

        # Done; return the response.
        return response

    def export_data(
        self,
        request: data_labeling_service.ExportDataRequest = None,
        *,
        name: str = None,
        annotated_dataset: str = None,
        filter: str = None,
        output_config: dataset.OutputConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Exports data and annotations from dataset.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ExportDataRequest):
                The request object. Request message for ExportData API.
            name (str):
                Required. Dataset resource name, format:
                projects/{project_id}/datasets/{dataset_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            annotated_dataset (str):
                Required. Annotated dataset resource name. DataItem in
                Dataset and their annotations in specified annotated
                dataset will be exported. It's in format of
                projects/{project_id}/datasets/{dataset_id}/annotatedDatasets/
                {annotated_dataset_id}

                This corresponds to the ``annotated_dataset`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. Filter is not supported at
                this moment.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_config (google.cloud.datalabeling_v1beta1.types.OutputConfig):
                Required. Specify the output
                destination.

                This corresponds to the ``output_config`` field
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
                :class:`google.cloud.datalabeling_v1beta1.types.ExportDataOperationResponse`
                Response used for ExportDataset longrunning operation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, annotated_dataset, filter, output_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.ExportDataRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ExportDataRequest):
            request = data_labeling_service.ExportDataRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if annotated_dataset is not None:
                request.annotated_dataset = annotated_dataset
            if filter is not None:
                request.filter = filter
            if output_config is not None:
                request.output_config = output_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.export_data]

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
            operations.ExportDataOperationResponse,
            metadata_type=operations.ExportDataOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_data_item(
        self,
        request: data_labeling_service.GetDataItemRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataset.DataItem:
        r"""Gets a data item in a dataset by resource name. This
        API can be called after data are imported into dataset.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.GetDataItemRequest):
                The request object. Request message for GetDataItem.
            name (str):
                Required. The name of the data item to get, format:
                projects/{project_id}/datasets/{dataset_id}/dataItems/{data_item_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.DataItem:
                DataItem is a piece of data, without
                annotation. For example, an image.

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
        # in a data_labeling_service.GetDataItemRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.GetDataItemRequest):
            request = data_labeling_service.GetDataItemRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_data_item]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_data_items(
        self,
        request: data_labeling_service.ListDataItemsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDataItemsPager:
        r"""Lists data items in a dataset. This API can be called
        after data are imported into dataset. Pagination is
        supported.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ListDataItemsRequest):
                The request object. Request message for ListDataItems.
            parent (str):
                Required. Name of the dataset to list data items,
                format: projects/{project_id}/datasets/{dataset_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. Filter is not supported at
                this moment.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.services.data_labeling_service.pagers.ListDataItemsPager:
                Results of listing data items in a
                dataset.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a data_labeling_service.ListDataItemsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ListDataItemsRequest):
            request = data_labeling_service.ListDataItemsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_data_items]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDataItemsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_annotated_dataset(
        self,
        request: data_labeling_service.GetAnnotatedDatasetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataset.AnnotatedDataset:
        r"""Gets an annotated dataset by resource name.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.GetAnnotatedDatasetRequest):
                The request object. Request message for
                GetAnnotatedDataset.
            name (str):
                Required. Name of the annotated dataset to get, format:
                projects/{project_id}/datasets/{dataset_id}/annotatedDatasets/
                {annotated_dataset_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.AnnotatedDataset:
                AnnotatedDataset is a set holding
                annotations for data in a Dataset. Each
                labeling task will generate an
                AnnotatedDataset under the Dataset that
                the task is requested for.

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
        # in a data_labeling_service.GetAnnotatedDatasetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.GetAnnotatedDatasetRequest):
            request = data_labeling_service.GetAnnotatedDatasetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_annotated_dataset]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_annotated_datasets(
        self,
        request: data_labeling_service.ListAnnotatedDatasetsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAnnotatedDatasetsPager:
        r"""Lists annotated datasets for a dataset. Pagination is
        supported.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ListAnnotatedDatasetsRequest):
                The request object. Request message for
                ListAnnotatedDatasets.
            parent (str):
                Required. Name of the dataset to list annotated
                datasets, format:
                projects/{project_id}/datasets/{dataset_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. Filter is not supported at
                this moment.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.services.data_labeling_service.pagers.ListAnnotatedDatasetsPager:
                Results of listing annotated datasets
                for a dataset.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a data_labeling_service.ListAnnotatedDatasetsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ListAnnotatedDatasetsRequest):
            request = data_labeling_service.ListAnnotatedDatasetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_annotated_datasets]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAnnotatedDatasetsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_annotated_dataset(
        self,
        request: data_labeling_service.DeleteAnnotatedDatasetRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an annotated dataset by resource name.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.DeleteAnnotatedDatasetRequest):
                The request object. Request message for
                DeleteAnnotatedDataset.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.DeleteAnnotatedDatasetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.DeleteAnnotatedDatasetRequest):
            request = data_labeling_service.DeleteAnnotatedDatasetRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_annotated_dataset]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def label_image(
        self,
        request: data_labeling_service.LabelImageRequest = None,
        *,
        parent: str = None,
        basic_config: human_annotation_config.HumanAnnotationConfig = None,
        feature: data_labeling_service.LabelImageRequest.Feature = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Starts a labeling task for image. The type of image
        labeling task is configured by feature in the request.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.LabelImageRequest):
                The request object. Request message for starting an
                image labeling task.
            parent (str):
                Required. Name of the dataset to request labeling task,
                format: projects/{project_id}/datasets/{dataset_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            basic_config (google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig):
                Required. Basic human annotation
                config.

                This corresponds to the ``basic_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            feature (google.cloud.datalabeling_v1beta1.types.LabelImageRequest.Feature):
                Required. The type of image labeling
                task.

                This corresponds to the ``feature`` field
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

                The result type for the operation will be :class:`google.cloud.datalabeling_v1beta1.types.AnnotatedDataset` AnnotatedDataset is a set holding annotations for data in a Dataset. Each
                   labeling task will generate an AnnotatedDataset under
                   the Dataset that the task is requested for.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, basic_config, feature])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.LabelImageRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.LabelImageRequest):
            request = data_labeling_service.LabelImageRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if basic_config is not None:
                request.basic_config = basic_config
            if feature is not None:
                request.feature = feature

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.label_image]

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
            dataset.AnnotatedDataset,
            metadata_type=operations.LabelOperationMetadata,
        )

        # Done; return the response.
        return response

    def label_video(
        self,
        request: data_labeling_service.LabelVideoRequest = None,
        *,
        parent: str = None,
        basic_config: human_annotation_config.HumanAnnotationConfig = None,
        feature: data_labeling_service.LabelVideoRequest.Feature = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Starts a labeling task for video. The type of video
        labeling task is configured by feature in the request.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.LabelVideoRequest):
                The request object. Request message for LabelVideo.
            parent (str):
                Required. Name of the dataset to request labeling task,
                format: projects/{project_id}/datasets/{dataset_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            basic_config (google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig):
                Required. Basic human annotation
                config.

                This corresponds to the ``basic_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            feature (google.cloud.datalabeling_v1beta1.types.LabelVideoRequest.Feature):
                Required. The type of video labeling
                task.

                This corresponds to the ``feature`` field
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

                The result type for the operation will be :class:`google.cloud.datalabeling_v1beta1.types.AnnotatedDataset` AnnotatedDataset is a set holding annotations for data in a Dataset. Each
                   labeling task will generate an AnnotatedDataset under
                   the Dataset that the task is requested for.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, basic_config, feature])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.LabelVideoRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.LabelVideoRequest):
            request = data_labeling_service.LabelVideoRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if basic_config is not None:
                request.basic_config = basic_config
            if feature is not None:
                request.feature = feature

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.label_video]

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
            dataset.AnnotatedDataset,
            metadata_type=operations.LabelOperationMetadata,
        )

        # Done; return the response.
        return response

    def label_text(
        self,
        request: data_labeling_service.LabelTextRequest = None,
        *,
        parent: str = None,
        basic_config: human_annotation_config.HumanAnnotationConfig = None,
        feature: data_labeling_service.LabelTextRequest.Feature = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Starts a labeling task for text. The type of text
        labeling task is configured by feature in the request.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.LabelTextRequest):
                The request object. Request message for LabelText.
            parent (str):
                Required. Name of the data set to request labeling task,
                format: projects/{project_id}/datasets/{dataset_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            basic_config (google.cloud.datalabeling_v1beta1.types.HumanAnnotationConfig):
                Required. Basic human annotation
                config.

                This corresponds to the ``basic_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            feature (google.cloud.datalabeling_v1beta1.types.LabelTextRequest.Feature):
                Required. The type of text labeling
                task.

                This corresponds to the ``feature`` field
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

                The result type for the operation will be :class:`google.cloud.datalabeling_v1beta1.types.AnnotatedDataset` AnnotatedDataset is a set holding annotations for data in a Dataset. Each
                   labeling task will generate an AnnotatedDataset under
                   the Dataset that the task is requested for.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, basic_config, feature])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.LabelTextRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.LabelTextRequest):
            request = data_labeling_service.LabelTextRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if basic_config is not None:
                request.basic_config = basic_config
            if feature is not None:
                request.feature = feature

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.label_text]

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
            dataset.AnnotatedDataset,
            metadata_type=operations.LabelOperationMetadata,
        )

        # Done; return the response.
        return response

    def get_example(
        self,
        request: data_labeling_service.GetExampleRequest = None,
        *,
        name: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataset.Example:
        r"""Gets an example by resource name, including both data
        and annotation.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.GetExampleRequest):
                The request object. Request message for GetExample
            name (str):
                Required. Name of example, format:
                projects/{project_id}/datasets/{dataset_id}/annotatedDatasets/
                {annotated_dataset_id}/examples/{example_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. An expression for filtering Examples. Filter
                by annotation_spec.display_name is supported. Format
                "annotation_spec.display_name = {display_name}"

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.Example:
                An Example is a piece of data and its
                annotation. For example, an image with
                label "house".

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.GetExampleRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.GetExampleRequest):
            request = data_labeling_service.GetExampleRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_example]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_examples(
        self,
        request: data_labeling_service.ListExamplesRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListExamplesPager:
        r"""Lists examples in an annotated dataset. Pagination is
        supported.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ListExamplesRequest):
                The request object. Request message for ListExamples.
            parent (str):
                Required. Example resource parent.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. An expression for filtering Examples. For
                annotated datasets that have annotation spec set, filter
                by annotation_spec.display_name is supported. Format
                "annotation_spec.display_name = {display_name}"

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.services.data_labeling_service.pagers.ListExamplesPager:
                Results of listing Examples in and
                annotated dataset.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a data_labeling_service.ListExamplesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ListExamplesRequest):
            request = data_labeling_service.ListExamplesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_examples]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListExamplesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_annotation_spec_set(
        self,
        request: data_labeling_service.CreateAnnotationSpecSetRequest = None,
        *,
        parent: str = None,
        annotation_spec_set: gcd_annotation_spec_set.AnnotationSpecSet = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_annotation_spec_set.AnnotationSpecSet:
        r"""Creates an annotation spec set by providing a set of
        labels.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.CreateAnnotationSpecSetRequest):
                The request object. Request message for
                CreateAnnotationSpecSet.
            parent (str):
                Required. AnnotationSpecSet resource parent, format:
                projects/{project_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            annotation_spec_set (google.cloud.datalabeling_v1beta1.types.AnnotationSpecSet):
                Required. Annotation spec set to create. Annotation
                specs must be included. Only one annotation spec will be
                accepted for annotation specs with same display_name.

                This corresponds to the ``annotation_spec_set`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.AnnotationSpecSet:
                An AnnotationSpecSet is a collection
                of label definitions. For example, in
                image classification tasks, you define a
                set of possible labels for images as an
                AnnotationSpecSet. An AnnotationSpecSet
                is immutable upon creation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, annotation_spec_set])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.CreateAnnotationSpecSetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, data_labeling_service.CreateAnnotationSpecSetRequest
        ):
            request = data_labeling_service.CreateAnnotationSpecSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if annotation_spec_set is not None:
                request.annotation_spec_set = annotation_spec_set

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_annotation_spec_set
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

    def get_annotation_spec_set(
        self,
        request: data_labeling_service.GetAnnotationSpecSetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> annotation_spec_set.AnnotationSpecSet:
        r"""Gets an annotation spec set by resource name.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.GetAnnotationSpecSetRequest):
                The request object. Request message for
                GetAnnotationSpecSet.
            name (str):
                Required. AnnotationSpecSet resource name, format:
                projects/{project_id}/annotationSpecSets/{annotation_spec_set_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.AnnotationSpecSet:
                An AnnotationSpecSet is a collection
                of label definitions. For example, in
                image classification tasks, you define a
                set of possible labels for images as an
                AnnotationSpecSet. An AnnotationSpecSet
                is immutable upon creation.

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
        # in a data_labeling_service.GetAnnotationSpecSetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.GetAnnotationSpecSetRequest):
            request = data_labeling_service.GetAnnotationSpecSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_annotation_spec_set]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_annotation_spec_sets(
        self,
        request: data_labeling_service.ListAnnotationSpecSetsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAnnotationSpecSetsPager:
        r"""Lists annotation spec sets for a project. Pagination
        is supported.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ListAnnotationSpecSetsRequest):
                The request object. Request message for
                ListAnnotationSpecSets.
            parent (str):
                Required. Parent of AnnotationSpecSet resource, format:
                projects/{project_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. Filter is not supported at
                this moment.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.services.data_labeling_service.pagers.ListAnnotationSpecSetsPager:
                Results of listing annotation spec
                set under a project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a data_labeling_service.ListAnnotationSpecSetsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ListAnnotationSpecSetsRequest):
            request = data_labeling_service.ListAnnotationSpecSetsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_annotation_spec_sets
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
        response = pagers.ListAnnotationSpecSetsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_annotation_spec_set(
        self,
        request: data_labeling_service.DeleteAnnotationSpecSetRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an annotation spec set by resource name.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.DeleteAnnotationSpecSetRequest):
                The request object. Request message for
                DeleteAnnotationSpecSet.
            name (str):
                Required. AnnotationSpec resource name, format:
                ``projects/{project_id}/annotationSpecSets/{annotation_spec_set_id}``.

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
        # in a data_labeling_service.DeleteAnnotationSpecSetRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, data_labeling_service.DeleteAnnotationSpecSetRequest
        ):
            request = data_labeling_service.DeleteAnnotationSpecSetRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_annotation_spec_set
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

    def create_instruction(
        self,
        request: data_labeling_service.CreateInstructionRequest = None,
        *,
        parent: str = None,
        instruction: gcd_instruction.Instruction = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates an instruction for how data should be
        labeled.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.CreateInstructionRequest):
                The request object. Request message for
                CreateInstruction.
            parent (str):
                Required. Instruction resource parent, format:
                projects/{project_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instruction (google.cloud.datalabeling_v1beta1.types.Instruction):
                Required. Instruction of how to
                perform the labeling task.

                This corresponds to the ``instruction`` field
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

                The result type for the operation will be :class:`google.cloud.datalabeling_v1beta1.types.Instruction` Instruction of how to perform the labeling task for human operators.
                   Currently only PDF instruction is supported.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, instruction])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.CreateInstructionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.CreateInstructionRequest):
            request = data_labeling_service.CreateInstructionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if instruction is not None:
                request.instruction = instruction

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_instruction]

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
            gcd_instruction.Instruction,
            metadata_type=operations.CreateInstructionMetadata,
        )

        # Done; return the response.
        return response

    def get_instruction(
        self,
        request: data_labeling_service.GetInstructionRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instruction.Instruction:
        r"""Gets an instruction by resource name.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.GetInstructionRequest):
                The request object. Request message for GetInstruction.
            name (str):
                Required. Instruction resource name, format:
                projects/{project_id}/instructions/{instruction_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.Instruction:
                Instruction of how to perform the
                labeling task for human operators.
                Currently only PDF instruction is
                supported.

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
        # in a data_labeling_service.GetInstructionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.GetInstructionRequest):
            request = data_labeling_service.GetInstructionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_instruction]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_instructions(
        self,
        request: data_labeling_service.ListInstructionsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstructionsPager:
        r"""Lists instructions for a project. Pagination is
        supported.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ListInstructionsRequest):
                The request object. Request message for
                ListInstructions.
            parent (str):
                Required. Instruction resource parent, format:
                projects/{project_id}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. Filter is not supported at
                this moment.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.services.data_labeling_service.pagers.ListInstructionsPager:
                Results of listing instructions under
                a project.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a data_labeling_service.ListInstructionsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ListInstructionsRequest):
            request = data_labeling_service.ListInstructionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_instructions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListInstructionsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_instruction(
        self,
        request: data_labeling_service.DeleteInstructionRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an instruction object by resource name.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.DeleteInstructionRequest):
                The request object. Request message for
                DeleteInstruction.
            name (str):
                Required. Instruction resource name, format:
                projects/{project_id}/instructions/{instruction_id}

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
        # in a data_labeling_service.DeleteInstructionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.DeleteInstructionRequest):
            request = data_labeling_service.DeleteInstructionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_instruction]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def get_evaluation(
        self,
        request: data_labeling_service.GetEvaluationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> evaluation.Evaluation:
        r"""Gets an evaluation by resource name (to search, use
        [projects.evaluations.search][google.cloud.datalabeling.v1beta1.DataLabelingService.SearchEvaluations]).

        Args:
            request (google.cloud.datalabeling_v1beta1.types.GetEvaluationRequest):
                The request object. Request message for GetEvaluation.
            name (str):
                Required. Name of the evaluation. Format:

                "projects/{project_id}/datasets/{dataset_id}/evaluations/{evaluation_id}'

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.Evaluation:
                Describes an evaluation between a machine learning model's predictions and
                   ground truth labels. Created when an
                   [EvaluationJob][google.cloud.datalabeling.v1beta1.EvaluationJob]
                   runs successfully.

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
        # in a data_labeling_service.GetEvaluationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.GetEvaluationRequest):
            request = data_labeling_service.GetEvaluationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_evaluation]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def search_evaluations(
        self,
        request: data_labeling_service.SearchEvaluationsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchEvaluationsPager:
        r"""Searches
        [evaluations][google.cloud.datalabeling.v1beta1.Evaluation]
        within a project.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.SearchEvaluationsRequest):
                The request object. Request message for
                SearchEvaluation.
            parent (str):
                Required. Evaluation search parent (project ID). Format:
                "projects/{project_id}"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. To search evaluations, you can filter by the
                following:

                -  evaluation\_job.evaluation_job_id (the last part of
                   [EvaluationJob.name][google.cloud.datalabeling.v1beta1.EvaluationJob.name])
                -  evaluation\_job.model_id (the {model_name} portion of
                   [EvaluationJob.modelVersion][google.cloud.datalabeling.v1beta1.EvaluationJob.model_version])
                -  evaluation\_job.evaluation_job_run_time_start
                   (Minimum threshold for the
                   [evaluationJobRunTime][google.cloud.datalabeling.v1beta1.Evaluation.evaluation_job_run_time]
                   that created the evaluation)
                -  evaluation\_job.evaluation_job_run_time_end (Maximum
                   threshold for the
                   [evaluationJobRunTime][google.cloud.datalabeling.v1beta1.Evaluation.evaluation_job_run_time]
                   that created the evaluation)
                -  evaluation\_job.job_state
                   ([EvaluationJob.state][google.cloud.datalabeling.v1beta1.EvaluationJob.state])
                -  annotation\_spec.display_name (the Evaluation
                   contains a metric for the annotation spec with this
                   [displayName][google.cloud.datalabeling.v1beta1.AnnotationSpec.display_name])

                To filter by multiple critiera, use the ``AND`` operator
                or the ``OR`` operator. The following examples shows a
                string that filters by several critiera:

                "evaluation\ *job.evaluation_job_id =
                {evaluation_job_id} AND evaluation*\ job.model_id =
                {model_name} AND
                evaluation\ *job.evaluation_job_run_time_start =
                {timestamp_1} AND
                evaluation*\ job.evaluation_job_run_time_end =
                {timestamp_2} AND annotation\_spec.display_name =
                {display_name}"

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.services.data_labeling_service.pagers.SearchEvaluationsPager:
                Results of searching evaluations.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a data_labeling_service.SearchEvaluationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.SearchEvaluationsRequest):
            request = data_labeling_service.SearchEvaluationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_evaluations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.SearchEvaluationsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_example_comparisons(
        self,
        request: data_labeling_service.SearchExampleComparisonsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchExampleComparisonsPager:
        r"""Searches example comparisons from an evaluation. The
        return format is a list of example comparisons that show
        ground truth and prediction(s) for a single input.
        Search by providing an evaluation ID.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.SearchExampleComparisonsRequest):
                The request object. Request message of
                SearchExampleComparisons.
            parent (str):
                Required. Name of the
                [Evaluation][google.cloud.datalabeling.v1beta1.Evaluation]
                resource to search for example comparisons from. Format:

                "projects/{project_id}/datasets/{dataset_id}/evaluations/{evaluation_id}"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.services.data_labeling_service.pagers.SearchExampleComparisonsPager:
                Results of searching example
                comparisons.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a data_labeling_service.SearchExampleComparisonsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, data_labeling_service.SearchExampleComparisonsRequest
        ):
            request = data_labeling_service.SearchExampleComparisonsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.search_example_comparisons
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
        response = pagers.SearchExampleComparisonsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_evaluation_job(
        self,
        request: data_labeling_service.CreateEvaluationJobRequest = None,
        *,
        parent: str = None,
        job: evaluation_job.EvaluationJob = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> evaluation_job.EvaluationJob:
        r"""Creates an evaluation job.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.CreateEvaluationJobRequest):
                The request object. Request message for
                CreateEvaluationJob.
            parent (str):
                Required. Evaluation job resource parent. Format:
                "projects/{project_id}"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job (google.cloud.datalabeling_v1beta1.types.EvaluationJob):
                Required. The evaluation job to
                create.

                This corresponds to the ``job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.EvaluationJob:
                Defines an evaluation job that runs periodically to generate
                   [Evaluations][google.cloud.datalabeling.v1beta1.Evaluation].
                   [Creating an evaluation
                   job](/ml-engine/docs/continuous-evaluation/create-job)
                   is the starting point for using continuous
                   evaluation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.CreateEvaluationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.CreateEvaluationJobRequest):
            request = data_labeling_service.CreateEvaluationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if job is not None:
                request.job = job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_evaluation_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_evaluation_job(
        self,
        request: data_labeling_service.UpdateEvaluationJobRequest = None,
        *,
        evaluation_job: gcd_evaluation_job.EvaluationJob = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_evaluation_job.EvaluationJob:
        r"""Updates an evaluation job. You can only update certain fields of
        the job's
        [EvaluationJobConfig][google.cloud.datalabeling.v1beta1.EvaluationJobConfig]:
        ``humanAnnotationConfig.instruction``, ``exampleCount``, and
        ``exampleSamplePercentage``.

        If you want to change any other aspect of the evaluation job,
        you must delete the job and create a new one.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.UpdateEvaluationJobRequest):
                The request object. Request message for
                UpdateEvaluationJob.
            evaluation_job (google.cloud.datalabeling_v1beta1.types.EvaluationJob):
                Required. Evaluation job that is
                going to be updated.

                This corresponds to the ``evaluation_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. Mask for which fields to update. You can only
                provide the following fields:

                -  ``evaluationJobConfig.humanAnnotationConfig.instruction``
                -  ``evaluationJobConfig.exampleCount``
                -  ``evaluationJobConfig.exampleSamplePercentage``

                You can provide more than one of these fields by
                separating them with commas.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.EvaluationJob:
                Defines an evaluation job that runs periodically to generate
                   [Evaluations][google.cloud.datalabeling.v1beta1.Evaluation].
                   [Creating an evaluation
                   job](/ml-engine/docs/continuous-evaluation/create-job)
                   is the starting point for using continuous
                   evaluation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([evaluation_job, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a data_labeling_service.UpdateEvaluationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.UpdateEvaluationJobRequest):
            request = data_labeling_service.UpdateEvaluationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if evaluation_job is not None:
                request.evaluation_job = evaluation_job
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_evaluation_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("evaluation_job.name", request.evaluation_job.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_evaluation_job(
        self,
        request: data_labeling_service.GetEvaluationJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> evaluation_job.EvaluationJob:
        r"""Gets an evaluation job by resource name.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.GetEvaluationJobRequest):
                The request object. Request message for
                GetEvaluationJob.
            name (str):
                Required. Name of the evaluation job. Format:

                "projects/{project_id}/evaluationJobs/{evaluation_job_id}"

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.types.EvaluationJob:
                Defines an evaluation job that runs periodically to generate
                   [Evaluations][google.cloud.datalabeling.v1beta1.Evaluation].
                   [Creating an evaluation
                   job](/ml-engine/docs/continuous-evaluation/create-job)
                   is the starting point for using continuous
                   evaluation.

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
        # in a data_labeling_service.GetEvaluationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.GetEvaluationJobRequest):
            request = data_labeling_service.GetEvaluationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_evaluation_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def pause_evaluation_job(
        self,
        request: data_labeling_service.PauseEvaluationJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Pauses an evaluation job. Pausing an evaluation job that is
        already in a ``PAUSED`` state is a no-op.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.PauseEvaluationJobRequest):
                The request object. Request message for
                PauseEvaluationJob.
            name (str):
                Required. Name of the evaluation job that is going to be
                paused. Format:

                "projects/{project_id}/evaluationJobs/{evaluation_job_id}"

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
        # in a data_labeling_service.PauseEvaluationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.PauseEvaluationJobRequest):
            request = data_labeling_service.PauseEvaluationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.pause_evaluation_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def resume_evaluation_job(
        self,
        request: data_labeling_service.ResumeEvaluationJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Resumes a paused evaluation job. A deleted evaluation
        job can't be resumed. Resuming a running or scheduled
        evaluation job is a no-op.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ResumeEvaluationJobRequest):
                The request object. Request message ResumeEvaluationJob.
            name (str):
                Required. Name of the evaluation job that is going to be
                resumed. Format:

                "projects/{project_id}/evaluationJobs/{evaluation_job_id}"

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
        # in a data_labeling_service.ResumeEvaluationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ResumeEvaluationJobRequest):
            request = data_labeling_service.ResumeEvaluationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resume_evaluation_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def delete_evaluation_job(
        self,
        request: data_labeling_service.DeleteEvaluationJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Stops and deletes an evaluation job.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.DeleteEvaluationJobRequest):
                The request object. Request message DeleteEvaluationJob.
            name (str):
                Required. Name of the evaluation job that is going to be
                deleted. Format:

                "projects/{project_id}/evaluationJobs/{evaluation_job_id}"

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
        # in a data_labeling_service.DeleteEvaluationJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.DeleteEvaluationJobRequest):
            request = data_labeling_service.DeleteEvaluationJobRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_evaluation_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def list_evaluation_jobs(
        self,
        request: data_labeling_service.ListEvaluationJobsRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEvaluationJobsPager:
        r"""Lists all evaluation jobs within a project with
        possible filters. Pagination is supported.

        Args:
            request (google.cloud.datalabeling_v1beta1.types.ListEvaluationJobsRequest):
                The request object. Request message for
                ListEvaluationJobs.
            parent (str):
                Required. Evaluation job resource parent. Format:
                "projects/{project_id}"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Optional. You can filter the jobs to list by model_id
                (also known as model_name, as described in
                [EvaluationJob.modelVersion][google.cloud.datalabeling.v1beta1.EvaluationJob.model_version])
                or by evaluation job state (as described in
                [EvaluationJob.state][google.cloud.datalabeling.v1beta1.EvaluationJob.state]).
                To filter by both criteria, use the ``AND`` operator or
                the ``OR`` operator. For example, you can use the
                following string for your filter:
                "evaluation\ *job.model_id = {model_name} AND
                evaluation*\ job.state = {evaluation_job_state}"

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datalabeling_v1beta1.services.data_labeling_service.pagers.ListEvaluationJobsPager:
                Results for listing evaluation jobs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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
        # in a data_labeling_service.ListEvaluationJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, data_labeling_service.ListEvaluationJobsRequest):
            request = data_labeling_service.ListEvaluationJobsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_evaluation_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEvaluationJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-datalabeling",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DataLabelingServiceClient",)
