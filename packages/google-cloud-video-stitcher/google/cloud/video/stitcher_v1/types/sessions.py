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
from typing import MutableMapping, MutableSequence

from google.protobuf import duration_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.video.stitcher_v1.types import companions, events

__protobuf__ = proto.module(
    package="google.cloud.video.stitcher.v1",
    manifest={
        "VodSession",
        "Interstitials",
        "VodSessionAd",
        "VodSessionContent",
        "VodSessionAdBreak",
        "LiveSession",
        "AdTag",
        "ManifestOptions",
        "RenditionFilter",
    },
)


class VodSession(proto.Message):
    r"""Metadata for a VOD session.

    Attributes:
        name (str):
            Output only. The name of the VOD session, in the form of
            ``projects/{project_number}/locations/{location}/vodSessions/{id}``.
        interstitials (google.cloud.video.stitcher_v1.types.Interstitials):
            Output only. Metadata of what was stitched
            into the content.
        play_uri (str):
            Output only. The playback URI of the stitched
            content.
        source_uri (str):
            Required. URI of the media to stitch.
        ad_tag_uri (str):
            Required. Ad tag URI.
        ad_tag_macro_map (MutableMapping[str, str]):
            Key value pairs for ad tag macro replacement. If the
            specified ad tag URI has macros, this field provides the
            mapping to the value that will replace the macro in the ad
            tag URI. Macros are designated by square brackets. For
            example:

            Ad tag URI:
            ``"https://doubleclick.google.com/ad/1?geo_id=[geoId]"``

            Ad tag macro map: ``{"geoId": "123"}``

            Fully qualified ad tag:
            ``"``\ https://doubleclick.google.com/ad/1?geo_id=123"\`
        client_ad_tracking (bool):
            Indicates whether client side ad tracking is
            enabled. If client side ad tracking is enabled,
            then the client player is expected to trigger
            playback and activity events itself. If this is
            set to false, server side ad tracking is
            enabled, causing the Video Stitcher service will
            trigger playback events on behalf of the client
            player.
        manifest_options (google.cloud.video.stitcher_v1.types.ManifestOptions):
            Additional options that affect the output of
            the manifest.
        asset_id (str):
            Output only. The generated ID of the
            VodSession's source media.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    interstitials: "Interstitials" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Interstitials",
    )
    play_uri: str = proto.Field(
        proto.STRING,
        number=4,
    )
    source_uri: str = proto.Field(
        proto.STRING,
        number=5,
    )
    ad_tag_uri: str = proto.Field(
        proto.STRING,
        number=6,
    )
    ad_tag_macro_map: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=7,
    )
    client_ad_tracking: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    manifest_options: "ManifestOptions" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="ManifestOptions",
    )
    asset_id: str = proto.Field(
        proto.STRING,
        number=10,
    )


class Interstitials(proto.Message):
    r"""Describes what was stitched into a VOD session's manifest.

    Attributes:
        ad_breaks (MutableSequence[google.cloud.video.stitcher_v1.types.VodSessionAdBreak]):
            List of ad breaks ordered by time.
        session_content (google.cloud.video.stitcher_v1.types.VodSessionContent):
            Information related to the content of the VOD
            session.
    """

    ad_breaks: MutableSequence["VodSessionAdBreak"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="VodSessionAdBreak",
    )
    session_content: "VodSessionContent" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="VodSessionContent",
    )


class VodSessionAd(proto.Message):
    r"""Metadata for an inserted ad in a VOD session.

    Attributes:
        duration (google.protobuf.duration_pb2.Duration):
            Duration in seconds of the ad.
        companion_ads (google.cloud.video.stitcher_v1.types.CompanionAds):
            Metadata of companion ads associated with the
            ad.
        activity_events (MutableSequence[google.cloud.video.stitcher_v1.types.Event]):
            The list of progress tracking events for the ad break. These
            can be of the following IAB types: ``MUTE``, ``UNMUTE``,
            ``PAUSE``, ``CLICK``, ``CLICK_THROUGH``, ``REWIND``,
            ``RESUME``, ``ERROR``, ``FULLSCREEN``, ``EXIT_FULLSCREEN``,
            ``EXPAND``, ``COLLAPSE``, ``ACCEPT_INVITATION_LINEAR``,
            ``CLOSE_LINEAR``, ``SKIP``.
    """

    duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=1,
        message=duration_pb2.Duration,
    )
    companion_ads: companions.CompanionAds = proto.Field(
        proto.MESSAGE,
        number=2,
        message=companions.CompanionAds,
    )
    activity_events: MutableSequence[events.Event] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=events.Event,
    )


class VodSessionContent(proto.Message):
    r"""Metadata for the entire stitched content in a VOD session.

    Attributes:
        duration (google.protobuf.duration_pb2.Duration):
            The total duration in seconds of the content
            including the ads stitched in.
    """

    duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=1,
        message=duration_pb2.Duration,
    )


class VodSessionAdBreak(proto.Message):
    r"""Metadata for an inserted ad break.

    Attributes:
        progress_events (MutableSequence[google.cloud.video.stitcher_v1.types.ProgressEvent]):
            List of events that are expected to be
            triggered, ordered by time.
        ads (MutableSequence[google.cloud.video.stitcher_v1.types.VodSessionAd]):
            Ordered list of ads stitched into the ad
            break.
        end_time_offset (google.protobuf.duration_pb2.Duration):
            Ad break end time in seconds relative to the
            start of the VOD asset.
        start_time_offset (google.protobuf.duration_pb2.Duration):
            Ad break start time in seconds relative to
            the start of the VOD asset.
    """

    progress_events: MutableSequence[events.ProgressEvent] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=events.ProgressEvent,
    )
    ads: MutableSequence["VodSessionAd"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="VodSessionAd",
    )
    end_time_offset: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=3,
        message=duration_pb2.Duration,
    )
    start_time_offset: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=4,
        message=duration_pb2.Duration,
    )


class LiveSession(proto.Message):
    r"""Metadata for a live session.

    Attributes:
        name (str):
            Output only. The name of the live session, in the form of
            ``projects/{project}/locations/{location}/liveSessions/{id}``.
        play_uri (str):
            Output only. The URI to play the live
            session's ad-stitched stream.
        source_uri (str):
            The URI of the live session's source stream.
        default_ad_tag_id (str):
            The default ad tag to use when no ad tag ids are specified
            in an ad break's SCTE-35 message.

            default_ad_tag_id is necessary when ``adTagMap`` has more
            than one key. Its value must be present in the ``adTagMap``.
        ad_tag_map (MutableMapping[str, google.cloud.video.stitcher_v1.types.AdTag]):
            Key value pairs for ad tags. Ads parsed from
            ad tags must be MP4 videos each with at least
            one audio track.
        ad_tag_macros (MutableMapping[str, str]):
            Key value pairs for ad tag macro replacement. If the
            specified ad tag URI has macros, this field provides the
            mapping to the value that will replace the macro in the ad
            tag URI. Macros are designated by square brackets.

            For example:

            Ad tag URI:
            "https://doubleclick.google.com/ad/1?geo_id=[geoId]"

            Ad tag macros: ``{"geoId": "123"}``

            Fully qualified ad tag:
            ``"https://doubleclick.google.com/ad/1?geo_id=123"``
        client_ad_tracking (bool):
            Whether client side ad tracking is enabled.
            If enabled, the client player is expected to
            trigger playback and activity events itself.
            Otherwise, server side ad tracking is enabled
            and the Video Stitcher API will trigger playback
            events on behalf of the client player.
        default_slate_id (str):
            The default slate to use when no slates are specified in an
            ad break's SCTE-35 message. When specified, this value must
            match the ID for a slate that has already been created via
            the `CreateSlate <projects.locations.slates/create>`__
            method.
        stitching_policy (google.cloud.video.stitcher_v1.types.LiveSession.StitchingPolicy):
            Defines the stitcher behavior in case an ad does not align
            exactly with the ad break boundaries. If not specified, the
            default is ``COMPLETE_AD``.
        manifest_options (google.cloud.video.stitcher_v1.types.ManifestOptions):
            Additional options that affect the output of
            the manifest.
        stream_id (str):
            Output only. The generated ID of the
            LiveSession's source stream.
    """

    class StitchingPolicy(proto.Enum):
        r"""Defines the stitcher behavior in case an ad does not align exactly
        with the ad break boundaries. If not specified, the default is
        COMPLETE_AD.
        """
        STITCHING_POLICY_UNSPECIFIED = 0
        COMPLETE_AD = 1
        CUT_CURRENT = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    play_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    source_uri: str = proto.Field(
        proto.STRING,
        number=3,
    )
    default_ad_tag_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    ad_tag_map: MutableMapping[str, "AdTag"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=5,
        message="AdTag",
    )
    ad_tag_macros: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    client_ad_tracking: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    default_slate_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    stitching_policy: StitchingPolicy = proto.Field(
        proto.ENUM,
        number=9,
        enum=StitchingPolicy,
    )
    manifest_options: "ManifestOptions" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="ManifestOptions",
    )
    stream_id: str = proto.Field(
        proto.STRING,
        number=11,
    )


class AdTag(proto.Message):
    r"""Metadata of an ad tag.

    Attributes:
        uri (str):
            Ad tag URI template.
    """

    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ManifestOptions(proto.Message):
    r"""Options for manifest generation.

    Attributes:
        include_renditions (MutableSequence[google.cloud.video.stitcher_v1.types.RenditionFilter]):
            If specified, the output manifest will only
            return renditions matching the specified
            filters.
        bitrate_order (google.cloud.video.stitcher_v1.types.ManifestOptions.OrderPolicy):
            If specified, the output manifest will orders
            the video and muxed renditions by bitrate
            according to the ordering policy.
    """

    class OrderPolicy(proto.Enum):
        r"""Defines the ordering policy during manifest generation."""
        ORDER_POLICY_UNSPECIFIED = 0
        ASCENDING = 1
        DESCENDING = 2

    include_renditions: MutableSequence["RenditionFilter"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RenditionFilter",
    )
    bitrate_order: OrderPolicy = proto.Field(
        proto.ENUM,
        number=2,
        enum=OrderPolicy,
    )


class RenditionFilter(proto.Message):
    r"""Filters for a video or muxed redition.

    Attributes:
        bitrate_bps (int):
            Bitrate in bits per second for the rendition.
            If set, only renditions with the exact bitrate
            will match.
        codecs (str):
            Codecs for the rendition. If set, only
            renditions with the exact value will match.
    """

    bitrate_bps: int = proto.Field(
        proto.INT32,
        number=1,
    )
    codecs: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
