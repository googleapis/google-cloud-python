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

"""Web image search."""


class WebDetection(object):
    """Representation of a web detection sent from the Vision API.

    :type web_entities: list
    :param web_entities: List of
                         :class:`google.cloud.vision_v1.proto.\
                         web_detection_pb2.WebDetection.WebEntity`.

    :type full_matching_images: list
    :param full_matching_images: List of
                                 :class:`google.cloud.vision_v1.proto.\
                                 web_detection_pb2.WebDetection.WebImage`.

    :type partial_matching_images: list
    :param partial_matching_images: List of
                                    :class:`google.cloud.vision_v1.proto.\
                                    web_detection_pb2.WebDetection.WebImage`.

    :type pages_with_matching_images: list
    :param pages_with_matching_images: List of
                                       :class:`google.cloud.vision_v1.proto.\
                                       web_detection_pb2.WebDetection.\
                                       WebPage`.
    """
    def __init__(self, web_entities=(), full_matching_images=(),
                 partial_matching_images=(), pages_with_matching_images=()):
        self._web_entities = web_entities
        self._full_matching_images = full_matching_images
        self._partial_matching_images = partial_matching_images
        self._pages_with_matching_images = pages_with_matching_images

    @classmethod
    def from_api_repr(cls, detection):
        """Factory: construct ``WebDetection`` from Vision API response.

        :type detection: dict
        :param detection: Dictionary representing a ``WebDetection``.

        :rtype: :class:`~google.cloud.vision.web.WebDetection`
        :returns: Populated instance of ``WebDetection``.
        """
        web_entities = detection.get('webEntities')
        full_matching_images = detection.get('fullMatchingImages')
        partial_matching_images = detection.get('partialMatchingImages')
        pages_with_matching_images = detection.get('pagesWithMatchingImages')

        web_detection = {
            'web_entities': [WebEntity.from_api_repr(web_entity)
                             for web_entity in web_entities],
            'full_matching_images': [WebImage.from_api_repr(web_image)
                                     for web_image in full_matching_images],
            'partial_matching_images': [WebImage.from_api_repr(web_image)
                                        for web_image
                                        in partial_matching_images],
            'pages_with_matching_images': [WebPage.from_api_repr(web_page)
                                           for web_page
                                           in pages_with_matching_images],
        }
        return cls(**web_detection)

    @classmethod
    def from_pb(cls, detection):
        """Factory: construct ``WebDetection`` from Vision API response.

        :type detection: :class:`~google.cloud.vision_v1.proto.\
                          web_detection_pb2.WebDetection`
        :param detection: Dictionary representing a ``WebDetection``.

        :rtype: :class:`~google.cloud.vision.web.WebDetection`
        :returns: Populated instance of ``WebDetection``.
        """
        web_entities = [WebEntity.from_pb(web_entity)
                        for web_entity in detection.web_entities]
        full_image_matches = [WebImage.from_pb(web_image)
                              for web_image in detection.full_matching_images]
        partial_image_matches = [WebImage.from_pb(web_image)
                                 for web_image
                                 in detection.partial_matching_images]
        pages_with_images = [WebPage.from_pb(web_page)
                             for web_page
                             in detection.pages_with_matching_images]
        return cls(web_entities, full_image_matches, partial_image_matches,
                   pages_with_images)

    @property
    def web_entities(self):
        """Return the web entities.

        :rtype: list
        :returns: A list of ``WebEntity`` instances.
        """
        return self._web_entities

    @property
    def full_matching_images(self):
        """Return the full matching images.

        :rtype: list
        :returns: A list of ``WebImage`` instances.
        """
        return self._full_matching_images

    @property
    def partial_matching_images(self):
        """Return the partially matching images.

        :rtype: list
        :returns: A list of ``WebImage`` instances.
        """
        return self._partial_matching_images

    @property
    def pages_with_matching_images(self):
        """Return the web pages with matching images.

        :rtype: list
        :returns: A list of ``WebPage`` instances.
        """
        return self._pages_with_matching_images


class WebEntity(object):
    """Object containing a web entity sent from the Vision API.

    :type entity_id: str
    :param entity_id: ID string for the entity.

    :type score: float
    :param score: Overall relevancy score for the entity.

    :type description: str
    :param description: Description of the entity.
    """

    def __init__(self, entity_id, score, description):
        self._entity_id = entity_id
        self._score = score
        self._description = description

    @classmethod
    def from_api_repr(cls, web_entity):
        """Factory: construct ``WebImage`` from Vision API response.

        :type web_entity: dict
        :param web_entity: Dictionary representing a web entity

        :rtype: :class:`~google.cloud.vision.web.WebEntity`
        :returns: Populated instance of ``WebEntity``.
        """
        return cls(web_entity.get('entityId'), web_entity.get('score'),
                   web_entity.get('description'))

    @classmethod
    def from_pb(cls, web_entity):
        """Factory: construct ``WebEntity`` from Vision API response.

        :type web_entity: :class:`~google.cloud.vision_v1.proto.\
                          web_detection_pb2.WebDetection.WebEntity`
        :param web_entity: Dictionary representing a web entity

        :rtype: :class:`~google.cloud.vision.web.WebEntity`
        :returns: Populated instance of ``WebEntity``.
        """
        return cls(web_entity.entity_id, web_entity.score,
                   web_entity.description)

    @property
    def entity_id(self):
        """The entity ID.

        :rtype: str
        :returns: String representing the entity ID. Opaque.
        """
        return self._entity_id

    @property
    def score(self):
        """Overall relevancy score for the image.

        .. note::

            Not normalized nor comparable between requests.

        :rtype: float
        :returns: Relevancy score as a float.
        """
        return self._score

    @property
    def description(self):
        """Canonical description of the entity, in English.

        :rtype: str
        :returns: Description of the entity.
        """
        return self._description


class WebImage(object):
    """Object containing image information elsewhere on the web.

    :type url: str
    :param url: URL of the matched image.

    :type score: float
    :param score: Overall relevancy score of the image.
    """
    def __init__(self, url, score):
        self._url = url
        self._score = score

    @classmethod
    def from_api_repr(cls, web_image):
        """Factory: construct ``WebImage`` from Vision API response.

        :type web_image: dict
        :param web_image: Dictionary representing a web image

        :rtype: :class:`~google.cloud.vision.web.WebImage`
        :returns: Populated instance of ``WebImage``.
        """
        return cls(web_image['url'], web_image['score'])

    @classmethod
    def from_pb(cls, web_image):
        """Factory: construct ``WebImage`` from Vision API response.

        :type web_image: :class:`~google.cloud.vision_v1.proto.\
                         web_detection_pb2.WebDetection.WebImage`
        :param web_image: Dictionary representing a web image

        :rtype: :class:`~google.cloud.vision.web.WebImage`
        :returns: Populated instance of ``WebImage``.
        """
        return cls(web_image.url, web_image.score)

    @property
    def url(self):
        """The URL of the matched image.

        :rtype: str
        :returns: URL of matched image.
        """
        return self._url

    @property
    def score(self):
        """Overall relevancy score for the image.

        .. note::

            Not normalized nor comparable between requests.

        :rtype: float
        :returns: Relevancy score as a float.
        """
        return self._score


class WebPage(object):
    """Web page that may contain this image or a similar one.

    :type url: str
    :param url: URL of the matched image.

    :type score: float
    :param score: Overall relevancy score of the image.
    """
    def __init__(self, url, score):
        self._url = url
        self._score = score

    @classmethod
    def from_api_repr(cls, web_page):
        """Factory: construct ``WebPage`` from Vision API response.

        :type web_page: dict
        :param web_page: Dictionary representing a web page

        :rtype: :class:`~google.cloud.vision.web.WebPage`
        :returns: Populated instance of ``WebPage``.
        """
        return cls(web_page['url'], web_page['score'])

    @classmethod
    def from_pb(cls, web_page):
        """Factory: construct ``WebPage`` from Vision API response.

        :type web_page: :class:`~google.cloud.vision_v1.proto.\
                        web_detection_pb2.WebDetection.WebPage`
        :param web_page: Dictionary representing a web image

        :rtype: :class:`~google.cloud.vision.web.WebPage`
        :returns: Populated instance of ``WebPage``.
        """
        return cls(web_page.url, web_page.score)

    @property
    def url(self):
        """The page URL.

        :rtype: str
        :returns: String representing a URL.
        """
        return self._url

    @property
    def score(self):
        """Overall relevancy score for the image.

        .. note::

            Not normalized nor comparable between requests.

        :rtype: float
        :returns: Relevancy score as a float.
        """
        return self._score
