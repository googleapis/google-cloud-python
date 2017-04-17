# Copyright 2017 Google Inc.
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
import json
import sys

import mock
import pytest

import gooresmed.upload as upload_mod


SIMPLE_URL = (
    u'https://www.googleapis.com/upload/storage/v1/b/{BUCKET}/o?'
    u'uploadType=media&name={OBJECT}')
MULTIPART_URL = (
    u'https://www.googleapis.com/upload/storage/v1/b/{BUCKET}/o?'
    u'uploadType=multipart')
RESUMABLE_URL = (
    u'https://www.googleapis.com/upload/storage/v1/b/{BUCKET}/o?'
    u'uploadType=resumable')
ONE_MB = 1024 * 1024
BASIC_CONTENT = u'text/plain'
JSON_TYPE = u'application/json; charset=UTF-8'
JSON_TYPE_LINE = b'content-type: application/json; charset=UTF-8\r\n'


class Test_UploadBase(object):

    def test_constructor(self):
        upload = upload_mod._UploadBase(SIMPLE_URL)
        assert upload.upload_url == SIMPLE_URL
        assert not upload._finished

    def test_finished_property(self):
        upload = upload_mod._UploadBase(SIMPLE_URL)
        # Default value of @property.
        assert not upload.finished

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            upload.finished = False

        # Set it privately and then check the @property.
        upload._finished = True
        assert upload.finished

    def test__process_response(self):
        upload = upload_mod._UploadBase(SIMPLE_URL)
        # Make sure **not finished** before.
        assert not upload.finished
        ret_val = upload._process_response()
        assert ret_val is None
        # Make sure **finished** after.
        assert upload.finished


class TestSimpleUpload(object):

    def test__prepare_request_already_finished(self):
        upload = upload_mod.SimpleUpload(SIMPLE_URL)
        upload._finished = True
        with pytest.raises(ValueError):
            upload._prepare_request(None)

    def test__prepare_request(self):
        upload = upload_mod.SimpleUpload(SIMPLE_URL)
        content_type = u'image/jpeg'
        headers = upload._prepare_request(content_type)
        assert headers == {u'content-type': content_type}

    def test_transmit(self):
        data = b'I have got a lovely bunch of coconuts.'
        content_type = BASIC_CONTENT
        upload = upload_mod.SimpleUpload(SIMPLE_URL)

        transport = mock.Mock(spec=[u'post'])
        assert not upload.finished
        ret_val = upload.transmit(transport, data, content_type)
        assert ret_val is transport.post.return_value
        upload_headers = {u'content-type': content_type}
        transport.post.assert_called_once_with(
            SIMPLE_URL, data=data, headers=upload_headers)
        assert upload.finished


class TestMultipartUpload(object):

    def test__prepare_request_already_finished(self):
        upload = upload_mod.MultipartUpload(MULTIPART_URL)
        upload._finished = True
        with pytest.raises(ValueError):
            upload._prepare_request(b'Hi', {}, BASIC_CONTENT)

    def test__prepare_request_non_bytes_data(self):
        data = u'Nope not bytes.'
        upload = upload_mod.MultipartUpload(MULTIPART_URL)
        with pytest.raises(TypeError):
            upload._prepare_request(data, {}, BASIC_CONTENT)

    @mock.patch(u'gooresmed.upload._get_boundary', return_value=b'==3==')
    def test__prepare_request(self, mock_get_boundary):
        upload = upload_mod.MultipartUpload(MULTIPART_URL)
        data = b'Hi'
        metadata = {u'Some': u'Stuff'}
        content_type = BASIC_CONTENT
        payload, headers = upload._prepare_request(
            data, metadata, content_type)

        expected_payload = (
            b'--==3==\r\n' +
            JSON_TYPE_LINE +
            b'\r\n'
            b'{"Some": "Stuff"}\r\n'
            b'--==3==\r\n'
            b'content-type: text/plain\r\n'
            b'\r\n'
            b'Hi\r\n'
            b'--==3==--')
        assert payload == expected_payload
        multipart_type = b'multipart/related; boundary="==3=="'
        assert headers == {u'content-type': multipart_type}
        mock_get_boundary.assert_called_once_with()

    @mock.patch(u'gooresmed.upload._get_boundary', return_value=b'==4==')
    def test_transmit(self, mock_get_boundary):
        data = b'Mock data here and there.'
        metadata = {u'Hey': u'You', u'Guys': u'90909'}
        content_type = BASIC_CONTENT
        upload = upload_mod.MultipartUpload(MULTIPART_URL)

        transport = mock.Mock(spec=[u'post'])
        assert not upload.finished
        ret_val = upload.transmit(transport, data, metadata, content_type)
        assert ret_val is transport.post.return_value
        expected_payload = (
            b'--==4==\r\n' +
            JSON_TYPE_LINE +
            b'\r\n' +
            json.dumps(metadata).encode(u'utf-8') + b'\r\n' +
            b'--==4==\r\n'
            b'content-type: text/plain\r\n'
            b'\r\n'
            b'Mock data here and there.\r\n'
            b'--==4==--')
        multipart_type = b'multipart/related; boundary="==4=="'
        upload_headers = {u'content-type': multipart_type}
        transport.post.assert_called_once_with(
            MULTIPART_URL, data=expected_payload, headers=upload_headers)
        assert upload.finished
        mock_get_boundary.assert_called_once_with()


class TestResumableUpload(object):

    def test_constructor(self):
        chunk_size = ONE_MB
        upload = upload_mod.ResumableUpload(RESUMABLE_URL, chunk_size)
        assert upload.upload_url == RESUMABLE_URL
        assert not upload._finished
        assert upload._chunk_size == chunk_size
        assert upload._stream is None
        assert upload._total_bytes is None
        assert upload._upload_id is None

    def test_constructor_bad_chunk_size(self):
        with pytest.raises(ValueError):
            upload_mod.ResumableUpload(RESUMABLE_URL, 1)

    def test_chunk_size_property(self):
        upload = upload_mod.ResumableUpload(RESUMABLE_URL, ONE_MB)
        # Default value of @property.
        assert upload.chunk_size == ONE_MB

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            upload.chunk_size = 17

        # Set it privately and then check the @property.
        new_size = 102
        upload._chunk_size = new_size
        assert upload.chunk_size == new_size

    def test_upload_id_property(self):
        upload = upload_mod.ResumableUpload(RESUMABLE_URL, ONE_MB)
        # Default value of @property.
        assert upload.upload_id is None

        # Make sure we cannot set it on public @property.
        new_id = u'not-none'
        with pytest.raises(AttributeError):
            upload.upload_id = new_id

        # Set it privately and then check the @property.
        upload._upload_id = new_id
        assert upload.upload_id == new_id

    def test__prepare_initiate_request(self):
        data = b'some really big big data.'
        stream = io.BytesIO(data)
        metadata = {u'name': u'big-data-file.txt'}

        upload = upload_mod.ResumableUpload(RESUMABLE_URL, ONE_MB)
        payload, headers = upload._prepare_initiate_request(
            stream, metadata, BASIC_CONTENT)
        assert payload == b'{"name": "big-data-file.txt"}'
        expected_headers = {
            u'content-type': JSON_TYPE,
            u'x-upload-content-length': u'{:d}'.format(len(data)),
            u'x-upload-content-type': BASIC_CONTENT,
        }
        assert headers == expected_headers
        # Make sure the stream is still at the beginning.
        assert stream.tell() == 0

    def test__prepare_initiate_request_already_initiated(self):
        upload = upload_mod.ResumableUpload(RESUMABLE_URL, ONE_MB)
        # Fake that the upload has been started.
        upload._upload_id = u'definitely-started'

        with pytest.raises(ValueError):
            upload._prepare_initiate_request(io.BytesIO(), {}, BASIC_CONTENT)

    def test__prepare_initiate_request_bad_stream_position(self):
        upload = upload_mod.ResumableUpload(RESUMABLE_URL, ONE_MB)

        stream = io.BytesIO(b'data')
        stream.seek(1)
        with pytest.raises(ValueError):
            upload._prepare_initiate_request(stream, {}, BASIC_CONTENT)

        # Also test a bad object (i.e. non-stream)
        with pytest.raises(AttributeError):
            upload._prepare_initiate_request(None, {}, BASIC_CONTENT)

    def test__process_initiate_response_bad_response(self):
        upload = upload_mod.ResumableUpload(RESUMABLE_URL, ONE_MB)
        # First try with no location header missing.
        with pytest.raises(KeyError):
            upload._process_initiate_response({})

        # Then try with a location header that doesn't have upload_id.
        headers = {u'location': u'http://test.invalid?foo=bar&baz=quux'}
        with pytest.raises(KeyError):
            upload._process_initiate_response(headers)

        # Then try with a location header that has too many upload_id.
        headers = {u'location': u'http://test.invalid?upload_id=1&upload_id=2'}
        with pytest.raises(ValueError):
            upload._process_initiate_response(headers)

    def test__process_initiate_response(self):
        upload = upload_mod.ResumableUpload(RESUMABLE_URL, ONE_MB)

        upload_id = u'kmfeij3234'
        headers = {u'location': u'http://test.invalid?upload_id=' + upload_id}
        # Check upload_id before.
        assert upload._upload_id is None
        # Process the actual headers.
        ret_val = upload._process_initiate_response(headers)
        assert ret_val is None
        # Check upload_id after.
        assert upload._upload_id == upload_id

    def test_initiate(self):
        upload = upload_mod.ResumableUpload(RESUMABLE_URL, ONE_MB)
        data = b'Knock knock who is there'
        stream = io.BytesIO(data)
        upload_id = u'AACODBBBxuw9u3AA'
        metadata = {u'name': u'got-jokes.txt'}

        transport = mock.Mock(spec=[u'post'])
        response_headers = {
            u'location': u'http://test.invalid?upload_id=' + upload_id,
        }
        post_response = mock.Mock(headers=response_headers, spec=[u'headers'])
        transport.post.return_value = post_response
        # Check upload_id before.
        assert upload._upload_id is None
        # Make request and check the return value (against the mock).
        response = upload.initiate(transport, stream, metadata, BASIC_CONTENT)
        assert response is transport.post.return_value
        # Check upload_id after.
        assert upload._upload_id == upload_id
        # Make sure the mock was called as expected.
        json_bytes = b'{"name": "got-jokes.txt"}'
        expected_headers = {
            u'content-type': JSON_TYPE,
            u'x-upload-content-type': BASIC_CONTENT,
            u'x-upload-content-length': u'{:d}'.format(len(data)),
        }
        transport.post.assert_called_once_with(
            RESUMABLE_URL, data=json_bytes, headers=expected_headers)


@mock.patch(u'random.randrange', return_value=1234567890123456789)
def test__get_boundary(mock_rand):
    result = upload_mod._get_boundary()
    assert result == b'===============1234567890123456789=='
    mock_rand.assert_called_once_with(sys.maxsize)


class Test__construct_multipart_request(object):

    @mock.patch(u'gooresmed.upload._get_boundary', return_value=b'==1==')
    def test_binary(self, mock_get_boundary):
        data = b'By nary day tuh'
        metadata = {u'name': u'hi-file.bin'}
        content_type = u'application/octet-stream'
        payload, multipart_boundary = upload_mod._construct_multipart_request(
            data, metadata, content_type)

        assert multipart_boundary == mock_get_boundary.return_value
        expected_payload = (
            b'--==1==\r\n' +
            JSON_TYPE_LINE +
            b'\r\n'
            b'{"name": "hi-file.bin"}\r\n'
            b'--==1==\r\n'
            b'content-type: application/octet-stream\r\n'
            b'\r\n'
            b'By nary day tuh\r\n'
            b'--==1==--')
        assert payload == expected_payload
        mock_get_boundary.assert_called_once_with()

    @mock.patch(u'gooresmed.upload._get_boundary', return_value=b'==2==')
    def test_unicode(self, mock_get_boundary):
        data_unicode = u'\N{snowman}'
        # _construct_multipart_request ASSUMES callers pass bytes.
        data = data_unicode.encode(u'utf-8')
        metadata = {u'name': u'snowman.txt'}
        content_type = BASIC_CONTENT
        payload, multipart_boundary = upload_mod._construct_multipart_request(
            data, metadata, content_type)

        assert multipart_boundary == mock_get_boundary.return_value
        expected_payload = (
            b'--==2==\r\n' +
            JSON_TYPE_LINE +
            b'\r\n'
            b'{"name": "snowman.txt"}\r\n'
            b'--==2==\r\n'
            b'content-type: text/plain\r\n'
            b'\r\n'
            b'\xe2\x98\x83\r\n'
            b'--==2==--')
        assert payload == expected_payload
        mock_get_boundary.assert_called_once_with()


def test__get_total_bytes():
    data = b'some data'
    stream = io.BytesIO(data)
    # Check position before function call.
    assert stream.tell() == 0
    assert upload_mod._get_total_bytes(stream) == len(data)
    # Check position after function call.
    assert stream.tell() == 0

    # Make sure this works just as well when not at beginning.
    curr_pos = 3
    stream.seek(curr_pos)
    assert upload_mod._get_total_bytes(stream) == len(data)
    # Check position after function call.
    assert stream.tell() == curr_pos
