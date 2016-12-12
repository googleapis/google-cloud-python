# Copyright 2016 Google Inc.
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


class TestPartOfSpeech(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.language.syntax import PartOfSpeech
        return PartOfSpeech

    def test_reverse(self):
        klass = self._get_target_class()
        for attr in dir(klass):
            if attr.startswith('_'):
                continue
            if attr.islower():
                continue
            value = getattr(klass, attr)
            result = klass.reverse(value)
            self.assertEqual(result, attr)


class TestToken(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.language.syntax import Token
        return Token

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        from google.cloud.language.syntax import PartOfSpeech

        text_content = 'All'
        text_begin = -1
        part_of_speech = PartOfSpeech.DETERMINER
        edge_index = 3
        edge_label = 'PREDET'
        lemma = text_content
        token = self._make_one(text_content, text_begin, part_of_speech,
                               edge_index, edge_label, lemma)
        self.assertEqual(token.text_content, text_content)
        self.assertEqual(token.text_begin, text_begin)
        self.assertEqual(token.part_of_speech, part_of_speech)
        self.assertEqual(token.edge_index, edge_index)
        self.assertEqual(token.edge_label, edge_label)
        self.assertEqual(token.lemma, lemma)

    def test_from_api_repr(self):
        from google.cloud.language.syntax import PartOfSpeech

        klass = self._get_target_class()
        text_content = 'pretty'
        text_begin = -1
        part_of_speech = PartOfSpeech.ADJECTIVE
        edge_index = 3
        edge_label = 'AMOD'
        lemma = text_content
        payload = {
            'text': {
                'content': text_content,
                'beginOffset': text_begin,
            },
            'partOfSpeech': {
                'tag': part_of_speech,
            },
            'dependencyEdge': {
                'headTokenIndex': edge_index,
                'label': edge_label,
            },
            'lemma': lemma,
        }
        token = klass.from_api_repr(payload)
        self.assertEqual(token.text_content, text_content)
        self.assertEqual(token.text_begin, text_begin)
        self.assertEqual(token.part_of_speech, part_of_speech)
        self.assertEqual(token.edge_index, edge_index)
        self.assertEqual(token.edge_label, edge_label)
        self.assertEqual(token.lemma, lemma)


class TestSentence(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.language.syntax import Sentence
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
        self.assertEqual(sentence.sentiment, None)

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
