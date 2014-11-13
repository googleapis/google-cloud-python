import io

import unittest2


class Test__KeyIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.bucket import _KeyIterator
        return _KeyIterator

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
        from gcloud.storage.key import Key
        KEY = 'key'
        response = {'items': [{'name': KEY}], 'prefixes': ['foo']}
        connection = _Connection()
        bucket = _Bucket(connection)
        iterator = self._makeOne(bucket)
        keys = list(iterator.get_items_from_response(response))
        self.assertEqual(len(keys), 1)
        key = keys[0]
        self.assertTrue(isinstance(key, Key))
        self.assertTrue(key.connection is connection)
        self.assertEqual(key.name, KEY)
        self.assertEqual(iterator.prefixes, ('foo',))


class Test_Bucket(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.bucket import Bucket
        return Bucket

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

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
        bucket = self._makeOne(connection, NAME, properties)
        self.assertTrue(bucket.connection is connection)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket._properties, properties)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test_from_dict_defaults(self):
        NAME = 'name'
        properties = {'key': 'value', 'name': NAME}
        klass = self._getTargetClass()
        bucket = klass.from_dict(properties)
        self.assertEqual(bucket.connection, None)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket.properties, properties)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test_from_dict_explicit(self):
        NAME = 'name'
        connection = _Connection()
        properties = {'key': 'value', 'name': NAME}
        klass = self._getTargetClass()
        bucket = klass.from_dict(properties, connection)
        self.assertTrue(bucket.connection is connection)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket.properties, properties)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test___iter___empty(self):
        NAME = 'name'
        connection = _Connection({'items': []})
        bucket = self._makeOne(connection, NAME)
        keys = list(bucket)
        self.assertEqual(keys, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {})

    def test___iter___non_empty(self):
        NAME = 'name'
        KEY = 'key'
        connection = _Connection({'items': [{'name': KEY}]})
        bucket = self._makeOne(connection, NAME)
        keys = list(bucket)
        key, = keys
        self.assertTrue(key.bucket is bucket)
        self.assertEqual(key.name, KEY)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {})

    def test___contains___miss(self):
        NAME = 'name'
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        self.assertFalse(NONESUCH in bucket)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test___contains___hit(self):
        NAME = 'name'
        KEY = 'key'
        connection = _Connection({'name': KEY})
        bucket = self._makeOne(connection, NAME)
        self.assertTrue(KEY in bucket)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, KEY))

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
        bucket = self._makeOne(connection, NAME)
        self.assertEqual(bucket.path, '/b/%s' % NAME)

    def test_get_key_miss(self):
        NAME = 'name'
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        self.assertTrue(bucket.get_key(NONESUCH) is None)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_get_key_hit(self):
        NAME = 'name'
        KEY = 'key'
        connection = _Connection({'name': KEY})
        bucket = self._makeOne(connection, NAME)
        key = bucket.get_key(KEY)
        self.assertTrue(key.bucket is bucket)
        self.assertEqual(key.name, KEY)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, KEY))

    def test_get_all_keys_empty(self):
        NAME = 'name'
        connection = _Connection({'items': []})
        bucket = self._makeOne(connection, NAME)
        keys = bucket.get_all_keys()
        self.assertEqual(keys, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {})

    def test_get_all_keys_non_empty(self):
        NAME = 'name'
        KEY = 'key'
        connection = _Connection({'items': [{'name': KEY}]})
        bucket = self._makeOne(connection, NAME)
        keys = bucket.get_all_keys()
        key, = keys
        self.assertTrue(key.bucket is bucket)
        self.assertEqual(key.name, KEY)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], {})

    def test_iterator_defaults(self):
        NAME = 'name'
        connection = _Connection({'items': []})
        bucket = self._makeOne(connection, NAME)
        iterator = bucket.iterator()
        keys = list(iterator)
        self.assertEqual(keys, [])
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
        bucket = self._makeOne(connection, NAME)
        iterator = bucket.iterator(
            prefix='subfolder',
            delimiter='/',
            max_results=10,
            versions=True,
        )
        keys = list(iterator)
        self.assertEqual(keys, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], EXPECTED)

    def test_new_key_existing(self):
        from gcloud.storage.key import Key
        existing = Key()
        bucket = self._makeOne()
        self.assertTrue(bucket.new_key(existing) is existing)

    def test_new_key_str(self):
        from gcloud.storage.key import Key
        KEY = 'key'
        bucket = self._makeOne()
        key = bucket.new_key(KEY)
        self.assertTrue(isinstance(key, Key))
        self.assertTrue(key.bucket is bucket)
        self.assertEqual(key.name, KEY)

    def test_new_key_invalid(self):
        bucket = self._makeOne()
        self.assertRaises(TypeError, bucket.new_key, object())

    def test_delete_default_miss(self):
        from gcloud.storage.exceptions import NotFound
        NAME = 'name'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        self.assertRaises(NotFound, bucket.delete)
        self.assertEqual(connection._deleted, [(NAME, False)])

    def test_delete_explicit_hit(self):
        NAME = 'name'
        connection = _Connection()
        connection._delete_ok = True
        bucket = self._makeOne(connection, NAME)
        self.assertTrue(bucket.delete(True))
        self.assertEqual(connection._deleted, [(NAME, True)])

    def test_delete_key_miss(self):
        from gcloud.storage.exceptions import NotFound
        NAME = 'name'
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        self.assertRaises(NotFound, bucket.delete_key, NONESUCH)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'DELETE')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_delete_key_hit(self):
        NAME = 'name'
        KEY = 'key'
        connection = _Connection({})
        bucket = self._makeOne(connection, NAME)
        key = bucket.delete_key(KEY)
        self.assertTrue(key.bucket is bucket)
        self.assertEqual(key.name, KEY)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'DELETE')
        self.assertEqual(kw['path'], '/b/%s/o/%s' % (NAME, KEY))

    def test_delete_keys_empty(self):
        NAME = 'name'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        bucket.delete_keys([])
        self.assertEqual(connection._requested, [])

    def test_delete_keys_hit(self):
        NAME = 'name'
        KEY = 'key'
        connection = _Connection({})
        bucket = self._makeOne(connection, NAME)
        bucket.delete_keys([KEY])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'DELETE')
        self.assertEqual(kw[0]['path'], '/b/%s/o/%s' % (NAME, KEY))

    def test_delete_keys_miss_no_on_error(self):
        from gcloud.storage.exceptions import NotFound
        NAME = 'name'
        KEY = 'key'
        NONESUCH = 'nonesuch'
        connection = _Connection({})
        bucket = self._makeOne(connection, NAME)
        self.assertRaises(NotFound, bucket.delete_keys, [KEY, NONESUCH])
        kw = connection._requested
        self.assertEqual(len(kw), 2)
        self.assertEqual(kw[0]['method'], 'DELETE')
        self.assertEqual(kw[0]['path'], '/b/%s/o/%s' % (NAME, KEY))
        self.assertEqual(kw[1]['method'], 'DELETE')
        self.assertEqual(kw[1]['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_delete_keys_miss_w_on_error(self):
        NAME = 'name'
        KEY = 'key'
        NONESUCH = 'nonesuch'
        connection = _Connection({})
        bucket = self._makeOne(connection, NAME)
        errors = []
        bucket.delete_keys([KEY, NONESUCH], errors.append)
        self.assertEqual(errors, [NONESUCH])
        kw = connection._requested
        self.assertEqual(len(kw), 2)
        self.assertEqual(kw[0]['method'], 'DELETE')
        self.assertEqual(kw[0]['path'], '/b/%s/o/%s' % (NAME, KEY))
        self.assertEqual(kw[1]['method'], 'DELETE')
        self.assertEqual(kw[1]['path'], '/b/%s/o/%s' % (NAME, NONESUCH))

    def test_copy_keys_wo_name(self):
        SOURCE = 'source'
        DEST = 'dest'
        KEY = 'key'

        class _Key(object):
            name = KEY
            path = '/b/%s/o/%s' % (SOURCE, KEY)

        connection = _Connection({})
        source = self._makeOne(connection, SOURCE)
        dest = self._makeOne(connection, DEST)
        key = _Key()
        new_key = source.copy_key(key, dest)
        self.assertTrue(new_key.bucket is dest)
        self.assertEqual(new_key.name, KEY)
        kw, = connection._requested
        COPY_PATH = '/b/%s/o/%s/copyTo/b/%s/o/%s' % (SOURCE, KEY, DEST, KEY)
        self.assertEqual(kw['method'], 'POST')
        self.assertEqual(kw['path'], COPY_PATH)

    def test_copy_keys_w_name(self):
        SOURCE = 'source'
        DEST = 'dest'
        KEY = 'key'
        NEW_NAME = 'new_name'

        class _Key(object):
            name = KEY
            path = '/b/%s/o/%s' % (SOURCE, KEY)

        connection = _Connection({})
        source = self._makeOne(connection, SOURCE)
        dest = self._makeOne(connection, DEST)
        key = _Key()
        new_key = source.copy_key(key, dest, NEW_NAME)
        self.assertTrue(new_key.bucket is dest)
        self.assertEqual(new_key.name, NEW_NAME)
        kw, = connection._requested
        COPY_PATH = (
            '/b/%s/o/%s/copyTo/b/%s/o/%s' % (SOURCE, KEY, DEST, NEW_NAME))
        self.assertEqual(kw['method'], 'POST')
        self.assertEqual(kw['path'], COPY_PATH)

    def test_upload_file_default_key(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import bucket as MUT
        BASENAME = 'file.ext'
        FILENAME = '/path/to/%s' % BASENAME
        _uploaded = []

        class _Key(object):

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            def upload_from_filename(self, filename):
                _uploaded.append((self._bucket, self._name, filename))

        bucket = self._makeOne()
        with _Monkey(MUT, Key=_Key):
            bucket.upload_file(FILENAME)
        self.assertEqual(_uploaded, [(bucket, BASENAME, FILENAME)])

    def test_upload_file_explicit_key(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import bucket as MUT
        FILENAME = '/path/to/file'
        KEY = 'key'
        _uploaded = []

        class _Key(object):

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            def upload_from_filename(self, filename):
                _uploaded.append((self._bucket, self._name, filename))

        bucket = self._makeOne()
        with _Monkey(MUT, Key=_Key):
            bucket.upload_file(FILENAME, KEY)
        self.assertEqual(_uploaded, [(bucket, KEY, FILENAME)])

    def test_upload_file_object_no_key(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import bucket as MUT
        FILENAME = 'file.txt'
        FILEOBJECT = MockFile(FILENAME)
        _uploaded = []

        class _Key(object):

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            def upload_from_file(self, fh):
                _uploaded.append((self._bucket, self._name, fh))

        bucket = self._makeOne()
        with _Monkey(MUT, Key=_Key):
            bucket.upload_file_object(FILEOBJECT)
        self.assertEqual(_uploaded, [(bucket, FILENAME, FILEOBJECT)])

    def test_upload_file_object_explicit_key(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import bucket as MUT
        FILENAME = 'file.txt'
        FILEOBJECT = MockFile(FILENAME)
        KEY = 'key'
        _uploaded = []

        class _Key(object):

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            def upload_from_file(self, fh):
                _uploaded.append((self._bucket, self._name, fh))

        bucket = self._makeOne()
        with _Monkey(MUT, Key=_Key):
            bucket.upload_file_object(FILEOBJECT, KEY)
        self.assertEqual(_uploaded, [(bucket, KEY, FILEOBJECT)])

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
        bucket = self._makeOne(connection, NAME, before)
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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME, before)
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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME, before)
        self.assertEqual(bucket.location, 'AS')
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_location_setter(self):
        NAME = 'name'
        connection = _Connection({'location': 'AS'})
        bucket = self._makeOne(connection, NAME)
        bucket.location = 'AS'
        self.assertEqual(bucket.location, 'AS')
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'location': 'AS'})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_get_logging_eager_w_prefix(self):
        NAME = 'name'
        LOG_BUCKET = 'logs'
        LOG_PREFIX = 'pfx'
        before = {
            'logging': {'logBucket': LOG_BUCKET,
                        'logObjectPrefix': LOG_PREFIX}}
        connection = _Connection()
        bucket = self._makeOne(connection, NAME, before)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info['logObjectPrefix'], LOG_PREFIX)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_get_logging_lazy_wo_prefix(self):
        NAME = 'name'
        LOG_BUCKET = 'logs'
        after = {'logging': {'logBucket': LOG_BUCKET}}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info.get('logObjectPrefix'), None)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_enable_logging_defaults(self):
        NAME = 'name'
        LOG_BUCKET = 'logs'
        before = {'logging': None}
        after = {'logging': {'logBucket': LOG_BUCKET, 'logObjectPrefix': ''}}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME, before)
        self.assertTrue(bucket.get_logging() is None)
        bucket.enable_logging(LOG_BUCKET)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info['logObjectPrefix'], '')
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], after)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_enable_logging_explicit(self):
        NAME = 'name'
        LOG_BUCKET = 'logs'
        LOG_PFX = 'pfx'
        before = {'logging': None}
        after = {
            'logging': {'logBucket': LOG_BUCKET, 'logObjectPrefix': LOG_PFX}}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME, before)
        self.assertTrue(bucket.get_logging() is None)
        bucket.enable_logging(LOG_BUCKET, LOG_PFX)
        info = bucket.get_logging()
        self.assertEqual(info['logBucket'], LOG_BUCKET)
        self.assertEqual(info['logObjectPrefix'], LOG_PFX)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], after)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_disable_logging(self):
        NAME = 'name'
        before = {'logging': {'logBucket': 'logs', 'logObjectPrefix': 'pfx'}}
        after = {'logging': None}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME, before)
        self.assertTrue(bucket.get_logging() is not None)
        bucket.disable_logging()
        self.assertTrue(bucket.get_logging() is None)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'logging': None})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME, before)
        self.assertEqual(bucket.versioning_enabled, True)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_versioning_enabled_setter(self):
        NAME = 'name'
        before = {'versioning': {'enabled': False}}
        after = {'versioning': {'enabled': True}}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME, before)
        self.assertFalse(bucket.versioning_enabled)
        bucket.versioning_enabled = True
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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME)
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
        bucket = self._makeOne(connection, NAME)
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
        from gcloud.storage.bucket import _KeyIterator
        _saved = []

        class _Key(object):
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

        class _Iterator(_KeyIterator):
            def get_items_from_response(self, response):
                for item in response.get('items', []):
                    yield _Key(self.bucket, item['name'])

        NAME = 'name'
        KEY = 'key'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive, 'defaultObjectAcl': []}
        connection = _Connection(after, {'items': [{'name': KEY}]})
        bucket = self._makeOne(connection, NAME)
        bucket.acl.loaded = True
        bucket.default_object_acl.loaded = True
        bucket._iterator_class = _Iterator
        bucket.make_public(recursive=True)
        self.assertEqual(list(bucket.acl), permissive)
        self.assertEqual(list(bucket.default_object_acl), [])
        self.assertEqual(_saved, [(bucket, KEY, True)])
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
    _delete_ok = False

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []
        self._deleted = []

    def api_request(self, **kw):
        from gcloud.storage.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response

    def delete_bucket(self, bucket, force=False):
        from gcloud.storage.exceptions import NotFound
        self._deleted.append((bucket, force))
        if not self._delete_ok:
            raise NotFound('miss')
        return True


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
