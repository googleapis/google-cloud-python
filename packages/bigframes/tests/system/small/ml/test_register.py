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

from typing import cast

from bigframes.ml import core, imported, linear_model, llm


def test_linear_reg_register(
    ephemera_penguins_linear_model: linear_model.LinearRegression,
):
    model = ephemera_penguins_linear_model
    model.register()

    model_name = "bigframes_" + cast(
        str, cast(core.BqmlModel, model._bqml_model).model.model_id
    )
    # Only registered model contains the field, and the field includes project/dataset. Here only check model_id.
    assert (
        model_name[:63]  # truncated
        in cast(core.BqmlModel, model._bqml_model).model.training_runs[-1][
            "vertexAiModelId"
        ]
    )


def test_linear_reg_register_with_params(
    ephemera_penguins_linear_model: linear_model.LinearRegression,
):
    model_name = "bigframes_system_test_linear_reg_model"
    model = ephemera_penguins_linear_model
    model.register(model_name)

    # Only registered model contains the field, and the field includes project/dataset. Here only check model_id.
    assert (
        model_name[:63]  # truncated
        in cast(core.BqmlModel, model._bqml_model).model.training_runs[-1][
            "vertexAiModelId"
        ]
    )


def test_palm2_text_generator_register(
    ephemera_palm2_text_generator_model: llm.PaLM2TextGenerator,
):
    model = ephemera_palm2_text_generator_model
    model.register()

    model_name = "bigframes_" + cast(
        str, cast(core.BqmlModel, model._bqml_model).model.model_id
    )
    # Only registered model contains the field, and the field includes project/dataset. Here only check model_id.
    assert (
        model_name[:63]  # truncated
        in cast(core.BqmlModel, model._bqml_model).model.training_runs[-1][
            "vertexAiModelId"
        ]
    )


def test_imported_tensorflow_register(
    ephemera_imported_tensorflow_model: imported.TensorFlowModel,
):
    model = ephemera_imported_tensorflow_model
    model.register()

    model_name = "bigframes_" + cast(
        str, cast(core.BqmlModel, model._bqml_model).model.model_id
    )
    # Only registered model contains the field, and the field includes project/dataset. Here only check model_id.
    assert (
        model_name[:63]  # truncated
        in cast(core.BqmlModel, model._bqml_model).model.training_runs[-1][
            "vertexAiModelId"
        ]
    )
