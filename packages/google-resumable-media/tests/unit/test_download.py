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


def test_constructor_explicit():
    start = 11
    end = 10001
    download = make_download(EXAMPLE_URL, start=start, end=end)
    assert download.media_url == EXAMPLE_URL
    assert download.start == start
    assert download.end == end
    assert not download.in_progress
    assert not download.finished


def test_consume():
    download = make_download(EXAMPLE_URL)
    with pytest.raises(NotImplementedError):
        download.consume()
