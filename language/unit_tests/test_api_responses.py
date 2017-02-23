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


class TestEntityResponse(unittest.TestCase):
    ENTITY_DICT = {
        'mentions': [{'text': {'content': 'Italian'}}],
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

        self.assertEqual(len(entity_response.entities), 1)
        entity = entity_response.entities[0]
        self.assertEqual(entity.name, 'Italian')
        self.assertEqual(len(entity.mentions), 1)
        self.assertEqual(entity.mentions[0], 'Italian')
        self.assertTrue(entity.metadata['wikipedia_url'].endswith('Italy'))
        self.assertAlmostEqual(entity.salience, 0.15)
        self.assertEqual(entity.entity_type, EntityType.LOCATION)
        self.assertEqual(entity_response.language, 'en')
