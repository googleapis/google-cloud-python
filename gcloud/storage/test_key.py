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
        self.assertTrue(key._acl is None)

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
        self.assertTrue(key._acl is None)

    def test_from_dict_defaults(self):
        KEY = 'key'
        metadata = {'key': 'value', 'name': KEY}
        klass = self._getTargetClass()
        key = klass.from_dict(metadata)
        self.assertEqual(key.bucket, None)
        self.assertEqual(key.connection, None)
        self.assertEqual(key.name, KEY)
        self.assertEqual(key.metadata, metadata)
        self.assertTrue(key._acl is None)

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
        self.assertTrue(key._acl is None)

    def test_acl_property(self):
        from gcloud.storage.acl import ObjectACL
        key = self._makeOne()
        acl = key.acl
        self.assertTrue(isinstance(acl, ObjectACL))
        self.assertTrue(acl is key._acl)

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

    def test_generate_signed_url_w_default_method(self):
        KEY = 'key'
        EXPIRATION = '2014-10-16T20:34:37Z'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.generate_signed_url(EXPIRATION),
                         'http://example.com/abucket/akey?Signature=DEADBEEF'
                         '&Expiration=2014-10-16T20:34:37Z')
        self.assertEqual(connection._signed,
                         [('/name/key', EXPIRATION, {'method': 'GET'})])

    def test_generate_signed_url_w_explicit_method(self):
        KEY = 'key'
        EXPIRATION = '2014-10-16T20:34:37Z'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertEqual(key.generate_signed_url(EXPIRATION, method='POST'),
                         'http://example.com/abucket/akey?Signature=DEADBEEF'
                         '&Expiration=2014-10-16T20:34:37Z')
        self.assertEqual(connection._signed,
                         [('/name/key', EXPIRATION, {'method': 'POST'})])

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

    def test_download_to_file(self):
        from StringIO import StringIO
        from gcloud._testing import _Monkey
        from gcloud.storage import key as MUT
        _CHUNKS = ['abc', 'def']
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        fh = StringIO()
        with _Monkey(MUT, _KeyDataIterator=lambda self: iter(_CHUNKS)):
            key.download_to_file(fh)
        self.assertEqual(fh.getvalue(), ''.join(_CHUNKS))

    def test_download_to_filename(self):
        from tempfile import NamedTemporaryFile
        from gcloud._testing import _Monkey
        from gcloud.storage import key as MUT
        _CHUNKS = ['abc', 'def']
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        with _Monkey(MUT, _KeyDataIterator=lambda self: iter(_CHUNKS)):
            with NamedTemporaryFile() as f:
                key.download_to_filename(f.name)
                f.flush()
                with open(f.name) as g:
                    wrote = g.read()
        self.assertEqual(wrote, ''.join(_CHUNKS))

    def test_download_as_string(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import key as MUT
        _CHUNKS = ['abc', 'def']
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        with _Monkey(MUT, _KeyDataIterator=lambda self: iter(_CHUNKS)):
            fetched = key.download_as_string()
        self.assertEqual(fetched, ''.join(_CHUNKS))

    def test_upload_from_file(self):
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        KEY = 'key'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'location': UPLOAD_URL}
        chunk1_response = {}
        chunk2_response = {}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        with NamedTemporaryFile() as fh:
            fh.write(DATA)
            fh.flush()
            key.upload_from_file(fh, rewind=True)
        rq = connection._requested
        self.assertEqual(len(rq), 3)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['url']
        scheme, netloc, path, qs, _ = urlsplit(uri)
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

    def test_upload_from_filename(self):
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        KEY = 'key'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'location': UPLOAD_URL}
        chunk1_response = {}
        chunk2_response = {}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        with NamedTemporaryFile(suffix='.jpeg') as fh:
            fh.write(DATA)
            fh.flush()
            key.upload_from_filename(fh.name)
        rq = connection._requested
        self.assertEqual(len(rq), 3)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['url']
        scheme, netloc, path, qs, _ = urlsplit(uri)
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

    def test_upload_from_string(self):
        from urlparse import parse_qsl
        from urlparse import urlsplit
        KEY = 'key'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'location': UPLOAD_URL}
        chunk1_response = {}
        chunk2_response = {}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.CHUNK_SIZE = 5
        key.upload_from_string(DATA)
        rq = connection._requested
        self.assertEqual(len(rq), 3)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['url']
        scheme, netloc, path, qs, _ = urlsplit(uri)
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

    def test_reload_metadata(self):
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

    def test_get_metadata_acl_no_default(self):
        KEY = 'key'
        connection = _Connection()
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        self.assertRaises(KeyError, key.get_metadata, 'acl')
        kw = connection._requested
        self.assertEqual(len(kw), 0)

    def test_get_metadata_acl_w_default(self):
        KEY = 'key'
        after = {'bar': 'Bar'}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        default = object()
        self.assertRaises(KeyError, key.get_metadata, 'acl', default)
        kw = connection._requested
        self.assertEqual(len(kw), 0)

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
        KEY = 'key'
        ROLE = 'role'
        after = {'items': [{'entity': 'allUsers', 'role': ROLE}]}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.acl.loaded = True
        self.assertTrue(key.reload_acl() is key)
        self.assertTrue(isinstance(key.acl, ObjectACL))
        self.assertEqual(list(key.acl), after['items'])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s/acl' % KEY)

    def test_reload_acl_eager_nonempty(self):
        from gcloud.storage.acl import ObjectACL
        KEY = 'key'
        ROLE = 'role'
        after = {'items': []}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.acl.entity('allUsers', ROLE)
        self.assertTrue(key.reload_acl() is key)
        self.assertTrue(isinstance(key.acl, ObjectACL))
        self.assertEqual(list(key.acl), [])

    def test_reload_acl_lazy(self):
        from gcloud.storage.acl import ObjectACL
        KEY = 'key'
        ROLE = 'role'
        after = {'items': [{'entity': 'allUsers', 'role': ROLE}]}
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
        self.assertEqual(kw[0]['path'], '/b/name/o/%s/acl' % KEY)

    def test_get_acl_lazy(self):
        from gcloud.storage.acl import ObjectACL
        KEY = 'key'
        connection = _Connection({'items': []})
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        acl = key.get_acl()
        self.assertTrue(acl is key.acl)
        self.assertTrue(isinstance(acl, ObjectACL))
        self.assertEqual(list(key.acl), [])

    def test_get_acl_eager(self):
        key = self._makeOne()
        preset = key.acl
        preset.loaded = True
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
        key = self._makeOne(bucket, KEY)
        key.acl.loaded = True
        self.assertTrue(key.save_acl() is key)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], {'acl': []})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_save_acl_existing_set_new_passed(self):
        KEY = 'key'
        ROLE = 'role'
        new_acl = [{'entity': 'allUsers', 'role': ROLE}]
        connection = _Connection({'foo': 'Foo', 'acl': new_acl})
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.acl.entity('allUsers', 'other-role')
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
        connection = _Connection({'foo': 'Foo', 'acl': []})
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.acl.entity('allUsers', ROLE)
        self.assertTrue(key.clear_acl() is key)
        self.assertEqual(list(key.acl), [])
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], {'acl': []})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_make_public(self):
        from gcloud.storage.acl import _ACLEntity
        KEY = 'key'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        key = self._makeOne(bucket, KEY)
        key.acl.loaded = True
        key.make_public()
        self.assertEqual(list(key.acl), permissive)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % KEY)
        self.assertEqual(kw[0]['data'], {'acl': permissive})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})


class Test__KeyIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.key import _KeyIterator
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

    def test_get_items_from_response_empty(self):
        connection = _Connection()
        bucket = _Bucket(connection)
        iterator = self._makeOne(bucket)
        self.assertEqual(list(iterator.get_items_from_response({})), [])

    def test_get_items_from_response_non_empty(self):
        from gcloud.storage.key import Key
        KEY = 'key'
        response = {'items': [{'name': KEY}]}
        connection = _Connection()
        bucket = _Bucket(connection)
        iterator = self._makeOne(bucket)
        keys = list(iterator.get_items_from_response(response))
        self.assertEqual(len(keys), 1)
        key = keys[0]
        self.assertTrue(isinstance(key, Key))
        self.assertTrue(key.connection is connection)
        self.assertEqual(key.name, KEY)


class Test__KeyDataIterator(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage.key import _KeyDataIterator
        return _KeyDataIterator

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        self.assertTrue(iterator.key is key)
        self.assertEqual(iterator._bytes_written, 0)
        self.assertEqual(iterator._total_bytes, None)

    def test__iter__(self):
        response1 = _Response(status=200)
        response1['content-range'] = '0-9/15'
        response2 = _Response(status=200)
        response2['content-range'] = '10-14/15'
        connection = _Connection(
            (response1, '0123456789'),
            (response2, '01234'),
        )
        key = _Key(connection)
        iterator = self._makeOne(key)
        chunks = list(iterator)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0], '0123456789')
        self.assertEqual(chunks[1], '01234')
        self.assertEqual(iterator._bytes_written, 15)
        self.assertEqual(iterator._total_bytes, 15)
        kws = connection._requested
        self.assertEqual(kws[0]['method'], 'GET')
        self.assertEqual(kws[0]['url'],
                         'http://example.com/b/name/o/key?alt=media')
        self.assertEqual(kws[0]['headers'], {'Range': 'bytes=0-9'})
        self.assertEqual(kws[1]['method'], 'GET')
        self.assertEqual(kws[1]['url'],
                         'http://example.com/b/name/o/key?alt=media')
        self.assertEqual(kws[1]['headers'], {'Range': 'bytes=10-'})

    def test_reset(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 10
        iterator._total_bytes = 1000
        iterator.reset()
        self.assertEqual(iterator._bytes_written, 0)
        self.assertEqual(iterator._total_bytes, None)

    def test_has_more_data_new(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        self.assertTrue(iterator.has_more_data())

    def test_has_more_data_invalid(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 10  # no _total_bytes.
        self.assertRaises(ValueError, iterator.has_more_data)

    def test_has_more_data_true(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 10
        iterator._total_bytes = 1000
        self.assertTrue(iterator.has_more_data())

    def test_has_more_data_false(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 1000
        iterator._total_bytes = 1000
        self.assertFalse(iterator.has_more_data())

    def test_get_headers_new(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        headers = iterator.get_headers()
        self.assertEqual(len(headers), 1)
        self.assertEqual(headers['Range'], 'bytes=0-9')

    def test_get_headers_ok(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 10
        iterator._total_bytes = 1000
        headers = iterator.get_headers()
        self.assertEqual(len(headers), 1)
        self.assertEqual(headers['Range'], 'bytes=10-19')

    def test_get_headers_off_end(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = 95
        iterator._total_bytes = 100
        headers = iterator.get_headers()
        self.assertEqual(len(headers), 1)
        self.assertEqual(headers['Range'], 'bytes=95-')

    def test_get_url(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        self.assertEqual(iterator.get_url(),
                         'http://example.com/b/name/o/key?alt=media')

    def test_get_next_chunk_underflow(self):
        connection = _Connection()
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._bytes_written = iterator._total_bytes = 10
        self.assertRaises(RuntimeError, iterator.get_next_chunk)

    def test_get_next_chunk_200(self):
        response = _Response(status=200)
        response['content-range'] = '0-9/100'
        connection = _Connection((response, 'CHUNK'))
        key = _Key(connection)
        iterator = self._makeOne(key)
        chunk = iterator.get_next_chunk()
        self.assertEqual(chunk, 'CHUNK')
        self.assertEqual(iterator._bytes_written, len(chunk))
        self.assertEqual(iterator._total_bytes, 100)
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['url'],
                         'http://example.com/b/name/o/key?alt=media')
        self.assertEqual(kw['headers'], {'Range': 'bytes=0-9'})

    def test_get_next_chunk_206(self):
        response = _Response(status=206)
        connection = _Connection((response, 'CHUNK'))
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._total_bytes = 1000
        chunk = iterator.get_next_chunk()
        self.assertEqual(chunk, 'CHUNK')
        self.assertEqual(iterator._bytes_written, len(chunk))
        kw, = connection._requested
        self.assertEqual(kw['method'], 'GET')
        self.assertEqual(kw['url'],
                         'http://example.com/b/name/o/key?alt=media')
        self.assertEqual(kw['headers'], {'Range': 'bytes=0-9'})

    def test_get_next_chunk_416(self):
        from gcloud.storage.exceptions import StorageError
        response = _Response(status=416)
        connection = _Connection((response, ''))
        key = _Key(connection)
        iterator = self._makeOne(key)
        iterator._total_bytes = 1000
        self.assertRaises(StorageError, iterator.get_next_chunk)


class _Connection(object):
    API_BASE_URL = 'http://example.com'

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []
        self._signed = []

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

    def generate_signed_url(self, resource, expiration, **kw):
        self._signed.append((resource, expiration, kw))
        return ('http://example.com/abucket/akey?Signature=DEADBEEF'
                '&Expiration=%s' % expiration)


class _Key(object):
    CHUNK_SIZE = 10
    path = '/b/name/o/key'

    def __init__(self, connection):
        self.connection = connection


class _Bucket(object):
    path = '/b/name'
    name = 'name'

    def __init__(self, connection):
        self.connection = connection
        self._keys = {}
        self._deleted = []

    def get_key(self, key):
        return self._keys.get(key)

    def copy_key(self, key, destination_bucket, new_name):
        destination_bucket._keys[new_name] = self._keys[key.name]
        return key.from_dict({'name': new_name}, bucket=destination_bucket)

    def delete_key(self, key):
        del self._keys[key.name]
        self._deleted.append(key.name)


class _Response(dict):
    @property
    def status(self):
        return self['status']
