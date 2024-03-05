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


from .services.executions import ExecutionsAsyncClient, ExecutionsClient
from .services.jobs import JobsAsyncClient, JobsClient
from .services.revisions import RevisionsAsyncClient, RevisionsClient
from .services.services import ServicesAsyncClient, ServicesClient
from .services.tasks import TasksAsyncClient, TasksClient
from .types.condition import Condition
from .types.execution import (
    CancelExecutionRequest,
    DeleteExecutionRequest,
    Execution,
    GetExecutionRequest,
    ListExecutionsRequest,
    ListExecutionsResponse,
)
from .types.execution_template import ExecutionTemplate
from .types.job import (
    CreateJobRequest,
    DeleteJobRequest,
    ExecutionReference,
    GetJobRequest,
    Job,
    ListJobsRequest,
    ListJobsResponse,
    RunJobRequest,
    UpdateJobRequest,
)
from .types.k8s_min import (
    CloudSqlInstance,
    Container,
    ContainerPort,
    EmptyDirVolumeSource,
    EnvVar,
    EnvVarSource,
    GCSVolumeSource,
    GRPCAction,
    HTTPGetAction,
    HTTPHeader,
    NFSVolumeSource,
    Probe,
    ResourceRequirements,
    SecretKeySelector,
    SecretVolumeSource,
    TCPSocketAction,
    VersionToPath,
    Volume,
    VolumeMount,
)
from .types.revision import (
    DeleteRevisionRequest,
    GetRevisionRequest,
    ListRevisionsRequest,
    ListRevisionsResponse,
    Revision,
)
from .types.revision_template import RevisionTemplate
from .types.service import (
    CreateServiceRequest,
    DeleteServiceRequest,
    GetServiceRequest,
    ListServicesRequest,
    ListServicesResponse,
    Service,
    UpdateServiceRequest,
)
from .types.status import RevisionScalingStatus
from .types.task import (
    GetTaskRequest,
    ListTasksRequest,
    ListTasksResponse,
    Task,
    TaskAttemptResult,
)
from .types.task_template import TaskTemplate
from .types.traffic_target import (
    TrafficTarget,
    TrafficTargetAllocationType,
    TrafficTargetStatus,
)
from .types.vendor_settings import (
    BinaryAuthorization,
    EncryptionKeyRevocationAction,
    ExecutionEnvironment,
    IngressTraffic,
    RevisionScaling,
    ServiceScaling,
    VpcAccess,
)

__all__ = (
    "ExecutionsAsyncClient",
    "JobsAsyncClient",
    "RevisionsAsyncClient",
    "ServicesAsyncClient",
    "TasksAsyncClient",
    "BinaryAuthorization",
    "CancelExecutionRequest",
    "CloudSqlInstance",
    "Condition",
    "Container",
    "ContainerPort",
    "CreateJobRequest",
    "CreateServiceRequest",
    "DeleteExecutionRequest",
    "DeleteJobRequest",
    "DeleteRevisionRequest",
    "DeleteServiceRequest",
    "EmptyDirVolumeSource",
    "EncryptionKeyRevocationAction",
    "EnvVar",
    "EnvVarSource",
    "Execution",
    "ExecutionEnvironment",
    "ExecutionReference",
    "ExecutionTemplate",
    "ExecutionsClient",
    "GCSVolumeSource",
    "GRPCAction",
    "GetExecutionRequest",
    "GetJobRequest",
    "GetRevisionRequest",
    "GetServiceRequest",
    "GetTaskRequest",
    "HTTPGetAction",
    "HTTPHeader",
    "IngressTraffic",
    "Job",
    "JobsClient",
    "ListExecutionsRequest",
    "ListExecutionsResponse",
    "ListJobsRequest",
    "ListJobsResponse",
    "ListRevisionsRequest",
    "ListRevisionsResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "ListTasksRequest",
    "ListTasksResponse",
    "NFSVolumeSource",
    "Probe",
    "ResourceRequirements",
    "Revision",
    "RevisionScaling",
    "RevisionScalingStatus",
    "RevisionTemplate",
    "RevisionsClient",
    "RunJobRequest",
    "SecretKeySelector",
    "SecretVolumeSource",
    "Service",
    "ServiceScaling",
    "ServicesClient",
    "TCPSocketAction",
    "Task",
    "TaskAttemptResult",
    "TaskTemplate",
    "TasksClient",
    "TrafficTarget",
    "TrafficTargetAllocationType",
    "TrafficTargetStatus",
    "UpdateJobRequest",
    "UpdateServiceRequest",
    "VersionToPath",
    "Volume",
    "VolumeMount",
    "VpcAccess",
)
