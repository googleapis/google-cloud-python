# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.bare_metal_solution_v2.types import nfs_share as gcb_nfs_share
from google.cloud.bare_metal_solution_v2.types import (
    volume_snapshot as gcb_volume_snapshot,
)
from google.cloud.bare_metal_solution_v2.types import instance
from google.cloud.bare_metal_solution_v2.types import instance as gcb_instance
from google.cloud.bare_metal_solution_v2.types import lun
from google.cloud.bare_metal_solution_v2.types import network
from google.cloud.bare_metal_solution_v2.types import network as gcb_network
from google.cloud.bare_metal_solution_v2.types import nfs_share
from google.cloud.bare_metal_solution_v2.types import osimage, provisioning
from google.cloud.bare_metal_solution_v2.types import ssh_key
from google.cloud.bare_metal_solution_v2.types import ssh_key as gcb_ssh_key
from google.cloud.bare_metal_solution_v2.types import volume
from google.cloud.bare_metal_solution_v2.types import volume as gcb_volume
from google.cloud.bare_metal_solution_v2.types import volume_snapshot

from .base import BareMetalSolutionTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class BareMetalSolutionRestInterceptor:
    """Interceptor for BareMetalSolution.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BareMetalSolutionRestTransport.

    .. code-block:: python
        class MyCustomBareMetalSolutionInterceptor(BareMetalSolutionRestInterceptor):
            def pre_create_nfs_share(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_nfs_share(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_provisioning_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_provisioning_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_ssh_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_ssh_key(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_volume_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_volume_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_nfs_share(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_nfs_share(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_ssh_key(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_volume_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_detach_lun(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_detach_lun(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_disable_interactive_serial_console(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_disable_interactive_serial_console(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_enable_interactive_serial_console(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_enable_interactive_serial_console(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_evict_lun(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_evict_lun(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_evict_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_evict_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_lun(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_lun(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_nfs_share(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_nfs_share(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_provisioning_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_provisioning_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_volume_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_volume_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_instances(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_instances(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_luns(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_luns(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_networks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_networks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_network_usage(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_network_usage(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_nfs_shares(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_nfs_shares(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_os_images(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_os_images(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_provisioning_quotas(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_provisioning_quotas(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_ssh_keys(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_ssh_keys(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_volumes(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_volumes(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_volume_snapshots(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_volume_snapshots(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rename_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rename_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rename_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rename_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rename_nfs_share(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rename_nfs_share(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rename_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rename_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_reset_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_reset_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_resize_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_resize_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_restore_volume_snapshot(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_restore_volume_snapshot(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_submit_provisioning_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_submit_provisioning_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_instance(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_instance(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_network(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_network(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_nfs_share(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_nfs_share(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_provisioning_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_provisioning_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_volume(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_volume(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = BareMetalSolutionRestTransport(interceptor=MyCustomBareMetalSolutionInterceptor())
        client = BareMetalSolutionClient(transport=transport)


    """

    def pre_create_nfs_share(
        self,
        request: gcb_nfs_share.CreateNfsShareRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcb_nfs_share.CreateNfsShareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_nfs_share

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_create_nfs_share(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_nfs_share

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_create_provisioning_config(
        self,
        request: provisioning.CreateProvisioningConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[provisioning.CreateProvisioningConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_provisioning_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_create_provisioning_config(
        self, response: provisioning.ProvisioningConfig
    ) -> provisioning.ProvisioningConfig:
        """Post-rpc interceptor for create_provisioning_config

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_create_ssh_key(
        self,
        request: gcb_ssh_key.CreateSSHKeyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcb_ssh_key.CreateSSHKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_ssh_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_create_ssh_key(self, response: gcb_ssh_key.SSHKey) -> gcb_ssh_key.SSHKey:
        """Post-rpc interceptor for create_ssh_key

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_create_volume_snapshot(
        self,
        request: gcb_volume_snapshot.CreateVolumeSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcb_volume_snapshot.CreateVolumeSnapshotRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_volume_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_create_volume_snapshot(
        self, response: gcb_volume_snapshot.VolumeSnapshot
    ) -> gcb_volume_snapshot.VolumeSnapshot:
        """Post-rpc interceptor for create_volume_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_delete_nfs_share(
        self,
        request: nfs_share.DeleteNfsShareRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[nfs_share.DeleteNfsShareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_nfs_share

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_delete_nfs_share(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_nfs_share

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_delete_ssh_key(
        self, request: ssh_key.DeleteSSHKeyRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[ssh_key.DeleteSSHKeyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_ssh_key

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def pre_delete_volume_snapshot(
        self,
        request: volume_snapshot.DeleteVolumeSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[volume_snapshot.DeleteVolumeSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_volume_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def pre_detach_lun(
        self,
        request: gcb_instance.DetachLunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcb_instance.DetachLunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for detach_lun

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_detach_lun(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for detach_lun

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_disable_interactive_serial_console(
        self,
        request: instance.DisableInteractiveSerialConsoleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        instance.DisableInteractiveSerialConsoleRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for disable_interactive_serial_console

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_disable_interactive_serial_console(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for disable_interactive_serial_console

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_enable_interactive_serial_console(
        self,
        request: instance.EnableInteractiveSerialConsoleRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        instance.EnableInteractiveSerialConsoleRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for enable_interactive_serial_console

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_enable_interactive_serial_console(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for enable_interactive_serial_console

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_evict_lun(
        self, request: lun.EvictLunRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lun.EvictLunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for evict_lun

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_evict_lun(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for evict_lun

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_evict_volume(
        self, request: volume.EvictVolumeRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[volume.EvictVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for evict_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_evict_volume(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for evict_volume

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_get_instance(
        self, request: instance.GetInstanceRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[instance.GetInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_get_instance(self, response: instance.Instance) -> instance.Instance:
        """Post-rpc interceptor for get_instance

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_get_lun(
        self, request: lun.GetLunRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lun.GetLunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_lun

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_get_lun(self, response: lun.Lun) -> lun.Lun:
        """Post-rpc interceptor for get_lun

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_get_network(
        self, request: network.GetNetworkRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[network.GetNetworkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_get_network(self, response: network.Network) -> network.Network:
        """Post-rpc interceptor for get_network

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_get_nfs_share(
        self, request: nfs_share.GetNfsShareRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[nfs_share.GetNfsShareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_nfs_share

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_get_nfs_share(self, response: nfs_share.NfsShare) -> nfs_share.NfsShare:
        """Post-rpc interceptor for get_nfs_share

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_get_provisioning_config(
        self,
        request: provisioning.GetProvisioningConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[provisioning.GetProvisioningConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_provisioning_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_get_provisioning_config(
        self, response: provisioning.ProvisioningConfig
    ) -> provisioning.ProvisioningConfig:
        """Post-rpc interceptor for get_provisioning_config

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_get_volume(
        self, request: volume.GetVolumeRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[volume.GetVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_get_volume(self, response: volume.Volume) -> volume.Volume:
        """Post-rpc interceptor for get_volume

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_get_volume_snapshot(
        self,
        request: volume_snapshot.GetVolumeSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[volume_snapshot.GetVolumeSnapshotRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_volume_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_get_volume_snapshot(
        self, response: volume_snapshot.VolumeSnapshot
    ) -> volume_snapshot.VolumeSnapshot:
        """Post-rpc interceptor for get_volume_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_instances(
        self,
        request: instance.ListInstancesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[instance.ListInstancesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_instances

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_instances(
        self, response: instance.ListInstancesResponse
    ) -> instance.ListInstancesResponse:
        """Post-rpc interceptor for list_instances

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_luns(
        self, request: lun.ListLunsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[lun.ListLunsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_luns

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_luns(self, response: lun.ListLunsResponse) -> lun.ListLunsResponse:
        """Post-rpc interceptor for list_luns

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_networks(
        self, request: network.ListNetworksRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[network.ListNetworksRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_networks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_networks(
        self, response: network.ListNetworksResponse
    ) -> network.ListNetworksResponse:
        """Post-rpc interceptor for list_networks

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_network_usage(
        self,
        request: network.ListNetworkUsageRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[network.ListNetworkUsageRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_network_usage

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_network_usage(
        self, response: network.ListNetworkUsageResponse
    ) -> network.ListNetworkUsageResponse:
        """Post-rpc interceptor for list_network_usage

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_nfs_shares(
        self,
        request: nfs_share.ListNfsSharesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[nfs_share.ListNfsSharesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_nfs_shares

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_nfs_shares(
        self, response: nfs_share.ListNfsSharesResponse
    ) -> nfs_share.ListNfsSharesResponse:
        """Post-rpc interceptor for list_nfs_shares

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_os_images(
        self, request: osimage.ListOSImagesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[osimage.ListOSImagesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_os_images

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_os_images(
        self, response: osimage.ListOSImagesResponse
    ) -> osimage.ListOSImagesResponse:
        """Post-rpc interceptor for list_os_images

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_provisioning_quotas(
        self,
        request: provisioning.ListProvisioningQuotasRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[provisioning.ListProvisioningQuotasRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_provisioning_quotas

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_provisioning_quotas(
        self, response: provisioning.ListProvisioningQuotasResponse
    ) -> provisioning.ListProvisioningQuotasResponse:
        """Post-rpc interceptor for list_provisioning_quotas

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_ssh_keys(
        self, request: ssh_key.ListSSHKeysRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[ssh_key.ListSSHKeysRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_ssh_keys

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_ssh_keys(
        self, response: ssh_key.ListSSHKeysResponse
    ) -> ssh_key.ListSSHKeysResponse:
        """Post-rpc interceptor for list_ssh_keys

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_volumes(
        self, request: volume.ListVolumesRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[volume.ListVolumesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_volumes

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_volumes(
        self, response: volume.ListVolumesResponse
    ) -> volume.ListVolumesResponse:
        """Post-rpc interceptor for list_volumes

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_volume_snapshots(
        self,
        request: volume_snapshot.ListVolumeSnapshotsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[volume_snapshot.ListVolumeSnapshotsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_volume_snapshots

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_volume_snapshots(
        self, response: volume_snapshot.ListVolumeSnapshotsResponse
    ) -> volume_snapshot.ListVolumeSnapshotsResponse:
        """Post-rpc interceptor for list_volume_snapshots

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_rename_instance(
        self,
        request: instance.RenameInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[instance.RenameInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rename_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_rename_instance(self, response: instance.Instance) -> instance.Instance:
        """Post-rpc interceptor for rename_instance

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_rename_network(
        self, request: network.RenameNetworkRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[network.RenameNetworkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rename_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_rename_network(self, response: network.Network) -> network.Network:
        """Post-rpc interceptor for rename_network

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_rename_nfs_share(
        self,
        request: nfs_share.RenameNfsShareRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[nfs_share.RenameNfsShareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rename_nfs_share

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_rename_nfs_share(self, response: nfs_share.NfsShare) -> nfs_share.NfsShare:
        """Post-rpc interceptor for rename_nfs_share

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_rename_volume(
        self, request: volume.RenameVolumeRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[volume.RenameVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rename_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_rename_volume(self, response: volume.Volume) -> volume.Volume:
        """Post-rpc interceptor for rename_volume

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_reset_instance(
        self,
        request: instance.ResetInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[instance.ResetInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for reset_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_reset_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for reset_instance

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_resize_volume(
        self,
        request: gcb_volume.ResizeVolumeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcb_volume.ResizeVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for resize_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_resize_volume(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for resize_volume

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_restore_volume_snapshot(
        self,
        request: gcb_volume_snapshot.RestoreVolumeSnapshotRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        gcb_volume_snapshot.RestoreVolumeSnapshotRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for restore_volume_snapshot

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_restore_volume_snapshot(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for restore_volume_snapshot

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_start_instance(
        self,
        request: instance.StartInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[instance.StartInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for start_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_start_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for start_instance

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_stop_instance(
        self, request: instance.StopInstanceRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[instance.StopInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for stop_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_stop_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for stop_instance

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_submit_provisioning_config(
        self,
        request: provisioning.SubmitProvisioningConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[provisioning.SubmitProvisioningConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for submit_provisioning_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_submit_provisioning_config(
        self, response: provisioning.SubmitProvisioningConfigResponse
    ) -> provisioning.SubmitProvisioningConfigResponse:
        """Post-rpc interceptor for submit_provisioning_config

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_update_instance(
        self,
        request: gcb_instance.UpdateInstanceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcb_instance.UpdateInstanceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_instance

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_update_instance(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_instance

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_update_network(
        self,
        request: gcb_network.UpdateNetworkRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcb_network.UpdateNetworkRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_network

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_update_network(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_network

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_update_nfs_share(
        self,
        request: gcb_nfs_share.UpdateNfsShareRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcb_nfs_share.UpdateNfsShareRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_nfs_share

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_update_nfs_share(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_nfs_share

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_update_provisioning_config(
        self,
        request: provisioning.UpdateProvisioningConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[provisioning.UpdateProvisioningConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_provisioning_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_update_provisioning_config(
        self, response: provisioning.ProvisioningConfig
    ) -> provisioning.ProvisioningConfig:
        """Post-rpc interceptor for update_provisioning_config

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_update_volume(
        self,
        request: gcb_volume.UpdateVolumeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gcb_volume.UpdateVolumeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_volume

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_update_volume(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_volume

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BareMetalSolution server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the BareMetalSolution server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BareMetalSolutionRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BareMetalSolutionRestInterceptor


class BareMetalSolutionRestTransport(BareMetalSolutionTransport):
    """REST backend transport for BareMetalSolution.

    Performs management operations on Bare Metal Solution servers.

    The ``baremetalsolution.googleapis.com`` service provides management
    capabilities for Bare Metal Solution servers. To access the API
    methods, you must assign Bare Metal Solution IAM roles containing
    the desired permissions to your staff in your Google Cloud project.
    You must also enable the Bare Metal Solution API. Once enabled, the
    methods act upon specific servers in your Bare Metal Solution
    environment.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "baremetalsolution.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[BareMetalSolutionRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'baremetalsolution.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or BareMetalSolutionRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {}

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateNfsShare(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("CreateNfsShare")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_nfs_share.CreateNfsShareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create nfs share method over HTTP.

            Args:
                request (~.gcb_nfs_share.CreateNfsShareRequest):
                    The request object. Message for creating an NFS share.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/nfsShares",
                    "body": "nfs_share",
                },
            ]
            request, metadata = self._interceptor.pre_create_nfs_share(
                request, metadata
            )
            pb_request = gcb_nfs_share.CreateNfsShareRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_nfs_share(resp)
            return resp

    class _CreateProvisioningConfig(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("CreateProvisioningConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: provisioning.CreateProvisioningConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> provisioning.ProvisioningConfig:
            r"""Call the create provisioning
            config method over HTTP.

                Args:
                    request (~.provisioning.CreateProvisioningConfigRequest):
                        The request object. Request for CreateProvisioningConfig.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.provisioning.ProvisioningConfig:
                        A provisioning configuration.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/provisioningConfigs",
                    "body": "provisioning_config",
                },
            ]
            request, metadata = self._interceptor.pre_create_provisioning_config(
                request, metadata
            )
            pb_request = provisioning.CreateProvisioningConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = provisioning.ProvisioningConfig()
            pb_resp = provisioning.ProvisioningConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_provisioning_config(resp)
            return resp

    class _CreateSSHKey(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("CreateSSHKey")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "sshKeyId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_ssh_key.CreateSSHKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcb_ssh_key.SSHKey:
            r"""Call the create ssh key method over HTTP.

            Args:
                request (~.gcb_ssh_key.CreateSSHKeyRequest):
                    The request object. Message for registering a public SSH
                key in a project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcb_ssh_key.SSHKey:
                    An SSH key, used for authorizing with
                the interactive serial console feature.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/sshKeys",
                    "body": "ssh_key",
                },
            ]
            request, metadata = self._interceptor.pre_create_ssh_key(request, metadata)
            pb_request = gcb_ssh_key.CreateSSHKeyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcb_ssh_key.SSHKey()
            pb_resp = gcb_ssh_key.SSHKey.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_ssh_key(resp)
            return resp

    class _CreateVolumeSnapshot(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("CreateVolumeSnapshot")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_volume_snapshot.CreateVolumeSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcb_volume_snapshot.VolumeSnapshot:
            r"""Call the create volume snapshot method over HTTP.

            Args:
                request (~.gcb_volume_snapshot.CreateVolumeSnapshotRequest):
                    The request object. Message for creating a volume
                snapshot.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcb_volume_snapshot.VolumeSnapshot:
                    A snapshot of a volume. Only boot
                volumes can have snapshots.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*/volumes/*}/snapshots",
                    "body": "volume_snapshot",
                },
            ]
            request, metadata = self._interceptor.pre_create_volume_snapshot(
                request, metadata
            )
            pb_request = gcb_volume_snapshot.CreateVolumeSnapshotRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gcb_volume_snapshot.VolumeSnapshot()
            pb_resp = gcb_volume_snapshot.VolumeSnapshot.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_volume_snapshot(resp)
            return resp

    class _DeleteNfsShare(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("DeleteNfsShare")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: nfs_share.DeleteNfsShareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete nfs share method over HTTP.

            Args:
                request (~.nfs_share.DeleteNfsShareRequest):
                    The request object. Message for deleting an NFS share.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/locations/*/nfsShares/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_nfs_share(
                request, metadata
            )
            pb_request = nfs_share.DeleteNfsShareRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_nfs_share(resp)
            return resp

    class _DeleteSSHKey(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("DeleteSSHKey")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: ssh_key.DeleteSSHKeyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete ssh key method over HTTP.

            Args:
                request (~.ssh_key.DeleteSSHKeyRequest):
                    The request object. Message for deleting an SSH key from
                a project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/locations/*/sshKeys/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_ssh_key(request, metadata)
            pb_request = ssh_key.DeleteSSHKeyRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteVolumeSnapshot(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("DeleteVolumeSnapshot")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: volume_snapshot.DeleteVolumeSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete volume snapshot method over HTTP.

            Args:
                request (~.volume_snapshot.DeleteVolumeSnapshotRequest):
                    The request object. Message for deleting named Volume
                snapshot.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/locations/*/volumes/*/snapshots/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_volume_snapshot(
                request, metadata
            )
            pb_request = volume_snapshot.DeleteVolumeSnapshotRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DetachLun(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("DetachLun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_instance.DetachLunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the detach lun method over HTTP.

            Args:
                request (~.gcb_instance.DetachLunRequest):
                    The request object. Message for detach specific LUN from
                an Instance.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{instance=projects/*/locations/*/instances/*}:detachLun",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_detach_lun(request, metadata)
            pb_request = gcb_instance.DetachLunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_detach_lun(resp)
            return resp

    class _DisableInteractiveSerialConsole(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("DisableInteractiveSerialConsole")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: instance.DisableInteractiveSerialConsoleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the disable interactive
            serial console method over HTTP.

                Args:
                    request (~.instance.DisableInteractiveSerialConsoleRequest):
                        The request object. Message for disabling the interactive
                    serial console on an instance.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/instances/*}:disableInteractiveSerialConsole",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_disable_interactive_serial_console(
                request, metadata
            )
            pb_request = instance.DisableInteractiveSerialConsoleRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_disable_interactive_serial_console(resp)
            return resp

    class _EnableInteractiveSerialConsole(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("EnableInteractiveSerialConsole")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: instance.EnableInteractiveSerialConsoleRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the enable interactive serial
            console method over HTTP.

                Args:
                    request (~.instance.EnableInteractiveSerialConsoleRequest):
                        The request object. Message for enabling the interactive
                    serial console on an instance.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.operations_pb2.Operation:
                        This resource represents a
                    long-running operation that is the
                    result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/instances/*}:enableInteractiveSerialConsole",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_enable_interactive_serial_console(
                request, metadata
            )
            pb_request = instance.EnableInteractiveSerialConsoleRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_enable_interactive_serial_console(resp)
            return resp

    class _EvictLun(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("EvictLun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lun.EvictLunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the evict lun method over HTTP.

            Args:
                request (~.lun.EvictLunRequest):
                    The request object. Request for skip lun cooloff and
                delete it.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/volumes/*/luns/*}:evict",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_evict_lun(request, metadata)
            pb_request = lun.EvictLunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_evict_lun(resp)
            return resp

    class _EvictVolume(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("EvictVolume")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: volume.EvictVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the evict volume method over HTTP.

            Args:
                request (~.volume.EvictVolumeRequest):
                    The request object. Request for skip volume cooloff and
                delete it.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/volumes/*}:evict",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_evict_volume(request, metadata)
            pb_request = volume.EvictVolumeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_evict_volume(resp)
            return resp

    class _GetInstance(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("GetInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: instance.GetInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> instance.Instance:
            r"""Call the get instance method over HTTP.

            Args:
                request (~.instance.GetInstanceRequest):
                    The request object. Message for requesting server
                information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.instance.Instance:
                    A server.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/instances/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_instance(request, metadata)
            pb_request = instance.GetInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = instance.Instance()
            pb_resp = instance.Instance.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_instance(resp)
            return resp

    class _GetLun(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("GetLun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lun.GetLunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lun.Lun:
            r"""Call the get lun method over HTTP.

            Args:
                request (~.lun.GetLunRequest):
                    The request object. Message for requesting storage lun
                information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lun.Lun:
                    A storage volume logical unit number
                (LUN).

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/volumes/*/luns/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_lun(request, metadata)
            pb_request = lun.GetLunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lun.Lun()
            pb_resp = lun.Lun.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_lun(resp)
            return resp

    class _GetNetwork(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("GetNetwork")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: network.GetNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> network.Network:
            r"""Call the get network method over HTTP.

            Args:
                request (~.network.GetNetworkRequest):
                    The request object. Message for requesting network
                information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.network.Network:
                    A Network.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/networks/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_network(request, metadata)
            pb_request = network.GetNetworkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = network.Network()
            pb_resp = network.Network.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_network(resp)
            return resp

    class _GetNfsShare(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("GetNfsShare")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: nfs_share.GetNfsShareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> nfs_share.NfsShare:
            r"""Call the get nfs share method over HTTP.

            Args:
                request (~.nfs_share.GetNfsShareRequest):
                    The request object. Message for requesting NFS share
                information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.nfs_share.NfsShare:
                    An NFS share.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/nfsShares/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_nfs_share(request, metadata)
            pb_request = nfs_share.GetNfsShareRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = nfs_share.NfsShare()
            pb_resp = nfs_share.NfsShare.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_nfs_share(resp)
            return resp

    class _GetProvisioningConfig(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("GetProvisioningConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: provisioning.GetProvisioningConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> provisioning.ProvisioningConfig:
            r"""Call the get provisioning config method over HTTP.

            Args:
                request (~.provisioning.GetProvisioningConfigRequest):
                    The request object. Request for GetProvisioningConfig.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.provisioning.ProvisioningConfig:
                    A provisioning configuration.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/provisioningConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_provisioning_config(
                request, metadata
            )
            pb_request = provisioning.GetProvisioningConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = provisioning.ProvisioningConfig()
            pb_resp = provisioning.ProvisioningConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_provisioning_config(resp)
            return resp

    class _GetVolume(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("GetVolume")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: volume.GetVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume.Volume:
            r"""Call the get volume method over HTTP.

            Args:
                request (~.volume.GetVolumeRequest):
                    The request object. Message for requesting storage volume
                information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume.Volume:
                    A storage volume.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/volumes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_volume(request, metadata)
            pb_request = volume.GetVolumeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = volume.Volume()
            pb_resp = volume.Volume.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_volume(resp)
            return resp

    class _GetVolumeSnapshot(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("GetVolumeSnapshot")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: volume_snapshot.GetVolumeSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume_snapshot.VolumeSnapshot:
            r"""Call the get volume snapshot method over HTTP.

            Args:
                request (~.volume_snapshot.GetVolumeSnapshotRequest):
                    The request object. Message for requesting volume
                snapshot information.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume_snapshot.VolumeSnapshot:
                    A snapshot of a volume. Only boot
                volumes can have snapshots.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/volumes/*/snapshots/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_volume_snapshot(
                request, metadata
            )
            pb_request = volume_snapshot.GetVolumeSnapshotRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = volume_snapshot.VolumeSnapshot()
            pb_resp = volume_snapshot.VolumeSnapshot.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_volume_snapshot(resp)
            return resp

    class _ListInstances(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListInstances")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: instance.ListInstancesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> instance.ListInstancesResponse:
            r"""Call the list instances method over HTTP.

            Args:
                request (~.instance.ListInstancesRequest):
                    The request object. Message for requesting the list of
                servers.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.instance.ListInstancesResponse:
                    Response message for the list of
                servers.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/instances",
                },
            ]
            request, metadata = self._interceptor.pre_list_instances(request, metadata)
            pb_request = instance.ListInstancesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = instance.ListInstancesResponse()
            pb_resp = instance.ListInstancesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_instances(resp)
            return resp

    class _ListLuns(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListLuns")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: lun.ListLunsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> lun.ListLunsResponse:
            r"""Call the list luns method over HTTP.

            Args:
                request (~.lun.ListLunsRequest):
                    The request object. Message for requesting a list of
                storage volume luns.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.lun.ListLunsResponse:
                    Response message containing the list
                of storage volume luns.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*/volumes/*}/luns",
                },
            ]
            request, metadata = self._interceptor.pre_list_luns(request, metadata)
            pb_request = lun.ListLunsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = lun.ListLunsResponse()
            pb_resp = lun.ListLunsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_luns(resp)
            return resp

    class _ListNetworks(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListNetworks")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: network.ListNetworksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> network.ListNetworksResponse:
            r"""Call the list networks method over HTTP.

            Args:
                request (~.network.ListNetworksRequest):
                    The request object. Message for requesting a list of
                networks.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.network.ListNetworksResponse:
                    Response message containing the list
                of networks.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/networks",
                },
            ]
            request, metadata = self._interceptor.pre_list_networks(request, metadata)
            pb_request = network.ListNetworksRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = network.ListNetworksResponse()
            pb_resp = network.ListNetworksResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_networks(resp)
            return resp

    class _ListNetworkUsage(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListNetworkUsage")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: network.ListNetworkUsageRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> network.ListNetworkUsageResponse:
            r"""Call the list network usage method over HTTP.

            Args:
                request (~.network.ListNetworkUsageRequest):
                    The request object. Request to get networks with IPs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.network.ListNetworkUsageResponse:
                    Response with Networks with IPs
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{location=projects/*/locations/*}/networks:listNetworkUsage",
                },
            ]
            request, metadata = self._interceptor.pre_list_network_usage(
                request, metadata
            )
            pb_request = network.ListNetworkUsageRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = network.ListNetworkUsageResponse()
            pb_resp = network.ListNetworkUsageResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_network_usage(resp)
            return resp

    class _ListNfsShares(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListNfsShares")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: nfs_share.ListNfsSharesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> nfs_share.ListNfsSharesResponse:
            r"""Call the list nfs shares method over HTTP.

            Args:
                request (~.nfs_share.ListNfsSharesRequest):
                    The request object. Message for requesting a list of NFS
                shares.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.nfs_share.ListNfsSharesResponse:
                    Response message containing the list
                of NFS shares.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/nfsShares",
                },
            ]
            request, metadata = self._interceptor.pre_list_nfs_shares(request, metadata)
            pb_request = nfs_share.ListNfsSharesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = nfs_share.ListNfsSharesResponse()
            pb_resp = nfs_share.ListNfsSharesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_nfs_shares(resp)
            return resp

    class _ListOSImages(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListOSImages")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: osimage.ListOSImagesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> osimage.ListOSImagesResponse:
            r"""Call the list os images method over HTTP.

            Args:
                request (~.osimage.ListOSImagesRequest):
                    The request object. Request for getting all available OS
                images.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.osimage.ListOSImagesResponse:
                    Request for getting all available OS
                images.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/osImages",
                },
            ]
            request, metadata = self._interceptor.pre_list_os_images(request, metadata)
            pb_request = osimage.ListOSImagesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = osimage.ListOSImagesResponse()
            pb_resp = osimage.ListOSImagesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_os_images(resp)
            return resp

    class _ListProvisioningQuotas(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListProvisioningQuotas")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: provisioning.ListProvisioningQuotasRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> provisioning.ListProvisioningQuotasResponse:
            r"""Call the list provisioning quotas method over HTTP.

            Args:
                request (~.provisioning.ListProvisioningQuotasRequest):
                    The request object. Message for requesting the list of
                provisioning quotas.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.provisioning.ListProvisioningQuotasResponse:
                    Response message for the list of
                provisioning quotas.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/provisioningQuotas",
                },
            ]
            request, metadata = self._interceptor.pre_list_provisioning_quotas(
                request, metadata
            )
            pb_request = provisioning.ListProvisioningQuotasRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = provisioning.ListProvisioningQuotasResponse()
            pb_resp = provisioning.ListProvisioningQuotasResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_provisioning_quotas(resp)
            return resp

    class _ListSSHKeys(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListSSHKeys")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: ssh_key.ListSSHKeysRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> ssh_key.ListSSHKeysResponse:
            r"""Call the list ssh keys method over HTTP.

            Args:
                request (~.ssh_key.ListSSHKeysRequest):
                    The request object. Message for listing the public SSH
                keys in a project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.ssh_key.ListSSHKeysResponse:
                    Message for response of ListSSHKeys.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/sshKeys",
                },
            ]
            request, metadata = self._interceptor.pre_list_ssh_keys(request, metadata)
            pb_request = ssh_key.ListSSHKeysRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = ssh_key.ListSSHKeysResponse()
            pb_resp = ssh_key.ListSSHKeysResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_ssh_keys(resp)
            return resp

    class _ListVolumes(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListVolumes")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: volume.ListVolumesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume.ListVolumesResponse:
            r"""Call the list volumes method over HTTP.

            Args:
                request (~.volume.ListVolumesRequest):
                    The request object. Message for requesting a list of
                storage volumes.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume.ListVolumesResponse:
                    Response message containing the list
                of storage volumes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/volumes",
                },
            ]
            request, metadata = self._interceptor.pre_list_volumes(request, metadata)
            pb_request = volume.ListVolumesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = volume.ListVolumesResponse()
            pb_resp = volume.ListVolumesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_volumes(resp)
            return resp

    class _ListVolumeSnapshots(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ListVolumeSnapshots")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: volume_snapshot.ListVolumeSnapshotsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume_snapshot.ListVolumeSnapshotsResponse:
            r"""Call the list volume snapshots method over HTTP.

            Args:
                request (~.volume_snapshot.ListVolumeSnapshotsRequest):
                    The request object. Message for requesting a list of
                volume snapshots.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume_snapshot.ListVolumeSnapshotsResponse:
                    Response message containing the list
                of volume snapshots.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*/volumes/*}/snapshots",
                },
            ]
            request, metadata = self._interceptor.pre_list_volume_snapshots(
                request, metadata
            )
            pb_request = volume_snapshot.ListVolumeSnapshotsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = volume_snapshot.ListVolumeSnapshotsResponse()
            pb_resp = volume_snapshot.ListVolumeSnapshotsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_volume_snapshots(resp)
            return resp

    class _RenameInstance(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("RenameInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: instance.RenameInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> instance.Instance:
            r"""Call the rename instance method over HTTP.

            Args:
                request (~.instance.RenameInstanceRequest):
                    The request object. Message requesting rename of a
                server.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.instance.Instance:
                    A server.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/instances/*}:rename",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rename_instance(request, metadata)
            pb_request = instance.RenameInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = instance.Instance()
            pb_resp = instance.Instance.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rename_instance(resp)
            return resp

    class _RenameNetwork(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("RenameNetwork")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: network.RenameNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> network.Network:
            r"""Call the rename network method over HTTP.

            Args:
                request (~.network.RenameNetworkRequest):
                    The request object. Message requesting rename of a
                server.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.network.Network:
                    A Network.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/networks/*}:rename",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rename_network(request, metadata)
            pb_request = network.RenameNetworkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = network.Network()
            pb_resp = network.Network.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rename_network(resp)
            return resp

    class _RenameNfsShare(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("RenameNfsShare")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: nfs_share.RenameNfsShareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> nfs_share.NfsShare:
            r"""Call the rename nfs share method over HTTP.

            Args:
                request (~.nfs_share.RenameNfsShareRequest):
                    The request object. Message requesting rename of a
                server.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.nfs_share.NfsShare:
                    An NFS share.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/nfsShares/*}:rename",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rename_nfs_share(
                request, metadata
            )
            pb_request = nfs_share.RenameNfsShareRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = nfs_share.NfsShare()
            pb_resp = nfs_share.NfsShare.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rename_nfs_share(resp)
            return resp

    class _RenameVolume(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("RenameVolume")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: volume.RenameVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume.Volume:
            r"""Call the rename volume method over HTTP.

            Args:
                request (~.volume.RenameVolumeRequest):
                    The request object. Message requesting rename of a
                server.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume.Volume:
                    A storage volume.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/volumes/*}:rename",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rename_volume(request, metadata)
            pb_request = volume.RenameVolumeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = volume.Volume()
            pb_resp = volume.Volume.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rename_volume(resp)
            return resp

    class _ResetInstance(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ResetInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: instance.ResetInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the reset instance method over HTTP.

            Args:
                request (~.instance.ResetInstanceRequest):
                    The request object. Message requesting to reset a server.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/instances/*}:reset",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_reset_instance(request, metadata)
            pb_request = instance.ResetInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_reset_instance(resp)
            return resp

    class _ResizeVolume(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("ResizeVolume")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_volume.ResizeVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the resize volume method over HTTP.

            Args:
                request (~.gcb_volume.ResizeVolumeRequest):
                    The request object. Request for emergency resize Volume.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{volume=projects/*/locations/*/volumes/*}:resize",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_resize_volume(request, metadata)
            pb_request = gcb_volume.ResizeVolumeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_resize_volume(resp)
            return resp

    class _RestoreVolumeSnapshot(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("RestoreVolumeSnapshot")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_volume_snapshot.RestoreVolumeSnapshotRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the restore volume snapshot method over HTTP.

            Args:
                request (~.gcb_volume_snapshot.RestoreVolumeSnapshotRequest):
                    The request object. Message for restoring a volume
                snapshot.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{volume_snapshot=projects/*/locations/*/volumes/*/snapshots/*}:restoreVolumeSnapshot",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_restore_volume_snapshot(
                request, metadata
            )
            pb_request = gcb_volume_snapshot.RestoreVolumeSnapshotRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_restore_volume_snapshot(resp)
            return resp

    class _StartInstance(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("StartInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: instance.StartInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the start instance method over HTTP.

            Args:
                request (~.instance.StartInstanceRequest):
                    The request object. Message requesting to start a server.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/instances/*}:start",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_start_instance(request, metadata)
            pb_request = instance.StartInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_start_instance(resp)
            return resp

    class _StopInstance(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("StopInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: instance.StopInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the stop instance method over HTTP.

            Args:
                request (~.instance.StopInstanceRequest):
                    The request object. Message requesting to stop a server.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/locations/*/instances/*}:stop",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_stop_instance(request, metadata)
            pb_request = instance.StopInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_stop_instance(resp)
            return resp

    class _SubmitProvisioningConfig(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("SubmitProvisioningConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: provisioning.SubmitProvisioningConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> provisioning.SubmitProvisioningConfigResponse:
            r"""Call the submit provisioning
            config method over HTTP.

                Args:
                    request (~.provisioning.SubmitProvisioningConfigRequest):
                        The request object. Request for SubmitProvisioningConfig.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.provisioning.SubmitProvisioningConfigResponse:
                        Response for
                    SubmitProvisioningConfig.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/provisioningConfigs:submit",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_submit_provisioning_config(
                request, metadata
            )
            pb_request = provisioning.SubmitProvisioningConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = provisioning.SubmitProvisioningConfigResponse()
            pb_resp = provisioning.SubmitProvisioningConfigResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_submit_provisioning_config(resp)
            return resp

    class _UpdateInstance(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("UpdateInstance")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_instance.UpdateInstanceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update instance method over HTTP.

            Args:
                request (~.gcb_instance.UpdateInstanceRequest):
                    The request object. Message requesting to updating a
                server.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{instance.name=projects/*/locations/*/instances/*}",
                    "body": "instance",
                },
            ]
            request, metadata = self._interceptor.pre_update_instance(request, metadata)
            pb_request = gcb_instance.UpdateInstanceRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_instance(resp)
            return resp

    class _UpdateNetwork(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("UpdateNetwork")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_network.UpdateNetworkRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update network method over HTTP.

            Args:
                request (~.gcb_network.UpdateNetworkRequest):
                    The request object. Message requesting to updating a
                network.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{network.name=projects/*/locations/*/networks/*}",
                    "body": "network",
                },
            ]
            request, metadata = self._interceptor.pre_update_network(request, metadata)
            pb_request = gcb_network.UpdateNetworkRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_network(resp)
            return resp

    class _UpdateNfsShare(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("UpdateNfsShare")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_nfs_share.UpdateNfsShareRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update nfs share method over HTTP.

            Args:
                request (~.gcb_nfs_share.UpdateNfsShareRequest):
                    The request object. Message requesting to updating an NFS
                share.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{nfs_share.name=projects/*/locations/*/nfsShares/*}",
                    "body": "nfs_share",
                },
            ]
            request, metadata = self._interceptor.pre_update_nfs_share(
                request, metadata
            )
            pb_request = gcb_nfs_share.UpdateNfsShareRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_nfs_share(resp)
            return resp

    class _UpdateProvisioningConfig(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("UpdateProvisioningConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: provisioning.UpdateProvisioningConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> provisioning.ProvisioningConfig:
            r"""Call the update provisioning
            config method over HTTP.

                Args:
                    request (~.provisioning.UpdateProvisioningConfigRequest):
                        The request object. Message for updating a
                    ProvisioningConfig.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.provisioning.ProvisioningConfig:
                        A provisioning configuration.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{provisioning_config.name=projects/*/locations/*/provisioningConfigs/*}",
                    "body": "provisioning_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_provisioning_config(
                request, metadata
            )
            pb_request = provisioning.UpdateProvisioningConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = provisioning.ProvisioningConfig()
            pb_resp = provisioning.ProvisioningConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_provisioning_config(resp)
            return resp

    class _UpdateVolume(BareMetalSolutionRestStub):
        def __hash__(self):
            return hash("UpdateVolume")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gcb_volume.UpdateVolumeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update volume method over HTTP.

            Args:
                request (~.gcb_volume.UpdateVolumeRequest):
                    The request object. Message for updating a volume.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{volume.name=projects/*/locations/*/volumes/*}",
                    "body": "volume",
                },
            ]
            request, metadata = self._interceptor.pre_update_volume(request, metadata)
            pb_request = gcb_volume.UpdateVolumeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_volume(resp)
            return resp

    @property
    def create_nfs_share(
        self,
    ) -> Callable[[gcb_nfs_share.CreateNfsShareRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateNfsShare(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_provisioning_config(
        self,
    ) -> Callable[
        [provisioning.CreateProvisioningConfigRequest], provisioning.ProvisioningConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateProvisioningConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_ssh_key(
        self,
    ) -> Callable[[gcb_ssh_key.CreateSSHKeyRequest], gcb_ssh_key.SSHKey]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSSHKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_volume_snapshot(
        self,
    ) -> Callable[
        [gcb_volume_snapshot.CreateVolumeSnapshotRequest],
        gcb_volume_snapshot.VolumeSnapshot,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateVolumeSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_nfs_share(
        self,
    ) -> Callable[[nfs_share.DeleteNfsShareRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteNfsShare(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_ssh_key(
        self,
    ) -> Callable[[ssh_key.DeleteSSHKeyRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSSHKey(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_volume_snapshot(
        self,
    ) -> Callable[[volume_snapshot.DeleteVolumeSnapshotRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteVolumeSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def detach_lun(
        self,
    ) -> Callable[[gcb_instance.DetachLunRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DetachLun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def disable_interactive_serial_console(
        self,
    ) -> Callable[
        [instance.DisableInteractiveSerialConsoleRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DisableInteractiveSerialConsole(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def enable_interactive_serial_console(
        self,
    ) -> Callable[
        [instance.EnableInteractiveSerialConsoleRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EnableInteractiveSerialConsole(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def evict_lun(self) -> Callable[[lun.EvictLunRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EvictLun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def evict_volume(
        self,
    ) -> Callable[[volume.EvictVolumeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._EvictVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_instance(
        self,
    ) -> Callable[[instance.GetInstanceRequest], instance.Instance]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_lun(self) -> Callable[[lun.GetLunRequest], lun.Lun]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetLun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_network(self) -> Callable[[network.GetNetworkRequest], network.Network]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_nfs_share(
        self,
    ) -> Callable[[nfs_share.GetNfsShareRequest], nfs_share.NfsShare]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNfsShare(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_provisioning_config(
        self,
    ) -> Callable[
        [provisioning.GetProvisioningConfigRequest], provisioning.ProvisioningConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProvisioningConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_volume(self) -> Callable[[volume.GetVolumeRequest], volume.Volume]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_volume_snapshot(
        self,
    ) -> Callable[
        [volume_snapshot.GetVolumeSnapshotRequest], volume_snapshot.VolumeSnapshot
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVolumeSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_instances(
        self,
    ) -> Callable[[instance.ListInstancesRequest], instance.ListInstancesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInstances(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_luns(self) -> Callable[[lun.ListLunsRequest], lun.ListLunsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListLuns(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_networks(
        self,
    ) -> Callable[[network.ListNetworksRequest], network.ListNetworksResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNetworks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_network_usage(
        self,
    ) -> Callable[[network.ListNetworkUsageRequest], network.ListNetworkUsageResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNetworkUsage(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_nfs_shares(
        self,
    ) -> Callable[[nfs_share.ListNfsSharesRequest], nfs_share.ListNfsSharesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNfsShares(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_os_images(
        self,
    ) -> Callable[[osimage.ListOSImagesRequest], osimage.ListOSImagesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListOSImages(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_provisioning_quotas(
        self,
    ) -> Callable[
        [provisioning.ListProvisioningQuotasRequest],
        provisioning.ListProvisioningQuotasResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProvisioningQuotas(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_ssh_keys(
        self,
    ) -> Callable[[ssh_key.ListSSHKeysRequest], ssh_key.ListSSHKeysResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSSHKeys(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_volumes(
        self,
    ) -> Callable[[volume.ListVolumesRequest], volume.ListVolumesResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVolumes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_volume_snapshots(
        self,
    ) -> Callable[
        [volume_snapshot.ListVolumeSnapshotsRequest],
        volume_snapshot.ListVolumeSnapshotsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVolumeSnapshots(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rename_instance(
        self,
    ) -> Callable[[instance.RenameInstanceRequest], instance.Instance]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RenameInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rename_network(
        self,
    ) -> Callable[[network.RenameNetworkRequest], network.Network]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RenameNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rename_nfs_share(
        self,
    ) -> Callable[[nfs_share.RenameNfsShareRequest], nfs_share.NfsShare]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RenameNfsShare(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rename_volume(self) -> Callable[[volume.RenameVolumeRequest], volume.Volume]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RenameVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def reset_instance(
        self,
    ) -> Callable[[instance.ResetInstanceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResetInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def resize_volume(
        self,
    ) -> Callable[[gcb_volume.ResizeVolumeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ResizeVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def restore_volume_snapshot(
        self,
    ) -> Callable[
        [gcb_volume_snapshot.RestoreVolumeSnapshotRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RestoreVolumeSnapshot(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_instance(
        self,
    ) -> Callable[[instance.StartInstanceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def stop_instance(
        self,
    ) -> Callable[[instance.StopInstanceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def submit_provisioning_config(
        self,
    ) -> Callable[
        [provisioning.SubmitProvisioningConfigRequest],
        provisioning.SubmitProvisioningConfigResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SubmitProvisioningConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_instance(
        self,
    ) -> Callable[[gcb_instance.UpdateInstanceRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateInstance(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_network(
        self,
    ) -> Callable[[gcb_network.UpdateNetworkRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateNetwork(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_nfs_share(
        self,
    ) -> Callable[[gcb_nfs_share.UpdateNfsShareRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateNfsShare(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_provisioning_config(
        self,
    ) -> Callable[
        [provisioning.UpdateProvisioningConfigRequest], provisioning.ProvisioningConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateProvisioningConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_volume(
        self,
    ) -> Callable[[gcb_volume.UpdateVolumeRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateVolume(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(BareMetalSolutionRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(BareMetalSolutionRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("BareMetalSolutionRestTransport",)
