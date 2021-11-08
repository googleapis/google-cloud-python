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

import collections
import enum
from typing import Any, Dict, Iterable, Union

from google.cloud.bigquery_v2 import types


_STRUCT_TYPES = ("RECORD", "STRUCT")

# SQL types reference:
# https://cloud.google.com/bigquery/data-types#legacy_sql_data_types
# https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
LEGACY_TO_STANDARD_TYPES = {
    "STRING": types.StandardSqlDataType.TypeKind.STRING,
    "BYTES": types.StandardSqlDataType.TypeKind.BYTES,
    "INTEGER": types.StandardSqlDataType.TypeKind.INT64,
    "INT64": types.StandardSqlDataType.TypeKind.INT64,
    "FLOAT": types.StandardSqlDataType.TypeKind.FLOAT64,
    "FLOAT64": types.StandardSqlDataType.TypeKind.FLOAT64,
    "NUMERIC": types.StandardSqlDataType.TypeKind.NUMERIC,
    "BIGNUMERIC": types.StandardSqlDataType.TypeKind.BIGNUMERIC,
    "BOOLEAN": types.StandardSqlDataType.TypeKind.BOOL,
    "BOOL": types.StandardSqlDataType.TypeKind.BOOL,
    "GEOGRAPHY": types.StandardSqlDataType.TypeKind.GEOGRAPHY,
    "RECORD": types.StandardSqlDataType.TypeKind.STRUCT,
    "STRUCT": types.StandardSqlDataType.TypeKind.STRUCT,
    "TIMESTAMP": types.StandardSqlDataType.TypeKind.TIMESTAMP,
    "DATE": types.StandardSqlDataType.TypeKind.DATE,
    "TIME": types.StandardSqlDataType.TypeKind.TIME,
    "DATETIME": types.StandardSqlDataType.TypeKind.DATETIME,
    # no direct conversion from ARRAY, the latter is represented by mode="REPEATED"
}
"""String names of the legacy SQL types to integer codes of Standard SQL types."""


class _DefaultSentinel(enum.Enum):
    """Object used as 'sentinel' indicating default value should be used.

    Uses enum so that pytype/mypy knows that this is the only possible value.
    https://stackoverflow.com/a/60605919/101923

    Literal[_DEFAULT_VALUE] is an alternative, but only added in Python 3.8.
    https://docs.python.org/3/library/typing.html#typing.Literal
    """

    DEFAULT_VALUE = object()


_DEFAULT_VALUE = _DefaultSentinel.DEFAULT_VALUE


class SchemaField(object):
    """Describe a single field within a table schema.

    Args:
        name: The name of the field.

        field_type:
            The type of the field. See
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.type

        mode:
            Defaults to ``'NULLABLE'``. The mode of the field. See
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.mode

        description: Description for the field.

        fields: Subfields (requires ``field_type`` of 'RECORD').

        policy_tags: The policy tag list for the field.

        precision:
            Precison (number of digits) of fields with NUMERIC or BIGNUMERIC type.

        scale:
            Scale (digits after decimal) of fields with NUMERIC or BIGNUMERIC type.

        max_length: Maximum length of fields with STRING or BYTES type.
    """

    def __init__(
        self,
        name: str,
        field_type: str,
        mode: str = "NULLABLE",
        description: Union[str, _DefaultSentinel] = _DEFAULT_VALUE,
        fields: Iterable["SchemaField"] = (),
        policy_tags: Union["PolicyTagList", None, _DefaultSentinel] = _DEFAULT_VALUE,
        precision: Union[int, _DefaultSentinel] = _DEFAULT_VALUE,
        scale: Union[int, _DefaultSentinel] = _DEFAULT_VALUE,
        max_length: Union[int, _DefaultSentinel] = _DEFAULT_VALUE,
    ):
        self._properties: Dict[str, Any] = {
            "name": name,
            "type": field_type,
        }
        if mode is not None:
            self._properties["mode"] = mode.upper()
        if description is not _DEFAULT_VALUE:
            self._properties["description"] = description
        if precision is not _DEFAULT_VALUE:
            self._properties["precision"] = precision
        if scale is not _DEFAULT_VALUE:
            self._properties["scale"] = scale
        if max_length is not _DEFAULT_VALUE:
            self._properties["maxLength"] = max_length
        if policy_tags is not _DEFAULT_VALUE:
            self._properties["policyTags"] = (
                policy_tags.to_api_repr() if policy_tags is not None else None
            )
        self._fields = tuple(fields)

    @staticmethod
    def __get_int(api_repr, name):
        v = api_repr.get(name, _DEFAULT_VALUE)
        if v is not _DEFAULT_VALUE:
            v = int(v)
        return v

    @classmethod
    def from_api_repr(cls, api_repr: dict) -> "SchemaField":
        """Return a ``SchemaField`` object deserialized from a dictionary.

        Args:
            api_repr (Mapping[str, str]): The serialized representation
                of the SchemaField, such as what is output by
                :meth:`to_api_repr`.

        Returns:
            google.cloud.biquery.schema.SchemaField: The ``SchemaField`` object.
        """
        field_type = api_repr["type"].upper()

        # Handle optional properties with default values
        mode = api_repr.get("mode", "NULLABLE")
        description = api_repr.get("description", _DEFAULT_VALUE)
        fields = api_repr.get("fields", ())
        policy_tags = api_repr.get("policyTags", _DEFAULT_VALUE)

        if policy_tags is not None and policy_tags is not _DEFAULT_VALUE:
            policy_tags = PolicyTagList.from_api_repr(policy_tags)

        return cls(
            field_type=field_type,
            fields=[cls.from_api_repr(f) for f in fields],
            mode=mode.upper(),
            description=description,
            name=api_repr["name"],
            policy_tags=policy_tags,
            precision=cls.__get_int(api_repr, "precision"),
            scale=cls.__get_int(api_repr, "scale"),
            max_length=cls.__get_int(api_repr, "maxLength"),
        )

    @property
    def name(self):
        """str: The name of the field."""
        return self._properties["name"]

    @property
    def field_type(self):
        """str: The type of the field.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.type
        """
        return self._properties["type"]

    @property
    def mode(self):
        """Optional[str]: The mode of the field.

        See:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.mode
        """
        return self._properties.get("mode")

    @property
    def is_nullable(self):
        """bool: whether 'mode' is 'nullable'."""
        return self.mode == "NULLABLE"

    @property
    def description(self):
        """Optional[str]: description for the field."""
        return self._properties.get("description")

    @property
    def precision(self):
        """Optional[int]: Precision (number of digits) for the NUMERIC field."""
        return self._properties.get("precision")

    @property
    def scale(self):
        """Optional[int]: Scale (digits after decimal) for the NUMERIC field."""
        return self._properties.get("scale")

    @property
    def max_length(self):
        """Optional[int]: Maximum length for the STRING or BYTES field."""
        return self._properties.get("maxLength")

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
        resource = self._properties.get("policyTags")
        return PolicyTagList.from_api_repr(resource) if resource is not None else None

    def to_api_repr(self) -> dict:
        """Return a dictionary representing this schema field.

        Returns:
            Dict: A dictionary representing the SchemaField in a serialized form.
        """
        answer = self._properties.copy()

        # If this is a RECORD type, then sub-fields are also included,
        # add this to the serialized representation.
        if self.field_type.upper() in _STRUCT_TYPES:
            answer["fields"] = [f.to_api_repr() for f in self.fields]

        # Done; return the serialized dictionary.
        return answer

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            Tuple: The contents of this :class:`~google.cloud.bigquery.schema.SchemaField`.
        """
        field_type = self.field_type.upper()
        if field_type == "STRING" or field_type == "BYTES":
            if self.max_length is not None:
                field_type = f"{field_type}({self.max_length})"
        elif field_type.endswith("NUMERIC"):
            if self.precision is not None:
                if self.scale is not None:
                    field_type = f"{field_type}({self.precision}, {self.scale})"
                else:
                    field_type = f"{field_type}({self.precision})"

        policy_tags = (
            None if self.policy_tags is None else tuple(sorted(self.policy_tags.names))
        )

        return (
            self.name,
            field_type,
            # Mode is always str, if not given it defaults to a str value
            self.mode.upper(),  # pytype: disable=attribute-error
            self.description,
            self._fields,
            policy_tags,
        )

    def to_standard_sql(self) -> types.StandardSqlField:
        """Return the field as the standard SQL field representation object.

        Returns:
            An instance of :class:`~google.cloud.bigquery_v2.types.StandardSqlField`.
        """
        sql_type = types.StandardSqlDataType()

        if self.mode == "REPEATED":
            sql_type.type_kind = types.StandardSqlDataType.TypeKind.ARRAY
        else:
            sql_type.type_kind = LEGACY_TO_STANDARD_TYPES.get(
                self.field_type,
                types.StandardSqlDataType.TypeKind.TYPE_KIND_UNSPECIFIED,
            )

        if sql_type.type_kind == types.StandardSqlDataType.TypeKind.ARRAY:  # noqa: E721
            array_element_type = LEGACY_TO_STANDARD_TYPES.get(
                self.field_type,
                types.StandardSqlDataType.TypeKind.TYPE_KIND_UNSPECIFIED,
            )
            sql_type.array_element_type.type_kind = array_element_type

            # ARRAY cannot directly contain other arrays, only scalar types and STRUCTs
            # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#array-type
            if (
                array_element_type
                == types.StandardSqlDataType.TypeKind.STRUCT  # noqa: E721
            ):
                sql_type.array_element_type.struct_type.fields.extend(
                    field.to_standard_sql() for field in self.fields
                )

        elif (
            sql_type.type_kind
            == types.StandardSqlDataType.TypeKind.STRUCT  # noqa: E721
        ):
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
        key = self._key()
        policy_tags = key[-1]
        policy_tags_inst = None if policy_tags is None else PolicyTagList(policy_tags)
        adjusted_key = key[:-1] + (policy_tags_inst,)
        return f"{self.__class__.__name__}{adjusted_key}"


def _parse_schema_resource(info):
    """Parse a resource fragment into a schema field.

    Args:
        info: (Mapping[str, Dict]): should contain a "fields" key to be parsed

    Returns:
        Optional[Sequence[google.cloud.bigquery.schema.SchemaField`]:
            A list of parsed fields, or ``None`` if no "fields" key found.
    """
    return [SchemaField.from_api_repr(f) for f in info.get("fields", ())]


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
        if not isinstance(field, (SchemaField, collections.abc.Mapping)):
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

    def __init__(self, names: Iterable[str] = ()):
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
        return tuple(sorted(self._properties.get("names", ())))

    def __eq__(self, other):
        if not isinstance(other, PolicyTagList):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return f"{self.__class__.__name__}(names={self._key()})"

    @classmethod
    def from_api_repr(cls, api_repr: dict) -> "PolicyTagList":
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

    def to_api_repr(self) -> dict:
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
        answer = {"names": list(self.names)}
        return answer
