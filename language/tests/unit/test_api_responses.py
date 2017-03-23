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

from copy import copy
import unittest


class TestEntityResponse(unittest.TestCase):
    ENTITY_DICT = {
        'mentions': [{
            'text': {'content': 'Italian', 'beginOffset': 0},
            'type': 'PROPER',
        }],
        'metadata': {'wikipedia_url': 'http://en.wikipedia.org/wiki/Italy'},
        'name': 'Italian',
        'salience': 0.15,
        'type': 'LOCATION',
    }

    def test_constructor(self):
        from google.cloud.language.api_responses import EntityResponse
        from google.cloud.language.entity import Entity

        entity_response = EntityResponse(
            entities=[Entity.from_api_repr(self.ENTITY_DICT)],
            language='en',
        )
        self._verify_entity_response(entity_response)

    def test_api_repr_factory(self):
        from google.cloud.language.api_responses import EntityResponse

        entity_response = EntityResponse.from_api_repr({
            'entities': [self.ENTITY_DICT],
            'language': 'en',
        })
        self._verify_entity_response(entity_response)

    def _verify_entity_response(self, entity_response):
        from google.cloud.language.entity import EntityType
        from google.cloud.language.entity import Mention

        self.assertEqual(len(entity_response.entities), 1)
        entity = entity_response.entities[0]
        self.assertEqual(entity.name, 'Italian')
        self.assertEqual(len(entity.mentions), 1)
        self.assertIsInstance(entity.mentions[0], Mention)
        self.assertEqual(str(entity.mentions[0]), 'Italian')
        self.assertTrue(entity.metadata['wikipedia_url'].endswith('Italy'))
        self.assertAlmostEqual(entity.salience, 0.15)
        self.assertEqual(entity.entity_type, EntityType.LOCATION)
        self.assertEqual(entity_response.language, 'en')


class TestSentimentResponse(unittest.TestCase):
    SENTIMENT_DICT = {
        'score': 0.4,
        'magnitude': 3.14159,
    }
    SENTENCE_DICT = {
        'text': {
            'beginOffset': 0,
            'content': 'It is hailing in Wales.',
        },
        'sentiment': SENTIMENT_DICT,
    }

    def test_constructor(self):
        from google.cloud.language.api_responses import SentimentResponse
        from google.cloud.language.sentence import Sentence
        from google.cloud.language.sentiment import Sentiment

        sentiment_response = SentimentResponse(
            language='en',
            sentences=[Sentence.from_api_repr(self.SENTENCE_DICT)],
            sentiment=Sentiment.from_api_repr(self.SENTIMENT_DICT),
        )

        self._verify_sentiment_response(sentiment_response)

    def test_api_repr_factory(self):
        from google.cloud.language.api_responses import SentimentResponse

        sentiment_response = SentimentResponse.from_api_repr({
            'documentSentiment': self.SENTIMENT_DICT,
            'language': 'en',
            'sentences': [self.SENTENCE_DICT],
        })

        self._verify_sentiment_response(sentiment_response)

    def _verify_sentiment_response(self, sentiment_response):
        from google.cloud.language.sentiment import Sentiment

        self.assertEqual(sentiment_response.language, 'en')
        self.assertEqual(len(sentiment_response.sentences), 1)
        sentence = sentiment_response.sentences[0]
        self.assertEqual(sentence.begin, 0)
        self.assertEqual(sentence.content, 'It is hailing in Wales.')
        self.assertIsInstance(sentence.sentiment, Sentiment)
        self.assertAlmostEqual(sentiment_response.sentiment.score, 0.4)
        self.assertAlmostEqual(sentiment_response.sentiment.magnitude, 3.14159)


class TestSyntaxResponse(unittest.TestCase):
    SENTENCE_DICT = copy(TestSentimentResponse.SENTENCE_DICT)
    TOKEN_DICT = {
        'dependencyEdge': {
            'headTokenIndex': 0,
            'label': 'NSUBJ',
        },
        'lemma': 'it',
        'partOfSpeech': {
            'tag': 'PRON',
        },
        'text': {
            'beginOffset': 0,
            'content': 'It'
        },
    }

    def test_constructor(self):
        from google.cloud.language.api_responses import SyntaxResponse
        from google.cloud.language.sentence import Sentence
        from google.cloud.language.syntax import Token

        syntax_response = SyntaxResponse(
            language='en',
            sentences=[Sentence.from_api_repr(self.SENTENCE_DICT)],
            tokens=[Token.from_api_repr(self.TOKEN_DICT)],
        )

        self._verify_syntax_response(syntax_response)

    def test_api_repr_factory(self):
        from google.cloud.language.api_responses import SyntaxResponse

        syntax_response = SyntaxResponse.from_api_repr({
            'language': 'en',
            'sentences': [self.SENTENCE_DICT],
            'tokens': [self.TOKEN_DICT],
        })

        self._verify_syntax_response(syntax_response)

    def _verify_syntax_response(self, syntax_response):
        from google.cloud.language.sentiment import Sentiment
        from google.cloud.language.syntax import PartOfSpeech

        self.assertEqual(syntax_response.language, 'en')

        self.assertEqual(len(syntax_response.sentences), 1)
        sentence = syntax_response.sentences[0]
        self.assertEqual(sentence.begin, 0)
        self.assertEqual(sentence.content, 'It is hailing in Wales.')
        self.assertIsInstance(sentence.sentiment, Sentiment)
        self.assertEqual(len(syntax_response.tokens), 1)
        token = syntax_response.tokens[0]
        self.assertEqual(token.text_content, 'It')
        self.assertEqual(token.text_begin, 0)
        self.assertEqual(token.part_of_speech, PartOfSpeech.PRONOUN)
        self.assertEqual(token.edge_index, 0)
        self.assertEqual(token.edge_label, 'NSUBJ')
        self.assertEqual(token.lemma, 'it')
