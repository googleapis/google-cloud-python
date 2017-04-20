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

import mock
import pytest
from six.moves import http_client

import gooresmed.download as download_mod
from gooresmed import exceptions


EXAMPLE_URL = (
    u'https://www.googleapis.com/download/storage/v1/b/'
    u'{BUCKET}/o/{OBJECT}?alt=media')


class Test__add_bytes_range(object):

    def test_do_nothing(self):
        headers = {}
        ret_val = download_mod._add_bytes_range(None, None, headers)
        assert ret_val is None
        assert headers == {}

    def test_both_vals(self):
        headers = {}
        ret_val = download_mod._add_bytes_range(17, 1997, headers)
        assert ret_val is None
        assert headers == {u'range': u'bytes=17-1997'}

    def test_end_only(self):
        headers = {}
        ret_val = download_mod._add_bytes_range(None, 909, headers)
        assert ret_val is None
        assert headers == {u'range': u'bytes=0-909'}

    def test_start_only(self):
        headers = {}
        ret_val = download_mod._add_bytes_range(3735928559, None, headers)
        assert ret_val is None
        assert headers == {u'range': u'bytes=3735928559-'}

    def test_start_as_offset(self):
        headers = {}
        ret_val = download_mod._add_bytes_range(-123454321, None, headers)
        assert ret_val is None
        assert headers == {u'range': u'bytes=-123454321'}


class Test_DownloadBase(object):

    def test_constructor_defaults(self):
        download = download_mod._DownloadBase(EXAMPLE_URL)
        assert download.media_url == EXAMPLE_URL
        assert download.start is None
        assert download.end is None
        assert not download._finished

    def test_constructor_explicit(self):
        start = 11
        end = 10001
        download = download_mod._DownloadBase(
            EXAMPLE_URL, start=start, end=end)
        assert download.media_url == EXAMPLE_URL
        assert download.start == start
        assert download.end == end
        assert not download._finished

    def test_finished_property(self):
        download = download_mod._DownloadBase(EXAMPLE_URL)
        # Default value of @property.
        assert not download.finished

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            download.finished = False

        # Set it privately and then check the @property.
        download._finished = True
        assert download.finished


class TestDownload(object):

    def test__prepare_request_already_finished(self):
        download = download_mod.Download(EXAMPLE_URL)
        download._finished = True
        with pytest.raises(ValueError):
            download._prepare_request()

    def test__prepare_request(self):
        download1 = download_mod.Download(EXAMPLE_URL)
        headers1 = download1._prepare_request()
        assert headers1 == {}

        download2 = download_mod.Download(EXAMPLE_URL, start=53)
        headers2 = download2._prepare_request()
        assert headers2 == {u'range': u'bytes=53-'}

    def test__process_response(self):
        download = download_mod.Download(EXAMPLE_URL)
        # Make sure **not finished** before.
        assert not download.finished
        response = mock.Mock(
            status_code=int(http_client.OK), spec=[u'status_code'])
        ret_val = download._process_response(response)
        assert ret_val is None
        # Make sure **finished** after.
        assert download.finished

    def test__process_response_bad_status(self):
        download = download_mod.Download(EXAMPLE_URL)
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
        end = 65536
        download = download_mod.Download(EXAMPLE_URL, end=end)
        transport = mock.Mock(spec=[u'get'])
        transport.get.return_value = mock.Mock(
            status_code=int(http_client.OK), spec=[u'status_code'])

        assert not download.finished
        ret_val = download.consume(transport)
        assert ret_val is transport.get.return_value
        range_bytes = u'bytes={:d}-{:d}'.format(0, end)
        download_headers = {u'range': range_bytes}
        transport.get.assert_called_once_with(
            EXAMPLE_URL, headers=download_headers)
        assert download.finished


class TestChunkedDownload(object):

    def test_constructor_defaults(self):
        chunk_size = 256
        stream = mock.sentinel.stream
        download = download_mod.ChunkedDownload(
            EXAMPLE_URL, chunk_size, stream)
        assert download.media_url == EXAMPLE_URL
        assert download.chunk_size == chunk_size
        assert download.start == 0
        assert download.end is None
        assert not download._finished
        assert download._stream is stream
        assert download._bytes_downloaded == 0
        assert download._total_bytes is None

    def test_constructor_bad_start(self):
        with pytest.raises(ValueError):
            download_mod.ChunkedDownload(EXAMPLE_URL, 256, None, start=-11)

    def test_bytes_downloaded_property(self):
        download = download_mod.ChunkedDownload(EXAMPLE_URL, 256, None)
        # Default value of @property.
        assert download.bytes_downloaded == 0

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            download.bytes_downloaded = 1024

        # Set it privately and then check the @property.
        download._bytes_downloaded = 128
        assert download.bytes_downloaded == 128

    def test_total_bytes_property(self):
        download = download_mod.ChunkedDownload(EXAMPLE_URL, 256, None)
        # Default value of @property.
        assert download.total_bytes is None

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            download.total_bytes = 65536

        # Set it privately and then check the @property.
        download._total_bytes = 8192
        assert download.total_bytes == 8192

    def test__get_byte_range(self):
        chunk_size = 512
        download = download_mod.ChunkedDownload(EXAMPLE_URL, chunk_size, None)
        curr_start, curr_end = download._get_byte_range()
        assert curr_start == 0
        assert curr_end == chunk_size - 1

    def test__get_byte_range_with_end(self):
        chunk_size = 512
        start = 1024
        end = 1151
        download = download_mod.ChunkedDownload(
            EXAMPLE_URL, chunk_size, None, start=start, end=end)
        curr_start, curr_end = download._get_byte_range()
        assert curr_start == start
        assert curr_end == end
        # Make sure this is less than the chunk size.
        actual_size = curr_end - curr_start + 1
        assert actual_size < chunk_size

    def test__get_byte_range_with_total_bytes(self):
        chunk_size = 512
        download = download_mod.ChunkedDownload(EXAMPLE_URL, chunk_size, None)
        total_bytes = 207
        download._total_bytes = total_bytes
        curr_start, curr_end = download._get_byte_range()
        assert curr_start == 0
        assert curr_end == total_bytes - 1
        # Make sure this is less than the chunk size.
        actual_size = curr_end - curr_start + 1
        assert actual_size < chunk_size

    @staticmethod
    def _response_content_range(start_byte, end_byte, total_bytes):
        return u'bytes {:d}-{:d}/{:d}'.format(
            start_byte, end_byte, total_bytes)

    def _response_headers(self, start_byte, end_byte, total_bytes):
        content_length = end_byte - start_byte + 1
        resp_range = self._response_content_range(
            start_byte, end_byte, total_bytes)
        return {
            u'content-length': u'{:d}'.format(content_length),
            u'content-range': resp_range,
        }

    def _mock_response(self, start_byte, end_byte, total_bytes,
                       content=None, status_code=None):
        response_headers = self._response_headers(
            start_byte, end_byte, total_bytes)
        return mock.Mock(
            content=content, headers=response_headers, status_code=status_code,
            spec=[u'content', u'headers', u'status_code'])

    def test__prepare_request_already_finished(self):
        download = download_mod.ChunkedDownload(EXAMPLE_URL, 64, None)
        download._finished = True
        with pytest.raises(ValueError):
            download._prepare_request()

    def test__prepare_request(self):
        chunk_size = 2048
        download1 = download_mod.ChunkedDownload(EXAMPLE_URL, chunk_size, None)
        headers1 = download1._prepare_request()
        assert headers1 == {u'range': u'bytes=0-2047'}

        download2 = download_mod.ChunkedDownload(
            EXAMPLE_URL, chunk_size, None, start=19991)
        download2._total_bytes = 20101
        headers2 = download2._prepare_request()
        assert headers2 == {u'range': u'bytes=19991-20100'}

    def test__process_response(self):
        chunk_size = 333
        stream = io.BytesIO()
        download = download_mod.ChunkedDownload(
            EXAMPLE_URL, chunk_size, stream)
        already = 22
        download._bytes_downloaded = already
        total_bytes = 4444

        # Check internal state before.
        assert not download.finished
        assert download.bytes_downloaded == already
        assert download.total_bytes is None
        # Actually call the method to update.
        data = b'1234xyztL' * 37  # 9 * 37 == 33
        response = self._mock_response(
            already, already + chunk_size - 1, total_bytes, content=data,
            status_code=int(http_client.PARTIAL_CONTENT))
        download._process_response(response)
        # Check internal state after.
        assert not download.finished
        assert download.bytes_downloaded == already + chunk_size
        assert download.total_bytes == total_bytes
        assert stream.getvalue() == data

    def test__process_response_bad_status(self):
        chunk_size = 384
        stream = mock.Mock(spec=[u'write'])
        download = download_mod.ChunkedDownload(
            EXAMPLE_URL, chunk_size, stream)
        total_bytes = 300

        # Check internal state before.
        assert not download.finished
        assert download.bytes_downloaded == 0
        assert download.total_bytes is None
        # Actually call the method to update.
        response = self._mock_response(
            0, total_bytes - 1, total_bytes,
            status_code=int(http_client.NOT_FOUND))
        with pytest.raises(exceptions.InvalidResponse) as exc_info:
            download._process_response(response)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 5
        assert error.args[1] == response.status_code
        assert error.args[3] == http_client.OK
        assert error.args[4] == http_client.PARTIAL_CONTENT
        # Check internal state after.
        assert not download.finished
        assert download.bytes_downloaded == 0
        assert download.total_bytes is None
        stream.write.assert_not_called()

    def test__process_response_body_wrong_length(self):
        chunk_size = 10
        stream = mock.Mock(spec=[u'write'])
        download = download_mod.ChunkedDownload(
            EXAMPLE_URL, chunk_size, stream)
        total_bytes = 100

        # Check internal state before.
        assert not download.finished
        assert download.bytes_downloaded == 0
        assert download.total_bytes is None
        # Actually call the method to update.
        data = b'not 10'
        response = self._mock_response(
            0, chunk_size - 1, total_bytes, content=data,
            status_code=int(http_client.PARTIAL_CONTENT))
        with pytest.raises(exceptions.InvalidResponse) as exc_info:
            download._process_response(response)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 5
        assert error.args[2] == chunk_size
        assert error.args[4] == len(data)
        # Check internal state after.
        assert not download.finished
        assert download.bytes_downloaded == 0
        assert download.total_bytes is None
        stream.write.assert_not_called()

    def test__process_response_when_finished(self):
        chunk_size = 256
        stream = io.BytesIO()
        download = download_mod.ChunkedDownload(
            EXAMPLE_URL, chunk_size, stream)
        total_bytes = 200

        # Check internal state before.
        assert not download.finished
        assert download.bytes_downloaded == 0
        assert download.total_bytes is None
        # Actually call the method to update.
        data = b'abcd' * 50  # 4 * 50 == 200
        response = self._mock_response(
            0, total_bytes - 1, total_bytes, content=data,
            status_code=int(http_client.OK))
        download._process_response(response)
        # Check internal state after.
        assert download.finished
        assert download.bytes_downloaded == total_bytes
        assert total_bytes < chunk_size
        assert download.total_bytes == total_bytes
        assert stream.getvalue() == data

    def test__process_response_when_reaching_end(self):
        chunk_size = 8192
        end = 65000
        stream = io.BytesIO()
        download = download_mod.ChunkedDownload(
            EXAMPLE_URL, chunk_size, stream, end=end)
        download._bytes_downloaded = 7 * chunk_size
        download._total_bytes = 8 * chunk_size

        # Check internal state before.
        assert not download.finished
        assert download.bytes_downloaded == 7 * chunk_size
        assert download.total_bytes == 8 * chunk_size
        # Actually call the method to update.
        expected_size = end - 7 * chunk_size + 1
        data = b'B' * expected_size
        response = self._mock_response(
            7 * chunk_size, end, 8 * chunk_size, content=data,
            status_code=int(http_client.PARTIAL_CONTENT))
        download._process_response(response)
        # Check internal state after.
        assert download.finished
        assert download.bytes_downloaded == end + 1
        assert download.bytes_downloaded < download.total_bytes
        assert download.total_bytes == 8 * chunk_size
        assert stream.getvalue() == data

    def test_consume_next_chunk_already_finished(self):
        download = download_mod.ChunkedDownload(EXAMPLE_URL, 512, None)
        download._finished = True
        with pytest.raises(ValueError):
            download.consume_next_chunk(None)

    def _mock_transport(self, start, chunk_size, total_bytes, content=b''):
        transport = mock.Mock(spec=[u'get'])
        assert len(content) == chunk_size
        transport.get.return_value = self._mock_response(
            start, start + chunk_size - 1, total_bytes,
            content=content, status_code=int(http_client.OK))

        return transport

    def test_consume_next_chunk(self):
        start = 1536
        stream = io.BytesIO()
        data = b'Just one chunk.'
        chunk_size = len(data)
        download = download_mod.ChunkedDownload(
            EXAMPLE_URL, chunk_size, stream, start=start)
        total_bytes = 16384
        transport = self._mock_transport(
            start, chunk_size, total_bytes, content=data)

        # Verify the internal state before consuming a chunk.
        assert not download.finished
        assert download.bytes_downloaded == 0
        assert download.total_bytes is None
        # Actually consume the chunk and check the output.
        ret_val = download.consume_next_chunk(transport)
        assert ret_val is transport.get.return_value
        range_bytes = u'bytes={:d}-{:d}'.format(start, start + chunk_size - 1)
        download_headers = {u'range': range_bytes}
        transport.get.assert_called_once_with(
            EXAMPLE_URL, headers=download_headers)
        assert stream.getvalue() == data
        # Go back and check the internal state after consuming the chunk.
        assert not download.finished
        assert download.bytes_downloaded == chunk_size
        assert download.total_bytes == total_bytes


class Test__get_range_info(object):

    @staticmethod
    def _make_response(content_range):
        headers = {u'content-range': content_range}
        return mock.Mock(headers=headers, spec=[u'headers'])

    def test_success(self):
        content_range = u'Bytes 7-11/42'
        response = self._make_response(content_range)
        start_byte, end_byte, total_bytes = download_mod._get_range_info(
            response)
        assert start_byte == 7
        assert end_byte == 11
        assert total_bytes == 42

    def test_failure(self):
        content_range = u'nope x-6/y'
        response = self._make_response(content_range)
        with pytest.raises(exceptions.InvalidResponse) as exc_info:
            download_mod._get_range_info(response)

        error = exc_info.value
        assert error.response is response
        assert len(error.args) == 3
        assert error.args[1] == content_range
