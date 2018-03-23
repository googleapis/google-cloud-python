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

import six

from google.cloud.bigquery._helpers import _to_bytes
from google.cloud.bigquery._helpers import _bytes_to_json
from google.cloud.bigquery.table import _build_schema_resource
from google.cloud.bigquery.table import _parse_schema_resource


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
        prop = self._properties.get('encoding')
        return prop

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
        prop = self._properties.get('fieldName')
        return prop

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
        prop = self._properties.get('onlyReadLatest')
        return prop

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
        return prop

    @qualifier_encoded.setter
    def qualifier_encoded(self, value):
        self._properties['qualifierEncoded'] = six.binary_type(value)

    @property
    def qualifier_string(self):
        """str: A valid UTF-8 string qualifier

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.%28key%29.bigtableOptions.columnFamilies.columns.qualifierEncoded
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.qualifierEncoded
        """
        prop = self._properties.get('qualifierString')
        return prop

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
        prop = self._properties.get('type')
        return prop

    @type_.setter
    def type_(self, value):
        self._properties['type'] = value

    def to_api_repr(self):
        """Build an API representation of this object.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        config = copy.deepcopy(self._properties)
        qe = config.get('qualifierEncoded')
        if qe is not None:
            config['qualifierEncoded'] = _bytes_to_json(qe)
        return config

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a BigtableColumn given its API representation

        :type resource: dict
        :param resource:
            A column in the same representation as is returned from the API.

        :rtype: :class:`~google.cloud.bigquery.BigtableColumn`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        qe = resource.get('qualifierEncoded')
        if qe:
            config.qualifier_encoded = base64.standard_b64decode(_to_bytes(qe))
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
        prop = self._properties.get('encoding')
        return prop

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
        prop = self._properties.get('familyId')
        return prop

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
        prop = self._properties.get('onlyReadLatest')
        return prop

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
        prop = self._properties.get('type')
        return prop

    @type_.setter
    def type_(self, value):
        self._properties['type'] = value

    @property
    def columns(self):
        """List[google.cloud.bigquery.external_config.BigtableColumn]: Lists of
        columns that should be exposed as individual fields

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.columns
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns
        """
        prop = self._properties.get('columns', [])
        return prop

    @columns.setter
    def columns(self, value):
        self._properties['columns'] = value

    def to_api_repr(self):
        """Build an API representation of this object.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        config = copy.deepcopy(self._properties)
        config['columns'] = [c.to_api_repr() for c in config['columns']]
        return config

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a BigtableColumnFamily given its
           API representation

        :type resource: dict
        :param resource:
            A column family in the same representation as is returned
            from the API.

        :rtype:
            :class:`~google.cloud.bigquery.external_config.BigtableColumnFamily`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        config.columns = [BigtableColumn.from_api_repr(c)
                          for c in resource['columns']]
        return config


class BigtableOptions(object):
    """Options that describe how to treat Bigtable tables
       as BigQuery tables."""

    _SOURCE_FORMAT = 'BIGTABLE'
    _RESOURCE_NAME = 'bigtableOptions'

    def __init__(self):
        self._properties = {}

    @property
    def ignore_unspecified_column_families(self):
        """bool: If `True`, ignore columns not specified in columnFamilies
        list. Defaults to `False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.ignoreUnspecifiedColumnFamilies
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.ignoreUnspecifiedColumnFamilies
        """
        prop = self._properties.get('ignoreUnspecifiedColumnFamilies')
        return prop

    @ignore_unspecified_column_families.setter
    def ignore_unspecified_column_families(self, value):
        self._properties['ignoreUnspecifiedColumnFamilies'] = value

    @property
    def read_rowkey_as_string(self):
        """bool: If `True`, rowkey column families will be read and converted
        to string. Defaults to `False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.readRowkeyAsString
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.readRowkeyAsString
        """
        prop = self._properties.get('readRowkeyAsString')
        return prop

    @read_rowkey_as_string.setter
    def read_rowkey_as_string(self, value):
        self._properties['readRowkeyAsString'] = value

    @property
    def column_families(self):
        """List[google.cloud.bigquery.external_config.BigtableColumnFamily]:
        List of column families to expose in the table schema along with their
        types.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies
        """
        prop = self._properties.get('columnFamilies', [])
        return prop

    @column_families.setter
    def column_families(self, value):
        self._properties['columnFamilies'] = value

    def to_api_repr(self):
        """Build an API representation of this object.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        config = copy.deepcopy(self._properties)
        config['columnFamilies'] = [cf.to_api_repr()
                                    for cf in config['columnFamilies']]
        return config

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a BigtableOptions given its API representation

        :type resource: dict
        :param resource:
            A BigtableOptions in the same representation as is returned
            from the API.

        :rtype:
            :class:`~google.cloud.bigquery.external_config.BigtableOptions`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        config.column_families = [BigtableColumnFamily.from_api_repr(cf)
                                  for cf in resource['columnFamilies']]
        return config


class CSVOptions(object):
    """Options that describe how to treat CSV files as BigQuery tables."""

    _SOURCE_FORMAT = 'CSV'
    _RESOURCE_NAME = 'csvOptions'

    def __init__(self):
        self._properties = {}

    @property
    def allow_jagged_rows(self):
        """bool: If `True`, BigQuery treats missing trailing columns as null
        values. Defaults to `False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.allowJaggedRows
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.allowJaggedRows
        """
        prop = self._properties.get('allowJaggedRows')
        return prop

    @allow_jagged_rows.setter
    def allow_jagged_rows(self, value):
        self._properties['allowJaggedRows'] = value

    @property
    def allow_quoted_newlines(self):
        """bool: If `True`, quoted data sections that contain newline
        characters in a CSV file are allowed. Defaults to `False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.allowQuotedNewlines
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.allowQuotedNewlines
        """
        prop = self._properties.get('allowQuotedNewlines')
        return prop

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
        prop = self._properties.get('encoding')
        return prop

    @encoding.setter
    def encoding(self, value):
        self._properties['encoding'] = value

    @property
    def field_delimiter(self):
        """str: The separator for fields in a CSV file. Defaults a comma (',').

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.fieldDelimiter
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.fieldDelimiter
        """
        prop = self._properties.get('fieldDelimiter')
        return prop

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
        prop = self._properties.get('quote')
        return prop

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
        prop = self._properties.get('skipLeadingRows')
        if prop is not None:
            prop = int(prop)
        return prop

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        self._properties['skipLeadingRows'] = str(value)

    def to_api_repr(self):
        """Build an API representation of this object.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        config = copy.deepcopy(self._properties)
        slr = config.pop('skipLeadingRows', None)
        if slr is not None:
            config['skipLeadingRows'] = str(slr)
        return config

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a CSVOptions given its API representation

        :type resource: dict
        :param resource:
            A CSVOptions in the same representation as is
            returned from the API.

        :rtype: :class:`~google.cloud.bigquery.external_config.CSVOptions`
        :returns: Configuration parsed from ``resource``.
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
        prop = self._properties.get('skipLeadingRows')
        if prop is not None:
            prop = int(prop)
        return prop

    @skip_leading_rows.setter
    def skip_leading_rows(self, value):
        self._properties['skipLeadingRows'] = str(value)

    def to_api_repr(self):
        """Build an API representation of this object.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        config = copy.deepcopy(self._properties)
        slr = config.pop('skipLeadingRows', None)
        if slr is not None:
            config['skipLeadingRows'] = str(slr)
        return config

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a GoogleSheetsOptions given its API representation

        :type resource: dict
        :param resource:
            An GoogleSheetsOptions in the same representation as is
            returned from the API.

        :rtype:
            :class:`~google.cloud.bigquery.external_config.GoogleSheetsOptions`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        return config


_OPTION_CLASSES = (BigtableOptions, CSVOptions, GoogleSheetsOptions)


class ExternalConfig(object):
    """Description of an external data source.

    :type source_format: str
    :param source_format: the format of the external data. See
                          the ``source_format`` property on this class.
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
        """See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).sourceFormat
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.sourceFormat
        """
        return self._properties['sourceFormat']

    @property
    def options(self):
        """Source-specific options."""
        return self._options

    @property
    def autodetect(self):
        """bool: If `True`, try to detect schema and format options
        automatically.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).autodetect
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.autodetect
        """
        prop = self._properties.get('autodetect')
        return prop

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
        prop = self._properties.get('compression')
        return prop

    @compression.setter
    def compression(self, value):
        self._properties['compression'] = value

    @property
    def ignore_unknown_values(self):
        """bool: If `True`, extra values that are not represented in the table
        schema are ignored. Defaults to `False`.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).ignoreUnknownValues
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.ignoreUnknownValues
        """
        prop = self._properties.get('ignoreUnknownValues')
        return prop

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
        prop = self._properties.get('maxBadRecords')
        return prop

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
        prop = self._properties.get('sourceUris', [])
        return prop

    @source_uris.setter
    def source_uris(self, value):
        self._properties['sourceUris'] = value

    @property
    def schema(self):
        """List[google.cloud.bigquery.schema.SchemaField]: The schema for the
        data.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).schema
        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.schema
        """
        prop = self._properties.get('schema', [])
        return prop

    @schema.setter
    def schema(self, value):
        self._properties['schema'] = value

    def to_api_repr(self):
        """Build an API representation of this object.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        config = copy.deepcopy(self._properties)
        if self.schema:
            config['schema'] = {'fields': _build_schema_resource(self.schema)}
        if self.options is not None:
            r = self.options.to_api_repr()
            if r != {}:
                config[self.options._RESOURCE_NAME] = r
        return config

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a CSVOptions given its API representation

        :type resource: dict
        :param resource:
            An extract job configuration in the same representation as is
            returned from the API.

        :rtype: :class:`~google.cloud.bigquery.external_config.CSVOptions`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls(resource['sourceFormat'])
        schema = resource.get('schema')
        for optcls in _OPTION_CLASSES:
            opts = resource.get(optcls._RESOURCE_NAME)
            if opts is not None:
                config._options = optcls.from_api_repr(opts)
                break
        config._properties = copy.deepcopy(resource)
        if schema:
            config.schema = _parse_schema_resource(schema)
        return config
