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

"""Geometry and other generic classes used by the Vision API."""


class BoundsBase(object):
    """Base class for handling bounds with vertices.

    :type vertices: list of :class:`~google.cloud.vision.geometry.Vertex`
    :param vertices: List of vertcies describing points on an image.
    """
    def __init__(self, vertices):
        self._vertices = vertices

    @classmethod
    def from_api_repr(cls, response_vertices):
        """Factory: construct BoundsBase instance from Vision API response.

        :type response_vertices: dict
        :param response_vertices: List of vertices.

        :rtype: :class:`~google.cloud.vision.geometry.BoundsBase` or None
        :returns: Instance of BoundsBase with populated verticies or None.
        """
        if not response_vertices:
            return None

        vertices = [Vertex(vertex.get('x', None), vertex.get('y', None)) for
                    vertex in response_vertices.get('vertices', [])]
        return cls(vertices)

    @property
    def vertices(self):
        """List of vertices.

        :rtype: list of :class:`~google.cloud.vision.geometry.Vertex`
        :returns: List of populated vertices.
        """
        return self._vertices


class Bounds(BoundsBase):
    """A polygon boundry of the detected feature."""


class FDBounds(BoundsBase):
    """The bounding polygon of just the skin portion of the face."""


class LocationInformation(object):
    """Representation of location information returned by the Vision API.

    :type latitude: float
    :param latitude: Latitude coordinate of geographical location.

    :type longitude: float
    :param longitude: Longitude coordinate of geographical location.
    """
    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct location information from Vision API response.

        :type response: dict
        :param response: Dictionary response of locations.

        :rtype: :class:`~google.cloud.vision.geometry.LocationInformation`
        :returns: ``LocationInformation`` with populated latitude and
                  longitude.
        """
        latitude = response['latLng']['latitude']
        longitude = response['latLng']['longitude']
        return cls(latitude, longitude)

    @property
    def latitude(self):
        """Latitude coordinate.

        :rtype: float
        :returns: Latitude coordinate of location.
        """
        return self._latitude

    @property
    def longitude(self):
        """Longitude coordinate.

        :rtype: float
        :returns: Longitude coordinate of location.
        """
        return self._longitude


class Position(object):
    """A 3D position in the image.

    See:
    https://cloud.google.com/vision/reference/rest/v1/images/annotate#Position

    :type x_coordinate: float
    :param x_coordinate: X position coordinate.

    :type y_coordinate: float
    :param y_coordinate: Y position coordinate.

    :type z_coordinate: float
    :param z_coordinate: Z position coordinate.
    """
    def __init__(self, x_coordinate, y_coordinate, z_coordinate):
        self._x_coordinate = x_coordinate
        self._y_coordinate = y_coordinate
        self._z_coordinate = z_coordinate

    @classmethod
    def from_api_repr(cls, response_position):
        """Factory: construct 3D position from API response.

        :rtype: :class:`~google.cloud.vision.geometry.Position`
        :returns: `Position` constructed with 3D points from API response.
        """
        x_coordinate = response_position['x']
        y_coordinate = response_position['y']
        z_coordinate = response_position['z']
        return cls(x_coordinate, y_coordinate, z_coordinate)

    @property
    def x_coordinate(self):
        """X position coordinate.

        :rtype: float
        :returns: X position coordinate.
        """
        return self._x_coordinate

    @property
    def y_coordinate(self):
        """Y position coordinate.

        :rtype: float
        :returns: Y position coordinate.
        """
        return self._y_coordinate

    @property
    def z_coordinate(self):
        """Z position coordinate.

        :rtype: float
        :returns: Z position coordinate.
        """
        return self._z_coordinate


class Vertex(object):
    """A vertex represents a 2D point in the image.

    See:
    https://cloud.google.com/vision/reference/rest/v1/images/annotate#Vertex

    :type x_coordinate: float
    :param x_coordinate: X position coordinate.

    :type y_coordinate: float
    :param y_coordinate: Y position coordinate.
    """
    def __init__(self, x_coordinate, y_coordinate):
        self._x_coordinate = x_coordinate
        self._y_coordinate = y_coordinate

    @property
    def x_coordinate(self):
        """X position coordinate.

        :rtype: float
        :returns: X position coordinate.
        """
        return self._x_coordinate

    @property
    def y_coordinate(self):
        """Y position coordinate.

        :rtype: float
        :returns: Y position coordinate.
        """
        return self._y_coordinate
