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
# Generated code. DO NOT EDIT!
#
# Snippet for CreateCloudVmCluster
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-oracledatabase


# [START oracledatabase_v1_generated_OracleDatabase_CreateCloudVmCluster_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import oracledatabase_v1


def sample_create_cloud_vm_cluster():
    # Create a client
    client = oracledatabase_v1.OracleDatabaseClient()

    # Initialize request argument(s)
    cloud_vm_cluster = oracledatabase_v1.CloudVmCluster()
    cloud_vm_cluster.exadata_infrastructure = "exadata_infrastructure_value"
    cloud_vm_cluster.cidr = "cidr_value"
    cloud_vm_cluster.backup_subnet_cidr = "backup_subnet_cidr_value"
    cloud_vm_cluster.network = "network_value"

    request = oracledatabase_v1.CreateCloudVmClusterRequest(
        parent="parent_value",
        cloud_vm_cluster_id="cloud_vm_cluster_id_value",
        cloud_vm_cluster=cloud_vm_cluster,
    )

    # Make the request
    operation = client.create_cloud_vm_cluster(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END oracledatabase_v1_generated_OracleDatabase_CreateCloudVmCluster_sync]
