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

# DO NOT EDIT! This is a generated sample ("Request",  "samplegen_map_field_access")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-language

# sample-metadata
#   title: This sample reads and loops over a map field in the response
#   description: This sample reads and loops over a map field in the response
#   usage: python3 samples/v1/samplegen_map_field_access.py

# [START samplegen_map_field_access]
from google.cloud import language_v1
from google.cloud.language_v1 import enums


def sample_analyze_entities():
    """This sample reads and loops over a map field in the response"""

    client = language_v1.LanguageServiceClient()

    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"

    # The text content to analyze
    content = "Googleplex is at 1600 Amphitheatre Parkway, Mountain View, CA."
    document = {"type": type_, "language": language, "content": content}

    response = client.analyze_entities(document)
    for entity in response.entities:
        # Access value by key:
        print(u"URL: {}".format(entity.metadata["wikipedia_url"]))
        # Loop over keys and values:
        for key, value in entity.metadata.items():
            print(u"{}: {}".format(key, value))

        # Loop over just keys:
        for the_key, _ in entity.metadata.items():
            print(u"Key: {}".format(the_key))

        # Loop over just values:
        for _, the_value in entity.metadata.items():
            print(u"Value: {}".format(the_value))


# [END samplegen_map_field_access]


def main():
    sample_analyze_entities()


if __name__ == "__main__":
    main()
