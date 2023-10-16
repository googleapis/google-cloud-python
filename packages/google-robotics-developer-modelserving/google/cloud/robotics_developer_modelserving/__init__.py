# -*- coding: utf-8 -*-
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
#
from google.cloud.robotics_developer_modelserving import (
    gapic_version as package_version,
)

__version__ = package_version.__version__


from google.cloud.robotics_developer_modelserving_v1.services.model_serving.async_client import (
    ModelServingAsyncClient,
)
from google.cloud.robotics_developer_modelserving_v1.services.model_serving.client import (
    ModelServingClient,
)
from google.cloud.robotics_developer_modelserving_v1.types.common import (
    ExtraInputs,
    Tensor,
)
from google.cloud.robotics_developer_modelserving_v1.types.modelserving import (
    DoPingRequest,
    DoPingResponse,
    GeneratePlanRequest,
    GeneratePlanResponse,
)
from google.cloud.robotics_developer_modelserving_v1.types.types import (
    Content,
    ContentChunk,
    Plan,
    Prompt,
)

__all__ = (
    "ModelServingClient",
    "ModelServingAsyncClient",
    "ExtraInputs",
    "Tensor",
    "DoPingRequest",
    "DoPingResponse",
    "GeneratePlanRequest",
    "GeneratePlanResponse",
    "Content",
    "ContentChunk",
    "Plan",
    "Prompt",
)
