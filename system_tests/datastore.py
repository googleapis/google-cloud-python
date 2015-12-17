# Copyright 2014 Google Inc. All rights reserved.
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

import datetime
import unittest2

from gcloud._helpers import UTC
from gcloud import datastore
from gcloud.datastore import client
from gcloud.environment_vars import TESTS_DATASET
from gcloud.exceptions import Conflict
# This assumes the command is being run via tox hence the
# repository root is the current directory.
from system_tests import populate_datastore


client.DATASET = TESTS_DATASET
CLIENT = datastore.Client()


class TestDatastore(unittest2.TestCase):

    def setUp(self):
        self.case_entities_to_delete = []

    def tearDown(self):
        with CLIENT.transaction():
            keys = [entity.key for entity in self.case_entities_to_delete]
            CLIENT.delete_multi(keys)


class TestDatastoreAllocateIDs(TestDatastore):

    def test_allocate_ids(self):
        num_ids = 10
        allocated_keys = CLIENT.allocate_ids(CLIENT.key('Kind'), num_ids)
        self.assertEqual(len(allocated_keys), num_ids)

        unique_ids = set()
        for key in allocated_keys:
            unique_ids.add(key.id)
            self.assertEqual(key.name, None)
            self.assertNotEqual(key.id, None)

        self.assertEqual(len(unique_ids), num_ids)


class TestDatastoreSave(TestDatastore):

    PARENT = CLIENT.key('Blog', 'PizzaMan')

    def _get_post(self, id_or_name=None, post_content=None):
        post_content = post_content or {
            'title': u'How to make the perfect pizza in your grill',
            'tags': [u'pizza', u'grill'],
            'publishedAt': datetime.datetime(2001, 1, 1, tzinfo=UTC),
            'author': u'Silvano',
            'isDraft': False,
            'wordCount': 400,
            'rating': 5.0,
        }
        # Create an entity with the given content.
        # NOTE: Using a parent to ensure consistency for query
        #       in `test_empty_kind`.
        key = CLIENT.key('Post', parent=self.PARENT)
        entity = datastore.Entity(key=key)
        entity.update(post_content)

        # Update the entity key.
        if id_or_name is not None:
            entity.key = entity.key.completed_key(id_or_name)

        return entity

    def _generic_test_post(self, name=None, key_id=None):
        entity = self._get_post(id_or_name=(name or key_id))
        CLIENT.put(entity)

        # Register entity to be deleted.
        self.case_entities_to_delete.append(entity)

        if name is not None:
            self.assertEqual(entity.key.name, name)
        if key_id is not None:
            self.assertEqual(entity.key.id, key_id)
        retrieved_entity = CLIENT.get(entity.key)
        # Check the given and retrieved are the the same.
        self.assertEqual(retrieved_entity, entity)

    def test_post_with_name(self):
        self._generic_test_post(name='post1')

    def test_post_with_id(self):
        self._generic_test_post(key_id=123456789)

    def test_post_with_generated_id(self):
        self._generic_test_post()

    def test_save_multiple(self):
        with CLIENT.transaction() as xact:
            entity1 = self._get_post()
            xact.put(entity1)
            # Register entity to be deleted.
            self.case_entities_to_delete.append(entity1)

            second_post_content = {
                'title': u'How to make the perfect homemade pasta',
                'tags': [u'pasta', u'homemade'],
                'publishedAt': datetime.datetime(2001, 1, 1),
                'author': u'Silvano',
                'isDraft': False,
                'wordCount': 450,
                'rating': 4.5,
            }
            entity2 = self._get_post(post_content=second_post_content)
            xact.put(entity2)
            # Register entity to be deleted.
            self.case_entities_to_delete.append(entity2)

        keys = [entity1.key, entity2.key]
        matches = CLIENT.get_multi(keys)
        self.assertEqual(len(matches), 2)

    def test_empty_kind(self):
        query = CLIENT.query(kind='Post')
        query.ancestor = self.PARENT
        posts = list(query.fetch(limit=2))
        self.assertEqual(posts, [])


class TestDatastoreSaveKeys(TestDatastore):

    def test_save_key_self_reference(self):
        parent_key = CLIENT.key('Residence', 'NewYork')
        key = CLIENT.key('Person', 'name', parent=parent_key)
        entity = datastore.Entity(key=key)
        entity['fullName'] = u'Full name'
        entity['linkedTo'] = key  # Self reference.

        CLIENT.put(entity)
        self.case_entities_to_delete.append(entity)

        query = CLIENT.query(kind='Person')
        # Adding ancestor to ensure consistency.
        query.ancestor = parent_key
        query.add_filter('linkedTo', '=', key)

        stored_persons = list(query.fetch(limit=2))
        self.assertEqual(stored_persons, [entity])


class TestDatastoreQuery(TestDatastore):

    @classmethod
    def setUpClass(cls):
        super(TestDatastoreQuery, cls).setUpClass()
        cls.CHARACTERS = populate_datastore.CHARACTERS
        cls.ANCESTOR_KEY = CLIENT.key(*populate_datastore.ANCESTOR)

    def _base_query(self):
        return CLIENT.query(kind='Character', ancestor=self.ANCESTOR_KEY)

    def test_limit_queries(self):
        limit = 5
        query = self._base_query()

        # Fetch characters.
        iterator = query.fetch(limit=limit)
        character_entities, _, cursor = iterator.next_page()
        self.assertEqual(len(character_entities), limit)

        # Check cursor after fetch.
        self.assertTrue(cursor is not None)

        # Fetch remaining of characters.
        new_character_entities = list(iterator)
        characters_remaining = len(self.CHARACTERS) - limit
        self.assertEqual(len(new_character_entities), characters_remaining)

    def test_query_simple_filter(self):
        query = self._base_query()
        query.add_filter('appearances', '>=', 20)
        expected_matches = 6
        # We expect 6, but allow the query to get 1 extra.
        entities = list(query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

    def test_query_multiple_filters(self):
        query = self._base_query()
        query.add_filter('appearances', '>=', 26)
        query.add_filter('family', '=', 'Stark')
        expected_matches = 4
        # We expect 4, but allow the query to get 1 extra.
        entities = list(query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

    def test_ancestor_query(self):
        filtered_query = self._base_query()

        expected_matches = 8
        # We expect 8, but allow the query to get 1 extra.
        entities = list(filtered_query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

    def test_query___key___filter(self):
        rickard_key = CLIENT.key(*populate_datastore.RICKARD)

        query = self._base_query()
        query.add_filter('__key__', '=', rickard_key)
        expected_matches = 1
        # We expect 1, but allow the query to get 1 extra.
        entities = list(query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

    def test_ordered_query(self):
        query = self._base_query()
        query.order = 'appearances'
        expected_matches = 8
        # We expect 8, but allow the query to get 1 extra.
        entities = list(query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

        # Actually check the ordered data returned.
        self.assertEqual(entities[0]['name'], self.CHARACTERS[0]['name'])
        self.assertEqual(entities[7]['name'], self.CHARACTERS[3]['name'])

    def test_projection_query(self):
        filtered_query = self._base_query()
        filtered_query.projection = ['name', 'family']

        # NOTE: There are 9 responses because of Catelyn. She has both
        #       Stark and Tully as her families, hence occurs twice in
        #       the results.
        expected_matches = 9
        # We expect 9, but allow the query to get 1 extra.
        entities = list(filtered_query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

        arya_entity = entities[0]
        arya_dict = dict(arya_entity)
        self.assertEqual(arya_dict, {'name': 'Arya', 'family': 'Stark'})

        catelyn_stark_entity = entities[2]
        catelyn_stark_dict = dict(catelyn_stark_entity)
        self.assertEqual(catelyn_stark_dict,
                         {'name': 'Catelyn', 'family': 'Stark'})

        catelyn_tully_entity = entities[3]
        catelyn_tully_dict = dict(catelyn_tully_entity)
        self.assertEqual(catelyn_tully_dict,
                         {'name': 'Catelyn', 'family': 'Tully'})

        # Check both Catelyn keys are the same.
        self.assertEqual(catelyn_stark_entity.key, catelyn_tully_entity.key)

        sansa_entity = entities[8]
        sansa_dict = dict(sansa_entity)
        self.assertEqual(sansa_dict, {'name': 'Sansa', 'family': 'Stark'})

    def test_query_paginate_with_offset(self):
        page_query = self._base_query()
        page_query.order = 'appearances'
        offset = 2
        limit = 3
        iterator = page_query.fetch(limit=limit, offset=offset)

        # Fetch characters.
        entities, _, cursor = iterator.next_page()
        self.assertEqual(len(entities), limit)
        self.assertEqual(entities[0]['name'], 'Robb')
        self.assertEqual(entities[1]['name'], 'Bran')
        self.assertEqual(entities[2]['name'], 'Catelyn')

        # Fetch next set of characters.
        new_iterator = page_query.fetch(limit=limit, offset=0,
                                        start_cursor=cursor)
        entities = list(new_iterator)
        self.assertEqual(len(entities), limit)
        self.assertEqual(entities[0]['name'], 'Sansa')
        self.assertEqual(entities[1]['name'], 'Jon Snow')
        self.assertEqual(entities[2]['name'], 'Arya')

    def test_query_paginate_with_start_cursor(self):
        page_query = self._base_query()
        page_query.order = 'appearances'
        limit = 3
        offset = 2
        iterator = page_query.fetch(limit=limit, offset=offset)

        # Fetch characters.
        entities, _, cursor = iterator.next_page()
        self.assertEqual(len(entities), limit)

        # Use cursor to create a fresh query.
        fresh_query = self._base_query()
        fresh_query.order = 'appearances'

        new_entities = list(fresh_query.fetch(start_cursor=cursor,
                                              limit=limit))
        characters_remaining = len(self.CHARACTERS) - limit - offset
        self.assertEqual(len(new_entities), characters_remaining)
        self.assertEqual(new_entities[0]['name'], 'Sansa')
        self.assertEqual(new_entities[2]['name'], 'Arya')

    def test_query_group_by(self):
        query = self._base_query()
        query.group_by = ['alive']

        expected_matches = 2
        # We expect 2, but allow the query to get 1 extra.
        entities = list(query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

        self.assertEqual(entities[0]['name'], 'Catelyn')
        self.assertEqual(entities[1]['name'], 'Arya')


class TestDatastoreTransaction(TestDatastore):

    def test_transaction(self):
        entity = datastore.Entity(key=CLIENT.key('Company', 'Google'))
        entity['url'] = u'www.google.com'

        with CLIENT.transaction() as xact:
            result = CLIENT.get(entity.key)
            if result is None:
                xact.put(entity)
                self.case_entities_to_delete.append(entity)

        # This will always return after the transaction.
        retrieved_entity = CLIENT.get(entity.key)
        self.case_entities_to_delete.append(retrieved_entity)
        self.assertEqual(retrieved_entity, entity)

    def test_failure_with_contention(self):
        contention_key = 'baz'
        # Fool the Client constructor to avoid creating a new connection.
        local_client = datastore.Client(dataset_id=CLIENT.dataset_id,
                                        http=object())
        local_client.connection = CLIENT.connection

        # Insert an entity which will be retrieved in a transaction
        # and updated outside it with a contentious value.
        key = local_client.key('BreakTxn', 1234)
        orig_entity = datastore.Entity(key=key)
        orig_entity['foo'] = u'bar'
        local_client.put(orig_entity)
        self.case_entities_to_delete.append(orig_entity)

        with self.assertRaises(Conflict):
            with local_client.transaction() as txn:
                entity_in_txn = local_client.get(key)

                # Update the original entity outside the transaction.
                orig_entity[contention_key] = u'outside'
                CLIENT.put(orig_entity)

                # Try to update the entity which we already updated outside the
                # transaction.
                entity_in_txn[contention_key] = u'inside'
                txn.put(entity_in_txn)
