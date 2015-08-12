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
        properties = kw.pop('properties', None)
        blob = Blob(*args, **kw)
        blob._properties = properties or {}
        return blob

    def test_ctor(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        properties = {'key': 'value'}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertTrue(blob.bucket is bucket)
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(blob._properties, properties)
        self.assertFalse(blob._acl.loaded)
        self.assertTrue(blob._acl.blob is blob)

    def test_chunk_size_ctor(self):
        from gcloud.storage.blob import Blob
        BLOB_NAME = 'blob-name'
        BUCKET = object()
        chunk_size = 10 * Blob._CHUNK_SIZE_MULTIPLE
        blob = self._makeOne(BLOB_NAME, bucket=BUCKET, chunk_size=chunk_size)
        self.assertEqual(blob._chunk_size, chunk_size)

    def test_chunk_size_getter(self):
        BLOB_NAME = 'blob-name'
        BUCKET = object()
        blob = self._makeOne(BLOB_NAME, bucket=BUCKET)
        self.assertEqual(blob.chunk_size, None)
        VALUE = object()
        blob._chunk_size = VALUE
        self.assertTrue(blob.chunk_size is VALUE)

    def test_chunk_size_setter(self):
        BLOB_NAME = 'blob-name'
        BUCKET = object()
        blob = self._makeOne(BLOB_NAME, bucket=BUCKET)
        self.assertEqual(blob._chunk_size, None)
        blob._CHUNK_SIZE_MULTIPLE = 10
        blob.chunk_size = 20
        self.assertEqual(blob._chunk_size, 20)

    def test_chunk_size_setter_bad_value(self):
        BLOB_NAME = 'blob-name'
        BUCKET = object()
        blob = self._makeOne(BLOB_NAME, bucket=BUCKET)
        self.assertEqual(blob._chunk_size, None)
        blob._CHUNK_SIZE_MULTIPLE = 10
        with self.assertRaises(ValueError):
            blob.chunk_size = 11

    def test_acl_property(self):
        from gcloud.storage.acl import ObjectACL
        FAKE_BUCKET = _Bucket()
        blob = self._makeOne(None, bucket=FAKE_BUCKET)
        acl = blob.acl
        self.assertTrue(isinstance(acl, ObjectACL))
        self.assertTrue(acl is blob._acl)

    def test_path_no_bucket(self):
        FAKE_BUCKET = object()
        NAME = 'blob-name'
        blob = self._makeOne(NAME, bucket=FAKE_BUCKET)
        self.assertRaises(AttributeError, getattr, blob, 'path')

    def test_path_no_name(self):
        bucket = _Bucket()
        blob = self._makeOne(None, bucket=bucket)
        self.assertRaises(ValueError, getattr, blob, 'path')

    def test_path_normal(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.path, '/b/name/o/%s' % BLOB_NAME)

    def test_path_w_slash_in_name(self):
        BLOB_NAME = 'parent/child'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.path, '/b/name/o/parent%2Fchild')

    def test_public_url(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.public_url,
                         'https://storage.googleapis.com/name/%s' %
                         BLOB_NAME)

    def test_public_url_w_slash_in_name(self):
        BLOB_NAME = 'parent/child'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(
            blob.public_url,
            'https://storage.googleapis.com/name/parent%2Fchild')

    def _basic_generate_signed_url_helper(self, credentials=None):
        from gcloud._testing import _Monkey
        from gcloud.storage import blob as MUT

        BLOB_NAME = 'blob-name'
        EXPIRATION = '2014-10-16T20:34:37.000Z'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37.000Z')

        SIGNER = _Signer()
        with _Monkey(MUT, generate_signed_url=SIGNER):
            signed_uri = blob.generate_signed_url(EXPIRATION,
                                                  credentials=credentials)
            self.assertEqual(signed_uri, URI)

        PATH = '/name/%s' % (BLOB_NAME,)
        if credentials is None:
            EXPECTED_ARGS = (_Connection.credentials,)
        else:
            EXPECTED_ARGS = (credentials,)
        EXPECTED_KWARGS = {
            'api_access_endpoint': 'https://storage.googleapis.com',
            'expiration': EXPIRATION,
            'method': 'GET',
            'resource': PATH,
        }
        self.assertEqual(SIGNER._signed, [(EXPECTED_ARGS, EXPECTED_KWARGS)])

    def test_generate_signed_url_w_default_method(self):
        self._basic_generate_signed_url_helper()

    def test_generate_signed_url_w_credentials(self):
        credentials = object()
        self._basic_generate_signed_url_helper(credentials=credentials)

    def test_generate_signed_url_w_slash_in_name(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import blob as MUT

        BLOB_NAME = 'parent/child'
        EXPIRATION = '2014-10-16T20:34:37.000Z'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37.000Z')

        SIGNER = _Signer()
        with _Monkey(MUT, generate_signed_url=SIGNER):
            signed_url = blob.generate_signed_url(EXPIRATION)
            self.assertEqual(signed_url, URI)

        EXPECTED_ARGS = (_Connection.credentials,)
        EXPECTED_KWARGS = {
            'api_access_endpoint': 'https://storage.googleapis.com',
            'expiration': EXPIRATION,
            'method': 'GET',
            'resource': '/name/parent%2Fchild',
        }
        self.assertEqual(SIGNER._signed, [(EXPECTED_ARGS, EXPECTED_KWARGS)])

    def test_generate_signed_url_w_method_arg(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import blob as MUT

        BLOB_NAME = 'blob-name'
        EXPIRATION = '2014-10-16T20:34:37.000Z'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37.000Z')

        SIGNER = _Signer()
        with _Monkey(MUT, generate_signed_url=SIGNER):
            signed_uri = blob.generate_signed_url(EXPIRATION, method='POST')
            self.assertEqual(signed_uri, URI)

        PATH = '/name/%s' % (BLOB_NAME,)
        EXPECTED_ARGS = (_Connection.credentials,)
        EXPECTED_KWARGS = {
            'api_access_endpoint': 'https://storage.googleapis.com',
            'expiration': EXPIRATION,
            'method': 'POST',
            'resource': PATH,
        }
        self.assertEqual(SIGNER._signed, [(EXPECTED_ARGS, EXPECTED_KWARGS)])

    def test_exists_miss(self):
        from six.moves.http_client import NOT_FOUND
        NONESUCH = 'nonesuch'
        not_found_response = {'status': NOT_FOUND}
        connection = _Connection(not_found_response)
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(NONESUCH, bucket=bucket)
        self.assertFalse(blob.exists())

    def test_exists_hit(self):
        from six.moves.http_client import OK
        BLOB_NAME = 'blob-name'
        found_response = {'status': OK}
        connection = _Connection(found_response)
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        bucket._blobs[BLOB_NAME] = 1
        self.assertTrue(blob.exists())

    def test_delete(self):
        from six.moves.http_client import NOT_FOUND
        BLOB_NAME = 'blob-name'
        not_found_response = {'status': NOT_FOUND}
        connection = _Connection(not_found_response)
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        bucket._blobs[BLOB_NAME] = 1
        blob.delete()
        self.assertFalse(blob.exists())
        self.assertEqual(bucket._deleted, [(BLOB_NAME, None)])

    def _download_to_file_helper(self, chunk_size=None):
        from six.moves.http_client import OK
        from six.moves.http_client import PARTIAL_CONTENT
        from io import BytesIO
        BLOB_NAME = 'blob-name'
        chunk1_response = {'status': PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, b'abc'),
            (chunk2_response, b'def'),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        if chunk_size is not None:
            blob._CHUNK_SIZE_MULTIPLE = 1
            blob.chunk_size = chunk_size
        fh = BytesIO()
        blob.download_to_file(fh)
        self.assertEqual(fh.getvalue(), b'abcdef')

    def test_download_to_file_default(self):
        self._download_to_file_helper()

    def test_download_to_file_with_chunk_size(self):
        self._download_to_file_helper(chunk_size=3)

    def test_download_to_filename(self):
        import os
        import time
        from six.moves.http_client import OK
        from six.moves.http_client import PARTIAL_CONTENT
        from tempfile import NamedTemporaryFile
        BLOB_NAME = 'blob-name'
        chunk1_response = {'status': PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, b'abc'),
            (chunk2_response, b'def'),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK,
                      'updated': '2014-12-06T13:13:50.690Z'}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 3
        with NamedTemporaryFile() as f:
            blob.download_to_filename(f.name)
            f.flush()
            with open(f.name, 'rb') as g:
                wrote = g.read()
                mtime = os.path.getmtime(f.name)
                updatedTime = time.mktime(blob.updated.timetuple())
        self.assertEqual(wrote, b'abcdef')
        self.assertEqual(mtime, updatedTime)

    def test_download_as_string(self):
        from six.moves.http_client import OK
        from six.moves.http_client import PARTIAL_CONTENT
        BLOB_NAME = 'blob-name'
        chunk1_response = {'status': PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, b'abc'),
            (chunk2_response, b'def'),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 3
        fetched = blob.download_as_string()
        self.assertEqual(fetched, b'abcdef')

    def test_upload_from_file_size_failure(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        file_obj = object()
        with self.assertRaises(ValueError):
            blob.upload_from_file(file_obj, size=None)

    def _upload_from_file_simple_test_helper(self, properties=None,
                                             content_type_arg=None,
                                             expected_content_type=None):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from tempfile import NamedTemporaryFile
        BLOB_NAME = 'blob-name'
        DATA = b'ABCDEF'
        response = {'status': OK}
        connection = _Connection(
            (response, b'{}'),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5
        with NamedTemporaryFile() as fh:
            fh.write(DATA)
            fh.flush()
            blob.upload_from_file(fh, rewind=True,
                                  content_type=content_type_arg)
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
        self.assertEqual(headers['Content-Type'], expected_content_type)

    def test_upload_from_file_simple(self):
        self._upload_from_file_simple_test_helper(
            expected_content_type='application/octet-stream')

    def test_upload_from_file_simple_with_content_type(self):
        EXPECTED_CONTENT_TYPE = 'foo/bar'
        self._upload_from_file_simple_test_helper(
            properties={'contentType': EXPECTED_CONTENT_TYPE},
            expected_content_type=EXPECTED_CONTENT_TYPE)

    def test_upload_from_file_simple_with_content_type_passed(self):
        EXPECTED_CONTENT_TYPE = 'foo/bar'
        self._upload_from_file_simple_test_helper(
            content_type_arg=EXPECTED_CONTENT_TYPE,
            expected_content_type=EXPECTED_CONTENT_TYPE)

    def test_upload_from_file_simple_both_content_type_sources(self):
        EXPECTED_CONTENT_TYPE = 'foo/bar'
        ALT_CONTENT_TYPE = 'foo/baz'
        self._upload_from_file_simple_test_helper(
            properties={'contentType': ALT_CONTENT_TYPE},
            content_type_arg=EXPECTED_CONTENT_TYPE,
            expected_content_type=EXPECTED_CONTENT_TYPE)

    def test_upload_from_file_resumable(self):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from tempfile import NamedTemporaryFile
        from gcloud._testing import _Monkey
        from apitools.base.py import http_wrapper
        from apitools.base.py import transfer
        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = b'ABCDEF'
        loc_response = {'status': OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': OK}
        # Need valid JSON on last response, since resumable.
        connection = _Connection(
            (loc_response, b''),
            (chunk1_response, b''),
            (chunk2_response, b'{}'),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5
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
                         'application/octet-stream')
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
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from tempfile import NamedTemporaryFile
        from apitools.base.py import http_wrapper
        BLOB_NAME = 'parent/child'
        UPLOAD_URL = 'http://example.com/upload/name/parent%2Fchild'
        DATA = b'ABCDEF'
        loc_response = {'status': OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': OK}
        connection = _Connection(
            (loc_response, '{}'),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5
        with NamedTemporaryFile() as fh:
            fh.write(DATA)
            fh.flush()
            blob.upload_from_file(fh, rewind=True)
            self.assertEqual(fh.tell(), len(DATA))
        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['redirections'], 5)
        self.assertEqual(rq[0]['body'], DATA)
        self.assertEqual(rq[0]['connection_type'], None)
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
        self.assertEqual(headers['Content-Type'], 'application/octet-stream')

    def _upload_from_filename_test_helper(self, properties=None,
                                          content_type_arg=None,
                                          expected_content_type=None):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from tempfile import NamedTemporaryFile
        from apitools.base.py import http_wrapper
        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = b'ABCDEF'
        loc_response = {'status': OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': OK}
        connection = _Connection(
            (loc_response, '{}'),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket,
                             properties=properties)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5
        with NamedTemporaryFile(suffix='.jpeg') as fh:
            fh.write(DATA)
            fh.flush()
            blob.upload_from_filename(fh.name, content_type=content_type_arg)
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
        self.assertEqual(headers['Content-Type'], expected_content_type)

    def test_upload_from_filename(self):
        self._upload_from_filename_test_helper(
            expected_content_type='image/jpeg')

    def test_upload_from_filename_with_content_type(self):
        EXPECTED_CONTENT_TYPE = 'foo/bar'
        self._upload_from_filename_test_helper(
            properties={'contentType': EXPECTED_CONTENT_TYPE},
            expected_content_type=EXPECTED_CONTENT_TYPE)

    def test_upload_from_filename_with_content_type_passed(self):
        EXPECTED_CONTENT_TYPE = 'foo/bar'
        self._upload_from_filename_test_helper(
            content_type_arg=EXPECTED_CONTENT_TYPE,
            expected_content_type=EXPECTED_CONTENT_TYPE)

    def test_upload_from_filename_both_content_type_sources(self):
        EXPECTED_CONTENT_TYPE = 'foo/bar'
        ALT_CONTENT_TYPE = 'foo/baz'
        self._upload_from_filename_test_helper(
            properties={'contentType': ALT_CONTENT_TYPE},
            content_type_arg=EXPECTED_CONTENT_TYPE,
            expected_content_type=EXPECTED_CONTENT_TYPE)

    def test_upload_from_string_w_bytes(self):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from apitools.base.py import http_wrapper
        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = b'ABCDEF'
        loc_response = {'status': OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': OK}
        connection = _Connection(
            (loc_response, '{}'),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5
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
        self.assertEqual(rq[0]['body'], DATA)

    def test_upload_from_string_w_text(self):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from apitools.base.py import http_wrapper
        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = u'ABCDEF\u1234'
        ENCODED = DATA.encode('utf-8')
        loc_response = {'status': OK, 'location': UPLOAD_URL}
        chunk1_response = {'status': http_wrapper.RESUME_INCOMPLETE,
                           'range': 'bytes 0-4'}
        chunk2_response = {'status': OK}
        connection = _Connection(
            (loc_response, '{}'),
            (chunk1_response, ''),
            (chunk2_response, ''),
        )
        client = _Client(connection)
        bucket = _Bucket(client=client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5
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
        self.assertEqual(headers['Content-Length'], str(len(ENCODED)))
        self.assertEqual(headers['Content-Type'], 'text/plain')
        self.assertEqual(rq[0]['body'], ENCODED)

    def test_make_public(self):
        from gcloud.storage.acl import _ACLEntity
        BLOB_NAME = 'blob-name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = {'acl': permissive}
        connection = _Connection(after)
        client = _Client(connection)
        bucket = _Bucket(client=client)
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
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
        bucket = _Bucket()
        CACHE_CONTROL = 'no-cache'
        properties = {'cacheControl': CACHE_CONTROL}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.cache_control, CACHE_CONTROL)

    def test_cache_control_setter(self):
        BLOB_NAME = 'blob-name'
        CACHE_CONTROL = 'no-cache'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.cache_control, None)
        blob.cache_control = CACHE_CONTROL
        self.assertEqual(blob.cache_control, CACHE_CONTROL)

    def test_component_count(self):
        BUCKET = object()
        COMPONENT_COUNT = 42
        blob = self._makeOne('blob-name', bucket=BUCKET,
                             properties={'componentCount': COMPONENT_COUNT})
        self.assertEqual(blob.component_count, COMPONENT_COUNT)

    def test_component_count_unset(self):
        BUCKET = object()
        blob = self._makeOne('blob-name', bucket=BUCKET)
        self.assertEqual(blob.component_count, None)

    def test_component_count_string_val(self):
        BUCKET = object()
        COMPONENT_COUNT = 42
        blob = self._makeOne(
            'blob-name', bucket=BUCKET,
            properties={'componentCount': str(COMPONENT_COUNT)})
        self.assertEqual(blob.component_count, COMPONENT_COUNT)

    def test_content_disposition_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CONTENT_DISPOSITION = 'Attachment; filename=example.jpg'
        properties = {'contentDisposition': CONTENT_DISPOSITION}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.content_disposition, CONTENT_DISPOSITION)

    def test_content_disposition_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_DISPOSITION = 'Attachment; filename=example.jpg'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.content_disposition, None)
        blob.content_disposition = CONTENT_DISPOSITION
        self.assertEqual(blob.content_disposition, CONTENT_DISPOSITION)

    def test_content_encoding_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CONTENT_ENCODING = 'gzip'
        properties = {'contentEncoding': CONTENT_ENCODING}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.content_encoding, CONTENT_ENCODING)

    def test_content_encoding_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_ENCODING = 'gzip'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.content_encoding, None)
        blob.content_encoding = CONTENT_ENCODING
        self.assertEqual(blob.content_encoding, CONTENT_ENCODING)

    def test_content_language_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CONTENT_LANGUAGE = 'pt-BR'
        properties = {'contentLanguage': CONTENT_LANGUAGE}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.content_language, CONTENT_LANGUAGE)

    def test_content_language_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_LANGUAGE = 'pt-BR'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.content_language, None)
        blob.content_language = CONTENT_LANGUAGE
        self.assertEqual(blob.content_language, CONTENT_LANGUAGE)

    def test_content_type_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CONTENT_TYPE = 'image/jpeg'
        properties = {'contentType': CONTENT_TYPE}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.content_type, CONTENT_TYPE)

    def test_content_type_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_TYPE = 'image/jpeg'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.content_type, None)
        blob.content_type = CONTENT_TYPE
        self.assertEqual(blob.content_type, CONTENT_TYPE)

    def test_crc32c_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CRC32C = 'DEADBEEF'
        properties = {'crc32c': CRC32C}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.crc32c, CRC32C)

    def test_crc32c_setter(self):
        BLOB_NAME = 'blob-name'
        CRC32C = 'DEADBEEF'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.crc32c, None)
        blob.crc32c = CRC32C
        self.assertEqual(blob.crc32c, CRC32C)

    def test_etag(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        ETAG = 'ETAG'
        properties = {'etag': ETAG}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.etag, ETAG)

    def test_generation(self):
        BUCKET = object()
        GENERATION = 42
        blob = self._makeOne('blob-name', bucket=BUCKET,
                             properties={'generation': GENERATION})
        self.assertEqual(blob.generation, GENERATION)

    def test_generation_unset(self):
        BUCKET = object()
        blob = self._makeOne('blob-name', bucket=BUCKET)
        self.assertEqual(blob.generation, None)

    def test_generation_string_val(self):
        BUCKET = object()
        GENERATION = 42
        blob = self._makeOne('blob-name', bucket=BUCKET,
                             properties={'generation': str(GENERATION)})
        self.assertEqual(blob.generation, GENERATION)

    def test_id(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        ID = 'ID'
        properties = {'id': ID}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.id, ID)

    def test_md5_hash_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        MD5_HASH = 'DEADBEEF'
        properties = {'md5Hash': MD5_HASH}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.md5_hash, MD5_HASH)

    def test_md5_hash_setter(self):
        BLOB_NAME = 'blob-name'
        MD5_HASH = 'DEADBEEF'
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.md5_hash, None)
        blob.md5_hash = MD5_HASH
        self.assertEqual(blob.md5_hash, MD5_HASH)

    def test_media_link(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.media_link, MEDIA_LINK)

    def test_metadata_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        METADATA = {'foo': 'Foo'}
        properties = {'metadata': METADATA}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.metadata, METADATA)

    def test_metadata_setter(self):
        BLOB_NAME = 'blob-name'
        METADATA = {'foo': 'Foo'}
        bucket = _Bucket()
        blob = self._makeOne(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.metadata, None)
        blob.metadata = METADATA
        self.assertEqual(blob.metadata, METADATA)

    def test_metageneration(self):
        BUCKET = object()
        METAGENERATION = 42
        blob = self._makeOne('blob-name', bucket=BUCKET,
                             properties={'metageneration': METAGENERATION})
        self.assertEqual(blob.metageneration, METAGENERATION)

    def test_metageneration_unset(self):
        BUCKET = object()
        blob = self._makeOne('blob-name', bucket=BUCKET)
        self.assertEqual(blob.metageneration, None)

    def test_metageneration_string_val(self):
        BUCKET = object()
        METAGENERATION = 42
        blob = self._makeOne(
            'blob-name', bucket=BUCKET,
            properties={'metageneration': str(METAGENERATION)})
        self.assertEqual(blob.metageneration, METAGENERATION)

    def test_owner(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        OWNER = {'entity': 'project-owner-12345', 'entityId': '23456'}
        properties = {'owner': OWNER}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        owner = blob.owner
        self.assertEqual(owner['entity'], 'project-owner-12345')
        self.assertEqual(owner['entityId'], '23456')

    def test_self_link(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        SELF_LINK = 'http://example.com/self/'
        properties = {'selfLink': SELF_LINK}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.self_link, SELF_LINK)

    def test_size(self):
        BUCKET = object()
        SIZE = 42
        blob = self._makeOne('blob-name', bucket=BUCKET,
                             properties={'size': SIZE})
        self.assertEqual(blob.size, SIZE)

    def test_size_unset(self):
        BUCKET = object()
        blob = self._makeOne('blob-name', bucket=BUCKET)
        self.assertEqual(blob.size, None)

    def test_size_string_val(self):
        BUCKET = object()
        SIZE = 42
        blob = self._makeOne('blob-name', bucket=BUCKET,
                             properties={'size': str(SIZE)})
        self.assertEqual(blob.size, SIZE)

    def test_storage_class(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        STORAGE_CLASS = 'http://example.com/self/'
        properties = {'storageClass': STORAGE_CLASS}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.storage_class, STORAGE_CLASS)

    def test_time_deleted(self):
        import datetime
        from gcloud._helpers import _RFC3339_MICROS
        from gcloud._helpers import UTC
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        TIMESTAMP = datetime.datetime(2014, 11, 5, 20, 34, 37, tzinfo=UTC)
        TIME_DELETED = TIMESTAMP.strftime(_RFC3339_MICROS)
        properties = {'timeDeleted': TIME_DELETED}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.time_deleted, TIMESTAMP)

    def test_time_deleted_unset(self):
        BUCKET = object()
        blob = self._makeOne('blob-name', bucket=BUCKET)
        self.assertEqual(blob.time_deleted, None)

    def test_updated(self):
        import datetime
        from gcloud._helpers import _RFC3339_MICROS
        from gcloud._helpers import UTC
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        TIMESTAMP = datetime.datetime(2014, 11, 5, 20, 34, 37, tzinfo=UTC)
        UPDATED = TIMESTAMP.strftime(_RFC3339_MICROS)
        properties = {'updated': UPDATED}
        blob = self._makeOne(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.updated, TIMESTAMP)

    def test_updated_unset(self):
        BUCKET = object()
        blob = self._makeOne('blob-name', bucket=BUCKET)
        self.assertEqual(blob.updated, None)


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
    credentials = object()

    def __init__(self, *responses):
        super(_Connection, self).__init__(*responses)
        self._signed = []
        self.http = _HTTP(*responses)

    def api_request(self, **kw):
        from six.moves.http_client import NOT_FOUND
        from gcloud.exceptions import NotFound
        result = self._respond(**kw)
        if result.get('status') == NOT_FOUND:
            raise NotFound(result)
        return result

    def build_api_url(self, path, query_params=None,
                      api_base_url=API_BASE_URL):
        from six.moves.urllib.parse import urlencode
        from six.moves.urllib.parse import urlsplit
        from six.moves.urllib.parse import urlunsplit
        # Mimic the build_api_url interface.
        qs = urlencode(query_params or {})
        scheme, netloc, _, _, _ = urlsplit(api_base_url)
        return urlunsplit((scheme, netloc, path, qs, ''))


class _HTTP(_Responder):

    connections = {}  # For google-apitools debugging.

    def request(self, uri, method, headers, body, **kw):
        if hasattr(body, 'read'):
            body = body.read()
        return self._respond(uri=uri, method=method, headers=headers,
                             body=body, **kw)


class _Bucket(object):
    path = '/b/name'
    name = 'name'

    def __init__(self, client=None):
        if client is None:
            connection = _Connection()
            client = _Client(connection)
        self.client = client
        self._blobs = {}
        self._copied = []
        self._deleted = []

    def delete_blob(self, blob_name, client=None):
        del self._blobs[blob_name]
        self._deleted.append((blob_name, client))


class _Signer(object):

    def __init__(self):
        self._signed = []

    def __call__(self, *args, **kwargs):
        self._signed.append((args, kwargs))
        return ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
                '&Expiration=%s' % kwargs.get('expiration'))


class _Client(object):

    def __init__(self, connection):
        self._connection = connection

    @property
    def connection(self):
        return self._connection
