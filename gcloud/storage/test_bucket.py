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

import unittest2


class Test__BlobIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.bucket import _BlobIterator
        return _BlobIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket()
        iterator = self._makeOne(bucket, client=client)
        self.assertTrue(iterator.bucket is bucket)
        self.assertTrue(iterator.client is client)
        self.assertEqual(iterator.path, '%s/o' % bucket.path)
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)
        self.assertEqual(iterator.prefixes, set())

    def test_get_items_from_response_empty(self):
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket()
        iterator = self._makeOne(bucket, client=client)
        blobs = list(iterator.get_items_from_response({}))
        self.assertEqual(blobs, [])
        self.assertEqual(iterator.prefixes, set())

    def test_get_items_from_response_non_empty(self):
        from gcloud.storage.blob import Blob
        BLOB_NAME = 'blob-name'
        response = {'items': [{'name': BLOB_NAME}], 'prefixes': ['foo']}
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket()
        iterator = self._makeOne(bucket, client=client)
        blobs = list(iterator.get_items_from_response(response))
        self.assertEqual(len(blobs), 1)
        blob = blobs[0]
        self.assertTrue(isinstance(blob, Blob))
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(iterator.prefixes, set(['foo']))

    def test_get_items_from_response_cumulative_prefixes(self):
        from gcloud.storage.blob import Blob
        BLOB_NAME = 'blob-name1'
        response1 = {'items': [{'name': BLOB_NAME}], 'prefixes': ['foo']}
        response2 = {
            'items': [],
            'prefixes': ['foo', 'bar'],
        }
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket()
        iterator = self._makeOne(bucket, client=client)
        # Parse first response.
        blobs = list(iterator.get_items_from_response(response1))
        self.assertEqual(len(blobs), 1)
        blob = blobs[0]
        self.assertTrue(isinstance(blob, Blob))
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(iterator.prefixes, set(['foo']))
        # Parse second response.
        blobs = list(iterator.get_items_from_response(response2))
        self.assertEqual(len(blobs), 0)
        self.assertEqual(iterator.prefixes, set(['foo', 'bar']))


class Test_Bucket(unittest2.TestCase):

    def _makeOne(self, client=None, name=None, properties=None):
        from gcloud.storage.bucket import Bucket
        if client is None:
            connection = _Connection()
            client = _Client(connection)
        bucket = Bucket(client, name=name)
        bucket._properties = properties or {}
        return bucket

    def test_ctor(self):
        NAME = 'name'
        properties = {'key': 'value'}
        bucket = self._makeOne(name=NAME, properties=properties)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket._properties, properties)
        self.assertFalse(bucket._acl.loaded)
        self.assertTrue(bucket._acl.bucket is bucket)
        self.assertFalse(bucket._default_object_acl.loaded)
        self.assertTrue(bucket._default_object_acl.bucket is bucket)

    def test_blob(self):
        from gcloud.storage.blob import Blob

        BUCKET_NAME = 'BUCKET_NAME'
        BLOB_NAME = 'BLOB_NAME'
        CHUNK_SIZE = 1024 * 1024

        bucket = self._makeOne(name=BUCKET_NAME)
        blob = bucket.blob(BLOB_NAME, chunk_size=CHUNK_SIZE)
        self.assertTrue(isinstance(blob, Blob))
        self.assertTrue(blob.bucket is bucket)
        self.assertTrue(blob.client is bucket.client)
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(blob.chunk_size, CHUNK_SIZE)

    def test_exists_miss(self):
        from gcloud.exceptions import NotFound

        class _FakeConnection(object):

            _called_with = []

            @classmethod
            def api_request(cls, *args, **kwargs):
                cls._called_with.append((args, kwargs))
                raise NotFound(args)

        BUCKET_NAME = 'bucket-name'
        bucket = self._makeOne(name=BUCKET_NAME)
        client = _Client(_FakeConnection)
        self.assertFalse(bucket.exists(client=client))
        expected_called_kwargs = {
            'method': 'GET',
            'path': bucket.path,
            'query_params': {
                'fields': 'name',
            },
            '_target_object': None,
        }
        expected_cw = [((), expected_called_kwargs)]
        self.assertEqual(_FakeConnection._called_with, expected_cw)

    def test_exists_hit(self):
        class _FakeConnection(object):

            _called_with = []

            @classmethod
            def api_request(cls, *args, **kwargs):
                cls._called_with.append((args, kwargs))
                # exists() does not use the return value
                return object()

        BUCKET_NAME = 'bucket-name'
        bucket = self._makeOne(name=BUCKET_NAME)
        client = _Client(_FakeConnection)
        self.assertTrue(bucket.exists(client=client))
        expected_called_kwargs = {
            'method': 'GET',
            'path': bucket.path,
            'query_params': {
                'fields': 'name',
            },
            '_target_object': None,
        }
        expected_cw = [((), expected_called_kwargs)]
        self.assertEqual(_FakeConnection._called_with, expected_cw)

    def test_create_hit(self):
        BUCKET_NAME = 'bucket-name'
        DATA = {'name': BUCKET_NAME}
        connection = _Connection(DATA)
        PROJECT = 'PROJECT'
        client = _Client(connection, project=PROJECT)
        bucket = self._makeOne(client=client, name=BUCKET_NAME)
        bucket.create()

        kw, = connection._requested
        self.assertEqual(kw['method'], 'POST')
        self.assertEqual(kw['path'], '/b')
        self.assertEqual(kw['query_params'], {'project': PROJECT})
        self.assertEqual(kw['data'], DATA)

    def test_create_w_extra_properties(self):
        BUCKET_NAME = 'bucket-name'
        PROJECT = 'PROJECT'
        CORS = [{
            'maxAgeSeconds': 60,
            'methods': ['*'],
            'origin': ['https://example.com/frontend'],
            'responseHeader': ['X-Custom-Header'],
        }]
        LIFECYCLE_RULES = [{
            "action": {"type": "Delete"},
            "condition": {"age": 365}
        }]
        LOCATION = 'eu'
        STORAGE_CLASS = 'NEARLINE'
        DATA = {
            'name': BUCKET_NAME,
            'cors': CORS,
            'lifecycle': {'rule': LIFECYCLE_RULES},
            'location': LOCATION,
            'storageClass': STORAGE_CLASS,
            'versioning': {'enabled': True},
        }
        connection = _Connection(DATA)
        client = _Client(connection, project=PROJECT)
        bucket = self._makeOne(client=client, name=BUCKET_NAME)
        bucket.cors = CORS
        bucket.lifecycle_rules = LIFECYCLE_RULES
        bucket.location = LOCATION
        bucket.storage_class = STORAGE_CLASS
        bucket.versioning_enabled = True
        bucket.create()

        kw, = connection._requested
        self.assertEqual(kw['method'], 'POST')
        self.assertEqual(kw['path'], '/b')
        self.assertEqual(kw['query_params'], {'project': PROJECT})
        self.assertEqual(kw['data'], DATA)

    def test_acl_property(self):
        from gcloud.storage.acl import BucketACL
        bucket = self._makeOne()
        acl = bucket.acl
        self.assertTrue(isinstance(acl, BucketACL))
        self.assertTrue(acl is bucket._acl)

    def test_default_object_acl_property(self):
        from gcloud.storage.acl import DefaultObjectACL
        bucket = self._makeOne()
        acl = bucket.default_object_acl
        self.assertTrue(isinstance(acl, DefaultObjectACL))
        self.assertTrue(acl is bucket._default_object_acl)

    def test_path_no_name(self):
        bucket = self._makeOne()
        self.assertRaises(ValueError, getattr, bucket, 'path')

    def test_path_w_name(self):
        NAME = 'name'
        bucket = self._makeOne(name=NAME)
        self.assertEqual(bucket.path, '/b/%s' % NAME)

    def test_get_blob_miss(self):
        NAME = 'name'
        NONESUCH = 'nonesuch'
        connection = _Connection()
        client = _Client(connection)
        bucket = self._makeOne(name=NAME)
        result = bucket.get_blob(NONESUCH, client=client)
        self.assertTrue(result is None)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_get_blob_hit(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        connection = _Connection({'name': BLOB_NAME})
        client = _Client(connection)
        bucket = self._makeOne(name=NAME)
        blob = bucket.get_blob(BLOB_NAME, client=client)
        self.assertTrue(blob.bucket is bucket)
        self.assertEqual(blob.name, BLOB_NAME)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, BLOB_NAME))

    def test_list_blobs_defaults(self):
        NAME = 'name'
        connection = _Connection({'items': []})
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        iterator = bucket.list_blobs()
        blobs = list(iterator)
        self.assertEqual(blobs, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {'projection': 'noAcl'})

    def test_list_blobs_w_all_arguments(self):
        NAME = 'name'
        MAX_RESULTS = 10
        PAGE_TOKEN = 'ABCD'
        PREFIX = 'subfolder'
        DELIMITER = '/'
        VERSIONS = True
        PROJECTION = 'full'
        FIELDS = 'items/contentLanguage,nextPageToken'
        EXPECTED = {
            'maxResults': 10,
            'pageToken': PAGE_TOKEN,
            'prefix': PREFIX,
            'delimiter': DELIMITER,
            'versions': VERSIONS,
            'projection': PROJECTION,
            'fields': FIELDS,
        }
        connection = _Connection({'items': []})
        client = _Client(connection)
        bucket = self._makeOne(name=NAME)
        iterator = bucket.list_blobs(
            max_results=MAX_RESULTS,
            page_token=PAGE_TOKEN,
            prefix=PREFIX,
            delimiter=DELIMITER,
            versions=VERSIONS,
            projection=PROJECTION,
            fields=FIELDS,
            client=client,
        )
        blobs = list(iterator)
        self.assertEqual(blobs, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], EXPECTED)

    def test_list_blobs(self):
        NAME = 'name'
        connection = _Connection({'items': []})
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        iterator = bucket.list_blobs()
        blobs = list(iterator)
        self.assertEqual(blobs, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {'projection': 'noAcl'})

    def test_delete_miss(self):
        from gcloud.exceptions import NotFound
        NAME = 'name'
        connection = _Connection()
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        self.assertRaises(NotFound, bucket.delete)
        expected_cw = [{
            'method': 'DELETE',
            'path': bucket.path,
            '_target_object': None,
        }]
        self.assertEqual(connection._deleted_buckets, expected_cw)

    def test_delete_hit(self):
        NAME = 'name'
        GET_BLOBS_RESP = {'items': []}
        connection = _Connection(GET_BLOBS_RESP)
        connection._delete_bucket = True
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        result = bucket.delete(force=True)
        self.assertTrue(result is None)
        expected_cw = [{
            'method': 'DELETE',
            'path': bucket.path,
            '_target_object': None,
        }]
        self.assertEqual(connection._deleted_buckets, expected_cw)

    def test_delete_force_delete_blobs(self):
        NAME = 'name'
        BLOB_NAME1 = 'blob-name1'
        BLOB_NAME2 = 'blob-name2'
        GET_BLOBS_RESP = {
            'items': [
                {'name': BLOB_NAME1},
                {'name': BLOB_NAME2},
            ],
        }
        DELETE_BLOB1_RESP = DELETE_BLOB2_RESP = {}
        connection = _Connection(GET_BLOBS_RESP, DELETE_BLOB1_RESP,
                                 DELETE_BLOB2_RESP)
        connection._delete_bucket = True
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        result = bucket.delete(force=True)
        self.assertTrue(result is None)
        expected_cw = [{
            'method': 'DELETE',
            'path': bucket.path,
            '_target_object': None,
        }]
        self.assertEqual(connection._deleted_buckets, expected_cw)

    def test_delete_force_miss_blobs(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name1'
        GET_BLOBS_RESP = {'items': [{'name': BLOB_NAME}]}
        # Note the connection does not have a response for the blob.
        connection = _Connection(GET_BLOBS_RESP)
        connection._delete_bucket = True
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        result = bucket.delete(force=True)
        self.assertTrue(result is None)
        expected_cw = [{
            'method': 'DELETE',
            'path': bucket.path,
            '_target_object': None,
        }]
        self.assertEqual(connection._deleted_buckets, expected_cw)

    def test_delete_too_many(self):
        NAME = 'name'
        BLOB_NAME1 = 'blob-name1'
        BLOB_NAME2 = 'blob-name2'
        GET_BLOBS_RESP = {
            'items': [
                {'name': BLOB_NAME1},
                {'name': BLOB_NAME2},
            ],
        }
        connection = _Connection(GET_BLOBS_RESP)
        connection._delete_bucket = True
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)

        # Make the Bucket refuse to delete with 2 objects.
        bucket._MAX_OBJECTS_FOR_ITERATION = 1
        self.assertRaises(ValueError, bucket.delete, force=True)
        self.assertEqual(connection._deleted_buckets, [])

    def test_delete_blob_miss(self):
        from gcloud.exceptions import NotFound
        NAME = 'name'
        NONESUCH = 'nonesuch'
        connection = _Connection()
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        self.assertRaises(NotFound, bucket.delete_blob, NONESUCH)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'DELETE')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_delete_blob_hit(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        connection = _Connection({})
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        result = bucket.delete_blob(BLOB_NAME)
        self.assertTrue(result is None)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'DELETE')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, BLOB_NAME))

    def test_delete_blobs_empty(self):
        NAME = 'name'
        connection = _Connection()
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        bucket.delete_blobs([])
        self.assertEqual(connection._requested, [])

    def test_delete_blobs_hit(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        connection = _Connection({})
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        bucket.delete_blobs([BLOB_NAME])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'DELETE')
        self.assertEqual(kw[0]['path'], '/b/%s/o/%s' % (NAME, BLOB_NAME))

    def test_delete_blobs_miss_no_on_error(self):
        from gcloud.exceptions import NotFound
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        NONESUCH = 'nonesuch'
        connection = _Connection({})
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        self.assertRaises(NotFound, bucket.delete_blobs, [BLOB_NAME, NONESUCH])
        kw = connection._requested
        self.assertEqual(len(kw), 2)
        self.assertEqual(kw[0]['method'], 'DELETE')
        self.assertEqual(kw[0]['path'], '/b/%s/o/%s' % (NAME, BLOB_NAME))
        self.assertEqual(kw[1]['method'], 'DELETE')
        self.assertEqual(kw[1]['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_delete_blobs_miss_w_on_error(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        NONESUCH = 'nonesuch'
        connection = _Connection({})
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        errors = []
        bucket.delete_blobs([BLOB_NAME, NONESUCH], errors.append)
        self.assertEqual(errors, [NONESUCH])
        kw = connection._requested
        self.assertEqual(len(kw), 2)
        self.assertEqual(kw[0]['method'], 'DELETE')
        self.assertEqual(kw[0]['path'], '/b/%s/o/%s' % (NAME, BLOB_NAME))
        self.assertEqual(kw[1]['method'], 'DELETE')
        self.assertEqual(kw[1]['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_copy_blobs_wo_name(self):
        SOURCE = 'source'
        DEST = 'dest'
        BLOB_NAME = 'blob-name'

        class _Blob(object):
            name = BLOB_NAME
            path = '/b/%s/o/%s' % (SOURCE, BLOB_NAME)

        connection = _Connection({})
        client = _Client(connection)
        source = self._makeOne(client=client, name=SOURCE)
        dest = self._makeOne(client=client, name=DEST)
        blob = _Blob()
        new_blob = source.copy_blob(blob, dest)
        self.assertTrue(new_blob.bucket is dest)
        self.assertEqual(new_blob.name, BLOB_NAME)
        kw, = connection._requested
        COPY_PATH = '/b/%s/o/%s/copyTo/b/%s/o/%s' % (SOURCE, BLOB_NAME,
                                                     DEST, BLOB_NAME)
        self.assertEqual(kw['method'], 'POST')
        self.assertEqual(kw['path'], COPY_PATH)

    def test_copy_blobs_w_name(self):
        SOURCE = 'source'
        DEST = 'dest'
        BLOB_NAME = 'blob-name'
        NEW_NAME = 'new_name'

        class _Blob(object):
            name = BLOB_NAME
            path = '/b/%s/o/%s' % (SOURCE, BLOB_NAME)

        connection = _Connection({})
        client = _Client(connection)
        source = self._makeOne(client=client, name=SOURCE)
        dest = self._makeOne(client=client, name=DEST)
        blob = _Blob()
        new_blob = source.copy_blob(blob, dest, NEW_NAME)
        self.assertTrue(new_blob.bucket is dest)
        self.assertEqual(new_blob.name, NEW_NAME)
        kw, = connection._requested
        COPY_PATH = '/b/%s/o/%s/copyTo/b/%s/o/%s' % (SOURCE, BLOB_NAME,
                                                     DEST, NEW_NAME)
        self.assertEqual(kw['method'], 'POST')
        self.assertEqual(kw['path'], COPY_PATH)

    def test_rename_blob(self):
        BUCKET_NAME = 'BUCKET_NAME'
        BLOB_NAME = 'blob-name'
        NEW_BLOB_NAME = 'new-blob-name'

        DATA = {'name': NEW_BLOB_NAME}
        connection = _Connection(DATA)
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=BUCKET_NAME)

        class _Blob(object):

            def __init__(self, name, bucket_name):
                self.name = name
                self.path = '/b/%s/o/%s' % (bucket_name, name)
                self._deleted = []

            def delete(self, client=None):
                self._deleted.append(client)

        blob = _Blob(BLOB_NAME, BUCKET_NAME)
        renamed_blob = bucket.rename_blob(blob, NEW_BLOB_NAME, client=client)
        self.assertTrue(renamed_blob.bucket is bucket)
        self.assertEqual(renamed_blob.name, NEW_BLOB_NAME)
        self.assertEqual(blob._deleted, [client])

    def test_etag(self):
        ETAG = 'ETAG'
        properties = {'etag': ETAG}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.etag, ETAG)

    def test_id(self):
        ID = 'ID'
        properties = {'id': ID}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.id, ID)

    def test_location_getter(self):
        NAME = 'name'
        before = {'location': 'AS'}
        bucket = self._makeOne(name=NAME, properties=before)
        self.assertEqual(bucket.location, 'AS')

    def test_location_setter(self):
        NAME = 'name'
        bucket = self._makeOne(name=NAME)
        self.assertEqual(bucket.location, None)
        bucket.location = 'AS'
        self.assertEqual(bucket.location, 'AS')
        self.assertTrue('location' in bucket._changes)

    def test_lifecycle_rules_getter(self):
        NAME = 'name'
        LC_RULE = {'action': {'type': 'Delete'}, 'condition': {'age': 42}}
        rules = [LC_RULE]
        properties = {'lifecycle': {'rule': rules}}
        bucket = self._makeOne(name=NAME, properties=properties)
        self.assertEqual(bucket.lifecycle_rules, rules)
        # Make sure it's a copy
        self.assertFalse(bucket.lifecycle_rules is rules)

    def test_lifecycle_rules_setter(self):
        NAME = 'name'
        LC_RULE = {'action': {'type': 'Delete'}, 'condition': {'age': 42}}
        rules = [LC_RULE]
        bucket = self._makeOne(name=NAME)
        self.assertEqual(bucket.lifecycle_rules, [])
        bucket.lifecycle_rules = rules
        self.assertEqual(bucket.lifecycle_rules, rules)
        self.assertTrue('lifecycle' in bucket._changes)

    def test_cors_getter(self):
        NAME = 'name'
        CORS_ENTRY = {
            'maxAgeSeconds': 1234,
            'method': ['OPTIONS', 'GET'],
            'origin': ['127.0.0.1'],
            'responseHeader': ['Content-Type'],
        }
        properties = {'cors': [CORS_ENTRY, {}]}
        bucket = self._makeOne(name=NAME, properties=properties)
        entries = bucket.cors
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0], CORS_ENTRY)
        self.assertEqual(entries[1], {})
        # Make sure it was a copy, not the same object.
        self.assertFalse(entries[0] is CORS_ENTRY)

    def test_cors_setter(self):
        NAME = 'name'
        CORS_ENTRY = {
            'maxAgeSeconds': 1234,
            'method': ['OPTIONS', 'GET'],
            'origin': ['127.0.0.1'],
            'responseHeader': ['Content-Type'],
        }
        bucket = self._makeOne(name=NAME)

        self.assertEqual(bucket.cors, [])
        bucket.cors = [CORS_ENTRY]
        self.assertEqual(bucket.cors, [CORS_ENTRY])
        self.assertTrue('cors' in bucket._changes)

    def test_get_logging_w_prefix(self):
        NAME = 'name'
        LOG_BUCKET = 'logs'
        LOG_PREFIX = 'pfx'
        before = {
            'logging': {
                'logBucket': LOG_BUCKET,
                'logObjectPrefix': LOG_PREFIX,
            },
        }
        bucket = self._makeOne(name=NAME, properties=before)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info['logObjectPrefix'], LOG_PREFIX)

    def test_enable_logging_defaults(self):
        NAME = 'name'
        LOG_BUCKET = 'logs'
        before = {'logging': None}
        bucket = self._makeOne(name=NAME, properties=before)
        self.assertTrue(bucket.get_logging() is None)
        bucket.enable_logging(LOG_BUCKET)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info['logObjectPrefix'], '')

    def test_enable_logging(self):
        NAME = 'name'
        LOG_BUCKET = 'logs'
        LOG_PFX = 'pfx'
        before = {'logging': None}
        bucket = self._makeOne(name=NAME, properties=before)
        self.assertTrue(bucket.get_logging() is None)
        bucket.enable_logging(LOG_BUCKET, LOG_PFX)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info['logObjectPrefix'], LOG_PFX)

    def test_disable_logging(self):
        NAME = 'name'
        before = {'logging': {'logBucket': 'logs', 'logObjectPrefix': 'pfx'}}
        bucket = self._makeOne(name=NAME, properties=before)
        self.assertTrue(bucket.get_logging() is not None)
        bucket.disable_logging()
        self.assertTrue(bucket.get_logging() is None)

    def test_metageneration(self):
        METAGENERATION = 42
        properties = {'metageneration': METAGENERATION}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.metageneration, METAGENERATION)

    def test_metageneration_unset(self):
        bucket = self._makeOne()
        self.assertEqual(bucket.metageneration, None)

    def test_metageneration_string_val(self):
        METAGENERATION = 42
        properties = {'metageneration': str(METAGENERATION)}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.metageneration, METAGENERATION)

    def test_owner(self):
        OWNER = {'entity': 'project-owner-12345', 'entityId': '23456'}
        properties = {'owner': OWNER}
        bucket = self._makeOne(properties=properties)
        owner = bucket.owner
        self.assertEqual(owner['entity'], 'project-owner-12345')
        self.assertEqual(owner['entityId'], '23456')

    def test_project_number(self):
        PROJECT_NUMBER = 12345
        properties = {'projectNumber': PROJECT_NUMBER}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.project_number, PROJECT_NUMBER)

    def test_project_number_unset(self):
        bucket = self._makeOne()
        self.assertEqual(bucket.project_number, None)

    def test_project_number_string_val(self):
        PROJECT_NUMBER = 12345
        properties = {'projectNumber': str(PROJECT_NUMBER)}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.project_number, PROJECT_NUMBER)

    def test_self_link(self):
        SELF_LINK = 'http://example.com/self/'
        properties = {'selfLink': SELF_LINK}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.self_link, SELF_LINK)

    def test_storage_class_getter(self):
        STORAGE_CLASS = 'http://example.com/self/'
        properties = {'storageClass': STORAGE_CLASS}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.storage_class, STORAGE_CLASS)

    def test_storage_class_setter_invalid(self):
        NAME = 'name'
        bucket = self._makeOne(name=NAME)
        with self.assertRaises(ValueError):
            bucket.storage_class = 'BOGUS'
        self.assertFalse('storageClass' in bucket._changes)

    def test_storage_class_setter_STANDARD(self):
        NAME = 'name'
        bucket = self._makeOne(name=NAME)
        bucket.storage_class = 'STANDARD'
        self.assertEqual(bucket.storage_class, 'STANDARD')
        self.assertTrue('storageClass' in bucket._changes)

    def test_storage_class_setter_NEARLINE(self):
        NAME = 'name'
        bucket = self._makeOne(name=NAME)
        bucket.storage_class = 'NEARLINE'
        self.assertEqual(bucket.storage_class, 'NEARLINE')
        self.assertTrue('storageClass' in bucket._changes)

    def test_storage_class_setter_DURABLE_REDUCED_AVAILABILITY(self):
        NAME = 'name'
        bucket = self._makeOne(name=NAME)
        bucket.storage_class = 'DURABLE_REDUCED_AVAILABILITY'
        self.assertEqual(bucket.storage_class, 'DURABLE_REDUCED_AVAILABILITY')
        self.assertTrue('storageClass' in bucket._changes)

    def test_time_created(self):
        import datetime
        from gcloud._helpers import _RFC3339_MICROS
        from gcloud._helpers import UTC
        TIMESTAMP = datetime.datetime(2014, 11, 5, 20, 34, 37, tzinfo=UTC)
        TIME_CREATED = TIMESTAMP.strftime(_RFC3339_MICROS)
        properties = {'timeCreated': TIME_CREATED}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.time_created, TIMESTAMP)

    def test_time_created_unset(self):
        bucket = self._makeOne()
        self.assertEqual(bucket.time_created, None)

    def test_versioning_enabled_getter_missing(self):
        NAME = 'name'
        bucket = self._makeOne(name=NAME)
        self.assertEqual(bucket.versioning_enabled, False)

    def test_versioning_enabled_getter(self):
        NAME = 'name'
        before = {'versioning': {'enabled': True}}
        bucket = self._makeOne(name=NAME, properties=before)
        self.assertEqual(bucket.versioning_enabled, True)

    def test_versioning_enabled_setter(self):
        NAME = 'name'
        bucket = self._makeOne(name=NAME)
        self.assertFalse(bucket.versioning_enabled)
        bucket.versioning_enabled = True
        self.assertTrue(bucket.versioning_enabled)

    def test_configure_website_defaults(self):
        NAME = 'name'
        UNSET = {'website': {'mainPageSuffix': None,
                             'notFoundPage': None}}
        bucket = self._makeOne(name=NAME)
        bucket.configure_website()
        self.assertEqual(bucket._properties, UNSET)

    def test_configure_website(self):
        NAME = 'name'
        WEBSITE_VAL = {'website': {'mainPageSuffix': 'html',
                                   'notFoundPage': '404.html'}}
        bucket = self._makeOne(name=NAME)
        bucket.configure_website('html', '404.html')
        self.assertEqual(bucket._properties, WEBSITE_VAL)

    def test_disable_website(self):
        NAME = 'name'
        UNSET = {'website': {'mainPageSuffix': None,
                             'notFoundPage': None}}
        bucket = self._makeOne(name=NAME)
        bucket.disable_website()
        self.assertEqual(bucket._properties, UNSET)

    def test_make_public_defaults(self):
        from gcloud.storage.acl import _ACLEntity
        NAME = 'name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive, 'defaultObjectAcl': []}
        connection = _Connection(after)
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        bucket.acl.loaded = True
        bucket.default_object_acl.loaded = True
        bucket.make_public()
        self.assertEqual(list(bucket.acl), permissive)
        self.assertEqual(list(bucket.default_object_acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'acl': after['acl']})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def _make_public_w_future_helper(self, default_object_acl_loaded=True):
        from gcloud.storage.acl import _ACLEntity
        NAME = 'name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after1 = {'acl': permissive, 'defaultObjectAcl': []}
        after2 = {'acl': permissive, 'defaultObjectAcl': permissive}
        if default_object_acl_loaded:
            num_requests = 2
            connection = _Connection(after1, after2)
        else:
            num_requests = 3
            # We return the same value for default_object_acl.reload()
            # to consume.
            connection = _Connection(after1, after1, after2)
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        bucket.acl.loaded = True
        bucket.default_object_acl.loaded = default_object_acl_loaded
        bucket.make_public(future=True)
        self.assertEqual(list(bucket.acl), permissive)
        self.assertEqual(list(bucket.default_object_acl), permissive)
        kw = connection._requested
        self.assertEqual(len(kw), num_requests)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'acl': permissive})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})
        if not default_object_acl_loaded:
            self.assertEqual(kw[1]['method'], 'GET')
            self.assertEqual(kw[1]['path'], '/b/%s/defaultObjectAcl' % NAME)
        # Last could be 1 or 2 depending on `default_object_acl_loaded`.
        self.assertEqual(kw[-1]['method'], 'PATCH')
        self.assertEqual(kw[-1]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[-1]['data'], {'defaultObjectAcl': permissive})
        self.assertEqual(kw[-1]['query_params'], {'projection': 'full'})

    def test_make_public_w_future(self):
        self._make_public_w_future_helper(default_object_acl_loaded=True)

    def test_make_public_w_future_reload_default(self):
        self._make_public_w_future_helper(default_object_acl_loaded=False)

    def test_make_public_recursive(self):
        from gcloud.storage.acl import _ACLEntity
        from gcloud.storage.bucket import _BlobIterator
        _saved = []

        class _Blob(object):
            _granted = False

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            @property
            def acl(self):
                return self

            # Faux ACL methods
            def all(self):
                return self

            def grant_read(self):
                self._granted = True

            def save(self, client=None):
                _saved.append(
                    (self._bucket, self._name, self._granted, client))

        class _Iterator(_BlobIterator):
            def get_items_from_response(self, response):
                for item in response.get('items', []):
                    yield _Blob(self.bucket, item['name'])

        NAME = 'name'
        BLOB_NAME = 'blob-name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive, 'defaultObjectAcl': []}
        connection = _Connection(after, {'items': [{'name': BLOB_NAME}]})
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        bucket.acl.loaded = True
        bucket.default_object_acl.loaded = True
        bucket._iterator_class = _Iterator
        bucket.make_public(recursive=True)
        self.assertEqual(list(bucket.acl), permissive)
        self.assertEqual(list(bucket.default_object_acl), [])
        self.assertEqual(_saved, [(bucket, BLOB_NAME, True, None)])
        kw = connection._requested
        self.assertEqual(len(kw), 2)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'acl': permissive})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})
        self.assertEqual(kw[1]['method'], 'GET')
        self.assertEqual(kw[1]['path'], '/b/%s/o' % NAME)
        max_results = bucket._MAX_OBJECTS_FOR_ITERATION + 1
        self.assertEqual(kw[1]['query_params'],
                         {'maxResults': max_results, 'projection': 'full'})

    def test_make_public_recursive_too_many(self):
        from gcloud.storage.acl import _ACLEntity

        PERMISSIVE = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        AFTER = {'acl': PERMISSIVE, 'defaultObjectAcl': []}

        NAME = 'name'
        BLOB_NAME1 = 'blob-name1'
        BLOB_NAME2 = 'blob-name2'
        GET_BLOBS_RESP = {
            'items': [
                {'name': BLOB_NAME1},
                {'name': BLOB_NAME2},
            ],
        }
        connection = _Connection(AFTER, GET_BLOBS_RESP)
        client = _Client(connection)
        bucket = self._makeOne(client=client, name=NAME)
        bucket.acl.loaded = True
        bucket.default_object_acl.loaded = True

        # Make the Bucket refuse to make_public with 2 objects.
        bucket._MAX_OBJECTS_FOR_ITERATION = 1
        self.assertRaises(ValueError, bucket.make_public, recursive=True)


class _Connection(object):
    _delete_bucket = False

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []
        self._deleted_buckets = []

    @staticmethod
    def _is_bucket_path(path):
        # Now just ensure the path only has /b/ and one more segment.
        return path.startswith('/b/') and path.count('/') == 2

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        method = kw.get('method')
        path = kw.get('path', '')
        if method == 'DELETE' and self._is_bucket_path(path):
            self._deleted_buckets.append(kw)
            if self._delete_bucket:
                return
            else:
                raise NotFound('miss')

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response


class _Bucket(object):
    path = '/b/name'
    name = 'name'

    def __init__(self, client=None):
        self.client = client


class _Client(object):

    def __init__(self, connection, project=None):
        self.connection = connection
        self.project = project
