# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db.models.lookups import (
    EndsWith, IContains, IEndsWith, IExact, IStartsWith, StartsWith,
)


def icontains(self, compiler, connection):
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params.extend(rhs_params)
    rhs_sql = self.get_rhs_op(connection, rhs_sql)
    # Chop the leading and trailing percent signs that Django adds to the
    # param since this isn't a LIKE query as Django expects.
    params[0] = '(?i)%s' % params[0][1:-1]
    # rhs_sql is REGEXP_CONTAINS(%s, %%s), and lhs_sql is the column name.
    return rhs_sql % lhs_sql, params


def iexact(self, compiler, connection):
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params.extend(rhs_params)
    rhs_sql = self.get_rhs_op(connection, rhs_sql)
    # Wrap the parameter in ^ and $ to restrict the regex to an exact match.
    params[0] = '^(?i)%s$' % params[0]
    # rhs_sql is REGEXP_CONTAINS(%s, %%s), and lhs_sql is the column name.
    return rhs_sql % lhs_sql, params


def startswith_endswith(self, compiler, connection):
    """startswith, endswith, istartswith, and iendswith lookups."""
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params.extend(rhs_params)
    rhs_sql = self.get_rhs_op(connection, rhs_sql)
    # Chop the leading (endswith) or trailing (startswith) percent sign that
    # Django adds to the param since this isn't a LIKE query as Django expects.
    if 'endswith' in self.lookup_name:
        params[0] = params[0][1:]
    else:
        params[0] = params[0][:-1]
    # Construct the regex for istartswith or iendswith.
    if self.lookup_name.startswith('i'):
        regex = '^(?i)%s' if self.lookup_name == 'istartswith' else '(?i)%s$'
        params[0] = regex % params[0]
    # rhs_sql is e.g. 'STARTS_WITH(%s, %%s)' or REGEXP_CONTAINS(%s, %%s), and
    # lhs_sql is the column name.
    return rhs_sql % lhs_sql, params


def register_lookups():
    IContains.as_spanner = icontains
    IExact.as_spanner = iexact
    EndsWith.as_spanner = startswith_endswith
    IEndsWith.as_spanner = startswith_endswith
    StartsWith.as_spanner = startswith_endswith
    IStartsWith.as_spanner = startswith_endswith
