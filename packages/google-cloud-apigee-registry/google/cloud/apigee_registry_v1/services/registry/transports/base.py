# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.api import httpbody_pb2  # type: ignore
import google.api_core
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.oauth2 import service_account  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.apigee_registry_v1 import gapic_version as package_version
from google.cloud.apigee_registry_v1.types import registry_models, registry_service

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class RegistryTransport(abc.ABC):
    """Abstract transport class for Registry."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "apigeeregistry.googleapis.com"

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
                 The hostname to connect to.
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
        elif credentials is None:
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

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_apis: gapic_v1.method.wrap_method(
                self.list_apis,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api: gapic_v1.method.wrap_method(
                self.get_api,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_api: gapic_v1.method.wrap_method(
                self.create_api,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_api: gapic_v1.method.wrap_method(
                self.update_api,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api: gapic_v1.method.wrap_method(
                self.delete_api,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_versions: gapic_v1.method.wrap_method(
                self.list_api_versions,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api_version: gapic_v1.method.wrap_method(
                self.get_api_version,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_api_version: gapic_v1.method.wrap_method(
                self.create_api_version,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_api_version: gapic_v1.method.wrap_method(
                self.update_api_version,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_version: gapic_v1.method.wrap_method(
                self.delete_api_version,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_specs: gapic_v1.method.wrap_method(
                self.list_api_specs,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api_spec: gapic_v1.method.wrap_method(
                self.get_api_spec,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api_spec_contents: gapic_v1.method.wrap_method(
                self.get_api_spec_contents,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_api_spec: gapic_v1.method.wrap_method(
                self.create_api_spec,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_api_spec: gapic_v1.method.wrap_method(
                self.update_api_spec,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_spec: gapic_v1.method.wrap_method(
                self.delete_api_spec,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.tag_api_spec_revision: gapic_v1.method.wrap_method(
                self.tag_api_spec_revision,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_spec_revisions: gapic_v1.method.wrap_method(
                self.list_api_spec_revisions,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.rollback_api_spec: gapic_v1.method.wrap_method(
                self.rollback_api_spec,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_spec_revision: gapic_v1.method.wrap_method(
                self.delete_api_spec_revision,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_deployments: gapic_v1.method.wrap_method(
                self.list_api_deployments,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_api_deployment: gapic_v1.method.wrap_method(
                self.get_api_deployment,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_api_deployment: gapic_v1.method.wrap_method(
                self.create_api_deployment,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_api_deployment: gapic_v1.method.wrap_method(
                self.update_api_deployment,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_deployment: gapic_v1.method.wrap_method(
                self.delete_api_deployment,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.tag_api_deployment_revision: gapic_v1.method.wrap_method(
                self.tag_api_deployment_revision,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_api_deployment_revisions: gapic_v1.method.wrap_method(
                self.list_api_deployment_revisions,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.rollback_api_deployment: gapic_v1.method.wrap_method(
                self.rollback_api_deployment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_api_deployment_revision: gapic_v1.method.wrap_method(
                self.delete_api_deployment_revision,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_artifacts: gapic_v1.method.wrap_method(
                self.list_artifacts,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_artifact: gapic_v1.method.wrap_method(
                self.get_artifact,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_artifact_contents: gapic_v1.method.wrap_method(
                self.get_artifact_contents,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_artifact: gapic_v1.method.wrap_method(
                self.create_artifact,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.replace_artifact: gapic_v1.method.wrap_method(
                self.replace_artifact,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_artifact: gapic_v1.method.wrap_method(
                self.delete_artifact,
                default_retry=retries.Retry(
                    initial=0.2,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        core_exceptions.Aborted,
                        core_exceptions.Cancelled,
                        core_exceptions.DeadlineExceeded,
                        core_exceptions.ServiceUnavailable,
                    ),
                    deadline=60.0,
                ),
                default_timeout=60.0,
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
    def list_apis(
        self,
    ) -> Callable[
        [registry_service.ListApisRequest],
        Union[
            registry_service.ListApisResponse,
            Awaitable[registry_service.ListApisResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_api(
        self,
    ) -> Callable[
        [registry_service.GetApiRequest],
        Union[registry_models.Api, Awaitable[registry_models.Api]],
    ]:
        raise NotImplementedError()

    @property
    def create_api(
        self,
    ) -> Callable[
        [registry_service.CreateApiRequest],
        Union[registry_models.Api, Awaitable[registry_models.Api]],
    ]:
        raise NotImplementedError()

    @property
    def update_api(
        self,
    ) -> Callable[
        [registry_service.UpdateApiRequest],
        Union[registry_models.Api, Awaitable[registry_models.Api]],
    ]:
        raise NotImplementedError()

    @property
    def delete_api(
        self,
    ) -> Callable[
        [registry_service.DeleteApiRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_api_versions(
        self,
    ) -> Callable[
        [registry_service.ListApiVersionsRequest],
        Union[
            registry_service.ListApiVersionsResponse,
            Awaitable[registry_service.ListApiVersionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_api_version(
        self,
    ) -> Callable[
        [registry_service.GetApiVersionRequest],
        Union[registry_models.ApiVersion, Awaitable[registry_models.ApiVersion]],
    ]:
        raise NotImplementedError()

    @property
    def create_api_version(
        self,
    ) -> Callable[
        [registry_service.CreateApiVersionRequest],
        Union[registry_models.ApiVersion, Awaitable[registry_models.ApiVersion]],
    ]:
        raise NotImplementedError()

    @property
    def update_api_version(
        self,
    ) -> Callable[
        [registry_service.UpdateApiVersionRequest],
        Union[registry_models.ApiVersion, Awaitable[registry_models.ApiVersion]],
    ]:
        raise NotImplementedError()

    @property
    def delete_api_version(
        self,
    ) -> Callable[
        [registry_service.DeleteApiVersionRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_api_specs(
        self,
    ) -> Callable[
        [registry_service.ListApiSpecsRequest],
        Union[
            registry_service.ListApiSpecsResponse,
            Awaitable[registry_service.ListApiSpecsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_api_spec(
        self,
    ) -> Callable[
        [registry_service.GetApiSpecRequest],
        Union[registry_models.ApiSpec, Awaitable[registry_models.ApiSpec]],
    ]:
        raise NotImplementedError()

    @property
    def get_api_spec_contents(
        self,
    ) -> Callable[
        [registry_service.GetApiSpecContentsRequest],
        Union[httpbody_pb2.HttpBody, Awaitable[httpbody_pb2.HttpBody]],
    ]:
        raise NotImplementedError()

    @property
    def create_api_spec(
        self,
    ) -> Callable[
        [registry_service.CreateApiSpecRequest],
        Union[registry_models.ApiSpec, Awaitable[registry_models.ApiSpec]],
    ]:
        raise NotImplementedError()

    @property
    def update_api_spec(
        self,
    ) -> Callable[
        [registry_service.UpdateApiSpecRequest],
        Union[registry_models.ApiSpec, Awaitable[registry_models.ApiSpec]],
    ]:
        raise NotImplementedError()

    @property
    def delete_api_spec(
        self,
    ) -> Callable[
        [registry_service.DeleteApiSpecRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def tag_api_spec_revision(
        self,
    ) -> Callable[
        [registry_service.TagApiSpecRevisionRequest],
        Union[registry_models.ApiSpec, Awaitable[registry_models.ApiSpec]],
    ]:
        raise NotImplementedError()

    @property
    def list_api_spec_revisions(
        self,
    ) -> Callable[
        [registry_service.ListApiSpecRevisionsRequest],
        Union[
            registry_service.ListApiSpecRevisionsResponse,
            Awaitable[registry_service.ListApiSpecRevisionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def rollback_api_spec(
        self,
    ) -> Callable[
        [registry_service.RollbackApiSpecRequest],
        Union[registry_models.ApiSpec, Awaitable[registry_models.ApiSpec]],
    ]:
        raise NotImplementedError()

    @property
    def delete_api_spec_revision(
        self,
    ) -> Callable[
        [registry_service.DeleteApiSpecRevisionRequest],
        Union[registry_models.ApiSpec, Awaitable[registry_models.ApiSpec]],
    ]:
        raise NotImplementedError()

    @property
    def list_api_deployments(
        self,
    ) -> Callable[
        [registry_service.ListApiDeploymentsRequest],
        Union[
            registry_service.ListApiDeploymentsResponse,
            Awaitable[registry_service.ListApiDeploymentsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_api_deployment(
        self,
    ) -> Callable[
        [registry_service.GetApiDeploymentRequest],
        Union[registry_models.ApiDeployment, Awaitable[registry_models.ApiDeployment]],
    ]:
        raise NotImplementedError()

    @property
    def create_api_deployment(
        self,
    ) -> Callable[
        [registry_service.CreateApiDeploymentRequest],
        Union[registry_models.ApiDeployment, Awaitable[registry_models.ApiDeployment]],
    ]:
        raise NotImplementedError()

    @property
    def update_api_deployment(
        self,
    ) -> Callable[
        [registry_service.UpdateApiDeploymentRequest],
        Union[registry_models.ApiDeployment, Awaitable[registry_models.ApiDeployment]],
    ]:
        raise NotImplementedError()

    @property
    def delete_api_deployment(
        self,
    ) -> Callable[
        [registry_service.DeleteApiDeploymentRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def tag_api_deployment_revision(
        self,
    ) -> Callable[
        [registry_service.TagApiDeploymentRevisionRequest],
        Union[registry_models.ApiDeployment, Awaitable[registry_models.ApiDeployment]],
    ]:
        raise NotImplementedError()

    @property
    def list_api_deployment_revisions(
        self,
    ) -> Callable[
        [registry_service.ListApiDeploymentRevisionsRequest],
        Union[
            registry_service.ListApiDeploymentRevisionsResponse,
            Awaitable[registry_service.ListApiDeploymentRevisionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def rollback_api_deployment(
        self,
    ) -> Callable[
        [registry_service.RollbackApiDeploymentRequest],
        Union[registry_models.ApiDeployment, Awaitable[registry_models.ApiDeployment]],
    ]:
        raise NotImplementedError()

    @property
    def delete_api_deployment_revision(
        self,
    ) -> Callable[
        [registry_service.DeleteApiDeploymentRevisionRequest],
        Union[registry_models.ApiDeployment, Awaitable[registry_models.ApiDeployment]],
    ]:
        raise NotImplementedError()

    @property
    def list_artifacts(
        self,
    ) -> Callable[
        [registry_service.ListArtifactsRequest],
        Union[
            registry_service.ListArtifactsResponse,
            Awaitable[registry_service.ListArtifactsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_artifact(
        self,
    ) -> Callable[
        [registry_service.GetArtifactRequest],
        Union[registry_models.Artifact, Awaitable[registry_models.Artifact]],
    ]:
        raise NotImplementedError()

    @property
    def get_artifact_contents(
        self,
    ) -> Callable[
        [registry_service.GetArtifactContentsRequest],
        Union[httpbody_pb2.HttpBody, Awaitable[httpbody_pb2.HttpBody]],
    ]:
        raise NotImplementedError()

    @property
    def create_artifact(
        self,
    ) -> Callable[
        [registry_service.CreateArtifactRequest],
        Union[registry_models.Artifact, Awaitable[registry_models.Artifact]],
    ]:
        raise NotImplementedError()

    @property
    def replace_artifact(
        self,
    ) -> Callable[
        [registry_service.ReplaceArtifactRequest],
        Union[registry_models.Artifact, Awaitable[registry_models.Artifact]],
    ]:
        raise NotImplementedError()

    @property
    def delete_artifact(
        self,
    ) -> Callable[
        [registry_service.DeleteArtifactRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
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


__all__ = ("RegistryTransport",)
