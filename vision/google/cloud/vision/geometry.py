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

"""Geometry and other generic classes used by the Vision API."""


class BoundsBase(object):
    """Base class for handling bounds with vertices.

    :type vertices: list of :class:`~google.cloud.vision.geometry.Vertex`
    :param vertices: List of vertcies describing points on an image.
    """
    def __init__(self, vertices):
        self._vertices = vertices

    @classmethod
    def from_api_repr(cls, vertices):
        """Factory: construct BoundsBase instance from Vision API response.

        :type vertices: dict
        :param vertices: List of vertices.

        :rtype: :class:`~google.cloud.vision.geometry.BoundsBase` or None
        :returns: Instance of ``BoundsBase`` with populated verticies or None.
        """
        if vertices is None:
            return None
        return cls([Vertex(vertex.get('x', None), vertex.get('y', None))
                    for vertex in vertices.get('vertices', ())])

    @classmethod
    def from_pb(cls, vertices):
        """Factory: construct BoundsBase instance from a protobuf response.

        :type vertices: :class:`~google.cloud.vision_v1.proto.\
                                 geometry_pb2.BoundingPoly`
        :param vertices: List of vertices.

        :rtype: :class:`~google.cloud.vision.geometry.BoundsBase` or None
        :returns: Instance of ``BoundsBase`` with populated verticies.
        """
        return cls([Vertex(vertex.x, vertex.y)
                    for vertex in vertices.vertices])

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
    def from_api_repr(cls, location_info):
        """Factory: construct location information from Vision API response.

        :type location_info: dict
        :param location_info: Dictionary response of locations.

        :rtype: :class:`~google.cloud.vision.geometry.LocationInformation`
        :returns: ``LocationInformation`` with populated latitude and
                  longitude.
        """
        lat_long = location_info.get('latLng', {})
        latitude = lat_long.get('latitude')
        longitude = lat_long.get('longitude')
        return cls(latitude, longitude)

    @classmethod
    def from_pb(cls, location_info):
        """Factory: construct location information from a protobuf response.

        :type location_info: :class:`~google.cloud.vision.v1.LocationInfo`
        :param location_info: Protobuf response with ``LocationInfo``.

        :rtype: :class:`~google.cloud.vision.geometry.LocationInformation`
        :returns: ``LocationInformation`` with populated latitude and
                  longitude.
        """
        return cls(location_info.lat_lng.latitude,
                   location_info.lat_lng.longitude)

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

    See
    https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#Position

    :type x_coordinate: float
    :param x_coordinate: X position coordinate.

    :type y_coordinate: float
    :param y_coordinate: Y position coordinate.

    :type z_coordinate: float
    :param z_coordinate: Z position coordinate.
    """
    def __init__(self, x_coordinate=None, y_coordinate=None,
                 z_coordinate=None):
        self._x_coordinate = x_coordinate
        self._y_coordinate = y_coordinate
        self._z_coordinate = z_coordinate

    @classmethod
    def from_api_repr(cls, position):
        """Factory: construct 3D position from API response.

        :type position: dict
        :param position: Dictionary with 3 axis position data.

        :rtype: :class:`~google.cloud.vision.geometry.Position`
        :returns: ``Position`` constructed with 3D points from API response.
        """
        x_coordinate = position['x']
        y_coordinate = position['y']
        z_coordinate = position['z']
        return cls(x_coordinate, y_coordinate, z_coordinate)

    @classmethod
    def from_pb(cls, response_position):
        """Factory: construct 3D position from API response.

        :rtype: :class:`~google.cloud.vision.geometry.Position`
        :returns: ``Position`` constructed with 3D points from API response.
        """
        x_coordinate = response_position.x
        y_coordinate = response_position.y
        z_coordinate = response_position.z
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

    See
    https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#Vertex

    :type x_coordinate: float
    :param x_coordinate: X position coordinate.

    :type y_coordinate: float
    :param y_coordinate: Y position coordinate.
    """
    def __init__(self, x_coordinate=None, y_coordinate=None):
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
