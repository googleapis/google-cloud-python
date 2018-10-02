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

    Args:
        name (str): the name of the field.

        field_type (str): the type of the field. See
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#schema.fields.type

        mode (str): the mode of the field.  See
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#schema.fields.mode

        description (Optional[str]):description for the field.

        fields (Tuple[:class:`~google.cloud.bigquery.schema.SchemaField`]):
            subfields (requires ``field_type`` of 'RECORD').
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
        # Handle optional properties with default values
        mode = api_repr.get('mode', 'NULLABLE')
        description = api_repr.get('description')
        fields = api_repr.get('fields', ())
        return cls(
            field_type=api_repr['type'].upper(),
            fields=[cls.from_api_repr(f) for f in fields],
            mode=mode.upper(),
            description=description,
            name=api_repr['name'],
        )

    @property
    def name(self):
        """str: The name of the field."""
        return self._name

    @property
    def field_type(self):
        """str: The type of the field.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#schema.fields.type
        """
        return self._field_type

    @property
    def mode(self):
        """str: The mode of the field.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#schema.fields.mode
        """
        return self._mode

    @property
    def is_nullable(self):
        """bool: whether 'mode' is 'nullable'."""
        return self._mode == 'NULLABLE'

    @property
    def description(self):
        """Optional[str]: description for the field."""
        return self._description

    @property
    def fields(self):
        """tuple: Subfields contained in this field.

        Must be empty unset if ``field_type`` is not 'RECORD'.
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
            'mode': self.mode.upper(),
            'name': self.name,
            'type': self.field_type.upper(),
            'description': self.description,
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
            self._field_type.upper(),
            self._mode.upper(),
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

    Args:
        info: (Mapping[str->dict]): should contain a "fields" key to be parsed

    Returns:
        (Union[Sequence[:class:`google.cloud.bigquery.schema.SchemaField`],None])
            a list of parsed fields, or ``None`` if no "fields" key found.
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

    Args:
        fields [Sequence[:class:`~google.cloud.bigquery.schema.SchemaField`]):
            schema to be dumped

    Returns: (Sequence[dict])
        mappings describing the schema of the supplied fields.
    """
    return [field.to_api_repr() for field in fields]
