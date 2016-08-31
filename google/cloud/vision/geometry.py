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

"""Geometry and other generic classes used by the Vision API."""


class BoundsBase(object):
    """Base class for handling bounds with vertices."""
    def __init__(self, vertices):
        self._vertices = vertices

    @classmethod
    def from_api_repr(cls, response_vertices):
        """Factory: construct BoundsBase instance from Vision API response.

        :type response_vertices: dict
        :param response_vertices: List of vertices.

        :rtype: :class:`gcloud.vision.geometry.BoundsBase`
        :returns: Instance of BoundsBase with populated verticies.
        """
        vertices = []
        for vertex in response_vertices['vertices']:
            vertices.append(Vertex(vertex.get('x', None),
                                   vertex.get('y', None)))
        return cls(vertices)

    @property
    def vertices(self):
        """List of vertices.

        :rtype: list
        :returns: List of populated vertices.
        """
        return self._vertices


class Position(object):
    """A 3D position in the image.

    See:
    https://cloud.google.com/vision/reference/rest/v1/images/annotate#Position
    """
    def __init__(self, x_coordinate, y_coordinate, z_coordinate):
        self._x_coordinate = x_coordinate
        self._y_coordinate = y_coordinate
        self._z_coordinate = z_coordinate

    @classmethod
    def from_api_repr(cls, response_position):
        """Factory: construct 3D position from API response.

        :rtype: :class:`gcloud.vision.geometry.Position`
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
