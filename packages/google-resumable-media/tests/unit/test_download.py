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

import gooresmed.download as download_mod


EXAMPLE_URL = (
    'https://www.googleapis.com/download/storage/v1/b/'
    '{BUCKET}/o/{OBJECT}?alt=media')


def test_add_bytes_range_do_nothing():
    headers = {}
    ret_val = download_mod._add_bytes_range(None, None, headers)
    assert ret_val is None
    assert headers == {}


def test_add_bytes_range_both_vals():
    headers = {}
    ret_val = download_mod._add_bytes_range(17, 1997, headers)
    assert ret_val is None
    assert headers == {'Range': 'bytes=17-1997'}


def test_add_bytes_range_end_only():
    headers = {}
    ret_val = download_mod._add_bytes_range(None, 909, headers)
    assert ret_val is None
    assert headers == {'Range': 'bytes=0-909'}


def test_add_bytes_range_start_only():
    headers = {}
    ret_val = download_mod._add_bytes_range(3735928559, None, headers)
    assert ret_val is None
    assert headers == {'Range': 'bytes=3735928559-'}


def test_add_bytes_range_start_as_offset():
    headers = {}
    ret_val = download_mod._add_bytes_range(-123454321, None, headers)
    assert ret_val is None
    assert headers == {'Range': 'bytes=-123454321'}


def test_constructor_defaults():
    download = download_mod.Download(EXAMPLE_URL)
    assert download.media_url == EXAMPLE_URL
    assert download.start is None
    assert download.end is None
    assert not download._finished
    assert download._headers == {}


def test_constructor_explicit():
    start = 11
    end = 10001
    download = download_mod.Download(EXAMPLE_URL, start=start, end=end)
    assert download.media_url == EXAMPLE_URL
    assert download.start == start
    assert download.end == end
    assert not download._finished
    range_bytes = 'bytes={:d}-{:d}'.format(start, end)
    assert download._headers == {'Range': range_bytes}


def test_finished_property():
    download = download_mod.Download(EXAMPLE_URL)
    # Default value of @property.
    assert not download.finished

    # Make sure we cannot set it on public @property.
    with pytest.raises(AttributeError):
        download.finished = False

    # Set it privately and then check the @property.
    download._finished = True
    assert download.finished


def test_consume_already_finished():
    download = download_mod.Download(EXAMPLE_URL)
    download._finished = True
    with pytest.raises(ValueError):
        download.consume(None)


def test_consume():
    download = download_mod.Download(EXAMPLE_URL, end=65536)
    transport = mock.Mock(spec=['get'])

    assert not download.finished
    ret_val = download.consume(transport)
    assert ret_val is transport.get.return_value
    transport.get.assert_called_once_with(
        EXAMPLE_URL, headers=download._headers)
    assert download.finished
