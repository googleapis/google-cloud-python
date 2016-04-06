# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Label Descriptors for the `Google Monitoring API (V3)`_.

.. _Google Monitoring API (V3):
    https://cloud.google.com/monitoring/api/ref_v3/rest/v3/LabelDescriptor
"""

import collections


class LabelValueType(object):
    """Allowed values for the `type of a label`_.

    .. _type of a label:
        https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
        LabelDescriptor#ValueType
    """

    STRING = 'STRING'
    BOOL = 'BOOL'
    INT64 = 'INT64'


class LabelDescriptor(collections.namedtuple('LabelDescriptor',
                                             'key value_type description')):
    """Schema specification and documentation for a single label.

    :type key: string
    :param key: The name of the label.

    :type value_type: string
    :param value_type: The type of the label. It must be one of ``"STRING"``,
                       ``"BOOL"``, or ``"INT64"``.

    :type description: string
    :param description: A human-readable description for the label.
    """
    __slots__ = ()

    @classmethod
    def _from_dict(cls, info):
        """Construct a label descriptor from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`LabelDescriptor`
        :returns: A label descriptor.
        """
        return cls(
            info.get('key', ''),
            info.get('valueType', LabelValueType.STRING),
            info.get('description', ''),
        )
