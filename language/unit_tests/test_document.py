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


ANNOTATE_NAME = 'Moon'
ANNOTATE_CONTENT = 'A cow jumped over the %s.' % (ANNOTATE_NAME,)
ANNOTATE_SCORE = 1
ANNOTATE_MAGNITUDE = 0.2
ANNOTATE_SALIENCE = 0.11793101
ANNOTATE_WIKI_URL = 'http://en.wikipedia.org/wiki/Natural_satellite'


def _make_token_json(name, part_of_speech, head, edge_label):
    token_dict = {
        'text': {
            'content': name,
            'beginOffset': -1,
        },
        'partOfSpeech': {'tag': part_of_speech},
        'dependencyEdge': {
            'headTokenIndex': head,
            'label': edge_label,
        },
        'lemma': name,
    }
    return token_dict


def _get_token_and_sentences(include_syntax):
    from google.cloud.language.syntax import PartOfSpeech

    if include_syntax:
        token_info = [
            ('A', PartOfSpeech.DETERMINER, 1, 'DET'),
            ('cow', PartOfSpeech.NOUN, 2, 'NSUBJ'),
            ('jumped', PartOfSpeech.VERB, 2, 'ROOT'),
            ('over', PartOfSpeech.ADPOSITION, 2, 'PREP'),
            ('the', PartOfSpeech.DETERMINER, 5, 'DET'),
            (ANNOTATE_NAME, PartOfSpeech.NOUN, 3, 'POBJ'),
            ('.', PartOfSpeech.PUNCTUATION, 2, 'P'),
        ]
        sentences = [
            {
                'text': {
                    'content': ANNOTATE_CONTENT,
                    'beginOffset': -1,
                },
            },
        ]
    else:
        token_info = []
        sentences = []

    return token_info, sentences


def _get_entities(include_entities):
    from google.cloud.language.entity import EntityType

    if include_entities:
        entities = [
            {
                'name': ANNOTATE_NAME,
                'type': EntityType.LOCATION,
                'metadata': {
                    'wikipedia_url': ANNOTATE_WIKI_URL,
                },
                'salience': ANNOTATE_SALIENCE,
                'mentions': [
                    {
                        'text': {
                            'content': ANNOTATE_NAME,
                            'beginOffset': -1
                        }
                    }
                ]
            },
        ]
    else:
        entities = []

    return entities


def make_mock_client(response):
    import mock
    from google.cloud.language._http import Connection
    from google.cloud.language.client import Client

    connection = mock.Mock(spec=Connection)
    connection.api_request.return_value = response
    return mock.Mock(_connection=connection, spec=Client)


class TestDocument(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.language.document import Document

        return Document

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        import google.cloud.language.document as MUT

        client = object()
        content = 'abc'
        document = self._make_one(client, content)
        self.assertIs(document.client, client)
        self.assertEqual(document.content, content)
        self.assertIsNone(document.gcs_url)
        self.assertIsNone(document.language)
        self.assertEqual(document.doc_type, MUT.Document.PLAIN_TEXT)
        self.assertEqual(document.encoding, MUT.Encoding.UTF8)

    def test_constructor_explicit(self):
        import google.cloud.language.document as MUT

        client = object()
        gcs_url = 'gs://some-bucket/some-obj.html'
        language = 'ja'
        document = self._make_one(client, gcs_url=gcs_url,
                                  doc_type=MUT.Document.HTML,
                                  language=language,
                                  encoding=MUT.Encoding.UTF32)
        self.assertIs(document.client, client)
        self.assertIsNone(document.content)
        self.assertEqual(document.gcs_url, gcs_url)
        self.assertEqual(document.doc_type, MUT.Document.HTML)
        self.assertEqual(document.language, language)
        self.assertEqual(document.encoding, MUT.Encoding.UTF32)

    def test_constructor_explicit_language(self):
        client = object()
        content = 'abc'
        document = self._make_one(client, content, language='en-US')
        self.assertEqual(document.language, 'en-US')
        self.assertEqual(document._to_dict()['language'], 'en-US')

    def test_constructor_no_text(self):
        with self.assertRaises(ValueError):
            self._make_one(None, content=None, gcs_url=None)

    def test_constructor_text_and_gcs(self):
        with self.assertRaises(ValueError):
            self._make_one(None, content='abc',
                           gcs_url='gs://some-bucket/some-obj.txt')

    def test__to_dict_with_content(self):
        klass = self._get_target_class()
        content = 'Hello World'
        document = self._make_one(None, content=content)
        info = document._to_dict()
        self.assertEqual(info, {
            'content': content,
            'type': klass.PLAIN_TEXT,
        })

    def test__to_dict_with_gcs(self):
        klass = self._get_target_class()
        gcs_url = 'gs://some-bucket/some-obj.html'
        document = self._make_one(None, gcs_url=gcs_url)
        info = document._to_dict()
        self.assertEqual(info, {
            'gcsContentUri': gcs_url,
            'type': klass.PLAIN_TEXT,
        })

    def test__to_dict_with_no_content(self):
        klass = self._get_target_class()
        document = self._make_one(None, content='')
        document.content = None  # Manually unset the content.
        info = document._to_dict()
        self.assertEqual(info, {
            'type': klass.PLAIN_TEXT,
        })

    def _verify_entity(self, entity, name, entity_type, wiki_url, salience):
        from google.cloud.language.entity import Entity

        self.assertIsInstance(entity, Entity)
        self.assertEqual(entity.name, name)
        self.assertEqual(entity.entity_type, entity_type)
        if wiki_url:
            self.assertEqual(entity.metadata, {'wikipedia_url': wiki_url})
        else:
            self.assertEqual(entity.metadata, {})
        self.assertEqual(entity.salience, salience)
        self.assertEqual(entity.mentions, [name])

    @staticmethod
    def _expected_data(content, encoding_type=None,
                       extract_sentiment=False,
                       extract_entities=False,
                       extract_syntax=False):
        from google.cloud.language.document import Document

        expected = {
            'document': {
                'type': Document.PLAIN_TEXT,
                'content': content,
            },
        }
        if encoding_type is not None:
            expected['encodingType'] = encoding_type
        if extract_sentiment:
            features = expected.setdefault('features', {})
            features['extractDocumentSentiment'] = True
        if extract_entities:
            features = expected.setdefault('features', {})
            features['extractEntities'] = True
        if extract_syntax:
            features = expected.setdefault('features', {})
            features['extractSyntax'] = True
        return expected

    def test_analyze_entities(self):
        from google.cloud.language.document import Encoding
        from google.cloud.language.entity import EntityType

        name1 = 'R-O-C-K'
        name2 = 'USA'
        content = name1 + ' in the ' + name2
        wiki2 = 'http://en.wikipedia.org/wiki/United_States'
        salience1 = 0.91391456
        salience2 = 0.086085409
        response = {
            'entities': [
                {
                    'name': name1,
                    'type': EntityType.OTHER,
                    'metadata': {},
                    'salience': salience1,
                    'mentions': [
                        {
                            'text': {
                                'content': name1,
                                'beginOffset': -1
                            }
                        }
                    ]
                },
                {
                    'name': name2,
                    'type': EntityType.LOCATION,
                    'metadata': {'wikipedia_url': wiki2},
                    'salience': salience2,
                    'mentions': [
                        {
                            'text': {
                                'content': name2,
                                'beginOffset': -1,
                            },
                        },
                    ],
                },
            ],
            'language': 'en-US',
        }
        client = make_mock_client(response)
        document = self._make_one(client, content)

        entity_response = document.analyze_entities()
        self.assertEqual(len(entity_response.entities), 2)
        entity1 = entity_response.entities[0]
        self._verify_entity(entity1, name1, EntityType.OTHER,
                            None, salience1)
        entity2 = entity_response.entities[1]
        self._verify_entity(entity2, name2, EntityType.LOCATION,
                            wiki2, salience2)

        # Verify the request.
        expected = self._expected_data(
            content, encoding_type=Encoding.UTF8)
        client._connection.api_request.assert_called_once_with(
            path='analyzeEntities', method='POST', data=expected)

    def _verify_sentiment(self, sentiment, score, magnitude):
        from google.cloud.language.sentiment import Sentiment

        self.assertIsInstance(sentiment, Sentiment)
        self.assertEqual(sentiment.score, score)
        self.assertEqual(sentiment.magnitude, magnitude)

    def test_analyze_sentiment(self):
        from google.cloud.language.api_responses import SentimentResponse

        content = 'All the pretty horses.'
        score = 1
        magnitude = 0.6
        response = {
            'documentSentiment': {
                'score': score,
                'magnitude': magnitude,
            },
            'language': 'en-US',
        }
        client = make_mock_client(response)
        document = self._make_one(client, content)

        sentiment_response = document.analyze_sentiment()
        self.assertIsInstance(sentiment_response, SentimentResponse)
        self._verify_sentiment(sentiment_response.sentiment, score, magnitude)

        # Verify the request.
        expected = self._expected_data(content)
        client._connection.api_request.assert_called_once_with(
            path='analyzeSentiment', method='POST', data=expected)

    def _verify_token(self, token, text_content, part_of_speech, lemma):
        from google.cloud.language.syntax import Token

        self.assertIsInstance(token, Token)
        self.assertEqual(token.text_content, text_content)
        self.assertEqual(token.part_of_speech, part_of_speech)
        self.assertEqual(token.lemma, lemma)

    def test_analyze_syntax(self):
        from google.cloud.language.api_responses import SyntaxResponse
        from google.cloud.language.document import Encoding
        from google.cloud.language.syntax import PartOfSpeech

        name1 = 'R-O-C-K'
        name2 = 'USA'
        content = name1 + ' in the ' + name2
        response = {
            'sentences': [
                {
                    'text': {
                        'content': 'R-O-C-K in the USA',
                        'beginOffset': -1,
                    },
                    'sentiment': None,
                }
            ],
            'tokens': [
                {
                    'text': {
                        'content': 'R-O-C-K',
                        'beginOffset': -1,
                    },
                    'partOfSpeech': {
                        'tag': 'NOUN',
                    },
                    'dependencyEdge': {
                        'headTokenIndex': 0,
                        'label': 'ROOT',
                    },
                    'lemma': 'R-O-C-K',
                },
                {
                    'text': {
                        'content': 'in',
                        'beginOffset': -1,
                    },
                    'partOfSpeech': {
                        'tag': 'ADP',
                    },
                    'dependencyEdge': {
                        'headTokenIndex': 0,
                        'label': 'PREP',
                    },
                    'lemma': 'in',
                },
                {
                    'text': {
                        'content': 'the',
                        'beginOffset': -1,
                    },
                    'partOfSpeech': {
                        'tag': 'DET',
                    },
                    'dependencyEdge': {
                        'headTokenIndex': 3,
                        'label': 'DET',
                    },
                    'lemma': 'the',
                },
                {
                    'text': {
                        'content': 'USA',
                        'beginOffset': -1,
                    },
                    'partOfSpeech': {
                        'tag': 'NOUN',
                    },
                    'dependencyEdge': {
                        'headTokenIndex': 1,
                        'label': 'POBJ',
                    },
                    'lemma': 'USA',
                },
            ],
            'language': 'en-US',
        }
        client = make_mock_client(response)
        document = self._make_one(client, content)

        syntax_response = document.analyze_syntax()
        self.assertIsInstance(syntax_response, SyntaxResponse)

        tokens = syntax_response.tokens
        self.assertEqual(len(tokens), 4)
        token1 = tokens[0]
        self._verify_token(token1, name1, PartOfSpeech.NOUN, name1)
        token2 = tokens[1]
        self._verify_token(token2, 'in', PartOfSpeech.ADPOSITION, 'in')
        token3 = tokens[2]
        self._verify_token(token3, 'the', PartOfSpeech.DETERMINER, 'the')
        token4 = tokens[3]
        self._verify_token(token4, name2, PartOfSpeech.NOUN, name2)

        # Verify the request.
        expected = self._expected_data(
            content, encoding_type=Encoding.UTF8)
        client._connection.api_request.assert_called_once_with(
            path='analyzeSyntax', method='POST', data=expected)

    def _verify_sentences(self, include_syntax, annotations):
        from google.cloud.language.sentence import Sentence

        if include_syntax:
            self.assertEqual(len(annotations.sentences), 1)
            sentence = annotations.sentences[0]
            self.assertIsInstance(sentence, Sentence)
            self.assertEqual(sentence.content, ANNOTATE_CONTENT)
            self.assertEqual(sentence.begin, -1)
        else:
            self.assertEqual(annotations.sentences, [])

    def _verify_tokens(self, annotations, token_info):
        from google.cloud.language.syntax import Token

        self.assertEqual(len(annotations.tokens), len(token_info))
        for token, info in zip(annotations.tokens, token_info):
            self.assertIsInstance(token, Token)
            self.assertEqual(token.text_content, info[0])
            self.assertEqual(token.text_begin, -1)
            self.assertEqual(token.part_of_speech, info[1])
            self.assertEqual(token.edge_index, info[2])
            self.assertEqual(token.edge_label, info[3])
            self.assertEqual(token.lemma, info[0])

    def _annotate_text_helper(self, include_sentiment,
                              include_entities, include_syntax):
        from google.cloud.language.document import Annotations
        from google.cloud.language.document import Encoding
        from google.cloud.language.entity import EntityType

        token_info, sentences = _get_token_and_sentences(include_syntax)
        entities = _get_entities(include_entities)
        tokens = [_make_token_json(*info) for info in token_info]
        response = {
            'sentences': sentences,
            'tokens': tokens,
            'entities': entities,
            'language': 'en-US',
        }
        if include_sentiment:
            response['documentSentiment'] = {
                'score': ANNOTATE_SCORE,
                'magnitude': ANNOTATE_MAGNITUDE,
            }

        client = make_mock_client(response)
        document = self._make_one(client, ANNOTATE_CONTENT)

        annotations = document.annotate_text(
            include_syntax=include_syntax, include_entities=include_entities,
            include_sentiment=include_sentiment)
        self.assertIsInstance(annotations, Annotations)
        # Sentences
        self._verify_sentences(include_syntax, annotations)
        # Token
        self._verify_tokens(annotations, token_info)
        # Sentiment
        if include_sentiment:
            self._verify_sentiment(annotations.sentiment,
                                   ANNOTATE_SCORE, ANNOTATE_MAGNITUDE)
        else:
            self.assertIsNone(annotations.sentiment)
        # Entity
        if include_entities:
            self.assertEqual(len(annotations.entities), 1)
            entity = annotations.entities[0]
            self._verify_entity(entity, ANNOTATE_NAME, EntityType.LOCATION,
                                ANNOTATE_WIKI_URL, ANNOTATE_SALIENCE)
        else:
            self.assertEqual(annotations.entities, [])

        # Verify the request.
        expected = self._expected_data(
            ANNOTATE_CONTENT, encoding_type=Encoding.UTF8,
            extract_sentiment=include_sentiment,
            extract_entities=include_entities,
            extract_syntax=include_syntax)
        client._connection.api_request.assert_called_once_with(
            path='annotateText', method='POST', data=expected)

    def test_annotate_text(self):
        self._annotate_text_helper(True, True, True)

    def test_annotate_text_sentiment_only(self):
        self._annotate_text_helper(True, False, False)

    def test_annotate_text_entities_only(self):
        self._annotate_text_helper(False, True, False)

    def test_annotate_text_syntax_only(self):
        self._annotate_text_helper(False, False, True)
