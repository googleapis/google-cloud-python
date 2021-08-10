# Copyright 2021 Google LLC
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

"""SQLAlchemy and BigQuery escape % and _ differently in like expressions.

We need to correct for the autoescape option in various string
functions.
"""

import sqlalchemy.sql.operators
import sqlalchemy.sql.schema
import sqlalchemy_bigquery.base


def _check(raw, escaped, escape=None, autoescape=True):

    col = sqlalchemy.sql.schema.Column()
    op = col.contains(raw, escape=escape, autoescape=autoescape)
    o2 = sqlalchemy_bigquery.base.BigQueryCompiler._maybe_reescape(op)
    assert o2.left.__dict__ == op.left.__dict__
    assert not o2.modifiers.get("escape")

    assert o2.right.value == escaped


def test_like_autoescape_reescape():

    _check("ab%cd", "ab\\%cd")
    _check("ab%c_d", "ab\\%c\\_d")
    _check("ab%cd", "ab%cd", autoescape=False)
    _check("ab%c_d", "ab\\%c\\_d", escape="\\")
    _check("ab/%c/_/d", "ab/\\%c/\\_/d")
