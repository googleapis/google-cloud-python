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

"""Define annotations."""


class EntityAnnotation(object):
    _mid = None
    _locale = None
    _description = None
    _score = None
    _confidence = None
    _topicality = None
    _bounding_poly = None
    _locations = []
    _properties = []

    def __init__(self, mid, locale, description, score, confidence, topicality,
                 bounding_poly, locations, properties):
        self._mid = mid
        self._locale = locale
        self._description = description
        self._score = score
        self._confidence = confidence
        self._topicality = topicality
        self._bounding_poly = bounding_poly
        self._locations = locations
        self._properties = properties

    @property
    def mid(self):
        return self._mid

    @property
    def locale(self):
        return self._locale

    @property
    def description(self):
        return self._description

    @property
    def score(self):
        return self._score

    @property
    def confidence(self):
        return self._confidence

    @property
    def topicality(self):
        return self._topicality

    @property
    def bounding_poly(self):
        return self._bounding_poly

    @property
    def locations(self):
        return self._locations

    @property
    def properties(self):
        return self._properties


class LabelAnnotation(EntityAnnotation):
    def __init__(self):
        raise NotImplementedError


class LandmarkAnnotation(EntityAnnotation):
    def __init__(self):
        raise NotImplementedError


class LogoAnnotation(EntityAnnotation):
    def __init__(self):
        raise NotImplementedError


class TextAnnotation(EntityAnnotation):
    def __init__(self):
        raise NotImplementedError


class SafeSearchAnnotation(EntityAnnotation):
    def __init__(self):
        raise NotImplementedError
