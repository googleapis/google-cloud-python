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
from google.cloud.deploy_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.cloud_deploy import CloudDeployClient
from .services.cloud_deploy import CloudDeployAsyncClient

from .types.automation_payload import AutomationEvent
from .types.automationrun_payload import AutomationRunEvent
from .types.cloud_deploy import AbandonReleaseRequest
from .types.cloud_deploy import AbandonReleaseResponse
from .types.cloud_deploy import AdvanceChildRolloutJob
from .types.cloud_deploy import AdvanceChildRolloutJobRun
from .types.cloud_deploy import AdvanceRolloutOperation
from .types.cloud_deploy import AdvanceRolloutRequest
from .types.cloud_deploy import AdvanceRolloutResponse
from .types.cloud_deploy import AdvanceRolloutRule
from .types.cloud_deploy import AnthosCluster
from .types.cloud_deploy import ApproveRolloutRequest
from .types.cloud_deploy import ApproveRolloutResponse
from .types.cloud_deploy import AssociatedEntities
from .types.cloud_deploy import Automation
from .types.cloud_deploy import AutomationResourceSelector
from .types.cloud_deploy import AutomationRolloutMetadata
from .types.cloud_deploy import AutomationRule
from .types.cloud_deploy import AutomationRuleCondition
from .types.cloud_deploy import AutomationRun
from .types.cloud_deploy import BuildArtifact
from .types.cloud_deploy import Canary
from .types.cloud_deploy import CanaryDeployment
from .types.cloud_deploy import CancelAutomationRunRequest
from .types.cloud_deploy import CancelAutomationRunResponse
from .types.cloud_deploy import CancelRolloutRequest
from .types.cloud_deploy import CancelRolloutResponse
from .types.cloud_deploy import ChildRolloutJobs
from .types.cloud_deploy import CloudRunConfig
from .types.cloud_deploy import CloudRunLocation
from .types.cloud_deploy import CloudRunMetadata
from .types.cloud_deploy import CloudRunRenderMetadata
from .types.cloud_deploy import Config
from .types.cloud_deploy import CreateAutomationRequest
from .types.cloud_deploy import CreateChildRolloutJob
from .types.cloud_deploy import CreateChildRolloutJobRun
from .types.cloud_deploy import CreateCustomTargetTypeRequest
from .types.cloud_deploy import CreateDeliveryPipelineRequest
from .types.cloud_deploy import CreateDeployPolicyRequest
from .types.cloud_deploy import CreateReleaseRequest
from .types.cloud_deploy import CreateRolloutRequest
from .types.cloud_deploy import CreateTargetRequest
from .types.cloud_deploy import CustomCanaryDeployment
from .types.cloud_deploy import CustomMetadata
from .types.cloud_deploy import CustomTarget
from .types.cloud_deploy import CustomTargetDeployMetadata
from .types.cloud_deploy import CustomTargetSkaffoldActions
from .types.cloud_deploy import CustomTargetType
from .types.cloud_deploy import DefaultPool
from .types.cloud_deploy import DeleteAutomationRequest
from .types.cloud_deploy import DeleteCustomTargetTypeRequest
from .types.cloud_deploy import DeleteDeliveryPipelineRequest
from .types.cloud_deploy import DeleteDeployPolicyRequest
from .types.cloud_deploy import DeleteTargetRequest
from .types.cloud_deploy import DeliveryPipeline
from .types.cloud_deploy import DeliveryPipelineAttribute
from .types.cloud_deploy import DeployArtifact
from .types.cloud_deploy import DeployJob
from .types.cloud_deploy import DeployJobRun
from .types.cloud_deploy import DeployJobRunMetadata
from .types.cloud_deploy import DeploymentJobs
from .types.cloud_deploy import DeployParameters
from .types.cloud_deploy import DeployPolicy
from .types.cloud_deploy import DeployPolicyResourceSelector
from .types.cloud_deploy import ExecutionConfig
from .types.cloud_deploy import GetAutomationRequest
from .types.cloud_deploy import GetAutomationRunRequest
from .types.cloud_deploy import GetConfigRequest
from .types.cloud_deploy import GetCustomTargetTypeRequest
from .types.cloud_deploy import GetDeliveryPipelineRequest
from .types.cloud_deploy import GetDeployPolicyRequest
from .types.cloud_deploy import GetJobRunRequest
from .types.cloud_deploy import GetReleaseRequest
from .types.cloud_deploy import GetRolloutRequest
from .types.cloud_deploy import GetTargetRequest
from .types.cloud_deploy import GkeCluster
from .types.cloud_deploy import IgnoreJobRequest
from .types.cloud_deploy import IgnoreJobResponse
from .types.cloud_deploy import Job
from .types.cloud_deploy import JobRun
from .types.cloud_deploy import KubernetesConfig
from .types.cloud_deploy import ListAutomationRunsRequest
from .types.cloud_deploy import ListAutomationRunsResponse
from .types.cloud_deploy import ListAutomationsRequest
from .types.cloud_deploy import ListAutomationsResponse
from .types.cloud_deploy import ListCustomTargetTypesRequest
from .types.cloud_deploy import ListCustomTargetTypesResponse
from .types.cloud_deploy import ListDeliveryPipelinesRequest
from .types.cloud_deploy import ListDeliveryPipelinesResponse
from .types.cloud_deploy import ListDeployPoliciesRequest
from .types.cloud_deploy import ListDeployPoliciesResponse
from .types.cloud_deploy import ListJobRunsRequest
from .types.cloud_deploy import ListJobRunsResponse
from .types.cloud_deploy import ListReleasesRequest
from .types.cloud_deploy import ListReleasesResponse
from .types.cloud_deploy import ListRolloutsRequest
from .types.cloud_deploy import ListRolloutsResponse
from .types.cloud_deploy import ListTargetsRequest
from .types.cloud_deploy import ListTargetsResponse
from .types.cloud_deploy import Metadata
from .types.cloud_deploy import MultiTarget
from .types.cloud_deploy import OneTimeWindow
from .types.cloud_deploy import OperationMetadata
from .types.cloud_deploy import Phase
from .types.cloud_deploy import PipelineCondition
from .types.cloud_deploy import PipelineReadyCondition
from .types.cloud_deploy import PolicyRule
from .types.cloud_deploy import PolicyViolation
from .types.cloud_deploy import PolicyViolationDetails
from .types.cloud_deploy import Postdeploy
from .types.cloud_deploy import PostdeployJob
from .types.cloud_deploy import PostdeployJobRun
from .types.cloud_deploy import Predeploy
from .types.cloud_deploy import PredeployJob
from .types.cloud_deploy import PredeployJobRun
from .types.cloud_deploy import PrivatePool
from .types.cloud_deploy import PromoteReleaseOperation
from .types.cloud_deploy import PromoteReleaseRule
from .types.cloud_deploy import Release
from .types.cloud_deploy import RenderMetadata
from .types.cloud_deploy import RepairPhase
from .types.cloud_deploy import RepairPhaseConfig
from .types.cloud_deploy import RepairRolloutOperation
from .types.cloud_deploy import RepairRolloutRule
from .types.cloud_deploy import Retry
from .types.cloud_deploy import RetryAttempt
from .types.cloud_deploy import RetryJobRequest
from .types.cloud_deploy import RetryJobResponse
from .types.cloud_deploy import RetryPhase
from .types.cloud_deploy import Rollback
from .types.cloud_deploy import RollbackAttempt
from .types.cloud_deploy import RollbackTargetConfig
from .types.cloud_deploy import RollbackTargetRequest
from .types.cloud_deploy import RollbackTargetResponse
from .types.cloud_deploy import Rollout
from .types.cloud_deploy import RolloutRestriction
from .types.cloud_deploy import RuntimeConfig
from .types.cloud_deploy import SerialPipeline
from .types.cloud_deploy import SkaffoldModules
from .types.cloud_deploy import SkaffoldVersion
from .types.cloud_deploy import Stage
from .types.cloud_deploy import Standard
from .types.cloud_deploy import Strategy
from .types.cloud_deploy import Target
from .types.cloud_deploy import TargetArtifact
from .types.cloud_deploy import TargetAttribute
from .types.cloud_deploy import TargetsPresentCondition
from .types.cloud_deploy import TargetsTypeCondition
from .types.cloud_deploy import TerminateJobRunRequest
from .types.cloud_deploy import TerminateJobRunResponse
from .types.cloud_deploy import TimeWindows
from .types.cloud_deploy import UpdateAutomationRequest
from .types.cloud_deploy import UpdateCustomTargetTypeRequest
from .types.cloud_deploy import UpdateDeliveryPipelineRequest
from .types.cloud_deploy import UpdateDeployPolicyRequest
from .types.cloud_deploy import UpdateTargetRequest
from .types.cloud_deploy import VerifyJob
from .types.cloud_deploy import VerifyJobRun
from .types.cloud_deploy import WeeklyWindow
from .types.cloud_deploy import BackoffMode
from .types.cloud_deploy import RepairState
from .types.cloud_deploy import SkaffoldSupportState
from .types.customtargettype_notification_payload import CustomTargetTypeNotificationEvent
from .types.deliverypipeline_notification_payload import DeliveryPipelineNotificationEvent
from .types.deploypolicy_evaluation_payload import DeployPolicyEvaluationEvent
from .types.deploypolicy_notification_payload import DeployPolicyNotificationEvent
from .types.jobrun_notification_payload import JobRunNotificationEvent
from .types.log_enums import Type
from .types.release_notification_payload import ReleaseNotificationEvent
from .types.release_render_payload import ReleaseRenderEvent
from .types.rollout_notification_payload import RolloutNotificationEvent
from .types.rollout_update_payload import RolloutUpdateEvent
from .types.target_notification_payload import TargetNotificationEvent

__all__ = (
    'CloudDeployAsyncClient',
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
'AutomationEvent',
'AutomationResourceSelector',
'AutomationRolloutMetadata',
'AutomationRule',
'AutomationRuleCondition',
'AutomationRun',
'AutomationRunEvent',
'BackoffMode',
'BuildArtifact',
'Canary',
'CanaryDeployment',
'CancelAutomationRunRequest',
'CancelAutomationRunResponse',
'CancelRolloutRequest',
'CancelRolloutResponse',
'ChildRolloutJobs',
'CloudDeployClient',
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
'CustomTargetTypeNotificationEvent',
'DefaultPool',
'DeleteAutomationRequest',
'DeleteCustomTargetTypeRequest',
'DeleteDeliveryPipelineRequest',
'DeleteDeployPolicyRequest',
'DeleteTargetRequest',
'DeliveryPipeline',
'DeliveryPipelineAttribute',
'DeliveryPipelineNotificationEvent',
'DeployArtifact',
'DeployJob',
'DeployJobRun',
'DeployJobRunMetadata',
'DeployParameters',
'DeployPolicy',
'DeployPolicyEvaluationEvent',
'DeployPolicyNotificationEvent',
'DeployPolicyResourceSelector',
'DeploymentJobs',
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
'JobRunNotificationEvent',
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
'ReleaseNotificationEvent',
'ReleaseRenderEvent',
'RenderMetadata',
'RepairPhase',
'RepairPhaseConfig',
'RepairRolloutOperation',
'RepairRolloutRule',
'RepairState',
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
'RolloutNotificationEvent',
'RolloutRestriction',
'RolloutUpdateEvent',
'RuntimeConfig',
'SerialPipeline',
'SkaffoldModules',
'SkaffoldSupportState',
'SkaffoldVersion',
'Stage',
'Standard',
'Strategy',
'Target',
'TargetArtifact',
'TargetAttribute',
'TargetNotificationEvent',
'TargetsPresentCondition',
'TargetsTypeCondition',
'TerminateJobRunRequest',
'TerminateJobRunResponse',
'TimeWindows',
'Type',
'UpdateAutomationRequest',
'UpdateCustomTargetTypeRequest',
'UpdateDeliveryPipelineRequest',
'UpdateDeployPolicyRequest',
'UpdateTargetRequest',
'VerifyJob',
'VerifyJobRun',
'WeeklyWindow',
)
