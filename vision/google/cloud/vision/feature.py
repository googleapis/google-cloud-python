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

"""Feature represenging various types of annotating."""


class FeatureTypes(object):
    """Feature Types to indication which annotations to perform.

    See
    https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#Type
    """
    CROP_HINTS = 'CROP_HINTS'
    DOCUMENT_TEXT_DETECTION = 'DOCUMENT_TEXT_DETECTION'
    FACE_DETECTION = 'FACE_DETECTION'
    IMAGE_PROPERTIES = 'IMAGE_PROPERTIES'
    LABEL_DETECTION = 'LABEL_DETECTION'
    LANDMARK_DETECTION = 'LANDMARK_DETECTION'
    LOGO_DETECTION = 'LOGO_DETECTION'
    SAFE_SEARCH_DETECTION = 'SAFE_SEARCH_DETECTION'
    TEXT_DETECTION = 'TEXT_DETECTION'
    WEB_DETECTION = 'WEB_DETECTION'


class Feature(object):
    """Feature object specifying the annotation type and maximum results.

    :type feature_type: str
    :param feature_type: String representation of
                         :class:`~google.cloud.vision.feature.FeatureType`.

    :type max_results: int
    :param max_results: Number of results to return for the specified
                        feature type.

    See
    https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#Feature
    """
    def __init__(self, feature_type, max_results=1):
        try:
            self._feature_type = getattr(FeatureTypes, feature_type)
        except AttributeError:
            raise AttributeError('Feature type passed in cannot be found.')
        self._max_results = int(max_results)

    def as_dict(self):
        """Generate dictionary for Feature request format.

        :rtype: dict
        :returns: Dictionary representation of a
                  :class:`~google.cloud.vision.feature.FeatureType`.
        """
        return {
            'type': self.feature_type,
            'maxResults': self.max_results
        }

    @property
    def feature_type(self):
        """"Feature type string.

        :rtype: :class:`~google.cloud.vision.feature.FeatureTypes`
        :returns: Instance of
                  :class:`~google.cloud.vision.feature.FeatureTypes`
        """
        return self._feature_type

    @property
    def max_results(self):
        """Maximum number of results for feature type.

        :rtype: int
        :returns: Maxium results to be returned.
        """
        return self._max_results
