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
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union

import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.compute_v1 import gapic_version as package_version
from google.cloud.compute_v1.services import zone_operations
from google.cloud.compute_v1.types import compute

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class InstanceGroupManagersTransport(abc.ABC):
    """Abstract transport class for InstanceGroupManagers."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/compute",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    DEFAULT_HOST: str = "compute.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'compute.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
        """
        self._extended_operations_services: Dict[str, Any] = {}

        scopes_kwargs = {"scopes": scopes, "default_scopes": self.AUTH_SCOPES}

        # Save the scopes.
        self._scopes = scopes
        if not hasattr(self, "_ignore_credentials"):
            self._ignore_credentials: bool = False

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )
        elif credentials is None and not self._ignore_credentials:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )
            # Don't apply audience if the credentials file passed from user.
            if hasattr(credentials, "with_gdch_audience"):
                credentials = credentials.with_gdch_audience(
                    api_audience if api_audience else host
                )

        # If the credentials are service account credentials, then always try to use self signed JWT.
        if (
            always_use_jwt_access
            and isinstance(credentials, service_account.Credentials)
            and hasattr(service_account.Credentials, "with_always_use_jwt_access")
        ):
            credentials = credentials.with_always_use_jwt_access(True)

        # Save the credentials.
        self._credentials = credentials

        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

    @property
    def host(self):
        return self._host

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.abandon_instances: gapic_v1.method.wrap_method(
                self.abandon_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.aggregated_list: gapic_v1.method.wrap_method(
                self.aggregated_list,
                default_timeout=None,
                client_info=client_info,
            ),
            self.apply_updates_to_instances: gapic_v1.method.wrap_method(
                self.apply_updates_to_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_instances: gapic_v1.method.wrap_method(
                self.create_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete: gapic_v1.method.wrap_method(
                self.delete,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_instances: gapic_v1.method.wrap_method(
                self.delete_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_per_instance_configs: gapic_v1.method.wrap_method(
                self.delete_per_instance_configs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get: gapic_v1.method.wrap_method(
                self.get,
                default_timeout=None,
                client_info=client_info,
            ),
            self.insert: gapic_v1.method.wrap_method(
                self.insert,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list: gapic_v1.method.wrap_method(
                self.list,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_errors: gapic_v1.method.wrap_method(
                self.list_errors,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_managed_instances: gapic_v1.method.wrap_method(
                self.list_managed_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_per_instance_configs: gapic_v1.method.wrap_method(
                self.list_per_instance_configs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.patch: gapic_v1.method.wrap_method(
                self.patch,
                default_timeout=None,
                client_info=client_info,
            ),
            self.patch_per_instance_configs: gapic_v1.method.wrap_method(
                self.patch_per_instance_configs,
                default_timeout=None,
                client_info=client_info,
            ),
            self.recreate_instances: gapic_v1.method.wrap_method(
                self.recreate_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.resize: gapic_v1.method.wrap_method(
                self.resize,
                default_timeout=None,
                client_info=client_info,
            ),
            self.resume_instances: gapic_v1.method.wrap_method(
                self.resume_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_instance_template: gapic_v1.method.wrap_method(
                self.set_instance_template,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_target_pools: gapic_v1.method.wrap_method(
                self.set_target_pools,
                default_timeout=None,
                client_info=client_info,
            ),
            self.start_instances: gapic_v1.method.wrap_method(
                self.start_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.stop_instances: gapic_v1.method.wrap_method(
                self.stop_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.suspend_instances: gapic_v1.method.wrap_method(
                self.suspend_instances,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_per_instance_configs: gapic_v1.method.wrap_method(
                self.update_per_instance_configs,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def abandon_instances(
        self,
    ) -> Callable[
        [compute.AbandonInstancesInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListInstanceGroupManagersRequest],
        Union[
            compute.InstanceGroupManagerAggregatedList,
            Awaitable[compute.InstanceGroupManagerAggregatedList],
        ],
    ]:
        raise NotImplementedError()

    @property
    def apply_updates_to_instances(
        self,
    ) -> Callable[
        [compute.ApplyUpdatesToInstancesInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_instances(
        self,
    ) -> Callable[
        [compute.CreateInstancesInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete(
        self,
    ) -> Callable[
        [compute.DeleteInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_instances(
        self,
    ) -> Callable[
        [compute.DeleteInstancesInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_per_instance_configs(
        self,
    ) -> Callable[
        [compute.DeletePerInstanceConfigsInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetInstanceGroupManagerRequest],
        Union[compute.InstanceGroupManager, Awaitable[compute.InstanceGroupManager]],
    ]:
        raise NotImplementedError()

    @property
    def insert(
        self,
    ) -> Callable[
        [compute.InsertInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListInstanceGroupManagersRequest],
        Union[
            compute.InstanceGroupManagerList,
            Awaitable[compute.InstanceGroupManagerList],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_errors(
        self,
    ) -> Callable[
        [compute.ListErrorsInstanceGroupManagersRequest],
        Union[
            compute.InstanceGroupManagersListErrorsResponse,
            Awaitable[compute.InstanceGroupManagersListErrorsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_managed_instances(
        self,
    ) -> Callable[
        [compute.ListManagedInstancesInstanceGroupManagersRequest],
        Union[
            compute.InstanceGroupManagersListManagedInstancesResponse,
            Awaitable[compute.InstanceGroupManagersListManagedInstancesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_per_instance_configs(
        self,
    ) -> Callable[
        [compute.ListPerInstanceConfigsInstanceGroupManagersRequest],
        Union[
            compute.InstanceGroupManagersListPerInstanceConfigsResp,
            Awaitable[compute.InstanceGroupManagersListPerInstanceConfigsResp],
        ],
    ]:
        raise NotImplementedError()

    @property
    def patch(
        self,
    ) -> Callable[
        [compute.PatchInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def patch_per_instance_configs(
        self,
    ) -> Callable[
        [compute.PatchPerInstanceConfigsInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def recreate_instances(
        self,
    ) -> Callable[
        [compute.RecreateInstancesInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def resize(
        self,
    ) -> Callable[
        [compute.ResizeInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def resume_instances(
        self,
    ) -> Callable[
        [compute.ResumeInstancesInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_instance_template(
        self,
    ) -> Callable[
        [compute.SetInstanceTemplateInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_target_pools(
        self,
    ) -> Callable[
        [compute.SetTargetPoolsInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def start_instances(
        self,
    ) -> Callable[
        [compute.StartInstancesInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def stop_instances(
        self,
    ) -> Callable[
        [compute.StopInstancesInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def suspend_instances(
        self,
    ) -> Callable[
        [compute.SuspendInstancesInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_per_instance_configs(
        self,
    ) -> Callable[
        [compute.UpdatePerInstanceConfigsInstanceGroupManagerRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()

    @property
    def _zone_operations_client(self) -> zone_operations.ZoneOperationsClient:
        ex_op_service = self._extended_operations_services.get("zone_operations")
        if not ex_op_service:
            ex_op_service = zone_operations.ZoneOperationsClient(
                credentials=self._credentials,
                transport=self.kind,
            )
            self._extended_operations_services["zone_operations"] = ex_op_service

        return ex_op_service


__all__ = ("InstanceGroupManagersTransport",)
