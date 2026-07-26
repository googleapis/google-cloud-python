# Copyright 2026 Google LLC
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

import constants
import jinja2
import data_models
import pprint

import template_renderer


def _generate_sql_operator_def():
    pass


def _generate_accesor():
    pass


def _generate_tests():
    pass


def generate(bq_modules: list[data_models.BQModule]):

    for bq_module in bq_modules:
        for bq_func in bq_module.functions:
            pprint.pp(template_renderer.render_signature_def(bq_func, bq_module))

    # Write to file

    # Ruff format
    pass
