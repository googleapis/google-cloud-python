# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.oauth2 import service_account  # type: ignore
import google.protobuf
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.saasplatform_saasservicemgmt_v1beta1 import (
    gapic_version as package_version,
)
from google.cloud.saasplatform_saasservicemgmt_v1beta1.types import (
    deployments_resources,
    deployments_service,
)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)

if hasattr(DEFAULT_CLIENT_INFO, "protobuf_runtime_version"):  # pragma: NO COVER
    DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class SaasDeploymentsTransport(abc.ABC):
    """Abstract transport class for SaasDeployments."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "saasservicemgmt.googleapis.com"

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
                 The hostname to connect to (default: 'saasservicemgmt.googleapis.com').
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
            self.list_saas: gapic_v1.method.wrap_method(
                self.list_saas,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=80.0,
                ),
                default_timeout=80.0,
                client_info=client_info,
            ),
            self.get_saas: gapic_v1.method.wrap_method(
                self.get_saas,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_saas: gapic_v1.method.wrap_method(
                self.create_saas,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_saas: gapic_v1.method.wrap_method(
                self.update_saas,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_saas: gapic_v1.method.wrap_method(
                self.delete_saas,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_tenants: gapic_v1.method.wrap_method(
                self.list_tenants,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=80.0,
                ),
                default_timeout=80.0,
                client_info=client_info,
            ),
            self.get_tenant: gapic_v1.method.wrap_method(
                self.get_tenant,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_tenant: gapic_v1.method.wrap_method(
                self.create_tenant,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_tenant: gapic_v1.method.wrap_method(
                self.update_tenant,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_tenant: gapic_v1.method.wrap_method(
                self.delete_tenant,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_unit_kinds: gapic_v1.method.wrap_method(
                self.list_unit_kinds,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=80.0,
                ),
                default_timeout=80.0,
                client_info=client_info,
            ),
            self.get_unit_kind: gapic_v1.method.wrap_method(
                self.get_unit_kind,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_unit_kind: gapic_v1.method.wrap_method(
                self.create_unit_kind,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_unit_kind: gapic_v1.method.wrap_method(
                self.update_unit_kind,
                default_timeout=80.0,
                client_info=client_info,
            ),
            self.delete_unit_kind: gapic_v1.method.wrap_method(
                self.delete_unit_kind,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=80.0,
                ),
                default_timeout=80.0,
                client_info=client_info,
            ),
            self.list_units: gapic_v1.method.wrap_method(
                self.list_units,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=80.0,
                ),
                default_timeout=80.0,
                client_info=client_info,
            ),
            self.get_unit: gapic_v1.method.wrap_method(
                self.get_unit,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_unit: gapic_v1.method.wrap_method(
                self.create_unit,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_unit: gapic_v1.method.wrap_method(
                self.update_unit,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_unit: gapic_v1.method.wrap_method(
                self.delete_unit,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_unit_operations: gapic_v1.method.wrap_method(
                self.list_unit_operations,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=80.0,
                ),
                default_timeout=80.0,
                client_info=client_info,
            ),
            self.get_unit_operation: gapic_v1.method.wrap_method(
                self.get_unit_operation,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_unit_operation: gapic_v1.method.wrap_method(
                self.create_unit_operation,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_unit_operation: gapic_v1.method.wrap_method(
                self.update_unit_operation,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_unit_operation: gapic_v1.method.wrap_method(
                self.delete_unit_operation,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_releases: gapic_v1.method.wrap_method(
                self.list_releases,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=80.0,
                ),
                default_timeout=80.0,
                client_info=client_info,
            ),
            self.get_release: gapic_v1.method.wrap_method(
                self.get_release,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_release: gapic_v1.method.wrap_method(
                self.create_release,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.update_release: gapic_v1.method.wrap_method(
                self.update_release,
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_release: gapic_v1.method.wrap_method(
                self.delete_release,
                default_retry=retries.Retry(
                    initial=1.0,
                    maximum=10.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=30.0,
                ),
                default_timeout=30.0,
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
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def list_saas(
        self,
    ) -> Callable[
        [deployments_service.ListSaasRequest],
        Union[
            deployments_service.ListSaasResponse,
            Awaitable[deployments_service.ListSaasResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_saas(
        self,
    ) -> Callable[
        [deployments_service.GetSaasRequest],
        Union[deployments_resources.Saas, Awaitable[deployments_resources.Saas]],
    ]:
        raise NotImplementedError()

    @property
    def create_saas(
        self,
    ) -> Callable[
        [deployments_service.CreateSaasRequest],
        Union[deployments_resources.Saas, Awaitable[deployments_resources.Saas]],
    ]:
        raise NotImplementedError()

    @property
    def update_saas(
        self,
    ) -> Callable[
        [deployments_service.UpdateSaasRequest],
        Union[deployments_resources.Saas, Awaitable[deployments_resources.Saas]],
    ]:
        raise NotImplementedError()

    @property
    def delete_saas(
        self,
    ) -> Callable[
        [deployments_service.DeleteSaasRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_tenants(
        self,
    ) -> Callable[
        [deployments_service.ListTenantsRequest],
        Union[
            deployments_service.ListTenantsResponse,
            Awaitable[deployments_service.ListTenantsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_tenant(
        self,
    ) -> Callable[
        [deployments_service.GetTenantRequest],
        Union[deployments_resources.Tenant, Awaitable[deployments_resources.Tenant]],
    ]:
        raise NotImplementedError()

    @property
    def create_tenant(
        self,
    ) -> Callable[
        [deployments_service.CreateTenantRequest],
        Union[deployments_resources.Tenant, Awaitable[deployments_resources.Tenant]],
    ]:
        raise NotImplementedError()

    @property
    def update_tenant(
        self,
    ) -> Callable[
        [deployments_service.UpdateTenantRequest],
        Union[deployments_resources.Tenant, Awaitable[deployments_resources.Tenant]],
    ]:
        raise NotImplementedError()

    @property
    def delete_tenant(
        self,
    ) -> Callable[
        [deployments_service.DeleteTenantRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_unit_kinds(
        self,
    ) -> Callable[
        [deployments_service.ListUnitKindsRequest],
        Union[
            deployments_service.ListUnitKindsResponse,
            Awaitable[deployments_service.ListUnitKindsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_unit_kind(
        self,
    ) -> Callable[
        [deployments_service.GetUnitKindRequest],
        Union[
            deployments_resources.UnitKind, Awaitable[deployments_resources.UnitKind]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_unit_kind(
        self,
    ) -> Callable[
        [deployments_service.CreateUnitKindRequest],
        Union[
            deployments_resources.UnitKind, Awaitable[deployments_resources.UnitKind]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_unit_kind(
        self,
    ) -> Callable[
        [deployments_service.UpdateUnitKindRequest],
        Union[
            deployments_resources.UnitKind, Awaitable[deployments_resources.UnitKind]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_unit_kind(
        self,
    ) -> Callable[
        [deployments_service.DeleteUnitKindRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_units(
        self,
    ) -> Callable[
        [deployments_service.ListUnitsRequest],
        Union[
            deployments_service.ListUnitsResponse,
            Awaitable[deployments_service.ListUnitsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_unit(
        self,
    ) -> Callable[
        [deployments_service.GetUnitRequest],
        Union[deployments_resources.Unit, Awaitable[deployments_resources.Unit]],
    ]:
        raise NotImplementedError()

    @property
    def create_unit(
        self,
    ) -> Callable[
        [deployments_service.CreateUnitRequest],
        Union[deployments_resources.Unit, Awaitable[deployments_resources.Unit]],
    ]:
        raise NotImplementedError()

    @property
    def update_unit(
        self,
    ) -> Callable[
        [deployments_service.UpdateUnitRequest],
        Union[deployments_resources.Unit, Awaitable[deployments_resources.Unit]],
    ]:
        raise NotImplementedError()

    @property
    def delete_unit(
        self,
    ) -> Callable[
        [deployments_service.DeleteUnitRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_unit_operations(
        self,
    ) -> Callable[
        [deployments_service.ListUnitOperationsRequest],
        Union[
            deployments_service.ListUnitOperationsResponse,
            Awaitable[deployments_service.ListUnitOperationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_unit_operation(
        self,
    ) -> Callable[
        [deployments_service.GetUnitOperationRequest],
        Union[
            deployments_resources.UnitOperation,
            Awaitable[deployments_resources.UnitOperation],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_unit_operation(
        self,
    ) -> Callable[
        [deployments_service.CreateUnitOperationRequest],
        Union[
            deployments_resources.UnitOperation,
            Awaitable[deployments_resources.UnitOperation],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_unit_operation(
        self,
    ) -> Callable[
        [deployments_service.UpdateUnitOperationRequest],
        Union[
            deployments_resources.UnitOperation,
            Awaitable[deployments_resources.UnitOperation],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_unit_operation(
        self,
    ) -> Callable[
        [deployments_service.DeleteUnitOperationRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_releases(
        self,
    ) -> Callable[
        [deployments_service.ListReleasesRequest],
        Union[
            deployments_service.ListReleasesResponse,
            Awaitable[deployments_service.ListReleasesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_release(
        self,
    ) -> Callable[
        [deployments_service.GetReleaseRequest],
        Union[deployments_resources.Release, Awaitable[deployments_resources.Release]],
    ]:
        raise NotImplementedError()

    @property
    def create_release(
        self,
    ) -> Callable[
        [deployments_service.CreateReleaseRequest],
        Union[deployments_resources.Release, Awaitable[deployments_resources.Release]],
    ]:
        raise NotImplementedError()

    @property
    def update_release(
        self,
    ) -> Callable[
        [deployments_service.UpdateReleaseRequest],
        Union[deployments_resources.Release, Awaitable[deployments_resources.Release]],
    ]:
        raise NotImplementedError()

    @property
    def delete_release(
        self,
    ) -> Callable[
        [deployments_service.DeleteReleaseRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
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


__all__ = ("SaasDeploymentsTransport",)
