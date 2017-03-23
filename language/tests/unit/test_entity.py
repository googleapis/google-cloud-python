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


class TestEntity(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.language.entity import Entity

        return Entity

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        from google.cloud.language.entity import Mention
        from google.cloud.language.entity import MentionType
        from google.cloud.language.entity import TextSpan

        name = 'Italian'
        entity_type = 'LOCATION'
        wiki_url = 'http://en.wikipedia.org/wiki/Italy'
        metadata = {
            'foo': 'bar',
            'wikipedia_url': wiki_url,
        }
        salience = 0.19960518
        mentions = [Mention(
            mention_type=MentionType.PROPER,
            text=TextSpan(content='Italian', begin_offset=0),
        )]
        entity = self._make_one(name, entity_type, metadata,
                                salience, mentions)
        self.assertEqual(entity.name, name)
        self.assertEqual(entity.entity_type, entity_type)
        self.assertEqual(entity.metadata, metadata)
        self.assertEqual(entity.salience, salience)
        self.assertEqual(entity.mentions, mentions)

    def test_from_api_repr(self):
        from google.cloud.language.entity import EntityType
        from google.cloud.language.entity import Mention
        from google.cloud.language.entity import MentionType

        klass = self._get_target_class()
        name = 'Italy'
        entity_type = EntityType.LOCATION
        salience = 0.223
        wiki_url = 'http://en.wikipedia.org/wiki/Italy'
        mention1 = 'Italy'
        mention2 = 'To Italy'
        mention3 = 'From Italy'
        payload = {
            'name': name,
            'type': entity_type,
            'salience': salience,
            'metadata': {'wikipedia_url': wiki_url},
            'mentions': [
                {'text': {'content': mention1, 'beginOffset': 3},
                 'type': 'PROPER'},
                {'text': {'content': mention2, 'beginOffset': 5},
                 'type': 'PROPER'},
                {'text': {'content': mention3, 'beginOffset': 8},
                 'type': 'PROPER'},
            ],
        }
        entity = klass.from_api_repr(payload)
        self.assertEqual(entity.name, name)
        self.assertEqual(entity.entity_type, entity_type)
        self.assertEqual(entity.salience, salience)
        self.assertEqual(entity.metadata, {'wikipedia_url': wiki_url})

        # Assert that we got back Mention objects for each mention.
        self.assertIsInstance(entity.mentions[0], Mention)
        self.assertIsInstance(entity.mentions[1], Mention)
        self.assertIsInstance(entity.mentions[2], Mention)

        # Assert that the text (and string coercison) are correct.
        self.assertEqual([str(i) for i in entity.mentions],
                         [mention1, mention2, mention3])

        # Assert that the begin offsets are preserved.
        self.assertEqual([i.text.begin_offset for i in entity.mentions],
                         [3, 5, 8])

        # Assert that the mention types are preserved.
        for mention in entity.mentions:
            self.assertEqual(mention.mention_type, MentionType.PROPER)


class TestMention(unittest.TestCase):
    PAYLOAD = {
        'text': {'content': 'Greece', 'beginOffset': 42},
        'type': 'PROPER',
    }

    def test_constructor(self):
        from google.cloud.language.entity import Mention
        from google.cloud.language.entity import MentionType
        from google.cloud.language.entity import TextSpan

        mention = Mention(
            text=TextSpan(content='snails', begin_offset=90),
            mention_type=MentionType.COMMON,
        )

        self.assertIsInstance(mention.text, TextSpan)
        self.assertEqual(mention.text.content, 'snails')
        self.assertEqual(mention.text.begin_offset, 90)
        self.assertEqual(mention.mention_type, MentionType.COMMON)

    def test_from_api_repr(self):
        from google.cloud.language.entity import Mention
        from google.cloud.language.entity import MentionType
        from google.cloud.language.entity import TextSpan

        mention = Mention.from_api_repr(self.PAYLOAD)

        self.assertIsInstance(mention, Mention)
        self.assertIsInstance(mention.text, TextSpan)
        self.assertEqual(mention.text.content, 'Greece')
        self.assertEqual(mention.text.begin_offset, 42)
        self.assertEqual(mention.mention_type, MentionType.PROPER)

    def test_dunder_str(self):
        from google.cloud.language.entity import Mention

        mention = Mention.from_api_repr(self.PAYLOAD)
        self.assertEqual(str(mention), 'Greece')


class TestTextSpan(unittest.TestCase):
    def test_constructor(self):
        from google.cloud.language.entity import TextSpan

        text = TextSpan(content='Winston Churchill', begin_offset=1945)
        self.assertIsInstance(text, TextSpan)
        self.assertEqual(text.content, str(text), 'Winston Churchill')
        self.assertEqual(text.begin_offset, 1945)

    def test_from_api_repr(self):
        from google.cloud.language.entity import TextSpan

        text = TextSpan.from_api_repr({
            'beginOffset': 1953,
            'content': 'Queen Elizabeth',
        })
        self.assertIsInstance(text, TextSpan)
        self.assertEqual(text.content, str(text), 'Queen Elizabeth')
        self.assertEqual(text.begin_offset, 1953)
