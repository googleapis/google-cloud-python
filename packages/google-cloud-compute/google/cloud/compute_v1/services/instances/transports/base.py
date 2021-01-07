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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.compute_v1.types import compute


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-compute",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class InstancesTransport(abc.ABC):
    """Abstract transport class for Instances."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/compute",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.add_access_config: gapic_v1.method.wrap_method(
                self.add_access_config, default_timeout=None, client_info=client_info,
            ),
            self.add_resource_policies: gapic_v1.method.wrap_method(
                self.add_resource_policies,
                default_timeout=None,
                client_info=client_info,
            ),
            self.aggregated_list: gapic_v1.method.wrap_method(
                self.aggregated_list, default_timeout=None, client_info=client_info,
            ),
            self.attach_disk: gapic_v1.method.wrap_method(
                self.attach_disk, default_timeout=None, client_info=client_info,
            ),
            self.delete: gapic_v1.method.wrap_method(
                self.delete, default_timeout=None, client_info=client_info,
            ),
            self.delete_access_config: gapic_v1.method.wrap_method(
                self.delete_access_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.detach_disk: gapic_v1.method.wrap_method(
                self.detach_disk, default_timeout=None, client_info=client_info,
            ),
            self.get: gapic_v1.method.wrap_method(
                self.get, default_timeout=None, client_info=client_info,
            ),
            self.get_guest_attributes: gapic_v1.method.wrap_method(
                self.get_guest_attributes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy, default_timeout=None, client_info=client_info,
            ),
            self.get_screenshot: gapic_v1.method.wrap_method(
                self.get_screenshot, default_timeout=None, client_info=client_info,
            ),
            self.get_serial_port_output: gapic_v1.method.wrap_method(
                self.get_serial_port_output,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_shielded_instance_identity: gapic_v1.method.wrap_method(
                self.get_shielded_instance_identity,
                default_timeout=None,
                client_info=client_info,
            ),
            self.insert: gapic_v1.method.wrap_method(
                self.insert, default_timeout=None, client_info=client_info,
            ),
            self.list: gapic_v1.method.wrap_method(
                self.list, default_timeout=None, client_info=client_info,
            ),
            self.list_referrers: gapic_v1.method.wrap_method(
                self.list_referrers, default_timeout=None, client_info=client_info,
            ),
            self.remove_resource_policies: gapic_v1.method.wrap_method(
                self.remove_resource_policies,
                default_timeout=None,
                client_info=client_info,
            ),
            self.reset: gapic_v1.method.wrap_method(
                self.reset, default_timeout=None, client_info=client_info,
            ),
            self.set_deletion_protection: gapic_v1.method.wrap_method(
                self.set_deletion_protection,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_disk_auto_delete: gapic_v1.method.wrap_method(
                self.set_disk_auto_delete,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=None, client_info=client_info,
            ),
            self.set_labels: gapic_v1.method.wrap_method(
                self.set_labels, default_timeout=None, client_info=client_info,
            ),
            self.set_machine_resources: gapic_v1.method.wrap_method(
                self.set_machine_resources,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_machine_type: gapic_v1.method.wrap_method(
                self.set_machine_type, default_timeout=None, client_info=client_info,
            ),
            self.set_metadata: gapic_v1.method.wrap_method(
                self.set_metadata, default_timeout=None, client_info=client_info,
            ),
            self.set_min_cpu_platform: gapic_v1.method.wrap_method(
                self.set_min_cpu_platform,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_scheduling: gapic_v1.method.wrap_method(
                self.set_scheduling, default_timeout=None, client_info=client_info,
            ),
            self.set_service_account: gapic_v1.method.wrap_method(
                self.set_service_account, default_timeout=None, client_info=client_info,
            ),
            self.set_shielded_instance_integrity_policy: gapic_v1.method.wrap_method(
                self.set_shielded_instance_integrity_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_tags: gapic_v1.method.wrap_method(
                self.set_tags, default_timeout=None, client_info=client_info,
            ),
            self.simulate_maintenance_event: gapic_v1.method.wrap_method(
                self.simulate_maintenance_event,
                default_timeout=None,
                client_info=client_info,
            ),
            self.start: gapic_v1.method.wrap_method(
                self.start, default_timeout=None, client_info=client_info,
            ),
            self.start_with_encryption_key: gapic_v1.method.wrap_method(
                self.start_with_encryption_key,
                default_timeout=None,
                client_info=client_info,
            ),
            self.stop: gapic_v1.method.wrap_method(
                self.stop, default_timeout=None, client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update: gapic_v1.method.wrap_method(
                self.update, default_timeout=None, client_info=client_info,
            ),
            self.update_access_config: gapic_v1.method.wrap_method(
                self.update_access_config,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_display_device: gapic_v1.method.wrap_method(
                self.update_display_device,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_network_interface: gapic_v1.method.wrap_method(
                self.update_network_interface,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_shielded_instance_config: gapic_v1.method.wrap_method(
                self.update_shielded_instance_config,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def add_access_config(
        self,
    ) -> typing.Callable[
        [compute.AddAccessConfigInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def add_resource_policies(
        self,
    ) -> typing.Callable[
        [compute.AddResourcePoliciesInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def aggregated_list(
        self,
    ) -> typing.Callable[
        [compute.AggregatedListInstancesRequest],
        typing.Union[
            compute.InstanceAggregatedList,
            typing.Awaitable[compute.InstanceAggregatedList],
        ],
    ]:
        raise NotImplementedError()

    @property
    def attach_disk(
        self,
    ) -> typing.Callable[
        [compute.AttachDiskInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete(
        self,
    ) -> typing.Callable[
        [compute.DeleteInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_access_config(
        self,
    ) -> typing.Callable[
        [compute.DeleteAccessConfigInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def detach_disk(
        self,
    ) -> typing.Callable[
        [compute.DetachDiskInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get(
        self,
    ) -> typing.Callable[
        [compute.GetInstanceRequest],
        typing.Union[compute.Instance, typing.Awaitable[compute.Instance]],
    ]:
        raise NotImplementedError()

    @property
    def get_guest_attributes(
        self,
    ) -> typing.Callable[
        [compute.GetGuestAttributesInstanceRequest],
        typing.Union[
            compute.GuestAttributes, typing.Awaitable[compute.GuestAttributes]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> typing.Callable[
        [compute.GetIamPolicyInstanceRequest],
        typing.Union[compute.Policy, typing.Awaitable[compute.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_screenshot(
        self,
    ) -> typing.Callable[
        [compute.GetScreenshotInstanceRequest],
        typing.Union[compute.Screenshot, typing.Awaitable[compute.Screenshot]],
    ]:
        raise NotImplementedError()

    @property
    def get_serial_port_output(
        self,
    ) -> typing.Callable[
        [compute.GetSerialPortOutputInstanceRequest],
        typing.Union[
            compute.SerialPortOutput, typing.Awaitable[compute.SerialPortOutput]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_shielded_instance_identity(
        self,
    ) -> typing.Callable[
        [compute.GetShieldedInstanceIdentityInstanceRequest],
        typing.Union[
            compute.ShieldedInstanceIdentity,
            typing.Awaitable[compute.ShieldedInstanceIdentity],
        ],
    ]:
        raise NotImplementedError()

    @property
    def insert(
        self,
    ) -> typing.Callable[
        [compute.InsertInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list(
        self,
    ) -> typing.Callable[
        [compute.ListInstancesRequest],
        typing.Union[compute.InstanceList, typing.Awaitable[compute.InstanceList]],
    ]:
        raise NotImplementedError()

    @property
    def list_referrers(
        self,
    ) -> typing.Callable[
        [compute.ListReferrersInstancesRequest],
        typing.Union[
            compute.InstanceListReferrers,
            typing.Awaitable[compute.InstanceListReferrers],
        ],
    ]:
        raise NotImplementedError()

    @property
    def remove_resource_policies(
        self,
    ) -> typing.Callable[
        [compute.RemoveResourcePoliciesInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def reset(
        self,
    ) -> typing.Callable[
        [compute.ResetInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_deletion_protection(
        self,
    ) -> typing.Callable[
        [compute.SetDeletionProtectionInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_disk_auto_delete(
        self,
    ) -> typing.Callable[
        [compute.SetDiskAutoDeleteInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> typing.Callable[
        [compute.SetIamPolicyInstanceRequest],
        typing.Union[compute.Policy, typing.Awaitable[compute.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def set_labels(
        self,
    ) -> typing.Callable[
        [compute.SetLabelsInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_machine_resources(
        self,
    ) -> typing.Callable[
        [compute.SetMachineResourcesInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_machine_type(
        self,
    ) -> typing.Callable[
        [compute.SetMachineTypeInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_metadata(
        self,
    ) -> typing.Callable[
        [compute.SetMetadataInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_min_cpu_platform(
        self,
    ) -> typing.Callable[
        [compute.SetMinCpuPlatformInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_scheduling(
        self,
    ) -> typing.Callable[
        [compute.SetSchedulingInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_service_account(
        self,
    ) -> typing.Callable[
        [compute.SetServiceAccountInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_shielded_instance_integrity_policy(
        self,
    ) -> typing.Callable[
        [compute.SetShieldedInstanceIntegrityPolicyInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_tags(
        self,
    ) -> typing.Callable[
        [compute.SetTagsInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def simulate_maintenance_event(
        self,
    ) -> typing.Callable[
        [compute.SimulateMaintenanceEventInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start(
        self,
    ) -> typing.Callable[
        [compute.StartInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start_with_encryption_key(
        self,
    ) -> typing.Callable[
        [compute.StartWithEncryptionKeyInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def stop(
        self,
    ) -> typing.Callable[
        [compute.StopInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> typing.Callable[
        [compute.TestIamPermissionsInstanceRequest],
        typing.Union[
            compute.TestPermissionsResponse,
            typing.Awaitable[compute.TestPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update(
        self,
    ) -> typing.Callable[
        [compute.UpdateInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_access_config(
        self,
    ) -> typing.Callable[
        [compute.UpdateAccessConfigInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_display_device(
        self,
    ) -> typing.Callable[
        [compute.UpdateDisplayDeviceInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_network_interface(
        self,
    ) -> typing.Callable[
        [compute.UpdateNetworkInterfaceInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_shielded_instance_config(
        self,
    ) -> typing.Callable[
        [compute.UpdateShieldedInstanceConfigInstanceRequest],
        typing.Union[compute.Operation, typing.Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()


__all__ = ("InstancesTransport",)
