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
from six.moves import http_client

from google.resumable_media import _upload
from google.resumable_media import exceptions


SIMPLE_URL = (
    u'https://www.googleapis.com/upload/storage/v1/b/{BUCKET}/o?'
    u'uploadType=media&name={OBJECT}')


class Test_UploadBase(object):

    def test_constructor_defaults(self):
        upload = _upload._UploadBase(SIMPLE_URL)
        assert upload.upload_url == SIMPLE_URL
        assert upload._headers == {}
        assert not upload._finished

    def test_constructor_explicit(self):
        headers = {u'spin': u'doctors'}
        upload = _upload._UploadBase(SIMPLE_URL, headers=headers)
        assert upload.upload_url == SIMPLE_URL
        assert upload._headers is headers
        assert not upload._finished

    def test_finished_property(self):
        upload = _upload._UploadBase(SIMPLE_URL)
        # Default value of @property.
        assert not upload.finished

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            upload.finished = False

        # Set it privately and then check the @property.
        upload._finished = True
        assert upload.finished

    def test__process_response_bad_status(self):
        upload = _upload._UploadBase(SIMPLE_URL)
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
        upload = _upload._UploadBase(SIMPLE_URL)
        # Make sure **not finished** before.
        assert not upload.finished
        response = _make_response()
        ret_val = upload._process_response(response)
        assert ret_val is None
        # Make sure **finished** after.
        assert upload.finished


def _make_response(status_code=http_client.OK):
    return mock.Mock(status_code=status_code, spec=[u'status_code'])
