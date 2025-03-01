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
# Snippet for CreateAzureNodePool
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-gke-multicloud


# [START gkemulticloud_v1_generated_AzureClusters_CreateAzureNodePool_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import gke_multicloud_v1


def sample_create_azure_node_pool():
    # Create a client
    client = gke_multicloud_v1.AzureClustersClient()

    # Initialize request argument(s)
    azure_node_pool = gke_multicloud_v1.AzureNodePool()
    azure_node_pool.version = "version_value"
    azure_node_pool.config.ssh_config.authorized_key = "authorized_key_value"
    azure_node_pool.subnet_id = "subnet_id_value"
    azure_node_pool.autoscaling.min_node_count = 1489
    azure_node_pool.autoscaling.max_node_count = 1491
    azure_node_pool.max_pods_constraint.max_pods_per_node = 1798

    request = gke_multicloud_v1.CreateAzureNodePoolRequest(
        parent="parent_value",
        azure_node_pool=azure_node_pool,
        azure_node_pool_id="azure_node_pool_id_value",
    )

    # Make the request
    operation = client.create_azure_node_pool(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END gkemulticloud_v1_generated_AzureClusters_CreateAzureNodePool_sync]
