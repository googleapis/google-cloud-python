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
from google.api_core import gapic_v1
from google.api_core import retry as retries
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.compute_v1 import gapic_version as package_version
from google.cloud.compute_v1.services import global_operations
from google.cloud.compute_v1.types import compute

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


class NetworkFirewallPoliciesTransport(abc.ABC):
    """Abstract transport class for NetworkFirewallPolicies."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/compute",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    DEFAULT_HOST: str = "compute.googleapis.com"

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
                 The hostname to connect to (default: 'compute.googleapis.com').
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
        self._extended_operations_services: Dict[str, Any] = {}

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
            self.add_association: gapic_v1.method.wrap_method(
                self.add_association,
                default_timeout=None,
                client_info=client_info,
            ),
            self.add_rule: gapic_v1.method.wrap_method(
                self.add_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.aggregated_list: gapic_v1.method.wrap_method(
                self.aggregated_list,
                default_timeout=None,
                client_info=client_info,
            ),
            self.clone_rules: gapic_v1.method.wrap_method(
                self.clone_rules,
                default_timeout=None,
                client_info=client_info,
            ),
            self.delete: gapic_v1.method.wrap_method(
                self.delete,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get: gapic_v1.method.wrap_method(
                self.get,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_association: gapic_v1.method.wrap_method(
                self.get_association,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_iam_policy: gapic_v1.method.wrap_method(
                self.get_iam_policy,
                default_timeout=None,
                client_info=client_info,
            ),
            self.get_rule: gapic_v1.method.wrap_method(
                self.get_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.insert: gapic_v1.method.wrap_method(
                self.insert,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list: gapic_v1.method.wrap_method(
                self.list,
                default_timeout=None,
                client_info=client_info,
            ),
            self.patch: gapic_v1.method.wrap_method(
                self.patch,
                default_timeout=None,
                client_info=client_info,
            ),
            self.patch_rule: gapic_v1.method.wrap_method(
                self.patch_rule,
                default_timeout=None,
                client_info=client_info,
            ),
            self.remove_association: gapic_v1.method.wrap_method(
                self.remove_association,
                default_timeout=None,
                client_info=client_info,
            ),
            self.remove_rule: gapic_v1.method.wrap_method(
                self.remove_rule,
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
        }

    def close(self):
        """Closes resources associated with the transport.

        .. warning::
             Only call this method if the transport is NOT shared
             with other clients - this may cause errors in other clients!
        """
        raise NotImplementedError()

    @property
    def add_association(
        self,
    ) -> Callable[
        [compute.AddAssociationNetworkFirewallPolicyRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def add_rule(
        self,
    ) -> Callable[
        [compute.AddRuleNetworkFirewallPolicyRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def aggregated_list(
        self,
    ) -> Callable[
        [compute.AggregatedListNetworkFirewallPoliciesRequest],
        Union[
            compute.NetworkFirewallPolicyAggregatedList,
            Awaitable[compute.NetworkFirewallPolicyAggregatedList],
        ],
    ]:
        raise NotImplementedError()

    @property
    def clone_rules(
        self,
    ) -> Callable[
        [compute.CloneRulesNetworkFirewallPolicyRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def delete(
        self,
    ) -> Callable[
        [compute.DeleteNetworkFirewallPolicyRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def get(
        self,
    ) -> Callable[
        [compute.GetNetworkFirewallPolicyRequest],
        Union[compute.FirewallPolicy, Awaitable[compute.FirewallPolicy]],
    ]:
        raise NotImplementedError()

    @property
    def get_association(
        self,
    ) -> Callable[
        [compute.GetAssociationNetworkFirewallPolicyRequest],
        Union[
            compute.FirewallPolicyAssociation,
            Awaitable[compute.FirewallPolicyAssociation],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> Callable[
        [compute.GetIamPolicyNetworkFirewallPolicyRequest],
        Union[compute.Policy, Awaitable[compute.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_rule(
        self,
    ) -> Callable[
        [compute.GetRuleNetworkFirewallPolicyRequest],
        Union[compute.FirewallPolicyRule, Awaitable[compute.FirewallPolicyRule]],
    ]:
        raise NotImplementedError()

    @property
    def insert(
        self,
    ) -> Callable[
        [compute.InsertNetworkFirewallPolicyRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def list(
        self,
    ) -> Callable[
        [compute.ListNetworkFirewallPoliciesRequest],
        Union[compute.FirewallPolicyList, Awaitable[compute.FirewallPolicyList]],
    ]:
        raise NotImplementedError()

    @property
    def patch(
        self,
    ) -> Callable[
        [compute.PatchNetworkFirewallPolicyRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def patch_rule(
        self,
    ) -> Callable[
        [compute.PatchRuleNetworkFirewallPolicyRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def remove_association(
        self,
    ) -> Callable[
        [compute.RemoveAssociationNetworkFirewallPolicyRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def remove_rule(
        self,
    ) -> Callable[
        [compute.RemoveRuleNetworkFirewallPolicyRequest],
        Union[compute.Operation, Awaitable[compute.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> Callable[
        [compute.SetIamPolicyNetworkFirewallPolicyRequest],
        Union[compute.Policy, Awaitable[compute.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [compute.TestIamPermissionsNetworkFirewallPolicyRequest],
        Union[
            compute.TestPermissionsResponse, Awaitable[compute.TestPermissionsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def kind(self) -> str:
        raise NotImplementedError()

    @property
    def _global_operations_client(self) -> global_operations.GlobalOperationsClient:
        ex_op_service = self._extended_operations_services.get("global_operations")
        if not ex_op_service:
            ex_op_service = global_operations.GlobalOperationsClient(
                credentials=self._credentials,
                transport=self.kind,
            )
            self._extended_operations_services["global_operations"] = ex_op_service

        return ex_op_service


__all__ = ("NetworkFirewallPoliciesTransport",)
