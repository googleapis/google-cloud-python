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
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.artifactregistry_v1beta2.types import file
from google.cloud.artifactregistry_v1beta2.types import package
from google.cloud.artifactregistry_v1beta2.types import repository
from google.cloud.artifactregistry_v1beta2.types import repository as gda_repository
from google.cloud.artifactregistry_v1beta2.types import tag
from google.cloud.artifactregistry_v1beta2.types import tag as gda_tag
from google.cloud.artifactregistry_v1beta2.types import version
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-artifact-registry",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class ArtifactRegistryTransport(abc.ABC):
    """Abstract transport class for ArtifactRegistry."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
    )

    def __init__(
        self,
        *,
        host: str = "artifactregistry.googleapis.com",
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
            self.list_repositories: gapic_v1.method.wrap_method(
                self.list_repositories,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_repository: gapic_v1.method.wrap_method(
                self.get_repository,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_repository: gapic_v1.method.wrap_method(
                self.create_repository, default_timeout=30.0, client_info=client_info,
            ),
            self.update_repository: gapic_v1.method.wrap_method(
                self.update_repository, default_timeout=30.0, client_info=client_info,
            ),
            self.delete_repository: gapic_v1.method.wrap_method(
                self.delete_repository,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_packages: gapic_v1.method.wrap_method(
                self.list_packages,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_package: gapic_v1.method.wrap_method(
                self.get_package,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_package: gapic_v1.method.wrap_method(
                self.delete_package,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_versions: gapic_v1.method.wrap_method(
                self.list_versions,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_version: gapic_v1.method.wrap_method(
                self.get_version,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.delete_version: gapic_v1.method.wrap_method(
                self.delete_version,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_files: gapic_v1.method.wrap_method(
                self.list_files,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_file: gapic_v1.method.wrap_method(
                self.get_file,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.list_tags: gapic_v1.method.wrap_method(
                self.list_tags,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.get_tag: gapic_v1.method.wrap_method(
                self.get_tag,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.create_tag: gapic_v1.method.wrap_method(
                self.create_tag, default_timeout=30.0, client_info=client_info,
            ),
            self.update_tag: gapic_v1.method.wrap_method(
                self.update_tag, default_timeout=30.0, client_info=client_info,
            ),
            self.delete_tag: gapic_v1.method.wrap_method(
                self.delete_tag,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.set_iam_policy: gapic_v1.method.wrap_method(
                self.set_iam_policy, default_timeout=None, client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=30.0,
                client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=30.0,
                client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def list_repositories(
        self,
    ) -> typing.Callable[
        [repository.ListRepositoriesRequest],
        typing.Union[
            repository.ListRepositoriesResponse,
            typing.Awaitable[repository.ListRepositoriesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_repository(
        self,
    ) -> typing.Callable[
        [repository.GetRepositoryRequest],
        typing.Union[repository.Repository, typing.Awaitable[repository.Repository]],
    ]:
        raise NotImplementedError()

    @property
    def create_repository(
        self,
    ) -> typing.Callable[
        [gda_repository.CreateRepositoryRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def update_repository(
        self,
    ) -> typing.Callable[
        [gda_repository.UpdateRepositoryRequest],
        typing.Union[
            gda_repository.Repository, typing.Awaitable[gda_repository.Repository]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_repository(
        self,
    ) -> typing.Callable[
        [repository.DeleteRepositoryRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_packages(
        self,
    ) -> typing.Callable[
        [package.ListPackagesRequest],
        typing.Union[
            package.ListPackagesResponse, typing.Awaitable[package.ListPackagesResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_package(
        self,
    ) -> typing.Callable[
        [package.GetPackageRequest],
        typing.Union[package.Package, typing.Awaitable[package.Package]],
    ]:
        raise NotImplementedError()

    @property
    def delete_package(
        self,
    ) -> typing.Callable[
        [package.DeletePackageRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_versions(
        self,
    ) -> typing.Callable[
        [version.ListVersionsRequest],
        typing.Union[
            version.ListVersionsResponse, typing.Awaitable[version.ListVersionsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_version(
        self,
    ) -> typing.Callable[
        [version.GetVersionRequest],
        typing.Union[version.Version, typing.Awaitable[version.Version]],
    ]:
        raise NotImplementedError()

    @property
    def delete_version(
        self,
    ) -> typing.Callable[
        [version.DeleteVersionRequest],
        typing.Union[operations.Operation, typing.Awaitable[operations.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list_files(
        self,
    ) -> typing.Callable[
        [file.ListFilesRequest],
        typing.Union[file.ListFilesResponse, typing.Awaitable[file.ListFilesResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_file(
        self,
    ) -> typing.Callable[
        [file.GetFileRequest], typing.Union[file.File, typing.Awaitable[file.File]]
    ]:
        raise NotImplementedError()

    @property
    def list_tags(
        self,
    ) -> typing.Callable[
        [tag.ListTagsRequest],
        typing.Union[tag.ListTagsResponse, typing.Awaitable[tag.ListTagsResponse]],
    ]:
        raise NotImplementedError()

    @property
    def get_tag(
        self,
    ) -> typing.Callable[
        [tag.GetTagRequest], typing.Union[tag.Tag, typing.Awaitable[tag.Tag]]
    ]:
        raise NotImplementedError()

    @property
    def create_tag(
        self,
    ) -> typing.Callable[
        [gda_tag.CreateTagRequest],
        typing.Union[gda_tag.Tag, typing.Awaitable[gda_tag.Tag]],
    ]:
        raise NotImplementedError()

    @property
    def update_tag(
        self,
    ) -> typing.Callable[
        [gda_tag.UpdateTagRequest],
        typing.Union[gda_tag.Tag, typing.Awaitable[gda_tag.Tag]],
    ]:
        raise NotImplementedError()

    @property
    def delete_tag(
        self,
    ) -> typing.Callable[
        [tag.DeleteTagRequest], typing.Union[empty.Empty, typing.Awaitable[empty.Empty]]
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.SetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.GetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> typing.Callable[
        [iam_policy.TestIamPermissionsRequest],
        typing.Union[
            iam_policy.TestIamPermissionsResponse,
            typing.Awaitable[iam_policy.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("ArtifactRegistryTransport",)
