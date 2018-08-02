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

"""Define classes that describe external data sources.

   These are used for both Table.externalDataConfiguration and
   Job.configuration.query.tableDefinitions.
"""

from __future__ import absolute_import

import base64
import copy

from google.cloud.bigquery._helpers import _to_bytes
from google.cloud.bigquery._helpers import _bytes_to_json
from google.cloud.bigquery._helpers import _int_or_none
from google.cloud.bigquery.schema import SchemaField


class ExternalSourceFormat(object):
    """The format for external data files.

    Note that the set of allowed values for external data sources is different
    than the set used for loading data (see
    :class:`~google.cloud.bigquery.job.SourceFormat`).
    """

    CSV = 'CSV'
    """Specifies CSV format."""

    GOOGLE_SHEETS = 'GOOGLE_SHEETS'
    """Specifies Google Sheets format."""

    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    """Specifies newline delimited JSON format."""

    AVRO = 'AVRO'
    """Specifies Avro format."""

    DATASTORE_BACKUP = 'DATASTORE_BACKUP'
    """Specifies datastore backup format"""

    BIGTABLE = 'BIGTABLE'
    """Specifies Bigtable format."""


class BigtableColumn(object):
    """Options for a Bigtable column."""

    def __init__(self):
        self._properties = {}

    @property
    def encoding(self):
        """str: The encoding of the values when the type is not `STRING`

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.%28key%29.bigtableOptions.columnFamilies.columns.encoding
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.encoding
        """
        return self._properties.get('encoding')

    @encoding.setter
    def encoding(self, value):
        self._properties['encoding'] = value

    @property
    def field_name(self):
        """str: An identifier to use if the qualifier is not a valid BigQuery
        field identifier

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.%28key%29.bigtableOptions.columnFamilies.columns.fieldName
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.fieldName
        """
        return self._properties.get('fieldName')

    @field_name.setter
    def field_name(self, value):
        self._properties['fieldName'] = value

    @property
    def only_read_latest(self):
        """bool: If this is set, only the latest version of value in this
        column are exposed.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.%28key%29.bigtableOptions.columnFamilies.columns.onlyReadLatest
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.onlyReadLatest
        """
        return self._properties.get('onlyReadLatest')

    @only_read_latest.setter
    def only_read_latest(self, value):
        self._properties['onlyReadLatest'] = value

    @property
    def qualifier_encoded(self):
        """Union[str, bytes]: The qualifier encoded in binary.

        The type is ``str`` (Python 2.x) or ``bytes`` (Python 3.x). The module
        will handle base64 encoding for you.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.%28key%29.bigtableOptions.columnFamilies.columns.qualifierEncoded
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.qualifierEncoded
        """
        prop = self._properties.get('qualifierEncoded')
        if prop is None:
            return None
        return base64.standard_b64decode(_to_bytes(prop))

    @qualifier_encoded.setter
    def qualifier_encoded(self, value):
        self._properties['qualifierEncoded'] = _bytes_to_json(value)

    @property
    def qualifier_string(self):
        """str: A valid UTF-8 string qualifier

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.%28key%29.bigtableOptions.columnFamilies.columns.qualifierEncoded
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.qualifierEncoded
        """
        return self._properties.get('qualifierString')

    @qualifier_string.setter
    def qualifier_string(self, value):
        self._properties['qualifierString'] = value

    @property
    def type_(self):
        """str: The type to convert the value in cells of this column.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.%28key%29.bigtableOptions.columnFamilies.columns.type
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.type
        """
        return self._properties.get('type')

    @type_.setter
    def type_(self, value):
        self._properties['type'] = value

    def to_api_repr(self):
        """Build an API representation of this object.

        Returns:
            Dict[str, Any]:
                A dictionary in the format used by the BigQuery API.
        """
        return copy.deepcopy(self._properties)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a :class:`~.external_config.BigtableColumn`
        instance given its API representation.

        Args:
            resource (Dict[str, Any]):
                Definition of a :class:`~.external_config.BigtableColumn`
                instance in the same representation as is returned from the
                API.

        Returns:
            :class:`~.external_config.BigtableColumn`:
                Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config


class BigtableColumnFamily(object):
    """Options for a Bigtable column family."""

    def __init__(self):
        self._properties = {}

    @property
    def encoding(self):
        """str: The encoding of the values when the type is not `STRING`

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.encoding
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.encoding
        """
        return self._properties.get('encoding')

    @encoding.setter
    def encoding(self, value):
        self._properties['encoding'] = value

    @property
    def family_id(self):
        """str: Identifier of the column family.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.familyId
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.familyId
        """
        return self._properties.get('familyId')

    @family_id.setter
    def family_id(self, value):
        self._properties['familyId'] = value

    @property
    def only_read_latest(self):
        """bool: If this is set only the latest version of value are exposed
        for all columns in this column family.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.onlyReadLatest
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.onlyReadLatest
        """
        return self._properties.get('onlyReadLatest')

    @only_read_latest.setter
    def only_read_latest(self, value):
        self._properties['onlyReadLatest'] = value

    @property
    def type_(self):
        """str: The type to convert the value in cells of this column family.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.type
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.type
        """
        return self._properties.get('type')

    @type_.setter
    def type_(self, value):
        self._properties['type'] = value

    @property
    def columns(self):
        """List[:class:`~.external_config.BigtableColumn`]: Lists of columns
        that should be exposed as individual fields.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.columns
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns
        """
        prop = self._properties.get('columns', [])
        return [BigtableColumn.from_api_repr(col) for col in prop]

    @columns.setter
    def columns(self, value):
        self._properties['columns'] = [col.to_api_repr() for col in value]

    def to_api_repr(self):
        """Build an API representation of this object.

        Returns:
            Dict[str, Any]:
                A dictionary in the format used by the BigQuery API.
        """
        return copy.deepcopy(self._properties)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a :class:`~.external_config.BigtableColumnFamily`
        instance given its API representation.

        Args:
            resource (Dict[str, Any]):
                Definition of a :class:`~.external_config.BigtableColumnFamily`
                instance in the same representation as is returned from the
                API.

        Returns:
            :class:`~.external_config.BigtableColumnFamily`:
                Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config


class BigtableOptions(object):
    """Options that describe how to treat Bigtable tables as BigQuery tables.
    """

    _SOURCE_FORMAT = 'BIGTABLE'
    _RESOURCE_NAME = 'bigtableOptions'

    def __init__(self):
        self._properties = {}

    @property
    def ignore_unspecified_column_families(self):
        """bool: If :data:`True`, ignore columns not specified in
        :attr:`column_families` list. Defaults to :data:`False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.ignoreUnspecifiedColumnFamilies
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.ignoreUnspecifiedColumnFamilies
        """
        return self._properties.get('ignoreUnspecifiedColumnFamilies')

    @ignore_unspecified_column_families.setter
    def ignore_unspecified_column_families(self, value):
        self._properties['ignoreUnspecifiedColumnFamilies'] = value

    @property
    def read_rowkey_as_string(self):
        """bool: If :data:`True`, rowkey column families will be read and
        converted to string. Defaults to :data:`False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.readRowkeyAsString
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.readRowkeyAsString
        """
        return self._properties.get('readRowkeyAsString')

    @read_rowkey_as_string.setter
    def read_rowkey_as_string(self, value):
        self._properties['readRowkeyAsString'] = value

    @property
    def column_families(self):
        """List[:class:`~.external_config.BigtableColumnFamily`]: List of
        column families to expose in the table schema along with their types.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies
        """
        prop = self._properties.get('columnFamilies', [])
        return [BigtableColumnFamily.from_api_repr(cf) for cf in prop]

    @column_families.setter
    def column_families(self, value):
        self._properties['columnFamilies'] = [cf.to_api_repr() for cf in value]

    def to_api_repr(self):
        """Build an API representation of this object.

        Returns:
            Dict[str, Any]:
                A dictionary in the format used by the BigQuery API.
        """
        return copy.deepcopy(self._properties)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a :class:`~.external_config.BigtableOptions`
        instance given its API representation.

        Args:
            resource (Dict[str, Any]):
                Definition of a :class:`~.external_config.BigtableOptions`
                instance in the same representation as is returned from the
                API.

        Returns:
            :class:`~.external_config.BigtableOptions`:
                Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config


class CSVOptions(object):
    """Options that describe how to treat CSV files as BigQuery tables."""

    _SOURCE_FORMAT = 'CSV'
    _RESOURCE_NAME = 'csvOptions'

    def __init__(self):
        self._properties = {}

    @property
    def allow_jagged_rows(self):
        """bool: If :data:`True`, BigQuery treats missing trailing columns as
        null values. Defaults to :data:`False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.allowJaggedRows
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.allowJaggedRows
        """
        return self._properties.get('allowJaggedRows')

    @allow_jagged_rows.setter
    def allow_jagged_rows(self, value):
        self._properties['allowJaggedRows'] = value

    @property
    def allow_quoted_newlines(self):
        """bool: If :data:`True`, quoted data sections that contain newline
        characters in a CSV file are allowed. Defaults to :data:`False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.allowQuotedNewlines
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.allowQuotedNewlines
        """
        return self._properties.get('allowQuotedNewlines')

    @allow_quoted_newlines.setter
    def allow_quoted_newlines(self, value):
        self._properties['allowQuotedNewlines'] = value

    @property
    def encoding(self):
        """str: The character encoding of the data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.encoding
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.encoding
        """
        return self._properties.get('encoding')

    @encoding.setter
    def encoding(self, value):
        self._properties['encoding'] = value

    @property
    def field_delimiter(self):
        """str: The separator for fields in a CSV file. Defaults to comma (',').

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.fieldDelimiter
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.fieldDelimiter
        """
        return self._properties.get('fieldDelimiter')

    @field_delimiter.setter
    def field_delimiter(self, value):
        self._properties['fieldDelimiter'] = value

    @property
    def quote_character(self):
        """str: The value that is used to quote data sections in a CSV file.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.quote
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.quote
        """
        return self._properties.get('quote')

    @quote_character.setter
    def quote_character(self, value):
        self._properties['quote'] = value

    @property
    def skip_leading_rows(self):
        """int: The number of rows at the top of a CSV file.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.skipLeadingRows
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.skipLeadingRows
        """
        return _int_or_none(self._properties.get('skipLeadingRows'))

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        self._properties['skipLeadingRows'] = str(value)

    def to_api_repr(self):
        """Build an API representation of this object.

        Returns:
            Dict[str, Any]:
                A dictionary in the format used by the BigQuery API.
        """
        return copy.deepcopy(self._properties)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a :class:`~.external_config.CSVOptions` instance
        given its API representation.

        Args:
            resource (Dict[str, Any]):
                Definition of a :class:`~.external_config.CSVOptions`
                instance in the same representation as is returned from the
                API.

        Returns:
            :class:`~.external_config.CSVOptions`:
                Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config


class GoogleSheetsOptions(object):
    """Options that describe how to treat Google Sheets as BigQuery tables."""

    _SOURCE_FORMAT = 'GOOGLE_SHEETS'
    _RESOURCE_NAME = 'googleSheetsOptions'

    def __init__(self):
        self._properties = {}

    @property
    def skip_leading_rows(self):
        """int: The number of rows at the top of a sheet that BigQuery will
        skip when reading the data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).googleSheetsOptions.skipLeadingRows
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.googleSheetsOptions.skipLeadingRows
        """
        return _int_or_none(self._properties.get('skipLeadingRows'))

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        self._properties['skipLeadingRows'] = str(value)

    def to_api_repr(self):
        """Build an API representation of this object.

        Returns:
            Dict[str, Any]:
                A dictionary in the format used by the BigQuery API.
        """
        return copy.deepcopy(self._properties)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a :class:`~.external_config.GoogleSheetsOptions`
        instance given its API representation.

        Args:
            resource (Dict[str, Any]):
                Definition of a :class:`~.external_config.GoogleSheetsOptions`
                instance in the same representation as is returned from the
                API.

        Returns:
            :class:`~.external_config.GoogleSheetsOptions`:
                Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config


_OPTION_CLASSES = (BigtableOptions, CSVOptions, GoogleSheetsOptions)


class ExternalConfig(object):
    """Description of an external data source.

    Args:
        source_format (:class:`~.external_config.ExternalSourceFormat`):
            See :attr:`source_format`.
    """

    def __init__(self, source_format):
        self._properties = {'sourceFormat': source_format}
        self._options = None
        for optcls in _OPTION_CLASSES:
            if source_format == optcls._SOURCE_FORMAT:
                self._options = optcls()
                break

    @property
    def source_format(self):
        """:class:`~.external_config.ExternalSourceFormat`:
        Format of external source.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.sourceFormat
        """
        return self._properties['sourceFormat']

    @property
    def options(self):
        """Dict[str, Any]: Source-specific options."""
        return self._options

    @property
    def autodetect(self):
        """bool: If :data:`True`, try to detect schema and format options
        automatically.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).autodetect
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.autodetect
        """
        return self._properties.get('autodetect')

    @autodetect.setter
    def autodetect(self, value):
        self._properties['autodetect'] = value

    @property
    def compression(self):
        """str: The compression type of the data source.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).compression
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.compression
        """
        return self._properties.get('compression')

    @compression.setter
    def compression(self, value):
        self._properties['compression'] = value

    @property
    def ignore_unknown_values(self):
        """bool: If :data:`True`, extra values that are not represented in the
        table schema are ignored. Defaults to :data:`False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).ignoreUnknownValues
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.ignoreUnknownValues
        """
        return self._properties.get('ignoreUnknownValues')

    @ignore_unknown_values.setter
    def ignore_unknown_values(self, value):
        self._properties['ignoreUnknownValues'] = value

    @property
    def max_bad_records(self):
        """int: The maximum number of bad records that BigQuery can ignore when
        reading data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).maxBadRecords
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.maxBadRecords
        """
        return self._properties.get('maxBadRecords')

    @max_bad_records.setter
    def max_bad_records(self, value):
        self._properties['maxBadRecords'] = value

    @property
    def source_uris(self):
        """List[str]: URIs that point to your data in Google Cloud.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).sourceUris
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.sourceUris
        """
        return self._properties.get('sourceUris', [])

    @source_uris.setter
    def source_uris(self, value):
        self._properties['sourceUris'] = value

    @property
    def schema(self):
        """List[:class:`~google.cloud.bigquery.schema.SchemaField`]: The schema
        for the data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).schema
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.schema
        """
        prop = self._properties.get('schema', {})
        return [SchemaField.from_api_repr(field)
                for field in prop.get('fields', [])]

    @schema.setter
    def schema(self, value):
        prop = value
        if value is not None:
            prop = {'fields': [field.to_api_repr() for field in value]}
        self._properties['schema'] = prop

    def to_api_repr(self):
        """Build an API representation of this object.

        Returns:
            Dict[str, Any]:
                A dictionary in the format used by the BigQuery API.
        """
        config = copy.deepcopy(self._properties)
        if self.options is not None:
            r = self.options.to_api_repr()
            if r != {}:
                config[self.options._RESOURCE_NAME] = r
        return config

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct an :class:`~.external_config.ExternalConfig`
        instance given its API representation.

        Args:
            resource (Dict[str, Any]):
                Definition of an :class:`~.external_config.ExternalConfig`
                instance in the same representation as is returned from the
                API.

        Returns:
            :class:`~.external_config.ExternalConfig`:
                Configuration parsed from ``resource``.
        """
        config = cls(resource['sourceFormat'])
        for optcls in _OPTION_CLASSES:
            opts = resource.get(optcls._RESOURCE_NAME)
            if opts is not None:
                config._options = optcls.from_api_repr(opts)
                break
        config._properties = copy.deepcopy(resource)
        return config
