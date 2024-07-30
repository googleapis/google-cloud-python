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

import dataclasses
import json  # type: ignore
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.deploy_v1.types import cloud_deploy

from .base import CloudDeployTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class CloudDeployRestInterceptor:
    """Interceptor for CloudDeploy.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the CloudDeployRestTransport.

    .. code-block:: python
        class MyCustomCloudDeployInterceptor(CloudDeployRestInterceptor):
            def pre_abandon_release(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_abandon_release(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_advance_rollout(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_advance_rollout(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_approve_rollout(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_approve_rollout(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_cancel_automation_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_cancel_automation_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_cancel_rollout(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_cancel_rollout(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_automation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_automation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_custom_target_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_custom_target_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_delivery_pipeline(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_delivery_pipeline(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_release(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_release(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_rollout(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_rollout(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_target(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_target(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_automation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_automation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_custom_target_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_custom_target_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_delivery_pipeline(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_delivery_pipeline(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_target(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_target(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_automation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_automation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_automation_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_automation_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_custom_target_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_custom_target_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_delivery_pipeline(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_delivery_pipeline(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_job_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_job_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_release(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_release(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_rollout(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_rollout(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_target(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_target(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_ignore_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_ignore_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_automation_runs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_automation_runs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_automations(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_automations(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_custom_target_types(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_custom_target_types(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_delivery_pipelines(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_delivery_pipelines(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_job_runs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_job_runs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_releases(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_releases(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_rollouts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_rollouts(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_targets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_targets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_retry_job(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_retry_job(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_rollback_target(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_rollback_target(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_terminate_job_run(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_terminate_job_run(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_automation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_automation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_custom_target_type(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_custom_target_type(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_delivery_pipeline(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_delivery_pipeline(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_target(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_target(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = CloudDeployRestTransport(interceptor=MyCustomCloudDeployInterceptor())
        client = CloudDeployClient(transport=transport)


    """

    def pre_abandon_release(
        self,
        request: cloud_deploy.AbandonReleaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.AbandonReleaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for abandon_release

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_abandon_release(
        self, response: cloud_deploy.AbandonReleaseResponse
    ) -> cloud_deploy.AbandonReleaseResponse:
        """Post-rpc interceptor for abandon_release

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_advance_rollout(
        self,
        request: cloud_deploy.AdvanceRolloutRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.AdvanceRolloutRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for advance_rollout

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_advance_rollout(
        self, response: cloud_deploy.AdvanceRolloutResponse
    ) -> cloud_deploy.AdvanceRolloutResponse:
        """Post-rpc interceptor for advance_rollout

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_approve_rollout(
        self,
        request: cloud_deploy.ApproveRolloutRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.ApproveRolloutRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for approve_rollout

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_approve_rollout(
        self, response: cloud_deploy.ApproveRolloutResponse
    ) -> cloud_deploy.ApproveRolloutResponse:
        """Post-rpc interceptor for approve_rollout

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_automation_run(
        self,
        request: cloud_deploy.CancelAutomationRunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.CancelAutomationRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_automation_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_cancel_automation_run(
        self, response: cloud_deploy.CancelAutomationRunResponse
    ) -> cloud_deploy.CancelAutomationRunResponse:
        """Post-rpc interceptor for cancel_automation_run

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_rollout(
        self,
        request: cloud_deploy.CancelRolloutRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.CancelRolloutRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_rollout

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_cancel_rollout(
        self, response: cloud_deploy.CancelRolloutResponse
    ) -> cloud_deploy.CancelRolloutResponse:
        """Post-rpc interceptor for cancel_rollout

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_create_automation(
        self,
        request: cloud_deploy.CreateAutomationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.CreateAutomationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_automation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_create_automation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_automation

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_create_custom_target_type(
        self,
        request: cloud_deploy.CreateCustomTargetTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.CreateCustomTargetTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_custom_target_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_create_custom_target_type(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_custom_target_type

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_create_delivery_pipeline(
        self,
        request: cloud_deploy.CreateDeliveryPipelineRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.CreateDeliveryPipelineRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_delivery_pipeline

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_create_delivery_pipeline(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_delivery_pipeline

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_create_release(
        self,
        request: cloud_deploy.CreateReleaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.CreateReleaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_release

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_create_release(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_release

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_create_rollout(
        self,
        request: cloud_deploy.CreateRolloutRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.CreateRolloutRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_rollout

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_create_rollout(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_rollout

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_create_target(
        self,
        request: cloud_deploy.CreateTargetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.CreateTargetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_target

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_create_target(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_target

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_delete_automation(
        self,
        request: cloud_deploy.DeleteAutomationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.DeleteAutomationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_automation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_delete_automation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_automation

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_delete_custom_target_type(
        self,
        request: cloud_deploy.DeleteCustomTargetTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.DeleteCustomTargetTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_custom_target_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_delete_custom_target_type(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_custom_target_type

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_delete_delivery_pipeline(
        self,
        request: cloud_deploy.DeleteDeliveryPipelineRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.DeleteDeliveryPipelineRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_delivery_pipeline

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_delete_delivery_pipeline(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_delivery_pipeline

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_delete_target(
        self,
        request: cloud_deploy.DeleteTargetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.DeleteTargetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_target

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_delete_target(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_target

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_automation(
        self,
        request: cloud_deploy.GetAutomationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.GetAutomationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_automation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_automation(
        self, response: cloud_deploy.Automation
    ) -> cloud_deploy.Automation:
        """Post-rpc interceptor for get_automation

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_automation_run(
        self,
        request: cloud_deploy.GetAutomationRunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.GetAutomationRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_automation_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_automation_run(
        self, response: cloud_deploy.AutomationRun
    ) -> cloud_deploy.AutomationRun:
        """Post-rpc interceptor for get_automation_run

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_config(
        self,
        request: cloud_deploy.GetConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.GetConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_config(self, response: cloud_deploy.Config) -> cloud_deploy.Config:
        """Post-rpc interceptor for get_config

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_custom_target_type(
        self,
        request: cloud_deploy.GetCustomTargetTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.GetCustomTargetTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_custom_target_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_custom_target_type(
        self, response: cloud_deploy.CustomTargetType
    ) -> cloud_deploy.CustomTargetType:
        """Post-rpc interceptor for get_custom_target_type

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_delivery_pipeline(
        self,
        request: cloud_deploy.GetDeliveryPipelineRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.GetDeliveryPipelineRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_delivery_pipeline

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_delivery_pipeline(
        self, response: cloud_deploy.DeliveryPipeline
    ) -> cloud_deploy.DeliveryPipeline:
        """Post-rpc interceptor for get_delivery_pipeline

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_job_run(
        self,
        request: cloud_deploy.GetJobRunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.GetJobRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_job_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_job_run(self, response: cloud_deploy.JobRun) -> cloud_deploy.JobRun:
        """Post-rpc interceptor for get_job_run

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_release(
        self,
        request: cloud_deploy.GetReleaseRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.GetReleaseRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_release

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_release(self, response: cloud_deploy.Release) -> cloud_deploy.Release:
        """Post-rpc interceptor for get_release

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_rollout(
        self,
        request: cloud_deploy.GetRolloutRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.GetRolloutRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_rollout

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_rollout(self, response: cloud_deploy.Rollout) -> cloud_deploy.Rollout:
        """Post-rpc interceptor for get_rollout

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_target(
        self,
        request: cloud_deploy.GetTargetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.GetTargetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_target

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_target(self, response: cloud_deploy.Target) -> cloud_deploy.Target:
        """Post-rpc interceptor for get_target

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_ignore_job(
        self,
        request: cloud_deploy.IgnoreJobRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.IgnoreJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for ignore_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_ignore_job(
        self, response: cloud_deploy.IgnoreJobResponse
    ) -> cloud_deploy.IgnoreJobResponse:
        """Post-rpc interceptor for ignore_job

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_automation_runs(
        self,
        request: cloud_deploy.ListAutomationRunsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.ListAutomationRunsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_automation_runs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_automation_runs(
        self, response: cloud_deploy.ListAutomationRunsResponse
    ) -> cloud_deploy.ListAutomationRunsResponse:
        """Post-rpc interceptor for list_automation_runs

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_automations(
        self,
        request: cloud_deploy.ListAutomationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.ListAutomationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_automations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_automations(
        self, response: cloud_deploy.ListAutomationsResponse
    ) -> cloud_deploy.ListAutomationsResponse:
        """Post-rpc interceptor for list_automations

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_custom_target_types(
        self,
        request: cloud_deploy.ListCustomTargetTypesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.ListCustomTargetTypesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_custom_target_types

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_custom_target_types(
        self, response: cloud_deploy.ListCustomTargetTypesResponse
    ) -> cloud_deploy.ListCustomTargetTypesResponse:
        """Post-rpc interceptor for list_custom_target_types

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_delivery_pipelines(
        self,
        request: cloud_deploy.ListDeliveryPipelinesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.ListDeliveryPipelinesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_delivery_pipelines

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_delivery_pipelines(
        self, response: cloud_deploy.ListDeliveryPipelinesResponse
    ) -> cloud_deploy.ListDeliveryPipelinesResponse:
        """Post-rpc interceptor for list_delivery_pipelines

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_job_runs(
        self,
        request: cloud_deploy.ListJobRunsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.ListJobRunsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_job_runs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_job_runs(
        self, response: cloud_deploy.ListJobRunsResponse
    ) -> cloud_deploy.ListJobRunsResponse:
        """Post-rpc interceptor for list_job_runs

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_releases(
        self,
        request: cloud_deploy.ListReleasesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.ListReleasesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_releases

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_releases(
        self, response: cloud_deploy.ListReleasesResponse
    ) -> cloud_deploy.ListReleasesResponse:
        """Post-rpc interceptor for list_releases

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_rollouts(
        self,
        request: cloud_deploy.ListRolloutsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.ListRolloutsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_rollouts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_rollouts(
        self, response: cloud_deploy.ListRolloutsResponse
    ) -> cloud_deploy.ListRolloutsResponse:
        """Post-rpc interceptor for list_rollouts

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_targets(
        self,
        request: cloud_deploy.ListTargetsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.ListTargetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_targets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_targets(
        self, response: cloud_deploy.ListTargetsResponse
    ) -> cloud_deploy.ListTargetsResponse:
        """Post-rpc interceptor for list_targets

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_retry_job(
        self, request: cloud_deploy.RetryJobRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[cloud_deploy.RetryJobRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for retry_job

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_retry_job(
        self, response: cloud_deploy.RetryJobResponse
    ) -> cloud_deploy.RetryJobResponse:
        """Post-rpc interceptor for retry_job

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_rollback_target(
        self,
        request: cloud_deploy.RollbackTargetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.RollbackTargetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for rollback_target

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_rollback_target(
        self, response: cloud_deploy.RollbackTargetResponse
    ) -> cloud_deploy.RollbackTargetResponse:
        """Post-rpc interceptor for rollback_target

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_terminate_job_run(
        self,
        request: cloud_deploy.TerminateJobRunRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.TerminateJobRunRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for terminate_job_run

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_terminate_job_run(
        self, response: cloud_deploy.TerminateJobRunResponse
    ) -> cloud_deploy.TerminateJobRunResponse:
        """Post-rpc interceptor for terminate_job_run

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_update_automation(
        self,
        request: cloud_deploy.UpdateAutomationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.UpdateAutomationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_automation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_update_automation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_automation

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_update_custom_target_type(
        self,
        request: cloud_deploy.UpdateCustomTargetTypeRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.UpdateCustomTargetTypeRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_custom_target_type

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_update_custom_target_type(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_custom_target_type

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_update_delivery_pipeline(
        self,
        request: cloud_deploy.UpdateDeliveryPipelineRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.UpdateDeliveryPipelineRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_delivery_pipeline

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_update_delivery_pipeline(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_delivery_pipeline

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_update_target(
        self,
        request: cloud_deploy.UpdateTargetRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[cloud_deploy.UpdateTargetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_target

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_update_target(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_target

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the CloudDeploy server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the CloudDeploy server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class CloudDeployRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: CloudDeployRestInterceptor


class CloudDeployRestTransport(CloudDeployTransport):
    """REST backend transport for CloudDeploy.

    CloudDeploy service creates and manages Continuous Delivery
    operations on Google Cloud Platform via Skaffold
    (https://skaffold.dev).

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "clouddeploy.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[CloudDeployRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'clouddeploy.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or CloudDeployRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _AbandonRelease(CloudDeployRestStub):
        def __hash__(self):
            return hash("AbandonRelease")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.AbandonReleaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.AbandonReleaseResponse:
            r"""Call the abandon release method over HTTP.

            Args:
                request (~.cloud_deploy.AbandonReleaseRequest):
                    The request object. The request object used by ``AbandonRelease``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.AbandonReleaseResponse:
                    The response object for ``AbandonRelease``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/releases/*}:abandon",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_abandon_release(request, metadata)
            pb_request = cloud_deploy.AbandonReleaseRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.AbandonReleaseResponse()
            pb_resp = cloud_deploy.AbandonReleaseResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_abandon_release(resp)
            return resp

    class _AdvanceRollout(CloudDeployRestStub):
        def __hash__(self):
            return hash("AdvanceRollout")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.AdvanceRolloutRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.AdvanceRolloutResponse:
            r"""Call the advance rollout method over HTTP.

            Args:
                request (~.cloud_deploy.AdvanceRolloutRequest):
                    The request object. The request object used by ``AdvanceRollout``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.AdvanceRolloutResponse:
                    The response object from ``AdvanceRollout``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/releases/*/rollouts/*}:advance",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_advance_rollout(request, metadata)
            pb_request = cloud_deploy.AdvanceRolloutRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.AdvanceRolloutResponse()
            pb_resp = cloud_deploy.AdvanceRolloutResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_advance_rollout(resp)
            return resp

    class _ApproveRollout(CloudDeployRestStub):
        def __hash__(self):
            return hash("ApproveRollout")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.ApproveRolloutRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.ApproveRolloutResponse:
            r"""Call the approve rollout method over HTTP.

            Args:
                request (~.cloud_deploy.ApproveRolloutRequest):
                    The request object. The request object used by ``ApproveRollout``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.ApproveRolloutResponse:
                    The response object from ``ApproveRollout``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/releases/*/rollouts/*}:approve",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_approve_rollout(request, metadata)
            pb_request = cloud_deploy.ApproveRolloutRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.ApproveRolloutResponse()
            pb_resp = cloud_deploy.ApproveRolloutResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_approve_rollout(resp)
            return resp

    class _CancelAutomationRun(CloudDeployRestStub):
        def __hash__(self):
            return hash("CancelAutomationRun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.CancelAutomationRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.CancelAutomationRunResponse:
            r"""Call the cancel automation run method over HTTP.

            Args:
                request (~.cloud_deploy.CancelAutomationRunRequest):
                    The request object. The request object used by ``CancelAutomationRun``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.CancelAutomationRunResponse:
                    The response object from ``CancelAutomationRun``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/automationRuns/*}:cancel",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_cancel_automation_run(
                request, metadata
            )
            pb_request = cloud_deploy.CancelAutomationRunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.CancelAutomationRunResponse()
            pb_resp = cloud_deploy.CancelAutomationRunResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_cancel_automation_run(resp)
            return resp

    class _CancelRollout(CloudDeployRestStub):
        def __hash__(self):
            return hash("CancelRollout")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.CancelRolloutRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.CancelRolloutResponse:
            r"""Call the cancel rollout method over HTTP.

            Args:
                request (~.cloud_deploy.CancelRolloutRequest):
                    The request object. The request object used by ``CancelRollout``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.CancelRolloutResponse:
                    The response object from ``CancelRollout``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/releases/*/rollouts/*}:cancel",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_cancel_rollout(request, metadata)
            pb_request = cloud_deploy.CancelRolloutRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.CancelRolloutResponse()
            pb_resp = cloud_deploy.CancelRolloutResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_cancel_rollout(resp)
            return resp

    class _CreateAutomation(CloudDeployRestStub):
        def __hash__(self):
            return hash("CreateAutomation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "automationId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.CreateAutomationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create automation method over HTTP.

            Args:
                request (~.cloud_deploy.CreateAutomationRequest):
                    The request object. The request object for ``CreateAutomation``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/deliveryPipelines/*}/automations",
                    "body": "automation",
                },
            ]
            request, metadata = self._interceptor.pre_create_automation(
                request, metadata
            )
            pb_request = cloud_deploy.CreateAutomationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_automation(resp)
            return resp

    class _CreateCustomTargetType(CloudDeployRestStub):
        def __hash__(self):
            return hash("CreateCustomTargetType")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "customTargetTypeId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.CreateCustomTargetTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create custom target type method over HTTP.

            Args:
                request (~.cloud_deploy.CreateCustomTargetTypeRequest):
                    The request object. The request object for ``CreateCustomTargetType``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/customTargetTypes",
                    "body": "custom_target_type",
                },
            ]
            request, metadata = self._interceptor.pre_create_custom_target_type(
                request, metadata
            )
            pb_request = cloud_deploy.CreateCustomTargetTypeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_custom_target_type(resp)
            return resp

    class _CreateDeliveryPipeline(CloudDeployRestStub):
        def __hash__(self):
            return hash("CreateDeliveryPipeline")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "deliveryPipelineId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.CreateDeliveryPipelineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create delivery pipeline method over HTTP.

            Args:
                request (~.cloud_deploy.CreateDeliveryPipelineRequest):
                    The request object. The request object for ``CreateDeliveryPipeline``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/deliveryPipelines",
                    "body": "delivery_pipeline",
                },
            ]
            request, metadata = self._interceptor.pre_create_delivery_pipeline(
                request, metadata
            )
            pb_request = cloud_deploy.CreateDeliveryPipelineRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_delivery_pipeline(resp)
            return resp

    class _CreateRelease(CloudDeployRestStub):
        def __hash__(self):
            return hash("CreateRelease")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "releaseId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.CreateReleaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create release method over HTTP.

            Args:
                request (~.cloud_deploy.CreateReleaseRequest):
                    The request object. The request object for ``CreateRelease``,
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/deliveryPipelines/*}/releases",
                    "body": "release",
                },
            ]
            request, metadata = self._interceptor.pre_create_release(request, metadata)
            pb_request = cloud_deploy.CreateReleaseRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_release(resp)
            return resp

    class _CreateRollout(CloudDeployRestStub):
        def __hash__(self):
            return hash("CreateRollout")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "rolloutId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.CreateRolloutRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create rollout method over HTTP.

            Args:
                request (~.cloud_deploy.CreateRolloutRequest):
                    The request object. CreateRolloutRequest is the request object used by
                ``CreateRollout``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/deliveryPipelines/*/releases/*}/rollouts",
                    "body": "rollout",
                },
            ]
            request, metadata = self._interceptor.pre_create_rollout(request, metadata)
            pb_request = cloud_deploy.CreateRolloutRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_rollout(resp)
            return resp

    class _CreateTarget(CloudDeployRestStub):
        def __hash__(self):
            return hash("CreateTarget")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "targetId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.CreateTargetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create target method over HTTP.

            Args:
                request (~.cloud_deploy.CreateTargetRequest):
                    The request object. The request object for ``CreateTarget``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/targets",
                    "body": "target",
                },
            ]
            request, metadata = self._interceptor.pre_create_target(request, metadata)
            pb_request = cloud_deploy.CreateTargetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_target(resp)
            return resp

    class _DeleteAutomation(CloudDeployRestStub):
        def __hash__(self):
            return hash("DeleteAutomation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.DeleteAutomationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete automation method over HTTP.

            Args:
                request (~.cloud_deploy.DeleteAutomationRequest):
                    The request object. The request object for ``DeleteAutomation``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/automations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_automation(
                request, metadata
            )
            pb_request = cloud_deploy.DeleteAutomationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_automation(resp)
            return resp

    class _DeleteCustomTargetType(CloudDeployRestStub):
        def __hash__(self):
            return hash("DeleteCustomTargetType")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.DeleteCustomTargetTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete custom target type method over HTTP.

            Args:
                request (~.cloud_deploy.DeleteCustomTargetTypeRequest):
                    The request object. The request object for ``DeleteCustomTargetType``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/customTargetTypes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_custom_target_type(
                request, metadata
            )
            pb_request = cloud_deploy.DeleteCustomTargetTypeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_custom_target_type(resp)
            return resp

    class _DeleteDeliveryPipeline(CloudDeployRestStub):
        def __hash__(self):
            return hash("DeleteDeliveryPipeline")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.DeleteDeliveryPipelineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete delivery pipeline method over HTTP.

            Args:
                request (~.cloud_deploy.DeleteDeliveryPipelineRequest):
                    The request object. The request object for ``DeleteDeliveryPipeline``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_delivery_pipeline(
                request, metadata
            )
            pb_request = cloud_deploy.DeleteDeliveryPipelineRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_delivery_pipeline(resp)
            return resp

    class _DeleteTarget(CloudDeployRestStub):
        def __hash__(self):
            return hash("DeleteTarget")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.DeleteTargetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete target method over HTTP.

            Args:
                request (~.cloud_deploy.DeleteTargetRequest):
                    The request object. The request object for ``DeleteTarget``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/targets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_target(request, metadata)
            pb_request = cloud_deploy.DeleteTargetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_target(resp)
            return resp

    class _GetAutomation(CloudDeployRestStub):
        def __hash__(self):
            return hash("GetAutomation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.GetAutomationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.Automation:
            r"""Call the get automation method over HTTP.

            Args:
                request (~.cloud_deploy.GetAutomationRequest):
                    The request object. The request object for ``GetAutomation``
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.Automation:
                    An ``Automation`` resource in the Cloud Deploy API.

                An ``Automation`` enables the automation of manually
                driven actions for a Delivery Pipeline, which includes
                Release promotion among Targets, Rollout repair and
                Rollout deployment strategy advancement. The intention
                of Automation is to reduce manual intervention in the
                continuous delivery process.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/automations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_automation(request, metadata)
            pb_request = cloud_deploy.GetAutomationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.Automation()
            pb_resp = cloud_deploy.Automation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_automation(resp)
            return resp

    class _GetAutomationRun(CloudDeployRestStub):
        def __hash__(self):
            return hash("GetAutomationRun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.GetAutomationRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.AutomationRun:
            r"""Call the get automation run method over HTTP.

            Args:
                request (~.cloud_deploy.GetAutomationRunRequest):
                    The request object. The request object for ``GetAutomationRun``
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.AutomationRun:
                    An ``AutomationRun`` resource in the Cloud Deploy API.

                An ``AutomationRun`` represents an execution instance of
                an automation rule.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/automationRuns/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_automation_run(
                request, metadata
            )
            pb_request = cloud_deploy.GetAutomationRunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.AutomationRun()
            pb_resp = cloud_deploy.AutomationRun.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_automation_run(resp)
            return resp

    class _GetConfig(CloudDeployRestStub):
        def __hash__(self):
            return hash("GetConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.GetConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.Config:
            r"""Call the get config method over HTTP.

            Args:
                request (~.cloud_deploy.GetConfigRequest):
                    The request object. Request to get a configuration.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.Config:
                    Service-wide configuration.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/config}",
                },
            ]
            request, metadata = self._interceptor.pre_get_config(request, metadata)
            pb_request = cloud_deploy.GetConfigRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.Config()
            pb_resp = cloud_deploy.Config.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_config(resp)
            return resp

    class _GetCustomTargetType(CloudDeployRestStub):
        def __hash__(self):
            return hash("GetCustomTargetType")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.GetCustomTargetTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.CustomTargetType:
            r"""Call the get custom target type method over HTTP.

            Args:
                request (~.cloud_deploy.GetCustomTargetTypeRequest):
                    The request object. The request object for ``GetCustomTargetType``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.CustomTargetType:
                    A ``CustomTargetType`` resource in the Cloud Deploy API.

                A ``CustomTargetType`` defines a type of custom target
                that can be referenced in a ``Target`` in order to
                facilitate deploying to other systems besides the
                supported runtimes.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/customTargetTypes/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_custom_target_type(
                request, metadata
            )
            pb_request = cloud_deploy.GetCustomTargetTypeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.CustomTargetType()
            pb_resp = cloud_deploy.CustomTargetType.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_custom_target_type(resp)
            return resp

    class _GetDeliveryPipeline(CloudDeployRestStub):
        def __hash__(self):
            return hash("GetDeliveryPipeline")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.GetDeliveryPipelineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.DeliveryPipeline:
            r"""Call the get delivery pipeline method over HTTP.

            Args:
                request (~.cloud_deploy.GetDeliveryPipelineRequest):
                    The request object. The request object for ``GetDeliveryPipeline``
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.DeliveryPipeline:
                    A ``DeliveryPipeline`` resource in the Cloud Deploy API.

                A ``DeliveryPipeline`` defines a pipeline through which
                a Skaffold configuration can progress.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_delivery_pipeline(
                request, metadata
            )
            pb_request = cloud_deploy.GetDeliveryPipelineRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.DeliveryPipeline()
            pb_resp = cloud_deploy.DeliveryPipeline.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_delivery_pipeline(resp)
            return resp

    class _GetJobRun(CloudDeployRestStub):
        def __hash__(self):
            return hash("GetJobRun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.GetJobRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.JobRun:
            r"""Call the get job run method over HTTP.

            Args:
                request (~.cloud_deploy.GetJobRunRequest):
                    The request object. GetJobRunRequest is the request object used by
                ``GetJobRun``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.JobRun:
                    A ``JobRun`` resource in the Cloud Deploy API.

                A ``JobRun`` contains information of a single
                ``Rollout`` job evaluation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/releases/*/rollouts/*/jobRuns/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_job_run(request, metadata)
            pb_request = cloud_deploy.GetJobRunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.JobRun()
            pb_resp = cloud_deploy.JobRun.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_job_run(resp)
            return resp

    class _GetRelease(CloudDeployRestStub):
        def __hash__(self):
            return hash("GetRelease")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.GetReleaseRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.Release:
            r"""Call the get release method over HTTP.

            Args:
                request (~.cloud_deploy.GetReleaseRequest):
                    The request object. The request object for ``GetRelease``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.Release:
                    A ``Release`` resource in the Cloud Deploy API.

                A ``Release`` defines a specific Skaffold configuration
                instance that can be deployed.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/releases/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_release(request, metadata)
            pb_request = cloud_deploy.GetReleaseRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.Release()
            pb_resp = cloud_deploy.Release.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_release(resp)
            return resp

    class _GetRollout(CloudDeployRestStub):
        def __hash__(self):
            return hash("GetRollout")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.GetRolloutRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.Rollout:
            r"""Call the get rollout method over HTTP.

            Args:
                request (~.cloud_deploy.GetRolloutRequest):
                    The request object. GetRolloutRequest is the request object used by
                ``GetRollout``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.Rollout:
                    A ``Rollout`` resource in the Cloud Deploy API.

                A ``Rollout`` contains information around a specific
                deployment to a ``Target``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/releases/*/rollouts/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_rollout(request, metadata)
            pb_request = cloud_deploy.GetRolloutRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.Rollout()
            pb_resp = cloud_deploy.Rollout.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_rollout(resp)
            return resp

    class _GetTarget(CloudDeployRestStub):
        def __hash__(self):
            return hash("GetTarget")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.GetTargetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.Target:
            r"""Call the get target method over HTTP.

            Args:
                request (~.cloud_deploy.GetTargetRequest):
                    The request object. The request object for ``GetTarget``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.Target:
                    A ``Target`` resource in the Cloud Deploy API.

                A ``Target`` defines a location to which a Skaffold
                configuration can be deployed.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/targets/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_target(request, metadata)
            pb_request = cloud_deploy.GetTargetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.Target()
            pb_resp = cloud_deploy.Target.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_target(resp)
            return resp

    class _IgnoreJob(CloudDeployRestStub):
        def __hash__(self):
            return hash("IgnoreJob")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.IgnoreJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.IgnoreJobResponse:
            r"""Call the ignore job method over HTTP.

            Args:
                request (~.cloud_deploy.IgnoreJobRequest):
                    The request object. The request object used by ``IgnoreJob``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.IgnoreJobResponse:
                    The response object from ``IgnoreJob``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{rollout=projects/*/locations/*/deliveryPipelines/*/releases/*/rollouts/*}:ignoreJob",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_ignore_job(request, metadata)
            pb_request = cloud_deploy.IgnoreJobRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.IgnoreJobResponse()
            pb_resp = cloud_deploy.IgnoreJobResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_ignore_job(resp)
            return resp

    class _ListAutomationRuns(CloudDeployRestStub):
        def __hash__(self):
            return hash("ListAutomationRuns")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.ListAutomationRunsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.ListAutomationRunsResponse:
            r"""Call the list automation runs method over HTTP.

            Args:
                request (~.cloud_deploy.ListAutomationRunsRequest):
                    The request object. The request object for ``ListAutomationRuns``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.ListAutomationRunsResponse:
                    The response object from ``ListAutomationRuns``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/deliveryPipelines/*}/automationRuns",
                },
            ]
            request, metadata = self._interceptor.pre_list_automation_runs(
                request, metadata
            )
            pb_request = cloud_deploy.ListAutomationRunsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.ListAutomationRunsResponse()
            pb_resp = cloud_deploy.ListAutomationRunsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_automation_runs(resp)
            return resp

    class _ListAutomations(CloudDeployRestStub):
        def __hash__(self):
            return hash("ListAutomations")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.ListAutomationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.ListAutomationsResponse:
            r"""Call the list automations method over HTTP.

            Args:
                request (~.cloud_deploy.ListAutomationsRequest):
                    The request object. The request object for ``ListAutomations``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.ListAutomationsResponse:
                    The response object from ``ListAutomations``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/deliveryPipelines/*}/automations",
                },
            ]
            request, metadata = self._interceptor.pre_list_automations(
                request, metadata
            )
            pb_request = cloud_deploy.ListAutomationsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.ListAutomationsResponse()
            pb_resp = cloud_deploy.ListAutomationsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_automations(resp)
            return resp

    class _ListCustomTargetTypes(CloudDeployRestStub):
        def __hash__(self):
            return hash("ListCustomTargetTypes")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.ListCustomTargetTypesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.ListCustomTargetTypesResponse:
            r"""Call the list custom target types method over HTTP.

            Args:
                request (~.cloud_deploy.ListCustomTargetTypesRequest):
                    The request object. The request object for ``ListCustomTargetTypes``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.ListCustomTargetTypesResponse:
                    The response object from ``ListCustomTargetTypes.``
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/customTargetTypes",
                },
            ]
            request, metadata = self._interceptor.pre_list_custom_target_types(
                request, metadata
            )
            pb_request = cloud_deploy.ListCustomTargetTypesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.ListCustomTargetTypesResponse()
            pb_resp = cloud_deploy.ListCustomTargetTypesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_custom_target_types(resp)
            return resp

    class _ListDeliveryPipelines(CloudDeployRestStub):
        def __hash__(self):
            return hash("ListDeliveryPipelines")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.ListDeliveryPipelinesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.ListDeliveryPipelinesResponse:
            r"""Call the list delivery pipelines method over HTTP.

            Args:
                request (~.cloud_deploy.ListDeliveryPipelinesRequest):
                    The request object. The request object for ``ListDeliveryPipelines``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.ListDeliveryPipelinesResponse:
                    The response object from ``ListDeliveryPipelines``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/deliveryPipelines",
                },
            ]
            request, metadata = self._interceptor.pre_list_delivery_pipelines(
                request, metadata
            )
            pb_request = cloud_deploy.ListDeliveryPipelinesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.ListDeliveryPipelinesResponse()
            pb_resp = cloud_deploy.ListDeliveryPipelinesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_delivery_pipelines(resp)
            return resp

    class _ListJobRuns(CloudDeployRestStub):
        def __hash__(self):
            return hash("ListJobRuns")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.ListJobRunsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.ListJobRunsResponse:
            r"""Call the list job runs method over HTTP.

            Args:
                request (~.cloud_deploy.ListJobRunsRequest):
                    The request object. ListJobRunsRequest is the request object used by
                ``ListJobRuns``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.ListJobRunsResponse:
                    ListJobRunsResponse is the response object returned by
                ``ListJobRuns``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/deliveryPipelines/*/releases/*/rollouts/*}/jobRuns",
                },
            ]
            request, metadata = self._interceptor.pre_list_job_runs(request, metadata)
            pb_request = cloud_deploy.ListJobRunsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.ListJobRunsResponse()
            pb_resp = cloud_deploy.ListJobRunsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_job_runs(resp)
            return resp

    class _ListReleases(CloudDeployRestStub):
        def __hash__(self):
            return hash("ListReleases")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.ListReleasesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.ListReleasesResponse:
            r"""Call the list releases method over HTTP.

            Args:
                request (~.cloud_deploy.ListReleasesRequest):
                    The request object. The request object for ``ListReleases``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.ListReleasesResponse:
                    The response object from ``ListReleases``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/deliveryPipelines/*}/releases",
                },
            ]
            request, metadata = self._interceptor.pre_list_releases(request, metadata)
            pb_request = cloud_deploy.ListReleasesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.ListReleasesResponse()
            pb_resp = cloud_deploy.ListReleasesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_releases(resp)
            return resp

    class _ListRollouts(CloudDeployRestStub):
        def __hash__(self):
            return hash("ListRollouts")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.ListRolloutsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.ListRolloutsResponse:
            r"""Call the list rollouts method over HTTP.

            Args:
                request (~.cloud_deploy.ListRolloutsRequest):
                    The request object. ListRolloutsRequest is the request object used by
                ``ListRollouts``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.ListRolloutsResponse:
                    ListRolloutsResponse is the response object reutrned by
                ``ListRollouts``.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/deliveryPipelines/*/releases/*}/rollouts",
                },
            ]
            request, metadata = self._interceptor.pre_list_rollouts(request, metadata)
            pb_request = cloud_deploy.ListRolloutsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.ListRolloutsResponse()
            pb_resp = cloud_deploy.ListRolloutsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_rollouts(resp)
            return resp

    class _ListTargets(CloudDeployRestStub):
        def __hash__(self):
            return hash("ListTargets")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.ListTargetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.ListTargetsResponse:
            r"""Call the list targets method over HTTP.

            Args:
                request (~.cloud_deploy.ListTargetsRequest):
                    The request object. The request object for ``ListTargets``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.ListTargetsResponse:
                    The response object from ``ListTargets``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/targets",
                },
            ]
            request, metadata = self._interceptor.pre_list_targets(request, metadata)
            pb_request = cloud_deploy.ListTargetsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.ListTargetsResponse()
            pb_resp = cloud_deploy.ListTargetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_targets(resp)
            return resp

    class _RetryJob(CloudDeployRestStub):
        def __hash__(self):
            return hash("RetryJob")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.RetryJobRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.RetryJobResponse:
            r"""Call the retry job method over HTTP.

            Args:
                request (~.cloud_deploy.RetryJobRequest):
                    The request object. RetryJobRequest is the request object used by
                ``RetryJob``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.RetryJobResponse:
                    The response object from 'RetryJob'.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{rollout=projects/*/locations/*/deliveryPipelines/*/releases/*/rollouts/*}:retryJob",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_retry_job(request, metadata)
            pb_request = cloud_deploy.RetryJobRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.RetryJobResponse()
            pb_resp = cloud_deploy.RetryJobResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_retry_job(resp)
            return resp

    class _RollbackTarget(CloudDeployRestStub):
        def __hash__(self):
            return hash("RollbackTarget")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.RollbackTargetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.RollbackTargetResponse:
            r"""Call the rollback target method over HTTP.

            Args:
                request (~.cloud_deploy.RollbackTargetRequest):
                    The request object. The request object for ``RollbackTarget``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.RollbackTargetResponse:
                    The response object from ``RollbackTarget``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*}:rollbackTarget",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_rollback_target(request, metadata)
            pb_request = cloud_deploy.RollbackTargetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.RollbackTargetResponse()
            pb_resp = cloud_deploy.RollbackTargetResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_rollback_target(resp)
            return resp

    class _TerminateJobRun(CloudDeployRestStub):
        def __hash__(self):
            return hash("TerminateJobRun")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.TerminateJobRunRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> cloud_deploy.TerminateJobRunResponse:
            r"""Call the terminate job run method over HTTP.

            Args:
                request (~.cloud_deploy.TerminateJobRunRequest):
                    The request object. The request object used by ``TerminateJobRun``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.cloud_deploy.TerminateJobRunResponse:
                    The response object from ``TerminateJobRun``.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/deliveryPipelines/*/releases/*/rollouts/*/jobRuns/*}:terminate",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_terminate_job_run(
                request, metadata
            )
            pb_request = cloud_deploy.TerminateJobRunRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = cloud_deploy.TerminateJobRunResponse()
            pb_resp = cloud_deploy.TerminateJobRunResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_terminate_job_run(resp)
            return resp

    class _UpdateAutomation(CloudDeployRestStub):
        def __hash__(self):
            return hash("UpdateAutomation")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.UpdateAutomationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update automation method over HTTP.

            Args:
                request (~.cloud_deploy.UpdateAutomationRequest):
                    The request object. The request object for ``UpdateAutomation``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{automation.name=projects/*/locations/*/deliveryPipelines/*/automations/*}",
                    "body": "automation",
                },
            ]
            request, metadata = self._interceptor.pre_update_automation(
                request, metadata
            )
            pb_request = cloud_deploy.UpdateAutomationRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_automation(resp)
            return resp

    class _UpdateCustomTargetType(CloudDeployRestStub):
        def __hash__(self):
            return hash("UpdateCustomTargetType")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.UpdateCustomTargetTypeRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update custom target type method over HTTP.

            Args:
                request (~.cloud_deploy.UpdateCustomTargetTypeRequest):
                    The request object. The request object for ``UpdateCustomTargetType``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{custom_target_type.name=projects/*/locations/*/customTargetTypes/*}",
                    "body": "custom_target_type",
                },
            ]
            request, metadata = self._interceptor.pre_update_custom_target_type(
                request, metadata
            )
            pb_request = cloud_deploy.UpdateCustomTargetTypeRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_custom_target_type(resp)
            return resp

    class _UpdateDeliveryPipeline(CloudDeployRestStub):
        def __hash__(self):
            return hash("UpdateDeliveryPipeline")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.UpdateDeliveryPipelineRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update delivery pipeline method over HTTP.

            Args:
                request (~.cloud_deploy.UpdateDeliveryPipelineRequest):
                    The request object. The request object for ``UpdateDeliveryPipeline``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{delivery_pipeline.name=projects/*/locations/*/deliveryPipelines/*}",
                    "body": "delivery_pipeline",
                },
            ]
            request, metadata = self._interceptor.pre_update_delivery_pipeline(
                request, metadata
            )
            pb_request = cloud_deploy.UpdateDeliveryPipelineRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_delivery_pipeline(resp)
            return resp

    class _UpdateTarget(CloudDeployRestStub):
        def __hash__(self):
            return hash("UpdateTarget")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: cloud_deploy.UpdateTargetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update target method over HTTP.

            Args:
                request (~.cloud_deploy.UpdateTargetRequest):
                    The request object. The request object for ``UpdateTarget``.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{target.name=projects/*/locations/*/targets/*}",
                    "body": "target",
                },
            ]
            request, metadata = self._interceptor.pre_update_target(request, metadata)
            pb_request = cloud_deploy.UpdateTargetRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_target(resp)
            return resp

    @property
    def abandon_release(
        self,
    ) -> Callable[
        [cloud_deploy.AbandonReleaseRequest], cloud_deploy.AbandonReleaseResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AbandonRelease(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def advance_rollout(
        self,
    ) -> Callable[
        [cloud_deploy.AdvanceRolloutRequest], cloud_deploy.AdvanceRolloutResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._AdvanceRollout(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def approve_rollout(
        self,
    ) -> Callable[
        [cloud_deploy.ApproveRolloutRequest], cloud_deploy.ApproveRolloutResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ApproveRollout(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_automation_run(
        self,
    ) -> Callable[
        [cloud_deploy.CancelAutomationRunRequest],
        cloud_deploy.CancelAutomationRunResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelAutomationRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_rollout(
        self,
    ) -> Callable[
        [cloud_deploy.CancelRolloutRequest], cloud_deploy.CancelRolloutResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CancelRollout(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_automation(
        self,
    ) -> Callable[[cloud_deploy.CreateAutomationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAutomation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_custom_target_type(
        self,
    ) -> Callable[
        [cloud_deploy.CreateCustomTargetTypeRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCustomTargetType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_delivery_pipeline(
        self,
    ) -> Callable[
        [cloud_deploy.CreateDeliveryPipelineRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateDeliveryPipeline(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_release(
        self,
    ) -> Callable[[cloud_deploy.CreateReleaseRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRelease(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_rollout(
        self,
    ) -> Callable[[cloud_deploy.CreateRolloutRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRollout(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_target(
        self,
    ) -> Callable[[cloud_deploy.CreateTargetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTarget(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_automation(
        self,
    ) -> Callable[[cloud_deploy.DeleteAutomationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAutomation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_custom_target_type(
        self,
    ) -> Callable[
        [cloud_deploy.DeleteCustomTargetTypeRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCustomTargetType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_delivery_pipeline(
        self,
    ) -> Callable[
        [cloud_deploy.DeleteDeliveryPipelineRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteDeliveryPipeline(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_target(
        self,
    ) -> Callable[[cloud_deploy.DeleteTargetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTarget(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_automation(
        self,
    ) -> Callable[[cloud_deploy.GetAutomationRequest], cloud_deploy.Automation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAutomation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_automation_run(
        self,
    ) -> Callable[[cloud_deploy.GetAutomationRunRequest], cloud_deploy.AutomationRun]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAutomationRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_config(
        self,
    ) -> Callable[[cloud_deploy.GetConfigRequest], cloud_deploy.Config]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_custom_target_type(
        self,
    ) -> Callable[
        [cloud_deploy.GetCustomTargetTypeRequest], cloud_deploy.CustomTargetType
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCustomTargetType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_delivery_pipeline(
        self,
    ) -> Callable[
        [cloud_deploy.GetDeliveryPipelineRequest], cloud_deploy.DeliveryPipeline
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetDeliveryPipeline(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_job_run(
        self,
    ) -> Callable[[cloud_deploy.GetJobRunRequest], cloud_deploy.JobRun]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetJobRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_release(
        self,
    ) -> Callable[[cloud_deploy.GetReleaseRequest], cloud_deploy.Release]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRelease(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_rollout(
        self,
    ) -> Callable[[cloud_deploy.GetRolloutRequest], cloud_deploy.Rollout]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRollout(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_target(
        self,
    ) -> Callable[[cloud_deploy.GetTargetRequest], cloud_deploy.Target]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTarget(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def ignore_job(
        self,
    ) -> Callable[[cloud_deploy.IgnoreJobRequest], cloud_deploy.IgnoreJobResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._IgnoreJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_automation_runs(
        self,
    ) -> Callable[
        [cloud_deploy.ListAutomationRunsRequest],
        cloud_deploy.ListAutomationRunsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutomationRuns(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_automations(
        self,
    ) -> Callable[
        [cloud_deploy.ListAutomationsRequest], cloud_deploy.ListAutomationsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAutomations(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_custom_target_types(
        self,
    ) -> Callable[
        [cloud_deploy.ListCustomTargetTypesRequest],
        cloud_deploy.ListCustomTargetTypesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListCustomTargetTypes(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_delivery_pipelines(
        self,
    ) -> Callable[
        [cloud_deploy.ListDeliveryPipelinesRequest],
        cloud_deploy.ListDeliveryPipelinesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListDeliveryPipelines(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_job_runs(
        self,
    ) -> Callable[[cloud_deploy.ListJobRunsRequest], cloud_deploy.ListJobRunsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListJobRuns(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_releases(
        self,
    ) -> Callable[
        [cloud_deploy.ListReleasesRequest], cloud_deploy.ListReleasesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListReleases(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_rollouts(
        self,
    ) -> Callable[
        [cloud_deploy.ListRolloutsRequest], cloud_deploy.ListRolloutsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRollouts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_targets(
        self,
    ) -> Callable[[cloud_deploy.ListTargetsRequest], cloud_deploy.ListTargetsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTargets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def retry_job(
        self,
    ) -> Callable[[cloud_deploy.RetryJobRequest], cloud_deploy.RetryJobResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RetryJob(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def rollback_target(
        self,
    ) -> Callable[
        [cloud_deploy.RollbackTargetRequest], cloud_deploy.RollbackTargetResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RollbackTarget(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def terminate_job_run(
        self,
    ) -> Callable[
        [cloud_deploy.TerminateJobRunRequest], cloud_deploy.TerminateJobRunResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._TerminateJobRun(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_automation(
        self,
    ) -> Callable[[cloud_deploy.UpdateAutomationRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateAutomation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_custom_target_type(
        self,
    ) -> Callable[
        [cloud_deploy.UpdateCustomTargetTypeRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCustomTargetType(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_delivery_pipeline(
        self,
    ) -> Callable[
        [cloud_deploy.UpdateDeliveryPipelineRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateDeliveryPipeline(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_target(
        self,
    ) -> Callable[[cloud_deploy.UpdateTargetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTarget(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(CloudDeployRestStub):
        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(CloudDeployRestStub):
        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(CloudDeployRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/deliveryPipelines/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/targets/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1/{resource=projects/*/locations/*/customTargetTypes/*}:getIamPolicy",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(CloudDeployRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/deliveryPipelines/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/targets/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/customTargetTypes/*}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(CloudDeployRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/deliveryPipelines/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1/{resource=projects/*/locations/*/targets/*}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(CloudDeployRestStub):
        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(CloudDeployRestStub):
        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(CloudDeployRestStub):
        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(CloudDeployRestStub):
        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("CloudDeployRestTransport",)
