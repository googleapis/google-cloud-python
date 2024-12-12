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
# Snippet for LabelText
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-datalabeling


# [START datalabeling_v1beta1_generated_DataLabelingService_LabelText_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google.cloud import datalabeling_v1beta1


def sample_label_text():
    # Create a client
    client = datalabeling_v1beta1.DataLabelingServiceClient()

    # Initialize request argument(s)
    text_classification_config = datalabeling_v1beta1.TextClassificationConfig()
    text_classification_config.annotation_spec_set = "annotation_spec_set_value"

    basic_config = datalabeling_v1beta1.HumanAnnotationConfig()
    basic_config.instruction = "instruction_value"
    basic_config.annotated_dataset_display_name = "annotated_dataset_display_name_value"

    request = datalabeling_v1beta1.LabelTextRequest(
        text_classification_config=text_classification_config,
        parent="parent_value",
        basic_config=basic_config,
        feature="TEXT_ENTITY_EXTRACTION",
    )

    # Make the request
    operation = client.label_text(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)

# [END datalabeling_v1beta1_generated_DataLabelingService_LabelText_sync]
