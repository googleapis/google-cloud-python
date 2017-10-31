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
    def from_api_repr(cls, image_properties):
        """Factory: construct ``ImagePropertiesAnnotation`` from a response.

        :type image_properties: dict
        :param image_properties: Dictionary response from Vision API with image
                                 properties data.

        :rtype: list of
                :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`.
        :returns: List of ``ImagePropertiesAnnotation``.
        """
        colors = image_properties.get('dominantColors', {}).get('colors', ())
        return cls([ColorInformation.from_api_repr(color)
                    for color in colors])

    @classmethod
    def from_pb(cls, image_properties):
        """Factory: construct ``ImagePropertiesAnnotation`` from a response.

        :type image_properties: :class:`~google.cloud.vision_v1.proto.\
                                image_annotator_pb2.ImageProperties`
        :param image_properties: Protobuf response from Vision API with image
                                 properties data.

        :rtype: list of
                :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`
        :returns: List of ``ImagePropertiesAnnotation``.
        """
        colors = getattr(image_properties.dominant_colors, 'colors', ())
        if len(colors) > 0:
            return cls([ColorInformation.from_pb(color) for color in colors])

    @property
    def colors(self):
        """Colors in an image.

        :rtype: list of :class:`~google.cloud.vision.color.ColorInformation`
        :returns: Populated list of ``ColorInformation``.
        """
        return self._colors


class Color(object):
    """Representation of RGBA color information.

    :type red: float
    :param red: The amount of red in the color as a value in the interval
                [0.0, 255.0].

    :type green: float
    :param green: The amount of green in the color as a value in the interval
                  [0.0, 255.0].

    :type blue: float
    :param blue: The amount of blue in the color as a value in the interval
                 [0.0, 255.0].

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
        red = float(response.get('red', 0.0))
        green = float(response.get('green', 0.0))
        blue = float(response.get('blue', 0.0))
        alpha = response.get('alpha', 0.0)

        return cls(red, green, blue, alpha)

    @classmethod
    def from_pb(cls, color):
        """Factory: construct a ``Color`` from a protobuf response.

        :type color: :module: `google.type.color_pb2`
        :param color: ``Color`` from API Response.

        :rtype: :class:`~google.cloud.vision.color.Color`
        :returns: Instance of :class:`~google.cloud.vision.color.Color`.
        """
        return cls(color.red, color.green, color.blue, color.alpha.value)

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
    def from_api_repr(cls, color_information):
        """Factory: construct ``ColorInformation`` for a color.

        :type color_information: dict
        :param color_information: Color data with extra meta information.

        :rtype: :class:`~google.cloud.vision.color.ColorInformation`
        :returns: Instance of ``ColorInformation``.
        """
        color = Color.from_api_repr(color_information.get('color', {}))
        score = color_information.get('score')
        pixel_fraction = color_information.get('pixelFraction')
        return cls(color, score, pixel_fraction)

    @classmethod
    def from_pb(cls, color_information):
        """Factory: construct ``ColorInformation`` for a color.

        :type color_information: :class:`~google.cloud.vision_v1.proto.\
                                 image_annotator_pb2.ColorInfo`
        :param color_information: Color data with extra meta information.

        :rtype: :class:`~google.cloud.vision.color.ColorInformation`
        :returns: Instance of ``ColorInformation``.
        """
        color = Color.from_pb(color_information.color)
        score = color_information.score
        pixel_fraction = color_information.pixel_fraction
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
