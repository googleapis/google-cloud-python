# Copyright 2016 Google Inc. All Rights Reserved.
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
ANNOTATE_POLARITY = 1
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
    from gcloud.language.syntax import PartOfSpeech

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
    from gcloud.language.entity import EntityType

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


class TestDocument(unittest.TestCase):

    def _getTargetClass(self):
        from gcloud.language.document import Document
        return Document

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constructor_defaults(self):
        import gcloud.language.document as MUT

        client = object()
        content = 'abc'
        document = self._makeOne(client, content)
        self.assertIs(document.client, client)
        self.assertEqual(document.content, content)
        self.assertIsNone(document.gcs_url)
        self.assertEqual(document.doc_type, MUT.Document.PLAIN_TEXT)
        self.assertEqual(document.language, MUT.DEFAULT_LANGUAGE)
        self.assertEqual(document.encoding, MUT.Encoding.UTF8)

    def test_constructor_explicit(self):
        import gcloud.language.document as MUT

        client = object()
        gcs_url = 'gs://some-bucket/some-obj.html'
        language = 'ja'
        document = self._makeOne(client, gcs_url=gcs_url,
                                 doc_type=MUT.Document.HTML,
                                 language=language,
                                 encoding=MUT.Encoding.UTF32)
        self.assertIs(document.client, client)
        self.assertIsNone(document.content)
        self.assertEqual(document.gcs_url, gcs_url)
        self.assertEqual(document.doc_type, MUT.Document.HTML)
        self.assertEqual(document.language, language)
        self.assertEqual(document.encoding, MUT.Encoding.UTF32)

    def test_constructor_no_text(self):
        with self.assertRaises(ValueError):
            self._makeOne(None, content=None, gcs_url=None)

    def test_constructor_text_and_gcs(self):
        with self.assertRaises(ValueError):
            self._makeOne(None, content='abc',
                          gcs_url='gs://some-bucket/some-obj.txt')

    def test__to_dict_with_content(self):
        klass = self._getTargetClass()
        content = 'Hello World'
        document = self._makeOne(None, content=content)
        info = document._to_dict()
        self.assertEqual(info, {
            'content': content,
            'language': document.language,
            'type': klass.PLAIN_TEXT,
        })

    def test__to_dict_with_gcs(self):
        klass = self._getTargetClass()
        gcs_url = 'gs://some-bucket/some-obj.html'
        document = self._makeOne(None, gcs_url=gcs_url)
        info = document._to_dict()
        self.assertEqual(info, {
            'gcsContentUri': gcs_url,
            'language': document.language,
            'type': klass.PLAIN_TEXT,
        })

    def test__to_dict_with_no_content(self):
        klass = self._getTargetClass()
        document = self._makeOne(None, content='')
        document.content = None  # Manually unset the content.
        info = document._to_dict()
        self.assertEqual(info, {
            'language': document.language,
            'type': klass.PLAIN_TEXT,
        })

    def _verify_entity(self, entity, name, entity_type, wiki_url, salience):
        from gcloud.language.entity import Entity

        self.assertIsInstance(entity, Entity)
        self.assertEqual(entity.name, name)
        self.assertEqual(entity.entity_type, entity_type)
        self.assertEqual(entity.wikipedia_url, wiki_url)
        self.assertEqual(entity.metadata, {})
        self.assertEqual(entity.salience, salience)
        self.assertEqual(entity.mentions, [name])

    def test_analyze_entities(self):
        from gcloud.language.entity import EntityType

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
        connection = _Connection(response)
        client = _Client(connection=connection)
        document = self._makeOne(client, content)

        entities = document.analyze_entities()
        self.assertEqual(len(entities), 2)
        entity1 = entities[0]
        self._verify_entity(entity1, name1, EntityType.OTHER,
                            None, salience1)
        entity2 = entities[1]
        self._verify_entity(entity2, name2, EntityType.LOCATION,
                            wiki2, salience2)

        # Verify the request.
        self.assertEqual(len(connection._requested), 1)
        req = connection._requested[0]
        self.assertEqual(req['path'], 'analyzeEntities')
        self.assertEqual(req['method'], 'POST')

    def _verify_sentiment(self, sentiment, polarity, magnitude):
        from gcloud.language.sentiment import Sentiment

        self.assertIsInstance(sentiment, Sentiment)
        self.assertEqual(sentiment.polarity, polarity)
        self.assertEqual(sentiment.magnitude, magnitude)

    def test_analyze_sentiment(self):
        content = 'All the pretty horses.'
        polarity = 1
        magnitude = 0.6
        response = {
            'documentSentiment': {
                'polarity': polarity,
                'magnitude': magnitude,
            },
            'language': 'en-US',
        }
        connection = _Connection(response)
        client = _Client(connection=connection)
        document = self._makeOne(client, content)

        sentiment = document.analyze_sentiment()
        self._verify_sentiment(sentiment, polarity, magnitude)

        # Verify the request.
        self.assertEqual(len(connection._requested), 1)
        req = connection._requested[0]
        self.assertEqual(req['path'], 'analyzeSentiment')
        self.assertEqual(req['method'], 'POST')

    def _verify_sentences(self, include_syntax, annotations):
        from gcloud.language.syntax import Sentence

        if include_syntax:
            self.assertEqual(len(annotations.sentences), 1)
            sentence = annotations.sentences[0]
            self.assertIsInstance(sentence, Sentence)
            self.assertEqual(sentence.content, ANNOTATE_CONTENT)
            self.assertEqual(sentence.begin, -1)
        else:
            self.assertEqual(annotations.sentences, [])

    def _verify_tokens(self, annotations, token_info):
        from gcloud.language.syntax import Token

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
        from gcloud.language.document import Annotations
        from gcloud.language.entity import EntityType

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
                'polarity': ANNOTATE_POLARITY,
                'magnitude': ANNOTATE_MAGNITUDE,
            }

        connection = _Connection(response)
        client = _Client(connection=connection)
        document = self._makeOne(client, ANNOTATE_CONTENT)

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
                                   ANNOTATE_POLARITY, ANNOTATE_MAGNITUDE)
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
        self.assertEqual(len(connection._requested), 1)
        req = connection._requested[0]
        self.assertEqual(req['path'], 'annotateText')
        self.assertEqual(req['method'], 'POST')
        features = req['data']['features']
        self.assertEqual(features.get('extractDocumentSentiment', False),
                         include_sentiment)
        self.assertEqual(features.get('extractEntities', False),
                         include_entities)
        self.assertEqual(features.get('extractSyntax', False), include_syntax)

    def test_annotate_text(self):
        self._annotate_text_helper(True, True, True)

    def test_annotate_text_sentiment_only(self):
        self._annotate_text_helper(True, False, False)

    def test_annotate_text_entities_only(self):
        self._annotate_text_helper(False, True, False)

    def test_annotate_text_syntax_only(self):
        self._annotate_text_helper(False, False, True)


class _Connection(object):

    def __init__(self, response):
        self._response = response
        self._requested = []

    def api_request(self, **kwargs):
        self._requested.append(kwargs)
        return self._response


class _Client(object):

    def __init__(self, connection=None):
        self.connection = connection
