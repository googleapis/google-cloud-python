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

from .services.applications import ApplicationsClient
from .services.applications import ApplicationsAsyncClient
from .services.authorized_certificates import AuthorizedCertificatesClient
from .services.authorized_certificates import AuthorizedCertificatesAsyncClient
from .services.authorized_domains import AuthorizedDomainsClient
from .services.authorized_domains import AuthorizedDomainsAsyncClient
from .services.domain_mappings import DomainMappingsClient
from .services.domain_mappings import DomainMappingsAsyncClient
from .services.firewall import FirewallClient
from .services.firewall import FirewallAsyncClient
from .services.instances import InstancesClient
from .services.instances import InstancesAsyncClient
from .services.services import ServicesClient
from .services.services import ServicesAsyncClient
from .services.versions import VersionsClient
from .services.versions import VersionsAsyncClient

from .types.app_yaml import ApiConfigHandler
from .types.app_yaml import ApiEndpointHandler
from .types.app_yaml import ErrorHandler
from .types.app_yaml import HealthCheck
from .types.app_yaml import Library
from .types.app_yaml import LivenessCheck
from .types.app_yaml import ReadinessCheck
from .types.app_yaml import ScriptHandler
from .types.app_yaml import StaticFilesHandler
from .types.app_yaml import UrlMap
from .types.app_yaml import AuthFailAction
from .types.app_yaml import LoginRequirement
from .types.app_yaml import SecurityLevel
from .types.appengine import BatchUpdateIngressRulesRequest
from .types.appengine import BatchUpdateIngressRulesResponse
from .types.appengine import CreateApplicationRequest
from .types.appengine import CreateAuthorizedCertificateRequest
from .types.appengine import CreateDomainMappingRequest
from .types.appengine import CreateIngressRuleRequest
from .types.appengine import CreateVersionRequest
from .types.appengine import DebugInstanceRequest
from .types.appengine import DeleteAuthorizedCertificateRequest
from .types.appengine import DeleteDomainMappingRequest
from .types.appengine import DeleteIngressRuleRequest
from .types.appengine import DeleteInstanceRequest
from .types.appengine import DeleteServiceRequest
from .types.appengine import DeleteVersionRequest
from .types.appengine import GetApplicationRequest
from .types.appengine import GetAuthorizedCertificateRequest
from .types.appengine import GetDomainMappingRequest
from .types.appengine import GetIngressRuleRequest
from .types.appengine import GetInstanceRequest
from .types.appengine import GetServiceRequest
from .types.appengine import GetVersionRequest
from .types.appengine import ListAuthorizedCertificatesRequest
from .types.appengine import ListAuthorizedCertificatesResponse
from .types.appengine import ListAuthorizedDomainsRequest
from .types.appengine import ListAuthorizedDomainsResponse
from .types.appengine import ListDomainMappingsRequest
from .types.appengine import ListDomainMappingsResponse
from .types.appengine import ListIngressRulesRequest
from .types.appengine import ListIngressRulesResponse
from .types.appengine import ListInstancesRequest
from .types.appengine import ListInstancesResponse
from .types.appengine import ListServicesRequest
from .types.appengine import ListServicesResponse
from .types.appengine import ListVersionsRequest
from .types.appengine import ListVersionsResponse
from .types.appengine import RepairApplicationRequest
from .types.appengine import UpdateApplicationRequest
from .types.appengine import UpdateAuthorizedCertificateRequest
from .types.appengine import UpdateDomainMappingRequest
from .types.appengine import UpdateIngressRuleRequest
from .types.appengine import UpdateServiceRequest
from .types.appengine import UpdateVersionRequest
from .types.appengine import AuthorizedCertificateView
from .types.appengine import DomainOverrideStrategy
from .types.appengine import VersionView
from .types.application import Application
from .types.application import UrlDispatchRule
from .types.audit_data import AuditData
from .types.audit_data import CreateVersionMethod
from .types.audit_data import UpdateServiceMethod
from .types.certificate import AuthorizedCertificate
from .types.certificate import CertificateRawData
from .types.certificate import ManagedCertificate
from .types.certificate import ManagementStatus
from .types.deploy import CloudBuildOptions
from .types.deploy import ContainerInfo
from .types.deploy import Deployment
from .types.deploy import FileInfo
from .types.deploy import ZipInfo
from .types.domain import AuthorizedDomain
from .types.domain_mapping import DomainMapping
from .types.domain_mapping import ResourceRecord
from .types.domain_mapping import SslSettings
from .types.firewall import FirewallRule
from .types.instance import Instance
from .types.location import LocationMetadata
from .types.network_settings import NetworkSettings
from .types.operation import CreateVersionMetadataV1
from .types.operation import OperationMetadataV1
from .types.service import Service
from .types.service import TrafficSplit
from .types.version import AutomaticScaling
from .types.version import BasicScaling
from .types.version import CpuUtilization
from .types.version import DiskUtilization
from .types.version import EndpointsApiService
from .types.version import Entrypoint
from .types.version import ManualScaling
from .types.version import Network
from .types.version import NetworkUtilization
from .types.version import RequestUtilization
from .types.version import Resources
from .types.version import StandardSchedulerSettings
from .types.version import Version
from .types.version import Volume
from .types.version import VpcAccessConnector
from .types.version import InboundServiceType
from .types.version import ServingStatus

__all__ = (
    "ApplicationsAsyncClient",
    "AuthorizedCertificatesAsyncClient",
    "AuthorizedDomainsAsyncClient",
    "DomainMappingsAsyncClient",
    "FirewallAsyncClient",
    "InstancesAsyncClient",
    "ServicesAsyncClient",
    "VersionsAsyncClient",
    "ApiConfigHandler",
    "ApiEndpointHandler",
    "Application",
    "ApplicationsClient",
    "AuditData",
    "AuthFailAction",
    "AuthorizedCertificate",
    "AuthorizedCertificateView",
    "AuthorizedCertificatesClient",
    "AuthorizedDomain",
    "AuthorizedDomainsClient",
    "AutomaticScaling",
    "BasicScaling",
    "BatchUpdateIngressRulesRequest",
    "BatchUpdateIngressRulesResponse",
    "CertificateRawData",
    "CloudBuildOptions",
    "ContainerInfo",
    "CpuUtilization",
    "CreateApplicationRequest",
    "CreateAuthorizedCertificateRequest",
    "CreateDomainMappingRequest",
    "CreateIngressRuleRequest",
    "CreateVersionMetadataV1",
    "CreateVersionMethod",
    "CreateVersionRequest",
    "DebugInstanceRequest",
    "DeleteAuthorizedCertificateRequest",
    "DeleteDomainMappingRequest",
    "DeleteIngressRuleRequest",
    "DeleteInstanceRequest",
    "DeleteServiceRequest",
    "DeleteVersionRequest",
    "Deployment",
    "DiskUtilization",
    "DomainMapping",
    "DomainMappingsClient",
    "DomainOverrideStrategy",
    "EndpointsApiService",
    "Entrypoint",
    "ErrorHandler",
    "FileInfo",
    "FirewallClient",
    "FirewallRule",
    "GetApplicationRequest",
    "GetAuthorizedCertificateRequest",
    "GetDomainMappingRequest",
    "GetIngressRuleRequest",
    "GetInstanceRequest",
    "GetServiceRequest",
    "GetVersionRequest",
    "HealthCheck",
    "InboundServiceType",
    "Instance",
    "InstancesClient",
    "Library",
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
    "LivenessCheck",
    "LocationMetadata",
    "LoginRequirement",
    "ManagedCertificate",
    "ManagementStatus",
    "ManualScaling",
    "Network",
    "NetworkSettings",
    "NetworkUtilization",
    "OperationMetadataV1",
    "ReadinessCheck",
    "RepairApplicationRequest",
    "RequestUtilization",
    "ResourceRecord",
    "Resources",
    "ScriptHandler",
    "SecurityLevel",
    "Service",
    "ServicesClient",
    "ServingStatus",
    "SslSettings",
    "StandardSchedulerSettings",
    "StaticFilesHandler",
    "TrafficSplit",
    "UpdateApplicationRequest",
    "UpdateAuthorizedCertificateRequest",
    "UpdateDomainMappingRequest",
    "UpdateIngressRuleRequest",
    "UpdateServiceMethod",
    "UpdateServiceRequest",
    "UpdateVersionRequest",
    "UrlDispatchRule",
    "UrlMap",
    "Version",
    "VersionView",
    "VersionsClient",
    "Volume",
    "VpcAccessConnector",
    "ZipInfo",
)
