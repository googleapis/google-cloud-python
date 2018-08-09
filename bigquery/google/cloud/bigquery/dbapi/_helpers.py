# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import collections
import datetime
import decimal
import numbers

import six

from google.cloud import bigquery
from google.cloud.bigquery.dbapi import exceptions


def scalar_to_query_parameter(value, name=None):
    """Convert a scalar value into a query parameter.

    :type value: any
    :param value: A scalar value to convert into a query parameter.

    :type name: str
    :param name: (Optional) Name of the query parameter.

    :rtype: :class:`~google.cloud.bigquery.ScalarQueryParameter`
    :returns:
        A query parameter corresponding with the type and value of the plain
        Python object.
    :raises: :class:`~google.cloud.bigquery.dbapi.exceptions.ProgrammingError`
        if the type cannot be determined.
    """
    parameter_type = None

    if isinstance(value, bool):
        parameter_type = 'BOOL'
    elif isinstance(value, numbers.Integral):
        parameter_type = 'INT64'
    elif isinstance(value, numbers.Real):
        parameter_type = 'FLOAT64'
    elif isinstance(value, decimal.Decimal):
        parameter_type = 'NUMERIC'
    elif isinstance(value, six.text_type):
        parameter_type = 'STRING'
    elif isinstance(value, six.binary_type):
        parameter_type = 'BYTES'
    elif isinstance(value, datetime.datetime):
        parameter_type = 'DATETIME' if value.tzinfo is None else 'TIMESTAMP'
    elif isinstance(value, datetime.date):
        parameter_type = 'DATE'
    elif isinstance(value, datetime.time):
        parameter_type = 'TIME'
    else:
        raise exceptions.ProgrammingError(
            'encountered parameter {} with value {} of unexpected type'.format(
                name, value))
    return bigquery.ScalarQueryParameter(name, parameter_type, value)


def to_query_parameters_list(parameters):
    """Converts a sequence of parameter values into query parameters.

    :type parameters: Sequence[Any]
    :param parameters: Sequence of query parameter values.

    :rtype: List[google.cloud.bigquery.query._AbstractQueryParameter]
    :returns: A list of query parameters.
    """
    return [scalar_to_query_parameter(value) for value in parameters]


def to_query_parameters_dict(parameters):
    """Converts a dictionary of parameter values into query parameters.

    :type parameters: Mapping[str, Any]
    :param parameters: Dictionary of query parameter values.

    :rtype: List[google.cloud.bigquery.query._AbstractQueryParameter]
    :returns: A list of named query parameters.
    """
    return [
        scalar_to_query_parameter(value, name=name)
        for name, value
        in six.iteritems(parameters)]


def to_query_parameters(parameters):
    """Converts DB-API parameter values into query parameters.

    :type parameters: Mapping[str, Any] or Sequence[Any]
    :param parameters: A dictionary or sequence of query parameter values.

    :rtype: List[google.cloud.bigquery.query._AbstractQueryParameter]
    :returns: A list of query parameters.
    """
    if parameters is None:
        return []

    if isinstance(parameters, collections.Mapping):
        return to_query_parameters_dict(parameters)

    return to_query_parameters_list(parameters)
