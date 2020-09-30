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


from collections import abc as collections_abc
import datetime
import decimal
import functools
import numbers

import six

from google.cloud import bigquery
from google.cloud.bigquery import table
from google.cloud.bigquery.dbapi import exceptions


def scalar_to_query_parameter(value, name=None):
    """Convert a scalar value into a query parameter.

    Args:
        value (Any):
            A scalar value to convert into a query parameter.

        name (str):
            (Optional) Name of the query parameter.

    Returns:
        google.cloud.bigquery.ScalarQueryParameter:
            A query parameter corresponding with the type and value of the plain
            Python object.

    Raises:
        google.cloud.bigquery.dbapi.exceptions.ProgrammingError:
            if the type cannot be determined.
    """
    parameter_type = bigquery_scalar_type(value)

    if parameter_type is None:
        raise exceptions.ProgrammingError(
            "encountered parameter {} with value {} of unexpected type".format(
                name, value
            )
        )
    return bigquery.ScalarQueryParameter(name, parameter_type, value)


def array_to_query_parameter(value, name=None):
    """Convert an array-like value into a query parameter.

    Args:
        value (Sequence[Any]): The elements of the array (should not be a
            string-like Sequence).
        name (Optional[str]): Name of the query parameter.

    Returns:
        A query parameter corresponding with the type and value of the plain
        Python object.

    Raises:
        google.cloud.bigquery.dbapi.exceptions.ProgrammingError:
            if the type of array elements cannot be determined.
    """
    if not array_like(value):
        raise exceptions.ProgrammingError(
            "The value of parameter {} must be a sequence that is "
            "not string-like.".format(name)
        )

    if not value:
        raise exceptions.ProgrammingError(
            "Encountered an empty array-like value of parameter {}, cannot "
            "determine array elements type.".format(name)
        )

    # Assume that all elements are of the same type, and let the backend handle
    # any type incompatibilities among the array elements
    array_type = bigquery_scalar_type(value[0])
    if array_type is None:
        raise exceptions.ProgrammingError(
            "Encountered unexpected first array element of parameter {}, "
            "cannot determine array elements type.".format(name)
        )

    return bigquery.ArrayQueryParameter(name, array_type, value)


def to_query_parameters_list(parameters):
    """Converts a sequence of parameter values into query parameters.

    Args:
        parameters (Sequence[Any]): Sequence of query parameter values.

    Returns:
        List[google.cloud.bigquery.query._AbstractQueryParameter]:
            A list of query parameters.
    """
    result = []

    for value in parameters:
        if isinstance(value, collections_abc.Mapping):
            raise NotImplementedError("STRUCT-like parameter values are not supported.")
        elif array_like(value):
            param = array_to_query_parameter(value)
        else:
            param = scalar_to_query_parameter(value)
        result.append(param)

    return result


def to_query_parameters_dict(parameters):
    """Converts a dictionary of parameter values into query parameters.

    Args:
        parameters (Mapping[str, Any]): Dictionary of query parameter values.

    Returns:
        List[google.cloud.bigquery.query._AbstractQueryParameter]:
            A list of named query parameters.
    """
    result = []

    for name, value in six.iteritems(parameters):
        if isinstance(value, collections_abc.Mapping):
            raise NotImplementedError(
                "STRUCT-like parameter values are not supported "
                "(parameter {}).".format(name)
            )
        elif array_like(value):
            param = array_to_query_parameter(value, name=name)
        else:
            param = scalar_to_query_parameter(value, name=name)
        result.append(param)

    return result


def to_query_parameters(parameters):
    """Converts DB-API parameter values into query parameters.

    Args:
        parameters (Union[Mapping[str, Any], Sequence[Any]]):
            A dictionary or sequence of query parameter values.

    Returns:
        List[google.cloud.bigquery.query._AbstractQueryParameter]:
            A list of query parameters.
    """
    if parameters is None:
        return []

    if isinstance(parameters, collections_abc.Mapping):
        return to_query_parameters_dict(parameters)

    return to_query_parameters_list(parameters)


def bigquery_scalar_type(value):
    """Return a BigQuery name of the scalar type that matches the given value.

    If the scalar type name could not be determined (e.g. for non-scalar
    values), ``None`` is returned.

    Args:
        value (Any)

    Returns:
        Optional[str]: The BigQuery scalar type name.
    """
    if isinstance(value, bool):
        return "BOOL"
    elif isinstance(value, numbers.Integral):
        return "INT64"
    elif isinstance(value, numbers.Real):
        return "FLOAT64"
    elif isinstance(value, decimal.Decimal):
        return "NUMERIC"
    elif isinstance(value, six.text_type):
        return "STRING"
    elif isinstance(value, six.binary_type):
        return "BYTES"
    elif isinstance(value, datetime.datetime):
        return "DATETIME" if value.tzinfo is None else "TIMESTAMP"
    elif isinstance(value, datetime.date):
        return "DATE"
    elif isinstance(value, datetime.time):
        return "TIME"

    return None


def array_like(value):
    """Determine if the given value is array-like.

    Examples of array-like values (as interpreted by this function) are
    sequences such as ``list`` and ``tuple``, but not strings and other
    iterables such as sets.

    Args:
        value (Any)

    Returns:
        bool: ``True`` if the value is considered array-like, ``False`` otherwise.
    """
    return isinstance(value, collections_abc.Sequence) and not isinstance(
        value, (six.text_type, six.binary_type, bytearray)
    )


def to_bq_table_rows(rows_iterable):
    """Convert table rows to BigQuery table Row instances.

    Args:
        rows_iterable (Iterable[Mapping]):
            An iterable of row data items to convert to ``Row`` instances.

    Returns:
        Iterable[google.cloud.bigquery.table.Row]
    """

    def to_table_row(row):
        # NOTE: We fetch ARROW values, thus we need to convert them to Python
        # objects with as_py().
        values = tuple(value.as_py() for value in row.values())
        keys_to_index = {key: i for i, key in enumerate(row.keys())}
        return table.Row(values, keys_to_index)

    return (to_table_row(row_data) for row_data in rows_iterable)


def raise_on_closed(
    exc_msg, exc_class=exceptions.ProgrammingError, closed_attr_name="_closed"
):
    """Make public instance methods raise an error if the instance is closed."""

    def _raise_on_closed(method):
        """Make a non-static method raise an error if its containing instance is closed.
        """

        def with_closed_check(self, *args, **kwargs):
            if getattr(self, closed_attr_name):
                raise exc_class(exc_msg)
            return method(self, *args, **kwargs)

        functools.update_wrapper(with_closed_check, method)
        return with_closed_check

    def decorate_public_methods(klass):
        """Apply ``_raise_on_closed()`` decorator to public instance methods.
        """
        for name in dir(klass):
            if name.startswith("_"):
                continue

            member = getattr(klass, name)
            if not callable(member):
                continue

            # We need to check for class/static methods directly in the instance
            # __dict__, not via the retrieved attribute (`member`), as the
            # latter is already a callable *produced* by one of these descriptors.
            if isinstance(klass.__dict__[name], (staticmethod, classmethod)):
                continue

            member = _raise_on_closed(member)
            setattr(klass, name, member)

        return klass

    return decorate_public_methods
