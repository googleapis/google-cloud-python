import datetime
import pytz
import unittest2

from gcloud import datastore
# This assumes the command is being run via tox hence the
# repository root is the current directory.
from regression import regression_utils


class TestDatastore(unittest2.TestCase):

    def setUp(self):
        environ = regression_utils.get_environ()
        self._dataset_id = environ['dataset_id']
        self._client_email = environ['client_email']
        self._key_filename = environ['key_filename']
        self._datasets = {}

        self.entities_to_delete = []

    def tearDown(self):
        for entity in self.entities_to_delete:
            entity.delete()

    def _get_dataset(self):
        if self._dataset_id not in self._datasets:
            self._datasets[self._dataset_id] = datastore.get_dataset(
                self._dataset_id, self._client_email, self._key_filename)
        return self._datasets[self._dataset_id]

    def _get_post(self, name=None, key_id=None, post_content=None):
        from gcloud.datastore.entity import Entity
        post_content = post_content or {
            'title': 'How to make the perfect pizza in your grill',
            'tags': ['pizza', 'grill'],
            # NOTE: We don't support datetime.date, but should.
            # NOTE: Without a tz, assertEqual fails with
            #     "can't compare offset-naive and offset-aware datetimes"
            'publishedAt': datetime.datetime(2001, 1, 1, tzinfo=pytz.utc),
            'author': 'Silvano',
            'isDraft': False,
            'wordCount': 400,
            'rating': 5.0,
        }
        # Create an entity with the given content in our dataset.
        dataset = self._get_dataset()
        entity = Entity(dataset, 'Post')
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
        self.entities_to_delete.append(entity)

        if name is not None:
            self.assertEqual(entity.key().name(), name)
        if key_id is not None:
            self.assertEqual(entity.key().id(), key_id)
        retrieved_entity = self._get_dataset().get_entity(entity.key())
        # Check the keys are the same.
        self.assertEqual(retrieved_entity.key().path(),
                         entity.key().path())
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
        dataset = self._get_dataset()
        with dataset.transaction():
            entity1 = self._get_post()
            entity1.save()
            # Register entity to be deleted.
            self.entities_to_delete.append(entity1)

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
            self.entities_to_delete.append(entity2)

        keys = [entity1.key(), entity2.key()]
        matches = dataset.get_entities(keys)
        self.assertEqual(len(matches), 2)

    def test_empty_kind(self):
        from gcloud.datastore.query import Query
        dataset = self._get_dataset()
        posts = Query(dataset=dataset).kind('Post').limit(2).fetch()
        self.assertEqual(posts, [])
