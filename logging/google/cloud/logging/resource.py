# Copyright 2017 Google LLC
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

"""Monitored Resource for the Google Logging API V2."""

import collections


class Resource(collections.namedtuple('Resource', 'type labels')):
    """A monitored resource identified by specifying values for all labels.

    :type type: str
    :param type: The resource type name.

    :type labels: dict
    :param labels: A mapping from label names to values for all labels
                   enumerated in the associated :class:`ResourceDescriptor`.
    """
    __slots__ = ()

    @classmethod
    def _from_dict(cls, info):
        """Construct a resource object from the parsed JSON representation.

        :type info: dict
        :param info:
            A ``dict`` parsed from the JSON wire-format representation.

        :rtype: :class:`Resource`
        :returns: A resource object.
        """
        return cls(
            type=info['type'],
            labels=info.get('labels', {}),
        )

    def _to_dict(self):
        """Build a dictionary ready to be serialized to the JSON format.

        :rtype: dict
        :returns: A dict representation of the object that can be written to
                  the API.
        """
        return {
            'type': self.type,
            'labels': self.labels,
        }
