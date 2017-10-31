# Copyright 2017, Google LLC All rights reserved.
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

from __future__ import absolute_import


def add_single_feature_methods(cls):
    """Custom decorator intended for :class:`~vision.helpers.VisionHelpers`.

    This metaclass adds a `{feature}` method for every feature
    defined on the Feature enum.
    """
    # Sanity check: This only makes sense if we are building the GAPIC
    # subclass and have enums already attached.
    if not hasattr(cls, 'enums'):
        return cls

    # Iterate over the Feature.Type enum and add get a list of
    # features which will receive single-feature detection methods.
    features = [k for k in cls.enums.Feature.Type.__dict__.keys()
                if k.replace('_', '').isalpha() and k.upper() == k]

    # Add each single-feature method to the class.
    for feature in features:
        # Sanity check: Do not make a method for the falsy feature.
        if feature == 'TYPE_UNSPECIFIED':
            continue

        # Assign the appropriate metadata to the function.
        detect = _create_single_feature_method(feature, cls.enums.Feature.Type)

        # Assign a qualified name to the function, and perform module
        # replacement on the docstring.
        detect.__qualname__ = '{cls}.{name}'.format(
            cls=cls.__name__,
            name=detect.__name__,
        )
        detect.__doc__ = detect.__doc__.format(
            module=cls.__module__,
        )

        # Place the function on the class being created.
        setattr(cls, detect.__name__, detect)

    # Done; return the class.
    return cls


def _create_single_feature_method(feature, enum):
    """Return a function that will detect a single feature.

    Args:
        feature (str): A specific feature defined as an attribute on
            :class:`~enums.Feature.Type`.
        enum (class): The :class:`~enums.Feature.Type` class.

    Returns:
        function: A helper function to detect just that feature.
    """
    # Define the function properties.
    fx_name = feature.lower()
    if 'detection' in fx_name:
        fx_doc = 'Perform {0}.'.format(fx_name.replace('_', ' '))
    else:
        fx_doc = 'Return {desc} information.'.format(
            desc=fx_name.replace('_', ' '),
        )

    # Provide a complete docstring with argument and return value
    # information.
    fx_doc += """

    Args:
        image (:class:`~.{module}.types.Image`): The image to analyze.
        options (:class:`google.gax.CallOptions`): Overrides the
            default settings for this call, e.g, timeout, retries, etc.
        kwargs (dict): Additional properties to be set on the
            :class:`~.{module}.types.AnnotateImageRequest`.

    Returns:
        :class:`~.{module}.types.AnnotateImageResponse`: The API response.
    """

    # Get the actual feature value to send.
    feature_value = {'type': enum.__dict__[feature]}

    # Define the function to be returned.
    def inner(self, image, options=None, **kwargs):
        """Return a single feature annotation for the given image.

        Intended for use with functools.partial, to create the particular
        single-feature methods.
        """
        request = dict(
            image=image,
            features=[feature_value],
            **kwargs
        )
        return self.annotate_image(request, options=options)

    # Set the appropriate function metadata.
    inner.__name__ = fx_name
    inner.__doc__ = fx_doc

    # Return the final function.
    return inner
