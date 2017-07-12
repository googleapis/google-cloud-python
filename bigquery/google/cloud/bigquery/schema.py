# Copyright 2015 Google Inc.
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

"""Schemas for BigQuery tables / queries."""


class SchemaField(object):
    """Describe a single field within a table schema.

    :type name: str
    :param name: the name of the field.

    :type field_type: str
    :param field_type: the type of the field (one of 'STRING', 'INTEGER',
                       'FLOAT', 'BOOLEAN', 'TIMESTAMP' or 'RECORD').

    :type mode: str
    :param mode: the type of the field (one of 'NULLABLE', 'REQUIRED',
                 or 'REPEATED').

    :type description: str
    :param description: optional description for the field.

    :type fields: list of :class:`SchemaField`, or None
    :param fields: subfields (requires ``field_type`` of 'RECORD').
    """
    def __init__(self, name, field_type, mode='NULLABLE', description=None,
                 fields=None):
        self.name = name
        self.field_type = field_type
        self.mode = mode
        self.description = description
        self.fields = None if(fields is None) else tuple(fields)

    def _key(self):
        """
        A tuple describing the contents of this :class:`SchemaField`.
        Used to compute this instance's hashcode and evaluate equality.
        """
        return (
            self.name,
            self.field_type.lower(),
            self.mode,
            self.description,
            self.fields)

    def __eq__(self, other):
        return self._key() == other._key()

    def __hash__(self):
        return hash(self._key())
