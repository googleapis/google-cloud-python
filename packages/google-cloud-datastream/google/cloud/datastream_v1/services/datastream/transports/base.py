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

from google.cloud.datastream_v1 import gapic_version as package_version
from google.cloud.datastream_v1.types import datastream, datastream_resources

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class DatastreamTransport(abc.ABC):
    """Abstract transport class for Datastream."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "datastream.googleapis.com"

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
                 The hostname to connect to (default: 'datastream.googleapis.com').
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
            self.list_connection_profiles: gapic_v1.method.wrap_method(
                self.list_connection_profiles,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_connection_profile: gapic_v1.method.wrap_method(
                self.get_connection_profile,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_connection_profile: gapic_v1.method.wrap_method(
                self.create_connection_profile,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_connection_profile: gapic_v1.method.wrap_method(
                self.update_connection_profile,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_connection_profile: gapic_v1.method.wrap_method(
                self.delete_connection_profile,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.discover_connection_profile: gapic_v1.method.wrap_method(
                self.discover_connection_profile,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_streams: gapic_v1.method.wrap_method(
                self.list_streams,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_stream: gapic_v1.method.wrap_method(
                self.get_stream,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_stream: gapic_v1.method.wrap_method(
                self.create_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_stream: gapic_v1.method.wrap_method(
                self.update_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_stream: gapic_v1.method.wrap_method(
                self.delete_stream,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_stream_object: gapic_v1.method.wrap_method(
                self.get_stream_object,
                default_timeout=None,
                client_info=client_info,
            ),
            self.lookup_stream_object: gapic_v1.method.wrap_method(
                self.lookup_stream_object,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_stream_objects: gapic_v1.method.wrap_method(
                self.list_stream_objects,
                default_timeout=None,
                client_info=client_info,
            ),
            self.start_backfill_job: gapic_v1.method.wrap_method(
                self.start_backfill_job,
                default_timeout=None,
                client_info=client_info,
            ),
            self.stop_backfill_job: gapic_v1.method.wrap_method(
                self.stop_backfill_job,
                default_timeout=None,
                client_info=client_info,
            ),
            self.fetch_static_ips: gapic_v1.method.wrap_method(
                self.fetch_static_ips,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_private_connection: gapic_v1.method.wrap_method(
                self.create_private_connection,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_private_connection: gapic_v1.method.wrap_method(
                self.get_private_connection,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_private_connections: gapic_v1.method.wrap_method(
                self.list_private_connections,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_private_connection: gapic_v1.method.wrap_method(
                self.delete_private_connection,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_route: gapic_v1.method.wrap_method(
                self.create_route,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_route: gapic_v1.method.wrap_method(
                self.get_route,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_routes: gapic_v1.method.wrap_method(
                self.list_routes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_route: gapic_v1.method.wrap_method(
                self.delete_route,
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
    def list_connection_profiles(
        self,
    ) -> Callable[
        [datastream.ListConnectionProfilesRequest],
        Union[
            datastream.ListConnectionProfilesResponse,
            Awaitable[datastream.ListConnectionProfilesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_connection_profile(
        self,
    ) -> Callable[
        [datastream.GetConnectionProfileRequest],
        Union[
            datastream_resources.ConnectionProfile,
            Awaitable[datastream_resources.ConnectionProfile],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_connection_profile(
        self,
    ) -> Callable[
        [datastream.CreateConnectionProfileRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_connection_profile(
        self,
    ) -> Callable[
        [datastream.UpdateConnectionProfileRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_connection_profile(
        self,
    ) -> Callable[
        [datastream.DeleteConnectionProfileRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def discover_connection_profile(
        self,
    ) -> Callable[
        [datastream.DiscoverConnectionProfileRequest],
        Union[
            datastream.DiscoverConnectionProfileResponse,
            Awaitable[datastream.DiscoverConnectionProfileResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_streams(
        self,
    ) -> Callable[
        [datastream.ListStreamsRequest],
        Union[
            datastream.ListStreamsResponse, Awaitable[datastream.ListStreamsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_stream(
        self,
    ) -> Callable[
        [datastream.GetStreamRequest],
        Union[datastream_resources.Stream, Awaitable[datastream_resources.Stream]],
    ]:
        raise NotImplementedError()

    @property
    def create_stream(
        self,
    ) -> Callable[
        [datastream.CreateStreamRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_stream(
        self,
    ) -> Callable[
        [datastream.UpdateStreamRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete_stream(
        self,
    ) -> Callable[
        [datastream.DeleteStreamRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_stream_object(
        self,
    ) -> Callable[
        [datastream.GetStreamObjectRequest],
        Union[
            datastream_resources.StreamObject,
            Awaitable[datastream_resources.StreamObject],
        ],
    ]:
        raise NotImplementedError()

    @property
    def lookup_stream_object(
        self,
    ) -> Callable[
        [datastream.LookupStreamObjectRequest],
        Union[
            datastream_resources.StreamObject,
            Awaitable[datastream_resources.StreamObject],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_stream_objects(
        self,
    ) -> Callable[
        [datastream.ListStreamObjectsRequest],
        Union[
            datastream.ListStreamObjectsResponse,
            Awaitable[datastream.ListStreamObjectsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def start_backfill_job(
        self,
    ) -> Callable[
        [datastream.StartBackfillJobRequest],
        Union[
            datastream.StartBackfillJobResponse,
            Awaitable[datastream.StartBackfillJobResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def stop_backfill_job(
        self,
    ) -> Callable[
        [datastream.StopBackfillJobRequest],
        Union[
            datastream.StopBackfillJobResponse,
            Awaitable[datastream.StopBackfillJobResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def fetch_static_ips(
        self,
    ) -> Callable[
        [datastream.FetchStaticIpsRequest],
        Union[
            datastream.FetchStaticIpsResponse,
            Awaitable[datastream.FetchStaticIpsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_private_connection(
        self,
    ) -> Callable[
        [datastream.CreatePrivateConnectionRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_private_connection(
        self,
    ) -> Callable[
        [datastream.GetPrivateConnectionRequest],
        Union[
            datastream_resources.PrivateConnection,
            Awaitable[datastream_resources.PrivateConnection],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_private_connections(
        self,
    ) -> Callable[
        [datastream.ListPrivateConnectionsRequest],
        Union[
            datastream.ListPrivateConnectionsResponse,
            Awaitable[datastream.ListPrivateConnectionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_private_connection(
        self,
    ) -> Callable[
        [datastream.DeletePrivateConnectionRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_route(
        self,
    ) -> Callable[
        [datastream.CreateRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get_route(
        self,
    ) -> Callable[
        [datastream.GetRouteRequest],
        Union[datastream_resources.Route, Awaitable[datastream_resources.Route]],
    ]:
        raise NotImplementedError()

    @property
    def list_routes(
        self,
    ) -> Callable[
        [datastream.ListRoutesRequest],
        Union[datastream.ListRoutesResponse, Awaitable[datastream.ListRoutesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def delete_route(
        self,
    ) -> Callable[
        [datastream.DeleteRouteRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
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


__all__ = ("DatastreamTransport",)
