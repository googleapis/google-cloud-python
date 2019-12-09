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

# DO NOT EDIT! This is a generated sample ("Request",  "samplegen_no_config")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-vision

# sample-metadata
#   title:
#   usage: python3 samples/v1/samplegen_no_config.py

# [START ]
from google.cloud import vision_v1


def sample_create_product_set():

    client = vision_v1.ProductSearchClient()

    parent = client.location_path("[PROJECT]", "[LOCATION]")
    product_set = {}

    response = client.create_product_set(parent, product_set)
    print(response)


# [END ]


def main():
    sample_create_product_set()


if __name__ == "__main__":
    main()
