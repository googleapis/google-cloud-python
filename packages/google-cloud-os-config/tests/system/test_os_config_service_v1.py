# Copyright 2020 Google LLC
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

import os
import uuid

from google.cloud.osconfig_v1.services.os_config_service import OsConfigServiceClient
from google.cloud.osconfig_v1.types import patch_deployments
from google.cloud.osconfig_v1.types import patch_jobs
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


class TestOsConfigServiceV1(object):
    def test_patch_job(self):
        project_id = os.environ["PROJECT_ID"]
        client = OsConfigServiceClient()

        # ExecutePatchJob
        request = patch_jobs.ExecutePatchJobRequest(
            parent=f"projects/{project_id}",
            description="Python Client Library System Test",
            instance_filter=patch_jobs.PatchInstanceFilter(all_=True),
        )
        patch_job = client.execute_patch_job(request)
        assert patch_job is not None

        # GetPatchJob
        request = patch_jobs.GetPatchJobRequest(name=patch_job.name)
        patch_job = client.get_patch_job(request)
        assert patch_job.description == "Python Client Library System Test"

        # ListPatchJobInstanceDetails
        request = patch_jobs.ListPatchJobInstanceDetailsRequest(parent=patch_job.name)
        response = client.list_patch_job_instance_details(request)
        assert len(response.patch_job_instance_details) >= 0

        # CancelPatchJob
        request = patch_jobs.CancelPatchJobRequest(name=patch_job.name)
        patch_job = client.cancel_patch_job(request)
        assert patch_job.state == patch_jobs.PatchJob.State.CANCELED

        # ListPatchJobs
        request = patch_jobs.ListPatchJobsRequest(parent=f"projects/{project_id}")
        response = client.list_patch_jobs(request)
        assert response.patch_jobs

    def test_patch_deployment(self):
        project_id = os.environ["PROJECT_ID"]
        client = OsConfigServiceClient()

        patch_deployment = patch_deployments.PatchDeployment(
            instance_filter=patch_jobs.PatchInstanceFilter(all_=True),
            one_time_schedule=patch_deployments.OneTimeSchedule(
                execute_time=timestamp.Timestamp(seconds=200000000000)
            ),
        )
        patch_deployment_id = "python-client-library-test-" + str(uuid.uuid1())
        patch_deployment_name = (
            f"projects/{project_id}/patchDeployments/{patch_deployment_id}"
        )

        # CreatePatchDeploymentRequest
        request = patch_deployments.CreatePatchDeploymentRequest(
            parent=f"projects/{project_id}",
            patch_deployment_id=patch_deployment_id,
            patch_deployment=patch_deployment,
        )
        patch_deployment = client.create_patch_deployment(request)
        assert patch_deployment_id in patch_deployment.name

        # GetPatchDeployment
        request = patch_deployments.GetPatchDeploymentRequest(
            name=patch_deployment_name
        )
        patch_deployment = client.get_patch_deployment(request)
        assert patch_deployment_id in patch_deployment.name

        # ListPatchDeployments
        request = patch_deployments.ListPatchDeploymentsRequest(
            parent=f"projects/{project_id}"
        )
        response = client.list_patch_deployments(request)
        assert response.patch_deployments

        # DeletePatchDeployment
        request = patch_deployments.DeletePatchDeploymentRequest(
            name=patch_deployment_name
        )
        client.delete_patch_deployment(request)
