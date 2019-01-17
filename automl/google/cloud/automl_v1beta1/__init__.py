# -*- coding: utf-8 -*-
#
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

from __future__ import absolute_import

from google.cloud.automl_v1beta1 import types
from google.cloud.automl_v1beta1.gapic import auto_ml_client
from google.cloud.automl_v1beta1.gapic import enums
from google.cloud.automl_v1beta1.gapic import prediction_service_client


class PredictionServiceClient(prediction_service_client.PredictionServiceClient):
    __doc__ = prediction_service_client.PredictionServiceClient.__doc__
    enums = enums


class AutoMlClient(auto_ml_client.AutoMlClient):
    __doc__ = auto_ml_client.AutoMlClient.__doc__
    enums = enums


__all__ = ("enums", "types", "PredictionServiceClient", "AutoMlClient")
