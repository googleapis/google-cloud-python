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

from google.cloud.appengine_admin_v1.services.applications.client import (
    ApplicationsClient,
)
from google.cloud.appengine_admin_v1.services.applications.async_client import (
    ApplicationsAsyncClient,
)
from google.cloud.appengine_admin_v1.services.authorized_certificates.client import (
    AuthorizedCertificatesClient,
)
from google.cloud.appengine_admin_v1.services.authorized_certificates.async_client import (
    AuthorizedCertificatesAsyncClient,
)
from google.cloud.appengine_admin_v1.services.authorized_domains.client import (
    AuthorizedDomainsClient,
)
from google.cloud.appengine_admin_v1.services.authorized_domains.async_client import (
    AuthorizedDomainsAsyncClient,
)
from google.cloud.appengine_admin_v1.services.domain_mappings.client import (
    DomainMappingsClient,
)
from google.cloud.appengine_admin_v1.services.domain_mappings.async_client import (
    DomainMappingsAsyncClient,
)
from google.cloud.appengine_admin_v1.services.firewall.client import FirewallClient
from google.cloud.appengine_admin_v1.services.firewall.async_client import (
    FirewallAsyncClient,
)
from google.cloud.appengine_admin_v1.services.instances.client import InstancesClient
from google.cloud.appengine_admin_v1.services.instances.async_client import (
    InstancesAsyncClient,
)
from google.cloud.appengine_admin_v1.services.services.client import ServicesClient
from google.cloud.appengine_admin_v1.services.services.async_client import (
    ServicesAsyncClient,
)
from google.cloud.appengine_admin_v1.services.versions.client import VersionsClient
from google.cloud.appengine_admin_v1.services.versions.async_client import (
    VersionsAsyncClient,
)

from google.cloud.appengine_admin_v1.types.app_yaml import ApiConfigHandler
from google.cloud.appengine_admin_v1.types.app_yaml import ApiEndpointHandler
from google.cloud.appengine_admin_v1.types.app_yaml import ErrorHandler
from google.cloud.appengine_admin_v1.types.app_yaml import HealthCheck
from google.cloud.appengine_admin_v1.types.app_yaml import Library
from google.cloud.appengine_admin_v1.types.app_yaml import LivenessCheck
from google.cloud.appengine_admin_v1.types.app_yaml import ReadinessCheck
from google.cloud.appengine_admin_v1.types.app_yaml import ScriptHandler
from google.cloud.appengine_admin_v1.types.app_yaml import StaticFilesHandler
from google.cloud.appengine_admin_v1.types.app_yaml import UrlMap
from google.cloud.appengine_admin_v1.types.app_yaml import AuthFailAction
from google.cloud.appengine_admin_v1.types.app_yaml import LoginRequirement
from google.cloud.appengine_admin_v1.types.app_yaml import SecurityLevel
from google.cloud.appengine_admin_v1.types.appengine import (
    BatchUpdateIngressRulesRequest,
)
from google.cloud.appengine_admin_v1.types.appengine import (
    BatchUpdateIngressRulesResponse,
)
from google.cloud.appengine_admin_v1.types.appengine import CreateApplicationRequest
from google.cloud.appengine_admin_v1.types.appengine import (
    CreateAuthorizedCertificateRequest,
)
from google.cloud.appengine_admin_v1.types.appengine import CreateDomainMappingRequest
from google.cloud.appengine_admin_v1.types.appengine import CreateIngressRuleRequest
from google.cloud.appengine_admin_v1.types.appengine import CreateVersionRequest
from google.cloud.appengine_admin_v1.types.appengine import DebugInstanceRequest
from google.cloud.appengine_admin_v1.types.appengine import (
    DeleteAuthorizedCertificateRequest,
)
from google.cloud.appengine_admin_v1.types.appengine import DeleteDomainMappingRequest
from google.cloud.appengine_admin_v1.types.appengine import DeleteIngressRuleRequest
from google.cloud.appengine_admin_v1.types.appengine import DeleteInstanceRequest
from google.cloud.appengine_admin_v1.types.appengine import DeleteServiceRequest
from google.cloud.appengine_admin_v1.types.appengine import DeleteVersionRequest
from google.cloud.appengine_admin_v1.types.appengine import GetApplicationRequest
from google.cloud.appengine_admin_v1.types.appengine import (
    GetAuthorizedCertificateRequest,
)
from google.cloud.appengine_admin_v1.types.appengine import GetDomainMappingRequest
from google.cloud.appengine_admin_v1.types.appengine import GetIngressRuleRequest
from google.cloud.appengine_admin_v1.types.appengine import GetInstanceRequest
from google.cloud.appengine_admin_v1.types.appengine import GetServiceRequest
from google.cloud.appengine_admin_v1.types.appengine import GetVersionRequest
from google.cloud.appengine_admin_v1.types.appengine import (
    ListAuthorizedCertificatesRequest,
)
from google.cloud.appengine_admin_v1.types.appengine import (
    ListAuthorizedCertificatesResponse,
)
from google.cloud.appengine_admin_v1.types.appengine import ListAuthorizedDomainsRequest
from google.cloud.appengine_admin_v1.types.appengine import (
    ListAuthorizedDomainsResponse,
)
from google.cloud.appengine_admin_v1.types.appengine import ListDomainMappingsRequest
from google.cloud.appengine_admin_v1.types.appengine import ListDomainMappingsResponse
from google.cloud.appengine_admin_v1.types.appengine import ListIngressRulesRequest
from google.cloud.appengine_admin_v1.types.appengine import ListIngressRulesResponse
from google.cloud.appengine_admin_v1.types.appengine import ListInstancesRequest
from google.cloud.appengine_admin_v1.types.appengine import ListInstancesResponse
from google.cloud.appengine_admin_v1.types.appengine import ListServicesRequest
from google.cloud.appengine_admin_v1.types.appengine import ListServicesResponse
from google.cloud.appengine_admin_v1.types.appengine import ListVersionsRequest
from google.cloud.appengine_admin_v1.types.appengine import ListVersionsResponse
from google.cloud.appengine_admin_v1.types.appengine import RepairApplicationRequest
from google.cloud.appengine_admin_v1.types.appengine import UpdateApplicationRequest
from google.cloud.appengine_admin_v1.types.appengine import (
    UpdateAuthorizedCertificateRequest,
)
from google.cloud.appengine_admin_v1.types.appengine import UpdateDomainMappingRequest
from google.cloud.appengine_admin_v1.types.appengine import UpdateIngressRuleRequest
from google.cloud.appengine_admin_v1.types.appengine import UpdateServiceRequest
from google.cloud.appengine_admin_v1.types.appengine import UpdateVersionRequest
from google.cloud.appengine_admin_v1.types.appengine import AuthorizedCertificateView
from google.cloud.appengine_admin_v1.types.appengine import DomainOverrideStrategy
from google.cloud.appengine_admin_v1.types.appengine import VersionView
from google.cloud.appengine_admin_v1.types.application import Application
from google.cloud.appengine_admin_v1.types.application import UrlDispatchRule
from google.cloud.appengine_admin_v1.types.audit_data import AuditData
from google.cloud.appengine_admin_v1.types.audit_data import CreateVersionMethod
from google.cloud.appengine_admin_v1.types.audit_data import UpdateServiceMethod
from google.cloud.appengine_admin_v1.types.certificate import AuthorizedCertificate
from google.cloud.appengine_admin_v1.types.certificate import CertificateRawData
from google.cloud.appengine_admin_v1.types.certificate import ManagedCertificate
from google.cloud.appengine_admin_v1.types.certificate import ManagementStatus
from google.cloud.appengine_admin_v1.types.deploy import CloudBuildOptions
from google.cloud.appengine_admin_v1.types.deploy import ContainerInfo
from google.cloud.appengine_admin_v1.types.deploy import Deployment
from google.cloud.appengine_admin_v1.types.deploy import FileInfo
from google.cloud.appengine_admin_v1.types.deploy import ZipInfo
from google.cloud.appengine_admin_v1.types.domain import AuthorizedDomain
from google.cloud.appengine_admin_v1.types.domain_mapping import DomainMapping
from google.cloud.appengine_admin_v1.types.domain_mapping import ResourceRecord
from google.cloud.appengine_admin_v1.types.domain_mapping import SslSettings
from google.cloud.appengine_admin_v1.types.firewall import FirewallRule
from google.cloud.appengine_admin_v1.types.instance import Instance
from google.cloud.appengine_admin_v1.types.location import LocationMetadata
from google.cloud.appengine_admin_v1.types.network_settings import NetworkSettings
from google.cloud.appengine_admin_v1.types.operation import CreateVersionMetadataV1
from google.cloud.appengine_admin_v1.types.operation import OperationMetadataV1
from google.cloud.appengine_admin_v1.types.service import Service
from google.cloud.appengine_admin_v1.types.service import TrafficSplit
from google.cloud.appengine_admin_v1.types.version import AutomaticScaling
from google.cloud.appengine_admin_v1.types.version import BasicScaling
from google.cloud.appengine_admin_v1.types.version import CpuUtilization
from google.cloud.appengine_admin_v1.types.version import DiskUtilization
from google.cloud.appengine_admin_v1.types.version import EndpointsApiService
from google.cloud.appengine_admin_v1.types.version import Entrypoint
from google.cloud.appengine_admin_v1.types.version import ManualScaling
from google.cloud.appengine_admin_v1.types.version import Network
from google.cloud.appengine_admin_v1.types.version import NetworkUtilization
from google.cloud.appengine_admin_v1.types.version import RequestUtilization
from google.cloud.appengine_admin_v1.types.version import Resources
from google.cloud.appengine_admin_v1.types.version import StandardSchedulerSettings
from google.cloud.appengine_admin_v1.types.version import Version
from google.cloud.appengine_admin_v1.types.version import Volume
from google.cloud.appengine_admin_v1.types.version import VpcAccessConnector
from google.cloud.appengine_admin_v1.types.version import InboundServiceType
from google.cloud.appengine_admin_v1.types.version import ServingStatus

__all__ = (
    "ApplicationsClient",
    "ApplicationsAsyncClient",
    "AuthorizedCertificatesClient",
    "AuthorizedCertificatesAsyncClient",
    "AuthorizedDomainsClient",
    "AuthorizedDomainsAsyncClient",
    "DomainMappingsClient",
    "DomainMappingsAsyncClient",
    "FirewallClient",
    "FirewallAsyncClient",
    "InstancesClient",
    "InstancesAsyncClient",
    "ServicesClient",
    "ServicesAsyncClient",
    "VersionsClient",
    "VersionsAsyncClient",
    "ApiConfigHandler",
    "ApiEndpointHandler",
    "ErrorHandler",
    "HealthCheck",
    "Library",
    "LivenessCheck",
    "ReadinessCheck",
    "ScriptHandler",
    "StaticFilesHandler",
    "UrlMap",
    "AuthFailAction",
    "LoginRequirement",
    "SecurityLevel",
    "BatchUpdateIngressRulesRequest",
    "BatchUpdateIngressRulesResponse",
    "CreateApplicationRequest",
    "CreateAuthorizedCertificateRequest",
    "CreateDomainMappingRequest",
    "CreateIngressRuleRequest",
    "CreateVersionRequest",
    "DebugInstanceRequest",
    "DeleteAuthorizedCertificateRequest",
    "DeleteDomainMappingRequest",
    "DeleteIngressRuleRequest",
    "DeleteInstanceRequest",
    "DeleteServiceRequest",
    "DeleteVersionRequest",
    "GetApplicationRequest",
    "GetAuthorizedCertificateRequest",
    "GetDomainMappingRequest",
    "GetIngressRuleRequest",
    "GetInstanceRequest",
    "GetServiceRequest",
    "GetVersionRequest",
    "ListAuthorizedCertificatesRequest",
    "ListAuthorizedCertificatesResponse",
    "ListAuthorizedDomainsRequest",
    "ListAuthorizedDomainsResponse",
    "ListDomainMappingsRequest",
    "ListDomainMappingsResponse",
    "ListIngressRulesRequest",
    "ListIngressRulesResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "ListVersionsRequest",
    "ListVersionsResponse",
    "RepairApplicationRequest",
    "UpdateApplicationRequest",
    "UpdateAuthorizedCertificateRequest",
    "UpdateDomainMappingRequest",
    "UpdateIngressRuleRequest",
    "UpdateServiceRequest",
    "UpdateVersionRequest",
    "AuthorizedCertificateView",
    "DomainOverrideStrategy",
    "VersionView",
    "Application",
    "UrlDispatchRule",
    "AuditData",
    "CreateVersionMethod",
    "UpdateServiceMethod",
    "AuthorizedCertificate",
    "CertificateRawData",
    "ManagedCertificate",
    "ManagementStatus",
    "CloudBuildOptions",
    "ContainerInfo",
    "Deployment",
    "FileInfo",
    "ZipInfo",
    "AuthorizedDomain",
    "DomainMapping",
    "ResourceRecord",
    "SslSettings",
    "FirewallRule",
    "Instance",
    "LocationMetadata",
    "NetworkSettings",
    "CreateVersionMetadataV1",
    "OperationMetadataV1",
    "Service",
    "TrafficSplit",
    "AutomaticScaling",
    "BasicScaling",
    "CpuUtilization",
    "DiskUtilization",
    "EndpointsApiService",
    "Entrypoint",
    "ManualScaling",
    "Network",
    "NetworkUtilization",
    "RequestUtilization",
    "Resources",
    "StandardSchedulerSettings",
    "Version",
    "Volume",
    "VpcAccessConnector",
    "InboundServiceType",
    "ServingStatus",
)
