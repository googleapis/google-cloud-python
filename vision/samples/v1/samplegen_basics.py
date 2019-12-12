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

# DO NOT EDIT! This is a generated sample ("Request",  "samplegen_basics")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-vision

# sample-metadata
#   title: This is the sample title
#   description: This is the sample description
#   usage: python3 samples/v1/samplegen_basics.py [--display_name "This is the default value of the display_name request field"]

# [START samplegen_basics]
from google.cloud import vision_v1


def sample_create_product_set(display_name):
    """
    This is the sample description

    Args:
      display_name Description of the parameter
    """

    client = vision_v1.ProductSearchClient()

    # display_name = 'This is the default value of the display_name request field'

    # The project and location in which the product set should be created.
    parent = client.location_path("[PROJECT]", "[LOCATION]")
    product_set = {"display_name": display_name}

    response = client.create_product_set(parent, product_set)
    # The API response represents the created product set
    product_set = response
    print(u"The full name of the created product set: {}".format(product_set.name))


# [END samplegen_basics]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--display_name",
        type=str,
        default="This is the default value of the display_name request field",
    )
    args = parser.parse_args()

    sample_create_product_set(args.display_name)


if __name__ == "__main__":
    main()
