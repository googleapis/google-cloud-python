# Copyright 2016 Google Inc.
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

"""Client for interacting with the Google Cloud Vision API."""

from google.cloud.client import JSONClient
from google.cloud.vision.connection import Connection
from google.cloud.vision.image import Image
from google.cloud.vision._http import _HTTPVisionAPI


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of.
                    If not passed, falls back to the default inferred
                    from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type http: :class:`~httplib2.Http`
    :param http: (Optional) HTTP object to make requests. Can be any object
                 that defines ``request()`` with the same interface as
                 :meth:`~httplib2.Http.request`. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """
    _vision_api_internal = None

    def __init__(self, project=None, credentials=None, http=None):
        super(Client, self).__init__(
            project=project, credentials=credentials, http=http)
        self._connection = Connection(
            credentials=self._credentials, http=self._http)

    def image(self, content=None, filename=None, source_uri=None):
        """Get instance of Image using current client.

        :type content: bytes
        :param content: Byte stream of an image.

        :type filename: str
        :param filename: Filename to image.

        :type source_uri: str
        :param source_uri: Google Cloud Storage URI of image.

        :rtype: :class:`~google.cloud.vision.image.Image`
        :returns: Image instance with the current client attached.
        """
        return Image(client=self, content=content, filename=filename,
                     source_uri=source_uri)

    @property
    def _vision_api(self):
        """Proxy method that handles which transport call Vision Annotate.

        :rtype: :class:`~google.cloud.vision._rest._HTTPVisionAPI`
        :returns: Instance of ``_HTTPVisionAPI`` used to make requests.
        """
        if self._vision_api_internal is None:
            self._vision_api_internal = _HTTPVisionAPI(self)
        return self._vision_api_internal
