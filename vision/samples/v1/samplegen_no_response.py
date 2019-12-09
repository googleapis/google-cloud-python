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

# DO NOT EDIT! This is a generated sample ("Request",  "samplegen_no_response")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-vision

# sample-metadata
#   title: Delete Product Set (returns Empty)
#   description: Delete Product Set (returns Empty)
#   usage: python3 samples/v1/samplegen_no_response.py

# [START samplegen_no_response]
from google.cloud import vision_v1


def sample_delete_product_set():
    """Delete Product Set (returns Empty)"""

    client = vision_v1.ProductSearchClient()

    # The full name of the product set to delete
    name = client.product_set_path("[PROJECT]", "[LOCATION]", "[PRODUCT_SET]")

    client.delete_product_set(name)
    # Deleted product set.


# [END samplegen_no_response]


def main():
    sample_delete_product_set()


if __name__ == "__main__":
    main()
