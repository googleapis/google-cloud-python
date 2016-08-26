# Copyright 2016 Google Inc. All rights reserved.
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

from gcloud import _helpers
from gcloud.environment_vars import TESTS_PROJECT
from gcloud import exceptions
from gcloud import language
from gcloud import storage

from system_test_utils import unique_resource_id
from retry import RetryErrors


# 429 Too Many Requests in case API requests rate-limited.
retry_429 = RetryErrors(exceptions.TooManyRequests)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    TEST_BUCKET = None


def setUpModule():
    _helpers.PROJECT = TESTS_PROJECT
    Config.CLIENT = language.Client()
    # Now create a bucket for GCS stored content.
    storage_client = storage.Client()
    bucket_name = 'new' + unique_resource_id()
    Config.TEST_BUCKET = storage_client.bucket(bucket_name)
    retry_429(Config.TEST_BUCKET.create)()


def tearDownModule():
    retry_429(Config.TEST_BUCKET.delete)()


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
        from gcloud.language.entity import EntityType

        self.assertEqual(len(entities), 3)
        entity1, entity2, entity3 = entities
        # Verify entity 1.
        self.assertEqual(entity1.name, self.NAME1)
        self.assertEqual(entity1.entity_type, EntityType.PERSON)
        self.assertTrue(0.7 < entity1.salience < 0.8)
        self.assertEqual(entity1.mentions, [entity1.name])
        self.assertEqual(entity1.wikipedia_url,
                         'http://en.wikipedia.org/wiki/Caravaggio')
        self.assertEqual(entity1.metadata, {})
        # Verify entity 2.
        self.assertEqual(entity2.name, self.NAME2)
        self.assertEqual(entity2.entity_type, EntityType.LOCATION)
        self.assertTrue(0.15 < entity2.salience < 0.25)
        self.assertEqual(entity2.mentions, [entity2.name])
        self.assertEqual(entity2.wikipedia_url,
                         'http://en.wikipedia.org/wiki/Italy')
        self.assertEqual(entity2.metadata, {})
        # Verify entity 3.
        self.assertEqual(entity3.name, self.NAME3)
        self.assertEqual(entity3.entity_type, EntityType.EVENT)
        self.assertTrue(0 < entity3.salience < 0.1)
        self.assertEqual(entity3.mentions, [entity3.name])
        wiki_url = ('http://en.wikipedia.org/wiki/'
                    'The_Calling_of_St_Matthew_(Caravaggio)')
        self.assertEqual(entity3.wikipedia_url, wiki_url)
        self.assertEqual(entity3.metadata, {})

    def test_analyze_entities(self):
        document = Config.CLIENT.document_from_text(self.TEXT_CONTENT)
        entities = document.analyze_entities()
        self._check_analyze_entities_result(entities)

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
        entities = document.analyze_entities()
        self._check_analyze_entities_result(entities)

    def test_analyze_sentiment(self):
        positive_msg = 'Jogging is fun'
        document = Config.CLIENT.document_from_text(positive_msg)
        sentiment = document.analyze_sentiment()
        self.assertEqual(sentiment.polarity, 1)
        self.assertTrue(0.5 < sentiment.magnitude < 1.5)
