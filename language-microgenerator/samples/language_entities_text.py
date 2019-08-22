# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
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

import sys

from google.cloud import language_v1
from google.cloud.language_v1.types.language_service import EncodingType

def entities_text():

    client = language_v1.LanguageService()

    content = "President Kennedy spoke at the White House."

    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = language_v1.Document(type=type_, content=content)
    request = language_v1.AnalyzeEntitiesRequest(
        document=document,
        encoding_type=EncodingType.UTF8
    )

    response = client.analyze_entities(request)
    entities = response.entities

    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity.type.name))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        for metadata_entry in entity.metadata:
            print(metadata_entry)

        # Retrieving metadata entries in current client:
        # print(u'{:<16}: {}'.format('wikipedia_url',
        #       entity.metadata.get('wikipedia_url', '-')))
        # print(u'{:<16}: {}'.format('mid', entity.metadata.get('mid', '-')))


def main():
    entities_text()


if __name__ == "__main__":
    main()
