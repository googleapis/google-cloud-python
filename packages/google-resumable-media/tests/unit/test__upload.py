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
import sys

import mock
import pytest
from six.moves import http_client

from google.resumable_media import _upload
from google.resumable_media import exceptions


SIMPLE_URL = (
    u'https://www.googleapis.com/upload/storage/v1/b/{BUCKET}/o?'
    u'uploadType=media&name={OBJECT}')
BASIC_CONTENT = u'text/plain'
JSON_TYPE_LINE = b'content-type: application/json; charset=UTF-8\r\n'


class TestUploadBase(object):

    def test_constructor_defaults(self):
        upload = _upload.UploadBase(SIMPLE_URL)
        assert upload.upload_url == SIMPLE_URL
        assert upload._headers == {}
        assert not upload._finished

    def test_constructor_explicit(self):
        headers = {u'spin': u'doctors'}
        upload = _upload.UploadBase(SIMPLE_URL, headers=headers)
        assert upload.upload_url == SIMPLE_URL
        assert upload._headers is headers
        assert not upload._finished

    def test_finished_property(self):
        upload = _upload.UploadBase(SIMPLE_URL)
        # Default value of @property.
        assert not upload.finished

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            upload.finished = False

        # Set it privately and then check the @property.
        upload._finished = True
        assert upload.finished

    def test__process_response_bad_status(self):
        upload = _upload.UploadBase(SIMPLE_URL)
        upload._get_status_code = _get_status_code
        # Make sure **not finished** before.
        assert not upload.finished
        status_code = http_client.SERVICE_UNAVAILABLE
        response = _make_response(status_code=status_code)
        with pytest.raises(exceptions.InvalidResponse) as exc_info:
            upload._process_response(response)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 4
        assert error.args[1] == status_code
        assert error.args[3] == http_client.OK
        # Make sure **finished** after (even in failure).
        assert upload.finished

    def test__process_response(self):
        upload = _upload.UploadBase(SIMPLE_URL)
        upload._get_status_code = _get_status_code
        # Make sure **not finished** before.
        assert not upload.finished
        response = _make_response()
        ret_val = upload._process_response(response)
        assert ret_val is None
        # Make sure **finished** after.
        assert upload.finished

    def test__get_status_code(self):
        with pytest.raises(NotImplementedError) as exc_info:
            _upload.UploadBase._get_status_code(None)

        exc_info.match(u'virtual')


class TestSimpleUpload(object):

    def test__prepare_request_already_finished(self):
        upload = _upload.SimpleUpload(SIMPLE_URL)
        upload._finished = True
        with pytest.raises(ValueError):
            upload._prepare_request(None)

    def test__prepare_request(self):
        upload = _upload.SimpleUpload(SIMPLE_URL)
        content_type = u'image/jpeg'
        headers = upload._prepare_request(content_type)
        assert headers == {u'content-type': content_type}

    def test__prepare_request_with_headers(self):
        headers = {u'x-goog-cheetos': u'spicy'}
        upload = _upload.SimpleUpload(SIMPLE_URL, headers=headers)
        content_type = u'image/jpeg'
        new_headers = upload._prepare_request(content_type)
        assert new_headers is headers
        expected = {u'content-type': content_type, u'x-goog-cheetos': u'spicy'}
        assert headers == expected

    def test_transmit(self):
        upload = _upload.SimpleUpload(SIMPLE_URL)
        with pytest.raises(NotImplementedError) as exc_info:
            upload.transmit(None, None, None)

        exc_info.match(u'virtual')


@mock.patch(u'random.randrange', return_value=1234567890123456789)
def test_get_boundary(mock_rand):
    result = _upload.get_boundary()
    assert result == b'===============1234567890123456789=='
    mock_rand.assert_called_once_with(sys.maxsize)


class Test_construct_multipart_request(object):

    @mock.patch(u'google.resumable_media._upload.get_boundary',
                return_value=b'==1==')
    def test_binary(self, mock_get_boundary):
        data = b'By nary day tuh'
        metadata = {u'name': u'hi-file.bin'}
        content_type = u'application/octet-stream'
        payload, multipart_boundary = _upload.construct_multipart_request(
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

    @mock.patch(u'google.resumable_media._upload.get_boundary',
                return_value=b'==2==')
    def test_unicode(self, mock_get_boundary):
        data_unicode = u'\N{snowman}'
        # construct_multipart_request( ASSUMES callers pass bytes.
        data = data_unicode.encode(u'utf-8')
        metadata = {u'name': u'snowman.txt'}
        content_type = BASIC_CONTENT
        payload, multipart_boundary = _upload.construct_multipart_request(
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


def test_get_total_bytes():
    data = b'some data'
    stream = io.BytesIO(data)
    # Check position before function call.
    assert stream.tell() == 0
    assert _upload.get_total_bytes(stream) == len(data)
    # Check position after function call.
    assert stream.tell() == 0

    # Make sure this works just as well when not at beginning.
    curr_pos = 3
    stream.seek(curr_pos)
    assert _upload.get_total_bytes(stream) == len(data)
    # Check position after function call.
    assert stream.tell() == curr_pos


class Test_get_next_chunk(object):

    def test_exhausted(self):
        data = b'the end'
        stream = io.BytesIO(data)
        stream.seek(len(data))
        with pytest.raises(ValueError):
            _upload.get_next_chunk(stream, 1)

    def test_success(self):
        stream = io.BytesIO(b'0123456789')
        chunk_size = 3
        # Splits into 4 chunks: 012, 345, 678, 9
        result0 = _upload.get_next_chunk(stream, chunk_size)
        result1 = _upload.get_next_chunk(stream, chunk_size)
        result2 = _upload.get_next_chunk(stream, chunk_size)
        result3 = _upload.get_next_chunk(stream, chunk_size)
        assert result0 == (0, 2, b'012')
        assert result1 == (3, 5, b'345')
        assert result2 == (6, 8, b'678')
        assert result3 == (9, 9, b'9')
        assert stream.tell() == 10


def _make_response(status_code=http_client.OK):
    return mock.Mock(status_code=status_code, spec=[u'status_code'])


def _get_status_code(response):
    return response.status_code
