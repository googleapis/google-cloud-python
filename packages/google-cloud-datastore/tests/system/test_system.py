# Copyright 2014 Google LLC
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
import os
import unittest
import warnings

import requests
import six

from google.cloud._helpers import UTC
from google.cloud import datastore
from google.cloud.datastore.helpers import GeoPoint
from google.cloud.datastore.client import DATASTORE_DATASET
from google.cloud.exceptions import Conflict

from test_utils.system import unique_resource_id

from tests.system.utils import clear_datastore
from tests.system.utils import populate_datastore


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """

    CLIENT = None
    TO_DELETE = []


def clone_client(client):
    emulator_dataset = os.getenv(DATASTORE_DATASET)

    if emulator_dataset is None:
        return datastore.Client(
            project=client.project,
            namespace=client.namespace,
            credentials=client._credentials,
            _http=client._http,
        )
    else:
        return datastore.Client(
            project=client.project, namespace=client.namespace, _http=client._http,
        )


def setUpModule():
    emulator_dataset = os.getenv(DATASTORE_DATASET)
    # Isolated namespace so concurrent test runs don't collide.
    test_namespace = "ns" + unique_resource_id()
    if emulator_dataset is None:
        Config.CLIENT = datastore.Client(namespace=test_namespace)
    else:
        http = requests.Session()  # Un-authorized.
        Config.CLIENT = datastore.Client(
            project=emulator_dataset, namespace=test_namespace, _http=http,
        )


def tearDownModule():
    keys = [entity.key for entity in Config.TO_DELETE]
    with Config.CLIENT.transaction():
        Config.CLIENT.delete_multi(keys)


class TestDatastore(unittest.TestCase):
    def setUp(self):
        self.case_entities_to_delete = []

    def tearDown(self):
        with Config.CLIENT.transaction():
            keys = [entity.key for entity in self.case_entities_to_delete]
            Config.CLIENT.delete_multi(keys)


class TestDatastoreAllocateIDs(TestDatastore):
    def test_allocate_ids(self):
        num_ids = 10
        allocated_keys = Config.CLIENT.allocate_ids(Config.CLIENT.key("Kind"), num_ids)
        self.assertEqual(len(allocated_keys), num_ids)

        unique_ids = set()
        for key in allocated_keys:
            unique_ids.add(key.id)
            self.assertIsNone(key.name)
            self.assertNotEqual(key.id, None)

        self.assertEqual(len(unique_ids), num_ids)


class TestDatastoreReserveIDs(TestDatastore):
    def test_reserve_ids_sequential(self):
        # Smoke test to make sure it doesn't blow up. No return value or
        # verifiable side effect to verify.
        num_ids = 10
        Config.CLIENT.reserve_ids_sequential(Config.CLIENT.key("Kind", 1234), num_ids)

    def test_reserve_ids(self):
        with warnings.catch_warnings(record=True) as warned:
            num_ids = 10
            Config.CLIENT.reserve_ids(Config.CLIENT.key("Kind", 1234), num_ids)

        warned = [
            warning
            for warning in warned
            if "reserve_ids_sequential" in str(warning.message)
        ]
        assert len(warned) == 1

    def test_reserve_ids_multi(self):
        # Smoke test to make sure it doesn't blow up. No return value or
        # verifiable side effect to verify.
        keys = [Config.CLIENT.key("KIND", 1234), Config.CLIENT.key("KIND", 1235)]
        Config.CLIENT.reserve_ids_multi(keys)


class TestDatastoreSave(TestDatastore):
    @classmethod
    def setUpClass(cls):
        cls.PARENT = Config.CLIENT.key("Blog", "PizzaMan")

    def _get_post(self, id_or_name=None, post_content=None):
        post_content = post_content or {
            "title": u"How to make the perfect pizza in your grill",
            "tags": [u"pizza", u"grill"],
            "publishedAt": datetime.datetime(2001, 1, 1, tzinfo=UTC),
            "author": u"Silvano",
            "isDraft": False,
            "wordCount": 400,
            "rating": 5.0,
        }
        # Create an entity with the given content.
        # NOTE: Using a parent to ensure consistency for query
        #       in `test_empty_kind`.
        key = Config.CLIENT.key("Post", parent=self.PARENT)
        entity = datastore.Entity(key=key)
        entity.update(post_content)

        # Update the entity key.
        if id_or_name is not None:
            entity.key = entity.key.completed_key(id_or_name)

        return entity

    def _generic_test_post(self, name=None, key_id=None):
        entity = self._get_post(id_or_name=(name or key_id))
        Config.CLIENT.put(entity)

        # Register entity to be deleted.
        self.case_entities_to_delete.append(entity)

        if name is not None:
            self.assertEqual(entity.key.name, name)
        if key_id is not None:
            self.assertEqual(entity.key.id, key_id)
        retrieved_entity = Config.CLIENT.get(entity.key)
        # Check the given and retrieved are the the same.
        self.assertEqual(retrieved_entity, entity)

    def test_post_with_name(self):
        self._generic_test_post(name="post1")

    def test_post_with_id(self):
        self._generic_test_post(key_id=123456789)

    def test_post_with_generated_id(self):
        self._generic_test_post()

    def test_save_multiple(self):
        with Config.CLIENT.transaction() as xact:
            entity1 = self._get_post()
            xact.put(entity1)
            # Register entity to be deleted.
            self.case_entities_to_delete.append(entity1)

            second_post_content = {
                "title": u"How to make the perfect homemade pasta",
                "tags": [u"pasta", u"homemade"],
                "publishedAt": datetime.datetime(2001, 1, 1),
                "author": u"Silvano",
                "isDraft": False,
                "wordCount": 450,
                "rating": 4.5,
            }
            entity2 = self._get_post(post_content=second_post_content)
            xact.put(entity2)
            # Register entity to be deleted.
            self.case_entities_to_delete.append(entity2)

        keys = [entity1.key, entity2.key]
        matches = Config.CLIENT.get_multi(keys)
        self.assertEqual(len(matches), 2)

    def test_empty_kind(self):
        query = Config.CLIENT.query(kind="Post")
        query.ancestor = self.PARENT
        posts = list(query.fetch(limit=2))
        self.assertEqual(posts, [])

    def test_all_value_types(self):
        key = Config.CLIENT.key("TestPanObject", 1234)
        entity = datastore.Entity(key=key)
        entity["timestamp"] = datetime.datetime(2014, 9, 9, tzinfo=UTC)
        key_stored = Config.CLIENT.key("SavedKey", "right-here")
        entity["key"] = key_stored
        entity["truthy"] = True
        entity["float"] = 2.718281828
        entity["int"] = 3735928559
        entity["words"] = u"foo"
        entity["blob"] = b"seekretz"
        entity_stored = datastore.Entity(key=key_stored)
        entity_stored["hi"] = "bye"
        entity["nested"] = entity_stored
        entity["items"] = [1, 2, 3]
        entity["geo"] = GeoPoint(1.0, 2.0)
        entity["nothing_here"] = None

        # Store the entity.
        self.case_entities_to_delete.append(entity)
        Config.CLIENT.put(entity)

        # Check the original and retrieved are the the same.
        retrieved_entity = Config.CLIENT.get(entity.key)
        self.assertEqual(retrieved_entity, entity)


class TestDatastoreSaveKeys(TestDatastore):
    def test_save_key_self_reference(self):
        parent_key = Config.CLIENT.key("Residence", "NewYork")
        key = Config.CLIENT.key("Person", "name", parent=parent_key)
        entity = datastore.Entity(key=key)
        entity["fullName"] = u"Full name"
        entity["linkedTo"] = key  # Self reference.

        Config.CLIENT.put(entity)
        self.case_entities_to_delete.append(entity)

        query = Config.CLIENT.query(kind="Person")
        # Adding ancestor to ensure consistency.
        query.ancestor = parent_key
        query.add_filter("linkedTo", "=", key)

        stored_persons = list(query.fetch(limit=2))
        self.assertEqual(stored_persons, [entity])


class TestDatastoreQuery(TestDatastore):
    @classmethod
    def setUpClass(cls):
        cls.CLIENT = clone_client(Config.CLIENT)
        # Remove the namespace from the cloned client, since these
        # query tests rely on the entities to be already stored and indexed,
        # hence ``test_namespace`` set at runtime can't be used.
        cls.CLIENT.namespace = None

        # In the emulator, re-populating the datastore is cheap.
        if os.getenv(DATASTORE_DATASET) is not None:
            # Populate the datastore with the cloned client.
            populate_datastore.add_characters(client=cls.CLIENT)

        cls.CHARACTERS = populate_datastore.CHARACTERS
        # Use the client for this test instead of the global.
        cls.ANCESTOR_KEY = cls.CLIENT.key(*populate_datastore.ANCESTOR)

    @classmethod
    def tearDownClass(cls):
        # In the emulator, destroy the query entities.
        if os.getenv(DATASTORE_DATASET) is not None:
            # Use the client for this test instead of the global.
            clear_datastore.remove_all_entities(client=cls.CLIENT)

    def _base_query(self):
        # Use the client for this test instead of the global.
        return self.CLIENT.query(kind="Character", ancestor=self.ANCESTOR_KEY)

    def test_limit_queries(self):
        limit = 5
        query = self._base_query()

        # Fetch characters.
        iterator = query.fetch(limit=limit)
        page = six.next(iterator.pages)
        character_entities = list(page)
        cursor = iterator.next_page_token
        self.assertEqual(len(character_entities), limit)

        # Check cursor after fetch.
        self.assertIsNotNone(cursor)

        # Fetch remaining characters.
        new_character_entities = list(query.fetch(start_cursor=cursor))
        characters_remaining = len(self.CHARACTERS) - limit
        self.assertEqual(len(new_character_entities), characters_remaining)

    def test_query_simple_filter(self):
        query = self._base_query()
        query.add_filter("appearances", ">=", 20)
        expected_matches = 6
        # We expect 6, but allow the query to get 1 extra.
        entities = list(query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

    def test_query_multiple_filters(self):
        query = self._base_query()
        query.add_filter("appearances", ">=", 26)
        query.add_filter("family", "=", "Stark")
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

    def test_query_key_filter(self):
        # Use the client for this test instead of the global.
        rickard_key = self.CLIENT.key(*populate_datastore.RICKARD)

        query = self._base_query()
        query.key_filter(rickard_key)
        expected_matches = 1
        # We expect 1, but allow the query to get 1 extra.
        entities = list(query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

    def test_ordered_query(self):
        query = self._base_query()
        query.order = "appearances"
        expected_matches = 8
        # We expect 8, but allow the query to get 1 extra.
        entities = list(query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

        # Actually check the ordered data returned.
        self.assertEqual(entities[0]["name"], self.CHARACTERS[0]["name"])
        self.assertEqual(entities[7]["name"], self.CHARACTERS[3]["name"])

    def test_projection_query(self):
        filtered_query = self._base_query()
        filtered_query.projection = ["name", "family"]
        filtered_query.order = ["name", "family"]

        # NOTE: There are 9 responses because of Catelyn. She has both
        #       Stark and Tully as her families, hence occurs twice in
        #       the results.
        expected_matches = 9
        # We expect 9, but allow the query to get 1 extra.
        entities = list(filtered_query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

        arya_entity = entities[0]
        catelyn_tully_entity = entities[3]
        sansa_entity = entities[8]

        arya_dict = dict(arya_entity)
        self.assertEqual(arya_dict, {"name": "Arya", "family": "Stark"})

        catelyn_stark_entity = entities[2]
        catelyn_stark_dict = dict(catelyn_stark_entity)
        self.assertEqual(catelyn_stark_dict, {"name": "Catelyn", "family": "Stark"})

        catelyn_tully_dict = dict(catelyn_tully_entity)
        self.assertEqual(catelyn_tully_dict, {"name": "Catelyn", "family": "Tully"})

        # Check both Catelyn keys are the same.
        self.assertEqual(catelyn_stark_entity.key, catelyn_tully_entity.key)

        sansa_dict = dict(sansa_entity)
        self.assertEqual(sansa_dict, {"name": "Sansa", "family": "Stark"})

    def test_query_paginate_simple_uuid_keys(self):

        # See issue #4264
        page_query = self.CLIENT.query(kind="uuid_key")
        iterator = page_query.fetch()

        seen = set()
        page_count = 0
        for page in iterator.pages:
            page_count += 1
            for entity in page:
                uuid_str = entity.key.name
                self.assertNotIn(uuid_str, seen, uuid_str)
                seen.add(uuid_str)

        self.assertTrue(page_count > 1)

    def test_query_paginate_simple_timestamp_keys(self):

        # See issue #4264
        page_query = self.CLIENT.query(kind="timestamp_key")
        iterator = page_query.fetch()

        seen = set()
        page_count = 0
        for page in iterator.pages:
            page_count += 1
            for entity in page:
                timestamp = entity.key.id
                self.assertNotIn(timestamp, seen, timestamp)
                seen.add(timestamp)

        self.assertTrue(page_count > 1)

    def test_query_offset_timestamp_keys(self):
        # See issue #4675
        max_all = 10000
        offset = 1
        max_offset = max_all - offset
        query = self.CLIENT.query(kind="timestamp_key")
        all_w_limit = list(query.fetch(limit=max_all))
        self.assertEqual(len(all_w_limit), max_all)

        offset_w_limit = list(query.fetch(offset=offset, limit=max_offset))
        self.assertEqual(offset_w_limit, all_w_limit[offset:])

    def test_query_paginate_with_offset(self):
        page_query = self._base_query()
        page_query.order = "appearances"
        offset = 2
        limit = 3
        iterator = page_query.fetch(limit=limit, offset=offset)

        # Fetch characters.
        page = six.next(iterator.pages)
        entities = list(page)
        cursor = iterator.next_page_token
        self.assertEqual(len(entities), limit)
        self.assertEqual(entities[0]["name"], "Robb")
        self.assertEqual(entities[1]["name"], "Bran")
        self.assertEqual(entities[2]["name"], "Catelyn")

        # Fetch next set of characters.
        new_iterator = page_query.fetch(limit=limit, offset=0, start_cursor=cursor)
        entities = list(new_iterator)
        self.assertEqual(len(entities), limit)
        self.assertEqual(entities[0]["name"], "Sansa")
        self.assertEqual(entities[1]["name"], "Jon Snow")
        self.assertEqual(entities[2]["name"], "Arya")

    def test_query_paginate_with_start_cursor(self):
        page_query = self._base_query()
        page_query.order = "appearances"
        limit = 3
        offset = 2
        iterator = page_query.fetch(limit=limit, offset=offset)

        # Fetch characters.
        page = six.next(iterator.pages)
        entities = list(page)
        cursor = iterator.next_page_token
        self.assertEqual(len(entities), limit)

        # Use cursor to create a fresh query.
        fresh_query = self._base_query()
        fresh_query.order = "appearances"

        new_entities = list(fresh_query.fetch(start_cursor=cursor, limit=limit))
        characters_remaining = len(self.CHARACTERS) - limit - offset
        self.assertEqual(len(new_entities), characters_remaining)
        self.assertEqual(new_entities[0]["name"], "Sansa")
        self.assertEqual(new_entities[2]["name"], "Arya")

    def test_query_distinct_on(self):
        query = self._base_query()
        query.distinct_on = ["alive"]

        expected_matches = 2
        # We expect 2, but allow the query to get 1 extra.
        entities = list(query.fetch(limit=expected_matches + 1))
        self.assertEqual(len(entities), expected_matches)

        self.assertEqual(entities[0]["name"], "Catelyn")
        self.assertEqual(entities[1]["name"], "Arya")


class TestDatastoreQueryOffsets(TestDatastore):
    TOTAL_OBJECTS = 2500
    NAMESPACE = "LargeCharacterEntity"
    KIND = "LargeCharacter"

    @classmethod
    def setUpClass(cls):
        cls.CLIENT = clone_client(Config.CLIENT)
        # Remove the namespace from the cloned client, since these
        # query tests rely on the entities to be already stored
        # cls.CLIENT.namespace = cls.NAMESPACE
        cls.CLIENT.namespace = None

        # Populating the datastore if necessary.
        populate_datastore.add_large_character_entities(client=cls.CLIENT)

    @classmethod
    def tearDownClass(cls):
        # In the emulator, destroy the query entities.
        if os.getenv(DATASTORE_DATASET) is not None:
            # Use the client for this test instead of the global.
            clear_datastore.remove_all_entities(client=cls.CLIENT)

    def _base_query(self):
        # Use the client for this test instead of the global.
        return self.CLIENT.query(kind=self.KIND, namespace=self.NAMESPACE)

    def _verify(self, limit, offset, expected):
        # Query used for all tests
        page_query = self._base_query()
        page_query.add_filter("family", "=", "Stark")
        page_query.add_filter("alive", "=", False)

        iterator = page_query.fetch(limit=limit, offset=offset)
        entities = [e for e in iterator]
        self.assertEqual(len(entities), expected)

    def test_query_in_bounds_offsets(self):
        # Verify that with no offset there are the correct # of results
        self._verify(limit=None, offset=None, expected=self.TOTAL_OBJECTS)

        # Verify that with no limit there are results (offset provided)")
        self._verify(limit=None, offset=900, expected=self.TOTAL_OBJECTS - 900)

        # Offset beyond items larger Verify 200 items found")
        self._verify(limit=200, offset=1100, expected=200)

    def test_query_partially_out_of_bounds_offsets(self):
        # Offset within range, expect 50 despite larger limit")
        self._verify(limit=100, offset=self.TOTAL_OBJECTS - 50, expected=50)

    def test_query_out_of_bounds_offsets(self):
        # Offset beyond items larger Verify no items found")
        self._verify(limit=200, offset=self.TOTAL_OBJECTS + 1000, expected=0)


class TestDatastoreTransaction(TestDatastore):
    def test_transaction_via_with_statement(self):
        entity = datastore.Entity(key=Config.CLIENT.key("Company", "Google"))
        entity["url"] = u"www.google.com"

        with Config.CLIENT.transaction() as xact:
            result = Config.CLIENT.get(entity.key)
            if result is None:
                xact.put(entity)
                self.case_entities_to_delete.append(entity)

        # This will always return after the transaction.
        retrieved_entity = Config.CLIENT.get(entity.key)
        self.case_entities_to_delete.append(retrieved_entity)
        self.assertEqual(retrieved_entity, entity)

    def test_transaction_via_explicit_begin_get_commit(self):
        # See
        # github.com/GoogleCloudPlatform/google-cloud-python/issues/1859
        # Note that this example lacks the threading which provokes the race
        # condition in that issue:  we are basically just exercising the
        # "explict" path for using transactions.
        BEFORE_1 = 100
        BEFORE_2 = 0
        TRANSFER_AMOUNT = 40
        key1 = Config.CLIENT.key("account", "123")
        account1 = datastore.Entity(key=key1)
        account1["balance"] = BEFORE_1
        key2 = Config.CLIENT.key("account", "234")
        account2 = datastore.Entity(key=key2)
        account2["balance"] = BEFORE_2
        Config.CLIENT.put_multi([account1, account2])
        self.case_entities_to_delete.append(account1)
        self.case_entities_to_delete.append(account2)

        xact = Config.CLIENT.transaction()
        xact.begin()
        from_account = Config.CLIENT.get(key1, transaction=xact)
        to_account = Config.CLIENT.get(key2, transaction=xact)
        from_account["balance"] -= TRANSFER_AMOUNT
        to_account["balance"] += TRANSFER_AMOUNT

        xact.put(from_account)
        xact.put(to_account)
        xact.commit()

        after1 = Config.CLIENT.get(key1)
        after2 = Config.CLIENT.get(key2)
        self.assertEqual(after1["balance"], BEFORE_1 - TRANSFER_AMOUNT)
        self.assertEqual(after2["balance"], BEFORE_2 + TRANSFER_AMOUNT)

    def test_failure_with_contention(self):
        contention_prop_name = "baz"
        local_client = clone_client(Config.CLIENT)

        # Insert an entity which will be retrieved in a transaction
        # and updated outside it with a contentious value.
        key = local_client.key("BreakTxn", 1234)
        orig_entity = datastore.Entity(key=key)
        orig_entity["foo"] = u"bar"
        local_client.put(orig_entity)
        self.case_entities_to_delete.append(orig_entity)

        with self.assertRaises(Conflict):
            with local_client.transaction() as txn:
                entity_in_txn = local_client.get(key)

                # Update the original entity outside the transaction.
                orig_entity[contention_prop_name] = u"outside"
                Config.CLIENT.put(orig_entity)

                # Try to update the entity which we already updated outside the
                # transaction.
                entity_in_txn[contention_prop_name] = u"inside"
                txn.put(entity_in_txn)

    def test_empty_array_put(self):
        local_client = clone_client(Config.CLIENT)

        key = local_client.key("EmptyArray", 1234)
        local_client = datastore.Client()
        entity = datastore.Entity(key=key)
        entity["children"] = []
        local_client.put(entity)
        retrieved = local_client.get(entity.key)

        self.assertEqual(entity["children"], retrieved["children"])
