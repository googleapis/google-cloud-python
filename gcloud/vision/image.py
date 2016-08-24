# Copyright 2016 Google Inc. All rights reserved.
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

from base64 import b64encode


class Image(object):
    """Image representation containing either the source or content of the
    image that will get annotated.

    :type image_source: str
    :param image_source: A string which can be a URL, a Google Cloud Storage
                         path, or a byte stream/string of the image.

    See:
    https://cloud.google.com/vision/reference/rest/v1/images/annotate#Image
    """

    def __init__(self, image_source, client):
        """Initialize Image class

        :type image_source: str
        :param image_source: String or Bytes

        :type client: :class:`Client`
        :param client: Instance of Vision client.
        """

        self.client = client
        self._content = b64encode(image_source)

    def as_dict(self):
        """Generate dictionary structure for request"""
        return {
            'content': self.content
        }

    @property
    def content(self):
        """Base64 encoded image content"""
        return self._content
