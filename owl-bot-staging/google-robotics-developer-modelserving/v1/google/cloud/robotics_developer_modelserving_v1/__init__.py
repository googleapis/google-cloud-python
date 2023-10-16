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
from google.cloud.robotics_developer_modelserving_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.model_serving import ModelServingClient
from .services.model_serving import ModelServingAsyncClient

from .types.common import ExtraInputs
from .types.common import Tensor
from .types.modelserving import DoPingRequest
from .types.modelserving import DoPingResponse
from .types.modelserving import GeneratePlanRequest
from .types.modelserving import GeneratePlanResponse
from .types.types import Content
from .types.types import ContentChunk
from .types.types import Plan
from .types.types import Prompt

__all__ = (
    'ModelServingAsyncClient',
'Content',
'ContentChunk',
'DoPingRequest',
'DoPingResponse',
'ExtraInputs',
'GeneratePlanRequest',
'GeneratePlanResponse',
'ModelServingClient',
'Plan',
'Prompt',
'Tensor',
)
