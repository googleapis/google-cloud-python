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

import pytest


EXAMPLE_URL = (
    'https://www.googleapis.com/download/storage/v1/b/'
    '{BUCKET}/o/{OBJECT}?alt=media')


def call__add_bytes_range(*args, **kwargs):
    from gooresmed import download

    return download._add_bytes_range(*args, **kwargs)


def test_add_bytes_range_do_nothing():
    headers = {}
    ret_val = call__add_bytes_range(None, None, headers)
    assert ret_val is None
    assert headers == {}


def test_add_bytes_range_both_vals():
    headers = {}
    ret_val = call__add_bytes_range(17, 1997, headers)
    assert ret_val is None
    assert headers == {'Range': 'bytes=17-1997'}


def test_add_bytes_range_end_only():
    headers = {}
    ret_val = call__add_bytes_range(None, 909, headers)
    assert ret_val is None
    assert headers == {'Range': 'bytes=0-909'}


def test_add_bytes_range_start_only():
    headers = {}
    ret_val = call__add_bytes_range(3735928559, None, headers)
    assert ret_val is None
    assert headers == {'Range': 'bytes=3735928559-'}


def test_add_bytes_range_start_as_offset():
    headers = {}
    ret_val = call__add_bytes_range(-123454321, None, headers)
    assert ret_val is None
    assert headers == {'Range': 'bytes=-123454321'}


def make_download(*args, **kwargs):
    from gooresmed import download

    return download.Download(*args, **kwargs)


def test_constructor_defaults():
    download = make_download(EXAMPLE_URL)
    assert download.media_url == EXAMPLE_URL
    assert download.start is None
    assert download.end is None
    assert not download.in_progress
    assert not download.finished
    assert download._headers == {}


def test_constructor_explicit():
    start = 11
    end = 10001
    download = make_download(EXAMPLE_URL, start=start, end=end)
    assert download.media_url == EXAMPLE_URL
    assert download.start == start
    assert download.end == end
    assert not download.in_progress
    assert not download.finished
    range_bytes = 'bytes={:d}-{:d}'.format(start, end)
    assert download._headers == {'Range': range_bytes}


def test_consume():
    download = make_download(EXAMPLE_URL)
    with pytest.raises(NotImplementedError):
        download.consume()
