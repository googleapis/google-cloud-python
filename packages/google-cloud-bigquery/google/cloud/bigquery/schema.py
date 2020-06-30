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

from six.moves import collections_abc

from google.cloud.bigquery_v2 import types


_STRUCT_TYPES = ("RECORD", "STRUCT")

# SQL types reference:
# https://cloud.google.com/bigquery/data-types#legacy_sql_data_types
# https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
LEGACY_TO_STANDARD_TYPES = {
    "STRING": types.StandardSqlDataType.STRING,
    "BYTES": types.StandardSqlDataType.BYTES,
    "INTEGER": types.StandardSqlDataType.INT64,
    "INT64": types.StandardSqlDataType.INT64,
    "FLOAT": types.StandardSqlDataType.FLOAT64,
    "FLOAT64": types.StandardSqlDataType.FLOAT64,
    "NUMERIC": types.StandardSqlDataType.NUMERIC,
    "BOOLEAN": types.StandardSqlDataType.BOOL,
    "BOOL": types.StandardSqlDataType.BOOL,
    "GEOGRAPHY": types.StandardSqlDataType.GEOGRAPHY,
    "RECORD": types.StandardSqlDataType.STRUCT,
    "STRUCT": types.StandardSqlDataType.STRUCT,
    "TIMESTAMP": types.StandardSqlDataType.TIMESTAMP,
    "DATE": types.StandardSqlDataType.DATE,
    "TIME": types.StandardSqlDataType.TIME,
    "DATETIME": types.StandardSqlDataType.DATETIME,
    # no direct conversion from ARRAY, the latter is represented by mode="REPEATED"
}
"""String names of the legacy SQL types to integer codes of Standard SQL types."""


class SchemaField(object):
    """Describe a single field within a table schema.

    Args:
        name (str): The name of the field.

        field_type (str): The type of the field. See
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.type

        mode (Optional[str]): The mode of the field.  See
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.mode

        description (Optional[str]): Description for the field.

        fields (Optional[Tuple[google.cloud.bigquery.schema.SchemaField]]):
            Subfields (requires ``field_type`` of 'RECORD').

        policy_tags (Optional[PolicyTagList]): The policy tag list for the field.

    """

    def __init__(
        self,
        name,
        field_type,
        mode="NULLABLE",
        description=None,
        fields=(),
        policy_tags=None,
    ):
        self._name = name
        self._field_type = field_type
        self._mode = mode
        self._description = description
        self._fields = tuple(fields)
        self._policy_tags = policy_tags

    @classmethod
    def from_api_repr(cls, api_repr):
        """Return a ``SchemaField`` object deserialized from a dictionary.

        Args:
            api_repr (Mapping[str, str]): The serialized representation
                of the SchemaField, such as what is output by
                :meth:`to_api_repr`.

        Returns:
            google.cloud.biquery.schema.SchemaField: The ``SchemaField`` object.
        """
        # Handle optional properties with default values
        mode = api_repr.get("mode", "NULLABLE")
        description = api_repr.get("description")
        fields = api_repr.get("fields", ())

        return cls(
            field_type=api_repr["type"].upper(),
            fields=[cls.from_api_repr(f) for f in fields],
            mode=mode.upper(),
            description=description,
            name=api_repr["name"],
            policy_tags=PolicyTagList.from_api_repr(api_repr.get("policyTags")),
        )

    @property
    def name(self):
        """str: The name of the field."""
        return self._name

    @property
    def field_type(self):
        """str: The type of the field.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.type
        """
        return self._field_type

    @property
    def mode(self):
        """Optional[str]: The mode of the field.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.mode
        """
        return self._mode

    @property
    def is_nullable(self):
        """bool: whether 'mode' is 'nullable'."""
        return self._mode == "NULLABLE"

    @property
    def description(self):
        """Optional[str]: description for the field."""
        return self._description

    @property
    def fields(self):
        """Optional[tuple]: Subfields contained in this field.

        Must be empty unset if ``field_type`` is not 'RECORD'.
        """
        return self._fields

    @property
    def policy_tags(self):
        """Optional[google.cloud.bigquery.schema.PolicyTagList]: Policy tag list
        definition for this field.
        """
        return self._policy_tags

    def to_api_repr(self):
        """Return a dictionary representing this schema field.

        Returns:
            Dict: A dictionary representing the SchemaField in a serialized form.
        """
        # Put together the basic representation. See http://bit.ly/2hOAT5u.
        answer = {
            "mode": self.mode.upper(),
            "name": self.name,
            "type": self.field_type.upper(),
            "description": self.description,
        }

        # If this is a RECORD type, then sub-fields are also included,
        # add this to the serialized representation.
        if self.field_type.upper() in _STRUCT_TYPES:
            answer["fields"] = [f.to_api_repr() for f in self.fields]

        # If this contains a policy tag definition, include that as well:
        if self.policy_tags is not None:
            answer["policyTags"] = self.policy_tags.to_api_repr()

        # Done; return the serialized dictionary.
        return answer

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            Tuple: The contents of this :class:`~google.cloud.bigquery.schema.SchemaField`.
        """
        return (
            self._name,
            self._field_type.upper(),
            self._mode.upper(),
            self._description,
            self._fields,
            self._policy_tags,
        )

    def to_standard_sql(self):
        """Return the field as the standard SQL field representation object.

        Returns:
            An instance of :class:`~google.cloud.bigquery_v2.types.StandardSqlField`.
        """
        sql_type = types.StandardSqlDataType()

        if self.mode == "REPEATED":
            sql_type.type_kind = types.StandardSqlDataType.ARRAY
        else:
            sql_type.type_kind = LEGACY_TO_STANDARD_TYPES.get(
                self.field_type, types.StandardSqlDataType.TYPE_KIND_UNSPECIFIED
            )

        if sql_type.type_kind == types.StandardSqlDataType.ARRAY:  # noqa: E721
            array_element_type = LEGACY_TO_STANDARD_TYPES.get(
                self.field_type, types.StandardSqlDataType.TYPE_KIND_UNSPECIFIED
            )
            sql_type.array_element_type.type_kind = array_element_type

            # ARRAY cannot directly contain other arrays, only scalar types and STRUCTs
            # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#array-type
            if array_element_type == types.StandardSqlDataType.STRUCT:  # noqa: E721
                sql_type.array_element_type.struct_type.fields.extend(
                    field.to_standard_sql() for field in self.fields
                )

        elif sql_type.type_kind == types.StandardSqlDataType.STRUCT:  # noqa: E721
            sql_type.struct_type.fields.extend(
                field.to_standard_sql() for field in self.fields
            )

        return types.StandardSqlField(name=self.name, type=sql_type)

    def __eq__(self, other):
        if not isinstance(other, SchemaField):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return "SchemaField{}".format(self._key())


def _parse_schema_resource(info):
    """Parse a resource fragment into a schema field.

    Args:
        info: (Mapping[str, Dict]): should contain a "fields" key to be parsed

    Returns:
        Optional[Sequence[google.cloud.bigquery.schema.SchemaField`]:
            A list of parsed fields, or ``None`` if no "fields" key found.
    """
    if "fields" not in info:
        return ()

    schema = []
    for r_field in info["fields"]:
        name = r_field["name"]
        field_type = r_field["type"]
        mode = r_field.get("mode", "NULLABLE")
        description = r_field.get("description")
        sub_fields = _parse_schema_resource(r_field)
        policy_tags = PolicyTagList.from_api_repr(r_field.get("policyTags"))
        schema.append(
            SchemaField(name, field_type, mode, description, sub_fields, policy_tags)
        )
    return schema


def _build_schema_resource(fields):
    """Generate a resource fragment for a schema.

    Args:
        fields (Sequence[google.cloud.bigquery.schema.SchemaField): schema to be dumped.

    Returns:
        Sequence[Dict]: Mappings describing the schema of the supplied fields.
    """
    return [field.to_api_repr() for field in fields]


def _to_schema_fields(schema):
    """Coerce `schema` to a list of schema field instances.

    Args:
        schema(Sequence[Union[ \
            :class:`~google.cloud.bigquery.schema.SchemaField`, \
            Mapping[str, Any] \
        ]]):
            Table schema to convert. If some items are passed as mappings,
            their content must be compatible with
            :meth:`~google.cloud.bigquery.schema.SchemaField.from_api_repr`.

    Returns:
        Sequence[:class:`~google.cloud.bigquery.schema.SchemaField`]

    Raises:
        Exception: If ``schema`` is not a sequence, or if any item in the
        sequence is not a :class:`~google.cloud.bigquery.schema.SchemaField`
        instance or a compatible mapping representation of the field.
    """
    for field in schema:
        if not isinstance(field, (SchemaField, collections_abc.Mapping)):
            raise ValueError(
                "Schema items must either be fields or compatible "
                "mapping representations."
            )

    return [
        field if isinstance(field, SchemaField) else SchemaField.from_api_repr(field)
        for field in schema
    ]


class PolicyTagList(object):
    """Define Policy Tags for a column.

    Args:
        names (
            Optional[Tuple[str]]): list of policy tags to associate with
            the column.  Policy tag identifiers are of the form
            `projects/*/locations/*/taxonomies/*/policyTags/*`.
    """

    def __init__(self, names=()):
        self._properties = {}
        self._properties["names"] = tuple(names)

    @property
    def names(self):
        """Tuple[str]: Policy tags associated with this definition.
        """
        return self._properties.get("names", ())

    def _key(self):
        """A tuple key that uniquely describes this PolicyTagList.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            Tuple: The contents of this :class:`~google.cloud.bigquery.schema.PolicyTagList`.
        """
        return tuple(sorted(self._properties.items()))

    def __eq__(self, other):
        if not isinstance(other, PolicyTagList):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return "PolicyTagList{}".format(self._key())

    @classmethod
    def from_api_repr(cls, api_repr):
        """Return a :class:`PolicyTagList` object deserialized from a dict.

        This method creates a new ``PolicyTagList`` instance that points to
        the ``api_repr`` parameter as its internal properties dict. This means
        that when a ``PolicyTagList`` instance is stored as a property of
        another object, any changes made at the higher level will also appear
        here.

        Args:
            api_repr (Mapping[str, str]):
                The serialized representation of the PolicyTagList, such as
                what is output by :meth:`to_api_repr`.

        Returns:
            Optional[google.cloud.bigquery.schema.PolicyTagList]:
                The ``PolicyTagList`` object or None.
        """
        if api_repr is None:
            return None
        names = api_repr.get("names", ())
        return cls(names=names)

    def to_api_repr(self):
        """Return a dictionary representing this object.

        This method returns the properties dict of the ``PolicyTagList``
        instance rather than making a copy. This means that when a
        ``PolicyTagList`` instance is stored as a property of another
        object, any changes made at the higher level will also appear here.

        Returns:
            dict:
                A dictionary representing the PolicyTagList object in
                serialized form.
        """
        answer = {"names": [name for name in self.names]}
        return answer
