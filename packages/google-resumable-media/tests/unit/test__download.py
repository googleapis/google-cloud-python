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

from google.resumable_media import _download


EXAMPLE_URL = (
    u'https://www.googleapis.com/download/storage/v1/b/'
    u'{BUCKET}/o/{OBJECT}?alt=media')


class Test_DownloadBase(object):

    def test_constructor_defaults(self):
        download = _download._DownloadBase(EXAMPLE_URL)
        assert download.media_url == EXAMPLE_URL
        assert download.start is None
        assert download.end is None
        assert download._headers == {}
        assert not download._finished

    def test_constructor_explicit(self):
        start = 11
        end = 10001
        headers = {u'foof': u'barf'}
        download = _download._DownloadBase(
            EXAMPLE_URL, start=start, end=end, headers=headers)
        assert download.media_url == EXAMPLE_URL
        assert download.start == start
        assert download.end == end
        assert download._headers is headers
        assert not download._finished

    def test_finished_property(self):
        download = _download._DownloadBase(EXAMPLE_URL)
        # Default value of @property.
        assert not download.finished

        # Make sure we cannot set it on public @property.
        with pytest.raises(AttributeError):
            download.finished = False

        # Set it privately and then check the @property.
        download._finished = True
        assert download.finished
