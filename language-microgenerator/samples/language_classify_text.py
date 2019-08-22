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

    text = 'Android is a mobile operating system developed by Google, ' \
           'based on the Linux kernel and designed primarily for ' \
           'touchscreen mobile devices such as smartphones and tablets.'


    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = language_v1.Document(type=type_, content=text)
    request = language_v1.ClassifyTextRequest(
        document=document
    )

    response = client.classify_text(request)
    categories = response.categories

    for category in categories:
        print(u'=' * 20)
        print(u'{:<16}: {}'.format('name', category.name))
        print(u'{:<16}: {}'.format('confidence', category.confidence))

def main():
    entities_text()


if __name__ == "__main__":
    main()
