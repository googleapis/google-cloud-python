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

from google.resumable_media import _download
from google.resumable_media import exceptions


EXAMPLE_URL = (
    u'https://www.googleapis.com/download/storage/v1/b/'
    u'{BUCKET}/o/{OBJECT}?alt=media')


class TestDownloadBase(object):

    def test_constructor_defaults(self):
        download = _download.DownloadBase(EXAMPLE_URL)
        assert download.media_url == EXAMPLE_URL
        assert download.start is None
        assert download.end is None
        assert download._headers == {}
        assert not download._finished

    def test_constructor_explicit(self):
        start = 11
        end = 10001
        headers = {u'foof': u'barf'}
        download = _download.DownloadBase(
            EXAMPLE_URL, start=start, end=end, headers=headers)
        assert download.media_url == EXAMPLE_URL
        assert download.start == start
        assert download.end == end
        assert download._headers is headers
        assert not download._finished

    def test_finished_property(self):
        download = _download.DownloadBase(EXAMPLE_URL)
        # Default value of @property.
        assert not download.finished

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            download.finished = False

        # Set it privately and then check the @property.
        download._finished = True
        assert download.finished

    def test__get_status_code(self):
        with pytest.raises(NotImplementedError) as exc_info:
            _download.DownloadBase._get_status_code(None)

        exc_info.match(u'virtual')


class TestDownload(object):

    def test__prepare_request_already_finished(self):
        download = _download.Download(EXAMPLE_URL)
        download._finished = True
        with pytest.raises(ValueError):
            download._prepare_request()

    def test__prepare_request(self):
        download1 = _download.Download(EXAMPLE_URL)
        headers1 = download1._prepare_request()
        assert headers1 == {}

        download2 = _download.Download(EXAMPLE_URL, start=53)
        headers2 = download2._prepare_request()
        assert headers2 == {u'range': u'bytes=53-'}

    def test__prepare_request_with_headers(self):
        headers = {u'spoonge': u'borb'}
        download = _download.Download(
            EXAMPLE_URL, start=11, end=111, headers=headers)
        new_headers = download._prepare_request()
        assert new_headers is headers
        assert headers == {u'range': u'bytes=11-111', u'spoonge': u'borb'}

    def test__process_response(self):
        download = _download.Download(EXAMPLE_URL)
        download._get_status_code = _get_status_code
        # Make sure **not finished** before.
        assert not download.finished
        response = mock.Mock(
            status_code=int(http_client.OK), spec=[u'status_code'])
        ret_val = download._process_response(response)
        assert ret_val is None
        # Make sure **finished** after.
        assert download.finished

    def test__process_response_bad_status(self):
        download = _download.Download(EXAMPLE_URL)
        download._get_status_code = _get_status_code
        # Make sure **not finished** before.
        assert not download.finished
        response = mock.Mock(
            status_code=int(http_client.NOT_FOUND), spec=[u'status_code'])
        with pytest.raises(exceptions.InvalidResponse) as exc_info:
            download._process_response(response)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 5
        assert error.args[1] == response.status_code
        assert error.args[3] == http_client.OK
        assert error.args[4] == http_client.PARTIAL_CONTENT
        # Make sure **finished** even after a failure.
        assert download.finished

    def test_consume(self):
        download = _download.Download(EXAMPLE_URL)
        with pytest.raises(NotImplementedError) as exc_info:
            download.consume(None)

        exc_info.match(u'virtual')


class Test__add_bytes_range(object):

    def test_do_nothing(self):
        headers = {}
        ret_val = _download.add_bytes_range(None, None, headers)
        assert ret_val is None
        assert headers == {}

    def test_both_vals(self):
        headers = {}
        ret_val = _download.add_bytes_range(17, 1997, headers)
        assert ret_val is None
        assert headers == {u'range': u'bytes=17-1997'}

    def test_end_only(self):
        headers = {}
        ret_val = _download.add_bytes_range(None, 909, headers)
        assert ret_val is None
        assert headers == {u'range': u'bytes=0-909'}

    def test_start_only(self):
        headers = {}
        ret_val = _download.add_bytes_range(3735928559, None, headers)
        assert ret_val is None
        assert headers == {u'range': u'bytes=3735928559-'}

    def test_start_as_offset(self):
        headers = {}
        ret_val = _download.add_bytes_range(-123454321, None, headers)
        assert ret_val is None
        assert headers == {u'range': u'bytes=-123454321'}


class Test_get_range_info(object):

    @staticmethod
    def _make_response(content_range):
        headers = {u'content-range': content_range}
        return mock.Mock(headers=headers, spec=[u'headers'])

    def _success_helper(self, **kwargs):
        content_range = u'Bytes 7-11/42'
        response = self._make_response(content_range)
        start_byte, end_byte, total_bytes = _download.get_range_info(
            response, _get_headers, **kwargs)
        assert start_byte == 7
        assert end_byte == 11
        assert total_bytes == 42

    def test_success(self):
        self._success_helper()

    def test_success_with_callback(self):
        callback = mock.Mock(spec=[])
        self._success_helper(callback=callback)
        callback.assert_not_called()

    def _failure_helper(self, **kwargs):
        content_range = u'nope x-6/y'
        response = self._make_response(content_range)
        with pytest.raises(exceptions.InvalidResponse) as exc_info:
            _download.get_range_info(response, _get_headers, **kwargs)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 3
        assert error.args[1] == content_range

    def test_failure(self):
        self._failure_helper()

    def test_failure_with_callback(self):
        callback = mock.Mock(spec=[])
        self._failure_helper(callback=callback)
        callback.assert_called_once_with()

    def _missing_header_helper(self, **kwargs):
        response = mock.Mock(headers={}, spec=[u'headers'])
        with pytest.raises(exceptions.InvalidResponse) as exc_info:
            _download.get_range_info(response, _get_headers, **kwargs)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 2
        assert error.args[1] == u'content-range'

    def test_missing_header(self):
        self._missing_header_helper()

    def test_missing_header_with_callback(self):
        callback = mock.Mock(spec=[])
        self._missing_header_helper(callback=callback)
        callback.assert_called_once_with()


def _get_status_code(response):
    return response.status_code


def _get_headers(response):
    return response.headers
