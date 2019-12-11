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

from django.db.models.expressions import OrderBy


def order_by(self, compiler, connection, **extra_context):
    # In Django 3.1, this can be replaced with
    # DatabaseFeatures.supports_order_by_nulls_modifier = False.
    template = None
    if self.nulls_last:
        template = '%(expression)s IS NULL, %(expression)s %(ordering)s'
    elif self.nulls_first:
        template = '%(expression)s IS NOT NULL, %(expression)s %(ordering)s'
    return self.as_sql(compiler, connection, template=template, **extra_context)


def register_expressions():
    OrderBy.as_spanner = order_by
