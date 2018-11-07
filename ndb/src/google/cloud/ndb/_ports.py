# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Ported implementations from the Google App Engine SDK.

The following members have been brought in:

- ``google.appengine.api.datastore_types.GeoPt``
"""


import functools

from google.cloud.ndb import exceptions


@functools.total_ordering
class GeoPt:
    """A geographical point, specified by latitude and longitude.

    Typically, latitude and longitude are floating-point coordinates. Often
    used to integrate with mapping sites like Google Maps. May also be used as
    ICBM coordinates.

    This is the ``georss:point`` element. In XML output, the coordinates are
    provided as the lat and lon attributes. See:
    `http://georss.org/ <http://georss.org/>`_.

    When serialized, a :class:`GeoPt` will be of the form
    ``<latitude>,<longitude>``.

    Args:
        lat (Union[str, float]): One of

            * the latitude (as float or string), must be in the range
              ``[-90, 90]``
            * a string containing both the latitude and longitude, comma
              separated
        lon (Optional[Union[str, float]]): The longitude (as float or string),
            must be in the range ``[-180, 180]``.
    """

    __slots__ = ("lat", "lon")

    def __init__(self, lat, lon=None):
        if lon is None:
            lat, lon = self._split_single_argument(lat)

        lat, lon = self._to_bounded_float(lat, lon)
        self.lat = lat
        self.lon = lon

    @staticmethod
    def _split_single_argument(value):
        """Split a single constructor argument into two.

        Args:
            value (str): The value to be split. Expected to be of the form
                ``"{latitude},{longitude}"``.

        Returns:
            Tuple[str, str]: The components of the comma-separated ``value``.

        Raises:
            .BadValueError: If the value is not formatted correctly.
        """
        try:
            latitude, longitude = value.split(",")
            return latitude, longitude
        except (AttributeError, ValueError):
            raise exceptions.BadValueError(
                'Expected a "lat,long" formatted string; received '
                "{} (a {}).".format(value, value.__class__.__name__)
            )

    @staticmethod
    def _to_bounded_float(latitude, longitude):
        """Convert latitude and longitude to floating point values.

        Args:
            latitude (Union[float, str]): The latitude value to be converted.
                Must be in the range ``[-90, 90]``.
            longitude (Union[float, str]): The longitude value to be converted.
                Must be in the range ``[-180, 180]``.

        Returns:
            Tuple[float, float]: The components of the comma-separated ``value``.

        Raises:
            .BadValueError: If one of ``latitude``, ``longitude`` is not
                convertible to a floating point number.
            .BadValueError: If ``latitude`` is outside the range ``[-90, 90]``.
            .BadValueError: If ``longitude`` is outside the range
                ``[-180, 180]``.
        """
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            template = (
                "Expected floats for lat and long; received {} (a {}) "
                "and {} (a {})."
            )
            msg = template.format(
                latitude,
                latitude.__class__.__name__,
                longitude,
                longitude.__class__.__name__,
            )
            raise exceptions.BadValueError(msg)

        if abs(latitude) > 90:
            raise exceptions.BadValueError(
                "Latitude must be between -90 and 90; "
                "received {:f}".format(latitude)
            )

        if abs(longitude) > 180:
            raise exceptions.BadValueError(
                "Longitude must be between -180 and 180; "
                "received {:f}".format(longitude)
            )

        return latitude, longitude

    def __eq__(self, other):
        if not isinstance(other, GeoPt):
            try:
                other = GeoPt(other)
            except exceptions.BadValueError:
                return NotImplemented

        return self.lat == other.lat and self.lon == other.lon

    def __lt__(self, other):
        if not isinstance(other, GeoPt):
            try:
                other = GeoPt(other)
            except exceptions.BadValueError:
                return NotImplemented

        return (self.lat, self.lon) < (other.lat, other.lon)

    def __hash__(self):
        """Returns an integer hash of this point.

        Implements Python's hash protocol so that GeoPts may be used in sets
        and as dictionary keys.

        Returns:
            int: The hash of the ``(latitude, longitude)`` tuple.
        """
        return hash((self.lat, self.lon))

    def __repr__(self):
        """Returns an ``eval()``-able string representation of this GeoPt.

        The returned string is of the form
        ``datastore_types.GeoPt(latitude, longitude)``.

        Returns:
            str: The repr for this instance.
        """
        return "datastore_types.GeoPt({!r}, {!r})".format(self.lat, self.lon)

    def __str__(self):
        return "{},{}".format(self.lat, self.lon)

    def ToXml(self):
        """Convert the current point to XML.

        Returns:
            str: The equivalent XML.
        """
        return "<georss:point>{} {}</georss:point>".format(self.lat, self.lon)
