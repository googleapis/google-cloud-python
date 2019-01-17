# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Accesses the google.cloud.iot.v1 DeviceManager API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.cloud.iot_v1.gapic import device_manager_client_config
from google.cloud.iot_v1.gapic import enums
from google.cloud.iot_v1.gapic.transports import device_manager_grpc_transport
from google.cloud.iot_v1.proto import device_manager_pb2
from google.cloud.iot_v1.proto import device_manager_pb2_grpc
from google.cloud.iot_v1.proto import resources_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-iot").version


class DeviceManagerClient(object):
    """Internet of Things (IoT) service. Securely connect and manage IoT devices."""

    SERVICE_ADDRESS = "cloudiot.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.iot.v1.DeviceManager"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DeviceManagerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}",
            project=project,
            location=location,
        )

    @classmethod
    def registry_path(cls, project, location, registry):
        """Return a fully-qualified registry string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/registries/{registry}",
            project=project,
            location=location,
            registry=registry,
        )

    @classmethod
    def device_path(cls, project, location, registry, device):
        """Return a fully-qualified device string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/registries/{registry}/devices/{device}",
            project=project,
            location=location,
            registry=registry,
            device=device,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.DeviceManagerGrpcTransport,
                    Callable[[~.Credentials, type], ~.DeviceManagerGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = device_manager_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=device_manager_grpc_transport.DeviceManagerGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = device_manager_grpc_transport.DeviceManagerGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def create_device_registry(
        self,
        parent,
        device_registry,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a device registry that contains devices.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # TODO: Initialize `device_registry`:
            >>> device_registry = {}
            >>>
            >>> response = client.create_device_registry(parent, device_registry)

        Args:
            parent (str): The project and cloud region where this device registry must be created.
                For example, ``projects/example-project/locations/us-central1``.
            device_registry (Union[dict, ~google.cloud.iot_v1.types.DeviceRegistry]): The device registry. The field ``name`` must be empty. The server will
                generate that field from the device registry ``id`` provided and the
                ``parent`` field.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.DeviceRegistry`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.DeviceRegistry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_device_registry" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_device_registry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_device_registry,
                default_retry=self._method_configs["CreateDeviceRegistry"].retry,
                default_timeout=self._method_configs["CreateDeviceRegistry"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.CreateDeviceRegistryRequest(
            parent=parent, device_registry=device_registry
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_device_registry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_device_registry(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets a device registry configuration.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> response = client.get_device_registry(name)

        Args:
            name (str): The name of the device registry. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.DeviceRegistry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_device_registry" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_device_registry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_device_registry,
                default_retry=self._method_configs["GetDeviceRegistry"].retry,
                default_timeout=self._method_configs["GetDeviceRegistry"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.GetDeviceRegistryRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_device_registry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_device_registry(
        self,
        device_registry,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a device registry configuration.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> # TODO: Initialize `device_registry`:
            >>> device_registry = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_device_registry(device_registry, update_mask)

        Args:
            device_registry (Union[dict, ~google.cloud.iot_v1.types.DeviceRegistry]): The new values for the device registry. The ``id`` field must be empty,
                and the ``name`` field must indicate the path of the resource. For
                example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.DeviceRegistry`
            update_mask (Union[dict, ~google.cloud.iot_v1.types.FieldMask]): Only updates the ``device_registry`` fields indicated by this mask. The
                field mask must not be empty, and it must not contain fields that are
                immutable or only set by the server. Mutable top-level fields:
                ``event_notification_config``, ``http_config``, ``mqtt_config``, and
                ``state_notification_config``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.DeviceRegistry` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_device_registry" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_device_registry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_device_registry,
                default_retry=self._method_configs["UpdateDeviceRegistry"].retry,
                default_timeout=self._method_configs["UpdateDeviceRegistry"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.UpdateDeviceRegistryRequest(
            device_registry=device_registry, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("device_registry.name", device_registry.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_device_registry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_device_registry(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a device registry configuration.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> client.delete_device_registry(name)

        Args:
            name (str): The name of the device registry. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_device_registry" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_device_registry"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_device_registry,
                default_retry=self._method_configs["DeleteDeviceRegistry"].retry,
                default_timeout=self._method_configs["DeleteDeviceRegistry"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.DeleteDeviceRegistryRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_device_registry"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_device_registries(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists device registries.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.location_path('[PROJECT]', '[LOCATION]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_device_registries(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_device_registries(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The project and cloud region path. For example,
                ``projects/example-project/locations/us-central1``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.iot_v1.types.DeviceRegistry` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_device_registries" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_device_registries"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_device_registries,
                default_retry=self._method_configs["ListDeviceRegistries"].retry,
                default_timeout=self._method_configs["ListDeviceRegistries"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ListDeviceRegistriesRequest(
            parent=parent, page_size=page_size
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_device_registries"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="device_registries",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def create_device(
        self,
        parent,
        device,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a device in a device registry.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # TODO: Initialize `device`:
            >>> device = {}
            >>>
            >>> response = client.create_device(parent, device)

        Args:
            parent (str): The name of the device registry where this device should be created. For
                example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.
            device (Union[dict, ~google.cloud.iot_v1.types.Device]): The device registration details. The field ``name`` must be empty. The
                server generates ``name`` from the device registry ``id`` and the
                ``parent`` field.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.Device`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Device` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_device,
                default_retry=self._method_configs["CreateDevice"].retry,
                default_timeout=self._method_configs["CreateDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.CreateDeviceRequest(parent=parent, device=device)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["create_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_device(
        self,
        name,
        field_mask=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets details about a device.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> response = client.get_device(name)

        Args:
            name (str): The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
            field_mask (Union[dict, ~google.cloud.iot_v1.types.FieldMask]): The fields of the ``Device`` resource to be returned in the response. If
                the field mask is unset or empty, all fields are returned.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Device` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_device,
                default_retry=self._method_configs["GetDevice"].retry,
                default_timeout=self._method_configs["GetDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.GetDeviceRequest(name=name, field_mask=field_mask)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def update_device(
        self,
        device,
        update_mask,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Updates a device.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> # TODO: Initialize `device`:
            >>> device = {}
            >>>
            >>> # TODO: Initialize `update_mask`:
            >>> update_mask = {}
            >>>
            >>> response = client.update_device(device, update_mask)

        Args:
            device (Union[dict, ~google.cloud.iot_v1.types.Device]): The new values for the device. The ``id`` and ``num_id`` fields must be
                empty, and the field ``name`` must specify the name path. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``\ or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.Device`
            update_mask (Union[dict, ~google.cloud.iot_v1.types.FieldMask]): Only updates the ``device`` fields indicated by this mask. The field
                mask must not be empty, and it must not contain fields that are
                immutable or only set by the server. Mutable top-level fields:
                ``credentials``, ``blocked``, and ``metadata``

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Device` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "update_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "update_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.update_device,
                default_retry=self._method_configs["UpdateDevice"].retry,
                default_timeout=self._method_configs["UpdateDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.UpdateDeviceRequest(
            device=device, update_mask=update_mask
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("device.name", device.name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["update_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_device(
        self,
        name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes a device.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> client.delete_device(name)

        Args:
            name (str): The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_device,
                default_retry=self._method_configs["DeleteDevice"].retry,
                default_timeout=self._method_configs["DeleteDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.DeleteDeviceRequest(name=name)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_devices(
        self,
        parent,
        device_num_ids=None,
        device_ids=None,
        field_mask=None,
        gateway_list_options=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        List devices in a device registry.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_devices(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_devices(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): The device registry path. Required. For example,
                ``projects/my-project/locations/us-central1/registries/my-registry``.
            device_num_ids (list[long]): A list of device numeric IDs. If empty, this field is ignored. Maximum
                IDs: 10,000.
            device_ids (list[str]): A list of device string IDs. For example, ``['device0', 'device12']``.
                If empty, this field is ignored. Maximum IDs: 10,000
            field_mask (Union[dict, ~google.cloud.iot_v1.types.FieldMask]): The fields of the ``Device`` resource to be returned in the response.
                The fields ``id`` and ``num_id`` are always returned, along with any
                other fields specified.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.FieldMask`
            gateway_list_options (Union[dict, ~google.cloud.iot_v1.types.GatewayListOptions]): Options related to gateways.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.GatewayListOptions`
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.iot_v1.types.Device` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_devices" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_devices"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_devices,
                default_retry=self._method_configs["ListDevices"].retry,
                default_timeout=self._method_configs["ListDevices"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ListDevicesRequest(
            parent=parent,
            device_num_ids=device_num_ids,
            device_ids=device_ids,
            field_mask=field_mask,
            gateway_list_options=gateway_list_options,
            page_size=page_size,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_devices"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="devices",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def modify_cloud_to_device_config(
        self,
        name,
        binary_data,
        version_to_update=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Modifies the configuration for the device, which is eventually sent from
        the Cloud IoT Core servers. Returns the modified configuration version and
        its metadata.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> # TODO: Initialize `binary_data`:
            >>> binary_data = b''
            >>>
            >>> response = client.modify_cloud_to_device_config(name, binary_data)

        Args:
            name (str): The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
            binary_data (bytes): The configuration data for the device.
            version_to_update (long): The version number to update. If this value is zero, it will not check the
                version number of the server and will always update the current version;
                otherwise, this update will fail if the version number found on the server
                does not match this version number. This is used to support multiple
                simultaneous updates without losing data.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.DeviceConfig` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "modify_cloud_to_device_config" not in self._inner_api_calls:
            self._inner_api_calls[
                "modify_cloud_to_device_config"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.modify_cloud_to_device_config,
                default_retry=self._method_configs["ModifyCloudToDeviceConfig"].retry,
                default_timeout=self._method_configs[
                    "ModifyCloudToDeviceConfig"
                ].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ModifyCloudToDeviceConfigRequest(
            name=name, binary_data=binary_data, version_to_update=version_to_update
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["modify_cloud_to_device_config"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_device_config_versions(
        self,
        name,
        num_versions=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the last few versions of the device configuration in descending
        order (i.e.: newest first).

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> response = client.list_device_config_versions(name)

        Args:
            name (str): The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
            num_versions (int): The number of versions to list. Versions are listed in decreasing order of
                the version number. The maximum number of versions retained is 10. If this
                value is zero, it will return all the versions available.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.ListDeviceConfigVersionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_device_config_versions" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_device_config_versions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_device_config_versions,
                default_retry=self._method_configs["ListDeviceConfigVersions"].retry,
                default_timeout=self._method_configs[
                    "ListDeviceConfigVersions"
                ].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ListDeviceConfigVersionsRequest(
            name=name, num_versions=num_versions
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["list_device_config_versions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_device_states(
        self,
        name,
        num_states=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the last few versions of the device state in descending order (i.e.:
        newest first).

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> response = client.list_device_states(name)

        Args:
            name (str): The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
            num_states (int): The number of states to list. States are listed in descending order of
                update time. The maximum number of states retained is 10. If this
                value is zero, it will return all the states available.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.ListDeviceStatesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_device_states" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_device_states"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_device_states,
                default_retry=self._method_configs["ListDeviceStates"].retry,
                default_timeout=self._method_configs["ListDeviceStates"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.ListDeviceStatesRequest(
            name=name, num_states=num_states
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["list_device_states"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def set_iam_policy(
        self,
        resource,
        policy,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sets the access control policy on the specified resource. Replaces any
        existing policy.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> resource = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # TODO: Initialize `policy`:
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.iot_v1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The
                size of the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iot_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "set_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "set_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.set_iam_policy,
                default_retry=self._method_configs["SetIamPolicy"].retry,
                default_timeout=self._method_configs["SetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.SetIamPolicyRequest(resource=resource, policy=policy)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["set_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def get_iam_policy(
        self,
        resource,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does not have a policy
        set.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> resource = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "get_iam_policy" not in self._inner_api_calls:
            self._inner_api_calls[
                "get_iam_policy"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_iam_policy,
                default_retry=self._method_configs["GetIamPolicy"].retry,
                default_timeout=self._method_configs["GetIamPolicy"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["get_iam_policy"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def test_iam_permissions(
        self,
        resource,
        permissions,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Returns permissions that a caller has on the specified resource. If the
        resource does not exist, this will return an empty set of permissions,
        not a NOT\_FOUND error.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> resource = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # TODO: Initialize `permissions`:
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "test_iam_permissions" not in self._inner_api_calls:
            self._inner_api_calls[
                "test_iam_permissions"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.test_iam_permissions,
                default_retry=self._method_configs["TestIamPermissions"].retry,
                default_timeout=self._method_configs["TestIamPermissions"].timeout,
                client_info=self._client_info,
            )

        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("resource", resource)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["test_iam_permissions"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def send_command_to_device(
        self,
        name,
        binary_data,
        subfolder=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sends a command to the specified device. In order for a device to be
        able to receive commands, it must: 1) be connected to Cloud IoT Core
        using the MQTT protocol, and 2) be subscribed to the group of MQTT
        topics specified by /devices/{device-id}/commands/#. This subscription
        will receive commands at the top-level topic
        /devices/{device-id}/commands as well as commands for subfolders, like
        /devices/{device-id}/commands/subfolder. Note that subscribing to
        specific subfolders is not supported. If the command could not be
        delivered to the device, this method will return an error; in
        particular, if the device is not subscribed, this method will return
        FAILED\_PRECONDITION. Otherwise, this method will return OK. If the
        subscription is QoS 1, at least once delivery will be guaranteed; for
        QoS 0, no acknowledgment will be expected from the device.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> name = client.device_path('[PROJECT]', '[LOCATION]', '[REGISTRY]', '[DEVICE]')
            >>>
            >>> # TODO: Initialize `binary_data`:
            >>> binary_data = b''
            >>>
            >>> response = client.send_command_to_device(name, binary_data)

        Args:
            name (str): The name of the device. For example,
                ``projects/p0/locations/us-central1/registries/registry0/devices/device0``
                or
                ``projects/p0/locations/us-central1/registries/registry0/devices/{num_id}``.
            binary_data (bytes): The command data to send to the device.
            subfolder (str): Optional subfolder for the command. If empty, the command will be delivered
                to the /devices/{device-id}/commands topic, otherwise it will be delivered
                to the /devices/{device-id}/commands/{subfolder} topic. Multi-level
                subfolders are allowed. This field must not have more than 256 characters,
                and must not contain any MQTT wildcards ("+" or "#") or null characters.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.SendCommandToDeviceResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "send_command_to_device" not in self._inner_api_calls:
            self._inner_api_calls[
                "send_command_to_device"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.send_command_to_device,
                default_retry=self._method_configs["SendCommandToDevice"].retry,
                default_timeout=self._method_configs["SendCommandToDevice"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.SendCommandToDeviceRequest(
            name=name, binary_data=binary_data, subfolder=subfolder
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["send_command_to_device"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def bind_device_to_gateway(
        self,
        parent,
        gateway_id,
        device_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Associates the device with the gateway.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # TODO: Initialize `gateway_id`:
            >>> gateway_id = ''
            >>>
            >>> # TODO: Initialize `device_id`:
            >>> device_id = ''
            >>>
            >>> response = client.bind_device_to_gateway(parent, gateway_id, device_id)

        Args:
            parent (str): The name of the registry. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.
            gateway_id (str): The value of ``gateway_id`` can be either the device numeric ID or the
                user-defined device identifier.
            device_id (str): The device to associate with the specified gateway. The value of
                ``device_id`` can be either the device numeric ID or the user-defined
                device identifier.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.BindDeviceToGatewayResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "bind_device_to_gateway" not in self._inner_api_calls:
            self._inner_api_calls[
                "bind_device_to_gateway"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.bind_device_to_gateway,
                default_retry=self._method_configs["BindDeviceToGateway"].retry,
                default_timeout=self._method_configs["BindDeviceToGateway"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.BindDeviceToGatewayRequest(
            parent=parent, gateway_id=gateway_id, device_id=device_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["bind_device_to_gateway"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def unbind_device_from_gateway(
        self,
        parent,
        gateway_id,
        device_id,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes the association between the device and the gateway.

        Example:
            >>> from google.cloud import iot_v1
            >>>
            >>> client = iot_v1.DeviceManagerClient()
            >>>
            >>> parent = client.registry_path('[PROJECT]', '[LOCATION]', '[REGISTRY]')
            >>>
            >>> # TODO: Initialize `gateway_id`:
            >>> gateway_id = ''
            >>>
            >>> # TODO: Initialize `device_id`:
            >>> device_id = ''
            >>>
            >>> response = client.unbind_device_from_gateway(parent, gateway_id, device_id)

        Args:
            parent (str): The name of the registry. For example,
                ``projects/example-project/locations/us-central1/registries/my-registry``.
            gateway_id (str): The value of ``gateway_id`` can be either the device numeric ID or the
                user-defined device identifier.
            device_id (str): The device to disassociate from the specified gateway. The value of
                ``device_id`` can be either the device numeric ID or the user-defined
                device identifier.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iot_v1.types.UnbindDeviceFromGatewayResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "unbind_device_from_gateway" not in self._inner_api_calls:
            self._inner_api_calls[
                "unbind_device_from_gateway"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.unbind_device_from_gateway,
                default_retry=self._method_configs["UnbindDeviceFromGateway"].retry,
                default_timeout=self._method_configs["UnbindDeviceFromGateway"].timeout,
                client_info=self._client_info,
            )

        request = device_manager_pb2.UnbindDeviceFromGatewayRequest(
            parent=parent, gateway_id=gateway_id, device_id=device_id
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["unbind_device_from_gateway"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
