# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore
import pkg_resources

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.tasks_v2beta3.services.cloud_tasks import pagers
from google.cloud.tasks_v2beta3.types import cloudtasks
from google.cloud.tasks_v2beta3.types import queue
from google.cloud.tasks_v2beta3.types import queue as gct_queue
from google.cloud.tasks_v2beta3.types import target
from google.cloud.tasks_v2beta3.types import task
from google.cloud.tasks_v2beta3.types import task as gct_task

from .transports.base import DEFAULT_CLIENT_INFO, CloudTasksTransport
from .transports.grpc import CloudTasksGrpcTransport
from .transports.grpc_asyncio import CloudTasksGrpcAsyncIOTransport


class CloudTasksClientMeta(type):
    """Metaclass for the CloudTasks client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[CloudTasksTransport]]
    _transport_registry["grpc"] = CloudTasksGrpcTransport
    _transport_registry["grpc_asyncio"] = CloudTasksGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: str = None,
    ) -> Type[CloudTasksTransport]:
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


class CloudTasksClient(metaclass=CloudTasksClientMeta):
    """Cloud Tasks allows developers to manage the execution of
    background work in their applications.
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

    DEFAULT_ENDPOINT = "cloudtasks.googleapis.com"
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
            CloudTasksClient: The constructed client.
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
            CloudTasksClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudTasksTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudTasksTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def queue_path(
        project: str,
        location: str,
        queue: str,
    ) -> str:
        """Returns a fully-qualified queue string."""
        return "projects/{project}/locations/{location}/queues/{queue}".format(
            project=project,
            location=location,
            queue=queue,
        )

    @staticmethod
    def parse_queue_path(path: str) -> Dict[str, str]:
        """Parses a queue path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/queues/(?P<queue>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def task_path(
        project: str,
        location: str,
        queue: str,
        task: str,
    ) -> str:
        """Returns a fully-qualified task string."""
        return "projects/{project}/locations/{location}/queues/{queue}/tasks/{task}".format(
            project=project,
            location=location,
            queue=queue,
            task=task,
        )

    @staticmethod
    def parse_task_path(path: str) -> Dict[str, str]:
        """Parses a task path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/queues/(?P<queue>.+?)/tasks/(?P<task>.+?)$",
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
        default mTLS endpoint; if the environment variabel is "never", use the default API
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
        transport: Union[str, CloudTasksTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud tasks client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, CloudTasksTransport]): The
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
        if isinstance(transport, CloudTasksTransport):
            # transport is a CloudTasksTransport instance.
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
            )

    def list_queues(
        self,
        request: Union[cloudtasks.ListQueuesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListQueuesPager:
        r"""Lists queues.
        Queues are returned in lexicographical order.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_list_queues():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.ListQueuesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_queues(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.ListQueuesRequest, dict]):
                The request object. Request message for
                [ListQueues][google.cloud.tasks.v2beta3.CloudTasks.ListQueues].
            parent (str):
                Required. The location name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.services.cloud_tasks.pagers.ListQueuesPager:
                Response message for
                [ListQueues][google.cloud.tasks.v2beta3.CloudTasks.ListQueues].

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
        # in a cloudtasks.ListQueuesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.ListQueuesRequest):
            request = cloudtasks.ListQueuesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_queues]

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
        response = pagers.ListQueuesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_queue(
        self,
        request: Union[cloudtasks.GetQueueRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> queue.Queue:
        r"""Gets a queue.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_get_queue():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.GetQueueRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.GetQueueRequest, dict]):
                The request object. Request message for
                [GetQueue][google.cloud.tasks.v2beta3.CloudTasks.GetQueue].
            name (str):
                Required. The resource name of the queue. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, queue types, and
                others.

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
        # in a cloudtasks.GetQueueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.GetQueueRequest):
            request = cloudtasks.GetQueueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_queue]

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

    def create_queue(
        self,
        request: Union[cloudtasks.CreateQueueRequest, dict] = None,
        *,
        parent: str = None,
        queue: gct_queue.Queue = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_queue.Queue:
        r"""Creates a queue.

        Queues created with this method allow tasks to live for a
        maximum of 31 days. After a task is 31 days old, the task will
        be deleted regardless of whether it was dispatched or not.

        WARNING: Using this method may have unintended side effects if
        you are using an App Engine ``queue.yaml`` or ``queue.xml`` file
        to manage your queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__
        before using this method.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_create_queue():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.CreateQueueRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.CreateQueueRequest, dict]):
                The request object. Request message for
                [CreateQueue][google.cloud.tasks.v2beta3.CloudTasks.CreateQueue].
            parent (str):
                Required. The location name in which the queue will be
                created. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID``

                The list of allowed locations can be obtained by calling
                Cloud Tasks' implementation of
                [ListLocations][google.cloud.location.Locations.ListLocations].

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            queue (google.cloud.tasks_v2beta3.types.Queue):
                Required. The queue to create.

                [Queue's name][google.cloud.tasks.v2beta3.Queue.name]
                cannot be the same as an existing queue.

                This corresponds to the ``queue`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, queue types, and
                others.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, queue])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudtasks.CreateQueueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.CreateQueueRequest):
            request = cloudtasks.CreateQueueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if queue is not None:
                request.queue = queue

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_queue]

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

    def update_queue(
        self,
        request: Union[cloudtasks.UpdateQueueRequest, dict] = None,
        *,
        queue: gct_queue.Queue = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_queue.Queue:
        r"""Updates a queue.

        This method creates the queue if it does not exist and updates
        the queue if it does exist.

        Queues created with this method allow tasks to live for a
        maximum of 31 days. After a task is 31 days old, the task will
        be deleted regardless of whether it was dispatched or not.

        WARNING: Using this method may have unintended side effects if
        you are using an App Engine ``queue.yaml`` or ``queue.xml`` file
        to manage your queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__
        before using this method.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_update_queue():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.UpdateQueueRequest(
                )

                # Make the request
                response = client.update_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.UpdateQueueRequest, dict]):
                The request object. Request message for
                [UpdateQueue][google.cloud.tasks.v2beta3.CloudTasks.UpdateQueue].
            queue (google.cloud.tasks_v2beta3.types.Queue):
                Required. The queue to create or update.

                The queue's
                [name][google.cloud.tasks.v2beta3.Queue.name] must be
                specified.

                Output only fields cannot be modified using UpdateQueue.
                Any value specified for an output only field will be
                ignored. The queue's
                [name][google.cloud.tasks.v2beta3.Queue.name] cannot be
                changed.

                This corresponds to the ``queue`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                A mask used to specify which fields
                of the queue are being updated.
                If empty, then all fields will be
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
            google.cloud.tasks_v2beta3.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, queue types, and
                others.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([queue, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudtasks.UpdateQueueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.UpdateQueueRequest):
            request = cloudtasks.UpdateQueueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if queue is not None:
                request.queue = queue
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_queue]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("queue.name", request.queue.name),)
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

    def delete_queue(
        self,
        request: Union[cloudtasks.DeleteQueueRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a queue.

        This command will delete the queue even if it has tasks in it.

        Note: If you delete a queue, a queue with the same name can't be
        created for 7 days.

        WARNING: Using this method may have unintended side effects if
        you are using an App Engine ``queue.yaml`` or ``queue.xml`` file
        to manage your queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__
        before using this method.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_delete_queue():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.DeleteQueueRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_queue(request=request)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.DeleteQueueRequest, dict]):
                The request object. Request message for
                [DeleteQueue][google.cloud.tasks.v2beta3.CloudTasks.DeleteQueue].
            name (str):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

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
        # in a cloudtasks.DeleteQueueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.DeleteQueueRequest):
            request = cloudtasks.DeleteQueueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_queue]

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

    def purge_queue(
        self,
        request: Union[cloudtasks.PurgeQueueRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> queue.Queue:
        r"""Purges a queue by deleting all of its tasks.
        All tasks created before this method is called are
        permanently deleted.
        Purge operations can take up to one minute to take
        effect. Tasks might be dispatched before the purge takes
        effect. A purge is irreversible.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_purge_queue():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.PurgeQueueRequest(
                    name="name_value",
                )

                # Make the request
                response = client.purge_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.PurgeQueueRequest, dict]):
                The request object. Request message for
                [PurgeQueue][google.cloud.tasks.v2beta3.CloudTasks.PurgeQueue].
            name (str):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, queue types, and
                others.

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
        # in a cloudtasks.PurgeQueueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.PurgeQueueRequest):
            request = cloudtasks.PurgeQueueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.purge_queue]

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

    def pause_queue(
        self,
        request: Union[cloudtasks.PauseQueueRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> queue.Queue:
        r"""Pauses the queue.

        If a queue is paused then the system will stop dispatching tasks
        until the queue is resumed via
        [ResumeQueue][google.cloud.tasks.v2beta3.CloudTasks.ResumeQueue].
        Tasks can still be added when the queue is paused. A queue is
        paused if its [state][google.cloud.tasks.v2beta3.Queue.state] is
        [PAUSED][google.cloud.tasks.v2beta3.Queue.State.PAUSED].

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_pause_queue():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.PauseQueueRequest(
                    name="name_value",
                )

                # Make the request
                response = client.pause_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.PauseQueueRequest, dict]):
                The request object. Request message for
                [PauseQueue][google.cloud.tasks.v2beta3.CloudTasks.PauseQueue].
            name (str):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, queue types, and
                others.

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
        # in a cloudtasks.PauseQueueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.PauseQueueRequest):
            request = cloudtasks.PauseQueueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.pause_queue]

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

    def resume_queue(
        self,
        request: Union[cloudtasks.ResumeQueueRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> queue.Queue:
        r"""Resume a queue.

        This method resumes a queue after it has been
        [PAUSED][google.cloud.tasks.v2beta3.Queue.State.PAUSED] or
        [DISABLED][google.cloud.tasks.v2beta3.Queue.State.DISABLED]. The
        state of a queue is stored in the queue's
        [state][google.cloud.tasks.v2beta3.Queue.state]; after calling
        this method it will be set to
        [RUNNING][google.cloud.tasks.v2beta3.Queue.State.RUNNING].

        WARNING: Resuming many high-QPS queues at the same time can lead
        to target overloading. If you are resuming high-QPS queues,
        follow the 500/50/5 pattern described in `Managing Cloud Tasks
        Scaling
        Risks <https://cloud.google.com/tasks/docs/manage-cloud-task-scaling>`__.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_resume_queue():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.ResumeQueueRequest(
                    name="name_value",
                )

                # Make the request
                response = client.resume_queue(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.ResumeQueueRequest, dict]):
                The request object. Request message for
                [ResumeQueue][google.cloud.tasks.v2beta3.CloudTasks.ResumeQueue].
            name (str):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/location/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.types.Queue:
                A queue is a container of related
                tasks. Queues are configured to manage
                how those tasks are dispatched.
                Configurable properties include rate
                limits, retry options, queue types, and
                others.

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
        # in a cloudtasks.ResumeQueueRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.ResumeQueueRequest):
            request = cloudtasks.ResumeQueueRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.resume_queue]

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

    def get_iam_policy(
        self,
        request: Union[iam_policy_pb2.GetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for a
        [Queue][google.cloud.tasks.v2beta3.Queue]. Returns an empty
        policy if the resource exists and does not have a policy set.

        Authorization requires the following `Google
        IAM <https://cloud.google.com/iam>`__ permission on the
        specified resource parent:

        -  ``cloudtasks.queues.getIamPolicy``

        .. code-block:: python

            from google.cloud import tasks_v2beta3
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_get_iam_policy():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

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
                The request object. Request message for `GetIamPolicy`
                method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.GetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

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
        request: Union[iam_policy_pb2.SetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy for a
        [Queue][google.cloud.tasks.v2beta3.Queue]. Replaces any existing
        policy.

        Note: The Cloud Console does not check queue-level IAM
        permissions yet. Project-level permissions are required to use
        the Cloud Console.

        Authorization requires the following `Google
        IAM <https://cloud.google.com/iam>`__ permission on the
        specified resource parent:

        -  ``cloudtasks.queues.setIamPolicy``

        .. code-block:: python

            from google.cloud import tasks_v2beta3
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_set_iam_policy():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

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
                The request object. Request message for `SetIamPolicy`
                method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.SetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

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
        request: Union[iam_policy_pb2.TestIamPermissionsRequest, dict] = None,
        *,
        resource: str = None,
        permissions: Sequence[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns permissions that a caller has on a
        [Queue][google.cloud.tasks.v2beta3.Queue]. If the resource does
        not exist, this will return an empty set of permissions, not a
        [NOT_FOUND][google.rpc.Code.NOT_FOUND] error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for
        authorization checking. This operation may "fail open" without
        warning.

        .. code-block:: python

            from google.cloud import tasks_v2beta3
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_test_iam_permissions():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value_1', 'permissions_value_2'],
                )

                # Make the request
                response = client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for
                `TestIamPermissions` method.
            resource (str):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (Sequence[str]):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, permissions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.TestIamPermissionsRequest()
            if resource is not None:
                request.resource = resource
            if permissions:
                request.permissions.extend(permissions)

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

    def list_tasks(
        self,
        request: Union[cloudtasks.ListTasksRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTasksPager:
        r"""Lists the tasks in a queue.

        By default, only the
        [BASIC][google.cloud.tasks.v2beta3.Task.View.BASIC] view is
        retrieved due to performance considerations;
        [response_view][google.cloud.tasks.v2beta3.ListTasksRequest.response_view]
        controls the subset of information which is returned.

        The tasks may be returned in any order. The ordering may change
        at any time.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_list_tasks():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.ListTasksRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_tasks(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.ListTasksRequest, dict]):
                The request object. Request message for listing tasks
                using
                [ListTasks][google.cloud.tasks.v2beta3.CloudTasks.ListTasks].
            parent (str):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.services.cloud_tasks.pagers.ListTasksPager:
                Response message for listing tasks using
                [ListTasks][google.cloud.tasks.v2beta3.CloudTasks.ListTasks].

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
        # in a cloudtasks.ListTasksRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.ListTasksRequest):
            request = cloudtasks.ListTasksRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_tasks]

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
        response = pagers.ListTasksPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_task(
        self,
        request: Union[cloudtasks.GetTaskRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> task.Task:
        r"""Gets a task.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_get_task():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.GetTaskRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_task(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.GetTaskRequest, dict]):
                The request object. Request message for getting a task
                using
                [GetTask][google.cloud.tasks.v2beta3.CloudTasks.GetTask].
            name (str):
                Required. The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.types.Task:
                A unit of scheduled work.
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
        # in a cloudtasks.GetTaskRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.GetTaskRequest):
            request = cloudtasks.GetTaskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_task]

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

    def create_task(
        self,
        request: Union[cloudtasks.CreateTaskRequest, dict] = None,
        *,
        parent: str = None,
        task: gct_task.Task = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gct_task.Task:
        r"""Creates a task and adds it to a queue.

        Tasks cannot be updated after creation; there is no UpdateTask
        command.

        -  The maximum task size is 100KB.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_create_task():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.CreateTaskRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_task(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.CreateTaskRequest, dict]):
                The request object. Request message for
                [CreateTask][google.cloud.tasks.v2beta3.CloudTasks.CreateTask].
            parent (str):
                Required. The queue name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID``

                The queue must already exist.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            task (google.cloud.tasks_v2beta3.types.Task):
                Required. The task to add.

                Task names have the following format:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``.
                The user can optionally specify a task
                [name][google.cloud.tasks.v2beta3.Task.name]. If a name
                is not specified then the system will generate a random
                unique task id, which will be set in the task returned
                in the [response][google.cloud.tasks.v2beta3.Task.name].

                If
                [schedule_time][google.cloud.tasks.v2beta3.Task.schedule_time]
                is not set or is in the past then Cloud Tasks will set
                it to the current time.

                Task De-duplication:

                Explicitly specifying a task ID enables task
                de-duplication. If a task's ID is identical to that of
                an existing task or a task that was deleted or executed
                recently then the call will fail with
                [ALREADY_EXISTS][google.rpc.Code.ALREADY_EXISTS]. If the
                task's queue was created using Cloud Tasks, then another
                task with the same name can't be created for ~1hour
                after the original task was deleted or executed. If the
                task's queue was created using queue.yaml or queue.xml,
                then another task with the same name can't be created
                for ~9days after the original task was deleted or
                executed.

                Because there is an extra lookup cost to identify
                duplicate task names, these
                [CreateTask][google.cloud.tasks.v2beta3.CloudTasks.CreateTask]
                calls have significantly increased latency. Using hashed
                strings for the task id or for the prefix of the task id
                is recommended. Choosing task ids that are sequential or
                have sequential prefixes, for example using a timestamp,
                causes an increase in latency and error rates in all
                task commands. The infrastructure relies on an
                approximately uniform distribution of task ids to store
                and serve tasks efficiently.

                This corresponds to the ``task`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.types.Task:
                A unit of scheduled work.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, task])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a cloudtasks.CreateTaskRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.CreateTaskRequest):
            request = cloudtasks.CreateTaskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if task is not None:
                request.task = task

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_task]

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

    def delete_task(
        self,
        request: Union[cloudtasks.DeleteTaskRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a task.
        A task can be deleted if it is scheduled or dispatched.
        A task cannot be deleted if it has executed successfully
        or permanently failed.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_delete_task():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.DeleteTaskRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_task(request=request)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.DeleteTaskRequest, dict]):
                The request object. Request message for deleting a task
                using
                [DeleteTask][google.cloud.tasks.v2beta3.CloudTasks.DeleteTask].
            name (str):
                Required. The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``

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
        # in a cloudtasks.DeleteTaskRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.DeleteTaskRequest):
            request = cloudtasks.DeleteTaskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_task]

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

    def run_task(
        self,
        request: Union[cloudtasks.RunTaskRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> task.Task:
        r"""Forces a task to run now.

        When this method is called, Cloud Tasks will dispatch the task,
        even if the task is already running, the queue has reached its
        [RateLimits][google.cloud.tasks.v2beta3.RateLimits] or is
        [PAUSED][google.cloud.tasks.v2beta3.Queue.State.PAUSED].

        This command is meant to be used for manual debugging. For
        example,
        [RunTask][google.cloud.tasks.v2beta3.CloudTasks.RunTask] can be
        used to retry a failed task after a fix has been made or to
        manually force a task to be dispatched now.

        The dispatched task is returned. That is, the task that is
        returned contains the [status][Task.status] after the task is
        dispatched but before the task is received by its target.

        If Cloud Tasks receives a successful response from the task's
        target, then the task will be deleted; otherwise the task's
        [schedule_time][google.cloud.tasks.v2beta3.Task.schedule_time]
        will be reset to the time that
        [RunTask][google.cloud.tasks.v2beta3.CloudTasks.RunTask] was
        called plus the retry delay specified in the queue's
        [RetryConfig][google.cloud.tasks.v2beta3.RetryConfig].

        [RunTask][google.cloud.tasks.v2beta3.CloudTasks.RunTask] returns
        [NOT_FOUND][google.rpc.Code.NOT_FOUND] when it is called on a
        task that has already succeeded or permanently failed.

        .. code-block:: python

            from google.cloud import tasks_v2beta3

            def sample_run_task():
                # Create a client
                client = tasks_v2beta3.CloudTasksClient()

                # Initialize request argument(s)
                request = tasks_v2beta3.RunTaskRequest(
                    name="name_value",
                )

                # Make the request
                response = client.run_task(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tasks_v2beta3.types.RunTaskRequest, dict]):
                The request object. Request message for forcing a task
                to run now using
                [RunTask][google.cloud.tasks.v2beta3.CloudTasks.RunTask].
            name (str):
                Required. The task name. For example:
                ``projects/PROJECT_ID/locations/LOCATION_ID/queues/QUEUE_ID/tasks/TASK_ID``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tasks_v2beta3.types.Task:
                A unit of scheduled work.
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
        # in a cloudtasks.RunTaskRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, cloudtasks.RunTaskRequest):
            request = cloudtasks.RunTaskRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_task]

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
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-tasks",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudTasksClient",)
