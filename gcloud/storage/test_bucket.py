import io

import unittest2


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
        self.assertEqual(bucket.metadata, None)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test_ctor_explicit(self):
        NAME = 'name'
        connection = _Connection()
        metadata = {'key': 'value'}
        bucket = self._makeOne(connection, NAME, metadata)
        self.assertTrue(bucket.connection is connection)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket.metadata, metadata)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test_from_dict_defaults(self):
        NAME = 'name'
        metadata = {'key': 'value', 'name': NAME}
        klass = self._getTargetClass()
        bucket = klass.from_dict(metadata)
        self.assertEqual(bucket.connection, None)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket.metadata, metadata)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

    def test_from_dict_explicit(self):
        NAME = 'name'
        connection = _Connection()
        metadata = {'key': 'value', 'name': NAME}
        klass = self._getTargetClass()
        bucket = klass.from_dict(metadata, connection)
        self.assertTrue(bucket.connection is connection)
        self.assertEqual(bucket.name, NAME)
        self.assertEqual(bucket.metadata, metadata)
        self.assertTrue(bucket._acl is None)
        self.assertTrue(bucket._default_object_acl is None)

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

    def test___iter___empty(self):
        NAME = 'name'
        connection = _Connection({'items': []})
        bucket = self._makeOne(connection, NAME)
        keys = list(bucket)
        self.assertEqual(keys, [])
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['path'], '/b/%s/o' % NAME)
        self.assertEqual(kw['query_params'], None)

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
        self.assertEqual(kw['query_params'], None)

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
        self.assertEqual(kw['query_params'], None)

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
        self.assertEqual(kw['query_params'], None)

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
        from gcloud.storage.exceptions import NotFoundError
        NAME = 'name'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        self.assertRaises(NotFoundError, bucket.delete)
        self.assertEqual(connection._deleted, [(NAME, False)])

    def test_delete_explicit_hit(self):
        NAME = 'name'
        connection = _Connection()
        connection._delete_ok = True
        bucket = self._makeOne(connection, NAME)
        self.assertTrue(bucket.delete(True))
        self.assertEqual(connection._deleted, [(NAME, True)])

    def test_delete_key_miss(self):
        from gcloud.storage.exceptions import NotFoundError
        NAME = 'name'
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        self.assertRaises(NotFoundError, bucket.delete_key, NONESUCH)
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
        from gcloud.storage.exceptions import NotFoundError
        NAME = 'name'
        KEY = 'key'
        NONESUCH = 'nonesuch'
        connection = _Connection({})
        bucket = self._makeOne(connection, NAME)
        self.assertRaises(NotFoundError, bucket.delete_keys, [KEY, NONESUCH])
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

            def set_contents_from_filename(self, filename):
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

            def set_contents_from_filename(self, filename):
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

            def set_contents_from_file(self, fh):
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

            def set_contents_from_file(self, fh):
                _uploaded.append((self._bucket, self._name, fh))
        bucket = self._makeOne()
        with _Monkey(MUT, Key=_Key):
            bucket.upload_file_object(FILEOBJECT, KEY)
        self.assertEqual(_uploaded, [(bucket, KEY, FILEOBJECT)])

    def test_has_metdata_none_set(self):
        NONESUCH = 'nonesuch'
        bucket = self._makeOne()
        self.assertFalse(bucket.has_metadata(NONESUCH))

    def test_has_metdata_miss(self):
        NONESUCH = 'nonesuch'
        metadata = {'key': 'value'}
        bucket = self._makeOne(metadata=metadata)
        self.assertFalse(bucket.has_metadata(NONESUCH))

    def test_has_metdata_none_passed(self):
        KEY = 'key'
        metadata = {KEY: 'value'}
        bucket = self._makeOne(metadata=metadata)
        self.assertTrue(bucket.has_metadata())

    def test_has_metdata_hit(self):
        KEY = 'key'
        metadata = {KEY: 'value'}
        bucket = self._makeOne(metadata=metadata)
        self.assertTrue(bucket.has_metadata(KEY))

    def test_reload_metadata(self):
        NAME = 'name'
        before = {'foo': 'Foo'}
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME, before)
        found = bucket.reload_metadata()
        self.assertTrue(found is bucket)
        self.assertEqual(found.metadata, after)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_get_metadata_none_set_none_passed(self):
        NAME = 'name'
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME)
        found = bucket.get_metadata()
        self.assertEqual(found, after)
        self.assertEqual(bucket.metadata, after)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_get_metadata_acl_no_default(self):
        NAME = 'name'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        self.assertRaises(KeyError, bucket.get_metadata, 'acl')
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_get_metadata_acl_w_default(self):
        NAME = 'name'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        default = object()
        self.assertRaises(KeyError, bucket.get_metadata, 'acl', default)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_get_metadata_defaultObjectAcl_no_default(self):
        NAME = 'name'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        self.assertRaises(KeyError, bucket.get_metadata, 'defaultObjectAcl')
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_get_metadata_none_set_defaultObjectAcl_miss_clear_default(self):
        NAME = 'name'
        connection = _Connection()
        bucket = self._makeOne(connection, NAME)
        default = object()
        self.assertRaises(KeyError, bucket.get_metadata, 'defaultObjectAcl',
                          default)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_get_metadata_miss(self):
        NAME = 'name'
        before = {'bar': 'Bar'}
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME, before)
        self.assertEqual(bucket.get_metadata('foo'), None)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_get_metadata_hit(self):
        NAME = 'name'
        before = {'bar': 'Bar'}
        connection = _Connection()
        bucket = self._makeOne(connection, NAME, before)
        self.assertEqual(bucket.get_metadata('bar'), 'Bar')
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_patch_metadata(self):
        NAME = 'name'
        before = {'foo': 'Foo'}
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME, before)
        self.assertTrue(bucket.patch_metadata(after) is bucket)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], after)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_configure_website_defaults(self):
        NAME = 'name'
        patched = {'website': {'mainPageSuffix': None,
                               'notFoundPage': None}}
        connection = _Connection(patched)
        bucket = self._makeOne(connection, NAME)
        self.assertTrue(bucket.configure_website() is bucket)
        self.assertEqual(bucket.metadata, patched)
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
        self.assertEqual(bucket.metadata, patched)
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
        self.assertEqual(bucket.metadata, patched)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], patched)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_reload_acl_eager_empty(self):
        from gcloud.storage.acl import BucketACL
        NAME = 'name'
        ROLE = 'role'
        connection = _Connection({'items': []})
        bucket = self._makeOne(connection, NAME)
        bucket.acl.entity('allUsers', ROLE)
        self.assertTrue(bucket.reload_acl() is bucket)
        self.assertTrue(isinstance(bucket.acl, BucketACL))
        self.assertEqual(list(bucket.acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s/acl' % NAME)

    def test_reload_acl_eager_nonempty(self):
        from gcloud.storage.acl import BucketACL
        NAME = 'name'
        ROLE = 'role'
        connection = _Connection(
            {'items': [{'entity': 'allUsers', 'role': ROLE}]})
        bucket = self._makeOne(connection, NAME)
        bucket.acl.loaded = True
        self.assertTrue(bucket.reload_acl() is bucket)
        self.assertTrue(isinstance(bucket.acl, BucketACL))
        self.assertEqual(list(bucket.acl),
                         [{'entity': 'allUsers', 'role': ROLE}])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s/acl' % NAME)

    def test_reload_acl_lazy(self):
        from gcloud.storage.acl import BucketACL
        NAME = 'name'
        ROLE = 'role'
        connection = _Connection(
            {'items': [{'entity': 'allUsers', 'role': ROLE}]})
        bucket = self._makeOne(connection, NAME)
        self.assertTrue(bucket.reload_acl() is bucket)
        self.assertTrue(isinstance(bucket.acl, BucketACL))
        self.assertEqual(list(bucket.acl),
                         [{'entity': 'allUsers', 'role': ROLE}])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s/acl' % NAME)

    def test_get_acl_lazy(self):
        from gcloud.storage.acl import BucketACL
        NAME = 'name'
        connection = _Connection({'items': []})
        bucket = self._makeOne(connection, NAME)
        acl = bucket.get_acl()
        self.assertTrue(acl is bucket.acl)
        self.assertTrue(isinstance(acl, BucketACL))
        self.assertEqual(list(bucket.acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s/acl' % NAME)

    def test_get_acl_eager(self):
        connection = _Connection()
        bucket = self._makeOne()
        preset = bucket.acl  # Ensure it is assigned
        preset.loaded = True
        acl = bucket.get_acl()
        self.assertTrue(acl is preset)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_save_acl_none_set_none_passed(self):
        connection = _Connection()
        bucket = self._makeOne()
        self.assertTrue(bucket.save_acl() is bucket)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_save_acl_existing_set_none_passed(self):
        NAME = 'name'
        connection = _Connection({'foo': 'Foo', 'acl': []})
        bucket = self._makeOne(connection, NAME)
        bucket.acl.loaded = True
        self.assertTrue(bucket.save_acl() is bucket)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'acl': []})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_save_acl_existing_set_new_passed(self):
        NAME = 'name'
        ROLE = 'role'
        new_acl = [{'entity': 'allUsers', 'role': ROLE}]
        connection = _Connection({'foo': 'Foo', 'acl': new_acl})
        bucket = self._makeOne(connection, NAME)
        bucket.acl.loaded = True
        self.assertTrue(bucket.save_acl(new_acl) is bucket)
        self.assertEqual(list(bucket.acl), new_acl)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'acl': new_acl})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_clear_acl(self):
        NAME = 'name'
        ROLE1 = 'role1'
        ROLE2 = 'role2'
        STICKY = {'entity': 'allUsers', 'role': ROLE2}
        connection = _Connection(
            # Emulate back-end, which makes some entries "sticky".
            {'foo': 'Foo', 'acl': [STICKY]},
            )
        bucket = self._makeOne(connection, NAME)
        bucket.acl.entity('allUsers', ROLE1)
        self.assertTrue(bucket.clear_acl() is bucket)
        self.assertEqual(list(bucket.acl), [STICKY])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'acl': []})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_reload_default_object_acl_eager_empty(self):
        from gcloud.storage.acl import DefaultObjectACL
        NAME = 'name'
        after = {'items': []}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME)
        bucket.default_object_acl.loaded = True
        self.assertTrue(bucket.reload_default_object_acl() is bucket)
        self.assertTrue(
            isinstance(bucket.default_object_acl, DefaultObjectACL))
        self.assertEqual(list(bucket.default_object_acl), [])

    def test_reload_default_object_acl_eager_nonempty(self):
        from gcloud.storage.acl import DefaultObjectACL
        NAME = 'name'
        ROLE = 'role'
        after = {'items': [{'entity': 'allUsers', 'role': ROLE}]}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME)
        bucket.default_object_acl.entity('allUsers', 'OTHERROLE')
        self.assertTrue(bucket.reload_default_object_acl() is bucket)
        self.assertTrue(
            isinstance(bucket.default_object_acl, DefaultObjectACL))
        self.assertEqual(list(bucket.default_object_acl),
                         [{'entity': 'allUsers', 'role': ROLE}])

    def test_reload_default_object_acl_lazy(self):
        from gcloud.storage.acl import DefaultObjectACL
        NAME = 'name'
        ROLE = 'role'
        after = {'items': [{'entity': 'allUsers', 'role': ROLE}]}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME)
        self.assertTrue(bucket.reload_default_object_acl() is bucket)
        self.assertTrue(
            isinstance(bucket.default_object_acl, DefaultObjectACL))
        self.assertEqual(list(bucket.default_object_acl),
                         [{'entity': 'allUsers', 'role': ROLE}])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/%s/defaultObjectAcl' % NAME)

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

    def test_save_default_object_acl_none_set_none_passed(self):
        connection = _Connection()
        bucket = self._makeOne()
        self.assertTrue(bucket.save_default_object_acl() is bucket)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_save_default_object_acl_existing_set_none_passed(self):
        NAME = 'name'
        connection = _Connection(
            {'foo': 'Foo', 'acl': [], 'defaultObjectAcl': []},
        )
        bucket = self._makeOne(connection, NAME)
        bucket.default_object_acl.loaded = True
        self.assertTrue(bucket.save_default_object_acl() is bucket)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'defaultObjectAcl': []})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_save_default_object_acl_existing_set_new_passed(self):
        NAME = 'name'
        ROLE = 'role'
        new_acl = [{'entity': 'allUsers', 'role': ROLE}]
        connection = _Connection(
            {'foo': 'Foo', 'acl': new_acl, 'defaultObjectAcl': new_acl},
        )
        metadata = {'defaultObjectAcl': []}
        bucket = self._makeOne(connection, NAME, metadata)
        bucket.default_object_acl.loaded = True
        self.assertTrue(bucket.save_default_object_acl(new_acl) is bucket)
        self.assertEqual(list(bucket.default_object_acl), new_acl)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'defaultObjectAcl': new_acl})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_clear_default_object_acl(self):
        NAME = 'name'
        ROLE = 'role'
        connection = _Connection(
            {'foo': 'Foo', 'acl': [], 'defaultObjectAcl': []},
        )
        bucket = self._makeOne(connection, NAME)
        bucket.default_object_acl.entity('allUsers', ROLE)
        self.assertTrue(bucket.clear_default_object_acl() is bucket)
        self.assertEqual(list(bucket.default_object_acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/%s' % NAME)
        self.assertEqual(kw[0]['data'], {'defaultObjectAcl': []})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_make_public_defaults(self):
        from gcloud.storage.acl import _ACLEntity
        NAME = 'name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive, 'defaultObjectAcl': []}
        connection = _Connection(after)
        bucket = self._makeOne(connection, NAME)
        bucket.acl.loaded = True
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
        from gcloud._testing import _Monkey
        from gcloud.storage import key
        from gcloud.storage import bucket as MUT
        _saved = []

        class _Key(object):
            _granted = False

            def __init__(self, bucket, name):
                self._bucket = bucket
                self._name = name

            def get_acl(self):
                return self

            def all(self):
                return self

            def grant_read(self):
                self._granted = True

            def save_acl(self):
                _saved.append((self._bucket, self._name, self._granted))

        class _KeyIterator(key._KeyIterator):
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
        with _Monkey(MUT, _KeyIterator=_KeyIterator):
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
        self.assertEqual(kw[1]['query_params'], None)


class TestBucketIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.bucket import BucketIterator
        return BucketIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        iterator = self._makeOne(connection)
        self.assertTrue(iterator.connection is connection)
        self.assertEqual(iterator.path, '/b')
        self.assertEqual(iterator.page_number, 0)
        self.assertEqual(iterator.next_page_token, None)

    def test_get_items_from_response_empty(self):
        connection = _Connection()
        iterator = self._makeOne(connection)
        self.assertEqual(list(iterator.get_items_from_response({})), [])

    def test_get_items_from_response_non_empty(self):
        from gcloud.storage.bucket import Bucket
        KEY = 'key'
        response = {'items': [{'name': KEY}]}
        connection = _Connection()
        iterator = self._makeOne(connection)
        buckets = list(iterator.get_items_from_response(response))
        self.assertEqual(len(buckets), 1)
        bucket = buckets[0]
        self.assertTrue(isinstance(bucket, Bucket))
        self.assertTrue(bucket.connection is connection)
        self.assertEqual(bucket.name, KEY)


class _Connection(object):
    _delete_ok = False

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []
        self._deleted = []

    def api_request(self, **kw):
        from gcloud.storage.exceptions import NotFoundError
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFoundError('miss')
        else:
            return response

    def delete_bucket(self, bucket, force=False):
        from gcloud.storage.exceptions import NotFoundError
        self._deleted.append((bucket, force))
        if not self._delete_ok:
            raise NotFoundError('miss')
        return True


class MockFile(io.StringIO):
    name = None

    def __init__(self, name, buffer_=None):
        super(MockFile, self).__init__(buffer_)
        self.name = name
