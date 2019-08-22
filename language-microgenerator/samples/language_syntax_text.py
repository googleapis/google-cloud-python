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


def syntax_text():
    client = language_v1.LanguageService()

    content = "President Kennedy spoke at the White House."

    document = language_v1.Document(
        type=language_v1.Document.Type.PLAIN_TEXT, content=content
    )
    request = language_v1.AnalyzeSyntaxRequest(
        document=document, encoding_type=EncodingType.UTF8
    )

    response = client.analyze_syntax(request)
    tokens = response.tokens

    print("language: {}".format(response.language))

    for token in tokens:
        part_of_speech_tag = language_v1.PartOfSpeech.Tag(token.part_of_speech.tag)
        print(u"{}: {}".format(part_of_speech_tag.name, token.text.content))


def main():
    syntax_text()


if __name__ == "__main__":
    main()
