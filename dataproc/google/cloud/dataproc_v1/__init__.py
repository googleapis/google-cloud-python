# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from google.cloud.dataproc_v1 import types
from google.cloud.dataproc_v1.gapic import cluster_controller_client
from google.cloud.dataproc_v1.gapic import enums
from google.cloud.dataproc_v1.gapic import job_controller_client
from google.cloud.dataproc_v1.gapic import workflow_template_service_client


class ClusterControllerClient(cluster_controller_client.ClusterControllerClient):
    __doc__ = cluster_controller_client.ClusterControllerClient.__doc__
    enums = enums


class JobControllerClient(job_controller_client.JobControllerClient):
    __doc__ = job_controller_client.JobControllerClient.__doc__
    enums = enums


class WorkflowTemplateServiceClient(
    workflow_template_service_client.WorkflowTemplateServiceClient
):
    __doc__ = workflow_template_service_client.WorkflowTemplateServiceClient.__doc__
    enums = enums


__all__ = (
    "enums",
    "types",
    "ClusterControllerClient",
    "JobControllerClient",
    "WorkflowTemplateServiceClient",
)
