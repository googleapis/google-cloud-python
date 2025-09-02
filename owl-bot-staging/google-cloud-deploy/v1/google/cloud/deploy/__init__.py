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
from google.cloud.deploy import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.deploy_v1.services.cloud_deploy.client import CloudDeployClient
from google.cloud.deploy_v1.services.cloud_deploy.async_client import CloudDeployAsyncClient

from google.cloud.deploy_v1.types.automation_payload import AutomationEvent
from google.cloud.deploy_v1.types.automationrun_payload import AutomationRunEvent
from google.cloud.deploy_v1.types.cloud_deploy import AbandonReleaseRequest
from google.cloud.deploy_v1.types.cloud_deploy import AbandonReleaseResponse
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceChildRolloutJob
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceChildRolloutJobRun
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceRolloutOperation
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceRolloutRequest
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceRolloutResponse
from google.cloud.deploy_v1.types.cloud_deploy import AdvanceRolloutRule
from google.cloud.deploy_v1.types.cloud_deploy import AnthosCluster
from google.cloud.deploy_v1.types.cloud_deploy import ApproveRolloutRequest
from google.cloud.deploy_v1.types.cloud_deploy import ApproveRolloutResponse
from google.cloud.deploy_v1.types.cloud_deploy import AssociatedEntities
from google.cloud.deploy_v1.types.cloud_deploy import Automation
from google.cloud.deploy_v1.types.cloud_deploy import AutomationResourceSelector
from google.cloud.deploy_v1.types.cloud_deploy import AutomationRolloutMetadata
from google.cloud.deploy_v1.types.cloud_deploy import AutomationRule
from google.cloud.deploy_v1.types.cloud_deploy import AutomationRuleCondition
from google.cloud.deploy_v1.types.cloud_deploy import AutomationRun
from google.cloud.deploy_v1.types.cloud_deploy import BuildArtifact
from google.cloud.deploy_v1.types.cloud_deploy import Canary
from google.cloud.deploy_v1.types.cloud_deploy import CanaryDeployment
from google.cloud.deploy_v1.types.cloud_deploy import CancelAutomationRunRequest
from google.cloud.deploy_v1.types.cloud_deploy import CancelAutomationRunResponse
from google.cloud.deploy_v1.types.cloud_deploy import CancelRolloutRequest
from google.cloud.deploy_v1.types.cloud_deploy import CancelRolloutResponse
from google.cloud.deploy_v1.types.cloud_deploy import ChildRolloutJobs
from google.cloud.deploy_v1.types.cloud_deploy import CloudRunConfig
from google.cloud.deploy_v1.types.cloud_deploy import CloudRunLocation
from google.cloud.deploy_v1.types.cloud_deploy import CloudRunMetadata
from google.cloud.deploy_v1.types.cloud_deploy import CloudRunRenderMetadata
from google.cloud.deploy_v1.types.cloud_deploy import Config
from google.cloud.deploy_v1.types.cloud_deploy import CreateAutomationRequest
from google.cloud.deploy_v1.types.cloud_deploy import CreateChildRolloutJob
from google.cloud.deploy_v1.types.cloud_deploy import CreateChildRolloutJobRun
from google.cloud.deploy_v1.types.cloud_deploy import CreateCustomTargetTypeRequest
from google.cloud.deploy_v1.types.cloud_deploy import CreateDeliveryPipelineRequest
from google.cloud.deploy_v1.types.cloud_deploy import CreateDeployPolicyRequest
from google.cloud.deploy_v1.types.cloud_deploy import CreateReleaseRequest
from google.cloud.deploy_v1.types.cloud_deploy import CreateRolloutRequest
from google.cloud.deploy_v1.types.cloud_deploy import CreateTargetRequest
from google.cloud.deploy_v1.types.cloud_deploy import CustomCanaryDeployment
from google.cloud.deploy_v1.types.cloud_deploy import CustomMetadata
from google.cloud.deploy_v1.types.cloud_deploy import CustomTarget
from google.cloud.deploy_v1.types.cloud_deploy import CustomTargetDeployMetadata
from google.cloud.deploy_v1.types.cloud_deploy import CustomTargetSkaffoldActions
from google.cloud.deploy_v1.types.cloud_deploy import CustomTargetType
from google.cloud.deploy_v1.types.cloud_deploy import DefaultPool
from google.cloud.deploy_v1.types.cloud_deploy import DeleteAutomationRequest
from google.cloud.deploy_v1.types.cloud_deploy import DeleteCustomTargetTypeRequest
from google.cloud.deploy_v1.types.cloud_deploy import DeleteDeliveryPipelineRequest
from google.cloud.deploy_v1.types.cloud_deploy import DeleteDeployPolicyRequest
from google.cloud.deploy_v1.types.cloud_deploy import DeleteTargetRequest
from google.cloud.deploy_v1.types.cloud_deploy import DeliveryPipeline
from google.cloud.deploy_v1.types.cloud_deploy import DeliveryPipelineAttribute
from google.cloud.deploy_v1.types.cloud_deploy import DeployArtifact
from google.cloud.deploy_v1.types.cloud_deploy import DeployJob
from google.cloud.deploy_v1.types.cloud_deploy import DeployJobRun
from google.cloud.deploy_v1.types.cloud_deploy import DeployJobRunMetadata
from google.cloud.deploy_v1.types.cloud_deploy import DeploymentJobs
from google.cloud.deploy_v1.types.cloud_deploy import DeployParameters
from google.cloud.deploy_v1.types.cloud_deploy import DeployPolicy
from google.cloud.deploy_v1.types.cloud_deploy import DeployPolicyResourceSelector
from google.cloud.deploy_v1.types.cloud_deploy import ExecutionConfig
from google.cloud.deploy_v1.types.cloud_deploy import GetAutomationRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetAutomationRunRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetConfigRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetCustomTargetTypeRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetDeliveryPipelineRequest
from google.cloud.deploy_v1.types.cloud_deploy import GetDeployPolicyRequest
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
from google.cloud.deploy_v1.types.cloud_deploy import ListAutomationRunsRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListAutomationRunsResponse
from google.cloud.deploy_v1.types.cloud_deploy import ListAutomationsRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListAutomationsResponse
from google.cloud.deploy_v1.types.cloud_deploy import ListCustomTargetTypesRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListCustomTargetTypesResponse
from google.cloud.deploy_v1.types.cloud_deploy import ListDeliveryPipelinesRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListDeliveryPipelinesResponse
from google.cloud.deploy_v1.types.cloud_deploy import ListDeployPoliciesRequest
from google.cloud.deploy_v1.types.cloud_deploy import ListDeployPoliciesResponse
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
from google.cloud.deploy_v1.types.cloud_deploy import OneTimeWindow
from google.cloud.deploy_v1.types.cloud_deploy import OperationMetadata
from google.cloud.deploy_v1.types.cloud_deploy import Phase
from google.cloud.deploy_v1.types.cloud_deploy import PipelineCondition
from google.cloud.deploy_v1.types.cloud_deploy import PipelineReadyCondition
from google.cloud.deploy_v1.types.cloud_deploy import PolicyRule
from google.cloud.deploy_v1.types.cloud_deploy import PolicyViolation
from google.cloud.deploy_v1.types.cloud_deploy import PolicyViolationDetails
from google.cloud.deploy_v1.types.cloud_deploy import Postdeploy
from google.cloud.deploy_v1.types.cloud_deploy import PostdeployJob
from google.cloud.deploy_v1.types.cloud_deploy import PostdeployJobRun
from google.cloud.deploy_v1.types.cloud_deploy import Predeploy
from google.cloud.deploy_v1.types.cloud_deploy import PredeployJob
from google.cloud.deploy_v1.types.cloud_deploy import PredeployJobRun
from google.cloud.deploy_v1.types.cloud_deploy import PrivatePool
from google.cloud.deploy_v1.types.cloud_deploy import PromoteReleaseOperation
from google.cloud.deploy_v1.types.cloud_deploy import PromoteReleaseRule
from google.cloud.deploy_v1.types.cloud_deploy import Release
from google.cloud.deploy_v1.types.cloud_deploy import RenderMetadata
from google.cloud.deploy_v1.types.cloud_deploy import RepairPhase
from google.cloud.deploy_v1.types.cloud_deploy import RepairPhaseConfig
from google.cloud.deploy_v1.types.cloud_deploy import RepairRolloutOperation
from google.cloud.deploy_v1.types.cloud_deploy import RepairRolloutRule
from google.cloud.deploy_v1.types.cloud_deploy import Retry
from google.cloud.deploy_v1.types.cloud_deploy import RetryAttempt
from google.cloud.deploy_v1.types.cloud_deploy import RetryJobRequest
from google.cloud.deploy_v1.types.cloud_deploy import RetryJobResponse
from google.cloud.deploy_v1.types.cloud_deploy import RetryPhase
from google.cloud.deploy_v1.types.cloud_deploy import Rollback
from google.cloud.deploy_v1.types.cloud_deploy import RollbackAttempt
from google.cloud.deploy_v1.types.cloud_deploy import RollbackTargetConfig
from google.cloud.deploy_v1.types.cloud_deploy import RollbackTargetRequest
from google.cloud.deploy_v1.types.cloud_deploy import RollbackTargetResponse
from google.cloud.deploy_v1.types.cloud_deploy import Rollout
from google.cloud.deploy_v1.types.cloud_deploy import RolloutRestriction
from google.cloud.deploy_v1.types.cloud_deploy import RuntimeConfig
from google.cloud.deploy_v1.types.cloud_deploy import SerialPipeline
from google.cloud.deploy_v1.types.cloud_deploy import SkaffoldModules
from google.cloud.deploy_v1.types.cloud_deploy import SkaffoldVersion
from google.cloud.deploy_v1.types.cloud_deploy import Stage
from google.cloud.deploy_v1.types.cloud_deploy import Standard
from google.cloud.deploy_v1.types.cloud_deploy import Strategy
from google.cloud.deploy_v1.types.cloud_deploy import Target
from google.cloud.deploy_v1.types.cloud_deploy import TargetArtifact
from google.cloud.deploy_v1.types.cloud_deploy import TargetAttribute
from google.cloud.deploy_v1.types.cloud_deploy import TargetsPresentCondition
from google.cloud.deploy_v1.types.cloud_deploy import TargetsTypeCondition
from google.cloud.deploy_v1.types.cloud_deploy import TerminateJobRunRequest
from google.cloud.deploy_v1.types.cloud_deploy import TerminateJobRunResponse
from google.cloud.deploy_v1.types.cloud_deploy import TimedPromoteReleaseCondition
from google.cloud.deploy_v1.types.cloud_deploy import TimedPromoteReleaseOperation
from google.cloud.deploy_v1.types.cloud_deploy import TimedPromoteReleaseRule
from google.cloud.deploy_v1.types.cloud_deploy import TimeWindows
from google.cloud.deploy_v1.types.cloud_deploy import UpdateAutomationRequest
from google.cloud.deploy_v1.types.cloud_deploy import UpdateCustomTargetTypeRequest
from google.cloud.deploy_v1.types.cloud_deploy import UpdateDeliveryPipelineRequest
from google.cloud.deploy_v1.types.cloud_deploy import UpdateDeployPolicyRequest
from google.cloud.deploy_v1.types.cloud_deploy import UpdateTargetRequest
from google.cloud.deploy_v1.types.cloud_deploy import VerifyJob
from google.cloud.deploy_v1.types.cloud_deploy import VerifyJobRun
from google.cloud.deploy_v1.types.cloud_deploy import WeeklyWindow
from google.cloud.deploy_v1.types.cloud_deploy import BackoffMode
from google.cloud.deploy_v1.types.cloud_deploy import RepairState
from google.cloud.deploy_v1.types.cloud_deploy import SkaffoldSupportState
from google.cloud.deploy_v1.types.customtargettype_notification_payload import CustomTargetTypeNotificationEvent
from google.cloud.deploy_v1.types.deliverypipeline_notification_payload import DeliveryPipelineNotificationEvent
from google.cloud.deploy_v1.types.deploypolicy_evaluation_payload import DeployPolicyEvaluationEvent
from google.cloud.deploy_v1.types.deploypolicy_notification_payload import DeployPolicyNotificationEvent
from google.cloud.deploy_v1.types.jobrun_notification_payload import JobRunNotificationEvent
from google.cloud.deploy_v1.types.log_enums import Type
from google.cloud.deploy_v1.types.release_notification_payload import ReleaseNotificationEvent
from google.cloud.deploy_v1.types.release_render_payload import ReleaseRenderEvent
from google.cloud.deploy_v1.types.rollout_notification_payload import RolloutNotificationEvent
from google.cloud.deploy_v1.types.rollout_update_payload import RolloutUpdateEvent
from google.cloud.deploy_v1.types.target_notification_payload import TargetNotificationEvent

__all__ = ('CloudDeployClient',
    'CloudDeployAsyncClient',
    'AutomationEvent',
    'AutomationRunEvent',
    'AbandonReleaseRequest',
    'AbandonReleaseResponse',
    'AdvanceChildRolloutJob',
    'AdvanceChildRolloutJobRun',
    'AdvanceRolloutOperation',
    'AdvanceRolloutRequest',
    'AdvanceRolloutResponse',
    'AdvanceRolloutRule',
    'AnthosCluster',
    'ApproveRolloutRequest',
    'ApproveRolloutResponse',
    'AssociatedEntities',
    'Automation',
    'AutomationResourceSelector',
    'AutomationRolloutMetadata',
    'AutomationRule',
    'AutomationRuleCondition',
    'AutomationRun',
    'BuildArtifact',
    'Canary',
    'CanaryDeployment',
    'CancelAutomationRunRequest',
    'CancelAutomationRunResponse',
    'CancelRolloutRequest',
    'CancelRolloutResponse',
    'ChildRolloutJobs',
    'CloudRunConfig',
    'CloudRunLocation',
    'CloudRunMetadata',
    'CloudRunRenderMetadata',
    'Config',
    'CreateAutomationRequest',
    'CreateChildRolloutJob',
    'CreateChildRolloutJobRun',
    'CreateCustomTargetTypeRequest',
    'CreateDeliveryPipelineRequest',
    'CreateDeployPolicyRequest',
    'CreateReleaseRequest',
    'CreateRolloutRequest',
    'CreateTargetRequest',
    'CustomCanaryDeployment',
    'CustomMetadata',
    'CustomTarget',
    'CustomTargetDeployMetadata',
    'CustomTargetSkaffoldActions',
    'CustomTargetType',
    'DefaultPool',
    'DeleteAutomationRequest',
    'DeleteCustomTargetTypeRequest',
    'DeleteDeliveryPipelineRequest',
    'DeleteDeployPolicyRequest',
    'DeleteTargetRequest',
    'DeliveryPipeline',
    'DeliveryPipelineAttribute',
    'DeployArtifact',
    'DeployJob',
    'DeployJobRun',
    'DeployJobRunMetadata',
    'DeploymentJobs',
    'DeployParameters',
    'DeployPolicy',
    'DeployPolicyResourceSelector',
    'ExecutionConfig',
    'GetAutomationRequest',
    'GetAutomationRunRequest',
    'GetConfigRequest',
    'GetCustomTargetTypeRequest',
    'GetDeliveryPipelineRequest',
    'GetDeployPolicyRequest',
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
    'ListAutomationRunsRequest',
    'ListAutomationRunsResponse',
    'ListAutomationsRequest',
    'ListAutomationsResponse',
    'ListCustomTargetTypesRequest',
    'ListCustomTargetTypesResponse',
    'ListDeliveryPipelinesRequest',
    'ListDeliveryPipelinesResponse',
    'ListDeployPoliciesRequest',
    'ListDeployPoliciesResponse',
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
    'OneTimeWindow',
    'OperationMetadata',
    'Phase',
    'PipelineCondition',
    'PipelineReadyCondition',
    'PolicyRule',
    'PolicyViolation',
    'PolicyViolationDetails',
    'Postdeploy',
    'PostdeployJob',
    'PostdeployJobRun',
    'Predeploy',
    'PredeployJob',
    'PredeployJobRun',
    'PrivatePool',
    'PromoteReleaseOperation',
    'PromoteReleaseRule',
    'Release',
    'RenderMetadata',
    'RepairPhase',
    'RepairPhaseConfig',
    'RepairRolloutOperation',
    'RepairRolloutRule',
    'Retry',
    'RetryAttempt',
    'RetryJobRequest',
    'RetryJobResponse',
    'RetryPhase',
    'Rollback',
    'RollbackAttempt',
    'RollbackTargetConfig',
    'RollbackTargetRequest',
    'RollbackTargetResponse',
    'Rollout',
    'RolloutRestriction',
    'RuntimeConfig',
    'SerialPipeline',
    'SkaffoldModules',
    'SkaffoldVersion',
    'Stage',
    'Standard',
    'Strategy',
    'Target',
    'TargetArtifact',
    'TargetAttribute',
    'TargetsPresentCondition',
    'TargetsTypeCondition',
    'TerminateJobRunRequest',
    'TerminateJobRunResponse',
    'TimedPromoteReleaseCondition',
    'TimedPromoteReleaseOperation',
    'TimedPromoteReleaseRule',
    'TimeWindows',
    'UpdateAutomationRequest',
    'UpdateCustomTargetTypeRequest',
    'UpdateDeliveryPipelineRequest',
    'UpdateDeployPolicyRequest',
    'UpdateTargetRequest',
    'VerifyJob',
    'VerifyJobRun',
    'WeeklyWindow',
    'BackoffMode',
    'RepairState',
    'SkaffoldSupportState',
    'CustomTargetTypeNotificationEvent',
    'DeliveryPipelineNotificationEvent',
    'DeployPolicyEvaluationEvent',
    'DeployPolicyNotificationEvent',
    'JobRunNotificationEvent',
    'Type',
    'ReleaseNotificationEvent',
    'ReleaseRenderEvent',
    'RolloutNotificationEvent',
    'RolloutUpdateEvent',
    'TargetNotificationEvent',
)
