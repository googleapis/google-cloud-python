# -*- coding: utf-8 -*-
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.automl.v1beta1',
    manifest={
        'AnnotationSpec',
    },
)


class AnnotationSpec(proto.Message):
    r"""A definition of an annotation spec.

    Attributes:
        name (str):
            Output only. Resource name of the annotation spec. Form:

            'projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/annotationSpecs/{annotation_spec_id}'
        display_name (str):
            Required. The name of the annotation spec to show in the
            interface. The name can be up to 32 characters long and must
            match the regexp ``[a-zA-Z0-9_]+``.
        example_count (int):
            Output only. The number of examples in the
            parent dataset labeled by the annotation spec.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    example_count: int = proto.Field(
        proto.INT32,
        number=9,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
