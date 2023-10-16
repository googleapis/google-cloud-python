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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.robotics_developer_modelserving_v1.types import types

__protobuf__ = proto.module(
    package="google.robotics.developer.modelserving.v1",
    manifest={
        "DoPingRequest",
        "DoPingResponse",
        "GeneratePlanRequest",
        "GeneratePlanResponse",
    },
)


class DoPingRequest(proto.Message):
    r"""Request for DoPing method."""


class DoPingResponse(proto.Message):
    r"""Response for DoPing method."""


class GeneratePlanRequest(proto.Message):
    r"""Request for GeneratePlan method.

    Attributes:
        prompt (google.cloud.robotics_developer_modelserving_v1.types.Prompt):
            Required. The structured textual input given
            to the model as a prompt. Given a prompt, the
            model will return a sequence of predicted steps.
    """

    prompt: types.Prompt = proto.Field(
        proto.MESSAGE,
        number=1,
        message=types.Prompt,
    )


class GeneratePlanResponse(proto.Message):
    r"""Response for GeneratePlan method.

    Attributes:
        plan (google.cloud.robotics_developer_modelserving_v1.types.Plan):
            Generated plan.
    """

    plan: types.Plan = proto.Field(
        proto.MESSAGE,
        number=1,
        message=types.Plan,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
