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
from google.cloud.run import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.run_v2.services.executions.client import ExecutionsClient
from google.cloud.run_v2.services.executions.async_client import ExecutionsAsyncClient
from google.cloud.run_v2.services.jobs.client import JobsClient
from google.cloud.run_v2.services.jobs.async_client import JobsAsyncClient
from google.cloud.run_v2.services.revisions.client import RevisionsClient
from google.cloud.run_v2.services.revisions.async_client import RevisionsAsyncClient
from google.cloud.run_v2.services.services.client import ServicesClient
from google.cloud.run_v2.services.services.async_client import ServicesAsyncClient
from google.cloud.run_v2.services.tasks.client import TasksClient
from google.cloud.run_v2.services.tasks.async_client import TasksAsyncClient

from google.cloud.run_v2.types.condition import Condition
from google.cloud.run_v2.types.execution import CancelExecutionRequest
from google.cloud.run_v2.types.execution import DeleteExecutionRequest
from google.cloud.run_v2.types.execution import Execution
from google.cloud.run_v2.types.execution import GetExecutionRequest
from google.cloud.run_v2.types.execution import ListExecutionsRequest
from google.cloud.run_v2.types.execution import ListExecutionsResponse
from google.cloud.run_v2.types.execution_template import ExecutionTemplate
from google.cloud.run_v2.types.job import CreateJobRequest
from google.cloud.run_v2.types.job import DeleteJobRequest
from google.cloud.run_v2.types.job import ExecutionReference
from google.cloud.run_v2.types.job import GetJobRequest
from google.cloud.run_v2.types.job import Job
from google.cloud.run_v2.types.job import ListJobsRequest
from google.cloud.run_v2.types.job import ListJobsResponse
from google.cloud.run_v2.types.job import RunJobRequest
from google.cloud.run_v2.types.job import UpdateJobRequest
from google.cloud.run_v2.types.k8s_min import CloudSqlInstance
from google.cloud.run_v2.types.k8s_min import Container
from google.cloud.run_v2.types.k8s_min import ContainerPort
from google.cloud.run_v2.types.k8s_min import EmptyDirVolumeSource
from google.cloud.run_v2.types.k8s_min import EnvVar
from google.cloud.run_v2.types.k8s_min import EnvVarSource
from google.cloud.run_v2.types.k8s_min import GCSVolumeSource
from google.cloud.run_v2.types.k8s_min import GRPCAction
from google.cloud.run_v2.types.k8s_min import HTTPGetAction
from google.cloud.run_v2.types.k8s_min import HTTPHeader
from google.cloud.run_v2.types.k8s_min import NFSVolumeSource
from google.cloud.run_v2.types.k8s_min import Probe
from google.cloud.run_v2.types.k8s_min import ResourceRequirements
from google.cloud.run_v2.types.k8s_min import SecretKeySelector
from google.cloud.run_v2.types.k8s_min import SecretVolumeSource
from google.cloud.run_v2.types.k8s_min import TCPSocketAction
from google.cloud.run_v2.types.k8s_min import VersionToPath
from google.cloud.run_v2.types.k8s_min import Volume
from google.cloud.run_v2.types.k8s_min import VolumeMount
from google.cloud.run_v2.types.revision import DeleteRevisionRequest
from google.cloud.run_v2.types.revision import GetRevisionRequest
from google.cloud.run_v2.types.revision import ListRevisionsRequest
from google.cloud.run_v2.types.revision import ListRevisionsResponse
from google.cloud.run_v2.types.revision import Revision
from google.cloud.run_v2.types.revision_template import RevisionTemplate
from google.cloud.run_v2.types.service import CreateServiceRequest
from google.cloud.run_v2.types.service import DeleteServiceRequest
from google.cloud.run_v2.types.service import GetServiceRequest
from google.cloud.run_v2.types.service import ListServicesRequest
from google.cloud.run_v2.types.service import ListServicesResponse
from google.cloud.run_v2.types.service import Service
from google.cloud.run_v2.types.service import UpdateServiceRequest
from google.cloud.run_v2.types.status import RevisionScalingStatus
from google.cloud.run_v2.types.task import GetTaskRequest
from google.cloud.run_v2.types.task import ListTasksRequest
from google.cloud.run_v2.types.task import ListTasksResponse
from google.cloud.run_v2.types.task import Task
from google.cloud.run_v2.types.task import TaskAttemptResult
from google.cloud.run_v2.types.task_template import TaskTemplate
from google.cloud.run_v2.types.traffic_target import TrafficTarget
from google.cloud.run_v2.types.traffic_target import TrafficTargetStatus
from google.cloud.run_v2.types.traffic_target import TrafficTargetAllocationType
from google.cloud.run_v2.types.vendor_settings import BinaryAuthorization
from google.cloud.run_v2.types.vendor_settings import RevisionScaling
from google.cloud.run_v2.types.vendor_settings import ServiceScaling
from google.cloud.run_v2.types.vendor_settings import VpcAccess
from google.cloud.run_v2.types.vendor_settings import EncryptionKeyRevocationAction
from google.cloud.run_v2.types.vendor_settings import ExecutionEnvironment
from google.cloud.run_v2.types.vendor_settings import IngressTraffic

__all__ = ('ExecutionsClient',
    'ExecutionsAsyncClient',
    'JobsClient',
    'JobsAsyncClient',
    'RevisionsClient',
    'RevisionsAsyncClient',
    'ServicesClient',
    'ServicesAsyncClient',
    'TasksClient',
    'TasksAsyncClient',
    'Condition',
    'CancelExecutionRequest',
    'DeleteExecutionRequest',
    'Execution',
    'GetExecutionRequest',
    'ListExecutionsRequest',
    'ListExecutionsResponse',
    'ExecutionTemplate',
    'CreateJobRequest',
    'DeleteJobRequest',
    'ExecutionReference',
    'GetJobRequest',
    'Job',
    'ListJobsRequest',
    'ListJobsResponse',
    'RunJobRequest',
    'UpdateJobRequest',
    'CloudSqlInstance',
    'Container',
    'ContainerPort',
    'EmptyDirVolumeSource',
    'EnvVar',
    'EnvVarSource',
    'GCSVolumeSource',
    'GRPCAction',
    'HTTPGetAction',
    'HTTPHeader',
    'NFSVolumeSource',
    'Probe',
    'ResourceRequirements',
    'SecretKeySelector',
    'SecretVolumeSource',
    'TCPSocketAction',
    'VersionToPath',
    'Volume',
    'VolumeMount',
    'DeleteRevisionRequest',
    'GetRevisionRequest',
    'ListRevisionsRequest',
    'ListRevisionsResponse',
    'Revision',
    'RevisionTemplate',
    'CreateServiceRequest',
    'DeleteServiceRequest',
    'GetServiceRequest',
    'ListServicesRequest',
    'ListServicesResponse',
    'Service',
    'UpdateServiceRequest',
    'RevisionScalingStatus',
    'GetTaskRequest',
    'ListTasksRequest',
    'ListTasksResponse',
    'Task',
    'TaskAttemptResult',
    'TaskTemplate',
    'TrafficTarget',
    'TrafficTargetStatus',
    'TrafficTargetAllocationType',
    'BinaryAuthorization',
    'RevisionScaling',
    'ServiceScaling',
    'VpcAccess',
    'EncryptionKeyRevocationAction',
    'ExecutionEnvironment',
    'IngressTraffic',
)
