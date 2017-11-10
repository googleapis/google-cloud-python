# Copyright 2017 Google LLC
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

"""Text annotations of an image."""

import json

from google.cloud.vision_v1.proto import text_annotation_pb2
from google.protobuf import json_format


class TextAnnotation(object):
    """Representation of a text annotation returned from the Vision API.

    :type pages: list
    :param pages: List of
                  :class:`~google.cloud.vision_v1.proto.\
                  text_annotation_pb2.Page`.

    :type text: str
    :param text: String containing text detected from the image.
    """
    def __init__(self, pages, text):
        self._pages = pages
        self._text = text

    @classmethod
    def from_api_repr(cls, annotation):
        """Factory: construct an instance of ``TextAnnotation`` from JSON.

        :type annotation: dict
        :param annotation: Dictionary response from Vision API.

        :rtype: :class:`~google.cloud.vision.text.TextAnnotation`
        :returns: Instance of ``TextAnnotation``.
        """
        annotation_json = json.dumps(annotation)
        text_annotation = text_annotation_pb2.TextAnnotation()
        json_format.Parse(annotation_json, text_annotation)
        return cls(text_annotation.pages, text_annotation.text)

    @classmethod
    def from_pb(cls, annotation):
        """Factory: construct an instance of ``TextAnnotation`` from protobuf.

        :type annotation: :class:`~google.cloud.vision_v1.proto.\
                          text_annotation_pb2.TextAnnotation`
        :param annotation: Populated instance of ``TextAnnotation``.

        :rtype: :class:`~google.cloud.vision.text.TextAnnotation`
        :returns: Populated instance of ``TextAnnotation``.
        """
        return cls(annotation.pages, annotation.text)

    @property
    def pages(self):
        """Pages found in text image.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision_v1.proto.\
                          text_annotation_pb2.Page`.
        """
        return self._pages

    @property
    def text(self):
        """Text detected from an image.

        :rtype: str
        :returns: String of text found in an image.
        """
        return self._text
