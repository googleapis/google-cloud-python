# Copyright 2017, Google Inc. All rights reserved.
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
import sys


class VisionHelpersMeta(type):
    """Custom metaclass intended for :class:`~vision.helpers.VisionHelpers`.

    This metaclass adds a `detect_{feature}` method for every feature
    defined on the Feature enum.
    """
    def __new__(mcls, name, bases, attrs):
        cls = super(VisionHelpersMeta, mcls).__new__(mcls, name, bases, attrs)

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

            # Define the function properties.
            fx_name = feature.lower()
            fx_qualname = '{cls}.{name}'.format(cls=cls.__name__, name=fx_name)
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
                image (:class:`~{module}.Image`): The image to analyze.
                options (:class:`google.gax.CallOptions`): Overrides the
                    default settings for this call, e.g, timeout, retries, etc.

            Returns:
                :class:`~{module}.AnnotateImageResponse`: The API response.
            """.format(module=cls.__module__ + '.image_annotator')

            # Create the single feature function.
            def detect_single_feature(self, image, options=None):
                request = {
                    'image': image,
                    'features': [self.enums.Feature.Type.__dict__[feature]],
                }
                return self.annotate_image(request, options=options)

            # Assign the appropriate metadata to the function.
            detect_single_feature.__name__ = fx_name
            detect_single_feature.__qualname__ = fx_qualname
            detect_single_feature.__doc__ = fx_doc

            # Place the function on the class being created.
            setattr(cls, fx_name, detect_single_feature)

        # Done; return the class.
        return cls
