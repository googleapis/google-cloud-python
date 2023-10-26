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

"""BigQuery DataFrame clients to interact with other cloud resources"""

from __future__ import annotations

import logging
import time
from typing import cast, Optional

import google.api_core.exceptions
from google.cloud import bigquery_connection_v1, resourcemanager_v3
from google.iam.v1 import iam_policy_pb2, policy_pb2

logger = logging.getLogger(__name__)


class BqConnectionManager:
    """Manager to handle operations with BQ connections."""

    # Wait time (in seconds) for an IAM binding to take effect after creation
    _IAM_WAIT_SECONDS = 120

    def __init__(
        self,
        bq_connection_client: bigquery_connection_v1.ConnectionServiceClient,
        cloud_resource_manager_client: resourcemanager_v3.ProjectsClient,
    ):
        self._bq_connection_client = bq_connection_client
        self._cloud_resource_manager_client = cloud_resource_manager_client

    @classmethod
    def resolve_full_connection_name(
        cls, connection_name: str, default_project: str, default_location: str
    ) -> str:
        """Retrieve the full connection name of the form <PROJECT_NUMBER/PROJECT_ID>.<LOCATION>.<CONNECTION_ID>.
        Use default project, location or connection_id when any of them are missing."""
        if connection_name.count(".") == 2:
            return connection_name

        if connection_name.count(".") == 1:
            return f"{default_project}.{connection_name}"

        if connection_name.count(".") == 0:
            return f"{default_project}.{default_location}.{connection_name}"

        raise ValueError(f"Invalid connection name format: {connection_name}.")

    def create_bq_connection(
        self, project_id: str, location: str, connection_id: str, iam_role: str
    ):
        """Create the BQ connection if not exist. In addition, try to add the IAM role to the connection to ensure required permissions.

        Args:
            project_id:
                ID of the project.
            location:
                Location of the connection.
            connection_id:
                ID of the connection.
            iam_role:
                str of the IAM role that the service account of the created connection needs to aquire. E.g. 'run.invoker', 'aiplatform.user'
        """
        # TODO(shobs): The below command to enable BigQuery Connection API needs
        # to be automated. Disabling for now since most target users would not
        # have the privilege to enable API in a project.
        # log("Making sure BigQuery Connection API is enabled")
        # if os.system("gcloud services enable bigqueryconnection.googleapis.com"):
        #    raise ValueError("Failed to enable BigQuery Connection API")
        # If the intended connection does not exist then create it
        service_account_id = self._get_service_account_if_connection_exists(
            project_id, location, connection_id
        )
        if service_account_id:
            logger.info(
                f"Connector {project_id}.{location}.{connection_id} already exists"
            )
        else:
            connection_name, service_account_id = self._create_bq_connection(
                project_id, location, connection_id
            )
            logger.info(
                f"Created BQ connection {connection_name} with service account id: {service_account_id}"
            )
        service_account_id = cast(str, service_account_id)
        # Ensure IAM role on the BQ connection
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#grant_permission_on_function
        self._ensure_iam_binding(project_id, service_account_id, iam_role)

    # Introduce retries to accommodate transient errors like etag mismatch,
    # which can be caused by concurrent operation on the same resource, and
    # manifests with message like:
    # google.api_core.exceptions.Aborted: 409 There were concurrent policy
    # changes. Please retry the whole read-modify-write with exponential
    # backoff. The request's ETag '\007\006\003,\264\304\337\272' did not match
    # the current policy's ETag '\007\006\003,\3750&\363'.
    @google.api_core.retry.Retry(
        predicate=google.api_core.retry.if_exception_type(
            google.api_core.exceptions.Aborted
        ),
        initial=10,
        maximum=20,
        multiplier=2,
        timeout=60,
    )
    def _ensure_iam_binding(
        self, project_id: str, service_account_id: str, iam_role: str
    ):
        """Ensure necessary IAM role is configured on a service account."""
        project = f"projects/{project_id}"
        service_account = f"serviceAccount:{service_account_id}"
        role = f"roles/{iam_role}"
        request = iam_policy_pb2.GetIamPolicyRequest(resource=project)
        policy = self._cloud_resource_manager_client.get_iam_policy(request=request)

        # Check if the binding already exists, and if does, do nothing more
        for binding in policy.bindings:
            if binding.role == role:
                if service_account in binding.members:
                    return

        # Create a new binding
        new_binding = policy_pb2.Binding(role=role, members=[service_account])
        policy.bindings.append(new_binding)
        request = iam_policy_pb2.SetIamPolicyRequest(resource=project, policy=policy)
        self._cloud_resource_manager_client.set_iam_policy(request=request)

        # We would wait for the IAM policy change to take effect
        # https://cloud.google.com/iam/docs/access-change-propagation
        logger.info(
            f"Waiting {self._IAM_WAIT_SECONDS} seconds for IAM to take effect.."
        )
        time.sleep(self._IAM_WAIT_SECONDS)

    def _create_bq_connection(self, project_id: str, location: str, connection_id: str):
        """Create the BigQuery Connection and returns corresponding service account id."""
        client = self._bq_connection_client
        connection = bigquery_connection_v1.Connection(
            cloud_resource=bigquery_connection_v1.CloudResourceProperties()
        )
        request = bigquery_connection_v1.CreateConnectionRequest(
            parent=client.common_location_path(project_id, location),
            connection_id=connection_id,
            connection=connection,
        )
        connection = client.create_connection(request)
        return connection.name, connection.cloud_resource.service_account_id

    def _get_service_account_if_connection_exists(
        self, project_id: str, location: str, connection_id: str
    ) -> Optional[str]:
        """Check if the BigQuery Connection exists."""
        client = self._bq_connection_client
        request = bigquery_connection_v1.GetConnectionRequest(
            name=client.connection_path(project_id, location, connection_id)
        )

        service_account = None
        try:
            service_account = client.get_connection(
                request=request
            ).cloud_resource.service_account_id
        except google.api_core.exceptions.NotFound:
            pass

        return service_account
