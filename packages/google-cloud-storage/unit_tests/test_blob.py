# Copyright 2014 Google Inc.
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

import unittest

import mock


class Test_Blob(unittest.TestCase):

    def _make_one(self, *args, **kw):
        from google.cloud.storage.blob import Blob

        properties = kw.pop('properties', None)
        blob = Blob(*args, **kw)
        blob._properties = properties or {}
        return blob

    def test_ctor_wo_encryption_key(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        properties = {'key': 'value'}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertIs(blob.bucket, bucket)
        self.assertEqual(blob.name, BLOB_NAME)
        self.assertEqual(blob._properties, properties)
        self.assertFalse(blob._acl.loaded)
        self.assertIs(blob._acl.blob, blob)
        self.assertEqual(blob._encryption_key, None)

    def test_ctor_w_encryption_key(self):
        KEY = b'01234567890123456789012345678901'  # 32 bytes
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket, encryption_key=KEY)
        self.assertEqual(blob._encryption_key, KEY)

    def test_chunk_size_ctor(self):
        from google.cloud.storage.blob import Blob

        BLOB_NAME = 'blob-name'
        BUCKET = object()
        chunk_size = 10 * Blob._CHUNK_SIZE_MULTIPLE
        blob = self._make_one(BLOB_NAME, bucket=BUCKET, chunk_size=chunk_size)
        self.assertEqual(blob._chunk_size, chunk_size)

    def test_chunk_size_getter(self):
        BLOB_NAME = 'blob-name'
        BUCKET = object()
        blob = self._make_one(BLOB_NAME, bucket=BUCKET)
        self.assertIsNone(blob.chunk_size)
        VALUE = object()
        blob._chunk_size = VALUE
        self.assertIs(blob.chunk_size, VALUE)

    def test_chunk_size_setter(self):
        BLOB_NAME = 'blob-name'
        BUCKET = object()
        blob = self._make_one(BLOB_NAME, bucket=BUCKET)
        self.assertIsNone(blob._chunk_size)
        blob._CHUNK_SIZE_MULTIPLE = 10
        blob.chunk_size = 20
        self.assertEqual(blob._chunk_size, 20)

    def test_chunk_size_setter_bad_value(self):
        BLOB_NAME = 'blob-name'
        BUCKET = object()
        blob = self._make_one(BLOB_NAME, bucket=BUCKET)
        self.assertIsNone(blob._chunk_size)
        blob._CHUNK_SIZE_MULTIPLE = 10
        with self.assertRaises(ValueError):
            blob.chunk_size = 11

    def test_acl_property(self):
        from google.cloud.storage.acl import ObjectACL

        FAKE_BUCKET = _Bucket()
        blob = self._make_one(None, bucket=FAKE_BUCKET)
        acl = blob.acl
        self.assertIsInstance(acl, ObjectACL)
        self.assertIs(acl, blob._acl)

    def test_path_no_bucket(self):
        FAKE_BUCKET = object()
        NAME = 'blob-name'
        blob = self._make_one(NAME, bucket=FAKE_BUCKET)
        self.assertRaises(AttributeError, getattr, blob, 'path')

    def test_path_no_name(self):
        bucket = _Bucket()
        blob = self._make_one(None, bucket=bucket)
        self.assertRaises(ValueError, getattr, blob, 'path')

    def test_path_normal(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.path, '/b/name/o/%s' % BLOB_NAME)

    def test_path_w_slash_in_name(self):
        BLOB_NAME = 'parent/child'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.path, '/b/name/o/parent%2Fchild')

    def test_public_url(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertEqual(blob.public_url,
                         'https://storage.googleapis.com/name/%s' %
                         BLOB_NAME)

    def test_public_url_w_slash_in_name(self):
        BLOB_NAME = 'parent/child'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertEqual(
            blob.public_url,
            'https://storage.googleapis.com/name/parent%2Fchild')

    def _basic_generate_signed_url_helper(self, credentials=None):
        BLOB_NAME = 'blob-name'
        EXPIRATION = '2014-10-16T20:34:37.000Z'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37.000Z')

        SIGNER = _Signer()
        with mock.patch('google.cloud.storage.blob.generate_signed_url',
                        new=SIGNER):
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
            'content_type': None,
            'response_type': None,
            'response_disposition': None,
            'generation': None,
        }
        self.assertEqual(SIGNER._signed, [(EXPECTED_ARGS, EXPECTED_KWARGS)])

    def test_generate_signed_url_w_default_method(self):
        self._basic_generate_signed_url_helper()

    def test_generate_signed_url_w_content_type(self):
        BLOB_NAME = 'blob-name'
        EXPIRATION = '2014-10-16T20:34:37.000Z'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37.000Z')

        SIGNER = _Signer()
        CONTENT_TYPE = "text/html"
        with mock.patch('google.cloud.storage.blob.generate_signed_url',
                        new=SIGNER):
            signed_url = blob.generate_signed_url(EXPIRATION,
                                                  content_type=CONTENT_TYPE)
            self.assertEqual(signed_url, URI)

        PATH = '/name/%s' % (BLOB_NAME,)
        EXPECTED_ARGS = (_Connection.credentials,)
        EXPECTED_KWARGS = {
            'api_access_endpoint': 'https://storage.googleapis.com',
            'expiration': EXPIRATION,
            'method': 'GET',
            'resource': PATH,
            'content_type': CONTENT_TYPE,
            'response_type': None,
            'response_disposition': None,
            'generation': None,
        }
        self.assertEqual(SIGNER._signed, [(EXPECTED_ARGS, EXPECTED_KWARGS)])

    def test_generate_signed_url_w_credentials(self):
        credentials = object()
        self._basic_generate_signed_url_helper(credentials=credentials)

    def test_generate_signed_url_w_slash_in_name(self):
        BLOB_NAME = 'parent/child'
        EXPIRATION = '2014-10-16T20:34:37.000Z'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37.000Z')

        SIGNER = _Signer()
        with mock.patch('google.cloud.storage.blob.generate_signed_url',
                        new=SIGNER):
            signed_url = blob.generate_signed_url(EXPIRATION)
            self.assertEqual(signed_url, URI)

        EXPECTED_ARGS = (_Connection.credentials,)
        EXPECTED_KWARGS = {
            'api_access_endpoint': 'https://storage.googleapis.com',
            'expiration': EXPIRATION,
            'method': 'GET',
            'resource': '/name/parent%2Fchild',
            'content_type': None,
            'response_type': None,
            'response_disposition': None,
            'generation': None,
        }
        self.assertEqual(SIGNER._signed, [(EXPECTED_ARGS, EXPECTED_KWARGS)])

    def test_generate_signed_url_w_method_arg(self):
        BLOB_NAME = 'blob-name'
        EXPIRATION = '2014-10-16T20:34:37.000Z'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        URI = ('http://example.com/abucket/a-blob-name?Signature=DEADBEEF'
               '&Expiration=2014-10-16T20:34:37.000Z')

        SIGNER = _Signer()
        with mock.patch('google.cloud.storage.blob.generate_signed_url',
                        new=SIGNER):
            signed_uri = blob.generate_signed_url(EXPIRATION, method='POST')
            self.assertEqual(signed_uri, URI)

        PATH = '/name/%s' % (BLOB_NAME,)
        EXPECTED_ARGS = (_Connection.credentials,)
        EXPECTED_KWARGS = {
            'api_access_endpoint': 'https://storage.googleapis.com',
            'expiration': EXPIRATION,
            'method': 'POST',
            'resource': PATH,
            'content_type': None,
            'response_type': None,
            'response_disposition': None,
            'generation': None,
        }
        self.assertEqual(SIGNER._signed, [(EXPECTED_ARGS, EXPECTED_KWARGS)])

    def test_exists_miss(self):
        from six.moves.http_client import NOT_FOUND

        NONESUCH = 'nonesuch'
        not_found_response = ({'status': NOT_FOUND}, b'')
        connection = _Connection(not_found_response)
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(NONESUCH, bucket=bucket)
        self.assertFalse(blob.exists())

    def test_exists_hit(self):
        from six.moves.http_client import OK

        BLOB_NAME = 'blob-name'
        found_response = ({'status': OK}, b'')
        connection = _Connection(found_response)
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        bucket._blobs[BLOB_NAME] = 1
        self.assertTrue(blob.exists())

    def test_delete(self):
        from six.moves.http_client import NOT_FOUND
        BLOB_NAME = 'blob-name'
        not_found_response = ({'status': NOT_FOUND}, b'')
        connection = _Connection(not_found_response)
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        bucket._blobs[BLOB_NAME] = 1
        blob.delete()
        self.assertFalse(blob.exists())
        self.assertEqual(bucket._deleted, [(BLOB_NAME, None)])

    def test_download_to_file_wo_media_link(self):
        from io import BytesIO
        from six.moves.http_client import OK
        from six.moves.http_client import PARTIAL_CONTENT

        BLOB_NAME = 'blob-name'
        MEDIA_LINK = 'http://example.com/media/'
        chunk1_response = {'status': PARTIAL_CONTENT,
                           'content-range': 'bytes 0-2/6'}
        chunk2_response = {'status': OK,
                           'content-range': 'bytes 3-5/6'}
        connection = _Connection(
            (chunk1_response, b'abc'),
            (chunk2_response, b'def'),
        )
        # Only the 'reload' request hits on this side:  the others are done
        # through the 'http' object.
        reload_response = {'status': OK, 'content-type': 'application/json'}
        connection._responses = [(reload_response, {"mediaLink": MEDIA_LINK})]
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        fh = BytesIO()
        blob.download_to_file(fh)
        self.assertEqual(fh.getvalue(), b'abcdef')
        self.assertEqual(blob.media_link, MEDIA_LINK)

    def _download_to_file_helper(self, chunk_size=None):
        from io import BytesIO
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
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
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
        from google.cloud._testing import _NamedTemporaryFile

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
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 3

        with _NamedTemporaryFile() as temp:
            blob.download_to_filename(temp.name)
            with open(temp.name, 'rb') as file_obj:
                wrote = file_obj.read()
                mtime = os.path.getmtime(temp.name)
                updatedTime = time.mktime(blob.updated.timetuple())

        self.assertEqual(wrote, b'abcdef')
        self.assertEqual(mtime, updatedTime)

    def test_download_to_filename_w_key(self):
        import os
        import time
        from six.moves.http_client import OK
        from six.moves.http_client import PARTIAL_CONTENT
        from google.cloud._testing import _NamedTemporaryFile

        BLOB_NAME = 'blob-name'
        KEY = b'aa426195405adee2c8081bb9e7e74b19'
        HEADER_KEY_VALUE = 'YWE0MjYxOTU0MDVhZGVlMmM4MDgxYmI5ZTdlNzRiMTk='
        HEADER_KEY_HASH_VALUE = 'V3Kwe46nKc3xLv96+iJ707YfZfFvlObta8TQcx2gpm0='
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
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties,
                              encryption_key=KEY)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 3

        with _NamedTemporaryFile() as temp:
            blob.download_to_filename(temp.name)
            with open(temp.name, 'rb') as file_obj:
                wrote = file_obj.read()
                mtime = os.path.getmtime(temp.name)
                updatedTime = time.mktime(blob.updated.timetuple())

        rq = connection.http._requested
        headers = {
            x.title(): str(y) for x, y in rq[0]['headers'].items()}
        self.assertEqual(headers['X-Goog-Encryption-Algorithm'], 'AES256')
        self.assertEqual(headers['X-Goog-Encryption-Key'], HEADER_KEY_VALUE)
        self.assertEqual(headers['X-Goog-Encryption-Key-Sha256'],
                         HEADER_KEY_HASH_VALUE)
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
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 3
        fetched = blob.download_as_string()
        self.assertEqual(fetched, b'abcdef')

    def test_upload_from_file_size_failure(self):
        BLOB_NAME = 'blob-name'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        file_obj = object()
        with self.assertRaises(ValueError):
            blob.upload_from_file(file_obj, size=None)

    def _upload_from_file_simple_test_helper(self, properties=None,
                                             content_type_arg=None,
                                             expected_content_type=None,
                                             chunk_size=5,
                                             status=None):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from google.cloud._testing import _NamedTemporaryFile

        BLOB_NAME = 'blob-name'
        DATA = b'ABCDEF'
        if status is None:
            status = OK
        response = {'status': status}
        connection = _Connection(
            (response, b'{}'),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = chunk_size

        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'wb') as file_obj:
                file_obj.write(DATA)

            with open(temp.name, 'rb') as file_obj:
                blob.upload_from_file(file_obj, rewind=True,
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
        headers = {
            x.title(): str(y) for x, y in rq[0]['headers'].items()}
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], expected_content_type)

    def test_upload_from_file_stream(self):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from google.cloud.streaming import http_wrapper

        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = b'ABCDE'
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
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5

        file_obj = _Stream(DATA)

        # Mock stream closes at end of data, like a socket might
        def is_stream_closed(stream):
            if stream.tell() < len(DATA):
                return stream._closed
            else:
                return stream.close() or True

        _Stream.closed = property(is_stream_closed)

        def fileno_mock():
            from io import UnsupportedOperation
            raise UnsupportedOperation()

        file_obj.fileno = fileno_mock

        blob.upload_from_file(file_obj)

        # Remove the temp property
        delattr(_Stream, "closed")

        rq = connection.http._requested
        self.assertEqual(len(rq), 3)

        # Requested[0]
        headers = {
            x.title(): str(y) for x, y in rq[0].pop('headers').items()}
        self.assertEqual(headers['Content-Length'], '0')
        self.assertEqual(headers['X-Upload-Content-Type'],
                         'application/octet-stream')

        uri = rq[0].pop('uri')
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable', 'name': BLOB_NAME})
        self.assertEqual(rq[0], {
            'method': 'POST',
            'body': '',
            'connection_type': None,
            'redirections': 5,
        })

        # Requested[1]
        headers = {
            x.title(): str(y) for x, y in rq[1].pop('headers').items()}
        self.assertEqual(headers['Content-Range'], 'bytes 0-4/*')
        self.assertEqual(rq[1], {
            'method': 'PUT',
            'uri': UPLOAD_URL,
            'body': DATA[:5],
            'connection_type': None,
            'redirections': 5,
        })

        # Requested[2]
        headers = {
            x.title(): str(y) for x, y in rq[2].pop('headers').items()}
        self.assertEqual(headers['Content-Range'], 'bytes */5')
        self.assertEqual(rq[2], {
            'method': 'PUT',
            'uri': UPLOAD_URL,
            'body': DATA[5:],
            'connection_type': None,
            'redirections': 5,
        })

    def test_upload_from_file_simple(self):
        self._upload_from_file_simple_test_helper(
            expected_content_type='application/octet-stream')

    def test_upload_from_file_simple_not_found(self):
        from six.moves.http_client import NOT_FOUND
        from google.cloud.exceptions import NotFound

        with self.assertRaises(NotFound):
            self._upload_from_file_simple_test_helper(status=NOT_FOUND)

    def test_upload_from_file_simple_w_chunk_size_None(self):
        self._upload_from_file_simple_test_helper(
            expected_content_type='application/octet-stream',
            chunk_size=None)

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
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud.streaming import http_wrapper

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
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5

        # Set the threshhold low enough that we force a resumable upload.
        patch = mock.patch(
            'google.cloud.streaming.transfer.RESUMABLE_UPLOAD_THRESHOLD',
            new=5)

        with patch:
            with _NamedTemporaryFile() as temp:
                with open(temp.name, 'wb') as file_obj:
                    file_obj.write(DATA)
                with open(temp.name, 'rb') as file_obj:
                    blob.upload_from_file(file_obj, rewind=True)

        rq = connection.http._requested
        self.assertEqual(len(rq), 3)

        # Requested[0]
        headers = {
            x.title(): str(y) for x, y in rq[0].pop('headers').items()}
        self.assertEqual(headers['X-Upload-Content-Length'], '6')
        self.assertEqual(headers['X-Upload-Content-Type'],
                         'application/octet-stream')

        uri = rq[0].pop('uri')
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable', 'name': BLOB_NAME})
        self.assertEqual(rq[0], {
            'method': 'POST',
            'body': '',
            'connection_type': None,
            'redirections': 5,
        })

        # Requested[1]
        headers = {
            x.title(): str(y) for x, y in rq[1].pop('headers').items()}
        self.assertEqual(headers['Content-Range'], 'bytes 0-4/6')
        self.assertEqual(rq[1], {
            'method': 'PUT',
            'uri': UPLOAD_URL,
            'body': DATA[:5],
            'connection_type': None,
            'redirections': 5,
        })

        # Requested[2]
        headers = {
            x.title(): str(y) for x, y in rq[2].pop('headers').items()}
        self.assertEqual(headers['Content-Range'], 'bytes 5-5/6')
        self.assertEqual(rq[2], {
            'method': 'PUT',
            'uri': UPLOAD_URL,
            'body': DATA[5:],
            'connection_type': None,
            'redirections': 5,
        })

    def test_upload_from_file_resumable_w_error(self):
        from six.moves.http_client import NOT_FOUND
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud.streaming.exceptions import HttpError

        BLOB_NAME = 'blob-name'
        DATA = b'ABCDEF'
        loc_response = {'status': NOT_FOUND}
        connection = _Connection(
            (loc_response, b'{"error": "no such bucket"}'),
        )
        client = _Client(connection)
        bucket = _Bucket(client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5

        # Set the threshhold low enough that we force a resumable upload.
        patch = mock.patch(
            'google.cloud.streaming.transfer.RESUMABLE_UPLOAD_THRESHOLD',
            new=5)

        with patch:
            with _NamedTemporaryFile() as temp:
                with open(temp.name, 'wb') as file_obj:
                    file_obj.write(DATA)
                with open(temp.name, 'rb') as file_obj:
                    with self.assertRaises(HttpError):
                        blob.upload_from_file(file_obj, rewind=True)

        rq = connection.http._requested
        self.assertEqual(len(rq), 1)

        # Requested[0]
        headers = {
            x.title(): str(y) for x, y in rq[0].pop('headers').items()}
        self.assertEqual(headers['X-Upload-Content-Length'], '6')
        self.assertEqual(headers['X-Upload-Content-Type'],
                         'application/octet-stream')

        uri = rq[0].pop('uri')
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable', 'name': BLOB_NAME})
        self.assertEqual(rq[0], {
            'method': 'POST',
            'body': '',
            'connection_type': None,
            'redirections': 5,
        })

    def test_upload_from_file_w_slash_in_name(self):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud.streaming import http_wrapper

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
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5

        with _NamedTemporaryFile() as temp:
            with open(temp.name, 'wb') as file_obj:
                file_obj.write(DATA)
            with open(temp.name, 'rb') as file_obj:
                blob.upload_from_file(file_obj, rewind=True)
                self.assertEqual(file_obj.tell(), len(DATA))

        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['redirections'], 5)
        self.assertEqual(rq[0]['body'], DATA)
        self.assertIsNone(rq[0]['connection_type'])
        self.assertEqual(rq[0]['method'], 'POST')
        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'media', 'name': 'parent/child'})
        headers = {
            x.title(): str(y) for x, y in rq[0]['headers'].items()}
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'application/octet-stream')

    def test_upload_from_filename_w_key(self):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud.streaming import http_wrapper

        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        DATA = b'ABCDEF'
        KEY = b'aa426195405adee2c8081bb9e7e74b19'
        HEADER_KEY_VALUE = 'YWE0MjYxOTU0MDVhZGVlMmM4MDgxYmI5ZTdlNzRiMTk='
        HEADER_KEY_HASH_VALUE = 'V3Kwe46nKc3xLv96+iJ707YfZfFvlObta8TQcx2gpm0='
        EXPECTED_CONTENT_TYPE = 'foo/bar'
        properties = {'contentType': EXPECTED_CONTENT_TYPE}
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
        blob = self._make_one(BLOB_NAME, bucket=bucket,
                              properties=properties, encryption_key=KEY)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5

        with _NamedTemporaryFile(suffix='.jpeg') as temp:
            with open(temp.name, 'wb') as file_obj:
                file_obj.write(DATA)
            blob.upload_from_filename(temp.name,
                                      content_type=EXPECTED_CONTENT_TYPE)

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
        headers = {
            x.title(): str(y) for x, y in rq[0]['headers'].items()}
        self.assertEqual(headers['X-Goog-Encryption-Algorithm'], 'AES256')
        self.assertEqual(headers['X-Goog-Encryption-Key'], HEADER_KEY_VALUE)
        self.assertEqual(headers['X-Goog-Encryption-Key-Sha256'],
                         HEADER_KEY_HASH_VALUE)
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'foo/bar')

    def _upload_from_filename_test_helper(self, properties=None,
                                          content_type_arg=None,
                                          expected_content_type=None):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from google.cloud._testing import _NamedTemporaryFile
        from google.cloud.streaming import http_wrapper

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
        blob = self._make_one(BLOB_NAME, bucket=bucket,
                              properties=properties)
        blob._CHUNK_SIZE_MULTIPLE = 1
        blob.chunk_size = 5

        with _NamedTemporaryFile(suffix='.jpeg') as temp:
            with open(temp.name, 'wb') as file_obj:
                file_obj.write(DATA)
            blob.upload_from_filename(temp.name,
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
        headers = {
            x.title(): str(y) for x, y in rq[0]['headers'].items()}
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
        from google.cloud.streaming import http_wrapper

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
        blob = self._make_one(BLOB_NAME, bucket=bucket)
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
        headers = {
            x.title(): str(y) for x, y in rq[0]['headers'].items()}
        self.assertEqual(headers['Content-Length'], '6')
        self.assertEqual(headers['Content-Type'], 'text/plain')
        self.assertEqual(rq[0]['body'], DATA)

    def test_upload_from_string_w_text(self):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from google.cloud.streaming import http_wrapper

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
        blob = self._make_one(BLOB_NAME, bucket=bucket)
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
        headers = {
            x.title(): str(y) for x, y in rq[0]['headers'].items()}
        self.assertEqual(headers['Content-Length'], str(len(ENCODED)))
        self.assertEqual(headers['Content-Type'], 'text/plain')
        self.assertEqual(rq[0]['body'], ENCODED)

    def test_upload_from_string_text_w_key(self):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit
        from google.cloud.streaming import http_wrapper

        BLOB_NAME = 'blob-name'
        KEY = b'aa426195405adee2c8081bb9e7e74b19'
        HEADER_KEY_VALUE = 'YWE0MjYxOTU0MDVhZGVlMmM4MDgxYmI5ZTdlNzRiMTk='
        HEADER_KEY_HASH_VALUE = 'V3Kwe46nKc3xLv96+iJ707YfZfFvlObta8TQcx2gpm0='
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
        blob = self._make_one(BLOB_NAME, bucket=bucket, encryption_key=KEY)
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
        headers = {
            x.title(): str(y) for x, y in rq[0]['headers'].items()}

        self.assertEqual(headers['X-Goog-Encryption-Algorithm'], 'AES256')
        self.assertEqual(headers['X-Goog-Encryption-Key'], HEADER_KEY_VALUE)
        self.assertEqual(headers['X-Goog-Encryption-Key-Sha256'],
                         HEADER_KEY_HASH_VALUE)
        self.assertEqual(headers['Content-Length'], str(len(ENCODED)))
        self.assertEqual(headers['Content-Type'], 'text/plain')
        self.assertEqual(rq[0]['body'], ENCODED)

    def test_create_resumable_upload_session(self):
        from six.moves.http_client import OK
        from six.moves.urllib.parse import parse_qsl
        from six.moves.urllib.parse import urlsplit

        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        loc_response = {'status': OK, 'location': UPLOAD_URL}
        connection = _Connection(
            (loc_response, '{}'),
        )
        client = _Client(connection)
        bucket = _Bucket(client=client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)

        resumable_url = blob.create_resumable_upload_session()

        self.assertEqual(resumable_url, UPLOAD_URL)

        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')

        uri = rq[0]['uri']
        scheme, netloc, path, qs, _ = urlsplit(uri)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'example.com')
        self.assertEqual(path, '/b/name/o')
        self.assertEqual(dict(parse_qsl(qs)),
                         {'uploadType': 'resumable', 'name': BLOB_NAME})
        headers = {
            key.title(): str(value) for key, value in rq[0]['headers'].items()}
        self.assertEqual(headers['Content-Length'], '0')
        self.assertEqual(
            headers['X-Upload-Content-Type'], 'application/octet-stream')

    def test_create_resumable_upload_session_args(self):
        from six.moves.http_client import OK

        BLOB_NAME = 'blob-name'
        UPLOAD_URL = 'http://example.com/upload/name/key'
        CONTENT_TYPE = 'text/plain'
        SIZE = 1024
        ORIGIN = 'http://google.com'

        loc_response = {'status': OK, 'location': UPLOAD_URL}
        connection = _Connection(
            (loc_response, '{}'),
        )
        client = _Client(connection)
        bucket = _Bucket(client=client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)

        resumable_url = blob.create_resumable_upload_session(
            content_type=CONTENT_TYPE,
            size=SIZE,
            origin=ORIGIN)

        self.assertEqual(resumable_url, UPLOAD_URL)

        rq = connection.http._requested
        self.assertEqual(len(rq), 1)
        self.assertEqual(rq[0]['method'], 'POST')

        headers = {
            key.title(): str(value) for key, value in rq[0]['headers'].items()}
        self.assertEqual(headers['Content-Length'], '0')
        self.assertEqual(headers['X-Upload-Content-Length'], str(SIZE))
        self.assertEqual(
            headers['X-Upload-Content-Type'], 'text/plain')
        self.assertEqual(
            headers['Origin'], ORIGIN)

    def test_make_public(self):
        from six.moves.http_client import OK
        from google.cloud.storage.acl import _ACLEntity

        BLOB_NAME = 'blob-name'
        permissive = [{'entity': 'allUsers', 'role': _ACLEntity.READER_ROLE}]
        after = ({'status': OK}, {'acl': permissive})
        connection = _Connection(after)
        client = _Client(connection)
        bucket = _Bucket(client=client)
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        blob.acl.loaded = True
        blob.make_public()
        self.assertEqual(list(blob.acl), permissive)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s' % BLOB_NAME)
        self.assertEqual(kw[0]['data'], {'acl': permissive})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_compose_wo_content_type_set(self):
        SOURCE_1 = 'source-1'
        SOURCE_2 = 'source-2'
        DESTINATION = 'destinaton'
        connection = _Connection()
        client = _Client(connection)
        bucket = _Bucket(client=client)
        source_1 = self._make_one(SOURCE_1, bucket=bucket)
        source_2 = self._make_one(SOURCE_2, bucket=bucket)
        destination = self._make_one(DESTINATION, bucket=bucket)

        with self.assertRaises(ValueError):
            destination.compose(sources=[source_1, source_2])

    def test_compose_minimal(self):
        from six.moves.http_client import OK

        SOURCE_1 = 'source-1'
        SOURCE_2 = 'source-2'
        DESTINATION = 'destinaton'
        RESOURCE = {
            'etag': 'DEADBEEF'
        }
        after = ({'status': OK}, RESOURCE)
        connection = _Connection(after)
        client = _Client(connection)
        bucket = _Bucket(client=client)
        source_1 = self._make_one(SOURCE_1, bucket=bucket)
        source_2 = self._make_one(SOURCE_2, bucket=bucket)
        destination = self._make_one(DESTINATION, bucket=bucket)
        destination.content_type = 'text/plain'

        destination.compose(sources=[source_1, source_2])

        self.assertEqual(destination.etag, 'DEADBEEF')

        SENT = {
            'sourceObjects': [
                {'name': source_1.name},
                {'name': source_2.name},
            ],
            'destination': {
                'contentType': 'text/plain',
            },
        }
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'POST')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s/compose' % DESTINATION)
        self.assertEqual(kw[0]['data'], SENT)

    def test_compose_w_additional_property_changes(self):
        from six.moves.http_client import OK

        SOURCE_1 = 'source-1'
        SOURCE_2 = 'source-2'
        DESTINATION = 'destinaton'
        RESOURCE = {
            'etag': 'DEADBEEF'
        }
        after = ({'status': OK}, RESOURCE)
        connection = _Connection(after)
        client = _Client(connection)
        bucket = _Bucket(client=client)
        source_1 = self._make_one(SOURCE_1, bucket=bucket)
        source_2 = self._make_one(SOURCE_2, bucket=bucket)
        destination = self._make_one(DESTINATION, bucket=bucket)
        destination.content_type = 'text/plain'
        destination.content_language = 'en-US'
        destination.metadata = {'my-key': 'my-value'}

        destination.compose(sources=[source_1, source_2])

        self.assertEqual(destination.etag, 'DEADBEEF')

        SENT = {
            'sourceObjects': [
                {'name': source_1.name},
                {'name': source_2.name},
            ],
            'destination': {
                'contentType': 'text/plain',
                'contentLanguage': 'en-US',
                'metadata': {
                    'my-key': 'my-value',
                }
            },
        }
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'POST')
        self.assertEqual(kw[0]['path'], '/b/name/o/%s/compose' % DESTINATION)
        self.assertEqual(kw[0]['data'], SENT)

    def test_rewrite_other_bucket_other_name_no_encryption_partial(self):
        from six.moves.http_client import OK

        SOURCE_BLOB = 'source'
        DEST_BLOB = 'dest'
        DEST_BUCKET = 'other-bucket'
        TOKEN = 'TOKEN'
        RESPONSE = {
            'totalBytesRewritten': 33,
            'objectSize': 42,
            'done': False,
            'rewriteToken': TOKEN,
            'resource': {'etag': 'DEADBEEF'},
        }
        response = ({'status': OK}, RESPONSE)
        connection = _Connection(response)
        client = _Client(connection)
        source_bucket = _Bucket(client=client)
        source_blob = self._make_one(SOURCE_BLOB, bucket=source_bucket)
        dest_bucket = _Bucket(client=client, name=DEST_BUCKET)
        dest_blob = self._make_one(DEST_BLOB, bucket=dest_bucket)

        token, rewritten, size = dest_blob.rewrite(source_blob)

        self.assertEqual(token, TOKEN)
        self.assertEqual(rewritten, 33)
        self.assertEqual(size, 42)

        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'POST')
        PATH = '/b/name/o/%s/rewriteTo/b/%s/o/%s' % (
            SOURCE_BLOB, DEST_BUCKET, DEST_BLOB)
        self.assertEqual(kw[0]['path'], PATH)
        self.assertEqual(kw[0]['query_params'], {})
        SENT = {}
        self.assertEqual(kw[0]['data'], SENT)

        headers = {
            key.title(): str(value) for key, value in kw[0]['headers'].items()}
        self.assertNotIn('X-Goog-Copy-Source-Encryption-Algorithm', headers)
        self.assertNotIn('X-Goog-Copy-Source-Encryption-Key', headers)
        self.assertNotIn('X-Goog-Copy-Source-Encryption-Key-Sha256', headers)
        self.assertNotIn('X-Goog-Encryption-Algorithm', headers)
        self.assertNotIn('X-Goog-Encryption-Key', headers)
        self.assertNotIn('X-Goog-Encryption-Key-Sha256', headers)

    def test_rewrite_same_name_no_old_key_new_key_done(self):
        import base64
        import hashlib
        from six.moves.http_client import OK

        KEY = b'01234567890123456789012345678901'  # 32 bytes
        KEY_B64 = base64.b64encode(KEY).rstrip().decode('ascii')
        KEY_HASH = hashlib.sha256(KEY).digest()
        KEY_HASH_B64 = base64.b64encode(KEY_HASH).rstrip().decode('ascii')
        BLOB_NAME = 'blob'
        RESPONSE = {
            'totalBytesRewritten': 42,
            'objectSize': 42,
            'done': True,
            'resource': {'etag': 'DEADBEEF'},
        }
        response = ({'status': OK}, RESPONSE)
        connection = _Connection(response)
        client = _Client(connection)
        bucket = _Bucket(client=client)
        plain = self._make_one(BLOB_NAME, bucket=bucket)
        encrypted = self._make_one(BLOB_NAME, bucket=bucket,
                                   encryption_key=KEY)

        token, rewritten, size = encrypted.rewrite(plain)

        self.assertIsNone(token)
        self.assertEqual(rewritten, 42)
        self.assertEqual(size, 42)

        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'POST')
        PATH = '/b/name/o/%s/rewriteTo/b/name/o/%s' % (BLOB_NAME, BLOB_NAME)
        self.assertEqual(kw[0]['path'], PATH)
        self.assertEqual(kw[0]['query_params'], {})
        SENT = {}
        self.assertEqual(kw[0]['data'], SENT)

        headers = {
            key.title(): str(value) for key, value in kw[0]['headers'].items()}
        self.assertNotIn('X-Goog-Copy-Source-Encryption-Algorithm', headers)
        self.assertNotIn('X-Goog-Copy-Source-Encryption-Key', headers)
        self.assertNotIn('X-Goog-Copy-Source-Encryption-Key-Sha256', headers)
        self.assertEqual(headers['X-Goog-Encryption-Algorithm'], 'AES256')
        self.assertEqual(headers['X-Goog-Encryption-Key'], KEY_B64)
        self.assertEqual(headers['X-Goog-Encryption-Key-Sha256'], KEY_HASH_B64)

    def test_rewrite_same_name_no_key_new_key_w_token(self):
        import base64
        import hashlib
        from six.moves.http_client import OK

        SOURCE_KEY = b'01234567890123456789012345678901'  # 32 bytes
        SOURCE_KEY_B64 = base64.b64encode(SOURCE_KEY).rstrip().decode('ascii')
        SOURCE_KEY_HASH = hashlib.sha256(SOURCE_KEY).digest()
        SOURCE_KEY_HASH_B64 = base64.b64encode(
            SOURCE_KEY_HASH).rstrip().decode('ascii')
        DEST_KEY = b'90123456789012345678901234567890'  # 32 bytes
        DEST_KEY_B64 = base64.b64encode(DEST_KEY).rstrip().decode('ascii')
        DEST_KEY_HASH = hashlib.sha256(DEST_KEY).digest()
        DEST_KEY_HASH_B64 = base64.b64encode(
            DEST_KEY_HASH).rstrip().decode('ascii')
        BLOB_NAME = 'blob'
        TOKEN = 'TOKEN'
        RESPONSE = {
            'totalBytesRewritten': 42,
            'objectSize': 42,
            'done': True,
            'resource': {'etag': 'DEADBEEF'},
        }
        response = ({'status': OK}, RESPONSE)
        connection = _Connection(response)
        client = _Client(connection)
        bucket = _Bucket(client=client)
        source = self._make_one(
            BLOB_NAME, bucket=bucket, encryption_key=SOURCE_KEY)
        dest = self._make_one(BLOB_NAME, bucket=bucket,
                              encryption_key=DEST_KEY)

        token, rewritten, size = dest.rewrite(source, token=TOKEN)

        self.assertIsNone(token)
        self.assertEqual(rewritten, 42)
        self.assertEqual(size, 42)

        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'POST')
        PATH = '/b/name/o/%s/rewriteTo/b/name/o/%s' % (BLOB_NAME, BLOB_NAME)
        self.assertEqual(kw[0]['path'], PATH)
        self.assertEqual(kw[0]['query_params'], {'rewriteToken': TOKEN})
        SENT = {}
        self.assertEqual(kw[0]['data'], SENT)

        headers = {
            key.title(): str(value) for key, value in kw[0]['headers'].items()}
        self.assertEqual(
            headers['X-Goog-Copy-Source-Encryption-Algorithm'], 'AES256')
        self.assertEqual(
            headers['X-Goog-Copy-Source-Encryption-Key'], SOURCE_KEY_B64)
        self.assertEqual(
            headers['X-Goog-Copy-Source-Encryption-Key-Sha256'],
            SOURCE_KEY_HASH_B64)
        self.assertEqual(
            headers['X-Goog-Encryption-Algorithm'], 'AES256')
        self.assertEqual(
            headers['X-Goog-Encryption-Key'], DEST_KEY_B64)
        self.assertEqual(
            headers['X-Goog-Encryption-Key-Sha256'], DEST_KEY_HASH_B64)

    def test_cache_control_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CACHE_CONTROL = 'no-cache'
        properties = {'cacheControl': CACHE_CONTROL}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.cache_control, CACHE_CONTROL)

    def test_cache_control_setter(self):
        BLOB_NAME = 'blob-name'
        CACHE_CONTROL = 'no-cache'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertIsNone(blob.cache_control)
        blob.cache_control = CACHE_CONTROL
        self.assertEqual(blob.cache_control, CACHE_CONTROL)

    def test_component_count(self):
        BUCKET = object()
        COMPONENT_COUNT = 42
        blob = self._make_one('blob-name', bucket=BUCKET,
                              properties={'componentCount': COMPONENT_COUNT})
        self.assertEqual(blob.component_count, COMPONENT_COUNT)

    def test_component_count_unset(self):
        BUCKET = object()
        blob = self._make_one('blob-name', bucket=BUCKET)
        self.assertIsNone(blob.component_count)

    def test_component_count_string_val(self):
        BUCKET = object()
        COMPONENT_COUNT = 42
        blob = self._make_one(
            'blob-name', bucket=BUCKET,
            properties={'componentCount': str(COMPONENT_COUNT)})
        self.assertEqual(blob.component_count, COMPONENT_COUNT)

    def test_content_disposition_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CONTENT_DISPOSITION = 'Attachment; filename=example.jpg'
        properties = {'contentDisposition': CONTENT_DISPOSITION}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.content_disposition, CONTENT_DISPOSITION)

    def test_content_disposition_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_DISPOSITION = 'Attachment; filename=example.jpg'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertIsNone(blob.content_disposition)
        blob.content_disposition = CONTENT_DISPOSITION
        self.assertEqual(blob.content_disposition, CONTENT_DISPOSITION)

    def test_content_encoding_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CONTENT_ENCODING = 'gzip'
        properties = {'contentEncoding': CONTENT_ENCODING}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.content_encoding, CONTENT_ENCODING)

    def test_content_encoding_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_ENCODING = 'gzip'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertIsNone(blob.content_encoding)
        blob.content_encoding = CONTENT_ENCODING
        self.assertEqual(blob.content_encoding, CONTENT_ENCODING)

    def test_content_language_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CONTENT_LANGUAGE = 'pt-BR'
        properties = {'contentLanguage': CONTENT_LANGUAGE}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.content_language, CONTENT_LANGUAGE)

    def test_content_language_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_LANGUAGE = 'pt-BR'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertIsNone(blob.content_language)
        blob.content_language = CONTENT_LANGUAGE
        self.assertEqual(blob.content_language, CONTENT_LANGUAGE)

    def test_content_type_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CONTENT_TYPE = 'image/jpeg'
        properties = {'contentType': CONTENT_TYPE}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.content_type, CONTENT_TYPE)

    def test_content_type_setter(self):
        BLOB_NAME = 'blob-name'
        CONTENT_TYPE = 'image/jpeg'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertIsNone(blob.content_type)
        blob.content_type = CONTENT_TYPE
        self.assertEqual(blob.content_type, CONTENT_TYPE)

    def test_crc32c_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        CRC32C = 'DEADBEEF'
        properties = {'crc32c': CRC32C}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.crc32c, CRC32C)

    def test_crc32c_setter(self):
        BLOB_NAME = 'blob-name'
        CRC32C = 'DEADBEEF'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertIsNone(blob.crc32c)
        blob.crc32c = CRC32C
        self.assertEqual(blob.crc32c, CRC32C)

    def test_etag(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        ETAG = 'ETAG'
        properties = {'etag': ETAG}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.etag, ETAG)

    def test_generation(self):
        BUCKET = object()
        GENERATION = 42
        blob = self._make_one('blob-name', bucket=BUCKET,
                              properties={'generation': GENERATION})
        self.assertEqual(blob.generation, GENERATION)

    def test_generation_unset(self):
        BUCKET = object()
        blob = self._make_one('blob-name', bucket=BUCKET)
        self.assertIsNone(blob.generation)

    def test_generation_string_val(self):
        BUCKET = object()
        GENERATION = 42
        blob = self._make_one('blob-name', bucket=BUCKET,
                              properties={'generation': str(GENERATION)})
        self.assertEqual(blob.generation, GENERATION)

    def test_id(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        ID = 'ID'
        properties = {'id': ID}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.id, ID)

    def test_md5_hash_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        MD5_HASH = 'DEADBEEF'
        properties = {'md5Hash': MD5_HASH}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.md5_hash, MD5_HASH)

    def test_md5_hash_setter(self):
        BLOB_NAME = 'blob-name'
        MD5_HASH = 'DEADBEEF'
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertIsNone(blob.md5_hash)
        blob.md5_hash = MD5_HASH
        self.assertEqual(blob.md5_hash, MD5_HASH)

    def test_media_link(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        MEDIA_LINK = 'http://example.com/media/'
        properties = {'mediaLink': MEDIA_LINK}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.media_link, MEDIA_LINK)

    def test_metadata_getter(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        METADATA = {'foo': 'Foo'}
        properties = {'metadata': METADATA}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.metadata, METADATA)

    def test_metadata_setter(self):
        BLOB_NAME = 'blob-name'
        METADATA = {'foo': 'Foo'}
        bucket = _Bucket()
        blob = self._make_one(BLOB_NAME, bucket=bucket)
        self.assertIsNone(blob.metadata)
        blob.metadata = METADATA
        self.assertEqual(blob.metadata, METADATA)

    def test_metageneration(self):
        BUCKET = object()
        METAGENERATION = 42
        blob = self._make_one('blob-name', bucket=BUCKET,
                              properties={'metageneration': METAGENERATION})
        self.assertEqual(blob.metageneration, METAGENERATION)

    def test_metageneration_unset(self):
        BUCKET = object()
        blob = self._make_one('blob-name', bucket=BUCKET)
        self.assertIsNone(blob.metageneration)

    def test_metageneration_string_val(self):
        BUCKET = object()
        METAGENERATION = 42
        blob = self._make_one(
            'blob-name', bucket=BUCKET,
            properties={'metageneration': str(METAGENERATION)})
        self.assertEqual(blob.metageneration, METAGENERATION)

    def test_owner(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        OWNER = {'entity': 'project-owner-12345', 'entityId': '23456'}
        properties = {'owner': OWNER}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        owner = blob.owner
        self.assertEqual(owner['entity'], 'project-owner-12345')
        self.assertEqual(owner['entityId'], '23456')

    def test_self_link(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        SELF_LINK = 'http://example.com/self/'
        properties = {'selfLink': SELF_LINK}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.self_link, SELF_LINK)

    def test_size(self):
        BUCKET = object()
        SIZE = 42
        blob = self._make_one('blob-name', bucket=BUCKET,
                              properties={'size': SIZE})
        self.assertEqual(blob.size, SIZE)

    def test_size_unset(self):
        BUCKET = object()
        blob = self._make_one('blob-name', bucket=BUCKET)
        self.assertIsNone(blob.size)

    def test_size_string_val(self):
        BUCKET = object()
        SIZE = 42
        blob = self._make_one('blob-name', bucket=BUCKET,
                              properties={'size': str(SIZE)})
        self.assertEqual(blob.size, SIZE)

    def test_storage_class(self):
        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        STORAGE_CLASS = 'http://example.com/self/'
        properties = {'storageClass': STORAGE_CLASS}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.storage_class, STORAGE_CLASS)

    def test_time_deleted(self):
        import datetime
        from google.cloud._helpers import _RFC3339_MICROS
        from google.cloud._helpers import UTC

        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        TIMESTAMP = datetime.datetime(2014, 11, 5, 20, 34, 37, tzinfo=UTC)
        TIME_DELETED = TIMESTAMP.strftime(_RFC3339_MICROS)
        properties = {'timeDeleted': TIME_DELETED}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.time_deleted, TIMESTAMP)

    def test_time_deleted_unset(self):
        BUCKET = object()
        blob = self._make_one('blob-name', bucket=BUCKET)
        self.assertIsNone(blob.time_deleted)

    def test_time_created(self):
        import datetime
        from google.cloud._helpers import _RFC3339_MICROS
        from google.cloud._helpers import UTC

        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        TIMESTAMP = datetime.datetime(2014, 11, 5, 20, 34, 37, tzinfo=UTC)
        TIME_CREATED = TIMESTAMP.strftime(_RFC3339_MICROS)
        properties = {'timeCreated': TIME_CREATED}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.time_created, TIMESTAMP)

    def test_time_created_unset(self):
        BUCKET = object()
        blob = self._make_one('blob-name', bucket=BUCKET)
        self.assertIsNone(blob.time_created)

    def test_updated(self):
        import datetime
        from google.cloud._helpers import _RFC3339_MICROS
        from google.cloud._helpers import UTC

        BLOB_NAME = 'blob-name'
        bucket = _Bucket()
        TIMESTAMP = datetime.datetime(2014, 11, 5, 20, 34, 37, tzinfo=UTC)
        UPDATED = TIMESTAMP.strftime(_RFC3339_MICROS)
        properties = {'updated': UPDATED}
        blob = self._make_one(BLOB_NAME, bucket=bucket, properties=properties)
        self.assertEqual(blob.updated, TIMESTAMP)

    def test_updated_unset(self):
        BUCKET = object()
        blob = self._make_one('blob-name', bucket=BUCKET)
        self.assertIsNone(blob.updated)


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
        from google.cloud.exceptions import NotFound

        info, content = self._respond(**kw)
        if info.get('status') == NOT_FOUND:
            raise NotFound(info)
        return content

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

    def __init__(self, client=None, name='name'):
        if client is None:
            connection = _Connection()
            client = _Client(connection)
        self.client = client
        self._blobs = {}
        self._copied = []
        self._deleted = []
        self.name = name
        self.path = '/b/' + name

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
        self._base_connection = connection

    @property
    def _connection(self):
        return self._base_connection


class _Stream(object):
    _closed = False

    def __init__(self, to_read=b''):
        import io

        self._written = []
        self._to_read = io.BytesIO(to_read)

    def seek(self, offset, whence=0):
        self._to_read.seek(offset, whence)

    def read(self, size):
        return self._to_read.read(size)

    def tell(self):
        return self._to_read.tell()

    def close(self):
        self._closed = True
