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

# DO NOT EDIT! This is a generated sample ("RequestPagedAll",  "samplegen_paged")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-vision

# sample-metadata
#   title: List product sets
#   description: List product sets
#   usage: python3 samples/v1/samplegen_paged.py

# [START samplegen_paged]
from google.cloud import vision_v1


def sample_list_product_sets():
    """List product sets"""

    client = vision_v1.ProductSearchClient()

    # The project and location where the product sets are contained.
    parent = client.location_path("[PROJECT]", "[LOCATION]")

    # Iterate over all results
    for response_item in client.list_product_sets(parent):
        # The entity in this iteration represents a product set
        product_set = response_item
        print(u"The full name of this product set: {}".format(product_set.name))


# [END samplegen_paged]


def main():
    sample_list_product_sets()


if __name__ == "__main__":
    main()
