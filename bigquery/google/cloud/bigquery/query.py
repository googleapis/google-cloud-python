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

"""BigQuery query processing."""

from collections import OrderedDict
import copy

from google.cloud.bigquery.table import _parse_schema_resource
from google.cloud.bigquery._helpers import _rows_from_json
from google.cloud.bigquery._helpers import _QUERY_PARAMS_FROM_JSON
from google.cloud.bigquery._helpers import _SCALAR_VALUE_TO_JSON_PARAM


class UDFResource(object):
    """Describe a single user-defined function (UDF) resource.

    Args:
        udf_type (str): the type of the resource ('inlineCode' or 'resourceUri')

        value (str): the inline code or resource URI.

    See
    https://cloud.google.com/bigquery/user-defined-functions#api
    """

    def __init__(self, udf_type, value):
        self.udf_type = udf_type
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, UDFResource):
            return NotImplemented
        return self.udf_type == other.udf_type and self.value == other.value

    def __ne__(self, other):
        return not self == other


class _AbstractQueryParameter(object):
    """Base class for named / positional query parameters.
    """

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct parameter from JSON resource.

        Args:
            resource (Dict): JSON mapping of parameter

        Returns:
            google.cloud.bigquery.query.ScalarQueryParameter
        """
        raise NotImplementedError

    def to_api_repr(self):
        """Construct JSON API representation for the parameter.

        Returns:
            Dict: JSON representation for the parameter.
        """
        raise NotImplementedError


class ScalarQueryParameter(_AbstractQueryParameter):
    """Named / positional query parameters for scalar values.

    Args:
        name (Optional[str]):
            Parameter name, used via ``@foo`` syntax.  If None, the
            parameter can only be addressed via position (``?``).

        type_ (str):
            name of parameter type.  One of 'STRING', 'INT64',
            'FLOAT64', 'NUMERIC', 'BOOL', 'TIMESTAMP', 'DATETIME', or
            'DATE'.

        value (Union[str, int, float, decimal.Decimal, bool,
                 datetime.datetime, datetime.date]): the scalar parameter value.
    """

    def __init__(self, name, type_, value):
        self.name = name
        self.type_ = type_
        self.value = value

    @classmethod
    def positional(cls, type_, value):
        """Factory for positional paramater.

        Args:
            type_ (str):
                name of parameter type.  One of 'STRING', 'INT64',
                'FLOAT64', 'NUMERIC', 'BOOL', 'TIMESTAMP', 'DATETIME', or
                'DATE'.

            value (Union[str, int, float, decimal.Decimal, bool,
                     datetime.datetime,
                     datetime.date]): the scalar parameter value.

        Returns:
            google.cloud.bigquery.query.ScalarQueryParameter: instance without name
        """
        return cls(None, type_, value)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct parameter from JSON resource.

        Args:
            resource (Dict): JSON mapping of parameter

        Returns:
            google.cloud.bigquery.query.ScalarQueryParameter: instance
        """
        name = resource.get("name")
        type_ = resource["parameterType"]["type"]

        # parameterValue might not be present if JSON resource originates
        # from the back-end - the latter omits it for None values.
        value = resource.get("parameterValue", {}).get("value")
        if value is not None:
            converted = _QUERY_PARAMS_FROM_JSON[type_](value, None)
        else:
            converted = None

        return cls(name, type_, converted)

    def to_api_repr(self):
        """Construct JSON API representation for the parameter.

        Returns:
            Dict: JSON mapping
        """
        value = self.value
        converter = _SCALAR_VALUE_TO_JSON_PARAM.get(self.type_)
        if converter is not None:
            value = converter(value)
        resource = {
            "parameterType": {"type": self.type_},
            "parameterValue": {"value": value},
        }
        if self.name is not None:
            resource["name"] = self.name
        return resource

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            Tuple: The contents of this :class:`~google.cloud.bigquery.query.ScalarQueryParameter`.
        """
        return (self.name, self.type_.upper(), self.value)

    def __eq__(self, other):
        if not isinstance(other, ScalarQueryParameter):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "ScalarQueryParameter{}".format(self._key())


class ArrayQueryParameter(_AbstractQueryParameter):
    """Named / positional query parameters for array values.

    Args:
        name (Optional[str]):
            Parameter name, used via ``@foo`` syntax.  If None, the
            parameter can only be addressed via position (``?``).

        array_type (str):
            name of type of array elements.  One of `'STRING'`, `'INT64'`,
            `'FLOAT64'`, `'NUMERIC'`, `'BOOL'`, `'TIMESTAMP'`, or `'DATE'`.

        values (List[appropriate scalar type]): the parameter array values.
    """

    def __init__(self, name, array_type, values):
        self.name = name
        self.array_type = array_type
        self.values = values

    @classmethod
    def positional(cls, array_type, values):
        """Factory for positional parameters.

        Args:
            array_type (str):
                name of type of array elements.  One of `'STRING'`, `'INT64'`,
                `'FLOAT64'`, `'NUMERIC'`, `'BOOL'`, `'TIMESTAMP'`, or `'DATE'`.

            values (List[appropriate scalar type]): the parameter array values.

        Returns:
            google.cloud.bigquery.query.ArrayQueryParameter: instance without name
        """
        return cls(None, array_type, values)

    @classmethod
    def _from_api_repr_struct(cls, resource):
        name = resource.get("name")
        converted = []
        # We need to flatten the array to use the StructQueryParameter
        # parse code.
        resource_template = {
            # The arrayType includes all the types of the fields of the STRUCT
            "parameterType": resource["parameterType"]["arrayType"]
        }
        for array_value in resource["parameterValue"]["arrayValues"]:
            struct_resource = copy.deepcopy(resource_template)
            struct_resource["parameterValue"] = array_value
            struct_value = StructQueryParameter.from_api_repr(struct_resource)
            converted.append(struct_value)
        return cls(name, "STRUCT", converted)

    @classmethod
    def _from_api_repr_scalar(cls, resource):
        name = resource.get("name")
        array_type = resource["parameterType"]["arrayType"]["type"]
        parameter_value = resource.get("parameterValue", {})
        array_values = parameter_value.get("arrayValues", ())
        values = [value["value"] for value in array_values]
        converted = [
            _QUERY_PARAMS_FROM_JSON[array_type](value, None) for value in values
        ]
        return cls(name, array_type, converted)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct parameter from JSON resource.

        Args:
            resource (Dict): JSON mapping of parameter

        Returns:
            google.cloud.bigquery.query.ArrayQueryParameter: instance
        """
        array_type = resource["parameterType"]["arrayType"]["type"]
        if array_type == "STRUCT":
            return cls._from_api_repr_struct(resource)
        return cls._from_api_repr_scalar(resource)

    def to_api_repr(self):
        """Construct JSON API representation for the parameter.

        Returns:
            Dict: JSON mapping
        """
        values = self.values
        if self.array_type == "RECORD" or self.array_type == "STRUCT":
            reprs = [value.to_api_repr() for value in values]
            a_type = reprs[0]["parameterType"]
            a_values = [repr_["parameterValue"] for repr_ in reprs]
        else:
            a_type = {"type": self.array_type}
            converter = _SCALAR_VALUE_TO_JSON_PARAM.get(self.array_type)
            if converter is not None:
                values = [converter(value) for value in values]
            a_values = [{"value": value} for value in values]
        resource = {
            "parameterType": {"type": "ARRAY", "arrayType": a_type},
            "parameterValue": {"arrayValues": a_values},
        }
        if self.name is not None:
            resource["name"] = self.name
        return resource

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            Tuple: The contents of this :class:`~google.cloud.bigquery.query.ArrayQueryParameter`.
        """
        return (self.name, self.array_type.upper(), self.values)

    def __eq__(self, other):
        if not isinstance(other, ArrayQueryParameter):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "ArrayQueryParameter{}".format(self._key())


class StructQueryParameter(_AbstractQueryParameter):
    """Named / positional query parameters for struct values.

    Args:
        name (Optional[str]):
            Parameter name, used via ``@foo`` syntax.  If None, the
            parameter can only be addressed via position (``?``).

        sub_params (Union[Tuple[
            google.cloud.bigquery.query.ScalarQueryParameter,
            google.cloud.bigquery.query.ArrayQueryParameter,
            google.cloud.bigquery.query.StructQueryParameter
        ]]): the sub-parameters for the struct
    """

    def __init__(self, name, *sub_params):
        self.name = name
        types = self.struct_types = OrderedDict()
        values = self.struct_values = {}
        for sub in sub_params:
            if isinstance(sub, self.__class__):
                types[sub.name] = "STRUCT"
                values[sub.name] = sub
            elif isinstance(sub, ArrayQueryParameter):
                types[sub.name] = "ARRAY"
                values[sub.name] = sub
            else:
                types[sub.name] = sub.type_
                values[sub.name] = sub.value

    @classmethod
    def positional(cls, *sub_params):
        """Factory for positional parameters.

        Args:
            sub_params (Union[Tuple[
                google.cloud.bigquery.query.ScalarQueryParameter,
                google.cloud.bigquery.query.ArrayQueryParameter,
                google.cloud.bigquery.query.StructQueryParameter
            ]]): the sub-parameters for the struct

        Returns:
            google.cloud.bigquery.query.StructQueryParameter: instance without name
        """
        return cls(None, *sub_params)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct parameter from JSON resource.

        Args:
            resource (Dict): JSON mapping of parameter

        Returns:
            google.cloud.bigquery.query.StructQueryParameter: instance
        """
        name = resource.get("name")
        instance = cls(name)
        type_resources = {}
        types = instance.struct_types
        for item in resource["parameterType"]["structTypes"]:
            types[item["name"]] = item["type"]["type"]
            type_resources[item["name"]] = item["type"]
        struct_values = resource["parameterValue"]["structValues"]
        for key, value in struct_values.items():
            type_ = types[key]
            converted = None
            if type_ == "STRUCT":
                struct_resource = {
                    "name": key,
                    "parameterType": type_resources[key],
                    "parameterValue": value,
                }
                converted = StructQueryParameter.from_api_repr(struct_resource)
            elif type_ == "ARRAY":
                struct_resource = {
                    "name": key,
                    "parameterType": type_resources[key],
                    "parameterValue": value,
                }
                converted = ArrayQueryParameter.from_api_repr(struct_resource)
            else:
                value = value["value"]
                converted = _QUERY_PARAMS_FROM_JSON[type_](value, None)
            instance.struct_values[key] = converted
        return instance

    def to_api_repr(self):
        """Construct JSON API representation for the parameter.

        Returns:
            Dict: JSON mapping
        """
        s_types = {}
        values = {}
        for name, value in self.struct_values.items():
            type_ = self.struct_types[name]
            if type_ in ("STRUCT", "ARRAY"):
                repr_ = value.to_api_repr()
                s_types[name] = {"name": name, "type": repr_["parameterType"]}
                values[name] = repr_["parameterValue"]
            else:
                s_types[name] = {"name": name, "type": {"type": type_}}
                converter = _SCALAR_VALUE_TO_JSON_PARAM.get(type_)
                if converter is not None:
                    value = converter(value)
                values[name] = {"value": value}

        resource = {
            "parameterType": {
                "type": "STRUCT",
                "structTypes": [s_types[key] for key in self.struct_types],
            },
            "parameterValue": {"structValues": values},
        }
        if self.name is not None:
            resource["name"] = self.name
        return resource

    def _key(self):
        """A tuple key that uniquely describes this field.

        Used to compute this instance's hashcode and evaluate equality.

        Returns:
            Tuple: The contents of this :class:`~google.cloud.biquery.ArrayQueryParameter`.
        """
        return (self.name, self.struct_types, self.struct_values)

    def __eq__(self, other):
        if not isinstance(other, StructQueryParameter):
            return NotImplemented
        return self._key() == other._key()

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "StructQueryParameter{}".format(self._key())


class _QueryResults(object):
    """Results of a query.

    See:
    https://g.co/cloud/bigquery/docs/reference/rest/v2/jobs/getQueryResults
    """

    def __init__(self, properties):
        self._properties = {}
        self._set_properties(properties)

    @classmethod
    def from_api_repr(cls, api_response):
        return cls(api_response)

    @property
    def project(self):
        """Project bound to the query job.

        Returns:
            str: The project that the query job is associated with.
        """
        return self._properties.get("jobReference", {}).get("projectId")

    @property
    def cache_hit(self):
        """Query results served from cache.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.cache_hit

        Returns:
            Optional[bool]:
                True if the query results were served from cache (None
                until set by the server).
        """
        return self._properties.get("cacheHit")

    @property
    def complete(self):
        """Server completed query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.job_complete

        Returns:
            Optional[bool]:
                True if the query completed on the server (None
                until set by the server).
        """
        return self._properties.get("jobComplete")

    @property
    def errors(self):
        """Errors generated by the query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.errors

        Returns:
            Optional[List[Mapping]]:
                Mappings describing errors generated on the server (None
                until set by the server).
        """
        return self._properties.get("errors")

    @property
    def job_id(self):
        """Job ID of the query job these results are from.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.job_reference

        Returns:
            str: Job ID of the query job.
        """
        return self._properties.get("jobReference", {}).get("jobId")

    @property
    def page_token(self):
        """Token for fetching next bach of results.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.page_token

        Returns:
            Optional[str]: Token generated on the server (None until set by the server).
        """
        return self._properties.get("pageToken")

    @property
    def total_rows(self):
        """Total number of rows returned by the query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.total_rows

        Returns:
            Optional[int}: Count generated on the server (None until set by the server).
        """
        total_rows = self._properties.get("totalRows")
        if total_rows is not None:
            return int(total_rows)

    @property
    def total_bytes_processed(self):
        """Total number of bytes processed by the query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.total_bytes_processed

        Returns:
            Optional[int]: Count generated on the server (None until set by the server).
        """
        total_bytes_processed = self._properties.get("totalBytesProcessed")
        if total_bytes_processed is not None:
            return int(total_bytes_processed)

    @property
    def num_dml_affected_rows(self):
        """Total number of rows affected by a DML query.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.num_dml_affected_rows

        Returns:
            Optional[int]: Count generated on the server (None until set by the server).
        """
        num_dml_affected_rows = self._properties.get("numDmlAffectedRows")
        if num_dml_affected_rows is not None:
            return int(num_dml_affected_rows)

    @property
    def rows(self):
        """Query results.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.rows

        Returns:
            Optional[List[google.cloud.bigquery.table.Row]]:
                Fields describing the schema (None until set by the server).
        """
        return _rows_from_json(self._properties.get("rows", ()), self.schema)

    @property
    def schema(self):
        """Schema for query results.

        See
        https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query#body.QueryResponse.FIELDS.schema

        Returns:
            Optional[List[SchemaField]]:
                Fields describing the schema (None until set by the server).
        """
        return _parse_schema_resource(self._properties.get("schema", {}))

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        Args:
            api_response (Dict): response returned from an API call
        """
        job_id_present = (
            "jobReference" in api_response
            and "jobId" in api_response["jobReference"]
            and "projectId" in api_response["jobReference"]
        )
        if not job_id_present:
            raise ValueError("QueryResult requires a job reference")

        self._properties.clear()
        self._properties.update(copy.deepcopy(api_response))


def _query_param_from_api_repr(resource):
    """Helper:  construct concrete query parameter from JSON resource."""
    qp_type = resource["parameterType"]
    if "arrayType" in qp_type:
        klass = ArrayQueryParameter
    elif "structTypes" in qp_type:
        klass = StructQueryParameter
    else:
        klass = ScalarQueryParameter
    return klass.from_api_repr(resource)
