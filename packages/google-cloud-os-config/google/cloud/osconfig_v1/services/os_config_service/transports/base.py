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

from google import auth
from google.auth import credentials  # type: ignore

from google.cloud.osconfig_v1.types import patch_deployments
from google.cloud.osconfig_v1.types import patch_jobs
from google.protobuf import empty_pb2 as empty  # type: ignore


class OsConfigServiceTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for OsConfigService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "osconfig.googleapis.com",
        credentials: credentials.Credentials = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def execute_patch_job(
        self
    ) -> typing.Callable[[patch_jobs.ExecutePatchJobRequest], patch_jobs.PatchJob]:
        raise NotImplementedError

    @property
    def get_patch_job(
        self
    ) -> typing.Callable[[patch_jobs.GetPatchJobRequest], patch_jobs.PatchJob]:
        raise NotImplementedError

    @property
    def cancel_patch_job(
        self
    ) -> typing.Callable[[patch_jobs.CancelPatchJobRequest], patch_jobs.PatchJob]:
        raise NotImplementedError

    @property
    def list_patch_jobs(
        self
    ) -> typing.Callable[
        [patch_jobs.ListPatchJobsRequest], patch_jobs.ListPatchJobsResponse
    ]:
        raise NotImplementedError

    @property
    def list_patch_job_instance_details(
        self
    ) -> typing.Callable[
        [patch_jobs.ListPatchJobInstanceDetailsRequest],
        patch_jobs.ListPatchJobInstanceDetailsResponse,
    ]:
        raise NotImplementedError

    @property
    def create_patch_deployment(
        self
    ) -> typing.Callable[
        [patch_deployments.CreatePatchDeploymentRequest],
        patch_deployments.PatchDeployment,
    ]:
        raise NotImplementedError

    @property
    def get_patch_deployment(
        self
    ) -> typing.Callable[
        [patch_deployments.GetPatchDeploymentRequest], patch_deployments.PatchDeployment
    ]:
        raise NotImplementedError

    @property
    def list_patch_deployments(
        self
    ) -> typing.Callable[
        [patch_deployments.ListPatchDeploymentsRequest],
        patch_deployments.ListPatchDeploymentsResponse,
    ]:
        raise NotImplementedError

    @property
    def delete_patch_deployment(
        self
    ) -> typing.Callable[[patch_deployments.DeletePatchDeploymentRequest], empty.Empty]:
        raise NotImplementedError


__all__ = ("OsConfigServiceTransport",)
