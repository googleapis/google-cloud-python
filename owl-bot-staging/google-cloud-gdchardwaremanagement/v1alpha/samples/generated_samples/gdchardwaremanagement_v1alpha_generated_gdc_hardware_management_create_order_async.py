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
# Snippet for CreateOrder
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-gdchardwaremanagement


# [START gdchardwaremanagement_v1alpha_generated_GDCHardwareManagement_CreateOrder_async]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import gdchardwaremanagement_v1alpha


async def sample_create_order():
    # Create a client
    client = gdchardwaremanagement_v1alpha.GDCHardwareManagementAsyncClient()

    # Initialize request argument(s)
    order = gdchardwaremanagement_v1alpha.Order()
    order.organization_contact.contacts.given_name = "given_name_value"
    order.organization_contact.contacts.email = "email_value"
    order.organization_contact.contacts.phone = "phone_value"
    order.customer_motivation = "customer_motivation_value"
    order.region_code = "region_code_value"
    order.billing_id = "billing_id_value"

    request = gdchardwaremanagement_v1alpha.CreateOrderRequest(
        parent="parent_value",
        order=order,
    )

    # Make the request
    operation = client.create_order(request=request)

    print("Waiting for operation to complete...")

    response = (await operation).result()

    # Handle the response
    print(response)

# [END gdchardwaremanagement_v1alpha_generated_GDCHardwareManagement_CreateOrder_async]
