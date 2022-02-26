# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.video.stitcher.v1",
    manifest={"VodStitchDetail", "AdStitchDetail",},
)


class VodStitchDetail(proto.Message):
    r"""Detailed information related to the interstitial of a VOD
    session.

    Attributes:
        name (str):
            The name of the stitch detail in the specified VOD session,
            in the form of
            ``projects/{project}/locations/{location}/vodSessions/{vod_session_id}/vodStitchDetails/{id}``.
        ad_stitch_details (Sequence[google.cloud.video.stitcher_v1.types.AdStitchDetail]):
            A list of ad processing details for the
            fetched ad playlist.
    """

    name = proto.Field(proto.STRING, number=1,)
    ad_stitch_details = proto.RepeatedField(
        proto.MESSAGE, number=3, message="AdStitchDetail",
    )


class AdStitchDetail(proto.Message):
    r"""Metadata for a stitched ad.

    Attributes:
        ad_break_id (str):
            Required. The ad break ID of the processed
            ad.
        ad_id (str):
            Required. The ad ID of the processed ad.
        ad_time_offset (google.protobuf.duration_pb2.Duration):
            Required. The time offset of the processed
            ad.
        skip_reason (str):
            Optional. Indicates the reason why the ad has
            been skipped.
        media (Sequence[google.cloud.video.stitcher_v1.types.AdStitchDetail.MediaEntry]):
            Optional. The metadata of the chosen media
            file for the ad.
    """

    ad_break_id = proto.Field(proto.STRING, number=1,)
    ad_id = proto.Field(proto.STRING, number=2,)
    ad_time_offset = proto.Field(
        proto.MESSAGE, number=3, message=duration_pb2.Duration,
    )
    skip_reason = proto.Field(proto.STRING, number=4,)
    media = proto.MapField(
        proto.STRING, proto.MESSAGE, number=5, message=struct_pb2.Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
