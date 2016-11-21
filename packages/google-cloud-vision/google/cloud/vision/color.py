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

"""Image properties class representation derived from Vision API response."""


class ImagePropertiesAnnotation(object):
    """Representation of image properties

    :type colors: list
    :param colors: List of
                   :class:`~google.cloud.vision.color.ColorInformation`.
    """
    def __init__(self, colors):
        self._colors = colors

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct ``ImagePropertiesAnnotation`` from a response.

        :type response: dict
        :param response: Dictionary response from Vision API with image
                         properties data.

        :rtype: :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`.
        :returns: Populated instance of ``ImagePropertiesAnnotation``.
        """
        raw_colors = response.get('dominantColors', {}).get('colors', ())
        colors = [ColorInformation.from_api_repr(color)
                  for color in raw_colors]
        return cls(colors)

    @property
    def colors(self):
        """Colors in an image.

        :rtype: list of :class:`~google.cloud.vision.color.ColorInformation`
        :returns: Populated list of ``ColorInformation``.
        """
        return self._colors


class Color(object):
    """Representation of RGBA color information.

    :type red: int
    :param red: The amount of red in the color as a value in the interval
                [0, 255].

    :type green: int
    :param green: The amount of green in the color as a value in the interval
                  [0, 255].

    :type blue: int
    :param blue: The amount of blue in the color as a value in the interval
                 [0, 255].

    :type alpha: float
    :param alpha: The fraction of this color that should be applied to the
                  pixel.
    """
    def __init__(self, red, green, blue, alpha):
        self._red = red
        self._green = green
        self._blue = blue
        self._alpha = alpha

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct a ``Color`` from a Vision API response.

        :type response: dict
        :param response: Color from API Response.

        :rtype: :class:`~google.cloud.vision.color.Color`
        :returns: Instance of :class:`~google.cloud.vision.color.Color`.
        """
        red = response.get('red', 0)
        green = response.get('green', 0)
        blue = response.get('blue', 0)
        alpha = response.get('alpha', 0.0)

        return cls(red, green, blue, alpha)

    @property
    def red(self):
        """Red component of the color.

        :rtype: int
        :returns: Red RGB value.
        """
        return self._red

    @property
    def green(self):
        """Green component of the color.

        :rtype: int
        :returns: Green RGB value.
        """
        return self._green

    @property
    def blue(self):
        """Blue component of the color.

        :rtype: int
        :returns: Blue RGB value.
        """
        return self._blue

    @property
    def alpha(self):
        """Alpha transparency level.

        :rtype: float
        :returns: Alpha transparency level.
        """
        return self._alpha


class ColorInformation(object):
    """Representation of color information from API response.

    :type color: :class:`~google.cloud.vision.color.Color`
    :param color: RGB components of the color.

    :type score: float
    :param score: Image-specific score for this color. Value in range [0, 1].

    :type pixel_fraction: float
    :param pixel_fraction: Stores the fraction of pixels the color occupies in
                           the image. Value in range [0, 1].
    """
    def __init__(self, color, score, pixel_fraction):
        self._color = color
        self._score = score
        self._pixel_fraction = pixel_fraction

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct ``ColorInformation`` for a color found.

        :type response: dict
        :param response: Color data with extra meta information.

        :rtype: :class:`~google.cloud.vision.color.ColorInformation`
        :returns: Instance of ``ColorInformation``.
        """
        color = Color.from_api_repr(response.get('color'))
        score = response.get('score')
        pixel_fraction = response.get('pixelFraction')

        return cls(color, score, pixel_fraction)

    @property
    def color(self):
        """RGB components of the color.

        :rtype: :class:`~google.vision.color.Color`
        :returns: Instance of ``Color``.
        """
        return self._color

    @property
    def score(self):
        """Image-specific score for this color. Value in range [0, 1].

        :rtype: float
        :returns: Image score for this color.
        """
        return self._score

    @property
    def pixel_fraction(self):
        """Stores the fraction of pixels the color occupies in the image.

        :rtype: float
        :returns: Pixel fraction value in range [0, 1].
        """
        return self._pixel_fraction
