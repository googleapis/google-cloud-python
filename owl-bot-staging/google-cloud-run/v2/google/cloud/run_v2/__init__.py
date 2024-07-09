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
from google.cloud.run_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.executions import ExecutionsClient
from .services.executions import ExecutionsAsyncClient
from .services.jobs import JobsClient
from .services.jobs import JobsAsyncClient
from .services.revisions import RevisionsClient
from .services.revisions import RevisionsAsyncClient
from .services.services import ServicesClient
from .services.services import ServicesAsyncClient
from .services.tasks import TasksClient
from .services.tasks import TasksAsyncClient

from .types.condition import Condition
from .types.execution import CancelExecutionRequest
from .types.execution import DeleteExecutionRequest
from .types.execution import Execution
from .types.execution import GetExecutionRequest
from .types.execution import ListExecutionsRequest
from .types.execution import ListExecutionsResponse
from .types.execution_template import ExecutionTemplate
from .types.job import CreateJobRequest
from .types.job import DeleteJobRequest
from .types.job import ExecutionReference
from .types.job import GetJobRequest
from .types.job import Job
from .types.job import ListJobsRequest
from .types.job import ListJobsResponse
from .types.job import RunJobRequest
from .types.job import UpdateJobRequest
from .types.k8s_min import CloudSqlInstance
from .types.k8s_min import Container
from .types.k8s_min import ContainerPort
from .types.k8s_min import EmptyDirVolumeSource
from .types.k8s_min import EnvVar
from .types.k8s_min import EnvVarSource
from .types.k8s_min import GCSVolumeSource
from .types.k8s_min import GRPCAction
from .types.k8s_min import HTTPGetAction
from .types.k8s_min import HTTPHeader
from .types.k8s_min import NFSVolumeSource
from .types.k8s_min import Probe
from .types.k8s_min import ResourceRequirements
from .types.k8s_min import SecretKeySelector
from .types.k8s_min import SecretVolumeSource
from .types.k8s_min import TCPSocketAction
from .types.k8s_min import VersionToPath
from .types.k8s_min import Volume
from .types.k8s_min import VolumeMount
from .types.revision import DeleteRevisionRequest
from .types.revision import GetRevisionRequest
from .types.revision import ListRevisionsRequest
from .types.revision import ListRevisionsResponse
from .types.revision import Revision
from .types.revision_template import RevisionTemplate
from .types.service import CreateServiceRequest
from .types.service import DeleteServiceRequest
from .types.service import GetServiceRequest
from .types.service import ListServicesRequest
from .types.service import ListServicesResponse
from .types.service import Service
from .types.service import UpdateServiceRequest
from .types.status import RevisionScalingStatus
from .types.task import GetTaskRequest
from .types.task import ListTasksRequest
from .types.task import ListTasksResponse
from .types.task import Task
from .types.task import TaskAttemptResult
from .types.task_template import TaskTemplate
from .types.traffic_target import TrafficTarget
from .types.traffic_target import TrafficTargetStatus
from .types.traffic_target import TrafficTargetAllocationType
from .types.vendor_settings import BinaryAuthorization
from .types.vendor_settings import RevisionScaling
from .types.vendor_settings import ServiceScaling
from .types.vendor_settings import VpcAccess
from .types.vendor_settings import EncryptionKeyRevocationAction
from .types.vendor_settings import ExecutionEnvironment
from .types.vendor_settings import IngressTraffic

__all__ = (
    'ExecutionsAsyncClient',
    'JobsAsyncClient',
    'RevisionsAsyncClient',
    'ServicesAsyncClient',
    'TasksAsyncClient',
'BinaryAuthorization',
'CancelExecutionRequest',
'CloudSqlInstance',
'Condition',
'Container',
'ContainerPort',
'CreateJobRequest',
'CreateServiceRequest',
'DeleteExecutionRequest',
'DeleteJobRequest',
'DeleteRevisionRequest',
'DeleteServiceRequest',
'EmptyDirVolumeSource',
'EncryptionKeyRevocationAction',
'EnvVar',
'EnvVarSource',
'Execution',
'ExecutionEnvironment',
'ExecutionReference',
'ExecutionTemplate',
'ExecutionsClient',
'GCSVolumeSource',
'GRPCAction',
'GetExecutionRequest',
'GetJobRequest',
'GetRevisionRequest',
'GetServiceRequest',
'GetTaskRequest',
'HTTPGetAction',
'HTTPHeader',
'IngressTraffic',
'Job',
'JobsClient',
'ListExecutionsRequest',
'ListExecutionsResponse',
'ListJobsRequest',
'ListJobsResponse',
'ListRevisionsRequest',
'ListRevisionsResponse',
'ListServicesRequest',
'ListServicesResponse',
'ListTasksRequest',
'ListTasksResponse',
'NFSVolumeSource',
'Probe',
'ResourceRequirements',
'Revision',
'RevisionScaling',
'RevisionScalingStatus',
'RevisionTemplate',
'RevisionsClient',
'RunJobRequest',
'SecretKeySelector',
'SecretVolumeSource',
'Service',
'ServiceScaling',
'ServicesClient',
'TCPSocketAction',
'Task',
'TaskAttemptResult',
'TaskTemplate',
'TasksClient',
'TrafficTarget',
'TrafficTargetAllocationType',
'TrafficTargetStatus',
'UpdateJobRequest',
'UpdateServiceRequest',
'VersionToPath',
'Volume',
'VolumeMount',
'VpcAccess',
)
