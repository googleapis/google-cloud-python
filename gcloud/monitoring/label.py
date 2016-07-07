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


class LabelValueType(object):
    """Allowed values for the `type of a label`_.

    .. _type of a label:
        https://cloud.google.com/monitoring/api/ref_v3/rest/v3/\
        LabelDescriptor#ValueType
    """

    STRING = 'STRING'
    BOOL = 'BOOL'
    INT64 = 'INT64'


class LabelDescriptor(object):
    """Schema specification and documentation for a single label.

    :type key: string
    :param key: The name of the label.

    :type value_type: string
    :param value_type:
        The type of the label. It must be one of :data:`LabelValueType.STRING`,
        :data:`LabelValueType.BOOL`, or :data:`LabelValueType.INT64`.
        See :class:`LabelValueType`.

    :type description: string
    :param description: A human-readable description for the label.
    """

    def __init__(self, key, value_type=LabelValueType.STRING, description=''):
        self.key = key
        self.value_type = value_type
        self.description = description

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
            info['key'],
            info.get('valueType', LabelValueType.STRING),
            info.get('description', ''),
        )

    def _to_dict(self):
        """Build a dictionary ready to be serialized to the JSON wire format.

        :rtype: dict
        :returns: A dictionary.
        """
        info = {
            'key': self.key,
            'valueType': self.value_type,
        }

        if self.description:
            info['description'] = self.description

        return info

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __repr__(self):
        return (
            'LabelDescriptor(key={key!r}, value_type={value_type!r},'
            ' description={description!r})'
        ).format(**self.__dict__)
