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

"""Virtual bases classes for downloading media from Google APIs."""


class _DownloadBase(object):
    """Base class for download helpers.

    Defines core shared behavior across different download types.

    Args:
        media_url (str): The URL containing the media to be downloaded.
        start (int): The first byte in a range to be downloaded.
        end (int): The last byte in a range to be downloaded.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.
    """

    def __init__(self, media_url, start=None, end=None, headers=None):
        self.media_url = media_url
        """str: The URL containing the media to be downloaded."""
        self.start = start
        """Optional[int]: The first byte in a range to be downloaded."""
        self.end = end
        """Optional[int]: The last byte in a range to be downloaded."""
        if headers is None:
            headers = {}
        self._headers = headers
        self._finished = False

    @property
    def finished(self):
        """bool: Flag indicating if the download has completed."""
        return self._finished
