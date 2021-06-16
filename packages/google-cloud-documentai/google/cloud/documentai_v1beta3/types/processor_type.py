# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.documentai.v1beta3", manifest={"ProcessorType",},
)


class ProcessorType(proto.Message):
    r"""A processor type is responsible for performing a certain
    document understanding task on a certain type of document.

    Attributes:
        name (str):
            The resource name of the processor type.
        type_ (str):
            The type of the processor.
        category (str):
            The processor category.
        available_locations (Sequence[google.cloud.documentai_v1beta3.types.ProcessorType.LocationInfo]):
            The locations in which this processor is
            available.
        allow_creation (bool):
            Whether the processor type allows creation.
            If yes, user can create a processor of this
            processor type. Otherwise, user needs to require
            for whitelisting.
    """

    class LocationInfo(proto.Message):
        r"""The location information about where the processor is
        available.

        Attributes:
            location_id (str):
                The location id.
        """

        location_id = proto.Field(proto.STRING, number=1,)

    name = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.STRING, number=2,)
    category = proto.Field(proto.STRING, number=3,)
    available_locations = proto.RepeatedField(
        proto.MESSAGE, number=4, message=LocationInfo,
    )
    allow_creation = proto.Field(proto.BOOL, number=6,)


__all__ = tuple(sorted(__protobuf__.manifest))
