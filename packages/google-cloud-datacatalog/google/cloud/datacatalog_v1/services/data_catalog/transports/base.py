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
from google.auth import credentials  # type: ignore

from google.cloud.datacatalog_v1.types import datacatalog
from google.cloud.datacatalog_v1.types import tags
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-datacatalog",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class DataCatalogTransport(abc.ABC):
    """Abstract transport class for DataCatalog."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "datacatalog.googleapis.com",
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
            self.search_catalog: gapic_v1.method.wrap_method(
                self.search_catalog,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_entry_group: gapic_v1.method.wrap_method(
                self.create_entry_group, default_timeout=None, client_info=client_info,
            ),
            self.get_entry_group: gapic_v1.method.wrap_method(
                self.get_entry_group,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_entry_group: gapic_v1.method.wrap_method(
                self.update_entry_group, default_timeout=None, client_info=client_info,
            ),
            self.delete_entry_group: gapic_v1.method.wrap_method(
                self.delete_entry_group, default_timeout=None, client_info=client_info,
            ),
            self.list_entry_groups: gapic_v1.method.wrap_method(
                self.list_entry_groups,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_entry: gapic_v1.method.wrap_method(
                self.create_entry, default_timeout=None, client_info=client_info,
            ),
            self.update_entry: gapic_v1.method.wrap_method(
                self.update_entry, default_timeout=None, client_info=client_info,
            ),
            self.delete_entry: gapic_v1.method.wrap_method(
                self.delete_entry, default_timeout=None, client_info=client_info,
            ),
            self.get_entry: gapic_v1.method.wrap_method(
                self.get_entry,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.lookup_entry: gapic_v1.method.wrap_method(
                self.lookup_entry,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_entries: gapic_v1.method.wrap_method(
                self.list_entries,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_tag_template: gapic_v1.method.wrap_method(
                self.create_tag_template, default_timeout=None, client_info=client_info,
            ),
            self.get_tag_template: gapic_v1.method.wrap_method(
                self.get_tag_template, default_timeout=None, client_info=client_info,
            ),
            self.update_tag_template: gapic_v1.method.wrap_method(
                self.update_tag_template, default_timeout=None, client_info=client_info,
            ),
            self.delete_tag_template: gapic_v1.method.wrap_method(
                self.delete_tag_template, default_timeout=None, client_info=client_info,
            ),
            self.create_tag_template_field: gapic_v1.method.wrap_method(
                self.create_tag_template_field,
                default_timeout=None,
                client_info=client_info,
            ),
            self.update_tag_template_field: gapic_v1.method.wrap_method(
                self.update_tag_template_field,
                default_timeout=None,
                client_info=client_info,
            ),
            self.rename_tag_template_field: gapic_v1.method.wrap_method(
                self.rename_tag_template_field,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete_tag_template_field: gapic_v1.method.wrap_method(
                self.delete_tag_template_field,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_tag: gapic_v1.method.wrap_method(
                self.create_tag, default_timeout=None, client_info=client_info,
            ),
            self.update_tag: gapic_v1.method.wrap_method(
                self.update_tag, default_timeout=None, client_info=client_info,
            ),
            self.delete_tag: gapic_v1.method.wrap_method(
                self.delete_tag, default_timeout=None, client_info=client_info,
            ),
            self.list_tags: gapic_v1.method.wrap_method(
                self.list_tags,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(exceptions.ServiceUnavailable,),
                ),
                default_timeout=60.0,
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
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.test_iam_permissions: gapic_v1.method.wrap_method(
                self.test_iam_permissions,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def search_catalog(
        self,
    ) -> typing.Callable[
        [datacatalog.SearchCatalogRequest],
        typing.Union[
            datacatalog.SearchCatalogResponse,
            typing.Awaitable[datacatalog.SearchCatalogResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_entry_group(
        self,
    ) -> typing.Callable[
        [datacatalog.CreateEntryGroupRequest],
        typing.Union[datacatalog.EntryGroup, typing.Awaitable[datacatalog.EntryGroup]],
    ]:
        raise NotImplementedError()

    @property
    def get_entry_group(
        self,
    ) -> typing.Callable[
        [datacatalog.GetEntryGroupRequest],
        typing.Union[datacatalog.EntryGroup, typing.Awaitable[datacatalog.EntryGroup]],
    ]:
        raise NotImplementedError()

    @property
    def update_entry_group(
        self,
    ) -> typing.Callable[
        [datacatalog.UpdateEntryGroupRequest],
        typing.Union[datacatalog.EntryGroup, typing.Awaitable[datacatalog.EntryGroup]],
    ]:
        raise NotImplementedError()

    @property
    def delete_entry_group(
        self,
    ) -> typing.Callable[
        [datacatalog.DeleteEntryGroupRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_entry_groups(
        self,
    ) -> typing.Callable[
        [datacatalog.ListEntryGroupsRequest],
        typing.Union[
            datacatalog.ListEntryGroupsResponse,
            typing.Awaitable[datacatalog.ListEntryGroupsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_entry(
        self,
    ) -> typing.Callable[
        [datacatalog.CreateEntryRequest],
        typing.Union[datacatalog.Entry, typing.Awaitable[datacatalog.Entry]],
    ]:
        raise NotImplementedError()

    @property
    def update_entry(
        self,
    ) -> typing.Callable[
        [datacatalog.UpdateEntryRequest],
        typing.Union[datacatalog.Entry, typing.Awaitable[datacatalog.Entry]],
    ]:
        raise NotImplementedError()

    @property
    def delete_entry(
        self,
    ) -> typing.Callable[
        [datacatalog.DeleteEntryRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_entry(
        self,
    ) -> typing.Callable[
        [datacatalog.GetEntryRequest],
        typing.Union[datacatalog.Entry, typing.Awaitable[datacatalog.Entry]],
    ]:
        raise NotImplementedError()

    @property
    def lookup_entry(
        self,
    ) -> typing.Callable[
        [datacatalog.LookupEntryRequest],
        typing.Union[datacatalog.Entry, typing.Awaitable[datacatalog.Entry]],
    ]:
        raise NotImplementedError()

    @property
    def list_entries(
        self,
    ) -> typing.Callable[
        [datacatalog.ListEntriesRequest],
        typing.Union[
            datacatalog.ListEntriesResponse,
            typing.Awaitable[datacatalog.ListEntriesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_tag_template(
        self,
    ) -> typing.Callable[
        [datacatalog.CreateTagTemplateRequest],
        typing.Union[tags.TagTemplate, typing.Awaitable[tags.TagTemplate]],
    ]:
        raise NotImplementedError()

    @property
    def get_tag_template(
        self,
    ) -> typing.Callable[
        [datacatalog.GetTagTemplateRequest],
        typing.Union[tags.TagTemplate, typing.Awaitable[tags.TagTemplate]],
    ]:
        raise NotImplementedError()

    @property
    def update_tag_template(
        self,
    ) -> typing.Callable[
        [datacatalog.UpdateTagTemplateRequest],
        typing.Union[tags.TagTemplate, typing.Awaitable[tags.TagTemplate]],
    ]:
        raise NotImplementedError()

    @property
    def delete_tag_template(
        self,
    ) -> typing.Callable[
        [datacatalog.DeleteTagTemplateRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_tag_template_field(
        self,
    ) -> typing.Callable[
        [datacatalog.CreateTagTemplateFieldRequest],
        typing.Union[tags.TagTemplateField, typing.Awaitable[tags.TagTemplateField]],
    ]:
        raise NotImplementedError()

    @property
    def update_tag_template_field(
        self,
    ) -> typing.Callable[
        [datacatalog.UpdateTagTemplateFieldRequest],
        typing.Union[tags.TagTemplateField, typing.Awaitable[tags.TagTemplateField]],
    ]:
        raise NotImplementedError()

    @property
    def rename_tag_template_field(
        self,
    ) -> typing.Callable[
        [datacatalog.RenameTagTemplateFieldRequest],
        typing.Union[tags.TagTemplateField, typing.Awaitable[tags.TagTemplateField]],
    ]:
        raise NotImplementedError()

    @property
    def delete_tag_template_field(
        self,
    ) -> typing.Callable[
        [datacatalog.DeleteTagTemplateFieldRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_tag(
        self,
    ) -> typing.Callable[
        [datacatalog.CreateTagRequest],
        typing.Union[tags.Tag, typing.Awaitable[tags.Tag]],
    ]:
        raise NotImplementedError()

    @property
    def update_tag(
        self,
    ) -> typing.Callable[
        [datacatalog.UpdateTagRequest],
        typing.Union[tags.Tag, typing.Awaitable[tags.Tag]],
    ]:
        raise NotImplementedError()

    @property
    def delete_tag(
        self,
    ) -> typing.Callable[
        [datacatalog.DeleteTagRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def list_tags(
        self,
    ) -> typing.Callable[
        [datacatalog.ListTagsRequest],
        typing.Union[
            datacatalog.ListTagsResponse, typing.Awaitable[datacatalog.ListTagsResponse]
        ],
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


__all__ = ("DataCatalogTransport",)
