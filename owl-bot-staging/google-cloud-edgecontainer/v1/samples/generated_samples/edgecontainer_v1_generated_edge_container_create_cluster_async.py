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
# Generated code. DO NOT EDIT!
#
# Snippet for CreateCluster
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-edgecontainer


# [START edgecontainer_v1_generated_EdgeContainer_CreateCluster_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import edgecontainer_v1


async def sample_create_cluster():
    # Create a client
    client = edgecontainer_v1.EdgeContainerAsyncClient()

    # Initialize request argument(s)
    cluster = edgecontainer_v1.Cluster()
    cluster.name = "name_value"
    cluster.fleet.project = "project_value"
    cluster.networking.cluster_ipv4_cidr_blocks = ['cluster_ipv4_cidr_blocks_value1', 'cluster_ipv4_cidr_blocks_value2']
    cluster.networking.services_ipv4_cidr_blocks = ['services_ipv4_cidr_blocks_value1', 'services_ipv4_cidr_blocks_value2']
    cluster.authorization.admin_users.username = "username_value"

    request = edgecontainer_v1.CreateClusterRequest(
        parent="parent_value",
        cluster_id="cluster_id_value",
        cluster=cluster,
    )

    # Make the request
    operation = client.create_cluster(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END edgecontainer_v1_generated_EdgeContainer_CreateCluster_async]
