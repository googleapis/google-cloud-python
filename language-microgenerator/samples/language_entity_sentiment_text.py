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


def entity_sentiment_text():

    client = language_v1.LanguageService()

    text = 'President Kennedy spoke at the White House.'

    document = language_v1.Document(type=language_v1.Document.Type.PLAIN_TEXT, content=text)
    request = language_v1.AnalyzeEntitySentimentRequest(
        document=document,
    )

    response = client.analyze_entity_sentiment(request)

    for entity in response.entities:
        print('Mentions: ')
        print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            print(u'  Sentiment : {}'.format(mention.sentiment.score))
            print(u'  Type : {}'.format(mention.type))
        print(u'Salience: {}'.format(entity.salience))
        print(u'Sentiment: {}\n'.format(entity.sentiment))

def main():
    entity_sentiment_text()


if __name__ == "__main__":
    main()
