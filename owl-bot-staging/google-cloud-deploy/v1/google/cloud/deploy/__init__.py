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
from google.cloud.deploy import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.deploy_v1.services.cloud_deploy.client import CloudDeployClient
from google.cloud.deploy_v1.services.cloud_deploy.async_client import CloudDeployAsyncClient

from google.cloud.deploy_v1.types.cloud_deploy import AbandonReleaseRequest
from google.cloud.deploy_v1.types.cloud_deploy import AbandonReleaseResponse
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceChildRolloutJob
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceChildRolloutJobRun
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceRolloutRequest
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceRolloutResponse
from google.cloud.deploy_v1.types.cloud_deploy import AnthosCluster
from google.cloud.deploy_v1.types.cloud_deploy import ApproveRolloutRequest
from google.cloud.deploy_v1.types.cloud_deploy import ApproveRolloutResponse
from google.cloud.deploy_v1.types.cloud_deploy import BuildArtifact
from google.cloud.deploy_v1.types.cloud_deploy import Canary
from google.cloud.deploy_v1.types.cloud_deploy import CanaryDeployment
from google.cloud.deploy_v1.types.cloud_deploy import CancelRolloutRequest
from google.cloud.deploy_v1.types.cloud_deploy import CancelRolloutResponse
from google.cloud.deploy_v1.types.cloud_deploy import ChildRolloutJobs
from google.cloud.deploy_v1.types.cloud_deploy import CloudRunConfig
from google.cloud.deploy_v1.types.cloud_deploy import CloudRunLocation
from google.cloud.deploy_v1.types.cloud_deploy import CloudRunMetadata
from google.cloud.deploy_v1.types.cloud_deploy import CloudRunRenderMetadata
from google.cloud.deploy_v1.types.cloud_deploy import Config
from google.cloud.deploy_v1.types.cloud_deploy import CreateChildRolloutJob
from google.cloud.deploy_v1.types.cloud_deploy import CreateChildRolloutJobRun
from google.cloud.deploy_v1.types.cloud_deploy import CreateDeliveryPipelineRequest
from google.cloud.deploy_v1.types.cloud_deploy import CreateReleaseRequest
from google.cloud.deploy_v1.types.cloud_deploy import CreateRolloutRequest
from google.cloud.deploy_v1.types.cloud_deploy import CreateTargetRequest
from google.cloud.deploy_v1.types.cloud_deploy import CustomCanaryDeployment
from google.cloud.deploy_v1.types.cloud_deploy import DefaultPool
from google.cloud.deploy_v1.types.cloud_deploy import DeleteDeliveryPipelineRequest
from google.cloud.deploy_v1.types.cloud_deploy import DeleteTargetRequest
from google.cloud.deploy_v1.types.cloud_deploy import DeliveryPipeline
from google.cloud.deploy_v1.types.cloud_deploy import DeployArtifact
from google.cloud.deploy_v1.types.cloud_deploy import DeployJob
from google.cloud.deploy_v1.types.cloud_deploy import DeployJobRun
from google.cloud.deploy_v1.types.cloud_deploy import DeployJobRunMetadata
from google.cloud.deploy_v1.types.cloud_deploy import DeploymentJobs
from google.cloud.deploy_v1.types.cloud_deploy import DeployParameters
from google.cloud.deploy_v1.types.cloud_deploy import ExecutionConfig
from google.cloud.deploy_v1.types.cloud_deploy import GetConfigRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetDeliveryPipelineRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetJobRunRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetReleaseRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetRolloutRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetTargetRequest
from google.cloud.deploy_v1.types.cloud_deploy import GkeCluster
from google.cloud.deploy_v1.types.cloud_deploy import IgnoreJobRequest
from google.cloud.deploy_v1.types.cloud_deploy import IgnoreJobResponse
from google.cloud.deploy_v1.types.cloud_deploy import Job
from google.cloud.deploy_v1.types.cloud_deploy import JobRun
from google.cloud.deploy_v1.types.cloud_deploy import KubernetesConfig
from google.cloud.deploy_v1.types.cloud_deploy import ListDeliveryPipelinesRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListDeliveryPipelinesResponse
from google.cloud.deploy_v1.types.cloud_deploy import ListJobRunsRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListJobRunsResponse
from google.cloud.deploy_v1.types.cloud_deploy import ListReleasesRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListReleasesResponse
from google.cloud.deploy_v1.types.cloud_deploy import ListRolloutsRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListRolloutsResponse
from google.cloud.deploy_v1.types.cloud_deploy import ListTargetsRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListTargetsResponse
from google.cloud.deploy_v1.types.cloud_deploy import Metadata
from google.cloud.deploy_v1.types.cloud_deploy import MultiTarget
from google.cloud.deploy_v1.types.cloud_deploy import OperationMetadata
from google.cloud.deploy_v1.types.cloud_deploy import Phase
from google.cloud.deploy_v1.types.cloud_deploy import PipelineCondition
from google.cloud.deploy_v1.types.cloud_deploy import PipelineReadyCondition
from google.cloud.deploy_v1.types.cloud_deploy import Postdeploy
from google.cloud.deploy_v1.types.cloud_deploy import PostdeployJob
from google.cloud.deploy_v1.types.cloud_deploy import PostdeployJobRun
from google.cloud.deploy_v1.types.cloud_deploy import Predeploy
from google.cloud.deploy_v1.types.cloud_deploy import PredeployJob
from google.cloud.deploy_v1.types.cloud_deploy import PredeployJobRun
from google.cloud.deploy_v1.types.cloud_deploy import PrivatePool
from google.cloud.deploy_v1.types.cloud_deploy import Release
from google.cloud.deploy_v1.types.cloud_deploy import RenderMetadata
from google.cloud.deploy_v1.types.cloud_deploy import RetryJobRequest
from google.cloud.deploy_v1.types.cloud_deploy import RetryJobResponse
from google.cloud.deploy_v1.types.cloud_deploy import Rollout
from google.cloud.deploy_v1.types.cloud_deploy import RuntimeConfig
from google.cloud.deploy_v1.types.cloud_deploy import SerialPipeline
from google.cloud.deploy_v1.types.cloud_deploy import SkaffoldVersion
from google.cloud.deploy_v1.types.cloud_deploy import Stage
from google.cloud.deploy_v1.types.cloud_deploy import Standard
from google.cloud.deploy_v1.types.cloud_deploy import Strategy
from google.cloud.deploy_v1.types.cloud_deploy import Target
from google.cloud.deploy_v1.types.cloud_deploy import TargetArtifact
from google.cloud.deploy_v1.types.cloud_deploy import TargetsPresentCondition
from google.cloud.deploy_v1.types.cloud_deploy import TargetsTypeCondition
from google.cloud.deploy_v1.types.cloud_deploy import TerminateJobRunRequest
from google.cloud.deploy_v1.types.cloud_deploy import TerminateJobRunResponse
from google.cloud.deploy_v1.types.cloud_deploy import UpdateDeliveryPipelineRequest
from google.cloud.deploy_v1.types.cloud_deploy import UpdateTargetRequest
from google.cloud.deploy_v1.types.cloud_deploy import VerifyJob
from google.cloud.deploy_v1.types.cloud_deploy import VerifyJobRun
from google.cloud.deploy_v1.types.cloud_deploy import SkaffoldSupportState
from google.cloud.deploy_v1.types.deliverypipeline_notification_payload import DeliveryPipelineNotificationEvent
from google.cloud.deploy_v1.types.jobrun_notification_payload import JobRunNotificationEvent
from google.cloud.deploy_v1.types.log_enums import Type
from google.cloud.deploy_v1.types.release_notification_payload import ReleaseNotificationEvent
from google.cloud.deploy_v1.types.release_render_payload import ReleaseRenderEvent
from google.cloud.deploy_v1.types.rollout_notification_payload import RolloutNotificationEvent
from google.cloud.deploy_v1.types.target_notification_payload import TargetNotificationEvent

__all__ = ('CloudDeployClient',
    'CloudDeployAsyncClient',
    'AbandonReleaseRequest',
    'AbandonReleaseResponse',
    'AdvanceChildRolloutJob',
    'AdvanceChildRolloutJobRun',
    'AdvanceRolloutRequest',
    'AdvanceRolloutResponse',
    'AnthosCluster',
    'ApproveRolloutRequest',
    'ApproveRolloutResponse',
    'BuildArtifact',
    'Canary',
    'CanaryDeployment',
    'CancelRolloutRequest',
    'CancelRolloutResponse',
    'ChildRolloutJobs',
    'CloudRunConfig',
    'CloudRunLocation',
    'CloudRunMetadata',
    'CloudRunRenderMetadata',
    'Config',
    'CreateChildRolloutJob',
    'CreateChildRolloutJobRun',
    'CreateDeliveryPipelineRequest',
    'CreateReleaseRequest',
    'CreateRolloutRequest',
    'CreateTargetRequest',
    'CustomCanaryDeployment',
    'DefaultPool',
    'DeleteDeliveryPipelineRequest',
    'DeleteTargetRequest',
    'DeliveryPipeline',
    'DeployArtifact',
    'DeployJob',
    'DeployJobRun',
    'DeployJobRunMetadata',
    'DeploymentJobs',
    'DeployParameters',
    'ExecutionConfig',
    'GetConfigRequest',
    'GetDeliveryPipelineRequest',
    'GetJobRunRequest',
    'GetReleaseRequest',
    'GetRolloutRequest',
    'GetTargetRequest',
    'GkeCluster',
    'IgnoreJobRequest',
    'IgnoreJobResponse',
    'Job',
    'JobRun',
    'KubernetesConfig',
    'ListDeliveryPipelinesRequest',
    'ListDeliveryPipelinesResponse',
    'ListJobRunsRequest',
    'ListJobRunsResponse',
    'ListReleasesRequest',
    'ListReleasesResponse',
    'ListRolloutsRequest',
    'ListRolloutsResponse',
    'ListTargetsRequest',
    'ListTargetsResponse',
    'Metadata',
    'MultiTarget',
    'OperationMetadata',
    'Phase',
    'PipelineCondition',
    'PipelineReadyCondition',
    'Postdeploy',
    'PostdeployJob',
    'PostdeployJobRun',
    'Predeploy',
    'PredeployJob',
    'PredeployJobRun',
    'PrivatePool',
    'Release',
    'RenderMetadata',
    'RetryJobRequest',
    'RetryJobResponse',
    'Rollout',
    'RuntimeConfig',
    'SerialPipeline',
    'SkaffoldVersion',
    'Stage',
    'Standard',
    'Strategy',
    'Target',
    'TargetArtifact',
    'TargetsPresentCondition',
    'TargetsTypeCondition',
    'TerminateJobRunRequest',
    'TerminateJobRunResponse',
    'UpdateDeliveryPipelineRequest',
    'UpdateTargetRequest',
    'VerifyJob',
    'VerifyJobRun',
    'SkaffoldSupportState',
    'DeliveryPipelineNotificationEvent',
    'JobRunNotificationEvent',
    'Type',
    'ReleaseNotificationEvent',
    'ReleaseRenderEvent',
    'RolloutNotificationEvent',
    'TargetNotificationEvent',
)
