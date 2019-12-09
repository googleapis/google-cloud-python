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

# DO NOT EDIT! This is a generated sample ("Request",  "samplegen_resource_path")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-vision

# sample-metadata
#   title: Create product set (demonstrate resource paths)
#   description: Create product set (demonstrate resource paths)
#   usage: python3 samples/v1/samplegen_resource_path.py [--project "[PROJECT ID]"]

# [START samplegen_resource_path]
from google.cloud import vision_v1


def sample_create_product_set(project):
    """
    Create product set (demonstrate resource paths)

    Args:
      project The Google Cloud Project for creating this product set
    """

    client = vision_v1.ProductSearchClient()

    # project = '[PROJECT ID]'
    parent = client.location_path(project, "us-central1")
    display_name = "[DISPLAY NAME]"
    product_set = {"display_name": display_name}

    response = client.create_product_set(parent, product_set)
    # The API response represents the created product set
    product_set = response
    print(u"The full name of the created product set: {}".format(product_set.name))


# [END samplegen_resource_path]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="[PROJECT ID]")
    args = parser.parse_args()

    sample_create_product_set(args.project)


if __name__ == "__main__":
    main()
