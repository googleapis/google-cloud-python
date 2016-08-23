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

from gcloud import language


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None


def setUpModule():
    Config.CLIENT = language.Client()


class TestLanguage(unittest.TestCase):

    def test_analyze_entities(self):
        from gcloud.language.entity import EntityType

        text_content = ("Michelangelo Caravaggio, Italian painter, is "
                        "known for 'The Calling of Saint Matthew'.")
        document = Config.CLIENT.document_from_text(text_content)
        entities = document.analyze_entities()
        self.assertEqual(len(entities), 3)
        entity1, entity2, entity3 = entities
        # Verify entity 1.
        self.assertEqual(entity1.name, 'Michelangelo Caravaggio')
        self.assertEqual(entity1.entity_type, EntityType.PERSON)
        self.assertTrue(0.7 < entity1.salience < 0.8)
        self.assertEqual(entity1.mentions, [entity1.name])
        self.assertEqual(entity1.metadata, {
            'wikipedia_url': 'http://en.wikipedia.org/wiki/Caravaggio',
        })
        # Verify entity 2.
        self.assertEqual(entity2.name, 'Italian')
        self.assertEqual(entity2.entity_type, EntityType.LOCATION)
        self.assertTrue(0.15 < entity2.salience < 0.25)
        self.assertEqual(entity2.mentions, [entity2.name])
        self.assertEqual(entity2.metadata, {
            'wikipedia_url': 'http://en.wikipedia.org/wiki/Italy',
        })
        # Verify entity 3.
        self.assertEqual(entity3.name, 'The Calling of Saint Matthew')
        self.assertEqual(entity3.entity_type, EntityType.EVENT)
        self.assertTrue(0 < entity3.salience < 0.1)
        self.assertEqual(entity3.mentions, [entity3.name])
        wiki_url = ('http://en.wikipedia.org/wiki/'
                    'The_Calling_of_St_Matthew_(Caravaggio)')
        self.assertEqual(entity3.metadata, {'wikipedia_url': wiki_url})
