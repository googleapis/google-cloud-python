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

    def test__prepare_request_already_finished(self):
        upload = upload_mod._UploadBase(SIMPLE_URL)
        upload._finished = True
        with pytest.raises(ValueError):
            upload._prepare_request(None)

    def test__prepare_request(self):
        upload = upload_mod._UploadBase(SIMPLE_URL)
        content_type = u'image/jpeg'
        headers = upload._prepare_request(content_type)
        assert headers == {u'content-type': content_type}

    def test__process_response(self):
        upload = upload_mod._UploadBase(SIMPLE_URL)
        # Make sure **not finished** before.
        assert not upload.finished
        ret_val = upload._process_response()
        assert ret_val is None
        # Make sure **finished** after.
        assert upload.finished


class TestSimpleUpload(object):

    def test_transmit(self):
        data = b'I have got a lovely bunch of coconuts.'
        content_type = u'text/plain'
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
            upload._prepare_request(b'Hi', {}, u'text/plain')

    def test__prepare_request_non_bytes_data(self):
        data = u'Nope not bytes.'
        upload = upload_mod.MultipartUpload(MULTIPART_URL)
        with pytest.raises(TypeError):
            upload._prepare_request(data, {}, u'text/plain')

    @mock.patch(u'gooresmed.upload._get_boundary', return_value=b'==3==')
    def test__prepare_request(self, mock_get_boundary):
        upload = upload_mod.MultipartUpload(MULTIPART_URL)
        data = b'Hi'
        metadata = {u'Some': u'Stuff'}
        content_type = u'text/plain'
        payload, headers = upload._prepare_request(
            data, metadata, content_type)

        expected_payload = (
            b'--==3==\r\n'
            b'content-type: application/json; charset=UTF-8\r\n'
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
        content_type = u'text/plain'
        upload = upload_mod.MultipartUpload(MULTIPART_URL)

        transport = mock.Mock(spec=[u'post'])
        assert not upload.finished
        ret_val = upload.transmit(transport, data, metadata, content_type)
        assert ret_val is transport.post.return_value
        expected_payload = (
            b'--==4==\r\n' +
            b'content-type: application/json; charset=UTF-8\r\n' +
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
            b'--==1==\r\n'
            b'content-type: application/json; charset=UTF-8\r\n'
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
        content_type = u'text/plain'
        payload, multipart_boundary = upload_mod._construct_multipart_request(
            data, metadata, content_type)

        assert multipart_boundary == mock_get_boundary.return_value
        expected_payload = (
            b'--==2==\r\n'
            b'content-type: application/json; charset=UTF-8\r\n'
            b'\r\n'
            b'{"name": "snowman.txt"}\r\n'
            b'--==2==\r\n'
            b'content-type: text/plain\r\n'
            b'\r\n'
            b'\xe2\x98\x83\r\n'
            b'--==2==--')
        assert payload == expected_payload
        mock_get_boundary.assert_called_once_with()
