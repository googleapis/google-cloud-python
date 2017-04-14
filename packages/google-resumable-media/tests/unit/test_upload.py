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

import mock
import pytest

import gooresmed.upload as upload_mod


EXAMPLE_URL = (
    'https://www.googleapis.com/upload/storage/v1/b/{BUCKET}/o?'
    'uploadType=media&name={OBJECT}')


class Test_UploadBase(object):

    def test_constructor(self):
        upload = upload_mod._UploadBase(EXAMPLE_URL)
        assert upload.upload_url == EXAMPLE_URL
        assert not upload._finished

    def test_finished_property(self):
        upload = upload_mod._UploadBase(EXAMPLE_URL)
        # Default value of @property.
        assert not upload.finished

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            upload.finished = False

        # Set it privately and then check the @property.
        upload._finished = True
        assert upload.finished


class TestSimpleUpload(object):

    def test__prepare_request_already_finished(self):
        upload = upload_mod.SimpleUpload(EXAMPLE_URL)
        upload._finished = True
        with pytest.raises(ValueError):
            upload._prepare_request(None)

    def test__prepare_request(self):
        upload = upload_mod.SimpleUpload(EXAMPLE_URL)
        content_type = 'image/jpeg'
        headers = upload._prepare_request(content_type)
        assert headers == {'content-type': 'image/jpeg'}

    def test__process_response(self):
        upload = upload_mod.SimpleUpload(EXAMPLE_URL)
        # Make sure **not finished** before.
        assert not upload.finished
        ret_val = upload._process_response()
        assert ret_val is None
        # Make sure **finished** after.
        assert upload.finished

    def test_transmit(self):
        data = b'I have got a lovely bunch of coconuts.'
        content_type = 'text/plain'
        upload = upload_mod.SimpleUpload(EXAMPLE_URL)

        transport = mock.Mock(spec=['post'])
        assert not upload.finished
        ret_val = upload.transmit(transport, data, content_type)
        assert ret_val is transport.post.return_value
        upload_headers = {'content-type': content_type}
        transport.post.assert_called_once_with(
            EXAMPLE_URL, data=data, headers=upload_headers)
        assert upload.finished
