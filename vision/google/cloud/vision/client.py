# Copyright 2016 Google LLC
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

import os
import warnings

from google.cloud.client import ClientWithProject
from google.cloud.environment_vars import DISABLE_GRPC

from google.cloud.vision._gax import _GAPICVisionAPI
from google.cloud.vision._http import _HTTPVisionAPI
from google.cloud.vision.batch import Batch
from google.cloud.vision.image import Image


_USE_GRPC = not os.getenv(DISABLE_GRPC, False)


class Client(ClientWithProject):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of.
                    If not passed, falls back to the default inferred
                    from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``_http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type _http: :class:`~requests.Session`
    :param _http: (Optional) HTTP object to make requests. Can be any object
                  that defines ``request()`` with the same interface as
                  :meth:`requests.Session.request`. If not passed, an
                  ``_http`` object is created that is bound to the
                  ``credentials`` for the current object.
                  This parameter should be considered private, and could
                  change in the future.

    :type _use_grpc: bool
    :param _use_grpc: (Optional) Explicitly specifies whether
                      to use the gRPC transport (via GAX) or HTTP. If unset,
                      falls back to the ``GOOGLE_CLOUD_DISABLE_GRPC``
                      environment variable.
                      This parameter should be considered private, and could
                      change in the future.
    """

    SCOPE = ('https://www.googleapis.com/auth/cloud-platform',)
    """The scopes required for authenticating as a Cloud Vision consumer."""

    _vision_api_internal = None

    def __init__(self, project=None, credentials=None, _http=None,
                 _use_grpc=None):
        warnings.warn(
            'This client class and objects that derive from it have been '
            'deprecated. Use `google.cloud.vision.ImageAnnotatorClient` '
            '(provided by this package) instead. This client will be removed '
            'in a future release.',
            DeprecationWarning,
        )

        super(Client, self).__init__(
            project=project, credentials=credentials, _http=_http)
        if _use_grpc is None:
            self._use_grpc = _USE_GRPC
        else:
            self._use_grpc = _use_grpc

    def batch(self):
        """Batch multiple images into a single API request.

        :rtype: :class:`google.cloud.vision.batch.Batch`
        :returns: Instance of ``Batch``.
        """
        return Batch(self)

    def image(self, content=None, filename=None, source_uri=None):
        """Get instance of Image using current client.

        :type content: bytes
        :param content: Byte stream of an image.

        :type filename: str
        :param filename: Filename to image.

        :type source_uri: str
        :param source_uri: URL or Google Cloud Storage URI of image.

        :rtype: :class:`~google.cloud.vision.image.Image`
        :returns: Image instance with the current client attached.
        """
        return Image(client=self, content=content, filename=filename,
                     source_uri=source_uri)

    @property
    def _vision_api(self):
        """Proxy method that handles which transport call Vision Annotate.

        :rtype: :class:`~google.cloud.vision._http._HTTPVisionAPI`
                or :class:`~google.cloud.vision._gax._GAPICVisionAPI`
        :returns: Instance of ``_HTTPVisionAPI`` or ``_GAPICVisionAPI`` used to
                  make requests.
        """
        if self._vision_api_internal is None:
            if self._use_grpc:
                self._vision_api_internal = _GAPICVisionAPI(self)
            else:
                self._vision_api_internal = _HTTPVisionAPI(self)
        return self._vision_api_internal
