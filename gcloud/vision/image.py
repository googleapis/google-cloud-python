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

    :type image: str
    :param image: A string which can be a URL, a Google Cloud Storage path,
                  or a byte stream of the image.

    See:
    https://cloud.google.com/vision/reference/rest/v1/images/annotate#Image
    """
    def __init__(self, image):
        self._source = None
        self._content = None

        # TODO: string index out of range for len(string) < 4.
        # TODO: Support file path.
        if image[:4] == 'http':
            import httplib2
            http = httplib2.Http()
            response, downloaded_image = http.request(image, 'GET')
            self._content = b64encode(downloaded_image)
        elif image[:5] == 'gs://':
            self._source = image
        elif type(image) == str:
            self._content = b64encode(image)

    def as_dict(self):
        """Generate dictionary for request"""

        if self.content:
            return {
                "content": self.content
            }
        else:
            return {
                "source": {
                    "gcs_image_uri": self.source
                }
            }

    @property
    def source(self):
        """Google Cloud Storage image URI"""
        return self._source

    @property
    def content(self):
        """Base64 encoded image content"""
        return self._content
