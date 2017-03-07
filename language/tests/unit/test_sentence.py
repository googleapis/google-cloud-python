# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest


class TestSentence(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.language.sentence import Sentence

        return Sentence

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        content = "All the king's horses."
        begin = 11
        sentence = self._make_one(content, begin)
        self.assertEqual(sentence.content, content)
        self.assertEqual(sentence.begin, begin)

    def test_from_api_repr(self):
        klass = self._get_target_class()
        content = 'All the pretty horses.'
        begin = -1
        payload = {
            'text': {
                'content': content,
                'beginOffset': begin,
            },
        }
        sentence = klass.from_api_repr(payload)
        self.assertEqual(sentence.content, content)
        self.assertEqual(sentence.begin, begin)
        self.assertIsNone(sentence.sentiment)

    def test_from_api_repr_with_sentiment(self):
        from google.cloud.language.sentiment import Sentiment

        klass = self._get_target_class()
        content = 'All the pretty horses.'
        begin = -1
        score = 0.5
        magnitude = 0.5
        payload = {
            'text': {
                'content': content,
                'beginOffset': begin,
            },
            'sentiment': {
                'score': score,
                'magnitude': magnitude,
            }
        }
        sentence = klass.from_api_repr(payload)
        self.assertEqual(sentence.content, content)
        self.assertEqual(sentence.begin, begin)
        self.assertIsInstance(sentence.sentiment, Sentiment)
        self.assertEqual(sentence.sentiment.score, score)
        self.assertEqual(sentence.sentiment.magnitude, magnitude)
