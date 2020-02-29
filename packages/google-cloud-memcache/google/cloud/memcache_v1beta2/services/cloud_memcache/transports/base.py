# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.memcache_v1beta2.types import cloud_memcache
from google.longrunning import operations_pb2 as operations  # type: ignore


class CloudMemcacheTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for CloudMemcache."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "memcache.googleapis.com",
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
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError

    @property
    def list_instances(
        self
    ) -> typing.Callable[
        [cloud_memcache.ListInstancesRequest], cloud_memcache.ListInstancesResponse
    ]:
        raise NotImplementedError

    @property
    def get_instance(
        self
    ) -> typing.Callable[[cloud_memcache.GetInstanceRequest], cloud_memcache.Instance]:
        raise NotImplementedError

    @property
    def create_instance(
        self
    ) -> typing.Callable[[cloud_memcache.CreateInstanceRequest], operations.Operation]:
        raise NotImplementedError

    @property
    def update_instance(
        self
    ) -> typing.Callable[[cloud_memcache.UpdateInstanceRequest], operations.Operation]:
        raise NotImplementedError

    @property
    def update_parameters(
        self
    ) -> typing.Callable[
        [cloud_memcache.UpdateParametersRequest], operations.Operation
    ]:
        raise NotImplementedError

    @property
    def delete_instance(
        self
    ) -> typing.Callable[[cloud_memcache.DeleteInstanceRequest], operations.Operation]:
        raise NotImplementedError

    @property
    def apply_parameters(
        self
    ) -> typing.Callable[[cloud_memcache.ApplyParametersRequest], operations.Operation]:
        raise NotImplementedError


__all__ = ("CloudMemcacheTransport",)
