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

from google.cloud import exceptions
from google.cloud import language
from google.cloud import storage

from test_utils.system import unique_resource_id
from test_utils.retry import RetryErrors


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    TEST_BUCKET = None


def setUpModule():
    Config.CLIENT = language.Client()
    # Now create a bucket for GCS stored content.
    storage_client = storage.Client()
    bucket_name = 'new' + unique_resource_id()
    Config.TEST_BUCKET = storage_client.bucket(bucket_name)
    # 429 Too Many Requests in case API requests rate-limited.
    retry_429 = RetryErrors(exceptions.TooManyRequests)
    retry_429(Config.TEST_BUCKET.create)()


def tearDownModule():
    # 409 Conflict if the bucket is full.
    # 429 Too Many Requests in case API requests rate-limited.
    bucket_retry = RetryErrors(
        (exceptions.TooManyRequests, exceptions.Conflict))
    bucket_retry(Config.TEST_BUCKET.delete)(force=True)


class TestLanguage(unittest.TestCase):

    NAME1 = 'Michelangelo Caravaggio'
    NAME2 = 'Italian'
    NAME3 = 'The Calling of Saint Matthew'
    TEXT_CONTENT = '%s, %s painter, is known for %r.' % (NAME1, NAME2, NAME3)

    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()

    def _check_analyze_entities_result(self, entities):
        from google.cloud.language.entity import EntityType

        self.assertEqual(len(entities), 3)
        entity1, entity2, entity3 = entities
        # Verify entity 1.
        self.assertEqual(entity1.name, self.NAME1)
        self.assertEqual(entity1.entity_type, EntityType.PERSON)
        self.assertGreater(entity1.salience, 0.0)
        # Other mentions may occur, e.g. "painter".
        self.assertIn(entity1.name, [str(i) for i in entity1.mentions])
        self.assertEqual(entity1.metadata['wikipedia_url'],
                         'http://en.wikipedia.org/wiki/Caravaggio')
        self.assertIsInstance(entity1.metadata, dict)
        # Verify entity 2.
        self.assertEqual(entity2.name, self.NAME2)
        self.assertEqual(entity2.entity_type, EntityType.LOCATION)
        self.assertGreater(entity2.salience, 0.0)
        self.assertEqual([str(i) for i in entity2.mentions], [entity2.name])
        self.assertEqual(entity2.metadata['wikipedia_url'],
                         'http://en.wikipedia.org/wiki/Italy')
        self.assertIsInstance(entity2.metadata, dict)
        # Verify entity 3.
        self.assertEqual(entity3.name, self.NAME3)
        choices = (EntityType.EVENT, EntityType.WORK_OF_ART)
        self.assertIn(entity3.entity_type, choices)
        self.assertGreater(entity3.salience, 0.0)
        self.assertEqual([str(i) for i in entity3.mentions], [entity3.name])
        wiki_url = ('http://en.wikipedia.org/wiki/'
                    'The_Calling_of_St_Matthew_(Caravaggio)')
        self.assertEqual(entity3.metadata['wikipedia_url'], wiki_url)
        self.assertIsInstance(entity3.metadata, dict)

    def test_analyze_entities(self):
        document = Config.CLIENT.document_from_text(self.TEXT_CONTENT)
        response = document.analyze_entities()
        self.assertEqual(response.language, 'en')
        self._check_analyze_entities_result(response.entities)

    def test_analyze_entities_from_blob(self):
        # Upload the text to a blob.
        bucket_name = Config.TEST_BUCKET.name
        blob_name = 'document.txt'
        blob = Config.TEST_BUCKET.blob(blob_name)
        self.to_delete_by_case.append(blob)  # Clean-up.
        blob.upload_from_string(self.TEXT_CONTENT)

        # Create a document referencing that blob.
        gcs_url = 'gs://%s/%s' % (bucket_name, blob_name)
        document = Config.CLIENT.document_from_url(gcs_url)
        entities = document.analyze_entities().entities
        self._check_analyze_entities_result(entities)

    def test_analyze_sentiment(self):
        positive_msg = 'Jogging is fun'
        document = Config.CLIENT.document_from_text(positive_msg)
        sentiment = document.analyze_sentiment().sentiment
        self.assertEqual(sentiment.score, 0.5)
        self.assertTrue(0.0 < sentiment.magnitude < 1.5)

    def _verify_token(self, token, text_content, part_of_speech, lemma):
        from google.cloud.language.syntax import Token

        self.assertIsInstance(token, Token)
        self.assertEqual(token.text_content, text_content)
        self.assertEqual(token.part_of_speech, part_of_speech)
        self.assertEqual(token.lemma, lemma)

    def _check_analyze_syntax_result(self, tokens):
        from google.cloud.language.syntax import PartOfSpeech

        self.assertEqual(len(tokens), 3)
        token1, token2, token3 = tokens
        # Verify token 1.
        self._verify_token(token1, 'Jogging', PartOfSpeech.NOUN, 'Jogging')
        # Verify token 2.
        self._verify_token(token2, 'is', PartOfSpeech.VERB, 'be')
        # Verify token 3.
        self._verify_token(token3, 'fun', PartOfSpeech.ADJECTIVE, 'fun')

    def test_analyze_syntax(self):
        positive_msg = 'Jogging is fun'
        document = Config.CLIENT.document_from_text(positive_msg)
        tokens = document.analyze_syntax().tokens
        self._check_analyze_syntax_result(tokens)
