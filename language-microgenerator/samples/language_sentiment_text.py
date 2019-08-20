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

def sample_analyze_sentiment(content):

    client = language_v1.LanguageService()

    # content = "Your text to analyze, e.g. Hello, world!"

    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = language_v1.Document(type=type_, content=content)
    request = language_v1.AnalyzeSentimentRequest(
        document=document, encoding_type=EncodingType.UTF8
    )

    response = client.analyze_sentiment(request)
    sentiment = response.document_sentiment

    print("Score: {}".format(sentiment.score))
    print("Magnitude: {}".format(sentiment.magnitude))


def main():
    sample_analyze_sentiment("Stuff to talk about")


if __name__ == "__main__":
    main()
