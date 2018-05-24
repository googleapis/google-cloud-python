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

import datetime
import decimal
import math
import unittest

import google.cloud._helpers
from google.cloud.bigquery.dbapi import _helpers
from google.cloud.bigquery.dbapi import exceptions


class TestQueryParameters(unittest.TestCase):

    def test_scalar_to_query_parameter(self):
        expected_types = [
            (True, 'BOOL'),
            (False, 'BOOL'),
            (123, 'INT64'),
            (-123456789, 'INT64'),
            (1.25, 'FLOAT64'),
            (decimal.Decimal('1.25'), 'NUMERIC'),
            (b'I am some bytes', 'BYTES'),
            (u'I am a string', 'STRING'),
            (datetime.date(2017, 4, 1), 'DATE'),
            (datetime.time(12, 34, 56), 'TIME'),
            (datetime.datetime(2012, 3, 4, 5, 6, 7), 'DATETIME'),
            (
                datetime.datetime(
                    2012, 3, 4, 5, 6, 7, tzinfo=google.cloud._helpers.UTC),
                'TIMESTAMP',
            ),
        ]
        for value, expected_type in expected_types:
            msg = 'value: {} expected_type: {}'.format(value, expected_type)
            parameter = _helpers.scalar_to_query_parameter(value)
            self.assertIsNone(parameter.name, msg=msg)
            self.assertEqual(parameter.type_, expected_type, msg=msg)
            self.assertEqual(parameter.value, value, msg=msg)
            named_parameter = _helpers.scalar_to_query_parameter(
                value, name='myvar')
            self.assertEqual(named_parameter.name, 'myvar', msg=msg)
            self.assertEqual(named_parameter.type_, expected_type, msg=msg)
            self.assertEqual(named_parameter.value, value, msg=msg)

    def test_scalar_to_query_parameter_w_unexpected_type(self):
        with self.assertRaises(exceptions.ProgrammingError):
            _helpers.scalar_to_query_parameter(value={'a': 'dictionary'})

    def test_scalar_to_query_parameter_w_special_floats(self):
        nan_parameter = _helpers.scalar_to_query_parameter(float('nan'))
        self.assertTrue(math.isnan(nan_parameter.value))
        self.assertEqual(nan_parameter.type_, 'FLOAT64')
        inf_parameter = _helpers.scalar_to_query_parameter(float('inf'))
        self.assertTrue(math.isinf(inf_parameter.value))
        self.assertEqual(inf_parameter.type_, 'FLOAT64')

    def test_to_query_parameters_w_dict(self):
        parameters = {
            'somebool': True,
            'somestring': u'a-string-value',
        }
        query_parameters = _helpers.to_query_parameters(parameters)
        query_parameter_tuples = []
        for param in query_parameters:
            query_parameter_tuples.append(
                (param.name, param.type_, param.value))
        self.assertSequenceEqual(
            sorted(query_parameter_tuples),
            sorted([
                ('somebool', 'BOOL', True),
                ('somestring', 'STRING', u'a-string-value'),
            ]))

    def test_to_query_parameters_w_list(self):
        parameters = [True, u'a-string-value']
        query_parameters = _helpers.to_query_parameters(parameters)
        query_parameter_tuples = []
        for param in query_parameters:
            query_parameter_tuples.append(
                (param.name, param.type_, param.value))
        self.assertSequenceEqual(
            sorted(query_parameter_tuples),
            sorted([
                (None, 'BOOL', True),
                (None, 'STRING', u'a-string-value'),
            ]))
