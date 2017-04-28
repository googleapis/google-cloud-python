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

import google.resumable_media.requests.download as download_mod


EXAMPLE_URL = (
    u'https://www.googleapis.com/download/storage/v1/b/'
    u'{BUCKET}/o/{OBJECT}?alt=media')


class TestDownload(object):

    def _consume_helper(self, end=65536, headers=None):
        download = download_mod.Download(EXAMPLE_URL, end=end, headers=headers)
        transport = mock.Mock(spec=[u'request'])
        transport.request.return_value = mock.Mock(
            status_code=int(http_client.OK), spec=[u'status_code'])

        assert not download.finished
        ret_val = download.consume(transport)
        assert ret_val is transport.request.return_value
        transport.request.assert_called_once_with(
            u'GET', EXAMPLE_URL, data=None, headers=download._headers)
        range_bytes = u'bytes={:d}-{:d}'.format(0, end)
        assert download._headers[u'range'] == range_bytes
        assert download.finished

    def test_consume(self):
        self._consume_helper()

    def test_consume_with_headers(self):
        headers = {}  # Empty headers
        end = 16383
        self._consume_helper(end=end, headers=headers)
        range_bytes = u'bytes={:d}-{:d}'.format(0, end)
        # Make sure the headers have been modified.
        assert headers == {u'range': range_bytes}


class TestChunkedDownload(object):

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

    def test_consume_next_chunk_already_finished(self):
        download = download_mod.ChunkedDownload(EXAMPLE_URL, 512, None)
        download._finished = True
        with pytest.raises(ValueError):
            download.consume_next_chunk(None)

    def _mock_transport(self, start, chunk_size, total_bytes, content=b''):
        transport = mock.Mock(spec=[u'request'])
        assert len(content) == chunk_size
        transport.request.return_value = self._mock_response(
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
        assert ret_val is transport.request.return_value
        range_bytes = u'bytes={:d}-{:d}'.format(start, start + chunk_size - 1)
        download_headers = {u'range': range_bytes}
        transport.request.assert_called_once_with(
            u'GET', EXAMPLE_URL, data=None, headers=download_headers)
        assert stream.getvalue() == data
        # Go back and check the internal state after consuming the chunk.
        assert not download.finished
        assert download.bytes_downloaded == chunk_size
        assert download.total_bytes == total_bytes
