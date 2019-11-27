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
    EndsWith, IEndsWith, IStartsWith, StartsWith,
)


def endswith(self, compiler, connection):
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params.extend(rhs_params)
    rhs_sql = self.get_rhs_op(connection, rhs_sql)
    # Chop leading '%' from param since this isn't a LIKE query.
    params[0] = params[0][1:]
    # rhs_sql is 'STARTS_WITH(%s, %%s)' and lhs_sql is the column name.
    return rhs_sql % lhs_sql, params


def startswith(self, compiler, connection):
    # Same logic as endswith but chop trailing (rather than leading) '%' from
    # param.
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_sql, rhs_params = self.process_rhs(compiler, connection)
    params.extend(rhs_params)
    rhs_sql = self.get_rhs_op(connection, rhs_sql)
    params[0] = params[0][:-1]
    return rhs_sql % lhs_sql, params


def register_lookups():
    EndsWith.as_spanner = endswith
    IEndsWith.as_spanner = endswith
    StartsWith.as_spanner = startswith
    IStartsWith.as_spanner = startswith
