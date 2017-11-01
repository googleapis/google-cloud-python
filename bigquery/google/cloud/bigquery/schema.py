# Copyright 2015 Google LLC
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
    :param mode: the mode of the field (one of 'NULLABLE', 'REQUIRED',
                 or 'REPEATED').

    :type description: str
    :param description: optional description for the field.

    :type fields: tuple of :class:`~google.cloud.bigquery.schema.SchemaField`
    :param fields: subfields (requires ``field_type`` of 'RECORD').
    """
    def __init__(self, name, field_type, mode='NULLABLE',
                 description=None, fields=()):
        self._name = name
        self._field_type = field_type
        self._mode = mode
        self._description = description
        self._fields = tuple(fields)

    @classmethod
    def from_api_repr(cls, api_repr):
        """Return a ``SchemaField`` object deserialized from a dictionary.

        Args:
            api_repr (Mapping[str, str]): The serialized representation
                of the SchemaField, such as what is output by
                :meth:`to_api_repr`.

        Returns:
            google.cloud.biquery.schema.SchemaField:
                The ``SchemaField`` object.
        """
        return cls(
            field_type=api_repr['type'].upper(),
            fields=[cls.from_api_repr(f) for f in api_repr.get('fields', ())],
            mode=api_repr['mode'].upper(),
            name=api_repr['name'],
        )

    @property
    def name(self):
        """str: The name of the field."""
        return self._name

    @property
    def field_type(self):
        """str: The type of the field.

        Will be one of 'STRING', 'INTEGER', 'FLOAT', 'BOOLEAN',
        'TIMESTAMP' or 'RECORD'.
        """
        return self._field_type

    @property
    def mode(self):
        """str: The mode of the field.

        Will be one of 'NULLABLE', 'REQUIRED', or 'REPEATED'.
        """
        return self._mode

    @property
    def is_nullable(self):
        """Check whether 'mode' is 'nullable'."""
        return self._mode == 'NULLABLE'

    @property
    def description(self):
        """Optional[str]: Description for the field."""
        return self._description

    @property
    def fields(self):
        """tuple: Subfields contained in this field.

        If ``field_type`` is not 'RECORD', this property must be
        empty / unset.
        """
        return self._fields

    def to_api_repr(self):
        """Return a dictionary representing this schema field.

        Returns:
            dict: A dictionary representing the SchemaField in a serialized
                form.
        """
        # Put together the basic representation. See http://bit.ly/2hOAT5u.
        answer = {
            'mode': self.mode.lower(),
            'name': self.name,
            'type': self.field_type.lower(),
        }

        # If this is a RECORD type, then sub-fields are also included,
        # add this to the serialized representation.
        if self.field_type.upper() == 'RECORD':
            answer['fields'] = [f.to_api_repr() for f in self.fields]

        # Done; return the serialized dictionary.
        return answer

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            tuple: The contents of this
                   :class:`~google.cloud.bigquery.schema.SchemaField`.
        """
        return (
            self._name,
            self._field_type.lower(),
            self._mode,
            self._description,
            self._fields,
        )

    def __eq__(self, other):
        if not isinstance(other, SchemaField):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return 'SchemaField{}'.format(self._key())


def _parse_schema_resource(info):
    """Parse a resource fragment into a schema field.

    :type info: mapping
    :param info: should contain a "fields" key to be parsed

    :rtype:
        list of :class:`google.cloud.bigquery.schema.SchemaField`, or
        ``NoneType``
    :returns: a list of parsed fields, or ``None`` if no "fields" key is
                present in ``info``.
    """
    if 'fields' not in info:
        return ()

    schema = []
    for r_field in info['fields']:
        name = r_field['name']
        field_type = r_field['type']
        mode = r_field.get('mode', 'NULLABLE')
        description = r_field.get('description')
        sub_fields = _parse_schema_resource(r_field)
        schema.append(
            SchemaField(name, field_type, mode, description, sub_fields))
    return schema


def _build_schema_resource(fields):
    """Generate a resource fragment for a schema.

    :type fields:
        sequence of :class:`~google.cloud.bigquery.schema.SchemaField`
    :param fields: schema to be dumped

    :rtype: mapping
    :returns: a mapping describing the schema of the supplied fields.
    """
    infos = []
    for field in fields:
        info = {'name': field.name,
                'type': field.field_type,
                'mode': field.mode}
        if field.description is not None:
            info['description'] = field.description
        if field.fields:
            info['fields'] = _build_schema_resource(field.fields)
        infos.append(info)
    return infos
