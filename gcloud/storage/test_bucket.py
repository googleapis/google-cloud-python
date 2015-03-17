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

import io

import unittest2


class Test__BlobIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.bucket import _BlobIterator
        return _BlobIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        bucket = _Bucket(connection)
        iterator = self._makeOne(bucket)
        self.assertTrue(iterator.bucket is bucket)
        self.assertTrue(iterator.connection is connection)
        self.assertEqual(iterator.path, '%s/o' % bucket.path)
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)
        self.assertEqual(iterator.prefixes, ())

    def test_get_items_from_response_empty(self):
        connection = _Connection()
        bucket = _Bucket(connection)
        iterator = self._makeOne(bucket)
        self.assertEqual(list(iterator.get_items_from_response({})), [])
        self.assertEqual(iterator.prefixes, ())

    def test_get_items_from_response_non_empty(self):
        from gcloud.storage.blob import Blob
        BLOB_NAME = 'blob-name'
        response = {'items': [{'name': BLOB_NAME}], 'prefixes': ['foo']}
        connection = _Connection()
        bucket = _Bucket(connection)
        iterator = self._makeOne(bucket)
        blobs = list(iterator.get_items_from_response(response))
        self.assertEqual(len(blobs), 1)
        blob = blobs[0]
        self.assertTrue(isinstance(blob, Blob))
        self.assertTrue(blob.connection is connection)
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(iterator.prefixes, ('foo',))


class Test_Bucket(unittest2.TestCase):

    def _makeOne(self, *args, **kw):
        from gcloud.storage.bucket import Bucket
        return Bucket(*args, **kw)

    def test_ctor_defaults(self):
        bucket = self._makeOne()
        self.assertEqual(bucket.connection, None)
        self.assertEqual(bucket.name, None)
        self.assertEqual(bucket._properties, {})
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test_ctor_explicit(self):
        NAME = 'name'
        connection = _Connection()
        properties = {'key': 'value'}
        bucket = self._makeOne(NAME, connection, properties)
        self.assertTrue(bucket.connection is connection)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket._properties, properties)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test_ctor_no_name_defaults(self):
        NAME = 'name'
        properties = {'key': 'value', 'name': NAME}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.connection, None)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket.properties, properties)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test_ctor_no_name_explicit(self):
        NAME = 'name'
        connection = _Connection()
        properties = {'key': 'value', 'name': NAME}
        bucket = self._makeOne(connection=connection, properties=properties)
        self.assertTrue(bucket.connection is connection)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket.properties, properties)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test___iter___empty(self):
        NAME = 'name'
        connection = _Connection({'items': []})
        bucket = self._makeOne(NAME, connection)
        blobs = list(bucket)
        self.assertEqual(blobs, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {})

    def test___iter___non_empty(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        connection = _Connection({'items': [{'name': BLOB_NAME}]})
        bucket = self._makeOne(NAME, connection)
        blobs = list(bucket)
        blob, = blobs
        self.assertTrue(blob.bucket is bucket)
        self.assertEqual(blob.name, BLOB_NAME)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {})

    def test___contains___miss(self):
        NAME = 'name'
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = self._makeOne(NAME, connection)
        self.assertFalse(NONESUCH in bucket)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test___contains___hit(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        connection = _Connection({'name': BLOB_NAME})
        bucket = self._makeOne(NAME, connection)
        self.assertTrue(BLOB_NAME in bucket)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, BLOB_NAME))

    def test_exists_miss(self):
        from gcloud.exceptions import NotFound

        class _FakeConnection(object):

            _called_with = []

            @classmethod
            def api_request(cls, *args, **kwargs):
                cls._called_with.append((args, kwargs))
                raise NotFound(args)

        BUCKET_NAME = 'bucket-name'
        bucket = self._makeOne(connection=_FakeConnection, name=BUCKET_NAME)
        self.assertFalse(bucket.exists())
        expected_called_kwargs = {
            'method': 'GET',
            'path': bucket.path,
            'query_params': {
                'fields': 'name',
            },
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
        bucket = self._makeOne(connection=_FakeConnection, name=BUCKET_NAME)
        self.assertTrue(bucket.exists())
        expected_called_kwargs = {
            'method': 'GET',
            'path': bucket.path,
            'query_params': {
                'fields': 'name',
            },
        }
        expected_cw = [((), expected_called_kwargs)]
        self.assertEqual(_FakeConnection._called_with, expected_cw)

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
        connection = _Connection()
        bucket = self._makeOne(NAME, connection)
        self.assertEqual(bucket.path, '/b/%s' % NAME)

    def test_get_blob_miss(self):
        NAME = 'name'
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = self._makeOne(NAME, connection)
        self.assertTrue(bucket.get_blob(NONESUCH) is None)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_get_blob_hit(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        connection = _Connection({'name': BLOB_NAME})
        bucket = self._makeOne(NAME, connection)
        blob = bucket.get_blob(BLOB_NAME)
        self.assertTrue(blob.bucket is bucket)
        self.assertEqual(blob.name, BLOB_NAME)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, BLOB_NAME))

    def test_get_all_blobs_empty(self):
        NAME = 'name'
        connection = _Connection({'items': []})
        bucket = self._makeOne(NAME, connection)
        blobs = bucket.get_all_blobs()
        self.assertEqual(blobs, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {})

    def test_get_all_blobs_non_empty(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        connection = _Connection({'items': [{'name': BLOB_NAME}]})
        bucket = self._makeOne(NAME, connection)
        blobs = bucket.get_all_blobs()
        blob, = blobs
        self.assertTrue(blob.bucket is bucket)
        self.assertEqual(blob.name, BLOB_NAME)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {})

    def test_iterator_defaults(self):
        NAME = 'name'
        connection = _Connection({'items': []})
        bucket = self._makeOne(NAME, connection)
        iterator = bucket.iterator()
        blobs = list(iterator)
        self.assertEqual(blobs, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {})

    def test_iterator_explicit(self):
        NAME = 'name'
        EXPECTED = {
            'prefix': 'subfolder',
            'delimiter': '/',
            'maxResults': 10,
            'versions': True,
        }
        connection = _Connection({'items': []})
        bucket = self._makeOne(NAME, connection)
        iterator = bucket.iterator(
            prefix='subfolder',
            delimiter='/',
            max_results=10,
            versions=True,
        )
        blobs = list(iterator)
        self.assertEqual(blobs, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], EXPECTED)

    def test_delete_default_miss(self):
        from gcloud.exceptions import NotFound
        NAME = 'name'
        connection = _Connection()
        bucket = self._makeOne(NAME, connection)
        self.assertRaises(NotFound, bucket.delete)
        expected_cw = [{'method': 'DELETE', 'path': bucket.path}]
        self.assertEqual(connection._deleted_buckets, expected_cw)

    def test_delete_explicit_hit(self):
        NAME = 'name'
        GET_BLOBS_RESP = {'items': []}
        connection = _Connection(GET_BLOBS_RESP)
        connection._delete_bucket = True
        bucket = self._makeOne(NAME, connection)
        self.assertEqual(bucket.delete(force=True), None)
        expected_cw = [{'method': 'DELETE', 'path': bucket.path}]
        self.assertEqual(connection._deleted_buckets, expected_cw)

    def test_delete_explicit_force_delete_blobs(self):
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
        bucket = self._makeOne(NAME, connection)
        self.assertEqual(bucket.delete(force=True), None)
        expected_cw = [{'method': 'DELETE', 'path': bucket.path}]
        self.assertEqual(connection._deleted_buckets, expected_cw)

    def test_delete_explicit_force_miss_blobs(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name1'
        GET_BLOBS_RESP = {'items': [{'name': BLOB_NAME}]}
        # Note the connection does not have a response for the blob.
        connection = _Connection(GET_BLOBS_RESP)
        connection._delete_bucket = True
        bucket = self._makeOne(NAME, connection)
        self.assertEqual(bucket.delete(force=True), None)
        expected_cw = [{'method': 'DELETE', 'path': bucket.path}]
        self.assertEqual(connection._deleted_buckets, expected_cw)

    def test_delete_explicit_too_many(self):
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
        bucket = self._makeOne(NAME, connection)

        # Make the Bucket refuse to delete with 2 objects.
        bucket._MAX_OBJECTS_FOR_BUCKET_DELETE = 1
        self.assertRaises(ValueError, bucket.delete, force=True)
        self.assertEqual(connection._deleted_buckets, [])

    def test_delete_blob_miss(self):
        from gcloud.exceptions import NotFound
        NAME = 'name'
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = self._makeOne(NAME, connection)
        self.assertRaises(NotFound, bucket.delete_blob, NONESUCH)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'DELETE')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_delete_blob_hit(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        connection = _Connection({})
        bucket = self._makeOne(NAME, connection)
        result = bucket.delete_blob(BLOB_NAME)
        self.assertTrue(result is None)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'DELETE')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, BLOB_NAME))

    def test_delete_blobs_empty(self):
        NAME = 'name'
        connection = _Connection()
        bucket = self._makeOne(NAME, connection)
        bucket.delete_blobs([])
        self.assertEqual(connection._requested, [])

    def test_delete_blobs_hit(self):
        NAME = 'name'
        BLOB_NAME = 'blob-name'
        connection = _Connection({})
        bucket = self._makeOne(NAME, connection)
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
        bucket = self._makeOne(NAME, connection)
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
        bucket = self._makeOne(NAME, connection)
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
        source = self._makeOne(SOURCE, connection)
        dest = self._makeOne(DEST, connection)
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
        source = self._makeOne(SOURCE, connection)
        dest = self._makeOne(DEST, connection)
        blob = _Blob()
        new_blob = source.copy_blob(blob, dest, NEW_NAME)
        self.assertTrue(new_blob.bucket is dest)
        self.assertEqual(new_blob.name, NEW_NAME)
        kw, = connection._requested
        COPY_PATH = '/b/%s/o/%s/copyTo/b/%s/o/%s' % (SOURCE, BLOB_NAME,
                                                     DEST, NEW_NAME)
        self.assertEqual(kw['method'], 'POST')
        self.assertEqual(kw['path'], COPY_PATH)

    def test_upload_file_default_blob(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import bucket as MUT
        BASENAME = 'file.ext'
        FILENAME = '/path/to/%s' % BASENAME
        _uploaded = []

        class _Blob(object):

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            def upload_from_filename(self, filename):
                _uploaded.append((self._bucket, self._name, filename))

        bucket = self._makeOne()
        with _Monkey(MUT, Blob=_Blob):
            bucket.upload_file(FILENAME)
        self.assertEqual(_uploaded, [(bucket, BASENAME, FILENAME)])

    def test_upload_file_explicit_blob(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import bucket as MUT
        FILENAME = '/path/to/file'
        BLOB_NAME = 'blob-name'
        _uploaded = []

        class _Blob(object):

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            def upload_from_filename(self, filename):
                _uploaded.append((self._bucket, self._name, filename))

        bucket = self._makeOne()
        with _Monkey(MUT, Blob=_Blob):
            bucket.upload_file(FILENAME, BLOB_NAME)
        self.assertEqual(_uploaded, [(bucket, BLOB_NAME, FILENAME)])

    def test_upload_file_object_no_blob(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import bucket as MUT
        FILENAME = 'file.txt'
        FILEOBJECT = MockFile(FILENAME)
        _uploaded = []

        class _Blob(object):

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            def upload_from_file(self, fh):
                _uploaded.append((self._bucket, self._name, fh))

        bucket = self._makeOne()
        with _Monkey(MUT, Blob=_Blob):
            found = bucket.upload_file_object(FILEOBJECT)
        self.assertEqual(_uploaded, [(bucket, FILENAME, FILEOBJECT)])
        self.assertTrue(isinstance(found, _Blob))
        self.assertEqual(found._name, FILENAME)
        self.assertTrue(found._bucket is bucket)

    def test_upload_file_object_explicit_blob(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import bucket as MUT
        FILENAME = 'file.txt'
        FILEOBJECT = MockFile(FILENAME)
        BLOB_NAME = 'blob-name'
        _uploaded = []

        class _Blob(object):

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            def upload_from_file(self, fh):
                _uploaded.append((self._bucket, self._name, fh))

        bucket = self._makeOne()
        with _Monkey(MUT, Blob=_Blob):
            found = bucket.upload_file_object(FILEOBJECT, BLOB_NAME)
        self.assertEqual(_uploaded, [(bucket, BLOB_NAME, FILEOBJECT)])
        self.assertTrue(isinstance(found, _Blob))
        self.assertEqual(found._name, BLOB_NAME)
        self.assertTrue(found._bucket is bucket)

    def test_get_cors_eager(self):
        NAME = 'name'
        CORS_ENTRY = {
            'maxAgeSeconds': 1234,
            'method': ['OPTIONS', 'GET'],
            'origin': ['127.0.0.1'],
            'responseHeader': ['Content-Type'],
            }
        before = {'cors': [CORS_ENTRY, {}]}
        connection = _Connection()
        bucket = self._makeOne(NAME, connection, before)
        entries = bucket.get_cors()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]['maxAgeSeconds'],
                         CORS_ENTRY['maxAgeSeconds'])
        self.assertEqual(entries[0]['method'],
                         CORS_ENTRY['method'])
        self.assertEqual(entries[0]['origin'],
                         CORS_ENTRY['origin'])
        self.assertEqual(entries[0]['responseHeader'],
                         CORS_ENTRY['responseHeader'])
        self.assertEqual(entries[1], {})
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_get_cors_lazy(self):
        NAME = 'name'
        CORS_ENTRY = {
            'maxAgeSeconds': 1234,
            'method': ['OPTIONS', 'GET'],
            'origin': ['127.0.0.1'],
            'responseHeader': ['Content-Type'],
            }
        after = {'cors': [CORS_ENTRY]}
        connection = _Connection(after)
        bucket = self._makeOne(NAME, connection)
        bucket._reload_properties()
        entries = bucket.get_cors()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['maxAgeSeconds'],
                         CORS_ENTRY['maxAgeSeconds'])
        self.assertEqual(entries[0]['method'],
                         CORS_ENTRY['method'])
        self.assertEqual(entries[0]['origin'],
                         CORS_ENTRY['origin'])
        self.assertEqual(entries[0]['responseHeader'],
                         CORS_ENTRY['responseHeader'])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_update_cors(self):
        NAME = 'name'
        CORS_ENTRY = {
            'maxAgeSeconds': 1234,
            'method': ['OPTIONS', 'GET'],
            'origin': ['127.0.0.1'],
            'responseHeader': ['Content-Type'],
            }
        after = {'cors': [CORS_ENTRY, {}]}
        connection = _Connection(after)
        bucket = self._makeOne(NAME, connection)
        bucket.update_cors([CORS_ENTRY, {}])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], after)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})
        entries = bucket.get_cors()
        self.assertEqual(entries, [CORS_ENTRY, {}])

    def test_get_default_object_acl_lazy(self):
        from gcloud.storage.acl import BucketACL
        NAME = 'name'
        connection = _Connection({'items': []})
        bucket = self._makeOne(NAME, connection)
        acl = bucket.get_default_object_acl()
        self.assertTrue(acl is bucket.default_object_acl)
        self.assertTrue(isinstance(acl, BucketACL))
        self.assertEqual(list(bucket.default_object_acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s/defaultObjectAcl' % NAME)

    def test_get_default_object_acl_eager(self):
        connection = _Connection()
        bucket = self._makeOne()
        preset = bucket.default_object_acl  # ensure it is assigned
        preset.loaded = True
        acl = bucket.get_default_object_acl()
        self.assertTrue(acl is preset)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

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

    def test_get_lifecycle_eager(self):
        NAME = 'name'
        LC_RULE = {'action': {'type': 'Delete'}, 'condition': {'age': 42}}
        before = {'lifecycle': {'rule': [LC_RULE]}}
        connection = _Connection()
        bucket = self._makeOne(NAME, connection, before)
        entries = bucket.get_lifecycle()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['action']['type'], 'Delete')
        self.assertEqual(entries[0]['condition']['age'], 42)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_get_lifecycle_lazy(self):
        NAME = 'name'
        LC_RULE = {'action': {'type': 'Delete'}, 'condition': {'age': 42}}
        after = {'lifecycle': {'rule': [LC_RULE]}}
        connection = _Connection(after)
        bucket = self._makeOne(NAME, connection)
        bucket._reload_properties()
        entries = bucket.get_lifecycle()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['action']['type'], 'Delete')
        self.assertEqual(entries[0]['condition']['age'], 42)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_update_lifecycle(self):
        NAME = 'name'
        LC_RULE = {'action': {'type': 'Delete'}, 'condition': {'age': 42}}
        after = {'lifecycle': {'rule': [LC_RULE]}}
        connection = _Connection(after)
        bucket = self._makeOne(NAME, connection)
        bucket.update_lifecycle([LC_RULE])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], after)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})
        entries = bucket.get_lifecycle()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['action']['type'], 'Delete')
        self.assertEqual(entries[0]['condition']['age'], 42)

    def test_location_getter(self):
        NAME = 'name'
        connection = _Connection()
        before = {'location': 'AS'}
        bucket = self._makeOne(NAME, connection, before)
        self.assertEqual(bucket.location, 'AS')
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_location_setter(self):
        NAME = 'name'
        connection = _Connection({'location': 'AS'})
        bucket = self._makeOne(NAME, connection)
        bucket.location = 'AS'
        bucket.patch()
        self.assertEqual(bucket.location, 'AS')
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'location': 'AS'})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

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
        resp_to_reload = before
        connection = _Connection(resp_to_reload)
        bucket = self._makeOne(NAME, connection)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info['logObjectPrefix'], LOG_PREFIX)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_enable_logging_defaults(self):
        NAME = 'name'
        LOG_BUCKET = 'logs'
        before = {'logging': None}
        resp_to_reload = before
        resp_to_enable_logging = {
            'logging': {'logBucket': LOG_BUCKET, 'logObjectPrefix': ''},
        }
        connection = _Connection(resp_to_reload, resp_to_enable_logging,
                                 resp_to_enable_logging)
        bucket = self._makeOne(NAME, connection, before)
        self.assertTrue(bucket.get_logging() is None)
        bucket.enable_logging(LOG_BUCKET)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info['logObjectPrefix'], '')
        kw = connection._requested
        self.assertEqual(len(kw), 3)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})
        self.assertEqual(kw[1]['method'], 'PATCH')
        self.assertEqual(kw[1]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[1]['data'], resp_to_enable_logging)
        self.assertEqual(kw[1]['query_params'], {'projection': 'full'})
        self.assertEqual(kw[2]['method'], 'GET')
        self.assertEqual(kw[2]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[2]['query_params'], {'projection': 'noAcl'})

    def test_enable_logging_explicit(self):
        NAME = 'name'
        LOG_BUCKET = 'logs'
        LOG_PFX = 'pfx'
        before = {'logging': None}
        resp_to_reload = before
        resp_to_enable_logging = {
            'logging': {'logBucket': LOG_BUCKET, 'logObjectPrefix': LOG_PFX},
        }
        connection = _Connection(resp_to_reload,
                                 resp_to_enable_logging,
                                 resp_to_enable_logging)
        bucket = self._makeOne(NAME, connection, before)
        self.assertTrue(bucket.get_logging() is None)
        bucket.enable_logging(LOG_BUCKET, LOG_PFX)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info['logObjectPrefix'], LOG_PFX)
        kw = connection._requested
        self.assertEqual(len(kw), 3)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})
        self.assertEqual(kw[1]['method'], 'PATCH')
        self.assertEqual(kw[1]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[1]['data'], resp_to_enable_logging)
        self.assertEqual(kw[1]['query_params'], {'projection': 'full'})
        self.assertEqual(kw[2]['method'], 'GET')
        self.assertEqual(kw[2]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[2]['query_params'], {'projection': 'noAcl'})

    def test_disable_logging(self):
        NAME = 'name'
        before = {'logging': {'logBucket': 'logs', 'logObjectPrefix': 'pfx'}}
        resp_to_reload = before
        resp_to_disable_logging = {'logging': None}
        connection = _Connection(resp_to_reload, resp_to_disable_logging,
                                 resp_to_disable_logging)
        bucket = self._makeOne(NAME, connection, before)
        self.assertTrue(bucket.get_logging() is not None)
        bucket.disable_logging()
        self.assertTrue(bucket.get_logging() is None)
        kw = connection._requested
        self.assertEqual(len(kw), 3)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})
        self.assertEqual(kw[1]['method'], 'PATCH')
        self.assertEqual(kw[1]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[1]['data'], {'logging': None})
        self.assertEqual(kw[1]['query_params'], {'projection': 'full'})
        self.assertEqual(kw[2]['method'], 'GET')
        self.assertEqual(kw[2]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[2]['query_params'], {'projection': 'noAcl'})

    def test_metageneration(self):
        METAGENERATION = 42
        properties = {'metageneration': METAGENERATION}
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

    def test_self_link(self):
        SELF_LINK = 'http://example.com/self/'
        properties = {'selfLink': SELF_LINK}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.self_link, SELF_LINK)

    def test_storage_class(self):
        STORAGE_CLASS = 'http://example.com/self/'
        properties = {'storageClass': STORAGE_CLASS}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.storage_class, STORAGE_CLASS)

    def test_time_created(self):
        TIME_CREATED = '2014-11-05T20:34:37Z'
        properties = {'timeCreated': TIME_CREATED}
        bucket = self._makeOne(properties=properties)
        self.assertEqual(bucket.time_created, TIME_CREATED)

    def test_versioning_enabled_getter_missing(self):
        NAME = 'name'
        connection = _Connection({})
        bucket = self._makeOne(NAME, connection)
        bucket._reload_properties()
        self.assertEqual(bucket.versioning_enabled, False)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_versioning_enabled_getter(self):
        NAME = 'name'
        before = {'versioning': {'enabled': True}}
        connection = _Connection()
        bucket = self._makeOne(NAME, connection, before)
        self.assertEqual(bucket.versioning_enabled, True)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_versioning_enabled_setter(self):
        NAME = 'name'
        before = {'versioning': {'enabled': False}}
        after = {'versioning': {'enabled': True}}
        connection = _Connection(after)
        bucket = self._makeOne(NAME, connection, before)
        self.assertFalse(bucket.versioning_enabled)
        bucket.versioning_enabled = True
        bucket.patch()
        self.assertTrue(bucket.versioning_enabled)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['data'], {'versioning': {'enabled': True}})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_configure_website_defaults(self):
        NAME = 'name'
        patched = {'website': {'mainPageSuffix': None,
                               'notFoundPage': None}}
        connection = _Connection(patched)
        bucket = self._makeOne(NAME, connection)
        self.assertTrue(bucket.configure_website() is bucket)
        self.assertEqual(bucket.properties, patched)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], patched)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_configure_website_explicit(self):
        NAME = 'name'
        patched = {'website': {'mainPageSuffix': 'html',
                               'notFoundPage': '404.html'}}
        connection = _Connection(patched)
        bucket = self._makeOne(NAME, connection)
        self.assertTrue(bucket.configure_website('html', '404.html') is bucket)
        self.assertEqual(bucket.properties, patched)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], patched)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_disable_website(self):
        NAME = 'name'
        patched = {'website': {'mainPageSuffix': None,
                               'notFoundPage': None}}
        connection = _Connection(patched)
        bucket = self._makeOne(NAME, connection)
        self.assertTrue(bucket.disable_website() is bucket)
        self.assertEqual(bucket.properties, patched)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], patched)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_make_public_defaults(self):
        from gcloud.storage.acl import _ACLEntity
        NAME = 'name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive, 'defaultObjectAcl': []}
        connection = _Connection(after)
        bucket = self._makeOne(NAME, connection)
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

    def test_make_public_w_future(self):
        from gcloud.storage.acl import _ACLEntity
        NAME = 'name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after1 = {'acl': permissive, 'defaultObjectAcl': []}
        after2 = {'acl': permissive, 'defaultObjectAcl': permissive}
        connection = _Connection(after1, after2)
        bucket = self._makeOne(NAME, connection)
        bucket.acl.loaded = True
        bucket.default_object_acl.loaded = True
        bucket.make_public(future=True)
        self.assertEqual(list(bucket.acl), permissive)
        self.assertEqual(list(bucket.default_object_acl), permissive)
        kw = connection._requested
        self.assertEqual(len(kw), 2)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'acl': permissive})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})
        self.assertEqual(kw[1]['method'], 'PATCH')
        self.assertEqual(kw[1]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[1]['data'], {'defaultObjectAcl': permissive})
        self.assertEqual(kw[1]['query_params'], {'projection': 'full'})

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

            def all(self):
                return self

            def grant_read(self):
                self._granted = True

            def save_acl(self):
                _saved.append((self._bucket, self._name, self._granted))

        class _Iterator(_BlobIterator):
            def get_items_from_response(self, response):
                for item in response.get('items', []):
                    yield _Blob(self.bucket, item['name'])

        NAME = 'name'
        BLOB_NAME = 'blob-name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive, 'defaultObjectAcl': []}
        connection = _Connection(after, {'items': [{'name': BLOB_NAME}]})
        bucket = self._makeOne(NAME, connection)
        bucket.acl.loaded = True
        bucket.default_object_acl.loaded = True
        bucket._iterator_class = _Iterator
        bucket.make_public(recursive=True)
        self.assertEqual(list(bucket.acl), permissive)
        self.assertEqual(list(bucket.default_object_acl), [])
        self.assertEqual(_saved, [(bucket, BLOB_NAME, True)])
        kw = connection._requested
        self.assertEqual(len(kw), 2)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'acl': permissive})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})
        self.assertEqual(kw[1]['method'], 'GET')
        self.assertEqual(kw[1]['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw[1]['query_params'], {})


class _Connection(object):
    _delete_bucket = False

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []
        self._deleted_buckets = []

    @staticmethod
    def _is_bucket_path(path):
        if not path.startswith('/b/'):  # pragma: NO COVER
            return False
        # Now just ensure the path only has /b/ and one more segment.
        return path.count('/') == 2

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

    def __init__(self, connection):
        self.connection = connection


class MockFile(io.StringIO):
    name = None

    def __init__(self, name, buffer_=None):
        super(MockFile, self).__init__(buffer_)
        self.name = name
