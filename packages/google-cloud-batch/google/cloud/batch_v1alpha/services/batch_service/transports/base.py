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
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.batch_v1alpha import gapic_version as package_version
from google.cloud.batch_v1alpha.types import (
    resource_allowance as gcb_resource_allowance,
)
from google.cloud.batch_v1alpha.types import batch
from google.cloud.batch_v1alpha.types import job
from google.cloud.batch_v1alpha.types import job as gcb_job
from google.cloud.batch_v1alpha.types import resource_allowance
from google.cloud.batch_v1alpha.types import task

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class BatchServiceTransport(abc.ABC):
    """Abstract transport class for BatchService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "batch.googleapis.com"

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
                 The hostname to connect to (default: 'batch.googleapis.com').
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
            self.create_job: gapic_v1.method.wrap_method(
                self.create_job,
                default_timeout=60.0,
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
            self.delete_job: gapic_v1.method.wrap_method(
                self.delete_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.cancel_job: gapic_v1.method.wrap_method(
                self.cancel_job,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_job: gapic_v1.method.wrap_method(
                self.update_job,
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
            self.create_resource_allowance: gapic_v1.method.wrap_method(
                self.create_resource_allowance,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_resource_allowance: gapic_v1.method.wrap_method(
                self.get_resource_allowance,
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
            self.delete_resource_allowance: gapic_v1.method.wrap_method(
                self.delete_resource_allowance,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_resource_allowances: gapic_v1.method.wrap_method(
                self.list_resource_allowances,
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
            self.update_resource_allowance: gapic_v1.method.wrap_method(
                self.update_resource_allowance,
                default_timeout=60.0,
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
    def create_job(
        self,
    ) -> Callable[[batch.CreateJobRequest], Union[gcb_job.Job, Awaitable[gcb_job.Job]]]:
        raise NotImplementedError()

    @property
    def get_job(
        self,
    ) -> Callable[[batch.GetJobRequest], Union[job.Job, Awaitable[job.Job]]]:
        raise NotImplementedError()

    @property
    def delete_job(
        self,
    ) -> Callable[
        [batch.DeleteJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def cancel_job(
        self,
    ) -> Callable[
        [batch.CancelJobRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_job(
        self,
    ) -> Callable[[batch.UpdateJobRequest], Union[gcb_job.Job, Awaitable[gcb_job.Job]]]:
        raise NotImplementedError()

    @property
    def list_jobs(
        self,
    ) -> Callable[
        [batch.ListJobsRequest],
        Union[batch.ListJobsResponse, Awaitable[batch.ListJobsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_task(
        self,
    ) -> Callable[[batch.GetTaskRequest], Union[task.Task, Awaitable[task.Task]]]:
        raise NotImplementedError()

    @property
    def list_tasks(
        self,
    ) -> Callable[
        [batch.ListTasksRequest],
        Union[batch.ListTasksResponse, Awaitable[batch.ListTasksResponse]],
    ]:
        raise NotImplementedError()

    @property
    def create_resource_allowance(
        self,
    ) -> Callable[
        [batch.CreateResourceAllowanceRequest],
        Union[
            gcb_resource_allowance.ResourceAllowance,
            Awaitable[gcb_resource_allowance.ResourceAllowance],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_resource_allowance(
        self,
    ) -> Callable[
        [batch.GetResourceAllowanceRequest],
        Union[
            resource_allowance.ResourceAllowance,
            Awaitable[resource_allowance.ResourceAllowance],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_resource_allowance(
        self,
    ) -> Callable[
        [batch.DeleteResourceAllowanceRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_resource_allowances(
        self,
    ) -> Callable[
        [batch.ListResourceAllowancesRequest],
        Union[
            batch.ListResourceAllowancesResponse,
            Awaitable[batch.ListResourceAllowancesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_resource_allowance(
        self,
    ) -> Callable[
        [batch.UpdateResourceAllowanceRequest],
        Union[
            gcb_resource_allowance.ResourceAllowance,
            Awaitable[gcb_resource_allowance.ResourceAllowance],
        ],
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


__all__ = ("BatchServiceTransport",)
