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
from google.api_core import gapic_v1, operations_v1
from google.api_core import retry as retries
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.config_v1 import gapic_version as package_version
from google.cloud.config_v1.types import config

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class ConfigTransport(abc.ABC):
    """Abstract transport class for Config."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "config.googleapis.com"

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
                 The hostname to connect to (default: 'config.googleapis.com').
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
            self.list_deployments: gapic_v1.method.wrap_method(
                self.list_deployments,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_deployment: gapic_v1.method.wrap_method(
                self.get_deployment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_deployment: gapic_v1.method.wrap_method(
                self.create_deployment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_deployment: gapic_v1.method.wrap_method(
                self.update_deployment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_deployment: gapic_v1.method.wrap_method(
                self.delete_deployment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_revisions: gapic_v1.method.wrap_method(
                self.list_revisions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_revision: gapic_v1.method.wrap_method(
                self.get_revision,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_resource: gapic_v1.method.wrap_method(
                self.get_resource,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_resources: gapic_v1.method.wrap_method(
                self.list_resources,
                default_timeout=None,
                client_info=client_info,
            ),
            self.export_deployment_statefile: gapic_v1.method.wrap_method(
                self.export_deployment_statefile,
                default_timeout=None,
                client_info=client_info,
            ),
            self.export_revision_statefile: gapic_v1.method.wrap_method(
                self.export_revision_statefile,
                default_timeout=None,
                client_info=client_info,
            ),
            self.import_statefile: gapic_v1.method.wrap_method(
                self.import_statefile,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_statefile: gapic_v1.method.wrap_method(
                self.delete_statefile,
                default_timeout=None,
                client_info=client_info,
            ),
            self.lock_deployment: gapic_v1.method.wrap_method(
                self.lock_deployment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.unlock_deployment: gapic_v1.method.wrap_method(
                self.unlock_deployment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.export_lock_info: gapic_v1.method.wrap_method(
                self.export_lock_info,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_preview: gapic_v1.method.wrap_method(
                self.create_preview,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_preview: gapic_v1.method.wrap_method(
                self.get_preview,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_previews: gapic_v1.method.wrap_method(
                self.list_previews,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_preview: gapic_v1.method.wrap_method(
                self.delete_preview,
                default_timeout=None,
                client_info=client_info,
            ),
            self.export_preview_result: gapic_v1.method.wrap_method(
                self.export_preview_result,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_terraform_versions: gapic_v1.method.wrap_method(
                self.list_terraform_versions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_terraform_version: gapic_v1.method.wrap_method(
                self.get_terraform_version,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_location: gapic_v1.method.wrap_method(
                self.get_location,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_locations: gapic_v1.method.wrap_method(
                self.list_locations,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
            self.cancel_operation: gapic_v1.method.wrap_method(
                self.cancel_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_operation: gapic_v1.method.wrap_method(
                self.delete_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_operation: gapic_v1.method.wrap_method(
                self.get_operation,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_operations: gapic_v1.method.wrap_method(
                self.list_operations,
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
    def operations_client(self):
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_deployments(
        self,
    ) -> Callable[
        [config.ListDeploymentsRequest],
        Union[
            config.ListDeploymentsResponse, Awaitable[config.ListDeploymentsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_deployment(
        self,
    ) -> Callable[
        [config.GetDeploymentRequest],
        Union[config.Deployment, Awaitable[config.Deployment]],
    ]:
        raise NotImplementedError()

    @property
    def create_deployment(
        self,
    ) -> Callable[
        [config.CreateDeploymentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_deployment(
        self,
    ) -> Callable[
        [config.UpdateDeploymentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_deployment(
        self,
    ) -> Callable[
        [config.DeleteDeploymentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_revisions(
        self,
    ) -> Callable[
        [config.ListRevisionsRequest],
        Union[config.ListRevisionsResponse, Awaitable[config.ListRevisionsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_revision(
        self,
    ) -> Callable[
        [config.GetRevisionRequest], Union[config.Revision, Awaitable[config.Revision]]
    ]:
        raise NotImplementedError()

    @property
    def get_resource(
        self,
    ) -> Callable[
        [config.GetResourceRequest], Union[config.Resource, Awaitable[config.Resource]]
    ]:
        raise NotImplementedError()

    @property
    def list_resources(
        self,
    ) -> Callable[
        [config.ListResourcesRequest],
        Union[config.ListResourcesResponse, Awaitable[config.ListResourcesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def export_deployment_statefile(
        self,
    ) -> Callable[
        [config.ExportDeploymentStatefileRequest],
        Union[config.Statefile, Awaitable[config.Statefile]],
    ]:
        raise NotImplementedError()

    @property
    def export_revision_statefile(
        self,
    ) -> Callable[
        [config.ExportRevisionStatefileRequest],
        Union[config.Statefile, Awaitable[config.Statefile]],
    ]:
        raise NotImplementedError()

    @property
    def import_statefile(
        self,
    ) -> Callable[
        [config.ImportStatefileRequest],
        Union[config.Statefile, Awaitable[config.Statefile]],
    ]:
        raise NotImplementedError()

    @property
    def delete_statefile(
        self,
    ) -> Callable[
        [config.DeleteStatefileRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def lock_deployment(
        self,
    ) -> Callable[
        [config.LockDeploymentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def unlock_deployment(
        self,
    ) -> Callable[
        [config.UnlockDeploymentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def export_lock_info(
        self,
    ) -> Callable[
        [config.ExportLockInfoRequest],
        Union[config.LockInfo, Awaitable[config.LockInfo]],
    ]:
        raise NotImplementedError()

    @property
    def create_preview(
        self,
    ) -> Callable[
        [config.CreatePreviewRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_preview(
        self,
    ) -> Callable[
        [config.GetPreviewRequest], Union[config.Preview, Awaitable[config.Preview]]
    ]:
        raise NotImplementedError()

    @property
    def list_previews(
        self,
    ) -> Callable[
        [config.ListPreviewsRequest],
        Union[config.ListPreviewsResponse, Awaitable[config.ListPreviewsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def delete_preview(
        self,
    ) -> Callable[
        [config.DeletePreviewRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def export_preview_result(
        self,
    ) -> Callable[
        [config.ExportPreviewResultRequest],
        Union[
            config.ExportPreviewResultResponse,
            Awaitable[config.ExportPreviewResultResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_terraform_versions(
        self,
    ) -> Callable[
        [config.ListTerraformVersionsRequest],
        Union[
            config.ListTerraformVersionsResponse,
            Awaitable[config.ListTerraformVersionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_terraform_version(
        self,
    ) -> Callable[
        [config.GetTerraformVersionRequest],
        Union[config.TerraformVersion, Awaitable[config.TerraformVersion]],
    ]:
        raise NotImplementedError()

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest],
        Union[
            operations_pb2.ListOperationsResponse,
            Awaitable[operations_pb2.ListOperationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_operation(
        self,
    ) -> Callable[
        [operations_pb2.GetOperationRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None,]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.SetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [iam_policy_pb2.GetIamPolicyRequest],
        Union[policy_pb2.Policy, Awaitable[policy_pb2.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest],
        Union[
            iam_policy_pb2.TestIamPermissionsResponse,
            Awaitable[iam_policy_pb2.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_location(
        self,
    ) -> Callable[
        [locations_pb2.GetLocationRequest],
        Union[locations_pb2.Location, Awaitable[locations_pb2.Location]],
    ]:
        raise NotImplementedError()

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest],
        Union[
            locations_pb2.ListLocationsResponse,
            Awaitable[locations_pb2.ListLocationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()


__all__ = ("ConfigTransport",)
