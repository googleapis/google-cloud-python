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


__protobuf__ = proto.module(
    package='google.robotics.developer.modelserving.v1',
    manifest={
        'Tensor',
        'ExtraInputs',
    },
)


class Tensor(proto.Message):
    r"""Tensor message for arbitrary input.

    Attributes:
        values (MutableSequence[float]):
            Tensors in float flattend to 1d. Reshaping
            information can be infered from model attributes
            or other extra inputs.
    """

    values: MutableSequence[float] = proto.RepeatedField(
        proto.FLOAT,
        number=1,
    )


class ExtraInputs(proto.Message):
    r"""Extra inputs to parameterize the inference.

    Attributes:
        items (MutableMapping[str, float]):
            items[input_key] specifies value set for an input_key.

            E.g., the following extra inputs will change
            input.tempeature to 0.1 in sampling decode. items {
            "temperature" : "0.1" }
        tensors (MutableMapping[str, google.cloud.robotics_developer_modelserving_v1.types.Tensor]):
            tensors[input_key] specifies tensors set for an input_key.

            E.g., the following extra inputs will change input.tensors
            as soft prompt. tensors { "prompt_embeddings" : [0.1, 0.2,
            0.3, 0.4] } It is invalid for the same key to appear in both
            items and tensors.
        strings (MutableMapping[str, str]):
            strings[input_key] specifies value in string type set for an
            input_key. E.g., the following extra inputs will change
            input.strings as decoding constraint. strings { "regex" :
            "a*b*\ c\ *d*\ e\ *f*\ g\ *h*" } It is invalid if the same
            key has appeared in items and tensors.
    """

    items: MutableMapping[str, float] = proto.MapField(
        proto.STRING,
        proto.FLOAT,
        number=1,
    )
    tensors: MutableMapping[str, 'Tensor'] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=2,
        message='Tensor',
    )
    strings: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
