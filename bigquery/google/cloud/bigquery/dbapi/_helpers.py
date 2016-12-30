# Copyright 2016 Google Inc.
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
import numbers
import six
import time

from google.cloud import bigquery
from google.cloud.bigquery.dbapi import exceptions


def wait_for_job(job):
    """Waits for a job to complete by polling until the state is `DONE`.

    Raises a DatabaseError if the job fails.

    :type: :class:`~google.cloud.bigquery.job._AsyncJob`
    :param job: Wait for this job to finish.
    """
    while True:
        job.reload()
        if job.state == 'DONE':
            if job.error_result:
                # TODO: raise a more specific exception, based on the error.
                # See: https://cloud.google.com/bigquery/troubleshooting-errors
                raise exceptions.DatabaseError(job.errors)
            return
        time.sleep(1)


def scalar_to_query_parameter(name=None, value=None):
    """Convert a scalar value into a query parameter.

    Note: the bytes type cannot be distinguished from a string in Python 2.

    Raises a :class:`~ google.cloud.bigquery.dbapi.exceptions.ProgrammingError`
    if the type cannot be determined.

    For more information about BigQuery data types, see:
    https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types

    :type: str
    :param name: Optional name of the query parameter.

    :type: any
    :param value: A scalar value to convert into a query parameter.

    :rtype: :class:`~google.cloud.bigquery.ScalarQueryParameter`
    """
    parameter_type = None

    if isinstance(value, bool):
        parameter_type = 'BOOL'
    elif isinstance(value, numbers.Integral):
        parameter_type = 'INT64'
    elif isinstance(value, numbers.Real):
        parameter_type = 'FLOAT64'
    elif isinstance(value, six.string_types):
        parameter_type = 'STRING'
    elif isinstance(value, bytes):
        parameter_type = 'BYTES'
    elif isinstance(value, datetime.datetime):
        parameter_type = 'TIMESTAMP' if value.tzinfo else 'DATETIME'
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
    """Converts a list of parameter values into query parameters.

    :type: list
    :param parameters: List of query parameter values.

    :rtype:
        list of :class:`~google.cloud.bigquery._helpers.AbstractQueryParameter`
    """
    query_parameters = []

    for value in parameters:
        query_parameters.append(scalar_to_query_parameter(value=value))

    return query_parameters


def to_query_parameters_dict(parameters):
    """Converts a dictionary of parameter values into query parameters.

    :type: dict
    :param parameters: Dictionary of query parameter values.

    :rtype:
        list of :class:`~google.cloud.bigquery._helpers.AbstractQueryParameter`
    """
    query_parameters = []

    for name in parameters:
        value = parameters[name]
        query_parameters.append(scalar_to_query_parameter(name, value))

    return query_parameters


def to_query_parameters(parameters):
    """Converts DB-API parameter values into query parameters.

    :type: dict or list
    :param parameters: Optional dictionary or list of query parameter values.

    :rtype:
        list of :class:`~google.cloud.bigquery._helpers.AbstractQueryParameter`
    """
    if parameters is None:
        return []

    if isinstance(parameters, collections.Mapping):
        return to_query_parameters_dict(parameters)

    return to_query_parameters_list(parameters)
