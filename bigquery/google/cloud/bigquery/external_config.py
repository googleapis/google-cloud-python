# Copyright 2017 Google Inc.
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
from google.cloud.bigquery._helpers import _TypedApiResourceProperty
from google.cloud.bigquery._helpers import _ListApiResourceProperty
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.table import _build_schema_resource
from google.cloud.bigquery.table import _parse_schema_resource
from google.cloud.bigquery.job import _int_or_none


class ExternalConfig(object):
    """Description of an external data source."""

    def __init__(self):
        self._properties = {}
        self._options = None
        self._schema = None

    autodetect = _TypedApiResourceProperty(
        'autodetect', 'autodetect', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).autodetect
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.autodetect
    """

    compression = _TypedApiResourceProperty(
        'compression', 'compression', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).compression
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.compression
    """

    ignore_unknown_values = _TypedApiResourceProperty(
        'ignore_unknown_values', 'ignoreUnknownValues', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).ignoreUnknownValues
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.ignoreUnknownValues
    """

    max_bad_records = _TypedApiResourceProperty(
        'max_bad_records', 'maxBadRecords', six.integer_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).maxBadRecords
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.maxBadRecords
    """

    source_format = _TypedApiResourceProperty(
        'source_format', 'sourceFormat', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).sourceFormat
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.sourceFormat
    """

    source_uris = _ListApiResourceProperty(
        'source_uris', 'sourceUris', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).sourceUris
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.sourceUris
    """

    @property
    def schema(self):
        """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).schema
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.schema
        """
        return self._schema

    @schema.setter
    def schema(self, value):
        if not all(isinstance(field, SchemaField) for field in value):
            raise ValueError('Schema items must be fields')
        self._schema = value

    @property
    def options(self):
        """Source-specific options. A subclass of ExternalConfigOptions."""
        return self._options

    @options.setter
    def options(self, value):
        # TODO: check that subclass is compatible with source_format.
        self._options = value

    def to_api_repr(self):
        """Build an API representation of this object.

        :rtype: dict
        :returns: A dictionary in the format used by the BigQuery API.
        """
        config = copy.deepcopy(self._properties)
        if self.schema is not None:
            config['schema'] = {'fields': _build_schema_resource(self.schema)}
        if self.options is not None:
            config[self.options._RESOURCE_NAME] = self.options.to_api_repr()
        return config

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct a CSVOptions given its API representation

        :type resource: dict
        :param resource:
            An extract job configuration in the same representation as is
            returned from the API.

        :rtype: :class:`google.cloud.bigquery.external_config.CSVOptions`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        schema = resource.pop('schema', None)
        if schema:
            config.schema = _parse_schema_resource(schema)
        for optcls in (BigtableOptions, CSVOptions, GoogleSheetsOptions):
            opts = resource.pop(optcls._RESOURCE_NAME, None)
            if opts is not None:
                config.options = optcls.from_api_repr(opts)
                break
        config._properties = copy.deepcopy(resource)
        return config


class BigtableColumn(object):
    """Options for a Bigtable column."""

    def __init__(self):
        self._properties = {}

    encoding = _TypedApiResourceProperty(
        'encoding', 'encoding', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.columns.encoding
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.encoding
    """

    field_name = _TypedApiResourceProperty(
        'field_name', 'fieldName', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.columns.field_name
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.field_name
    """

    only_read_latest = _TypedApiResourceProperty(
        'only_read_latest', 'onlyReadLatest', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.columns.only_read_latest
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.only_read_latest
    """

    qualifier_encoded = _TypedApiResourceProperty(
        'qualifier_encoded', 'qualifierEncoded', six.binary_type)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.columns.qualifier_encoded
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.qualifier_encoded
    """

    qualifier_string = _TypedApiResourceProperty(
        'qualifier_string', 'qualifierString', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.columns.qualifier_string
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.qualifier_string
    """

    type = _TypedApiResourceProperty('type', 'type', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.columns.type
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns.type
    """

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

        :rtype: :class:`google.cloud.bigquery.external_config.BigtableColumn`
        :returns: Configuration parsed from ``resource``.
        """
        qe = resource.pop('qualifierEncoded', None)
        config = cls()
        config._properties = copy.deepcopy(resource)
        if qe:
            config.qualifier_encoded = base64.standard_b64decode(_to_bytes(qe))
        return config


class BigtableColumnFamily(object):
    """Options for a Bigtable column family."""

    def __init__(self):
        self._properties = {}

    encoding = _TypedApiResourceProperty(
        'encoding', 'encoding', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.encoding
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.encoding
    """

    family_id = _TypedApiResourceProperty(
        'family_id', 'familyId', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.familyId
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.familyId
    """

    only_read_latest = _TypedApiResourceProperty(
        'only_read_latest', 'onlyReadLatest', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.onlyReadLatest
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.onlyReadLatest
    """

    type = _TypedApiResourceProperty('type', 'type', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.type
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.type
    """

    columns = _ListApiResourceProperty(
        'columns', 'columns', BigtableColumn)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies.columns
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies.columns
    """

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
            :class:`google.cloud.bigquery.external_config.BigtableColumnFamily`
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

    _RESOURCE_NAME = 'bigtableOptions'

    def __init__(self):
        self._properties = {}

    ignore_unspecified_column_families = _TypedApiResourceProperty(
        'ignore_unspecified_column_families',
        'ignoreUnspecifiedColumnFamilies', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.ignoreUnspecifiedColumnFamilies
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.ignoreUnspecifiedColumnFamilies
    """

    read_rowkey_as_string = _TypedApiResourceProperty(
        'read_rowkey_as_string', 'readRowkeyAsString', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.readRowkeyAsString
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.readRowkeyAsString
    """

    column_families = _ListApiResourceProperty(
        'column_families', 'columnFamilies', BigtableColumnFamily)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).bigtableOptions.columnFamilies
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.bigtableOptions.columnFamilies
    """

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

        :rtype: :class:`google.cloud.bigquery.external_config.BigtableOptions`
        :returns: Configuration parsed from ``resource``.
        """
        config = cls()
        config._properties = copy.deepcopy(resource)
        config.column_families = [BigtableColumnFamily.from_api_repr(cf)
                                  for cf in resource['columnFamilies']]
        return config


class CSVOptions(object):
    """Options that describe how to treat CSV files as BigQuery tables."""

    _RESOURCE_NAME = 'csvOptions'

    def __init__(self):
        self._properties = {}

    allow_jagged_rows = _TypedApiResourceProperty(
        'allow_jagged_rows', 'allowJaggedRows', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.allowJaggedRows
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.allowJaggedRows
    """

    allow_quoted_newlines = _TypedApiResourceProperty(
        'allow_quoted_newlines', 'allowQuotedNewlines', bool)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.allowQuotedNewlines
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.allowQuotedNewlines
    """

    encoding = _TypedApiResourceProperty(
        'encoding', 'encoding', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.encoding
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.encoding
    """

    field_delimiter = _TypedApiResourceProperty(
        'field_delimiter', 'fieldDelimiter', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.fieldDelimiter
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.fieldDelimiter
    """

    quote_character = _TypedApiResourceProperty(
        'quote_character', 'quote', six.string_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.quote
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.quote
    """

    skip_leading_rows = _TypedApiResourceProperty(
        'skip_leading_rows', 'skipLeadingRows', six.integer_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).csvOptions.skipLeadingRows
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.csvOptions.skipLeadingRows
    """

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

        :rtype: :class:`google.cloud.bigquery.external_config.CSVOptions`
        :returns: Configuration parsed from ``resource``.
        """
        slr = resource.pop('skipLeadingRows', None)
        config = cls()
        config._properties = copy.deepcopy(resource)
        config.skip_leading_rows = _int_or_none(slr)
        return config


class GoogleSheetsOptions(object):
    """Options that describe how to treat Google Sheets as BigQuery tables."""

    _RESOURCE_NAME = 'googleSheetsOptions'

    def __init__(self):
        self._properties = {}

    skip_leading_rows = _TypedApiResourceProperty(
        'skip_leading_rows', 'skipLeadingRows', six.integer_types)
    """See
    https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.query.tableDefinitions.(key).googleSheetsOptions.skipLeadingRows
    https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#externalDataConfiguration.googleSheetsOptions.skipLeadingRows
    """

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
            :class:`google.cloud.bigquery.external_config.GoogleSheetsOptions`
        :returns: Configuration parsed from ``resource``.
        """
        slr = resource.pop('skipLeadingRows', None)
        config = cls()
        config._properties = copy.deepcopy(resource)
        config.skip_leading_rows = _int_or_none(slr)
        return config
