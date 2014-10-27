import datetime
import pytz
import unittest2

from gcloud import datastore
# This assumes the command is being run via tox hence the
# repository root is the current directory.
from regression import populate_datastore
from regression import regression_utils


class TestDatastore(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dataset = regression_utils.get_dataset()

    def setUp(self):
        self.case_entities_to_delete = []

    def tearDown(self):
        with self.dataset.transaction():
            for entity in self.case_entities_to_delete:
                entity.delete()


class TestDatastoreSave(TestDatastore):

    def _get_post(self, name=None, key_id=None, post_content=None):
        post_content = post_content or {
            'title': 'How to make the perfect pizza in your grill',
            'tags': ['pizza', 'grill'],
            'publishedAt': datetime.datetime(2001, 1, 1, tzinfo=pytz.utc),
            'author': 'Silvano',
            'isDraft': False,
            'wordCount': 400,
            'rating': 5.0,
        }
        # Create an entity with the given content in our dataset.
        entity = self.dataset.entity(kind='Post')
        entity.update(post_content)

        # Update the entity key.
        key = None
        if name is not None:
            key = entity.key().name(name)
        if key_id is not None:
            key = entity.key().id(key_id)
        if key is not None:
            entity.key(key)

        return entity

    def _generic_test_post(self, name=None, key_id=None):
        entity = self._get_post(name=name, key_id=key_id)
        entity.save()

        # Register entity to be deleted.
        self.case_entities_to_delete.append(entity)

        if name is not None:
            self.assertEqual(entity.key().name(), name)
        if key_id is not None:
            self.assertEqual(entity.key().id(), key_id)
        retrieved_entity = self.dataset.get_entity(entity.key())
        # Check the keys are the same.
        self.assertEqual(retrieved_entity.key().path(), entity.key().path())
        self.assertEqual(retrieved_entity.key().namespace(),
                         entity.key().namespace())

        # Check the data is the same.
        retrieved_dict = dict(retrieved_entity.items())
        entity_dict = dict(entity.items())
        self.assertEqual(retrieved_dict, entity_dict)

    def test_post_with_name(self):
        self._generic_test_post(name='post1')

    def test_post_with_id(self):
        self._generic_test_post(key_id=123456789)

    def test_post_with_generated_id(self):
        self._generic_test_post()

    def test_save_multiple(self):
        with self.dataset.transaction():
            entity1 = self._get_post()
            entity1.save()
            # Register entity to be deleted.
            self.case_entities_to_delete.append(entity1)

            second_post_content = {
                'title': 'How to make the perfect homemade pasta',
                'tags': ['pasta', 'homemade'],
                'publishedAt': datetime.datetime(2001, 1, 1),
                'author': 'Silvano',
                'isDraft': False,
                'wordCount': 450,
                'rating': 4.5,
            }
            entity2 = self._get_post(post_content=second_post_content)
            entity2.save()
            # Register entity to be deleted.
            self.case_entities_to_delete.append(entity2)

        keys = [entity1.key(), entity2.key()]
        matches = self.dataset.get_entities(keys)
        self.assertEqual(len(matches), 2)

    def test_empty_kind(self):
        posts = self.dataset.query('Post').limit(2).fetch()
        self.assertEqual(posts, [])


class TestDatastoreQuery(TestDatastore):

    @classmethod
    def setUpClass(cls):
        super(TestDatastoreQuery, cls).setUpClass()
        cls.CHARACTERS = populate_datastore.CHARACTERS
        cls.ANCESTOR_KEY = datastore.key.Key(
            path=[populate_datastore.ANCESTOR])

    def _base_query(self):
        return self.dataset.query('Character').ancestor(self.ANCESTOR_KEY)

    def test_limit_queries(self):
        limit = 5
        query = self._base_query().limit(limit)
        # Verify there is not cursor before fetch().
        self.assertRaises(RuntimeError, query.cursor)

        # Fetch characters.
        character_entities = query.fetch()
        self.assertEqual(len(character_entities), limit)

        # Check cursor after fetch.
        cursor = query.cursor()
        self.assertTrue(cursor is not None)

        # Fetch next batch of characters.
        new_query = self._base_query().with_cursor(cursor)
        new_character_entities = new_query.fetch()
        characters_remaining = len(self.CHARACTERS) - limit
        self.assertEqual(len(new_character_entities), characters_remaining)

    def test_query_simple_filter(self):
        query = self._base_query().filter('appearances >=', 20)
        expected_matches = 6
        # We expect 6, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

    def test_query_multiple_filters(self):
        query = self._base_query().filter(
            'appearances >=', 26).filter('family =', 'Stark')
        expected_matches = 4
        # We expect 4, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

    def test_ancestor_query(self):
        filtered_query = self._base_query()

        expected_matches = 8
        # We expect 8, but allow the query to get 1 extra.
        entities = filtered_query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

    def test_query___key___filter(self):
        rickard_key = datastore.key.Key(
            path=[populate_datastore.ANCESTOR, populate_datastore.RICKARD])

        query = self._base_query().filter('__key__ =', rickard_key)
        expected_matches = 1
        # We expect 1, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

    def test_ordered_query(self):
        query = self._base_query().order('appearances')
        expected_matches = 8
        # We expect 8, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

        # Actually check the ordered data returned.
        self.assertEqual(entities[0]['name'], self.CHARACTERS[0]['name'])
        self.assertEqual(entities[7]['name'], self.CHARACTERS[3]['name'])

    def test_projection_query(self):
        filtered_query = self._base_query().projection(['name', 'family'])

        # NOTE: There are 9 responses because of Catelyn. She has both
        #       Stark and Tully as her families, hence occurs twice in
        #       the results.
        expected_matches = 9
        # We expect 9, but allow the query to get 1 extra.
        entities = filtered_query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

        arya_entity = entities[0]
        arya_dict = dict(arya_entity.items())
        self.assertEqual(arya_dict, {'name': 'Arya', 'family': 'Stark'})

        catelyn_stark_entity = entities[2]
        catelyn_stark_dict = dict(catelyn_stark_entity.items())
        self.assertEqual(catelyn_stark_dict,
                         {'name': 'Catelyn', 'family': 'Stark'})

        catelyn_tully_entity = entities[3]
        catelyn_tully_dict = dict(catelyn_tully_entity.items())
        self.assertEqual(catelyn_tully_dict,
                         {'name': 'Catelyn', 'family': 'Tully'})

        # Check both Catelyn keys are the same.
        catelyn_stark_key = catelyn_stark_entity.key()
        catelyn_tully_key = catelyn_tully_entity.key()
        self.assertEqual(catelyn_stark_key.path(), catelyn_tully_key.path())
        self.assertEqual(catelyn_stark_key.namespace(),
                         catelyn_tully_key.namespace())
        # Also check the _dataset_id since both retrieved from datastore.
        self.assertEqual(catelyn_stark_key._dataset_id,
                         catelyn_tully_key._dataset_id)

        sansa_entity = entities[8]
        sansa_dict = dict(sansa_entity.items())
        self.assertEqual(sansa_dict, {'name': 'Sansa', 'family': 'Stark'})

    def test_query_paginate_with_offset(self):
        query = self._base_query()
        offset = 2
        limit = 3
        page_query = query.offset(offset).limit(limit).order('appearances')
        # Make sure no query set before fetch.
        self.assertRaises(RuntimeError, page_query.cursor)

        # Fetch characters.
        entities = page_query.fetch()
        self.assertEqual(len(entities), limit)
        self.assertEqual(entities[0]['name'], 'Robb')
        self.assertEqual(entities[1]['name'], 'Bran')
        self.assertEqual(entities[2]['name'], 'Catelyn')

        # Use cursor to begin next query.
        cursor = page_query.cursor()
        next_query = page_query.with_cursor(cursor).offset(0)
        self.assertEqual(next_query.limit(), limit)
        # Fetch next set of characters.
        entities = next_query.fetch()
        self.assertEqual(len(entities), limit)
        self.assertEqual(entities[0]['name'], 'Sansa')
        self.assertEqual(entities[1]['name'], 'Jon Snow')
        self.assertEqual(entities[2]['name'], 'Arya')

    def test_query_paginate_with_start_cursor(self):
        query = self._base_query()
        offset = 2
        limit = 2
        page_query = query.offset(offset).limit(limit).order('appearances')
        # Make sure no query set before fetch.
        self.assertRaises(RuntimeError, page_query.cursor)

        # Fetch characters.
        entities = page_query.fetch()
        self.assertEqual(len(entities), limit)

        # Use cursor to create a fresh query.
        cursor = page_query.cursor()
        fresh_query = self._base_query()
        fresh_query = fresh_query.order('appearances').with_cursor(cursor)

        new_entities = fresh_query.fetch()
        characters_remaining = len(self.CHARACTERS) - limit - offset
        self.assertEqual(len(new_entities), characters_remaining)
        self.assertEqual(new_entities[0]['name'], 'Catelyn')
        self.assertEqual(new_entities[3]['name'], 'Arya')

    def test_query_group_by(self):
        query = self._base_query().group_by(['alive'])

        expected_matches = 2
        # We expect 2, but allow the query to get 1 extra.
        entities = query.fetch(limit=expected_matches + 1)
        self.assertEqual(len(entities), expected_matches)

        self.assertEqual(entities[0]['name'], 'Catelyn')
        self.assertEqual(entities[1]['name'], 'Arya')
