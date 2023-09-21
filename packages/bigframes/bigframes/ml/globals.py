# Copyright 2023 Google LLC
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

"""Global Singletons for BigQuery DataFrame ML."""

from bigframes.ml import core, sql

_BASE_SQL_GENERATOR = sql.BaseSqlGenerator()
_BQML_MODEL_FACTORY = core.BqmlModelFactory()


def base_sql_generator() -> sql.BaseSqlGenerator:
    """Base SQL Generator."""
    return _BASE_SQL_GENERATOR


def bqml_model_factory() -> core.BqmlModelFactory:
    """BQML Model Factory"""
    return _BQML_MODEL_FACTORY
