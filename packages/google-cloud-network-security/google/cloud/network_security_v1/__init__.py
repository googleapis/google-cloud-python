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
import sys

import google.api_core as api_core

from google.cloud.network_security_v1 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.address_group_service import (
    AddressGroupServiceAsyncClient,
    AddressGroupServiceClient,
)
from .services.dns_threat_detector_service import (
    DnsThreatDetectorServiceAsyncClient,
    DnsThreatDetectorServiceClient,
)
from .services.firewall_activation import (
    FirewallActivationAsyncClient,
    FirewallActivationClient,
)
from .services.intercept import InterceptAsyncClient, InterceptClient
from .services.mirroring import MirroringAsyncClient, MirroringClient
from .services.network_security import NetworkSecurityAsyncClient, NetworkSecurityClient
from .services.organization_address_group_service import (
    OrganizationAddressGroupServiceAsyncClient,
    OrganizationAddressGroupServiceClient,
)
from .services.organization_security_profile_group_service import (
    OrganizationSecurityProfileGroupServiceAsyncClient,
    OrganizationSecurityProfileGroupServiceClient,
)
from .types.address_group import (
    AddAddressGroupItemsRequest,
    AddressGroup,
    CloneAddressGroupItemsRequest,
    CreateAddressGroupRequest,
    DeleteAddressGroupRequest,
    GetAddressGroupRequest,
    ListAddressGroupReferencesRequest,
    ListAddressGroupReferencesResponse,
    ListAddressGroupsRequest,
    ListAddressGroupsResponse,
    RemoveAddressGroupItemsRequest,
    UpdateAddressGroupRequest,
)
from .types.authorization_policy import (
    AuthorizationPolicy,
    CreateAuthorizationPolicyRequest,
    DeleteAuthorizationPolicyRequest,
    GetAuthorizationPolicyRequest,
    ListAuthorizationPoliciesRequest,
    ListAuthorizationPoliciesResponse,
    UpdateAuthorizationPolicyRequest,
)
from .types.authz_policy import (
    AuthzPolicy,
    CreateAuthzPolicyRequest,
    DeleteAuthzPolicyRequest,
    GetAuthzPolicyRequest,
    ListAuthzPoliciesRequest,
    ListAuthzPoliciesResponse,
    UpdateAuthzPolicyRequest,
)
from .types.backend_authentication_config import (
    BackendAuthenticationConfig,
    CreateBackendAuthenticationConfigRequest,
    DeleteBackendAuthenticationConfigRequest,
    GetBackendAuthenticationConfigRequest,
    ListBackendAuthenticationConfigsRequest,
    ListBackendAuthenticationConfigsResponse,
    UpdateBackendAuthenticationConfigRequest,
)
from .types.client_tls_policy import (
    ClientTlsPolicy,
    CreateClientTlsPolicyRequest,
    DeleteClientTlsPolicyRequest,
    GetClientTlsPolicyRequest,
    ListClientTlsPoliciesRequest,
    ListClientTlsPoliciesResponse,
    UpdateClientTlsPolicyRequest,
)
from .types.common import OperationMetadata
from .types.dns_threat_detector import (
    CreateDnsThreatDetectorRequest,
    DeleteDnsThreatDetectorRequest,
    DnsThreatDetector,
    GetDnsThreatDetectorRequest,
    ListDnsThreatDetectorsRequest,
    ListDnsThreatDetectorsResponse,
    UpdateDnsThreatDetectorRequest,
)
from .types.firewall_activation import (
    CreateFirewallEndpointAssociationRequest,
    CreateFirewallEndpointRequest,
    DeleteFirewallEndpointAssociationRequest,
    DeleteFirewallEndpointRequest,
    FirewallEndpoint,
    FirewallEndpointAssociation,
    GetFirewallEndpointAssociationRequest,
    GetFirewallEndpointRequest,
    ListFirewallEndpointAssociationsRequest,
    ListFirewallEndpointAssociationsResponse,
    ListFirewallEndpointsRequest,
    ListFirewallEndpointsResponse,
    UpdateFirewallEndpointAssociationRequest,
    UpdateFirewallEndpointRequest,
)
from .types.gateway_security_policy import (
    CreateGatewaySecurityPolicyRequest,
    DeleteGatewaySecurityPolicyRequest,
    GatewaySecurityPolicy,
    GetGatewaySecurityPolicyRequest,
    ListGatewaySecurityPoliciesRequest,
    ListGatewaySecurityPoliciesResponse,
    UpdateGatewaySecurityPolicyRequest,
)
from .types.gateway_security_policy_rule import (
    CreateGatewaySecurityPolicyRuleRequest,
    DeleteGatewaySecurityPolicyRuleRequest,
    GatewaySecurityPolicyRule,
    GetGatewaySecurityPolicyRuleRequest,
    ListGatewaySecurityPolicyRulesRequest,
    ListGatewaySecurityPolicyRulesResponse,
    UpdateGatewaySecurityPolicyRuleRequest,
)
from .types.intercept import (
    CreateInterceptDeploymentGroupRequest,
    CreateInterceptDeploymentRequest,
    CreateInterceptEndpointGroupAssociationRequest,
    CreateInterceptEndpointGroupRequest,
    DeleteInterceptDeploymentGroupRequest,
    DeleteInterceptDeploymentRequest,
    DeleteInterceptEndpointGroupAssociationRequest,
    DeleteInterceptEndpointGroupRequest,
    GetInterceptDeploymentGroupRequest,
    GetInterceptDeploymentRequest,
    GetInterceptEndpointGroupAssociationRequest,
    GetInterceptEndpointGroupRequest,
    InterceptDeployment,
    InterceptDeploymentGroup,
    InterceptEndpointGroup,
    InterceptEndpointGroupAssociation,
    InterceptLocation,
    ListInterceptDeploymentGroupsRequest,
    ListInterceptDeploymentGroupsResponse,
    ListInterceptDeploymentsRequest,
    ListInterceptDeploymentsResponse,
    ListInterceptEndpointGroupAssociationsRequest,
    ListInterceptEndpointGroupAssociationsResponse,
    ListInterceptEndpointGroupsRequest,
    ListInterceptEndpointGroupsResponse,
    UpdateInterceptDeploymentGroupRequest,
    UpdateInterceptDeploymentRequest,
    UpdateInterceptEndpointGroupAssociationRequest,
    UpdateInterceptEndpointGroupRequest,
)
from .types.mirroring import (
    CreateMirroringDeploymentGroupRequest,
    CreateMirroringDeploymentRequest,
    CreateMirroringEndpointGroupAssociationRequest,
    CreateMirroringEndpointGroupRequest,
    DeleteMirroringDeploymentGroupRequest,
    DeleteMirroringDeploymentRequest,
    DeleteMirroringEndpointGroupAssociationRequest,
    DeleteMirroringEndpointGroupRequest,
    GetMirroringDeploymentGroupRequest,
    GetMirroringDeploymentRequest,
    GetMirroringEndpointGroupAssociationRequest,
    GetMirroringEndpointGroupRequest,
    ListMirroringDeploymentGroupsRequest,
    ListMirroringDeploymentGroupsResponse,
    ListMirroringDeploymentsRequest,
    ListMirroringDeploymentsResponse,
    ListMirroringEndpointGroupAssociationsRequest,
    ListMirroringEndpointGroupAssociationsResponse,
    ListMirroringEndpointGroupsRequest,
    ListMirroringEndpointGroupsResponse,
    MirroringDeployment,
    MirroringDeploymentGroup,
    MirroringEndpointGroup,
    MirroringEndpointGroupAssociation,
    MirroringLocation,
    UpdateMirroringDeploymentGroupRequest,
    UpdateMirroringDeploymentRequest,
    UpdateMirroringEndpointGroupAssociationRequest,
    UpdateMirroringEndpointGroupRequest,
)
from .types.security_profile_group import SecurityProfile, SecurityProfileGroup
from .types.security_profile_group_intercept import CustomInterceptProfile
from .types.security_profile_group_mirroring import CustomMirroringProfile
from .types.security_profile_group_service import (
    CreateSecurityProfileGroupRequest,
    CreateSecurityProfileRequest,
    DeleteSecurityProfileGroupRequest,
    DeleteSecurityProfileRequest,
    GetSecurityProfileGroupRequest,
    GetSecurityProfileRequest,
    ListSecurityProfileGroupsRequest,
    ListSecurityProfileGroupsResponse,
    ListSecurityProfilesRequest,
    ListSecurityProfilesResponse,
    UpdateSecurityProfileGroupRequest,
    UpdateSecurityProfileRequest,
)
from .types.security_profile_group_threatprevention import (
    AntivirusOverride,
    Protocol,
    Severity,
    SeverityOverride,
    ThreatAction,
    ThreatOverride,
    ThreatPreventionProfile,
    ThreatType,
)
from .types.security_profile_group_urlfiltering import UrlFilter, UrlFilteringProfile
from .types.server_tls_policy import (
    CreateServerTlsPolicyRequest,
    DeleteServerTlsPolicyRequest,
    GetServerTlsPolicyRequest,
    ListServerTlsPoliciesRequest,
    ListServerTlsPoliciesResponse,
    ServerTlsPolicy,
    UpdateServerTlsPolicyRequest,
)
from .types.tls import (
    CertificateProvider,
    CertificateProviderInstance,
    GrpcEndpoint,
    ValidationCA,
)
from .types.tls_inspection_policy import (
    CreateTlsInspectionPolicyRequest,
    DeleteTlsInspectionPolicyRequest,
    GetTlsInspectionPolicyRequest,
    ListTlsInspectionPoliciesRequest,
    ListTlsInspectionPoliciesResponse,
    TlsInspectionPolicy,
    UpdateTlsInspectionPolicyRequest,
)
from .types.url_list import (
    CreateUrlListRequest,
    DeleteUrlListRequest,
    GetUrlListRequest,
    ListUrlListsRequest,
    ListUrlListsResponse,
    UpdateUrlListRequest,
    UrlList,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.network_security_v1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.network_security_v1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.network_security_v1"
        if sys.version_info < (3, 9):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.9, and then update {_package_label}.",
                FutureWarning,
            )
        if sys.version_info[:2] == (3, 9):
            warnings.warn(
                f"You are using a Python version ({_py_version_str}) "
                + f"which Google will stop supporting in {_package_label} in "
                + "January 2026. Please "
                + "upgrade to the latest Python version, or at "
                + "least to Python 3.10, before then, and "
                + f"then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )

__all__ = (
    "AddressGroupServiceAsyncClient",
    "DnsThreatDetectorServiceAsyncClient",
    "FirewallActivationAsyncClient",
    "InterceptAsyncClient",
    "MirroringAsyncClient",
    "NetworkSecurityAsyncClient",
    "OrganizationAddressGroupServiceAsyncClient",
    "OrganizationSecurityProfileGroupServiceAsyncClient",
    "AddAddressGroupItemsRequest",
    "AddressGroup",
    "AddressGroupServiceClient",
    "AntivirusOverride",
    "AuthorizationPolicy",
    "AuthzPolicy",
    "BackendAuthenticationConfig",
    "CertificateProvider",
    "CertificateProviderInstance",
    "ClientTlsPolicy",
    "CloneAddressGroupItemsRequest",
    "CreateAddressGroupRequest",
    "CreateAuthorizationPolicyRequest",
    "CreateAuthzPolicyRequest",
    "CreateBackendAuthenticationConfigRequest",
    "CreateClientTlsPolicyRequest",
    "CreateDnsThreatDetectorRequest",
    "CreateFirewallEndpointAssociationRequest",
    "CreateFirewallEndpointRequest",
    "CreateGatewaySecurityPolicyRequest",
    "CreateGatewaySecurityPolicyRuleRequest",
    "CreateInterceptDeploymentGroupRequest",
    "CreateInterceptDeploymentRequest",
    "CreateInterceptEndpointGroupAssociationRequest",
    "CreateInterceptEndpointGroupRequest",
    "CreateMirroringDeploymentGroupRequest",
    "CreateMirroringDeploymentRequest",
    "CreateMirroringEndpointGroupAssociationRequest",
    "CreateMirroringEndpointGroupRequest",
    "CreateSecurityProfileGroupRequest",
    "CreateSecurityProfileRequest",
    "CreateServerTlsPolicyRequest",
    "CreateTlsInspectionPolicyRequest",
    "CreateUrlListRequest",
    "CustomInterceptProfile",
    "CustomMirroringProfile",
    "DeleteAddressGroupRequest",
    "DeleteAuthorizationPolicyRequest",
    "DeleteAuthzPolicyRequest",
    "DeleteBackendAuthenticationConfigRequest",
    "DeleteClientTlsPolicyRequest",
    "DeleteDnsThreatDetectorRequest",
    "DeleteFirewallEndpointAssociationRequest",
    "DeleteFirewallEndpointRequest",
    "DeleteGatewaySecurityPolicyRequest",
    "DeleteGatewaySecurityPolicyRuleRequest",
    "DeleteInterceptDeploymentGroupRequest",
    "DeleteInterceptDeploymentRequest",
    "DeleteInterceptEndpointGroupAssociationRequest",
    "DeleteInterceptEndpointGroupRequest",
    "DeleteMirroringDeploymentGroupRequest",
    "DeleteMirroringDeploymentRequest",
    "DeleteMirroringEndpointGroupAssociationRequest",
    "DeleteMirroringEndpointGroupRequest",
    "DeleteSecurityProfileGroupRequest",
    "DeleteSecurityProfileRequest",
    "DeleteServerTlsPolicyRequest",
    "DeleteTlsInspectionPolicyRequest",
    "DeleteUrlListRequest",
    "DnsThreatDetector",
    "DnsThreatDetectorServiceClient",
    "FirewallActivationClient",
    "FirewallEndpoint",
    "FirewallEndpointAssociation",
    "GatewaySecurityPolicy",
    "GatewaySecurityPolicyRule",
    "GetAddressGroupRequest",
    "GetAuthorizationPolicyRequest",
    "GetAuthzPolicyRequest",
    "GetBackendAuthenticationConfigRequest",
    "GetClientTlsPolicyRequest",
    "GetDnsThreatDetectorRequest",
    "GetFirewallEndpointAssociationRequest",
    "GetFirewallEndpointRequest",
    "GetGatewaySecurityPolicyRequest",
    "GetGatewaySecurityPolicyRuleRequest",
    "GetInterceptDeploymentGroupRequest",
    "GetInterceptDeploymentRequest",
    "GetInterceptEndpointGroupAssociationRequest",
    "GetInterceptEndpointGroupRequest",
    "GetMirroringDeploymentGroupRequest",
    "GetMirroringDeploymentRequest",
    "GetMirroringEndpointGroupAssociationRequest",
    "GetMirroringEndpointGroupRequest",
    "GetSecurityProfileGroupRequest",
    "GetSecurityProfileRequest",
    "GetServerTlsPolicyRequest",
    "GetTlsInspectionPolicyRequest",
    "GetUrlListRequest",
    "GrpcEndpoint",
    "InterceptClient",
    "InterceptDeployment",
    "InterceptDeploymentGroup",
    "InterceptEndpointGroup",
    "InterceptEndpointGroupAssociation",
    "InterceptLocation",
    "ListAddressGroupReferencesRequest",
    "ListAddressGroupReferencesResponse",
    "ListAddressGroupsRequest",
    "ListAddressGroupsResponse",
    "ListAuthorizationPoliciesRequest",
    "ListAuthorizationPoliciesResponse",
    "ListAuthzPoliciesRequest",
    "ListAuthzPoliciesResponse",
    "ListBackendAuthenticationConfigsRequest",
    "ListBackendAuthenticationConfigsResponse",
    "ListClientTlsPoliciesRequest",
    "ListClientTlsPoliciesResponse",
    "ListDnsThreatDetectorsRequest",
    "ListDnsThreatDetectorsResponse",
    "ListFirewallEndpointAssociationsRequest",
    "ListFirewallEndpointAssociationsResponse",
    "ListFirewallEndpointsRequest",
    "ListFirewallEndpointsResponse",
    "ListGatewaySecurityPoliciesRequest",
    "ListGatewaySecurityPoliciesResponse",
    "ListGatewaySecurityPolicyRulesRequest",
    "ListGatewaySecurityPolicyRulesResponse",
    "ListInterceptDeploymentGroupsRequest",
    "ListInterceptDeploymentGroupsResponse",
    "ListInterceptDeploymentsRequest",
    "ListInterceptDeploymentsResponse",
    "ListInterceptEndpointGroupAssociationsRequest",
    "ListInterceptEndpointGroupAssociationsResponse",
    "ListInterceptEndpointGroupsRequest",
    "ListInterceptEndpointGroupsResponse",
    "ListMirroringDeploymentGroupsRequest",
    "ListMirroringDeploymentGroupsResponse",
    "ListMirroringDeploymentsRequest",
    "ListMirroringDeploymentsResponse",
    "ListMirroringEndpointGroupAssociationsRequest",
    "ListMirroringEndpointGroupAssociationsResponse",
    "ListMirroringEndpointGroupsRequest",
    "ListMirroringEndpointGroupsResponse",
    "ListSecurityProfileGroupsRequest",
    "ListSecurityProfileGroupsResponse",
    "ListSecurityProfilesRequest",
    "ListSecurityProfilesResponse",
    "ListServerTlsPoliciesRequest",
    "ListServerTlsPoliciesResponse",
    "ListTlsInspectionPoliciesRequest",
    "ListTlsInspectionPoliciesResponse",
    "ListUrlListsRequest",
    "ListUrlListsResponse",
    "MirroringClient",
    "MirroringDeployment",
    "MirroringDeploymentGroup",
    "MirroringEndpointGroup",
    "MirroringEndpointGroupAssociation",
    "MirroringLocation",
    "NetworkSecurityClient",
    "OperationMetadata",
    "OrganizationAddressGroupServiceClient",
    "OrganizationSecurityProfileGroupServiceClient",
    "Protocol",
    "RemoveAddressGroupItemsRequest",
    "SecurityProfile",
    "SecurityProfileGroup",
    "ServerTlsPolicy",
    "Severity",
    "SeverityOverride",
    "ThreatAction",
    "ThreatOverride",
    "ThreatPreventionProfile",
    "ThreatType",
    "TlsInspectionPolicy",
    "UpdateAddressGroupRequest",
    "UpdateAuthorizationPolicyRequest",
    "UpdateAuthzPolicyRequest",
    "UpdateBackendAuthenticationConfigRequest",
    "UpdateClientTlsPolicyRequest",
    "UpdateDnsThreatDetectorRequest",
    "UpdateFirewallEndpointAssociationRequest",
    "UpdateFirewallEndpointRequest",
    "UpdateGatewaySecurityPolicyRequest",
    "UpdateGatewaySecurityPolicyRuleRequest",
    "UpdateInterceptDeploymentGroupRequest",
    "UpdateInterceptDeploymentRequest",
    "UpdateInterceptEndpointGroupAssociationRequest",
    "UpdateInterceptEndpointGroupRequest",
    "UpdateMirroringDeploymentGroupRequest",
    "UpdateMirroringDeploymentRequest",
    "UpdateMirroringEndpointGroupAssociationRequest",
    "UpdateMirroringEndpointGroupRequest",
    "UpdateSecurityProfileGroupRequest",
    "UpdateSecurityProfileRequest",
    "UpdateServerTlsPolicyRequest",
    "UpdateTlsInspectionPolicyRequest",
    "UpdateUrlListRequest",
    "UrlFilter",
    "UrlFilteringProfile",
    "UrlList",
    "ValidationCA",
)
