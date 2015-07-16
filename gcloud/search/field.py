# Copyright 2015 Google Inc. All rights reserved.
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

"""Define Search Field."""


from gcloud.search.value import Value


class Field(object):
    """Fields store data which makes up a document.

    See:
    https://cloud.google.com/search/reference/rest/google/cloudsearch/v1/FieldValueList

    :type name: string
    :param name: the name of the field

    :type values: iterable of string or ``None``
    :param values: the list of values to be associated with this field.
    """
    def __init__(self, name, values=None):
        self.name = name
        self.values = values or []

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a field given its API representation

        :type resource: dict
        :param resource: the resource representation returned from the API

        :rtype: :class:`gcloud.search.field.Field`
        :returns: Field parsed from ``resource``.
        """
        return cls(name=resource['name'])

    def add_value(self, value, tokenization=None):
        """Add a value to this field.

        :type value: string
        :param value: The value to add to the field.

        :type tokenization: string
        :param tokenization: The tokenization type of the value.
        """
        self.values.append(Value(value=value,
                                 tokenization=tokenization))
