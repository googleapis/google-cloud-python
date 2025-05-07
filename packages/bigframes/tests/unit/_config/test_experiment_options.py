# Copyright 2024 Google LLC
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

import pytest

import bigframes._config.experiment_options as experiment_options
import bigframes.exceptions as bfe


def test_semantic_operators_default_false():
    options = experiment_options.ExperimentOptions()

    assert options.semantic_operators is False


def test_semantic_operators_set_true_shows_warning():
    options = experiment_options.ExperimentOptions()

    with pytest.warns(FutureWarning):
        options.semantic_operators = True

    assert options.semantic_operators is True


def test_ai_operators_default_false():
    options = experiment_options.ExperimentOptions()

    assert options.ai_operators is False


def test_ai_operators_set_true_shows_warning():
    options = experiment_options.ExperimentOptions()

    with pytest.warns(bfe.PreviewWarning):
        options.ai_operators = True

    assert options.ai_operators is True
