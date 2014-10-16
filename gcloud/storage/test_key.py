import unittest2


class Test_Key(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.key import Key
        return Key

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        key = self._makeOne()
        self.assertEqual(key.bucket, None)
        self.assertEqual(key.connection, None)
        self.assertEqual(key.name, None)
        self.assertEqual(key.metadata, {})
        self.assertEqual(key.acl, None)

    def test_ctor_explicit(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        metadata = {'key': 'value'}
        key = self._makeOne(bucket, KEY, metadata)
        self.assertTrue(key.bucket is bucket)
        self.assertTrue(key.connection is connection)
        self.assertEqual(key.name, KEY)
        self.assertEqual(key.metadata, metadata)
        self.assertEqual(key.acl, None)

    def test_from_dict_defaults(self):
        KEY = 'key'
        metadata = {'key': 'value', 'name': KEY}
        klass = self._getTargetClass()
        key = klass.from_dict(metadata)
        self.assertEqual(key.bucket, None)
        self.assertEqual(key.connection, None)
        self.assertEqual(key.name, KEY)
        self.assertEqual(key.metadata, metadata)
        self.assertEqual(key.acl, None)

    def test_from_dict_explicit(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        metadata = {'key': 'value', 'name': KEY}
        klass = self._getTargetClass()
        key = klass.from_dict(metadata, bucket)
        self.assertTrue(key.bucket is bucket)
        self.assertTrue(key.connection is connection)
        self.assertEqual(key.name, KEY)
        self.assertEqual(key.metadata, metadata)
        self.assertEqual(key.acl, None)

    def test_path_no_bucket(self):
        key = self._makeOne()
        self.assertRaises(ValueError, getattr, key, 'path')

    def test_path_no_name(self):
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket)
        self.assertRaises(ValueError, getattr, key, 'path')

    def test_path_normal(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.path, '/b/name/o/%s' % KEY)

    def test_public_url(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.public_url,
                         'http://commondatastorage.googleapis.com/name/%s' %
                         KEY)

    def test_exists_miss(self):
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, NONESUCH)
        self.assertFalse(key.exists())

    def test_exists_hit(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        bucket._keys[KEY] = 1
        self.assertTrue(key.exists())

    def test_rename(self):
        KEY = 'key'
        NEW_NAME = 'new-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        bucket._keys[KEY] = 1
        orig_key_path = key.path
        new_key = key.rename(NEW_NAME)
        self.assertEqual(key.name, KEY)
        self.assertEqual(new_key.name, NEW_NAME)
        self.assertFalse(KEY in bucket._keys)
        self.assertTrue(KEY in bucket._deleted)
        self.assertTrue(NEW_NAME in bucket._keys)

    def test_delete(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        bucket._keys[KEY] = 1
        key.delete()
        self.assertFalse(key.exists())

    def test_get_contents_to_file(self):
        from StringIO import StringIO
        from gcloud._testing import _Monkey
        from gcloud.storage import key as MUT
        _CHUNKS = ['abc', 'def']
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        fh = StringIO()
        with _Monkey(MUT, KeyDataIterator=lambda self: iter(_CHUNKS)):
            key.get_contents_to_file(fh)
        self.assertEqual(fh.getvalue(), ''.join(_CHUNKS))

    def test_get_contents_to_filename(self):
        from tempfile import NamedTemporaryFile
        from gcloud._testing import _Monkey
        from gcloud.storage import key as MUT
        _CHUNKS = ['abc', 'def']
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        with _Monkey(MUT, KeyDataIterator=lambda self: iter(_CHUNKS)):
            with NamedTemporaryFile() as f:
                key.get_contents_to_filename(f.name)
                f.flush()
                with open(f.name) as g:
                    wrote = g.read()
        self.assertEqual(wrote, ''.join(_CHUNKS))

    def test_get_contents_as_string(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import key as MUT
        _CHUNKS = ['abc', 'def']
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        with _Monkey(MUT, KeyDataIterator=lambda self: iter(_CHUNKS)):
            fetched = key.get_contents_as_string()
        self.assertEqual(fetched, ''.join(_CHUNKS))

    def test_set_contents_from_file(self):
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        KEY = 'key'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'location': UPLOAD_URL}
        chunk1_response = {}
        chunk2_response = {}
        connection = _Connection((loc_response, ''),
                                 (chunk1_response, ''),
                                 (chunk2_response, ''),
                                 )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        with NamedTemporaryFile() as fh:
            fh.write(DATA)
            fh.flush()
            key.set_contents_from_file(fh, rewind=True)
        rq = connection._requested
        self.assertEqual(len(rq), 3)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['url']
        scheme, netloc, path, qs, frag = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable', 'name': 'key'})
        self.assertEqual(rq[0]['headers'],
                         {'X-Upload-Content-Length': 6,
                          'X-Upload-Content-Type': 'application/unknown'})
        self.assertEqual(rq[1]['method'], 'POST')
        self.assertEqual(rq[1]['url'], UPLOAD_URL)
        self.assertEqual(rq[1]['content_type'], 'text/plain')
        self.assertEqual(rq[1]['data'], DATA[:5])
        self.assertEqual(rq[1]['headers'], {'Content-Range': 'bytes 0-4/6'})
        self.assertEqual(rq[2]['method'], 'POST')
        self.assertEqual(rq[2]['url'], UPLOAD_URL)
        self.assertEqual(rq[2]['content_type'], 'text/plain')
        self.assertEqual(rq[2]['data'], DATA[5:])
        self.assertEqual(rq[2]['headers'], {'Content-Range': 'bytes 5-5/6'})

    def test_set_contents_from_filename(self):
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        KEY = 'key'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'location': UPLOAD_URL}
        chunk1_response = {}
        chunk2_response = {}
        connection = _Connection((loc_response, ''),
                                 (chunk1_response, ''),
                                 (chunk2_response, ''),
                                 )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        with NamedTemporaryFile(suffix='.jpeg') as fh:
            fh.write(DATA)
            fh.flush()
            key.set_contents_from_filename(fh.name)
        rq = connection._requested
        self.assertEqual(len(rq), 3)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['url']
        scheme, netloc, path, qs, frag = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable', 'name': 'key'})
        self.assertEqual(rq[0]['headers'],
                         {'X-Upload-Content-Length': 6,
                          'X-Upload-Content-Type': 'image/jpeg'})
        self.assertEqual(rq[1]['method'], 'POST')
        self.assertEqual(rq[1]['url'], UPLOAD_URL)
        self.assertEqual(rq[1]['content_type'], 'text/plain')
        self.assertEqual(rq[1]['data'], DATA[:5])
        self.assertEqual(rq[1]['headers'], {'Content-Range': 'bytes 0-4/6'})
        self.assertEqual(rq[2]['method'], 'POST')
        self.assertEqual(rq[2]['url'], UPLOAD_URL)
        self.assertEqual(rq[2]['content_type'], 'text/plain')
        self.assertEqual(rq[2]['data'], DATA[5:])
        self.assertEqual(rq[2]['headers'], {'Content-Range': 'bytes 5-5/6'})

    def test_set_contents_from_string(self):
        from urlparse import parse_qsl
        from urlparse import urlsplit
        KEY = 'key'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'location': UPLOAD_URL}
        chunk1_response = {}
        chunk2_response = {}
        connection = _Connection((loc_response, ''),
                                 (chunk1_response, ''),
                                 (chunk2_response, ''),
                                 )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        key.set_contents_from_string(DATA)
        rq = connection._requested
        self.assertEqual(len(rq), 3)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['url']
        scheme, netloc, path, qs, frag = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable', 'name': 'key'})
        self.assertEqual(rq[0]['headers'],
                         {'X-Upload-Content-Length': 6,
                          'X-Upload-Content-Type': 'text/plain'})
        self.assertEqual(rq[1]['method'], 'POST')
        self.assertEqual(rq[1]['url'], UPLOAD_URL)
        self.assertEqual(rq[1]['content_type'], 'text/plain')
        self.assertEqual(rq[1]['data'], DATA[:5])
        self.assertEqual(rq[1]['headers'], {'Content-Range': 'bytes 0-4/6'})
        self.assertEqual(rq[2]['method'], 'POST')
        self.assertEqual(rq[2]['url'], UPLOAD_URL)
        self.assertEqual(rq[2]['content_type'], 'text/plain')
        self.assertEqual(rq[2]['data'], DATA[5:])
        self.assertEqual(rq[2]['headers'], {'Content-Range': 'bytes 5-5/6'})

    def test_has_metdata_none_set(self):
        NONESUCH = 'nonesuch'
        key = self._makeOne()
        self.assertFalse(key.has_metadata(NONESUCH))

    def test_has_metdata_miss(self):
        NONESUCH = 'nonesuch'
        metadata = {'key': 'value'}
        key = self._makeOne(metadata=metadata)
        self.assertFalse(key.has_metadata(NONESUCH))

    def test_has_metdata_none_passed(self):
        KEY = 'key'
        metadata = {KEY: 'value'}
        key = self._makeOne(metadata=metadata)
        self.assertTrue(key.has_metadata())

    def test_has_metdata_hit(self):
        KEY = 'key'
        metadata = {KEY: 'value'}
        key = self._makeOne(metadata=metadata)
        self.assertTrue(key.has_metadata(KEY))

    def test_reload_metadata_default(self):
        KEY = 'key'
        before = {'foo': 'Foo'}
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY, before)
        found = key.reload_metadata()
        self.assertTrue(found is key)
        self.assertEqual(found.metadata, after)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_reload_metadata_explicit(self):
        KEY = 'key'
        before = {'foo': 'Foo'}
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY, before)
        found = key.reload_metadata(True)
        self.assertTrue(found is key)
        self.assertEqual(found.metadata, after)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_get_metadata_none_set_none_passed(self):
        KEY = 'key'
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        found = key.get_metadata()
        self.assertEqual(found, after)
        self.assertEqual(key.metadata, after)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_get_metadata_none_set_acl_hit(self):
        KEY = 'key'
        after = {'bar': 'Bar', 'acl': []}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        found = key.get_metadata('acl')
        self.assertEqual(found, [])
        self.assertEqual(key.metadata, after)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_get_metadata_none_set_acl_miss_explicit_default(self):
        KEY = 'key'
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        default = object()
        found = key.get_metadata('acl', default)
        self.assertTrue(found is default)
        self.assertEqual(key.metadata, after)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_get_metadata_miss(self):
        KEY = 'key'
        before = {'bar': 'Bar'}
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY, before)
        self.assertEqual(key.get_metadata('foo'), None)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_get_metadata_hit(self):
        KEY = 'key'
        before = {'bar': 'Bar'}
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY, before)
        self.assertEqual(key.get_metadata('bar'), 'Bar')
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_patch_metadata(self):
        KEY = 'key'
        before = {'foo': 'Foo'}
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY, before)
        self.assertTrue(key.patch_metadata(after) is key)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], after)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_reload_acl_eager_empty(self):
        from gcloud.storage.acl import ObjectACL
        metadata = {'acl': []}
        key = self._makeOne(metadata=metadata)
        self.assertTrue(key.reload_acl() is key)
        self.assertTrue(isinstance(key.acl, ObjectACL))
        self.assertEqual(list(key.acl), [])

    def test_reload_acl_eager_nonempty(self):
        from gcloud.storage.acl import ObjectACL
        ROLE = 'role'
        metadata = {'acl': [{'entity': 'allUsers', 'role': ROLE}]}
        key = self._makeOne(metadata=metadata)
        self.assertTrue(key.reload_acl() is key)
        self.assertTrue(isinstance(key.acl, ObjectACL))
        self.assertEqual(list(key.acl),
                         [{'entity': 'allUsers', 'role': ROLE}])

    def test_reload_acl_lazy(self):
        from gcloud.storage.acl import ObjectACL
        KEY = 'key'
        ROLE = 'role'
        after = {'acl': [{'entity': 'allUsers', 'role': ROLE}]}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertTrue(key.reload_acl() is key)
        self.assertTrue(isinstance(key.acl, ObjectACL))
        self.assertEqual(list(key.acl),
                         [{'entity': 'allUsers', 'role': ROLE}])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_get_acl_lazy(self):
        from gcloud.storage.acl import ObjectACL
        metadata = {'acl': []}
        key = self._makeOne(metadata=metadata)
        acl = key.get_acl()
        self.assertTrue(acl is key.acl)
        self.assertTrue(isinstance(acl, ObjectACL))
        self.assertEqual(list(key.acl), [])

    def test_get_acl_eager(self):
        from gcloud.storage.acl import ObjectACL
        key = self._makeOne()
        preset = key.acl = ObjectACL(key)
        acl = key.get_acl()
        self.assertTrue(acl is preset)

    def test_save_acl_none_set_none_passed(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertTrue(key.save_acl() is key)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_save_acl_existing_set_none_passed(self):
        KEY = 'key'
        connection = _Connection({'foo': 'Foo', 'acl': []})
        bucket = _Bucket(connection)
        metadata = {'acl': []}
        key = self._makeOne(bucket, KEY, metadata)
        key.reload_acl()
        self.assertTrue(key.save_acl() is key)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], metadata)
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_save_acl_existing_set_new_passed(self):
        KEY = 'key'
        ROLE = 'role'
        new_acl = [{'entity': 'allUsers', 'role': ROLE}]
        connection = _Connection({'foo': 'Foo', 'acl': new_acl})
        bucket = _Bucket(connection)
        metadata = {'acl': []}
        key = self._makeOne(bucket, KEY, metadata)
        key.reload_acl()
        self.assertTrue(key.save_acl(new_acl) is key)
        self.assertEqual(list(key.acl), new_acl)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], {'acl': new_acl})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_clear_acl(self):
        KEY = 'key'
        ROLE = 'role'
        old_acl = [{'entity': 'allUsers', 'role': ROLE}]
        connection = _Connection({'foo': 'Foo', 'acl': []})
        bucket = _Bucket(connection)
        metadata = {'acl': old_acl}
        key = self._makeOne(bucket, KEY, metadata)
        key.reload_acl()
        self.assertTrue(key.clear_acl() is key)
        self.assertEqual(list(key.acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], {'acl': []})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_make_public(self):
        from gcloud.storage.acl import ACL
        KEY = 'key'
        before = {'acl': []}
        permissive = [{'entity': 'allUsers', 'role': ACL.Role.Reader}]
        after = {'acl': permissive}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY, before)
        key.make_public()
        self.assertEqual(key.metadata, after)
        self.assertEqual(list(key.acl), after['acl'])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], {'acl': after['acl']})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})


class _Connection(object):
    API_BASE_URL = 'http://example.com'

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def make_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response

    def build_api_url(self, path, query_params=None,
                      api_base_url=API_BASE_URL):
        from urllib import urlencode
        from urlparse import urlsplit
        from urlparse import urlunsplit
        qs = urlencode(query_params or {})
        scheme, netloc, _, _, _ = urlsplit(api_base_url)
        return urlunsplit((scheme, netloc, path, qs, ''))


class _Bucket(object):
    path = '/b/name'
    name = 'name'

    def __init__(self, connection):
        self.connection = connection
        self._keys = {}
        self._deleted = []

    def get_key(self, key):
        return self._keys.get(key)  # XXX s.b. 'key.name'?

    def copy_key(self, key, destination_bucket, new_name):
        destination_bucket._keys[new_name] = self._keys[key.name]
        return key.from_dict({'name': new_name}, bucket=destination_bucket)

    def delete_key(self, key):
        del self._keys[key.name]  # XXX s.b. 'key'?
        self._deleted.append(key.name)
