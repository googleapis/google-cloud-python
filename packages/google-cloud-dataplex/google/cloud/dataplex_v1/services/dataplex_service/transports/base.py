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

from google.cloud.dataplex_v1 import gapic_version as package_version
from google.cloud.dataplex_v1.types import analyze, resources, service, tasks

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class DataplexServiceTransport(abc.ABC):
    """Abstract transport class for DataplexService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "dataplex.googleapis.com"

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
                 The hostname to connect to (default: 'dataplex.googleapis.com').
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
            self.create_lake: gapic_v1.method.wrap_method(
                self.create_lake,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_lake: gapic_v1.method.wrap_method(
                self.update_lake,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_lake: gapic_v1.method.wrap_method(
                self.delete_lake,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_lakes: gapic_v1.method.wrap_method(
                self.list_lakes,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_lake: gapic_v1.method.wrap_method(
                self.get_lake,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_lake_actions: gapic_v1.method.wrap_method(
                self.list_lake_actions,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_zone: gapic_v1.method.wrap_method(
                self.create_zone,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_zone: gapic_v1.method.wrap_method(
                self.update_zone,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_zone: gapic_v1.method.wrap_method(
                self.delete_zone,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_zones: gapic_v1.method.wrap_method(
                self.list_zones,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_zone: gapic_v1.method.wrap_method(
                self.get_zone,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_zone_actions: gapic_v1.method.wrap_method(
                self.list_zone_actions,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_asset: gapic_v1.method.wrap_method(
                self.create_asset,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_asset: gapic_v1.method.wrap_method(
                self.update_asset,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_asset: gapic_v1.method.wrap_method(
                self.delete_asset,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_assets: gapic_v1.method.wrap_method(
                self.list_assets,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_asset: gapic_v1.method.wrap_method(
                self.get_asset,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_asset_actions: gapic_v1.method.wrap_method(
                self.list_asset_actions,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_task: gapic_v1.method.wrap_method(
                self.create_task,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_task: gapic_v1.method.wrap_method(
                self.update_task,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_task: gapic_v1.method.wrap_method(
                self.delete_task,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_tasks: gapic_v1.method.wrap_method(
                self.list_tasks,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_task: gapic_v1.method.wrap_method(
                self.get_task,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_jobs: gapic_v1.method.wrap_method(
                self.list_jobs,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.run_task: gapic_v1.method.wrap_method(
                self.run_task,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_job: gapic_v1.method.wrap_method(
                self.get_job,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.cancel_job: gapic_v1.method.wrap_method(
                self.cancel_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_environment: gapic_v1.method.wrap_method(
                self.create_environment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_environment: gapic_v1.method.wrap_method(
                self.update_environment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_environment: gapic_v1.method.wrap_method(
                self.delete_environment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_environments: gapic_v1.method.wrap_method(
                self.list_environments,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_environment: gapic_v1.method.wrap_method(
                self.get_environment,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_sessions: gapic_v1.method.wrap_method(
                self.list_sessions,
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
    def create_lake(
        self,
    ) -> Callable[
        [service.CreateLakeRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_lake(
        self,
    ) -> Callable[
        [service.UpdateLakeRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_lake(
        self,
    ) -> Callable[
        [service.DeleteLakeRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_lakes(
        self,
    ) -> Callable[
        [service.ListLakesRequest],
        Union[service.ListLakesResponse, Awaitable[service.ListLakesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_lake(
        self,
    ) -> Callable[
        [service.GetLakeRequest], Union[resources.Lake, Awaitable[resources.Lake]]
    ]:
        raise NotImplementedError()

    @property
    def list_lake_actions(
        self,
    ) -> Callable[
        [service.ListLakeActionsRequest],
        Union[service.ListActionsResponse, Awaitable[service.ListActionsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def create_zone(
        self,
    ) -> Callable[
        [service.CreateZoneRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_zone(
        self,
    ) -> Callable[
        [service.UpdateZoneRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_zone(
        self,
    ) -> Callable[
        [service.DeleteZoneRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_zones(
        self,
    ) -> Callable[
        [service.ListZonesRequest],
        Union[service.ListZonesResponse, Awaitable[service.ListZonesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_zone(
        self,
    ) -> Callable[
        [service.GetZoneRequest], Union[resources.Zone, Awaitable[resources.Zone]]
    ]:
        raise NotImplementedError()

    @property
    def list_zone_actions(
        self,
    ) -> Callable[
        [service.ListZoneActionsRequest],
        Union[service.ListActionsResponse, Awaitable[service.ListActionsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def create_asset(
        self,
    ) -> Callable[
        [service.CreateAssetRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_asset(
        self,
    ) -> Callable[
        [service.UpdateAssetRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_asset(
        self,
    ) -> Callable[
        [service.DeleteAssetRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_assets(
        self,
    ) -> Callable[
        [service.ListAssetsRequest],
        Union[service.ListAssetsResponse, Awaitable[service.ListAssetsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_asset(
        self,
    ) -> Callable[
        [service.GetAssetRequest], Union[resources.Asset, Awaitable[resources.Asset]]
    ]:
        raise NotImplementedError()

    @property
    def list_asset_actions(
        self,
    ) -> Callable[
        [service.ListAssetActionsRequest],
        Union[service.ListActionsResponse, Awaitable[service.ListActionsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def create_task(
        self,
    ) -> Callable[
        [service.CreateTaskRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_task(
        self,
    ) -> Callable[
        [service.UpdateTaskRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_task(
        self,
    ) -> Callable[
        [service.DeleteTaskRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_tasks(
        self,
    ) -> Callable[
        [service.ListTasksRequest],
        Union[service.ListTasksResponse, Awaitable[service.ListTasksResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_task(
        self,
    ) -> Callable[[service.GetTaskRequest], Union[tasks.Task, Awaitable[tasks.Task]]]:
        raise NotImplementedError()

    @property
    def list_jobs(
        self,
    ) -> Callable[
        [service.ListJobsRequest],
        Union[service.ListJobsResponse, Awaitable[service.ListJobsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def run_task(
        self,
    ) -> Callable[
        [service.RunTaskRequest],
        Union[service.RunTaskResponse, Awaitable[service.RunTaskResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_job(
        self,
    ) -> Callable[[service.GetJobRequest], Union[tasks.Job, Awaitable[tasks.Job]]]:
        raise NotImplementedError()

    @property
    def cancel_job(
        self,
    ) -> Callable[
        [service.CancelJobRequest], Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]]
    ]:
        raise NotImplementedError()

    @property
    def create_environment(
        self,
    ) -> Callable[
        [service.CreateEnvironmentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_environment(
        self,
    ) -> Callable[
        [service.UpdateEnvironmentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_environment(
        self,
    ) -> Callable[
        [service.DeleteEnvironmentRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_environments(
        self,
    ) -> Callable[
        [service.ListEnvironmentsRequest],
        Union[
            service.ListEnvironmentsResponse,
            Awaitable[service.ListEnvironmentsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_environment(
        self,
    ) -> Callable[
        [service.GetEnvironmentRequest],
        Union[analyze.Environment, Awaitable[analyze.Environment]],
    ]:
        raise NotImplementedError()

    @property
    def list_sessions(
        self,
    ) -> Callable[
        [service.ListSessionsRequest],
        Union[service.ListSessionsResponse, Awaitable[service.ListSessionsResponse]],
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


__all__ = ("DataplexServiceTransport",)
