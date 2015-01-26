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


class Test_Blob(unittest2.TestCase):

    def _makeOne(self, *args, **kw):
        from gcloud.storage.blob import Blob
        return Blob(*args, **kw)

    def test_ctor_defaults(self):
        blob = self._makeOne()
        self.assertEqual(blob.bucket, None)
        self.assertEqual(blob.connection, None)
        self.assertEqual(blob.name, None)
        self.assertEqual(blob._properties, {})
        self.assertTrue(blob._acl is None)

    def test_ctor_explicit(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        properties = {'key': 'value'}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertTrue(blob.bucket is bucket)
        self.assertTrue(blob.connection is connection)
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(blob.properties, properties)
        self.assertTrue(blob._acl is None)

    def test_ctor_no_name_defaults(self):
        BLOB_NAME = 'blob-name'
        properties = {'key': 'value', 'name': BLOB_NAME}
        blob = self._makeOne(properties=properties)
        self.assertEqual(blob.bucket, None)
        self.assertEqual(blob.connection, None)
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(blob.properties, properties)
        self.assertTrue(blob._acl is None)

    def test_ctor_no_name_explicit(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        properties = {'key': 'value', 'name': BLOB_NAME}
        blob = self._makeOne(properties=properties, bucket=bucket)
        self.assertTrue(blob.bucket is bucket)
        self.assertTrue(blob.connection is connection)
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(blob.properties, properties)
        self.assertTrue(blob._acl is None)

    def test_acl_property(self):
        from gcloud.storage.acl import ObjectACL
        blob = self._makeOne()
        acl = blob.acl
        self.assertTrue(isinstance(acl, ObjectACL))
        self.assertTrue(acl is blob._acl)

    def test_path_no_bucket(self):
        blob = self._makeOne()
        self.assertRaises(ValueError, getattr, blob, 'path')

    def test_path_no_name(self):
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket)
        self.assertRaises(ValueError, getattr, blob, 'path')

    def test_path_normal(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        self.assertEqual(blob.path, '/b/name/o/%s' % BLOB_NAME)

    def test_path_w_slash_in_name(self):
        BLOB_NAME = 'parent/child'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        self.assertEqual(blob.path, '/b/name/o/parent%2Fchild')

    def test_public_url(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        self.assertEqual(blob.public_url,
                         'http://commondatastorage.googleapis.com/name/%s' %
                         BLOB_NAME)

    def test_public_url_w_slash_in_name(self):
        BLOB_NAME = 'parent/child'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        self.assertEqual(
            blob.public_url,
            'http://commondatastorage.googleapis.com/name/parent%2Fchild')

    def test_generate_signed_url_w_default_method(self):
        BLOB_NAME = 'blob-name'
        EXPIRATION = '2014-10-16T20:34:37Z'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37Z')
        self.assertEqual(blob.generate_signed_url(EXPIRATION), URI)
        PATH = '/name/%s' % (BLOB_NAME,)
        self.assertEqual(connection._signed,
                         [(PATH, EXPIRATION, {'method': 'GET'})])

    def test_generate_signed_url_w_slash_in_name(self):
        BLOB_NAME = 'parent/child'
        EXPIRATION = '2014-10-16T20:34:37Z'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37Z')
        self.assertEqual(blob.generate_signed_url(EXPIRATION), URI)
        self.assertEqual(connection._signed,
                         [('/name/parent%2Fchild',
                           EXPIRATION, {'method': 'GET'})])

    def test_generate_signed_url_w_explicit_method(self):
        BLOB_NAME = 'blob-name'
        EXPIRATION = '2014-10-16T20:34:37Z'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37Z')
        self.assertEqual(blob.generate_signed_url(EXPIRATION, method='POST'),
                         URI)
        PATH = '/name/%s' % (BLOB_NAME,)
        self.assertEqual(connection._signed,
                         [(PATH, EXPIRATION, {'method': 'POST'})])

    def test_exists_miss(self):
        NONESUCH = 'nonesuch'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, NONESUCH)
        self.assertFalse(blob.exists())

    def test_exists_hit(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        bucket._blobs[BLOB_NAME] = 1
        self.assertTrue(blob.exists())

    def test_rename(self):
        BLOB_NAME = 'blob-name'
        NEW_NAME = 'new-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        bucket._blobs[BLOB_NAME] = 1
        new_blob = blob.rename(NEW_NAME)
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(new_blob.name, NEW_NAME)
        self.assertFalse(BLOB_NAME in bucket._blobs)
        self.assertTrue(BLOB_NAME in bucket._deleted)
        self.assertTrue(NEW_NAME in bucket._blobs)

    def test_delete(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        bucket._blobs[BLOB_NAME] = 1
        blob.delete()
        self.assertFalse(blob.exists())

    def test_download_to_file(self):
        import httplib
        from StringIO import StringIO
        BLOB_NAME = 'blob-name'
        chunk1_response = {'status': httplib.PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': httplib.OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, 'abc'),
            (chunk2_response, 'def'),
        )
        bucket = _Bucket(connection)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        blob.CHUNK_SIZE = 3
        fh = StringIO()
        blob.download_to_file(fh)
        self.assertEqual(fh.getvalue(), 'abcdef')

    def test_download_to_filename(self):
        import httplib
        import os
        import time
        import datetime
        from tempfile import NamedTemporaryFile
        BLOB_NAME = 'blob-name'
        chunk1_response = {'status': httplib.PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': httplib.OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, 'abc'),
            (chunk2_response, 'def'),
        )
        bucket = _Bucket(connection)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK,
                      'updated': '2014-12-06T13:13:50.690Z'}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        blob.CHUNK_SIZE = 3
        with NamedTemporaryFile() as f:
            blob.download_to_filename(f.name)
            f.flush()
            with open(f.name) as g:
                wrote = g.read()
                mtime = os.path.getmtime(f.name)
                updatedTime = time.mktime(
                    datetime.datetime.strptime(
                        blob.properties['updated'],
                        '%Y-%m-%dT%H:%M:%S.%fz').timetuple()
                )
        self.assertEqual(wrote, 'abcdef')
        self.assertEqual(mtime, updatedTime)

    def test_download_as_string(self):
        import httplib
        BLOB_NAME = 'blob-name'
        chunk1_response = {'status': httplib.PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': httplib.OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, 'abc'),
            (chunk2_response, 'def'),
        )
        bucket = _Bucket(connection)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        blob.CHUNK_SIZE = 3
        fetched = blob.download_as_string()
        self.assertEqual(fetched, 'abcdef')

    def test_upload_from_file_simple(self):
        import httplib
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        BLOB_NAME = 'blob-name'
        DATA = 'ABCDEF'
        response = {'status': httplib.OK}
        connection = _Connection(
            (response, ''),
        )
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.CHUNK_SIZE = 5
        with NamedTemporaryFile() as fh:
            fh.write(DATA)
            fh.flush()
            blob.upload_from_file(fh, rewind=True)
        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'media', 'name': BLOB_NAME})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'application/unknown')

    def test_upload_from_file_resumable(self):
        import httplib
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        from gcloud._testing import _Monkey
        from _gcloud_vendor.apitools.base.py import http_wrapper
        from _gcloud_vendor.apitools.base.py import transfer
        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'status': httplib.OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': httplib.OK}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.CHUNK_SIZE = 5
        # Set the threshhold low enough that we force a resumable uploada.
        with _Monkey(transfer, _RESUMABLE_UPLOAD_THRESHOLD=5):
            with NamedTemporaryFile() as fh:
                fh.write(DATA)
                fh.flush()
                blob.upload_from_file(fh, rewind=True)
        rq = connection.http._requested
        self.assertEqual(len(rq), 3)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable', 'name': BLOB_NAME})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['X-Upload-Content-Length'], '6')
        self.assertEqual(headers['X-Upload-Content-Type'],
                         'application/unknown')
        self.assertEqual(rq[1]['method'], 'PUT')
        self.assertEqual(rq[1]['uri'], UPLOAD_URL)
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[1]['headers'].items()])
        self.assertEqual(rq[1]['body'], DATA[:5])
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[1]['headers'].items()])
        self.assertEqual(headers['Content-Range'], 'bytes 0-4/6')
        self.assertEqual(rq[2]['method'], 'PUT')
        self.assertEqual(rq[2]['uri'], UPLOAD_URL)
        self.assertEqual(rq[2]['body'], DATA[5:])
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[2]['headers'].items()])
        self.assertEqual(headers['Content-Range'], 'bytes 5-5/6')

    def test_upload_from_file_w_slash_in_name(self):
        import httplib
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        from _gcloud_vendor.apitools.base.py import http_wrapper
        BLOB_NAME = 'parent/child'
        UPLOAD_URL = 'http://example.com/upload/name/parent%2Fchild'
        DATA = 'ABCDEF'
        loc_response = {'status': httplib.OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': httplib.OK}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.CHUNK_SIZE = 5
        with NamedTemporaryFile() as fh:
            fh.write(DATA)
            fh.flush()
            blob.upload_from_file(fh, rewind=True)
        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'media', 'name': 'parent/child'})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'application/unknown')

    def test_upload_from_filename(self):
        import httplib
        from tempfile import NamedTemporaryFile
        from urlparse import parse_qsl
        from urlparse import urlsplit
        from _gcloud_vendor.apitools.base.py import http_wrapper
        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'status': httplib.OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': httplib.OK}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.CHUNK_SIZE = 5
        with NamedTemporaryFile(suffix='.jpeg') as fh:
            fh.write(DATA)
            fh.flush()
            blob.upload_from_filename(fh.name)
        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'media', 'name': BLOB_NAME})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'image/jpeg')

    def test_upload_from_string(self):
        import httplib
        from urlparse import parse_qsl
        from urlparse import urlsplit
        from _gcloud_vendor.apitools.base.py import http_wrapper
        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = 'ABCDEF'
        loc_response = {'status': httplib.OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': httplib.OK}
        connection = _Connection(
            (loc_response, ''),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.CHUNK_SIZE = 5
        blob.upload_from_string(DATA)
        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'media', 'name': BLOB_NAME})
        headers = dict(
            [(x.title(), str(y)) for x, y in rq[0]['headers'].items()])
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'text/plain')

    def test_make_public(self):
        from gcloud.storage.acl import _ACLEntity
        BLOB_NAME = 'blob-name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.acl.loaded = True
        blob.make_public()
        self.assertEqual(list(blob.acl), permissive)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'], {'acl': permissive})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_cache_control_getter(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        CACHE_CONTROL = 'no-cache'
        properties = {'cacheControl': CACHE_CONTROL}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.cache_control, CACHE_CONTROL)

    def test_cache_control_setter(self):
        BLOB_NAME = 'blob-name'
        CACHE_CONTROL = 'no-cache'
        after = {'cacheControl': CACHE_CONTROL}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.cache_control = CACHE_CONTROL
        self.assertEqual(blob.cache_control, CACHE_CONTROL)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'], {'cacheControl': CACHE_CONTROL})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_component_count(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        COMPONENT_COUNT = 42
        properties = {'componentCount': COMPONENT_COUNT}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.component_count, COMPONENT_COUNT)

    def test_content_disposition_getter(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        CONTENT_DISPOSITION = 'Attachment; filename=example.jpg'
        properties = {'contentDisposition': CONTENT_DISPOSITION}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.content_disposition, CONTENT_DISPOSITION)

    def test_content_disposition_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_DISPOSITION = 'Attachment; filename=example.jpg'
        after = {'contentDisposition': CONTENT_DISPOSITION}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.content_disposition = CONTENT_DISPOSITION
        self.assertEqual(blob.content_disposition, CONTENT_DISPOSITION)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'],
                         {'contentDisposition': CONTENT_DISPOSITION})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_content_encoding_getter(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        CONTENT_ENCODING = 'gzip'
        properties = {'contentEncoding': CONTENT_ENCODING}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.content_encoding, CONTENT_ENCODING)

    def test_content_encoding_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_ENCODING = 'gzip'
        after = {'contentEncoding': CONTENT_ENCODING}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.content_encoding = CONTENT_ENCODING
        self.assertEqual(blob.content_encoding, CONTENT_ENCODING)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'],
                         {'contentEncoding': CONTENT_ENCODING})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_content_language_getter(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        CONTENT_LANGUAGE = 'pt-BR'
        properties = {'contentLanguage': CONTENT_LANGUAGE}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.content_language, CONTENT_LANGUAGE)

    def test_content_language_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_LANGUAGE = 'pt-BR'
        after = {'contentLanguage': CONTENT_LANGUAGE}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.content_language = CONTENT_LANGUAGE
        self.assertEqual(blob.content_language, CONTENT_LANGUAGE)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'],
                         {'contentLanguage': CONTENT_LANGUAGE})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_content_type_getter(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        CONTENT_TYPE = 'image/jpeg'
        properties = {'contentType': CONTENT_TYPE}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.content_type, CONTENT_TYPE)

    def test_content_type_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_TYPE = 'image/jpeg'
        after = {'contentType': CONTENT_TYPE}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.content_type = CONTENT_TYPE
        self.assertEqual(blob.content_type, CONTENT_TYPE)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'],
                         {'contentType': CONTENT_TYPE})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_crc32c_getter(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        CRC32C = 'DEADBEEF'
        properties = {'crc32c': CRC32C}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.crc32c, CRC32C)

    def test_crc32c_setter(self):
        BLOB_NAME = 'blob-name'
        CRC32C = 'DEADBEEF'
        after = {'crc32c': CRC32C}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.crc32c = CRC32C
        self.assertEqual(blob.crc32c, CRC32C)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'],
                         {'crc32c': CRC32C})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_etag(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        ETAG = 'ETAG'
        properties = {'etag': ETAG}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.etag, ETAG)

    def test_generation(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        GENERATION = 42
        properties = {'generation': GENERATION}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.generation, GENERATION)

    def test_id(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        ID = 'ID'
        properties = {'id': ID}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.id, ID)

    def test_md5_hash_getter(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        MD5_HASH = 'DEADBEEF'
        properties = {'md5Hash': MD5_HASH}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.md5_hash, MD5_HASH)

    def test_md5_hash_setter(self):
        BLOB_NAME = 'blob-name'
        MD5_HASH = 'DEADBEEF'
        after = {'md5Hash': MD5_HASH}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.md5_hash = MD5_HASH
        self.assertEqual(blob.md5_hash, MD5_HASH)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'],
                         {'md5Hash': MD5_HASH})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_media_link(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.media_link, MEDIA_LINK)

    def test_metadata_getter(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        METADATA = {'foo': 'Foo'}
        properties = {'metadata': METADATA}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.metadata, METADATA)

    def test_metadata_setter(self):
        BLOB_NAME = 'blob-name'
        METADATA = {'foo': 'Foo'}
        after = {'metadata': METADATA}
        connection = _Connection(after)
        bucket = _Bucket(connection)
        blob = self._makeOne(bucket, BLOB_NAME)
        blob.metadata = METADATA
        self.assertEqual(blob.metadata, METADATA)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'],
                         {'metadata': METADATA})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_metageneration(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        METAGENERATION = 42
        properties = {'metageneration': METAGENERATION}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.metageneration, METAGENERATION)

    def test_owner(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        OWNER = {'entity': 'project-owner-12345', 'entityId': '23456'}
        properties = {'owner': OWNER}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        owner = blob.owner
        self.assertEqual(owner['entity'], 'project-owner-12345')
        self.assertEqual(owner['entityId'], '23456')

    def test_self_link(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        SELF_LINK = 'http://example.com/self/'
        properties = {'selfLink': SELF_LINK}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.self_link, SELF_LINK)

    def test_size(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        SIZE = 42
        properties = {'size': SIZE}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.size, SIZE)

    def test_storage_class(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        STORAGE_CLASS = 'http://example.com/self/'
        properties = {'storageClass': STORAGE_CLASS}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.storage_class, STORAGE_CLASS)

    def test_time_deleted(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        TIME_DELETED = '2014-11-05T20:34:37Z'
        properties = {'timeDeleted': TIME_DELETED}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.time_deleted, TIME_DELETED)

    def test_updated(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        bucket = _Bucket(connection)
        UPDATED = '2014-11-05T20:34:37Z'
        properties = {'updated': UPDATED}
        blob = self._makeOne(bucket, BLOB_NAME, properties)
        self.assertEqual(blob.updated, UPDATED)


class _Responder(object):

    def __init__(self, *responses):
        self._responses = responses[:]
        self._requested = []

    def _respond(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _Connection(_Responder):

    API_BASE_URL = 'http://example.com'
    USER_AGENT = 'testing 1.2.3'

    def __init__(self, *responses):
        super(_Connection, self).__init__(*responses)
        self._signed = []
        self.http = _HTTP(*responses)

    def api_request(self, **kw):
        return self._respond(**kw)

    def build_api_url(self, path, query_params=None,
                      api_base_url=API_BASE_URL, upload=False):
        from urllib import urlencode
        from urlparse import urlsplit
        from urlparse import urlunsplit
        # mimic the build_api_url interface, but avoid unused param and
        # missed coverage errors
        upload = not upload  # pragma NO COVER
        qs = urlencode(query_params or {})
        scheme, netloc, _, _, _ = urlsplit(api_base_url)
        return urlunsplit((scheme, netloc, path, qs, ''))

    def generate_signed_url(self, resource, expiration, **kw):
        self._signed.append((resource, expiration, kw))
        return ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
                '&Expiration=%s' % expiration)


class _HTTP(_Responder):

    def request(self, uri, method, headers, body, **kw):
        return self._respond(uri=uri, method=method, headers=headers,
                             body=body, **kw)


class _Bucket(object):
    path = '/b/name'
    name = 'name'

    def __init__(self, connection):
        self.connection = connection
        self._blobs = {}
        self._deleted = []

    def get_blob(self, blob):
        return self._blobs.get(blob)

    def copy_blob(self, blob, destination_bucket, new_name):
        destination_bucket._blobs[new_name] = self._blobs[blob.name]
        return blob.__class__(properties={'name': new_name},
                              bucket=destination_bucket)

    def delete_blob(self, blob):
        del self._blobs[blob.name]
        self._deleted.append(blob.name)
